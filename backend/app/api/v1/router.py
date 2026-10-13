from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.auth.qr_code import router as qr_code_router
from app.modules.rbac.user.router import router as user_router
from app.modules.rbac.role.router import router as role_router
from app.modules.rbac.menu.router import router as menu_router
from app.modules.rbac.dept.router import router as dept_router
from app.modules.dict.router import router as dict_router
from app.modules.config.router import router as config_router
from app.modules.notice.router import router as notice_router
from app.modules.log.router import router as log_router
from app.modules.tool.file.router import router as file_router
from app.modules.tool.codegen.router import router as codegen_router
from app.modules.tool.wxma.router import router as wxma_router
from app.modules.tool.sse.router import router as sse_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(qr_code_router)
router.include_router(user_router)
router.include_router(role_router)
router.include_router(menu_router)
router.include_router(dept_router)
router.include_router(dict_router)
router.include_router(config_router)
router.include_router(notice_router)
router.include_router(log_router)
router.include_router(file_router)
router.include_router(codegen_router)
router.include_router(wxma_router)
router.include_router(sse_router)
