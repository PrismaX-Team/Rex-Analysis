<template>
  <svg
    class="atlas"
    :class="{ live: interactive, lit: !!hot }"
    viewBox="-540 -540 1080 1080"
    role="img"
    :aria-label="t('1.0 任务星图：十个学科，四十道题，方法线连接跨学科的题')"
  >
    <defs>
      <radialGradient id="atlas-core" r="0.5">
        <stop offset="0" stop-color="var(--paper-solid)" />
        <stop offset="0.55" stop-color="var(--halo)" />
        <stop offset="1" stop-color="var(--halo)" stop-opacity="0" />
      </radialGradient>
      <linearGradient
        v-for="edge in edges"
        :id="`edge-${edge.key}`"
        :key="edge.key"
        gradientUnits="userSpaceOnUse"
        :x1="edge.a.x" :y1="edge.a.y" :x2="edge.b.x" :y2="edge.b.y"
      >
        <stop offset="0" :stop-color="edge.a.color" />
        <stop offset="1" :stop-color="edge.b.color" />
      </linearGradient>
    </defs>

    <g class="spin">
    <g class="scale" aria-hidden="true">
      <circle r="505" class="rim" />
      <circle r="345" class="orbit" />
      <circle r="210" />
      <circle r="96" />
      <line v-for="tick in ticks" :key="tick.k" :x1="tick.x1" :y1="tick.y1" :x2="tick.x2" :y2="tick.y2" :class="{ major: tick.major }" />
    </g>

    <g class="threads">
      <path
        v-for="edge in edges"
        :key="edge.key"
        :d="edge.d"
        :stroke="`url(#edge-${edge.key})`"
        :class="{ on: active.threads.has(edge.thread) }"
      />
      <template v-if="moving">
        <circle v-for="edge in edges" :key="`p-${edge.key}`" r="2.4" class="spark" :fill="edge.b.color">
          <animateMotion :dur="`${edge.dur}s`" :begin="`${edge.delay}s`" repeatCount="indefinite" :path="edge.d" />
        </circle>
      </template>
    </g>

    <g
      v-for="domain in domains"
      :key="domain.id"
      class="domain"
      :class="{ on: active.domains.has(domain.id) }"
      :style="{ '--c': domain.color }"
      @pointerenter="emit('update:hot', { kind: 'domain', id: domain.id })"
      @pointerleave="emit('update:hot', null)"
      @click="emit('domain', domain.id)"
    >
      <line class="spoke" :x1="domain.inner.x" :y1="domain.inner.y" :x2="domain.x" :y2="domain.y" />
      <circle class="halo" :cx="domain.x" :cy="domain.y" r="74" />
      <circle class="field" :cx="domain.x" :cy="domain.y" r="52" />
      <text class="dname" :x="domain.text.x" :y="domain.text.y" :text-anchor="domain.text.anchor">{{ domain.en }}</text>
      <text class="dsub" :x="domain.text.x" :y="domain.text.y + 20" :text-anchor="domain.text.anchor">{{ en ? domain.label_en || domain.label : domain.label }} · {{ domain.tasks.length }}</text>
      <g
        v-for="task in domain.tasks"
        :key="task.id"
        class="star"
        :class="{ on: active.tasks.has(task.id), hot: hot?.kind === 'task' && hot.id === task.id }"
        @pointerenter.stop="emit('update:hot', { kind: 'task', id: task.id })"
        @pointerleave.stop="emit('update:hot', { kind: 'domain', id: domain.id })"
        @click.stop="emit('task', task.id)"
      >
        <circle class="hit" :cx="task.x" :cy="task.y" r="18" />
        <circle class="ring" :cx="task.x" :cy="task.y" r="12" />
        <circle class="dot" :cx="task.x" :cy="task.y" r="5.5" />
      </g>
    </g>

    </g>

    <g class="core" aria-hidden="true">
      <circle r="88" fill="url(#atlas-core)" />
      <circle r="44" class="core-ring" />
      <text class="core-v" y="8">RCB</text>
      <text class="core-n" y="34">40 TASKS</text>
    </g>

    <g v-if="tip" class="tip" :transform="`translate(${tip.x} ${tip.y})`" aria-hidden="true">
      <text class="tip-id" :text-anchor="tip.anchor" y="-8">{{ tip.id }}</text>
      <text class="tip-label" :text-anchor="tip.anchor" y="14">{{ tip.label }}</text>
    </g>
  </svg>
</template>

<script setup>
import { useI18n } from "../i18n/useI18n";
const { t, en } = useI18n();
import { computed } from "vue";
import { useTheme } from "../theme/useTheme";

const props = defineProps({
  atlas: { type: Object, required: true },
  interactive: { type: Boolean, default: false },
  hot: { type: Object, default: null },
});
const emit = defineEmits(["update:hot", "domain", "task"]);
const { theme } = useTheme();
// Dark theme uses lifted steps of the same hues so marks clear the navy field.
const tint = (d) => (theme.value === "dark" && d.color_dark) || d.color;

const moving = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const R = 345;

function polar(r, deg) {
  const a = (deg * Math.PI) / 180;
  return { x: +(Math.cos(a) * r).toFixed(1), y: +(Math.sin(a) * r).toFixed(1) };
}

// Each discipline has four star slots. Give the slot facing the centre to the task with the most
// cross-discipline links, and turn every star toward the disciplines it links to, so threads cross less.
function placeStars(own, angle, list) {
  const order = new Map(list.map((d, i) => [d.id, -90 + (360 / list.length) * i]));
  const center = polar(R, angle);
  const slots = [0, 1, 2, 3].map((k) => polar(38, angle + 45 + k * 90));
  const want = own.map((id) => {
    let x = 0;
    let y = 0;
    let n = 0;
    for (const thread of props.atlas.threads) {
      if (!thread.tasks.includes(id)) continue;
      for (const other of thread.tasks) {
        const d = other.split("_")[0];
        if (other === id || d === id.split("_")[0]) continue;
        const p = polar(R, order.get(d));
        x += p.x - center.x;
        y += p.y - center.y;
        n += 1;
      }
    }
    return { id, x, y, n };
  });
  want.sort((a, b) => b.n - a.n);
  const out = [null, null, null, null];
  for (const task of want) {
    let best = -1;
    let score = -Infinity;
    slots.forEach((slot, k) => {
      if (out[k]) return;
      const s = task.n ? (slot.x * task.x + slot.y * task.y) / Math.hypot(task.x, task.y) : -(slot.x * center.x + slot.y * center.y) / R;
      if (s > score) { score = s; best = k; }
    });
    out[best] = task.id;
  }
  return out;
}

const domains = computed(() => {
  const list = props.atlas.domains;
  const ids = Object.keys(props.atlas.labels);
  // Neighbouring disciplines sit next to each other on the ring.
  return list.map((domain, index) => {
    const angle = -90 + (360 / list.length) * index;
    const center = polar(R, angle);
    const text = polar(R + 112, angle);
    const cos = Math.cos((angle * Math.PI) / 180);
    const own = placeStars(ids.filter((id) => id.startsWith(`${domain.id}_`)).sort(), angle, list);
    return {
      ...domain,
      angle,
      
      color: tint(domain),
      ...center,
      inner: polar(R - 110, angle),
      text: { x: text.x, y: text.y - 4, anchor: Math.abs(cos) < 0.3 ? "middle" : cos > 0 ? "start" : "end" },
      tasks: own.map((id, k) => {
        const p = polar(38, angle + 45 + k * 90);
        if (!id) return null;
        return { id, label: props.atlas.labels[id], x: +(center.x + p.x).toFixed(1), y: +(center.y + p.y).toFixed(1), color: tint(domain) };
      }).filter(Boolean),
    };
  });
});

const stars = computed(() => {
  const map = new Map();
  for (const domain of domains.value) for (const task of domain.tasks) map.set(task.id, { ...task, domain: domain.id, angle: domain.angle });
  return map;
});

const edges = computed(() => {
  const out = [];
  for (const thread of props.atlas.threads) {
    for (let i = 0; i < thread.tasks.length - 1; i += 1) {
      const a = stars.value.get(thread.tasks[i]);
      const b = stars.value.get(thread.tasks[i + 1]);
      if (!a || !b) continue;
      const mx = (a.x + b.x) / 2;
      const my = (a.y + b.y) / 2;
      // Cross-discipline links bow toward the core; links inside one discipline bow outward.
      const pull = a.domain === b.domain ? 1.35 : 0.32;
      const d = `M${a.x} ${a.y} Q${(mx * pull).toFixed(1)} ${(my * pull).toFixed(1)} ${b.x} ${b.y}`;
      const span = Math.hypot(a.x - b.x, a.y - b.y);
      out.push({ key: `${thread.id}-${i}`, thread: thread.id, a, b, d, dur: (2.5 + span / 160).toFixed(1), delay: ((out.length * 0.37) % 4).toFixed(2) });
    }
  }
  return out;
});

const ticks = Array.from({ length: 120 }, (_, k) => {
  const major = k % 12 === 0;
  const a = polar(505, k * 3 - 90);
  const b = polar(major ? 486 : 496, k * 3 - 90);
  return { k, major, x1: a.x, y1: a.y, x2: b.x, y2: b.y };
});

const active = computed(() => {
  const tasks = new Set();
  const threads = new Set();
  const domainsOn = new Set();
  const hot = props.hot;
  if (hot) {
    const all = props.atlas.threads;
    if (hot.kind === "thread") {
      threads.add(hot.id);
    } else if (hot.kind === "task") {
      tasks.add(hot.id);
      for (const t of all) if (t.tasks.includes(hot.id)) threads.add(t.id);
    } else if (hot.kind === "domain") {
      domainsOn.add(hot.id);
      for (const t of all) if (t.tasks.some((id) => id.startsWith(`${hot.id}_`))) threads.add(t.id);
      for (const id of stars.value.keys()) if (id.startsWith(`${hot.id}_`)) tasks.add(id);
    }
    for (const t of all) if (threads.has(t.id)) for (const id of t.tasks) tasks.add(id);
    for (const id of tasks) domainsOn.add(stars.value.get(id)?.domain);
  }
  return { tasks, threads, domains: domainsOn };
});

const tip = computed(() => {
  if (props.hot?.kind !== "task") return null;
  const star = stars.value.get(props.hot.id);
  if (!star) return null;
  const cos = Math.cos((star.angle * Math.PI) / 180);
  // Put the label on the inner side of the ring so it never collides with the discipline name.
  const inner = polar(R - 96, star.angle);
  return { id: star.id, label: star.label, x: inner.x, y: inner.y, anchor: Math.abs(cos) < 0.3 ? "middle" : cos > 0 ? "end" : "start" };
});
</script>
