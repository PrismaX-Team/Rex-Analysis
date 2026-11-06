<template>
  <TopBar :bench="benchId" :version="version" />
  <main class="shell page">
    <router-link class="back" :to="`${base}/leaderboard`">← 排行榜</router-link>
    <template v-if="run">
      <p class="kicker">Run · {{ run.group === "llm" ? "大模型" : "智能体" }}</p>
      <h1>{{ run.system }}</h1>
      <div class="run-stats">
        <div><span>均分</span><b class="grad-num">{{ run.score.toFixed(2) }}</b></div>
        <div v-if="run.model"><span>模型</span><b>{{ run.model }}</b></div>
        <div><span>题数</span><b>{{ run.task_count }}</b></div>
        <div v-if="run.cost_usd != null"><span>单题成本</span><b>${{ run.cost_usd.toFixed(2) }}</b></div>
        <div v-if="run.date"><span>日期</span><b>{{ run.date }}</b></div>
        <div v-if="run.source"><span>来源</span><b>{{ run.source === "community" ? "社区提交" : "内测" }}</b></div>
      </div>
      <ScoreNote :bench="benchId" :version="version" />

      <template v-if="run.tasks.length">
        <h2 class="run-h">分题成绩</h2>
        <div class="run-grid">
          <section v-for="d in domains" :key="d.id" class="run-dom">
            <header>
              <span>{{ d.label }}</span>
              <b>{{ d.avg == null ? "–" : d.avg.toFixed(1) }}</b>
            </header>
            <router-link
              v-for="t in d.tasks"
              :key="t.task_id"
              class="run-task"
              :to="`${base}/tasks/${t.task_id}`"
            >
              <span class="rt-id">{{ t.task_id }}</span>
              <span class="rt-bar"><i :style="{ width: `${Math.min(100, t.score ?? 0)}%` }"></i><em></em></span>
              <span class="rt-score">{{ t.score == null ? "未评分" : t.score.toFixed(1) }}</span>
            </router-link>
          </section>
        </div>
        <p class="lb-foot">竖线是 50 分：左边是 Re-Discovery（复现原论文），右边是 New-Discovery（证据超过原论文）。</p>
      </template>
      <div v-else class="empty">分题分数尚未迁入。</div>

      <p v-if="run.report_url" class="lb-foot">
        {{ run.report_note }}
        <a :href="run.report_url" target="_blank" rel="noreferrer">在原项目站查看报告 ↗</a>
      </p>
    </template>
    <div v-else class="empty">没有这次提交。</div>
  </main>
</template>

<script setup>
import { computed } from "vue";
import TopBar from "../components/TopBar.vue";
import ScoreNote from "../components/ScoreNote.vue";
import { getRun, getTasks } from "../data/client";
import { useBench } from "../data/useBench";

const { route, benchId, version, base } = useBench();
const run = computed(() => getRun(benchId.value, version.value, route.params.runId));

const domains = computed(() => {
  const labels = {};
  for (const task of getTasks(benchId.value, version.value).tasks) labels[task.domain] = task.domain_label;
  const groups = new Map();
  for (const t of run.value?.tasks || []) {
    const d = t.task_id.split("_")[0];
    if (!groups.has(d)) groups.set(d, []);
    groups.get(d).push(t);
  }
  return [...groups.entries()].map(([id, tasks]) => {
    const scored = tasks.filter((t) => t.score != null);
    return {
      id,
      label: labels[id] || id,
      tasks,
      avg: scored.length ? scored.reduce((a, t) => a + t.score, 0) / scored.length : null,
    };
  });
});
</script>
