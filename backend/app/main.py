"""FastAPI application entry point and application factory."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi_pagination import add_pagination
from loguru import logger

from app.api.router import router as api_router
from app.core.config import settings
from app.core.redis import close_redis
from app.core.middleware import setup_cors, RequestLogMiddleware, IpRateLimitMiddleware
from app.core.exceptions import (
    BusinessException,
    business_exception_handler,
    global_exception_handler,
    validation_exception_handler,
)
import app.core.registry  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and release them on shutdown."""
    logger.info(f"youlai-fastapi starting | session_type={settings.SESSION_TYPE}")
    yield
    await close_redis()
    logger.info("youlai-fastapi shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="youlai-fastapi",
        description="youlai-fastapi 企业级权限管理系统后端",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    setup_cors(app)
    app.add_middleware(RequestLogMiddleware)
    app.add_middleware(IpRateLimitMiddleware)

    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    add_pagination(app)

    @app.get("/health", tags=["系统"], summary="健康检查")
    async def health_check():
        return {"status": "ok", "service": "youlai-fastapi"}

    # 方式1：显式定义根路由处理函数
    # @app.get("/", summary="根目录", description="返回欢迎信息与项目基础状态")
    # async def root():
    #     return {
    #         "status": "success",
    #         "message": "Welcome to the API!",
    #         "docs_url": "/docs",  # 引导用户查看 Swagger 文档
    #     }

    # 方式2: 重定向到文档页面
    # @app.get("/", include_in_schema=False)  # include_in_schema=False 可在 API 文档中隐藏该重定向接口
    # async def redirect_to_docs():
    #     return RedirectResponse(url="/docs")

    # 方式3：
    @app.get("/", response_class=HTMLResponse)
    def read_root():
        html_content = """
        <html>
            <body>
                <h2>Welcome to My FastAPI Project</h2>
                <p>Visit <a href="/docs">/docs</a> for API documentation.</p>
            </body>
        </html>
        """
        return html_content

    app.include_router(api_router, prefix="/api")
    logger.info("All routers registered")
    return app


app = create_app()
