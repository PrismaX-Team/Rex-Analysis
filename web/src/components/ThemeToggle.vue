<template>
  <button
    type="button"
    class="theme-toggle"
    :aria-label="theme === 'dark' ? t('切换到浅色') : t('切换到深色')"
    :title="theme === 'dark' ? t('浅色') : t('深色')"
    @click="toggle"
  >
    <svg v-if="theme === 'dark'" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5" /><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8" /></svg>
    <svg v-else viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z" /></svg>
  </button>
</template>

<script setup>
import { useTheme } from "../theme/useTheme";
import { useI18n } from "../i18n/useI18n";

const { theme, toggle } = useTheme();
const { t } = useI18n();
</script>
