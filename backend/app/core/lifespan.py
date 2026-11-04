from loguru import logger
from contextlib import asynccontextmanager
from fastapi import FastAPI
import redis.asyncio as aioredis
from app.core.config import settings

# import logging
# logger = logging.getLogger("uvicorn")
REDIS_URL = settings.REDIS_URL


async def init_redis(app: FastAPI):
    """初始化并检测 Redis"""
    logger.info("🔄 正在检测 Redis 配置及连接状态...")
    try:
        # 创建连接池
        redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
        # 强制 PING 检测
        await redis_client.ping()
        logger.info("✅ Redis 连接成功，配置校验通过！")

        # 挂载到 app.state
        # app.state.redis = redis_client
    except (aioredis.ConnectionError, aioredis.TimeoutError) as e:
        # logger.error(f"❌ Redis 连接失败: {e}")
        logger.error(f"❌ Redis 连接失败: {type(e).__name__}")
        # 抛出系统异常，直接阻断 Uvicorn 启动
        # raise RuntimeError("项目启动失败：无法连接到 Redis 服务。")


async def close_redis(app: FastAPI):
    """关闭 Redis 连接"""
    if hasattr(app.state, "redis"):
        await app.state.redis.close()
        logger.info("🔒 Redis 连接已成功关闭")


@asynccontextmanager
async def register_lifespan(app: FastAPI):
    """
    统一的生命周期管理器
    未来如果有 MySQL、MongoDB 等，都可以写在这里面顺序执行
    """
    logger.info(f"fastapi starting | session_type={settings.SESSION_TYPE}")
    # ---- 【启动时执行】 ----
    await init_redis(app)
    # await init_db(app) # 示例：未来扩展其他中间件

    yield  # 运行阶段

    # ---- 【关闭时执行】 ----
    # await close_db(app)
    await close_redis(app)

    logger.info("fastapi shutdown complete")