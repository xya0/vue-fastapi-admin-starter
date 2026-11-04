"""FastAPI application entry point and application factory."""

from fastapi import FastAPI

from fastapi_pagination import add_pagination
from scalar_fastapi import add_scalar_reference


from app.api.router import register_api
from app.core.lifespan import register_lifespan
from app.core.middleware import register_middleware
from app.core.exceptions import register_exception_handlers


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="FastAPI",
        description="企业级权限管理系统后端",
        version="1.0.0",
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
        lifespan=register_lifespan,
    )
    # 将 Scalar 注册到 /docs 路径
    add_scalar_reference(app, route="/docs")
    # 分页数据库查询
    add_pagination(app)
    # 中间件处理方法
    register_middleware(app)
    # 全局异常处理方法
    register_exception_handlers(app)
    # 注册API路由
    register_api(app)

    return app


app = create_app()
