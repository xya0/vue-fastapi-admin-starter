from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse

from app.api.v1.router import router as v1_router

# router = APIRouter()
# router.include_router(v1_router, prefix="/v1")


def register_api(app: FastAPI) -> None:
    """
    注册路由
    """
    # -------------------------------------------------------------
    # 模块化路由注册
    # -------------------------------------------------------------
    app.include_router(v1_router, prefix="/api/v1")  # tags=["Version 1"]

    # -------------------------------------------------------------
    # 基础与系统级路由注册
    # -------------------------------------------------------------
    # 创建一个独立的路由组，用于存放服务自带的系统级或根路径接口
    router = APIRouter()

    @router.get("/health", tags=["系统"], summary="健康检查")
    async def health_check():
        return {"status": "ok", "service": "fastapi"}

    @router.get("/", response_class=HTMLResponse, tags=['系统'], summary="根目录")
    def root():
        html_content = """
        <html>
            <body>
                <h2>Welcome to My FastAPI Project</h2>
                <p>Visit <a href="/docs">/docs</a> for API documentation.</p>
            </body>
        </html>
        """
        return html_content

    # 将上述定义的系统级路由（根路径和健康检查）正式注册到 FastAPI 实例中
    app.include_router(router)

