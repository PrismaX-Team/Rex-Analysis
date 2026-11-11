<template>
  <div v-if="rows.length" class="lb-wrap">
    <table class="lb">
      <thead>
        <tr>
          <th class="c-rank">#</th>
          <th class="c-sys">{{ t("模型") }}</th>
          <th v-if="hasHarness" class="c-harness">Harness</th>
          <th class="c-score" :aria-sort="ariaSort('score')"><button type="button" class="sort" @click="sortBy('score')">{{ t("均分") }}<i :class="arrow('score')"></i></button></th>
          <th v-for="d in domains" :key="d" class="c-dom" :title="domLabel(d)">{{ domLabel(d).slice(0, 2) }}</th>
          <th class="c-new" :title="t('分数达到 50（原论文证据水平）的题数')">New</th>
          <th class="c-meta">{{ t("题数") }}</th>
          <template v-if="!pass5">
            <th class="c-meta" :aria-sort="ariaSort('cost_usd')"><button type="button" class="sort" @click="sortBy('cost_usd')">{{ t("单题成本") }}<i :class="arrow('cost_usd')"></i></button></th>
            <th class="c-meta" :aria-sort="ariaSort('duration_seconds')"><button type="button" class="sort" @click="sortBy('duration_seconds')">{{ t("单题用时") }}<i :class="arrow('duration_seconds')"></i></button></th>
            <th class="c-src">{{ t("来源") }}</th>
          </template>
          <th v-else class="c-meta c-spread" :title="t('五次尝试的单题平均分 ± 标准差')">{{ t("单次均值 ± σ") }}</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="row in sorted" :key="row.run_id">
          <tr class="lb-row" :class="{ open: openId === row.run_id }" @click="toggle(row.run_id)">
            <td class="c-rank"><span class="rank" :class="`r${row.rank}`">{{ row.rank }}</span></td>
            <td class="c-sys">
              <span class="sys">{{ modelOf(row) }}</span>
            </td>
            <td v-if="hasHarness" class="c-harness">
              <a v-if="row.source_url" :href="row.source_url" target="_blank" rel="noreferrer" @click.stop>{{ harnessOf(row) }}</a>
              <template v-else>{{ harnessOf(row) }}</template>
            </td>
            <td class="c-score"><span class="score">{{ row.score.toFixed(2) }}</span></td>
            <td v-for="d in domains" :key="d" class="c-dom">
              <span
                class="heat"
                :class="[bin(row.domains?.[d]), { stack: pass5 }]"
                :title="domTitle(row, d)"
              >{{ fmt(row.domains?.[d]) }}<small v-if="pass5 && row.domain_spread?.[d]?.mean != null">{{ row.domain_spread[d].mean.toFixed(1) }}±{{ row.domain_spread[d].std.toFixed(1) }}</small></span>
            </td>
            <td class="c-new">
              <span v-if="row.new_count" class="new-badge" :title="newTitle(row)">{{ row.new_count }}</span>
              <span v-else class="new-none">–</span>
            </td>
            <td class="c-meta" :class="{ partial: row.task_count < fullCount }">{{ row.task_count }}</td>
            <template v-if="!pass5">
              <td class="c-meta">{{ cost(row.cost_usd) }}</td>
              <td class="c-meta">{{ dur(row.duration_seconds) }}</td>
              <td class="c-src"><span class="src" :class="row.source">{{ row.source === "community" ? t("社区") : t("内测") }}</span></td>
            </template>
            <td v-else class="c-meta c-spread">{{ row.attempt_mean.toFixed(1) }} ± {{ row.attempt_std.toFixed(1) }}</td>
          </tr>
          <tr v-if="openId === row.run_id" class="lb-detail">
            <td :colspan="(pass5 ? 6 : 8) + domains.length + (hasHarness ? 1 : 0)">
              <p v-if="newTasks(row).length" class="strip-new">
                <b>New-Discovery</b>
                <router-link v-for="t in newTasks(row)" :key="t.task_id" :to="`/${bench}/${version}/tasks/${t.task_id}`" @click.stop>
                  {{ t.task_id }} <em>{{ t.score.toFixed(1) }}</em>
                </router-link>
              </p>
              <div class="strip">
                <div v-for="d in domains" :key="d" class="strip-dom">
                  <span class="strip-name">{{ domLabel(d) }}</span>
                  <span class="strip-cells">
                    <router-link
                      v-for="t in tasksOf(row, d)"
                      :key="t.task_id"
                      :class="['cell', bin(t.score), { top: isFrontier(t, row) }]"
                      :to="`/${bench}/${version}/tasks/${t.task_id}`"
                      :title="cellTitle(t, row)"
                      @click.stop
                    >{{ t.score == null ? "–" : Math.round(t.score) }}</router-link>
                  </span>
                </div>
              </div>
              <div class="strip-foot">
                <span class="strip-keys">
                  <span><i class="dot-top"></i>{{ t("本题全榜最高") }}</span>
                  <span v-if="pass5">{{ t("悬停小格看五次尝试的分数、均值 ± 标准差和最低 / 最高") }}</span>
                </span>
                <button v-if="!pass5" type="button" @click.stop="$emit('open', row.run_id)">{{ t("查看这次提交 →") }}</button>
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
  <div v-if="rows.length" class="heat-legend" :aria-label="t('颜色图例')">
    <span>Re-Discovery</span>
    <i class="h0">&lt;10</i><i class="h1">10</i><i class="h2">20</i><i class="h3">30</i><i class="h4">40</i>
    <span class="lg-new">New-Discovery</span>
    <i class="hn">50+</i>
    <i class="none">{{ t("未评分") }}</i>
    <span v-if="pass5" class="lg-note">{{ t("Pass@5 学科格：上为五次取最好的均分，下为全部尝试的均值 ± 标准差") }}</span>
  </div>
  <div v-else class="empty">{{ t("这一版还没有公开提交。") }}</div>
</template>

<script setup>
import { computed, ref } from "vue";
import { getRun } from "../data/client";
import { useI18n } from "../i18n/useI18n";

const { t, en } = useI18n();
const domLabel = (id) => (en.value ? props.domainLabelsEn?.[id] || props.domainLabels?.[id] : props.domainLabels?.[id]) || id;

const props = defineProps({
  rows: { type: Array, required: true },
  domains: { type: Array, default: () => [] },
  domainLabels: { type: Object, default: () => ({}) },
  domainLabelsEn: { type: Object, default: () => ({}) },
  frontier: { type: Object, default: () => ({}) },
  bench: { type: String, default: "" },
  version: { type: String, default: "" },
  // "pass1": one run per task. "pass5": best of five; rows carry their own tasks.
  mode: { type: String, default: "pass1" },
  // Harness shared by rows that are bare models (RCB: ResearchHarness).
  sharedHarness: { type: String, default: "" },
});
defineEmits(["open"]);
const pass5 = computed(() => props.mode === "pass5");

const openId = ref("");

// Model is the main column. A row with a separate model ran inside a named harness (an agent);
// a row without one is a model run in the bench's shared harness.
const modelOf = (row) => row.model || row.system;
const harnessOf = (row) => (row.model ? row.system : props.sharedHarness);
const hasHarness = computed(() => !pass5.value && props.rows.some((r) => r.model || props.sharedHarness));

// Sort by score (default, the official rank), cost or time. Ranks stay as published.
const sortKey = ref("score");
const sortDir = ref("desc");
function sortBy(key) {
  if (sortKey.value === key) sortDir.value = sortDir.value === "desc" ? "asc" : "desc";
  else {
    sortKey.value = key;
    sortDir.value = key === "score" ? "desc" : "asc";
  }
}
const sorted = computed(() => {
  if (sortKey.value === "score" && sortDir.value === "desc") return props.rows;
  const k = sortKey.value;
  const sign = sortDir.value === "desc" ? -1 : 1;
  return [...props.rows].sort((a, b) => {
    if (a[k] == null) return 1;
    if (b[k] == null) return -1;
    return sign * (a[k] - b[k]) || a.rank - b.rank;
  });
});
const ariaSort = (k) => (sortKey.value === k ? (sortDir.value === "desc" ? "descending" : "ascending") : "none");
const arrow = (k) => (sortKey.value === k ? `arr ${sortDir.value}` : "arr");
const fullCount = computed(() => Math.max(0, ...props.rows.map((r) => r.task_count)));

function toggle(id) {
  openId.value = openId.value === id ? "" : id;
}

function tasksOf(row, domain) {
  return allTasks(row).filter((t) => t.task_id.startsWith(`${domain}_`));
}

function isFrontier(task, row) {
  if (task.score == null) return false;
  const f = props.frontier[task.task_id];
  return f?.run_id ? f.run_id === row.run_id : f?.score === task.score;
}

const f1 = (v) => (v == null ? "–" : v.toFixed(1));

function cellTitle(t, row) {
  const lines = [`${t.task_id} · ${t.score == null ? "未评分" : t.score.toFixed(1)}${t.score >= 50 ? " · New-Discovery" : ""}`];
  if (t.runs) {
    lines.push(`五次：${t.runs.map(f1).join(" / ")}`);
    lines.push(`均值 ± σ：${f1(t.mean)} ± ${f1(t.std)}`);
    lines.push(`最低 / 最高：${f1(t.min)} / ${f1(t.max)}`);
    if (t.attempts != null) lines.push(`计入尝试：${t.scored_runs} / ${t.attempts}`);
  }
  if (isFrontier(t, row)) lines.push("本题全榜最高");
  return lines.join("\n");
}

function domTitle(row, d) {
  const v = row.domains?.[d];
  const head = `${props.domainLabels[d] || d} · ${f1(v)}${v >= 50 ? " · New-Discovery" : ""}`;
  const sp = row.domain_spread?.[d];
  return sp ? `${head}\n全部尝试：${f1(sp.mean)} ± ${f1(sp.std)}` : head;
}

function allTasks(row) {
  return (pass5.value ? row.tasks : getRun(props.bench, props.version, row.run_id)?.tasks) || [];
}

function newTasks(row) {
  return allTasks(row).filter((t) => t.score >= 50).sort((a, b) => b.score - a.score);
}

function newTitle(row) {
  return `越过 50 分的题：\n${newTasks(row).map((t) => `${t.task_id} ${t.score.toFixed(1)}`).join("\n")}`;
}

// Re-Discovery: five blue bins of 10 points below 50. New-Discovery: one green step at 50+.
function bin(v) {
  if (v == null) return "none";
  if (v >= 50) return "hn";
  return `h${Math.min(4, Math.max(0, Math.floor(v / 10)))}`;
}

const fmt = (v) => (v == null ? "–" : v.toFixed(1));

function cost(v) {
  if (v == null) return "–";
  if (v < 0.01) return "<$0.01";
  return v < 10 ? `$${v.toFixed(2)}` : `$${Math.round(v)}`;
}

function dur(s) {
  if (s == null) return "–";
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  return h ? `${h}h ${String(m).padStart(2, "0")}m` : `${m}m`;
}
</script>
