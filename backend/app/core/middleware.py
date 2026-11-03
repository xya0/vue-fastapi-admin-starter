"""全局中间件。"""

import time

from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.rate_limit import check_rate_limit
from app.core.exceptions import BusinessException


def setup_cors(app):
    # ALLOWED_ORIGINS 为 * 时放行所有来源（带凭据时浏览器不允许 *，故关闭 credentials）
    if settings.ALLOWED_ORIGINS.strip() == "*":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
            allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
            expose_headers=["Content-Disposition"],
            max_age=600,
        )
        return

    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://.*" if settings.DEBUG else settings.ALLOWED_ORIGINS or "http://localhost",
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        expose_headers=["Content-Disposition"],
        max_age=600,
    )


class RequestLogMiddleware(BaseHTTPMiddleware):
    """记录每一个 HTTP 请求的路由、响应状态码以及处理该请求所耗费的时间（响应时间）"""
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration_ms = int((time.time() - start) * 1000)
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)")
        return response


class IpRateLimitMiddleware(BaseHTTPMiddleware):
    """IP 全局滑动窗口限流（ZSet Lua 原子计数），Redis 异常时放行。"""

    async def dispatch(self, request: Request, call_next):
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)

        client_ip = (
            request.headers.get("x-forwarded-for", "").split(",")[0].strip()
            or request.headers.get("x-real-ip", "").strip()
            or (request.client.host if request.client else "unknown")
        )
        key = f"rate_limit:ip:{client_ip}"
        limit = settings.RATE_LIMIT_IP_LIMIT
        window = settings.RATE_LIMIT_IP_WINDOW
        try:
            count = await check_rate_limit(key, limit, window)
        except BusinessException as e:
            response = JSONResponse(
                status_code=e.http_status,
                content={"code": e.code, "msg": e.msg, "data": None},
            )
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + window)
            response.headers["Retry-After"] = str(window)
            return response

        response = await call_next(request)
        remaining = max(0, limit - (count or 0))
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + window)
        return response


def add_gzip_middleware(app: FastAPI):
    """
    添加gzip压缩中间件

    :param app: FastAPI对象
    :return:
    """
    from starlette.middleware.gzip import GZipMiddleware
    app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=9)


def register_middleware(app: FastAPI):
    """
    全局中间件处理
    """
    # 加载跨域中间件
    setup_cors(app)
    # 加载gzip压缩中间件
    add_gzip_middleware(app)
    # 其他中间件
    # app.add_middleware(RequestLogMiddleware)
    # app.add_middleware(IpRateLimitMiddleware)

