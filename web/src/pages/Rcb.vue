<template>
  <div class="home" :class="{ open }">
    <div class="home-bg" aria-hidden="true"><i></i><i></i><i></i></div>

    <header class="home-bar">
      <router-link class="brand" to="/">
        <span class="mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
        Rex-Analysis
      </router-link>
      <span class="crumb" aria-hidden="true">/</span>
      <router-link class="bench-crumb" to="/rcb" @click="open = false">{{ pick(bench.name, bench.name_en) }}</router-link>
      <a class="github" :href="bench.github" target="_blank" rel="noreferrer">GitHub ↗</a>
      <LocaleToggle />
      <ThemeToggle />
    </header>

    <main class="home-main">
      <section class="hero">
        <p class="eyebrow"><span class="pulse"></span>From Re-Discovery to New-Discovery</p>
        <h1 class="wordmark">
          <span>ResearchClaw</span>
          <span class="grad">Bench</span>
        </h1>
        <p class="hero-lede">
          {{ t("每个任务包来自一篇真实的论文：题面、数据、相关工作都给你，答案藏在评分清单里。") }}
          {{ t("智能体要像研究者一样，独立把这项研究做一遍。") }}
        </p>

        <dl class="rcb-stats">
          <div><dt>{{ t("任务") }}</dt><dd>{{ taskTotal }}</dd></div>
          <div><dt>{{ t("学科") }}</dt><dd>{{ atlas.domains.length }}</dd></div>
          <div><dt>{{ t("提交") }}</dt><dd>{{ runCount }}</dd></div>
          <div class="zone-up" :title="t('前沿（全榜每题最高分）达到 50 的题数')"><dt>{{ t("越过原论文") }}</dt><dd>{{ overCount }}<small>/{{ taskTotal }}</small></dd></div>
          <div><dt>{{ en ? "Best " + (board.groups?.[0]?.label_en || "score") : `${board.groups?.[0]?.label}最高分` }}</dt><dd>{{ best }}</dd></div>
        </dl>
        <div class="rcb-go">
          <router-link class="go-solid" to="/rcb/1.0/leaderboard">{{ t("排行榜 →") }}</router-link>
          <router-link class="go-ghost" to="/rcb/1.0/tasks">{{ en ? `Browse ${taskTotal} tasks` : `浏览 40 个任务` }}</router-link>
          <button type="button" class="go-ghost" @click="open = true">{{ t("展开星图") }}</button>
        </div>
      </section>

      <section class="stage" :class="{ open }">
        <div class="stage-pane">
          <div class="atlas-wrap" @click="!open && (open = true)">
            <Atlas
              :atlas="atlas"
              :interactive="open"
              :hot="open ? shown : null"
              @update:hot="hover"
              @domain="pin('domain', $event)"
              @task="pin('task', $event)"
            />
          </div>
        </div>

        <aside v-if="open" class="atlas-side">
          <button type="button" class="close" @click="open = false">{{ t("← 返回") }}</button>
          <p class="eyebrow">{{ t("RCB · 任务星图") }}</p>
          <h2>{{ t("四十篇论文，") }}<br />{{ t("散落在十个学科。") }}</h2>
          <p class="side-lede">
            {{ t("我们从十个学科各选了四篇论文，把每一篇还原成一个研究任务，交给智能体从头做一遍。") }}
          </p>
          <p class="side-lede">
            {{ t("放在一起看，它们并不孤立。同一种方法会在不同学科里反复出现：图神经网络从分子走到晶体，") }}
            {{ t("又走到网络流量；连接组既是神经科学的问题，也是视觉的问题。图上的每一条彩线，都是这样一次跨界。") }}
          </p>

          <div class="readout" :class="{ pinned: !!pinned && shown === pinned }">
            <Transition name="ro" mode="out-in">
              <div v-if="focus" :key="focusKey" class="ro-body">
                <p class="ro-id" :style="{ color: focus.color }">{{ focus.kicker }}</p>
                <p class="ro-title">{{ focus.title }}</p>
                <p class="ro-sub">{{ focus.sub }}</p>
                <div class="ro-foot">
                  <router-link v-if="focus.to" class="ro-go" :to="focus.to">{{ focus.go }}</router-link>
                  <span v-if="pinned && shown === pinned" class="ro-pin">{{ t("已选中 · 再点一次取消") }}</span>
                  <span v-else-if="focus.to" class="ro-pin">{{ t("点击可选中") }}</span>
                </div>
              </div>
              <p v-else key="empty" class="ro-empty">{{ t("停在一颗星上，看它是哪项研究；点一下把它留在这里。") }}</p>
            </Transition>
          </div>

          <p class="side-k">{{ t("跨学科的线索") }}</p>
          <ul class="threads-list">
            <li
              v-for="thread in threadRows"
              :key="thread.id"
              :class="{ on: shown?.kind === 'thread' && shown.id === thread.id }"
              @pointerenter="hover({ kind: 'thread', id: thread.id })"
              @pointerleave="hover(null)"
              @click="pin('thread', thread.id)"
            >
              <span class="chips"><i v-for="c in thread.colors" :key="c" :style="{ background: c }"></i></span>
              <span>{{ thread.label }}</span>
              <small>{{ thread.names }}</small>
            </li>
          </ul>

          <div class="side-go">
            <router-link to="/rcb/1.0/leaderboard">{{ t("看排行榜") }}</router-link>
            <router-link to="/rcb/1.0/tasks">{{ en ? `Browse ${taskTotal} tasks` : "浏览 40 个任务" }}</router-link>
          </div>
        </aside>
      </section>
    </main>

    <footer class="home-foot">
      <span>{{ t("RADS · 0–100 · 50 以下 Re-Discovery，50 以上 New-Discovery") }}</span>
      <span>{{ en ? `${taskTotal} tasks · ${atlas.domains.length} fields · ${runCount} submissions` : `40 题 · 10 学科 · ${runCount} 次提交` }}</span>
    </footer>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import Atlas from "../components/Atlas.vue";
import ThemeToggle from "../components/ThemeToggle.vue";
import { useTheme } from "../theme/useTheme";
import { getAtlas, getBench, getLeaderboard, getTasks } from "../data/client";
import LocaleToggle from "../components/LocaleToggle.vue";
import { useI18n } from "../i18n/useI18n";

const { t, en } = useI18n();
const pick = (zh, enText) => (en.value && enText ? enText : zh);
const bench = getBench("rcb");
const taskTotal = getTasks("rcb", "1.0").tasks.length;
const atlas = getAtlas("rcb", "1.0");
const board = getLeaderboard("rcb", "1.0");
const runCount = board.rows.length;
const lead = board.rows.filter((r) => r.group === board.groups?.[0]?.id);
const best = Math.max(...lead.map((r) => r.score)).toFixed(2);
const overCount = Object.values(board.frontier || {}).filter((f) => f.score >= 50).length;
const open = ref(false);
// What the panel shows: the hovered item if any, else the pinned one. Hover changes are
// settled for a moment so sweeping the pointer across the map doesn't flicker the panel.
const hot = ref(null);
const pinned = ref(null);
const shown = computed(() => hot.value || pinned.value);
let settle = 0;

function hover(item) {
  clearTimeout(settle);
  const same = (a, b) => a?.kind === b?.kind && a?.id === b?.id;
  if (same(item, hot.value)) return;
  settle = setTimeout(() => { hot.value = item; }, item ? 140 : 260);
}

function pin(kind, id) {
  if (!open.value) return;
  clearTimeout(settle);
  const item = { kind, id };
  const again = pinned.value?.kind === kind && pinned.value?.id === id;
  pinned.value = again ? null : item;
  hot.value = null;
}

const domainOf = (id) => id.split("_")[0];
const domainMeta = new Map(atlas.domains.map((d) => [d.id, d]));
const { theme } = useTheme();
const hues = computed(() => Object.fromEntries(atlas.domains.map((d) => [d.id, (theme.value === "dark" && d.color_dark) || d.color])));
const nameOf = (d) => (en.value ? domainMeta.get(d)?.label_en || domainMeta.get(d)?.label : domainMeta.get(d)?.label) || d;

const threadRows = computed(() => {
  const hue = hues.value;
  return atlas.threads.map((thread) => {
    const ds = [...new Set(thread.tasks.map(domainOf))];
    return { ...thread, colors: ds.map((d) => hue[d]), names: ds.map(nameOf).join(" · ") };
  });
});

const focusKey = computed(() => (shown.value ? `${shown.value.kind}:${shown.value.id}` : ""));

const focus = computed(() => {
  const h = shown.value;
  const hue = hues.value;
  if (!h) return null;
  if (h.kind === "task") {
    const d = domainOf(h.id);
    const lines = atlas.threads.filter((t) => t.tasks.includes(h.id));
    const labelOf = (id) => (en.value ? atlas.labels_en?.[id] || atlas.labels[id] : atlas.labels[id]);
    const peers = [...new Set(lines.flatMap((t) => t.tasks).filter((id) => id !== h.id))].map(labelOf);
    return {
      kicker: `${nameOf(d)} · ${h.id}`,
      color: hue[d],
      title: en.value ? atlas.labels_en?.[h.id] || atlas.labels[h.id] : atlas.labels[h.id],
      sub: peers.length
        ? `沿着「${lines.map((t) => t.label).join("」「")}」，它和 ${peers.slice(0, 3).join("、")}${peers.length > 3 ? " 等" : ""} 走到了一起。`
        : t("它在这张图上独自成星。"),
      to: `/rcb/1.0/tasks/${h.id}`,
      go: t("查看题面 →"),
    };
  }
  if (h.kind === "domain") {
    const lines = atlas.threads.filter((t) => t.tasks.some((id) => domainOf(id) === h.id));
    const reach = [...new Set(lines.flatMap((t) => t.tasks.map(domainOf)).filter((d) => d !== h.id))];
    return {
      kicker: domainMeta.get(h.id).en,
      color: hue[h.id],
      title: reach.length ? `${nameOf(h.id)}，连着 ${reach.length} 个邻居` : nameOf(h.id),
      sub: reach.length ? `它通过${lines.map((t) => `「${t.label}」`).join("")}，与${reach.map(nameOf).join("、")}相遇。` : "",
      to: `/rcb/1.0/tasks?domain=${h.id}`,
      go: en.value ? `See the ${h.id} tasks →` : `看${nameOf(h.id)}的四道题 →`,
    };
  }
  const thread = threadRows.value.find((t) => t.id === h.id);
  return {
    kicker: thread.names,
    color: thread.colors[0],
    title: thread.label,
    sub: thread.tasks.map((id) => (en.value ? atlas.labels_en?.[id] || atlas.labels[id] : atlas.labels[id])).join(" → "),
  };
});

function onKey(event) {
  if (event.key === "Escape") open.value = false;
}
watch(open, (value) => {
  if (!value) {
    clearTimeout(settle);
    hot.value = null;
    pinned.value = null;
  }
});
onMounted(() => window.addEventListener("keydown", onKey));
onBeforeUnmount(() => window.removeEventListener("keydown", onKey));
</script>
