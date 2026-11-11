<template>
  <button
    type="button"
    class="locale-toggle"
    :aria-label="locale === 'en' ? 'Switch language' : '切换语言'"
    :title="locale === 'en' ? 'Switch to Chinese' : '切换到 English'"
    @click="toggle"
  >{{ locale === "en" ? "中文" : "EN" }}</button>
</template>

<script setup>
import { locale, setLocale } from "../i18n/useLocale";

function toggle() {
  setLocale(locale.value === "en" ? "zh" : "en");
}
</script>
