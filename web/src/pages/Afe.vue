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

    <main class="afe-main">
      <section class="afe-hero">
        <p class="eyebrow"><span class="pulse"></span>frontier, still moving / 2026</p>
        <h1 class="wordmark">
          <span>AgentFrontier</span>
          <span class="grad">Exam 1.0</span>
        </h1>
        <p class="afe-tagline">{{ bench.tagline }}</p>
        <p class="afe-lede">{{ bench.summary }}</p>

        <dl class="rcb-stats">
          <div><dt>任务</dt><dd>{{ pack.tasks.length }}</dd></div>
          <div><dt>领域</dt><dd>{{ pack.domains.length }}</dd></div>
          <div><dt>设计原则</dt><dd>{{ philosophy.length }}</dd></div>
        </dl>
        <div class="rcb-go">
          <router-link class="go-solid" :to="`${base}/tasks`">浏览任务 →</router-link>
          <router-link class="go-ghost" :to="`${base}/about`">评测说明</router-link>
          <a class="go-ghost" :href="REX_URL" target="_blank" rel="noreferrer">参与共建 ↗</a>
        </div>
      </section>

      <section id="philosophy" class="afe-sec">
        <header class="afe-sec-head">
          <p class="eyebrow">设计哲学</p>
          <h2>一个能够持续向前的 Benchmark</h2>
        </header>
        <ol class="afe-phil">
          <li v-for="p in philosophy" :key="p.n">
            <span class="afe-phil-n">{{ p.n }}</span>
            <b>{{ p.name }}</b>
            <p>{{ p.text }}</p>
          </li>
        </ol>
      </section>

      <section id="domains" class="afe-sec">
        <header class="afe-sec-head">
          <p class="eyebrow">领域</p>
          <h2>每个领域单独出题、单独验证</h2>
          <p class="afe-sec-lede">题目来自真实、尚未解决的科学问题。智能体看到题面和数据，自己选方法、做计算，交出报告、代码和结果。</p>
        </header>
        <div class="afe-domains">
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
            <h3>{{ d.label }}</h3>
            <ul class="afe-samples">
              <li v-for="t in d.samples" :key="t.task_id">{{ t.label }}</li>
            </ul>
            <footer><span class="afe-go">看这 {{ d.count }} 题 →</span></footer>
          </router-link>
        </div>
      </section>

      <section v-if="featured" id="example" class="afe-sec">
        <header class="afe-sec-head">
          <p class="eyebrow">任务实例</p>
          <h2>{{ featured.label }}</h2>
          <p class="afe-inst-en">{{ featured.title }}</p>
        </header>
        <router-link class="afe-inst" :style="{ '--c': domainHue(featured.domain) }" :to="`${base}/tasks/${featured.task_id}`">
          <span class="afe-inst-tag">{{ featured.domain_label }}</span>
          <div class="afe-inst-body">
            <p class="afe-inst-q">{{ featured.summary }}</p>
            <ul class="afe-inst-data">
              <li v-for="f in featured.data" :key="f.path">{{ f.name }}<small>{{ f.size }}</small></li>
            </ul>
          </div>
          <span class="afe-inst-go">查看完整题面 →</span>
        </router-link>
      </section>

      <section class="afe-sec afe-committee">
        <p>由身处科学前沿的专家共同支持，顾问委员会参与任务遴选、科学审核与评测可信度。</p>
        <router-link to="/#team">看委员会成员 →</router-link>
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
import { getBench, getFeatured, getTasks } from "../data/client";

const bench = getBench("afe");
const version = bench.version || "1.0";
const base = `/afe/${version}`;
const pack = getTasks("afe", version);
const { theme } = useTheme();

// From the AFE task site (设计哲学). Verbatim, only the numbering is local.
const philosophy = [
  { n: "01", name: "Live Question", text: "评测的不是解决办法明确的静态题目，而是仍未解决、并值得不断推进的真实前沿问题。" },
  { n: "02", name: "Live Environment", text: "在开放环境下，模型可以检索调研问题的前沿方法，公开前沿是研究的起点，而不是需要隔离的信息。" },
  { n: "03", name: "Live Metric", text: "评分规则固定，但比较坐标持续更新；每个结果都相对于其他 Agent 和当前前沿进行衡量。" },
  { n: "04", name: "Live Community", text: "Benchmark 不是一次性封闭发布的题库，而由研究者、领域专家等贡献者持续共同发现、构建和完善。" },
  { n: "05", name: "Innovation", text: "评测关注的不是完成既定步骤，而是 Agent 能否把调研转化为经过验证的改进，在尚未解决的科学问题上取得可衡量的进展。" },
  { n: "06", name: "确定性验证", text: "Verifier 在运行前冻结，并在离线环境中评分；相同的冻结输入、Validation 历史、Context 和提交必须得到相同结果。" },
  { n: "07", name: "受控评测", text: "资源和网络边界预先固定，研究过程被完整记录与审计，防止 hacking、访问隐藏输入或通过绕过约束获得虚假高分。" },
];

const domainHue = (id) => {
  const d = pack.domains.find((x) => x.id === id);
  return d ? (theme.value === "dark" ? d.color_dark || d.color : d.color) : "var(--accent)";
};

// One task on show. The full statement lives on its own page; this is a taste of it.
const featured = computed(() => {
  const ids = getFeatured("afe");
  const pick = ids.map((id) => pack.tasks.find((t) => t.task_id === id)).find(Boolean) || pack.tasks[0];
  return pick || null;
});

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
