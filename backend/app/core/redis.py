"""异步 Redis 客户端（带内存缓存降级与懒初始化机制）。"""

import asyncio
import logging
import time
from typing import Optional, Any
import redis.asyncio as aioredis

from app.core.config import settings

logger = logging.getLogger("uvicorn")

# 全局缓存客户端实例与并发锁
_redis: Any = None
_redis_lock = asyncio.Lock()


class MemoryCacheAdapter:
    """
    基于 Python 内存字典实现的异步缓存适配器
    完美对齐 aioredis 的常用 API（支持 get, set, setex, delete, incr, decr, aclose 等）
    """

    def __init__(self, maxsize: int = 1024, ttl: int = 600):
        self._cache = {}
        # 为内存计数器/操作引入独立的异步锁，确保并发安全
        self._lock = asyncio.Lock()
        self.default_ttl = ttl
        self.maxsize = maxsize
        logger.info(f"实例化内存缓存降级适配器 (Maxsize: {maxsize}, 默认 TTL: {ttl}s)")

    async def get(self, key: str) -> Optional[Any]:
        """获取缓存，如果过期则自动清理并返回 None"""
        async with self._lock:
            if key not in self._cache:
                return None

            value, expire_at = self._cache[key]

            # 检查是否过期 (expire_at 为 None 表示永不过期)
            if expire_at is not None and time.time() > expire_at:
                del self._cache[key]  # 惰性删除
                return None

            return value

    async def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """对齐 Redis 的 set 方法，支持 ex 参数"""
        ttl = ex if ex is not None else self.default_ttl
        return await self._set_with_ttl(key, value, ttl)

    async def setex(self, name: str, time_to_live: int, value: Any) -> bool:
        """完全对齐 Redis 的 setex 方法"""
        return await self._set_with_ttl(name, value, time_to_live)

    async def _set_with_ttl(self, key: str, value: Any, ttl: int) -> bool:
        """内部公共写入逻辑，包含基础的容量 FIFO 淘汰策略"""
        async with self._lock:
            if len(self._cache) >= self.maxsize and key not in self._cache:
                first_key = next(iter(self._cache))
                del self._cache[first_key]

            expire_at = time.time() + ttl if ttl is not None and ttl > 0 else None
            self._cache[key] = (value, expire_at)
            return True

    async def delete(self, key: str) -> bool:
        """对齐 Redis 的 delete 方法"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    async def incr(self, name: str, amount: int = 1) -> int:
        """
        💡 补齐：对齐 Redis 的 incr 方法（原子自增）
        如果 key 不存在，则默认从 0 开始自增
        """
        async with self._lock:
            # 先复用内部逻辑检查并获取当前值（防过期）
            current_val = 0
            if name in self._cache:
                val, expire_at = self._cache[name]
                if expire_at is None or time.time() <= expire_at:
                    try:
                        current_val = int(val)
                    except (TypeError, ValueError):
                        current_val = 0
                else:
                    # 已过期则清理
                    del self._cache[name]

            new_val = current_val + amount
            # 保留原有的过期时间（如果之前存在的话），否则使用默认 TTL
            expire_at = self._cache[name][1] if name in self._cache else (
                time.time() + self.default_ttl if self.default_ttl else None)

            self._cache[name] = (new_val, expire_at)
            return new_val

    async def decr(self, name: str, amount: int = 1) -> int:
        """💡 补齐：对齐 Redis 的 decr 方法（原子自减）"""
        return await self.incr(name, -amount)

    async def aclose(self) -> None:
        """对齐 Redis 的异步关闭方法"""
        async with self._lock:
            self._cache.clear()
            logger.info("🔒 内存缓存适配器已清理关闭")


async def get_redis() -> Any:
    """
    获取或懒初始化缓存客户端：
    1. 优先尝试连接真实 Redis 并发送 ping 校验。
    2. 如果 Redis 连不上或配置错误，自动降级并返回内存缓存适配器实例。
    """
    global _redis
    if _redis is None:
        async with _redis_lock:
            if _redis is None:
                # 1. 尝试初始化 Redis 客户端
                redis_client = aioredis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                    max_connections=100,
                )
                try:
                    # 2. 强制发送 PING 验证连接是否真实可用
                    await redis_client.ping()
                    logger.info("✅ Redis 连接成功，当前使用 Redis 缓存服务。")
                    _redis = redis_client
                except (aioredis.ConnectionError, aioredis.TimeoutError, Exception) as e:
                    # 3. 连接失败，平滑降级到内存缓存适配器
                    # logger.warning(f"⚠️ Redis 连接失败 ({e})。自动降级为内存缓存方案 (MemoryCacheAdapter)...")
                    logger.warning(f"⚠️ Redis 连接失败。自动降级为内存缓存方案 (MemoryCacheAdapter)...")
                    _redis = MemoryCacheAdapter(
                        maxsize=getattr(settings, "CACHE_MAXSIZE", 1024),
                        ttl=getattr(settings, "CACHE_TTL", 600)
                    )
    return _redis


async def close_redis() -> None:
    """关闭缓存连接池（应用 shutdown 时调用）。"""
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None
        logger.info("🔒 缓存连接已安全关闭")


# import asyncio
# import redis.asyncio as aioredis
#
# from app.core.config import settings
#
# _redis: aioredis.Redis | None = None
# _redis_lock = asyncio.Lock()
#
#
# async def get_redis() -> aioredis.Redis:
#     """获取或懒初始化 Redis 连接（使用 Lock 防止并发重复创建）。"""
#     global _redis
#     if _redis is None:
#         async with _redis_lock:
#             if _redis is None:
#                 _redis = aioredis.from_url(
#                     settings.REDIS_URL,
#                     encoding="utf-8",
#                     decode_responses=True,  # 响应解码为 str
#                     max_connections=100,    # 连接池上限，超出排队等待而非无限新建
#                 )
#     return _redis
#
#
# async def close_redis() -> None:
#     """关闭 Redis 连接池（应用 shutdown 时调用）。"""
#     global _redis
#     if _redis is not None:
#         await _redis.aclose()
#         _redis = None

