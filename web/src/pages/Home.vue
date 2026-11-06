<template>
  <div class="hub">
    <div class="hub-bg" aria-hidden="true"><i></i><i></i><i></i></div>

    <header class="hub-bar">
      <router-link class="brand" to="/">
        <span class="mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
        Rex-Analysis
      </router-link>
      <nav class="hub-nav" aria-label="主导航">
        <a href="#benches" @click.prevent="jump('benches')">Benchmarks</a>
        <router-link to="/leaderboard">排行榜</router-link>
        <router-link to="/about">评测说明</router-link>
        <a :href="REX_URL" target="_blank" rel="noreferrer">提交科学问题 ↗</a>
      </nav>
      <ThemeToggle class="hub-theme" />
    </header>

    <main class="hub-main">
      <section class="hub-hero">
        <a class="hero-pill" href="#boards" @click.prevent="jump('boards')">
          <span class="pill-tag">{{ heroTag }}</span>
          <span>{{ newest.name }} 已上线</span>
          <span class="pill-arrow" aria-hidden="true">→</span>
        </a>
        <h1 class="hub-title">Rex-<span class="grad">Analysis</span></h1>
        <p class="hub-lede">面向科研智能体的评测平台。真实研究任务，独立完成，公开评分。</p>
        <div class="hero-go">
          <a class="go-solid" href="#boards" @click.prevent="jump('boards')">浏览评测榜单</a>
          <a class="go-ghost" href="#benches" @click.prevent="jump('benches')">查看全部 Benchmarks</a>
        </div>
        <a class="scroll-cue" href="#boards" @click.prevent="jump('boards')" aria-label="向下浏览">
          <span>向下浏览</span><i aria-hidden="true"></i>
        </a>
      </section>

      <!-- Rotating glance at each bench's leaderboard: its own section under the hero. -->
      <section id="boards" class="hub-section">
        <header class="section-head">
          <h2>评测榜单</h2>
          <p>每个 bench 一张榜，自动轮播，鼠标停留时暂停。</p>
        </header>
        <div
          class="hero-board"
          aria-roledescription="carousel"
          aria-label="排行榜轮播"
          @pointerenter="paused = true"
          @pointerleave="paused = false"
          @focusin="paused = true"
          @focusout="paused = false"
        >
          <div class="hb-track" :style="{ transform: `translateX(-${index * 100}%)` }">
            <section
              v-for="(slide, i) in slides"
              :key="slide.key"
              class="hb-slide"
              :aria-hidden="i !== index"
              :style="{ '--c': slide.color }"
            >
              <div class="hb-intro">
                <span class="hb-k">{{ slide.live ? "LIVE" : "COMING SOON" }} · {{ slide.bench }}</span>
                <h3 class="hb-name">{{ slide.name }}</h3>
                <p class="hb-desc">{{ slide.desc }}</p>
                <p class="hb-foot">{{ slide.live ? slide.foot : "榜单将在 bench 上线后出现" }}</p>
                <router-link v-if="slide.live" class="hb-more" :to="slide.to" :tabindex="i === index ? 0 : -1">完整榜单 →</router-link>
              </div>
              <div v-if="slide.live && !slide.rows.length" class="hb-pending">
                <strong>{{ slide.tasks }}</strong>
                <span>道任务已公开</span>
                <p>成绩公开后，这里会显示前五名。</p>
                <router-link :to="`${slide.base}/tasks`" :tabindex="i === index ? 0 : -1">浏览任务 →</router-link>
              </div>
              <ol v-else-if="slide.live" class="hb-rows">
                <li v-for="row in slide.rows" :key="row.run_id">
                  <router-link :to="`${slide.base}/runs/${row.run_id}`" :tabindex="i === index ? 0 : -1">
                    <span class="hb-rank">{{ row.rank }}</span>
                    <span class="hb-sys">{{ row.system }}<small>{{ row.model || `${row.task_count} / 40 题` }}</small></span>
                    <span class="hb-bar" aria-hidden="true"><i :style="{ width: `${(row.score / slide.max) * 100}%` }"></i></span>
                    <span class="hb-score">{{ row.score.toFixed(2) }}</span>
                  </router-link>
                </li>
              </ol>
              <ol v-else class="hb-rows hb-ghost" aria-hidden="true">
                <li v-for="n in 5" :key="n"><span></span><span></span><span></span><span></span></li>
              </ol>
            </section>
          </div>
          <nav v-if="slides.length > 1" class="hb-nav" aria-label="切换榜单">
            <button type="button" class="hb-arrow" aria-label="上一个" @click="go(index - 1)">‹</button>
            <button
              v-for="(slide, i) in slides"
              :key="`dot-${slide.key}`"
              type="button"
              class="hb-dot"
              :class="{ on: i === index, run: i === index && !paused && moving }"
              :aria-label="slide.name"
              :aria-current="i === index"
              @click="go(i)"
            ><i :style="{ animationDuration: `${INTERVAL}ms` }"></i></button>
            <button type="button" class="hb-arrow" aria-label="下一个" @click="go(index + 1)">›</button>
          </nav>
        </div>
      </section>

      <section id="benches" class="hub-section">
        <header class="section-head">
          <h2>Benchmarks</h2>
          <p>{{ benches.length }} 个已上线，更多 bench 正在筹备。点卡片进入该 bench 的榜、题和说明。</p>
        </header>

        <div class="hub-grid">
          <router-link
            v-for="bench in benches"
            :key="bench.id"
            :to="bench.entry"
            class="bench is-live"
            :style="{ '--c': accentOf(bench) }"
          >
            <header class="bench-head">
              <span class="bench-tag">LIVE</span>
              <span class="bench-mono">{{ bench.short }}</span>
            </header>
            <h3 class="bench-name">{{ bench.name }}</h3>
            <p class="bench-tagline">{{ bench.tagline }}</p>
            <p class="bench-summary">{{ bench.summary }}</p>
            <dl class="bench-stats">
              <div v-for="s in statsOf(bench)" :key="s.label">
                <dt>{{ s.label }}</dt>
                <dd>{{ s.value }}</dd>
              </div>
            </dl>
            <footer class="bench-foot">
              <span class="bench-chip">{{ bench.task_type }}</span>
              <span class="bench-chip ghost">{{ bench.scoring }}</span>
              <span class="bench-go">进入 →</span>
            </footer>
          </router-link>

          <!-- Reserved slots for benches still to come. -->
          <div v-for="n in slots" :key="`slot-${n}`" class="bench slot" aria-label="即将上线的 bench">
            <header class="bench-head">
              <span class="bench-tag">COMING SOON</span>
              <span class="bench-mono">#{{ String(benches.length + n).padStart(2, "0") }}</span>
            </header>
            <div class="slot-body">
              <span class="slot-bar w70"></span>
              <span class="slot-bar w40"></span>
              <span class="slot-bar w90"></span>
              <span class="slot-bar w60"></span>
            </div>
            <p class="slot-text">新的 bench 筹备中</p>
          </div>
        </div>
      </section>

      <section id="rex" class="hub-section">
        <header class="section-head">
          <h2>关于 ReX</h2>
          <p>ReX 科学共研计划：把真实的科研难题交给模型和智能体，先和提出者对齐目标，再攻关、再验证。</p>
        </header>
        <div class="rex">
          <div class="rex-intro">
            <span class="rex-k">ReX 科学共研计划 · 上海人工智能实验室</span>
            <h3 class="rex-name"><span class="grad">Re</span>X</h3>
            <p class="rex-word">
              <b>Re</b> 是 Research，也是 Recursive：求解、验证、反馈，循环往复。
              <b>X</b> 是任意一个科学任务。
            </p>
            <p class="rex-desc">
              研究者提交科学问题，书生·端砚调用基础模型、科学智能体和算力去攻关。每次合作只盯一个可独立验证的阶段目标，
              开工前先约定问题、可用的数据和条件，以及怎样算成功。
            </p>
            <div class="rex-go">
              <a class="rex-btn" :href="REX_URL" target="_blank" rel="noreferrer">提交科学问题 ↗</a>
              <span class="rex-note">中英文均可，方案不完整也能先交</span>
            </div>
          </div>

          <div class="rex-body">
            <ol class="rex-levels">
              <li v-for="lv in levels" :key="lv.id" :class="lv.id">
                <span class="lv-id">{{ lv.id }}</span>
                <div>
                  <p class="lv-name">{{ lv.name }}<small>{{ lv.zone }}</small></p>
                  <p class="lv-text">{{ lv.text }}</p>
                </div>
              </li>
            </ol>
            <div class="rex-flow-wrap">
              <ol class="rex-flow" role="tablist" aria-label="合作流程">
                <li v-for="(st, i) in flow" :key="st.title">
                  <button
                    type="button"
                    role="tab"
                    :aria-selected="step === i"
                    :class="{ on: step === i, done: i < step }"
                    @click="step = i"
                  ><span>{{ String(i + 1).padStart(2, "0") }}</span>{{ st.title }}</button>
                </li>
              </ol>
              <p class="rex-step" role="tabpanel">{{ flow[step].text }}</p>
            </div>
          </div>
        </div>
      </section>

      <section id="overall" class="hub-section">
        <header class="section-head">
          <h2>Leaderboard</h2>
          <p>每个 bench 的模型前五名。分数只在同一个 bench 内可比。</p>
        </header>
        <OverallBoard />
      </section>

      <section id="fields" class="hub-section">
        <header class="section-head">
          <h2>覆盖领域</h2>
          <p>所有数据集的学科版图。</p>
        </header>
        <FieldCoverage />
      </section>

      <section id="team" class="hub-section">
        <header class="section-head">
          <h2>团队</h2>
          <p>由身处科学前沿的专家共同支持。</p>
        </header>
        <Committee />
      </section>

      <section id="how" class="hub-section">
        <header class="section-head">
          <h2>如何参与</h2>
          <p>不论你是来看结果，还是来提交自己的智能体，都从这三步开始。</p>
        </header>
        <ol class="how">
          <li v-for="step in how" :key="step.n">
            <component
              :is="step.href ? 'a' : 'router-link'"
              class="how-card"
              v-bind="step.href ? { href: step.href, target: '_blank', rel: 'noreferrer' } : { to: step.to }"
            >
              <span class="how-n">{{ step.n }}</span>
              <h3>{{ step.title }}</h3>
              <p>{{ step.text }}</p>
              <span class="how-go">{{ step.go }}</span>
            </component>
          </li>
        </ol>
      </section>
    </main>

    <footer class="hub-foot">
      <span>各 bench 的分数不可横比，评分规则见各自的说明页。</span>
      <a href="mailto:xu_wanghan@sjtu.edu.cn">联系我们</a>
    </footer>
  </div>
</template>

<script setup>
import { REX_URL } from "../data/links";
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import ThemeToggle from "../components/ThemeToggle.vue";
import OverallBoard from "../components/OverallBoard.vue";
import FieldCoverage from "../components/FieldCoverage.vue";
import Committee from "../components/Committee.vue";
import { useTheme } from "../theme/useTheme";
import { getBenches, getBenchSlots, getCarouselSize, getLeaderboard, getTasks } from "../data/client";

const { theme } = useTheme();

// Condensed from the ReX page: three task levels and the four-step collaboration.
const levels = [
  { id: "L1", name: "成果再发现", zone: "Re-Discovery", text: "隐去原结论，只给已有数据，看能否把关键发现重新做出来。" },
  { id: "L2", name: "求解与创新", zone: "开放问题", text: "通过计算、分析或有限的湿实验，在开放问题上拿到可度量的进展。" },
  { id: "L3", name: "原创突破", zone: "New-Discovery", text: "提出原创假设，并用真实的湿实验去检验。" },
];
const flow = [
  { title: "提交科学问题", text: "在 ReX 页面填写表单：团队信息、科学问题与阶段目标、任务设计与验证方式，并附一个带 README 的任务包。" },
  { title: "评估并约定目标", text: "团队评估问题的科学价值、可行性和资源需求，与提出者商定任务等级、技术对接方式和阶段目标。" },
  { title: "攻关与验证", text: "调用基础模型和科学智能体求解，每一步结果按事先约定的指标验证，不达标就回到求解。" },
  { title: "交付阶段报告", text: "交付阶段报告。经授权后，评测结果、失败案例和专家反馈会用于改进模型与智能体。" },
];
const step = ref(0);

const benches = getBenches();
const slots = getBenchSlots();
const live = benches.filter((b) => b.status === "live");
// The hero pill names the most recently added live bench.
const newest = [...live].sort((x, y) => (x.launched || "").localeCompare(y.launched || "")).at(-1);

// Static stats from benches.json, plus live ones read off the leaderboard so they never go stale.
function statsOf(bench) {
  const version = bench.version || "1.0";
  const board = getLeaderboard(bench.id, version);
  const pack = getTasks(bench.id, version);
  const disciplines = new Set(pack.tasks.map((t) => t.domain)).size;
  const first = board.groups?.[0];
  const rows = board.rows.filter((r) => !first || r.group === first.id);
  const top = rows.length ? Math.max(...rows.map((r) => r.score)).toFixed(2) : "–";
  return [
    { label: "任务", value: String(pack.tasks.length) },
    { label: "领域", value: String(disciplines) },
    { label: "提交", value: String(board.rows.length) },
    { label: first ? `${first.label}最高分` : "最高分", value: top },
  ];
}


const how = [
  { n: "01", title: "选一个 bench", text: "每个 bench 测一种科研能力。先读它的说明页：任务长什么样、怎么评分。", to: "/about", go: "读评测说明 →" },
  { n: "02", title: "跑完全部任务", text: "下载公开任务包，让你的智能体独立完成每一题，按格式交出报告和结果文件。", to: "/#benches", go: "选一个 bench →" },
  { n: "03", title: "评分并上榜", text: "用官方评测流程打分，把完整运行目录发给我们，核对后进入排行榜。", to: "/leaderboard", go: "看排行榜 →" },
];
// Pill on the hero: the most recently launched live bench and its launch month (benches.json "launched").
const heroTag = newest.launched ? `v${newest.launched.replace("-", ".")}` : `v${newest.version || "1.0"}`;

// One slide per bench: live benches show their top agents, reserved slots show a skeleton
// board so the carousel already reads as "several benches", matching the grid below.
const slides = computed(() => {
  const shown = live.map((bench) => {
    const version = bench.version || "1.0";
    const base = `${bench.entry}/${version}`;
    const board = getLeaderboard(bench.id, version);
    const first = board.groups?.[0];
    const rows = board.rows.filter((r) => !first || (r.group || "agent") === first.id);
    return {
      key: bench.id,
      live: true,
      bench: bench.short,
      name: bench.name,
      desc: bench.summary,
      max: Math.max(...rows.slice(0, 5).map((r) => r.score), 1),
      color: accentOf(bench),
      base,
      to: `${base}/leaderboard`,
      rows: rows.slice(0, 5),
      foot: board.rows.length ? `${bench.scoring} · 共 ${board.rows.length} 次提交` : `${bench.scoring}`,
      tasks: getTasks(bench.id, version).tasks.length,
    };
  });
  const size = getCarouselSize();
  const reserved = Array.from({ length: Math.max(0, Math.min(slots, size - shown.length)) }, (_, k) => ({
    key: `slot-${k}`,
    live: false,
    bench: `#${String(shown.length + k + 1).padStart(2, "0")}`,
    name: "新的 bench 筹备中",
    desc: "新的研究任务包正在准备。上线后，这里会显示它的前五名。",
    color: "var(--muted)",
  }));
  return [...shown, ...reserved].slice(0, size);
});

// Auto-advance; pauses on hover/focus and is off entirely for reduced motion.
const INTERVAL = 6000;
const index = ref(0);
const paused = ref(false);
const moving = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
let timer = 0;

function go(i) {
  const n = slides.value.length;
  index.value = ((i % n) + n) % n;
  restart();
}

function restart() {
  clearInterval(timer);
  if (!moving || slides.value.length < 2) return;
  timer = setInterval(() => { if (!paused.value) index.value = (index.value + 1) % slides.value.length; }, INTERVAL);
}

onMounted(restart);
onBeforeUnmount(() => clearInterval(timer));

function accentOf(bench) {
  return theme.value === "dark" ? bench.accent_dark || bench.accent : bench.accent;
}

function jump(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}
</script>
