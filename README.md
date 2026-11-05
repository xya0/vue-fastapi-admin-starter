





# 全栈项目框架

一个基于 Vue 3 + FastAPI 的全栈项目框架，使用 Python 3.11+ 和最新的前端技术。

## 技术栈

<table>
  <thead>
    <tr>
      <th style="white-space: nowrap;">架&nbsp;构</th>
      <th style="white-space: nowrap;">技术组件</th>
      <th style="white-space: nowrap;">描述 / 作用</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>后&nbsp;端</strong></td>
      <td><strong>FastAPI</strong> / <strong>Pydantic v2</strong> / <strong>Uvicorn</strong> / <strong>SQLAlchemy 2.0</strong> / <strong>Python-Jose</strong></td>
      <td>现代高性能框架，集成数据验证、ASGI服务、ORM预留及JWT认证。</td>
    </tr>
    <tr>
      <td><strong>前&nbsp;端</strong></td>
      <td><strong>Vue 3</strong> / <strong>Vite 6</strong> / <strong>Vue Router 4</strong> / <strong>Pinia</strong> / <strong>Axios</strong> / <strong>TypeScript</strong></td>
      <td>基于组合式API与TS类型安全的现代前端流，含高效构建、路由、状态管理及网络请求。</td>
    </tr>
  </tbody>
</table>

| 架构     | 技术组件                                                     | 描述 / 作用                                                  |
| :------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **后端** | **FastAPI** / **Pydantic v2** / **Uvicorn** / **SQLAlchemy 2.0** / **Python-Jose** | 现代高性能框架，集成数据验证、ASGI服务、ORM预留及JWT认证。   |
| **前端** | **Vue 3** / **Vite 6** / **Vue Router 4** / **Pinia** / **Axios** / **TypeScript** | 基于组合式API与TS类型安全的现代前端流，含高效构建、路由、状态管理及网络请求。 |

## 项目结构

```
vue-python-framework/
├── frontend/                 # Vue 3 前端项目
│   ├── src/
│   │   ├── assets/          # 静态资源
│   │   ├── components/      # Vue 组件
│   │   ├── layouts/         # 布局组件
│   │   ├── pages/           # 页面组件
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── types/           # TypeScript 类型
│   │   ├── utils/           # 工具函数
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
└── backend/                 # FastAPI 后端项目
    ├── api/
    │   └── v1/             # API v1 路由
    ├── core/               # 核心配置
    ├── models/             # 数据模型 (预留)
    ├── schemas/            # Pydantic 模型
    ├── services/           # 业务逻辑 (预留)
    ├── utils/              # 工具函数
    ├── main.py             # 入口文件
    └── pyproject.toml
```

## 快速开始

### 后端启动

- UV

```
uv sync
copy .env.example .env
uv run uvicorn app.main:app --reload
```

- pip + venv

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -e .

# 复制环境变量配置
cp .env.example .env

# 启动开发服务器
python main.py
# 或者
uvicorn core.app:app --reload
```

后端运行在 http://localhost:8000

### 前端启动

```bash
# 进入前端目录
cd frontend
# 安装依赖
npm install
# 启动开发服务器
npm run dev

# --- 或者 ---
npx vite --port=4000
```

前端运行在 http://localhost:5173

### API 文档

启动后端后访问：

- Swagger UI: http://localhost:8000/docs
- ~~ReDoc: http://localhost:8000/redoc~~

## 环境变量

后端 `.env` 配置：

| 变量           | 说明       | 默认值                  |
| -------------- | ---------- | ----------------------- |
| `APP_NAME`     | 应用名称   | Vue-Python API          |
| `DEBUG`        | 调试模式   | true                    |
| `HOST`         | 服务器地址 | 0.0.0.0                 |
| `PORT`         | 服务器端口 | 8000                    |
| `DATABASE_URL` | 数据库连接 | sqlite:///./data/app.db |
| `SECRET_KEY`   | JWT 密钥   | (需修改)                |

## 开发指南

### 添加新的 API 端点

1. 在 `backend/api/v1/` 目录创建新的路由文件
2. 在 `schemas/` 目录定义 Pydantic 模型
3. 在 `backend/api/v1/__init__.py` 注册路由

### 添加新的前端页面

1. 在 `frontend/src/pages/` 创建 Vue 组件
2. 在 `frontend/src/router/index.ts` 添加路由
3. 在 `frontend/src/types/index.ts` 添加类型定义

## 生产构建

### 前端构建

```bash
cd frontend
npm run build
```

### 后端部署

推荐使用 Gunicorn + Uvicorn workers：

```bash
pip install gunicorn
gunicorn core.app:app -w 4 -k uvicorn.workers.UvicornWorker
```



## Acknowledgments / References

本项目的开发离不开以下优秀开源项目的启发或支持：
- [Vue3 + Vite + TypeScript 企业级中后台前端](https://github.com/youlaitech/vue3-element-admin) 
- https://gitee.com/youlaiorg/youlai-fastapi

- https://deepwiki.com/youlaitech/vue3-element-admin