<template>
  <div v-if="rows.length" class="lb-wrap">
    <table class="lb">
      <thead>
        <tr>
          <th class="c-rank">#</th>
          <th class="c-sys">系统</th>
          <th class="c-score">均分</th>
          <th v-for="d in domains" :key="d" class="c-dom" :title="domainLabels[d] || d">{{ (domainLabels[d] || d).slice(0, 2) }}</th>
          <th class="c-new" title="分数达到 50（原论文证据水平）的题数">New</th>
          <th class="c-meta">题数</th>
          <template v-if="!pass5">
            <th class="c-meta">单题成本</th>
            <th class="c-meta">单题用时</th>
            <th class="c-src">来源</th>
          </template>
          <th v-else class="c-meta c-spread" title="五次尝试的单题平均分 ± 标准差">单次均值 ± σ</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="row in rows" :key="row.run_id">
          <tr class="lb-row" :class="{ open: openId === row.run_id }" @click="toggle(row.run_id)">
            <td class="c-rank"><span class="rank" :class="`r${row.rank}`">{{ row.rank }}</span></td>
            <td class="c-sys">
              <span class="sys">
                <a v-if="row.source_url" :href="row.source_url" target="_blank" rel="noreferrer" @click.stop>{{ row.system }}</a>
                <template v-else>{{ row.system }}</template>
              </span>
              <span v-if="row.model" class="model">{{ row.model }}</span>
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
              <td class="c-src"><span class="src" :class="row.source">{{ row.source === "community" ? "社区" : "内测" }}</span></td>
            </template>
            <td v-else class="c-meta c-spread">{{ row.attempt_mean.toFixed(1) }} ± {{ row.attempt_std.toFixed(1) }}</td>
          </tr>
          <tr v-if="openId === row.run_id" class="lb-detail">
            <td :colspan="(pass5 ? 6 : 8) + domains.length">
              <p v-if="newTasks(row).length" class="strip-new">
                <b>New-Discovery</b>
                <router-link v-for="t in newTasks(row)" :key="t.task_id" :to="`/${bench}/${version}/tasks/${t.task_id}`" @click.stop>
                  {{ t.task_id }} <em>{{ t.score.toFixed(1) }}</em>
                </router-link>
              </p>
              <div class="strip">
                <div v-for="d in domains" :key="d" class="strip-dom">
                  <span class="strip-name">{{ domainLabels[d] || d }}</span>
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
                  <span><i class="dot-top"></i>本题全榜最高</span>
                  <span v-if="pass5">悬停小格看五次尝试的分数、均值 ± 标准差和最低 / 最高</span>
                </span>
                <button v-if="!pass5" type="button" @click.stop="$emit('open', row.run_id)">查看这次提交 →</button>
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
  <div v-if="rows.length" class="heat-legend" aria-label="颜色图例">
    <span>Re-Discovery</span>
    <i class="h0">&lt;10</i><i class="h1">10</i><i class="h2">20</i><i class="h3">30</i><i class="h4">40</i>
    <span class="lg-new">New-Discovery</span>
    <i class="hn">50+</i>
    <i class="none">未评分</i>
    <span v-if="pass5" class="lg-note">Pass@5 学科格：上为五次取最好的均分，下为全部尝试的均值 ± 标准差</span>
  </div>
  <div v-else class="empty">这一版还没有公开提交。</div>
</template>

<script setup>
import { computed, ref } from "vue";
import { getRun } from "../data/client";

const props = defineProps({
  rows: { type: Array, required: true },
  domains: { type: Array, default: () => [] },
  domainLabels: { type: Object, default: () => ({}) },
  frontier: { type: Object, default: () => ({}) },
  bench: { type: String, default: "" },
  version: { type: String, default: "" },
  // "pass1": one run per task. "pass5": best of five; rows carry their own tasks.
  mode: { type: String, default: "pass1" },
});
defineEmits(["open"]);
const pass5 = computed(() => props.mode === "pass5");

const openId = ref("");
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
