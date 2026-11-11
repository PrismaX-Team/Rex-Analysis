<template>
  <TopBar :bench="''" />
  <main class="shell page">
    <p class="kicker">Rex-Analysis · About</p>
    <h1>{{ t("评测说明") }}</h1>
    <p class="lede">{{ t("全站通用的规则在这里。每个 bench 的任务格式和评分细则，在它自己的说明页。") }}</p>

    <div class="doc-layout">
      <nav class="doc-toc" :aria-label="t('目录')">
        <a v-for="h in toc" :key="h.id" :href="`#${h.id}`" @click.prevent="jump(h.id)">{{ h.text }}</a>
        <a href="#benches" @click.prevent="jump('benches')">{{ t("各 bench 的说明") }}</a>
      </nav>
      <div class="doc-main">
        <article class="prose doc" v-html="html"></article>

        <section id="benches" class="prose doc">
          <h1>{{ t("各 bench 的说明") }}</h1>
        </section>
        <div class="site-cards">
          <router-link
            v-for="b in live"
            :key="b.id"
            class="site-card"
            :to="`${b.entry}/${b.version || '1.0'}/about`"
            :style="{ '--c': accentOf(b) }"
          >
            <span class="site-card-k">{{ b.short }} · {{ en ? b.task_type_en || b.task_type : b.task_type }}</span>
            <span class="site-card-name">{{ en ? b.name_en || b.name : b.name }}</span>
            <span class="site-card-desc">{{ en ? b.scoring_en || b.scoring : b.scoring }}</span>
            <span class="site-card-go">{{ t("评分规则 →") }}</span>
          </router-link>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { computed } from "vue";
import TopBar from "../components/TopBar.vue";
import { useTheme } from "../theme/useTheme";
import { getBenches, getSiteAbout, getSiteAboutEn } from "../data/client";
import { useI18n } from "../i18n/useI18n";

const { t, en } = useI18n();
import { renderMarkdown } from "../data/markdown";

const { theme } = useTheme();
const live = getBenches().filter((b) => b.status === "live");
const accentOf = (b) => (theme.value === "dark" ? b.accent_dark || b.accent : b.accent);

const source = computed(() => (en.value ? getSiteAboutEn() : getSiteAbout()));
const toc = computed(() =>
  source.value.split("\n").filter((l) => l.startsWith("# ")).map((l, i) => ({ id: `s${i}`, text: l.slice(2).trim() })),
);
const html = computed(() => {
  let i = 0;
  return renderMarkdown(source.value).replace(/<h1>/g, () => `<h1 id="s${i++}">`);
});

function jump(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}
</script>
