<template>
  <div class="home afe">
    <div class="home-bg" aria-hidden="true"><i></i><i></i><i></i></div>

    <header class="home-bar">
      <router-link class="brand" to="/">
        <span class="mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
        Rex-Analysis
      </router-link>
      <span class="crumb" aria-hidden="true">/</span>
      <router-link class="bench-crumb" to="/afe">{{ bench.name }}</router-link>
      <a class="github" :href="bench.github" target="_blank" rel="noreferrer">GitHub ↗</a>
      <ThemeToggle />
    </header>

    <main class="home-main">
      <section class="hero">
        <p class="eyebrow"><span class="pulse"></span>frontier, still moving / 2026</p>
        <h1 class="wordmark">
          <span>AgentFrontier</span>
          <span class="grad">Exam 1.0</span>
        </h1>
        <p class="hero-lede afe-head">{{ bench.tagline }}</p>
        <p class="hero-lede">{{ bench.summary }}</p>

        <dl class="rcb-stats">
          <div><dt>任务</dt><dd>{{ pack.tasks.length }}</dd></div>
          <div><dt>领域</dt><dd>{{ pack.domains.length }}</dd></div>
          <div><dt>提交</dt><dd>{{ board.rows.length }}</dd></div>
        </dl>
        <div class="rcb-go">
          <router-link class="go-solid" :to="`${base}/tasks`">浏览 {{ pack.tasks.length }} 个任务 →</router-link>
          <router-link class="go-ghost" :to="`${base}/leaderboard`">排行榜</router-link>
          <router-link class="go-ghost" :to="`${base}/about`">评测说明</router-link>
          <a class="go-ghost" :href="REX_URL" target="_blank" rel="noreferrer">参与共建 ↗</a>
        </div>
      </section>

      <section class="afe-panel">
        <p class="eyebrow">AFE1.0 · 领域</p>
        <router-link
          v-for="d in domains"
          :key="d.id"
          class="afe-domain"
          :style="{ '--c': d.hue }"
          :to="{ path: `${base}/tasks`, query: { domain: d.id } }"
        >
          <header>
            <span class="afe-en">{{ d.en }}</span>
            <span class="afe-count">{{ d.count }}<small> 题</small></span>
          </header>
          <h2>{{ d.label }}</h2>
          <ul class="afe-samples">
            <li v-for="t in d.samples" :key="t.task_id">{{ t.label }}</li>
          </ul>
          <footer>
            <span>{{ d.count }} 道题</span>
            <span class="afe-go">看这 {{ d.count }} 题 →</span>
          </footer>
        </router-link>
      </section>
    </main>

    <footer class="home-foot">
      <span>在未解决的科学问题上持续突破。</span>
      <span>{{ pack.tasks.length }} 题 · {{ pack.domains.length }} 个领域</span>
    </footer>
  </div>
</template>

<script setup>
import { computed } from "vue";
import ThemeToggle from "../components/ThemeToggle.vue";
import { useTheme } from "../theme/useTheme";
import { REX_URL } from "../data/links";
import { getBench, getLeaderboard, getTasks } from "../data/client";

const bench = getBench("afe");
const version = bench.version || "1.0";
const base = `/afe/${version}`;
const pack = getTasks("afe", version);
const board = getLeaderboard("afe", version);
const { theme } = useTheme();

const domains = computed(() =>
  pack.domains.map((d) => {
    const tasks = pack.tasks.filter((t) => t.domain === d.id);
    return {
      ...d,
      hue: theme.value === "dark" ? d.color_dark || d.color : d.color,
      samples: tasks.slice(0, 3),
    };
  }),
);
</script>
