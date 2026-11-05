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
</template>

<script setup>
defineOptions({ name: "Dashboard", inheritAttrs: false });

import { useUserStore } from "@/stores/user";
import { User } from "@element-plus/icons-vue";

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
</style>
