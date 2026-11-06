import { createRouter, createWebHistory } from "vue-router";
import { getBenches, versionExists } from "./data/client";
import Home from "./pages/Home.vue";
import Rcb from "./pages/Rcb.vue";
import Afe from "./pages/Afe.vue";
import Leaderboard from "./pages/Leaderboard.vue";
import Run from "./pages/Run.vue";
import Tasks from "./pages/Tasks.vue";
import Task from "./pages/Task.vue";
import About from "./pages/About.vue";
import SiteLeaderboard from "./pages/SiteLeaderboard.vue";
import SiteAbout from "./pages/SiteAbout.vue";

// Each bench has its own entry page; the inner pages are shared and read the bench from the URL.
const benchIds = getBenches().filter((b) => b.status === "live").map((b) => b.id).join("|");
const B = `/:bench(${benchIds})`;

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "home", component: Home },
    { path: "/leaderboard", name: "site-leaderboard", component: SiteLeaderboard },
    { path: "/about", name: "site-about", component: SiteAbout },
    { path: "/rcb", name: "rcb", component: Rcb },
    { path: "/afe", name: "afe", component: Afe },
    { path: `${B}/:version/leaderboard`, name: "leaderboard", component: Leaderboard },
    { path: `${B}/:version/runs/:runId`, name: "run", component: Run },
    { path: `${B}/:version/tasks`, name: "tasks", component: Tasks },
    { path: `${B}/:version/tasks/:taskId`, name: "task", component: Task },
    { path: `${B}/:version/about`, name: "about", component: About },
  ],
  // Hash links (/#benches) scroll to the section; everything else starts at the top.
  scrollBehavior(to) {
    return to.hash ? { el: to.hash, behavior: "smooth", top: 84 } : { top: 0 };
  },
});

// An unknown version falls back to the bench's entry page instead of an empty detail page.
router.beforeEach((to) => {
  const { bench, version } = to.params;
  if (!bench || !version) return true;
  if (!versionExists(bench, version)) return { path: `/${bench}` };
  return true;
});
