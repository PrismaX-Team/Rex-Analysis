import { ref } from "vue";

const KEY = "rcb-theme";
const root = document.documentElement;
// index.html stamps data-theme before the app loads; read it back as the starting value.
const theme = ref(root.dataset.theme === "dark" ? "dark" : "light");

export function useTheme() {
  function toggle() {
    theme.value = theme.value === "dark" ? "light" : "dark";
    root.classList.add("theme-anim");
    root.dataset.theme = theme.value;
    setTimeout(() => root.classList.remove("theme-anim"), 350);
    try { localStorage.setItem(KEY, theme.value); } catch { /* private mode */ }
  }
  return { theme, toggle };
}
