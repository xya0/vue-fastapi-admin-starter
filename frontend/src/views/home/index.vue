<template>
  <div class="dash">
    <section class="dash-header">
      <div class="card dash-header__card">
        <div class="dash-header__start">
          <div class="dash-avatar">
            <img v-if="userStore.userInfo.avatar" :src="userStore.userInfo.avatar" alt="" />
            <el-icon v-else :size="22"><User /></el-icon>
          </div>
          <div class="dash-header__text">
            <h1 class="dash-header__greeting">{{ greetings }}</h1>
            <p class="dash-header__date">{{ currentDateStr }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>

  <div class="page-container">
    <el-card class="page-content" shadow="never">
      <section v-for="group in appGroups" :key="group.category.key" class="app-section">
        <header class="app-section__header">
          <span class="app-section__name">{{ group.category.name }}</span>
          <span class="app-section__count">{{ group.apps.length }}</span>
          <span class="app-section__desc">{{ group.category.description }}</span>
        </header>

        <div class="app-grid">
          <div
            v-for="app in group.apps"
            :key="app.name"
            class="app-card"
            :class="[`app-card--${app.theme}`, { 'is-disabled': !app.ssoReady && !app.url }]"
            @click="handleAppClick(app)"
          >
            <div class="app-card__icon">
              <app-icon :name="app.icon" size="22" />
              <!-- <el-icon :size="22">
                <component :is="app.icon" />
              </el-icon> -->
            </div>
            <div class="app-card__body">
              <div class="app-card__name">{{ app.name }}</div>
              <div class="app-card__desc">{{ app.description }}</div>
            </div>
            <el-icon v-if="app.ssoReady || app.url" class="app-card__arrow">
              <ArrowRight />
            </el-icon>
          </div>
        </div>
      </section>
    </el-card>
  </div>
</template>

<script setup>
import { ArrowRight } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import { appConfig } from "@/settings";

defineOptions({ name: "Dashboard", inheritAttrs: false });

import { useUserStore } from "@/stores/user";
import { User } from "@element-plus/icons-vue";
import App from "@/App.vue";

const userStore = useUserStore();

const hours = new Date().getHours();
const greetings = computed(() => {
  const n = userStore.userInfo.nickname;
  if (hours >= 6 && hours < 8) return `早安，${n}`;
  if (hours >= 8 && hours < 12) return `上午好，${n}`;
  if (hours >= 12 && hours < 18) return `下午好，${n}`;
  if (hours >= 18 && hours < 24) return `晚上好，${n}`;
  return `夜深了，${n}`;
});

const currentDateStr = computed(() => {
  const d = new Date();
  const w = ["日", "一", "二", "三", "四", "五", "六"];
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日 星期${w[d.getDay()]}`;
});

// ===========================================================
/** 分类清单，数组顺序即页面分组顺序 */
const categories = [
  {
    key: "agent",
    name: "AI工具",
    description: "智能助手、工作流与多智能体",
  },
  {
    key: "smart",
    name: "智能与多端",
    description: "AI办公与多端应用",
  },
];

/** 应用清单：接入统一认证的应用补上 url 并置 ssoReady 为 true */
const apps = [
  {
    name: "Google AI搜索",
    description: "利用Google 搜索中的AI 模式获取AI 生成的回答",
    url: "https://www.google.com/ai",
    icon: "ri:google-fill",
    theme: "primary",
    ssoReady: true,
    category: "agent",
  },
  {
    name: "百度文心",
    description: "百度旗下全能AI 助手",
    url: "https://wenxin.baidu.com/",
    icon: "ri:baidu-fill",
    theme: "success",
    ssoReady: false,
    category: "agent",
  },
  {
    name: "DeepSeek",
    description: "探索未至之境",
    url: "https://www.deepseek.com/",
    icon: "ri:deepseek-fill",
    theme: "warning",
    ssoReady: false,
    category: "agent",
  },

  {
    name: "WorkBuddy",
    description: "全场景 AI 办公工作台",
    url: "https://www.workbuddy.cn/",
    icon: "ri:ai",
    theme: "info",
    ssoReady: false,
    category: "smart",
  },
];

const router = useRouter();

const appGroups = categories
  .map((category) => ({ category, apps: apps.filter((app) => app.category === category.key) }))
  // 未启用统一认证时不展示账号分组
  .filter(
    (group) => group.apps.length > 0 && (appConfig.oidcEnabled || group.category.key !== "account")
  );

// 站内路径走路由跳转，外部地址新标签打开
function handleAppClick(app) {
  // 未接入统一认证且没有入口的应用只作展示
  if (!app.ssoReady && !app.url) {
    ElMessage.info(`${app.name} 尚未接入统一认证`);
    return;
  }
  if (/^https?:\/\//.test(app.url)) {
    window.open(app.url, "_blank", "noopener");
    return;
  }
  // 统一认证授权地址需要整页跳转，由后端重定向到认证中心
  if (app.url.startsWith("/oauth2/")) {
    window.location.href = app.url;
    return;
  }
  router.push(app.url);
}
</script>

<style lang="scss" scoped>
$gap: 12px;
$pad: 10px;

.card {
  overflow: hidden;
  background: var(--el-bg-color-overlay);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
}

.dash {
  display: flex;
  flex-direction: column;
  gap: $gap;
  padding: $pad;
  background: var(--page-bg);
}

.dash-header {
  &__card {
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    align-items: center;
    justify-content: space-between;
    min-height: 78px;
    padding: 16px 18px;
  }
  &__start {
    display: flex;
    flex: 1;
    gap: 12px;
    align-items: center;
    min-width: 260px;
  }
  &__text {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }
  &__greeting {
    margin: 0;
    font-size: 18px;
    font-weight: 500;
    line-height: 1.3;
    color: var(--el-text-color-primary);
  }
  &__date {
    margin: 0;
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }
}

.dash-avatar {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  overflow: hidden;
  color: var(--el-color-primary);
  background: color-mix(in srgb, var(--el-color-primary) 14%, var(--el-bg-color-overlay));
  border: 1px solid color-mix(in srgb, var(--el-color-primary) 18%, transparent);
  border-radius: 50%;
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.dash-bottom {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $gap;
}

.todo-row {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 11px 0;
  & + & {
    border-top: 1px solid var(--el-border-color-lighter);
  }
  &--done {
    .todo-row__title {
      color: var(--el-text-color-placeholder);
      text-decoration: line-through;
    }
  }
  &__icon--pending {
    flex-shrink: 0;
    color: var(--el-color-primary);
  }
  &__icon--done {
    flex-shrink: 0;
    color: var(--el-color-success);
  }
  &__title {
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 13px;
    color: var(--el-text-color-regular);
    white-space: nowrap;
  }
  &__tag {
    flex-shrink: 0;
    color: var(--el-text-color-secondary);
    background: var(--el-fill-color-light);
    &.el-tag--warning {
      color: color-mix(in srgb, var(--el-color-warning) 78%, var(--el-text-color-primary));
      background: color-mix(in srgb, var(--el-color-warning) 9%, var(--el-bg-color-overlay));
    }
    &.el-tag--success {
      color: var(--el-color-success);
      background: color-mix(in srgb, var(--el-color-success) 8%, var(--el-bg-color-overlay));
    }
  }
  &__time {
    flex-shrink: 0;
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }
}

.feed {
  display: flex;
  flex-direction: column;
  padding: 10px 20px 16px;
  &__item {
    position: relative;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: baseline;
    padding: 10px 0 10px 16px;
    &::before {
      position: absolute;
      top: 22px;
      bottom: -4px;
      left: 3px;
      width: 1px;
      content: "";
      background: var(--el-border-color-lighter);
    }
    &:last-child::before {
      display: none;
    }
  }
  &__dot {
    position: absolute;
    top: 12px;
    left: 0;
    width: 7px;
    height: 7px;
    background: var(--el-color-primary);
    border: 2px solid var(--el-color-primary-light-8);
    border-radius: 50%;
  }
  &__text {
    flex: 1;
    min-width: 0;
    font-size: 13px;
    line-height: 1.4;
    color: var(--el-text-color-regular);
  }
  &__time {
    flex-shrink: 0;
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }
}

@media (max-width: 1200px) {
  .dash-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  .dash-header__card {
    flex-direction: column;
    align-items: flex-start;
  }
  .dash-header__end {
    justify-content: flex-start;
  }
}
@media (max-width: 992px) {
  .dash-chart {
    grid-template-columns: 1fr;
  }
  .dash-bottom {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 768px) {
  .dash {
    gap: 10px;
    padding: 10px;
  }
  .dash-stats {
    grid-template-columns: 1fr;
  }
}

/* 分组按内容高度排列，不占用页面剩余高度 */
.page-container {
  flex: 0 0 auto;
  width: 100%;
  height: auto;
  padding: 8px 12px 16px;
}

.page-content :deep(.el-card__body) {
  grid-template-rows: none;
  grid-auto-rows: min-content;
  align-content: start;
}

.app-section + .app-section {
  padding-top: 24px;
  margin-top: 24px;
  border-top: 1px solid var(--el-border-color-extra-light);
}

.app-section__header {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: baseline;
  margin-bottom: 16px;
}

.app-section__name {
  position: relative;
  padding-left: 10px;
  font-size: 15px;
  font-weight: 600;
  color: var(--el-text-color-primary);

  &::before {
    position: absolute;
    top: 50%;
    left: 0;
    width: 3px;
    height: 14px;
    content: "";
    background: var(--el-color-primary);
    border-radius: 2px;
    transform: translateY(-50%);
  }
}

.app-section__count {
  padding: 0 6px;
  font-size: 12px;
  line-height: 16px;
  color: var(--el-text-color-secondary);
  background: var(--el-fill-color-light);
  border-radius: 8px;
}

.app-section__desc {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.app-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 14px;
}

.app-card {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: 16px;
  cursor: pointer;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 10px;
  transition:
    border-color 0.2s,
    box-shadow 0.2s,
    transform 0.2s;

  &:hover {
    border-color: var(--app-border);
    box-shadow: 0 6px 16px rgb(0 0 0 / 6%);
    transform: translateY(-2px);

    .app-card__arrow {
      color: var(--app-color);
      transform: translateX(2px);
    }
  }

  &.is-disabled {
    cursor: not-allowed;

    .app-card__icon {
      opacity: 0.75;
      filter: saturate(0.7);
    }

    .app-card__name {
      color: var(--el-text-color-regular);
    }

    &:hover {
      border-color: var(--el-border-color-lighter);
      box-shadow: none;
      transform: none;
    }
  }

  &__icon {
    display: flex;
    flex-shrink: 0;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    color: var(--app-color);
    background: var(--app-bg);
    border-radius: 10px;
  }

  &__body {
    flex: 1;
    min-width: 0;
  }

  &__name {
    font-size: 15px;
    font-weight: 600;
    line-height: 22px;
    color: var(--el-text-color-primary);
  }

  &__desc {
    display: -webkit-box;
    margin-top: 6px;
    overflow: hidden;
    font-size: 12px;
    line-height: 1.7;
    color: var(--el-text-color-secondary);
    -webkit-box-orient: vertical;
  }

  &__arrow {
    flex-shrink: 0;
    align-self: center;
    font-size: 14px;
    color: var(--el-text-color-placeholder);
    transition:
      color 0.2s,
      transform 0.2s;
  }
}

.app-card--primary {
  --app-color: var(--el-color-primary);
  --app-bg: var(--el-color-primary-light-9);
  --app-border: var(--el-color-primary-light-5);
}

.app-card--success {
  --app-color: var(--el-color-success);
  --app-bg: var(--el-color-success-light-9);
  --app-border: var(--el-color-success-light-5);
}

.app-card--warning {
  --app-color: var(--el-color-warning);
  --app-bg: var(--el-color-warning-light-9);
  --app-border: var(--el-color-warning-light-5);
}

.app-card--info {
  --app-color: var(--el-color-info);
  --app-bg: var(--el-color-info-light-9);
  --app-border: var(--el-color-info-light-5);
}
</style>
