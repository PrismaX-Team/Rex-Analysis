<template>
  <TopBar :bench="benchId" :version="version" />
  <main class="shell page">
    <p class="kicker">{{ bench?.name }} · Leaderboard</p>
    <h1>排行榜</h1>
    <p class="lede">{{ bench?.board_lede || "按均分排名。点一行展开分题成绩。" }}</p>
    <ScoreNote :bench="benchId" :version="version" />

    <div v-if="pass5Board" class="lb-mode" role="tablist" aria-label="计分方式">
      <button type="button" role="tab" :aria-selected="mode === 'pass1'" @click="mode = 'pass1'">
        Pass@1<small>每题一次</small>
      </button>
      <button type="button" role="tab" :aria-selected="mode === 'pass5'" @click="mode = 'pass5'">
        Pass@5<small>五次取最好</small>
      </button>
    </div>


    <template v-if="mode === 'pass5' && pass5Board">
      <p class="lb-group-note">{{ pass5Board.note }}</p>
      <LeaderboardTable
        :key="'p5'"
        :bench="benchId"
        mode="pass5"
        :rows="pass5Board.rows"
        :domains="pass5Board.domains || []"
        :domain-labels="domainLabels"
        :frontier="pass5Board.frontier || {}"
        :version="version"
      />
      <p class="lb-foot">数据来源：{{ pass5Board.source }}（{{ pass5Board.generated_at }}）。Pass@5 和 Pass@1 的分数不能直接横比。</p>
    </template>

    <template v-else-if="board.rows.length">
      <div v-if="groups.length > 1" class="lb-tabs" role="tablist">
        <button
          v-for="g in groups"
          :key="g.id"
          type="button"
          role="tab"
          :aria-selected="group === g.id"
          @click="group = g.id"
        >
          {{ g.label }}<small>{{ g.en }} · {{ countOf(g.id) }}</small>
        </button>
      </div>
      <p v-if="groupNote" class="lb-group-note">{{ groupNote }}</p>

      <div class="podium">
        <router-link
          v-for="row in rows.slice(0, 3)"
          :key="row.run_id"
          class="podium-card"
          :class="`p${row.rank}`"
          :to="`${base}/runs/${row.run_id}`"
        >
          <span class="podium-rank">#{{ row.rank }}</span>
          <span class="podium-sys">{{ row.system }}</span>
          <span class="podium-model">{{ row.model || `${row.task_count} / ${fullCount} 题` }}</span>
          <span class="podium-score">{{ row.score.toFixed(2) }}</span>
          <span v-if="row.new_count" class="podium-new" :title="`${row.new_count} 道题越过 50 分`">New-Discovery × {{ row.new_count }}</span>
          <span class="podium-bar"><i :style="{ width: `${(row.score / maxScore) * 100}%` }"></i></span>
        </router-link>
      </div>

      <LeaderboardTable
        :rows="rows"
        :domains="board.domains || []"
        :domain-labels="domainLabels"
        :frontier="board.frontier || {}"
        :bench="benchId"
        :version="version"
        @open="openRun"
      />
      <p v-if="board.note" class="lb-foot">{{ board.note }} 数据来源：{{ board.source }}</p>
    </template>
    <div v-else class="empty board-empty">
      <p>{{ bench?.board_empty || "这一版还没有公开提交。" }}</p>
      <router-link :to="`${base}/tasks`">先看任务 →</router-link>
    </div>
  </main>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { useRouter } from "vue-router";
import TopBar from "../components/TopBar.vue";
import ScoreNote from "../components/ScoreNote.vue";
import LeaderboardTable from "../components/LeaderboardTable.vue";
import { getLeaderboard, getPass5, getTasks } from "../data/client";
import { useBench } from "../data/useBench";

const router = useRouter();
const { route, benchId, version, bench, base } = useBench();
const board = computed(() => getLeaderboard(benchId.value, version.value));

const pass5Board = computed(() => getPass5(benchId.value, version.value));
const mode = ref("pass1");

const groups = computed(() => board.value.groups || [{ id: "all", label: "全部", en: "All" }]);
// ?group=agent lets the home table link straight to a tab.
const pickGroup = () => (groups.value.some((g) => g.id === route.query.group) ? route.query.group : groups.value[0].id);
const group = ref(pickGroup());
watch([benchId, version], () => { group.value = pickGroup(); mode.value = "pass1"; });
watch(() => route.query.group, () => { group.value = pickGroup(); });

const countOf = (id) => board.value.rows.filter((r) => (r.group || "all") === id).length;
const rows = computed(() => board.value.rows.filter((r) => (r.group || "all") === group.value));
const fullCount = computed(() => getTasks(benchId.value, version.value).tasks.length);
const maxScore = computed(() => Math.max(...rows.value.map((r) => r.score), 1));
const groupNote = computed(() => groups.value.find((g) => g.id === group.value)?.note || "");

const domainLabels = computed(() => {
  const map = {};
  for (const task of getTasks(benchId.value, version.value).tasks) map[task.domain] = task.domain_label;
  return map;
});

function openRun(runId) {
  router.push({ name: "run", params: { bench: benchId.value, version: version.value, runId } });
}
</script>
