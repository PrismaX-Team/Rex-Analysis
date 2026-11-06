<template>
<div class="ov-wrap">
  <table class="ov">
    <thead>
      <tr>
        <th class="ov-bench">Benchmark</th>
        <th class="ov-cat">分类</th>
        <th v-for="m in medals" :key="m.n" class="ov-place"><i v-if="m.cls" class="medal" :class="m.cls"></i>{{ m.label }}</th>
        <th class="ov-more">详情</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in overall" :key="row.id" :style="{ '--c': row.color }" @click="$router.push(row.to)">
        <td class="ov-bench">
          <span class="ov-mono">{{ row.short }}</span>
          <span class="ov-name">{{ row.name }}<small v-if="row.groupLabel">{{ row.groupLabel }}榜</small></span>
        </td>
        <td class="ov-cat"><span class="ov-chip">{{ row.category }}</span></td>
        <td v-if="row.pending" :colspan="medals.length" class="ov-pending">{{ row.pending }}</td>
        <td v-for="(m, i) in medals" v-else :key="m.n" class="ov-place">
          <template v-if="row.top[i]">
            <span class="ov-sys">{{ row.top[i].system }}</span>
            <span v-if="row.top[i].model" class="ov-model">{{ row.top[i].model }}</span>
            <span class="ov-score">{{ row.top[i].score.toFixed(2) }}</span>
          </template>
          <span v-else class="ov-empty">–</span>
        </td>
        <td class="ov-more"><router-link :to="row.to" @click.stop>查看 →</router-link></td>
      </tr>
    </tbody>
  </table>
</div>
</template>

<script setup>
import { computed } from "vue";
import { useTheme } from "../theme/useTheme";
import { getBenches, getLeaderboard } from "../data/client";

// Shared by the home page and the site-wide leaderboard page.
const { theme } = useTheme();
const benches = getBenches();
const accentOf = (bench) => (theme.value === "dark" ? bench.accent_dark || bench.accent : bench.accent);

// Overall board: per live bench, one row per ranking group, top five each.
// Rows come from benches.json, so a new bench shows up here without touching this page.
const medals = [
  { n: 1, label: "1st", cls: "gold" },
  { n: 2, label: "2nd", cls: "silver" },
  { n: 3, label: "3rd", cls: "bronze" },
  { n: 4, label: "4th", cls: "" },
  { n: 5, label: "5th", cls: "" },
];
const overall = computed(() =>
  benches
    .filter((b) => b.status === "live")
    .flatMap((bench) => {
      const version = bench.version || "1.0";
      const board = getLeaderboard(bench.id, version);
      // A live bench whose board isn't published yet still gets one row saying so.
      if (!board.rows.length) {
        return [{
          id: bench.id,
          short: bench.short,
          name: bench.name,
          category: bench.category || bench.task_type,
          groupLabel: "",
          color: accentOf(bench),
          to: { path: `${bench.entry}/${version}/tasks` },
          pending: "暂无公开成绩",
          top: [],
        }];
      }
      const groups = board.groups?.length ? board.groups : [{ id: "", label: "" }];
      // One row per ranking group (models first, then agents), each with its own top five.
      return groups.map((g) => ({
        id: `${bench.id}-${g.id}`,
        short: bench.short,
        name: bench.name,
        category: bench.category || bench.task_type,
        groupLabel: groups.length > 1 ? g.label : "",
        color: accentOf(bench),
        to: { path: `${bench.entry}/${version}/leaderboard`, query: g.id ? { group: g.id } : {} },
        top: board.rows
          .filter((r) => !g.id || r.group === g.id)
          .sort((a, b) => a.rank - b.rank)
          .slice(0, medals.length),
      }));
    }),
);
</script>
