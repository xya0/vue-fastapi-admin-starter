<template>
  <span
    v-if="isLocalSvg"
    class="icon-component"
    :class="[`i-svg:${localIconName}`, props.className]"
    :style="iconStyle"
    aria-hidden="true"
  />

  <el-icon v-else-if="isElementIcon" :size="size" :color="color" :style="iconStyle">
    <component :is="elementIconName" />
  </el-icon>

  <IconifyIcon
    v-else-if="resolvedIconify"
    :icon="resolvedIconify"
    :width="size"
    :height="size"
    :color="color"
    :style="iconStyle"
    aria-hidden="true"
  />

  <span
    v-else
    class="icon-component icon-component--fallback"
    :style="iconStyle"
    aria-hidden="true"
  >
    ?
  </span>
</template>

<script setup>
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import { Icon as IconifyIcon } from "@iconify/vue";

const props = defineProps({
  name: {
    type: String,
    default: "",
  },
  size: {
    type: [Number, String],
    default: "1em",
  },
  color: {
    type: String,
    default: "currentColor",
  },
  type: {
    type: String,
    default: "auto",
    validator: (value) => ["auto", "svg", "element", "iconify"].includes(value),
  },
  className: {
    type: String,
    default: "",
  },
});

const normalizedName = computed(() => String(props.name || "").trim());

const hasIconifyPrefix = computed(() => /^[a-z0-9-]+:/i.test(normalizedName.value));

const elementIconName = computed(() => {
  const rawName = normalizedName.value.replace(/^el:|^element-plus:/i, "").trim();
  if (!rawName) return "";

  if (ElementPlusIconsVue[rawName]) return rawName;

  const normalized = rawName.charAt(0).toUpperCase() + rawName.slice(1);
  return ElementPlusIconsVue[normalized] ? normalized : "";
});

const isElementIcon = computed(() => {
  if (props.type === "element") return !!elementIconName.value;
  if (props.type === "svg" || props.type === "iconify") return false;
  return !!elementIconName.value || /^el:|^element-plus:/i.test(normalizedName.value);
});

const localIconName = computed(() => {
  const name = normalizedName.value.replace(/^svg:/i, "");
  return name.replace(/^el:|^element-plus:/i, "").replace(/^iconify:/i, "");
});

const isLocalSvg = computed(() => {
  if (!normalizedName.value) return false;
  if (props.type === "svg") return true;
  if (props.type === "element" || props.type === "iconify") return false;
  return !hasIconifyPrefix.value && !elementIconName.value && !!localIconName.value;
});

const resolvedIconify = computed(() => {
  if (props.type === "iconify") return normalizedName.value;
  if (props.type === "svg" || props.type === "element") return "";
  return hasIconifyPrefix.value ? normalizedName.value : "";
});

const iconStyle = computed(() => ({
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  width: typeof props.size === "number" ? `${props.size}px` : props.size,
  height: typeof props.size === "number" ? `${props.size}px` : props.size,
  color: props.color,
  flexShrink: 0,
}));

defineOptions({
  name: "AppIcon",
  inheritAttrs: false,
});
</script>

<style scoped lang="scss">
.icon-component {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.icon-component--fallback {
  font-size: 12px;
  font-weight: 700;
  color: var(--el-text-color-secondary);
}
</style>
