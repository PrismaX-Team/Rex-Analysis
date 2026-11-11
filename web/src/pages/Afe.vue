<template>
  <div class="home afe">
    <div class="home-bg" aria-hidden="true"><i></i><i></i><i></i></div>

    <header class="home-bar">
      <router-link class="brand" to="/">
        <span class="mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
        Rex-Analysis
      </router-link>
      <span class="crumb" aria-hidden="true">/</span>
      <router-link class="bench-crumb" to="/afe">{{ pick(bench.name, bench.name_en) }}</router-link>
      <a class="github" :href="bench.github" target="_blank" rel="noreferrer">GitHub ↗</a>
      <LocaleToggle />
      <ThemeToggle />
    </header>

    <main class="afe-main">
      <section class="afe-hero">
        <p class="eyebrow"><span class="pulse"></span>frontier, still moving / 2026</p>
        <h1 class="wordmark">
          <span>AgentFrontier</span>
          <span class="grad">Exam 1.0</span>
        </h1>
        <p class="afe-tagline">{{ pick(bench.tagline, bench.tagline_en) }}</p>
        <p class="afe-lede">{{ pick(bench.summary, bench.summary_en) }}</p>

        <div class="rcb-go">
          <router-link class="go-solid" :to="`${base}/about`">{{ t("评测说明") }}</router-link>
          <a class="go-ghost" :href="REX_URL" target="_blank" rel="noreferrer">{{ t("参与共建 ↗") }}</a>
        </div>
      </section>

      <section id="philosophy" class="afe-sec">
        <header class="afe-sec-head">
          <p class="eyebrow">{{ t("设计哲学") }}</p>
          <h2>{{ t("一个能够持续向前的 Benchmark") }}</h2>
        </header>
        <ol class="afe-phil">
          <li v-for="p in philosophy" :key="p.n">
            <span class="afe-phil-n">{{ p.n }}</span>
            <b>{{ t(p.name) }}</b>
            <p>{{ t(p.text) }}</p>
          </li>
        </ol>
      </section>

      <section id="traits" class="afe-sec">
        <header class="afe-sec-head">
          <p class="eyebrow">{{ t("任务特性") }}</p>
          <h2>{{ t("一道题要满足四个条件") }}</h2>
        </header>
        <ul class="afe-traits">
          <li v-for="item in traits" :key="item.name">
            <b>{{ t(item.name) }}</b>
            <p>{{ t(item.text) }}</p>
          </li>
        </ul>
      </section>

      <section id="team" class="afe-sec afe-team">
        <header class="afe-sec-head">
          <p class="eyebrow">{{ t("团队") }}</p>
          <h2>{{ t("由身处科学前沿的专家共同支持") }}</h2>
        </header>
        <Committee />
      </section>
    </main>

    <footer class="home-foot">
      <span>{{ t("在未解决的科学问题上持续突破。") }}</span>
      <span>{{ pick(bench.name, bench.name_en) }}</span>
    </footer>
  </div>
</template>

<script setup>
import ThemeToggle from "../components/ThemeToggle.vue";
import Committee from "../components/Committee.vue";
import { REX_URL } from "../data/links";
import { getBench } from "../data/client";
import LocaleToggle from "../components/LocaleToggle.vue";
import { useI18n } from "../i18n/useI18n";

const { t, en } = useI18n();
const pick = (zh, enText) => (en.value && enText ? enText : zh);

const bench = getBench("afe");
const version = bench.version || "1.0";
const base = `/afe/${version}`;

// From the AFE task site (设计哲学), verbatim. Only the numbering is local.
const philosophy = [
  { n: "01", name: "Live Question", text: "评测的不是解决办法明确的静态题目，而是仍未解决、并值得不断推进的真实前沿问题。" },
  { n: "02", name: "Live Environment", text: "在开放环境下，模型可以检索调研问题的前沿方法，公开前沿是研究的起点，而不是需要隔离的信息。" },
  { n: "03", name: "Live Metric", text: "评分规则固定，但比较坐标持续更新；每个结果都相对于其他 Agent 和当前前沿进行衡量。" },
  { n: "04", name: "Live Community", text: "Benchmark 不是一次性封闭发布的题库，而由研究者、领域专家等贡献者持续共同发现、构建和完善。" },
  { n: "05", name: "Innovation", text: "评测关注的不是完成既定步骤，而是 Agent 能否把调研转化为经过验证的改进，在尚未解决的科学问题上取得可衡量的进展。" },
  { n: "06", name: "确定性验证", text: "Verifier 在运行前冻结，并在离线环境中评分；相同的冻结输入、Validation 历史、Context 和提交必须得到相同结果。" },
  { n: "07", name: "受控评测", text: "资源和网络边界预先固定，研究过程被完整记录与审计，防止 hacking、访问隐藏输入或通过绕过约束获得虚假高分。" },
];

// Also from the task site (任务特性).
const traits = [
  { name: "科学重要性", text: "结果变好后，应能推进真实研究问题或重要科学计算瓶颈。" },
  { name: "Verifier 可信度", text: "评分算法、输入、常数、容差、聚合和无效输出处理能够完整固定，并在本地、离线、确定性运行。" },
  { name: "前沿空间", text: "当前最佳可达结果仍未知，并有可信证据表明存在实质改进空间。" },
  { name: "长期可持续性", text: "数据、软件和验证路径能够稳定获得，不依赖脆弱服务、秘密凭证或不可重复的外部行为。" },
];

</script>
