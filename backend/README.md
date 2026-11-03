<div align="center">


**FastAPI 企业级权限管理系统后端（Python）**



## 项目简介

**youlai-fastapi** 是一套基于 Python（FastAPI + SQLAlchemy 2.0 + PostgreSQL）的企业级权限管理系统后端，配套前端 [vue3-element-admin](https://gitee.com/youlaiorg/vue3-element-admin) 和移动端 [youlai-app](https://gitee.com/youlaiorg/youlai-app)，并提供 **7 种语言实现**（Java / Node.js / Go / Python / PHP / C# / Rust），共享同一套 API 规范与数据库结构。适用于 Python 技术栈团队的企业中后台学习与二次开发。完整接口文档见 [Apifox](https://www.apifox.cn/apidoc/shared-195e783f-4d85-4235-a038-eec696de4ea5)。

## 核心特性

- 🔐 **安全体系** — PyJWT + bcrypt + Redis Token，支持令牌签发、续期与多端会话
- 🛡️ **细粒度权限** — RBAC 数据 / 菜单 / 按钮 / 接口级，数据权限五档
- ⚡ **代码生成器** — 一键生成前后端 CRUD 代码（codegen 模块）
- 📦 **模块齐全** — 用户、角色、菜单、部门、字典、配置、文件、通知、操作日志
- 🌐 **多语言生态** — 与其它语言版本共享 API 规范与数据库结构
- 🔌 **实时通信** — SSE 推送：在线用户数、字典同步、通知广播



## 快速开始

**环境要求**：Python 3.11+ · uv · PostgreSQL 16+ · Redis 7.x（生产）

> 测试/本地开发可直接使用 SQLite，不需要安装 PostgreSQL。SQLite 使用 `sqlite+aiosqlite`，初始化脚本位于 `sql/sqlite/youlai-admin.sql`。

1. 克隆项目：
   ```bash
   git clone https://github.com/youlaitech/youlai-fastapi.git
   ```

2. 使用 uv 创建环境并安装依赖：
   ```bash
   uv sync --all-extras
   ```

   Windows PowerShell 也可直接使用：
   ```powershell
   uv sync --all-extras
   ```

3. 初始化 SQLite 测试数据库（推荐本地开发）：
   ```bash
   uv run python scripts/init_sqlite.py
   ```

   使用测试配置启动：
   ```bash
   # Linux/macOS
   ENV_FILE=.env.test uv run fastapi dev app/main.py
   
   # Windows PowerShell
   $env:ENV_FILE = ".env.test"
   uv run fastapi dev app/main.py
   ```

   SQLite 初始化脚本 `sql/sqlite/youlai-admin.sql` 已包含建表、索引和完整测试种子数据。

4. 生产环境使用 PostgreSQL：
   ```bash
   psql -d youlai_admin -f sql/postgresql/youlai-admin.sql
   ```

5. 启动服务：

   **方式一：PyCharm / VS Code 启动（推荐）**
   用 PyCharm 或 VS Code 打开项目并选中虚拟环境，运行 `app/main.py` 或 `fastapi dev` 任务即可。

   **方式二：命令行启动**
   ```bash
   fastapi dev app/main.py
   ```
   启动后访问 [http://localhost:8000/docs](http://localhost:8000/docs)，能打开接口文档即说明后端已正常运行。

6. 启动前端（可选）：
   如需可视化操作界面，启动配套前端 [vue3-element-admin](https://gitee.com/youlaiorg/vue3-element-admin)，访问 [http://localhost:3000](http://localhost:3000)，使用 `admin` / `123456` 登录。

## 目录结构

> 按业务域组织，每个域自包含 `router/schemas/models/service`，参考 [zhanymkanov/fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)。

```text
youlai-fastapi/
├── app/
│   ├── api/              # API 聚合与版本管理
│   ├── core/             # 配置、数据库、安全、中间件、Redis
│   ├── common/           # 通用响应、分页、枚举、常量
│   └── modules/          # 业务领域模块
│       ├── auth/         # 认证
│       ├── rbac/         # 用户、角色、菜单、部门
│       ├── config/
│       ├── dict/
│       ├── notice/
│       ├── log/
│       └── tool/         # 文件、代码生成、SSE 等
├── alembic/              # 数据库迁移
├── scripts/              # 初始化/运维脚本
├── sql/
│   ├── postgresql/       # 生产数据库脚本
│   └── sqlite/           # 测试数据库脚本
├── tests/
├── .env                  # 本地/生产环境变量
├── .env.test             # SQLite 测试环境
├── pyproject.toml        # uv/Python 项目依赖定义
└── uv.lock               # uv 锁定依赖版本（联网执行 uv lock 后生成）
```



