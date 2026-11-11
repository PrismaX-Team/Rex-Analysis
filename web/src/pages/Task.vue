<template>
  <TopBar :bench="benchId" :version="version" />
  <main class="shell page">
    <router-link class="back" :to="`${base}/tasks`">{{ t("← 全部任务") }}</router-link>
    <template v-if="task">
      <header class="task-head" :style="{ '--c': color }">
        <p class="kicker"><i class="dot"></i>{{ domainLabel }} · {{ task.task_id }}</p>
        <h1>{{ headline }}</h1>
        <p v-if="headline !== task.title" class="task-en">{{ task.title }}</p>
      </header>

      <div class="task-layout">
        <article class="prose task-body">
          <template v-if="task.statement">
            <div class="statement" v-html="statementHtml"></div>
          </template>
          <template v-else>
            <h2>{{ t("研究任务") }}</h2>
            <p class="task-statement">{{ task.task }}</p>
          </template>

          <h2>{{ t("数据") }} <small>{{ task.data.length }}</small></h2>
          <ul class="data-list">
            <li v-for="item in task.data" :key="item.path">
              <strong>{{ item.name }}<small v-if="item.size">{{ item.size }}</small></strong>
              <code>{{ item.path }}</code>
              <span v-if="item.description">{{ item.description }}</span>
            </li>
          </ul>
        </article>

        <aside class="task-side">
          <dl>
            <div><dt>{{ t("学科") }}</dt><dd><i class="dot" :style="{ '--c': color }"></i>{{ domainLabel }}</dd></div>
            <div><dt>{{ t("版本") }}</dt><dd>{{ version }}</dd></div>
            <div v-if="typeName"><dt>{{ t("类型") }}</dt><dd>{{ typeName }}</dd></div>
            <div><dt>{{ t("数据文件") }}</dt><dd>{{ task.data.length }}</dd></div>
          </dl>
          <a v-if="sourceUrl" class="side-btn" :href="sourceUrl" target="_blank" rel="noreferrer">{{ task.source_url ? t("公开任务包") : t("项目仓库") }} ↗</a>
          <p class="side-note">{{ en ? bench?.private_note_en || bench?.private_note : bench?.private_note }}</p>
        </aside>
      </div>
    </template>
    <div v-else class="empty">{{ t("没有这一题。") }}</div>
  </main>
</template>

<script setup>
import { computed } from "vue";
import TopBar from "../components/TopBar.vue";
import { getTask, getTaskMeta } from "../data/client";
import { renderMarkdown } from "../data/markdown";
import { useBench } from "../data/useBench";
import { useI18n } from "../i18n/useI18n";

const { t, en } = useI18n();

const { route, benchId, version, bench, base } = useBench();
const task = computed(() => getTask(benchId.value, version.value, route.params.taskId));
const meta = computed(() => getTaskMeta(benchId.value, version.value));
const headline = computed(() => {
  const id = task.value.task_id;
  return (en.value ? meta.value.labelsEn[id] || meta.value.labels[id] : meta.value.labels[id]) || task.value.title;
});
const color = computed(() => meta.value.domains.find((d) => d.id === task.value?.domain)?.color || "var(--accent)");
const typeName = computed(() => ({ reconstruction: "复现", discovery: "发现", abstraction: "抽象" })[task.value?.task_type] ? t({ reconstruction: "复现", discovery: "发现", abstraction: "抽象" }[task.value.task_type]) : "");
const domainLabel = computed(() => { const x = task.value; if (!x) return ""; return en.value ? x.domain_label_en || x.domain_label : x.domain_label; });
// AFE statements are the full markdown the agent reads; the first "# title" is already the page heading.
const statementHtml = computed(() => renderMarkdown(task.value.statement.replace(/^# .*\n+/, "")));
const sourceUrl = computed(() => task.value?.source_url || bench.value?.github || "");
</script>
