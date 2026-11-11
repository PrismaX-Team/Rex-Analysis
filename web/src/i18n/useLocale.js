import { ref, computed } from "vue";

// UI language. One reactive value for the whole app; pages read it through t().
const KEY = "rex-locale";
const SUPPORTED = ["zh", "en"];

function initial() {
  try {
    const saved = localStorage.getItem(KEY);
    if (saved && SUPPORTED.includes(saved)) return saved;
  } catch { /* private mode */ }
  return "zh";
}

export const locale = ref(initial());

export function setLocale(next) {
  if (!SUPPORTED.includes(next) || next === locale.value) return;
  locale.value = next;
  try { localStorage.setItem(KEY, next); } catch { /* private mode */ }
  document.documentElement.lang = next === "zh" ? "zh-CN" : "en";
}

export const isEn = computed(() => locale.value === "en");
