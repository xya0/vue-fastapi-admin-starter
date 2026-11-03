<template>
  <el-button text @click="toggleTheme" aria-label="切换主题" circle>
    <el-icon :size="20">
      <component :is="currentThemeIcon" />
    </el-icon>
  </el-button>
</template>

<script setup>
import { useSettingsStore } from "@/stores";
import { ThemeMode } from "@/enums";
import { Moon, Sunny } from "@element-plus/icons-vue";

const settingsStore = useSettingsStore();

const currentThemeIcon = computed(() => {
  return settingsStore.resolvedTheme === ThemeMode.DARK ? Moon : Sunny;
});

const toggleTheme = () => {
  // 若当前为自动（AUTO），以 resolvedTheme 为基准切换至相反主题；否则在 LIGHT/DARK 间切换
  const isDark = settingsStore.resolvedTheme === ThemeMode.DARK;
  settingsStore.theme = isDark ? ThemeMode.LIGHT : ThemeMode.DARK;
};
</script>
