# FastAPI 企业级权限管理系统 — 目录架构

本版本基于原 `youlai-fastapi` 项目进行生产级目录重构，核心原则是：

> 基础设施横向共享，业务领域纵向隔离。

## 目录

```text
app/
├── api/                         # HTTP API 聚合与版本管理
│   ├── router.py
│   └── v1/router.py
├── core/                        # 核心基础设施
│   ├── config.py                # 配置
│   ├── database.py              # SQLAlchemy
│   ├── dependencies.py          # FastAPI Depends
│   ├── exceptions.py            # 全局异常
│   ├── middleware.py            # 中间件
│   ├── rate_limit.py            # 限流
│   ├── redis.py                 # Redis
│   └── registry.py              # ORM 模型注册
├── common/                      # 跨业务通用能力
│   ├── constants.py
│   ├── enums.py
│   ├── pagination.py
│   ├── response.py
│   └── serializers.py
├── modules/                     # 业务领域模块
│   ├── auth/                    # 登录、Token、二维码
│   ├── captcha/                 # 验证码
│   ├── rbac/                    # 用户-角色-菜单/权限-部门
│   │   ├── user/
│   │   ├── role/
│   │   ├── menu/
│   │   └── dept/
│   ├── config/                  # 系统配置
│   ├── dict/                    # 字典
│   ├── notice/                  # 通知
│   ├── log/                     # 操作日志
│   └── tool/                    # 文件、代码生成、SSE、微信小程序
└── main.py
```

## 请求调用链

```text
HTTP Request
    ↓
app/api/v1/router.py
    ↓
modules/<domain>/router.py
    ↓
modules/<domain>/service.py
    ↓
modules/<domain>/repository.py（后续新增）
    ↓
SQLAlchemy Model
    ↓
Database
```

当前源码中部分历史模块尚未独立 Repository 层，因此保留现有 Service 直接访问 ORM 的实现，避免为了目录调整而改变业务行为。后续新增复杂业务时建议采用 `router → service → repository → model`。

## 主要迁移关系

| 原目录 | 新目录 |
|---|---|
| `app/config.py` | `app/core/config.py` |
| `app/database.py` | `app/core/database.py` |
| `app/dependencies.py` | `app/core/dependencies.py` |
| `app/exceptions.py` | `app/core/exceptions.py` |
| `app/middleware.py` | `app/core/middleware.py` |
| `app/redis.py` | `app/core/redis.py` |
| `app/registry.py` | `app/core/registry.py` |
| `app/constants.py` | `app/common/constants.py` |
| `app/pagination.py` | `app/common/pagination.py` |
| `app/response.py` | `app/common/response.py` |
| `app/serializers.py` | `app/common/serializers.py` |
| `app/auth` | `app/modules/auth` |
| `app/captcha` | `app/modules/captcha` |
| `app/system/user` | `app/modules/rbac/user` |
| `app/system/role` | `app/modules/rbac/role` |
| `app/system/menu` | `app/modules/rbac/menu` |
| `app/system/dept` | `app/modules/rbac/dept` |
| `app/system/config` | `app/modules/config` |
| `app/system/dict` | `app/modules/dict` |
| `app/system/notice` | `app/modules/notice` |
| `app/system/log` | `app/modules/log` |
| `app/tool` | `app/modules/tool` |

## API 版本

`main.py` 不再直接注册所有业务 Router，而是只挂载：

```python
app.include_router(api_router, prefix="/api")
```

由 `app/api/router.py` 管理版本，再由 `app/api/v1/router.py` 聚合业务模块。未来可以增加 `v2`，做到 API 版本与业务模块解耦。
