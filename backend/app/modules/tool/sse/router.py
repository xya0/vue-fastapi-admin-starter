"""SSE 路由。"""

from fastapi import APIRouter, Depends, Request

from app.core.dependencies import get_current_user
from app.modules.auth.schemas import SysUserDetails
from app.modules.tool.sse.manager import get_online_count, sse_connect
from app.common.response import Result

router = APIRouter(prefix="/sse", tags=["SSE推送"])


@router.get("/connect", summary="SSE 长连接")
async def connect(request: Request, user: SysUserDetails = Depends(get_current_user)):
    return await sse_connect(request, user.username or "")


@router.get("/online-count", summary="在线用户数")
async def online_count():
    return Result(data=await get_online_count())
