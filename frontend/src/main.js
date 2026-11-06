import { createApp } from "vue";
import App from "./App.vue";

import AppIcon from "@/components/Icon/index.vue";

import "element-plus/theme-chalk/dark/css-vars.css";
import "@/styles/index.scss";
import "uno.css";
import "animate.css";

import { setupDirective } from "@/directives";
import { setupRouter } from "@/router";
import { setupStore } from "@/stores";
import { setupI18n } from "@/lang";
import { setupFormCreate } from "@/plugins/form-create";
import * as ElementPlusIcons from "@element-plus/icons-vue";
import { setupPermissionGuard } from "@/router/guards/permission";
import { setupSse } from "@/composables";

const app = createApp(App);

setupDirective(app); // 1. 注册自定义指令（权限等）
setupI18n(app); // 2. 注册国际化
setupRouter(app); // 3. 注册路由
setupStore(app); // 4. 注册 Pinia 状态管理
setupFormCreate(app); // 5. 注册 FormCreate 动态表单
// 全局注册 Element Plus 图标
Object.entries(ElementPlusIcons).forEach(([name, comp]) => app.component(name, comp));
// 全局注册自定义图标组件
app.component("AppIcon", AppIcon);

setupPermissionGuard(); // 6. 安装路由守卫（登录拦截 + 动态路由）
setupSse(); // 7. 安装 SSE（服务端推送）事件监听

app.mount("#app");
