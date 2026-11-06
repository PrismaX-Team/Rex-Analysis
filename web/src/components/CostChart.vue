<template>
  <figure v-if="points.length > 1" class="cc">
    <figcaption class="cc-head">
      <h2>分数与成本</h2>
      <p>横轴是单题成本（对数刻度），纵轴是均分，点的面积表示单题用时。连线是 Pareto 前沿：在不多花钱的前提下分数最高的那些提交。</p>
    </figcaption>

    <div class="cc-plot" @pointerleave="hot = ''">
      <svg :viewBox="`0 0 ${W} ${H}`" role="img" :aria-label="aria">
        <g class="cc-grid">
          <line v-for="t in yTicks" :key="`y${t}`" :x1="L" :x2="W - R" :y1="y(t)" :y2="y(t)" />
          <text v-for="t in yTicks" :key="`yt${t}`" :x="L - 10" :y="y(t) + 4" text-anchor="end">{{ t }}</text>
          <line v-for="t in xTicks" :key="`x${t}`" :x1="x(t)" :x2="x(t)" :y1="T" :y2="H - B" />
          <text v-for="t in xTicks" :key="`xt${t}`" :x="x(t)" :y="H - B + 20" text-anchor="middle">{{ tick(t) }}</text>
        </g>
        <text class="cc-axis" :x="(L + W - R) / 2" :y="H - 6" text-anchor="middle">单题成本（美元，对数刻度）</text>
        <text class="cc-axis" :transform="`translate(16 ${(T + H - B) / 2}) rotate(-90)`" text-anchor="middle">均分</text>

        <path class="cc-front" :d="frontPath" />

        <g class="cc-dots">
          <circle
            v-for="p in byArea"
            :key="p.id"
            :class="{ front: p.front, hot: hot === p.id, dim: hot && hot !== p.id }"
            :cx="p.cx"
            :cy="p.cy"
            :r="p.r"
          />
        </g>

        <g class="cc-labels">
          <text v-for="l in labels" :key="l.id" :x="l.x" :y="l.y" :text-anchor="l.anchor">{{ l.text }}</text>
        </g>

        <!-- Hit targets: at least 24px across, larger than the painted dot. -->
        <circle
          v-for="p in points"
          :key="`h${p.id}`"
          class="cc-hit"
          :cx="p.cx"
          :cy="p.cy"
          :r="Math.max(12, p.r + 4)"
          tabindex="0"
          :aria-label="describe(p)"
          @pointerenter="hot = p.id"
          @focus="hot = p.id"
          @blur="hot = ''"
        />
      </svg>

      <div v-if="hotPoint" class="cc-tip" :style="tipStyle">
        <b>{{ hotPoint.score.toFixed(2) }}</b>
        <span class="cc-tip-name">{{ hotPoint.label }}</span>
        <span>单题成本 {{ money(hotPoint.cost) }} · 单题用时 {{ duration(hotPoint.time) }}</span>
        <span v-if="hotPoint.front" class="cc-tip-front">在 Pareto 前沿上</span>
      </div>
    </div>

    <p class="cc-legend">
      <span><i class="k-front"></i>Pareto 前沿</span>
      <span><i class="k-dot"></i>其他提交</span>
      <span><i class="k-size"></i>面积 = 单题用时</span>
    </p>
  </figure>
</template>

<script setup>
import { computed, ref } from "vue";

const props = defineProps({
  rows: { type: Array, required: true },
  labelOf: { type: Function, default: (r) => r.system },
});

const W = 960;
const H = 420;
const L = 64;
const R = 24;
const T = 20;
const B = 52;

const hot = ref("");

const valid = computed(() => props.rows.filter((r) => r.cost_usd > 0 && r.score != null));
const costs = computed(() => valid.value.map((r) => r.cost_usd));
// Log axis padded a little past the data, not out to the next power of ten.
const xMin = computed(() => Math.min(...costs.value) / 1.6);
const xMax = computed(() => Math.max(...costs.value) * 1.6);
const yMax = computed(() => Math.ceil(Math.max(...valid.value.map((r) => r.score)) / 10) * 10);
// A scatter doesn't need a zero baseline; start at the ten just below the lowest score.
const yMin = computed(() => Math.max(0, Math.floor((Math.min(...valid.value.map((r) => r.score)) - 1) / 10) * 10));

const x = (v) => L + ((Math.log10(v) - Math.log10(xMin.value)) / (Math.log10(xMax.value) - Math.log10(xMin.value))) * (W - L - R);
const y = (v) => T + (1 - (v - yMin.value) / (yMax.value - yMin.value)) * (H - T - B);

// 1-2-5 ticks inside the padded range.
const xTicks = computed(() => {
  const out = [];
  for (let e = Math.floor(Math.log10(xMin.value)); e <= Math.ceil(Math.log10(xMax.value)); e++) {
    for (const m of [1, 2, 5]) {
      const v = m * 10 ** e;
      if (v >= xMin.value && v <= xMax.value) out.push(v);
    }
  }
  return out;
});
const yTicks = computed(() => Array.from({ length: (yMax.value - yMin.value) / 10 + 1 }, (_, i) => yMin.value + i * 10));

// A point is on the frontier when no other point is at least as cheap and scores higher.
const frontIds = computed(() => {
  const sorted = [...valid.value].sort((a, b) => a.cost_usd - b.cost_usd || b.score - a.score);
  const ids = new Set();
  let best = -Infinity;
  for (const r of sorted) {
    if (r.score > best) {
      ids.add(r.run_id);
      best = r.score;
    }
  }
  return ids;
});

const maxTime = computed(() => Math.max(...valid.value.map((r) => r.duration_seconds || 0), 1));
const points = computed(() =>
  valid.value.map((r) => ({
    id: r.run_id,
    label: props.labelOf(r),
    score: r.score,
    cost: r.cost_usd,
    time: r.duration_seconds,
    front: frontIds.value.has(r.run_id),
    cx: x(r.cost_usd),
    cy: y(r.score),
    // Area proportional to time: radius grows with the square root.
    r: 4 + 9 * Math.sqrt((r.duration_seconds || 0) / maxTime.value),
  })),
);
// Big dots first so small ones stay on top and hoverable.
const byArea = computed(() => [...points.value].sort((a, b) => b.r - a.r));

const frontPath = computed(() =>
  points.value
    .filter((p) => p.front)
    .sort((a, b) => a.cx - b.cx)
    .map((p, i) => `${i ? "L" : "M"}${p.cx.toFixed(1)},${p.cy.toFixed(1)}`)
    .join(""),
);

// Label only the frontier. The frontier rises left to right, so the space below-right of a
// point is clear of both its segments; the top point (no segment to its right) goes left.
// A label that would overlap one already placed, or a dot, is dropped (the tooltip has it).
const labels = computed(() => {
  const placed = points.value.map((p) => ({ x0: p.cx - p.r, x1: p.cx + p.r, y0: p.cy - p.r, y1: p.cy + p.r, self: p.id }));
  const out = [];
  const front = points.value.filter((p) => p.front).sort((a, b) => b.score - a.score);
  const top = front[0]?.id;
  for (const p of front) {
    const width = [...p.label].reduce((n, ch) => n + (ch.charCodeAt(0) > 255 ? 13 : 7), 0);
    let box;
    let anchor;
    if (p.id === top || p.cx + width > W - R) {
      // Left of the dot, nudged up so it clears the segment arriving from the left.
      box = { x0: p.cx - p.r - 6 - width, x1: p.cx - p.r - 6, y0: p.cy - p.r - 16, y1: p.cy - p.r - 2 };
      anchor = "end";
    } else {
      const lx = p.cx + p.r * 0.5;
      const ly = p.cy + p.r + 14;
      box = { x0: lx, x1: lx + width, y0: ly - 11, y1: ly + 3 };
      anchor = "start";
    }
    const clash = placed.some((b) => b.self !== p.id && box.x0 < b.x1 && box.x1 > b.x0 && box.y0 < b.y1 && box.y1 > b.y0);
    if (clash) continue;
    placed.push(box);
    out.push({ id: p.id, text: p.label, x: anchor === "end" ? box.x1 : box.x0, y: box.y1 - 3, anchor });
  }
  return out;
});

const hotPoint = computed(() => points.value.find((p) => p.id === hot.value) || null);
const tipStyle = computed(() => {
  const p = hotPoint.value;
  const left = (p.cx / W) * 100;
  const top = (p.cy / H) * 100;
  return {
    top: `${top}%`,
    ...(left > 60 ? { right: `${100 - left + 2}%` } : { left: `${left + 2}%` }),
  };
});

function money(v) {
  if (v == null) return "–";
  if (v < 0.01) return `$${v.toFixed(3)}`;
  return v < 10 ? `$${v.toFixed(2)}` : `$${Math.round(v)}`;
}
// Axis ticks: no trailing zeros ($0.05, $0.2, $1, $10).
const tick = (v) => `$${Number(v.toPrecision(2))}`;

function duration(s) {
  if (s == null) return "–";
  const h = Math.floor(s / 3600);
  const m = Math.round((s % 3600) / 60);
  return h ? `${h}h ${String(m).padStart(2, "0")}m` : `${m}m`;
}

const describe = (p) => `${p.label}：均分 ${p.score.toFixed(2)}，单题成本 ${money(p.cost)}，单题用时 ${duration(p.time)}${p.front ? "，在 Pareto 前沿上" : ""}`;
const aria = computed(() => `${points.value.length} 个提交的均分与单题成本，${frontIds.value.size} 个在 Pareto 前沿上。`);
</script>
