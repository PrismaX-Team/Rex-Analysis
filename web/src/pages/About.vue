<template>
  <TopBar :bench="benchId" :version="version" />
  <main class="shell page">
    <p class="kicker">{{ bench?.name }} · About</p>
    <h1>{{ t("说明") }}</h1>
    <p class="lede">{{ t("这一版的任务包长什么样、怎么评分、怎么提交。") }}</p>

    <div class="doc-layout">
      <nav class="doc-toc" :aria-label="t('目录')">
        <a v-for="h in toc" :key="h.id" :href="`#${h.id}`" @click.prevent="jump(h.id)">{{ h.text }}</a>
      </nav>
      <div class="doc-main">
        <ScoreNote :bench="benchId" :version="version" />
        <article class="prose doc" v-html="html"></article>
      </div>
    </div>
  </main>
</template>

<script setup>
import { computed } from "vue";
import TopBar from "../components/TopBar.vue";
import ScoreNote from "../components/ScoreNote.vue";
import { getAbout, getAboutEn } from "../data/client";
import { useI18n } from "../i18n/useI18n";

const { t, en } = useI18n();
import { renderMarkdown } from "../data/markdown";
import { useBench } from "../data/useBench";

const { benchId, version, bench } = useBench();
const source = computed(() => (en.value ? getAboutEn(benchId.value, version.value) : getAbout(benchId.value, version.value)));

// Top-level "# " headings become sections; give them ids so the side index can jump to them.
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
