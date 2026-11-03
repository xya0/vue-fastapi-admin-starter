"""文档认证及路由"""

import os
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(tags=["API Documentation"])

security = HTTPBasic()

DOCS_USERNAME = os.getenv("DOCS_USERNAME", "admin")
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD", "ChangeMe123!")


# ==========================================
# 文档访问认证
# ==========================================

def verify_docs_auth(
    credentials: HTTPBasicCredentials = Depends(security),
):
    username_ok = secrets.compare_digest(
        credentials.username.encode("utf-8"),
        DOCS_USERNAME.encode("utf-8"),
    )

    password_ok = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        DOCS_PASSWORD.encode("utf-8"),
    )

    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid documentation credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


# ==========================================
# OpenAPI JSON
# ==========================================

def get_openapi_schema():
    from app.main import app
    return app.openapi()


@router.get("/openapi.json", include_in_schema=False)
async def openapi_json(
    _: str = Depends(verify_docs_auth),
):
    return get_openapi_schema()


# ==========================================
# Swagger UI
# ==========================================

@router.get("/docs", include_in_schema=False)
async def swagger_docs(
    _: str = Depends(verify_docs_auth),
):
    from app.main import app

    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Swagger UI",
    )


# ==========================================
# ReDoc
# ==========================================

@router.get("/redoc", include_in_schema=False)
async def redoc_docs(
    _: str = Depends(verify_docs_auth),
):
    from app.main import app

    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - ReDoc",
    )

