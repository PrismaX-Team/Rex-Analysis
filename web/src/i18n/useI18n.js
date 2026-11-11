import { computed } from "vue";
import { locale } from "./useLocale";
import { translate } from "./dict";

// t("中文原文") -> the string in the current language. Keys are the Chinese source text,
// so a missing translation falls back to Chinese rather than a raw key.
export function useI18n() {
  const t = (text) => translate(text, locale.value);
  const en = computed(() => locale.value === "en");
  return { t, en, locale };
}
