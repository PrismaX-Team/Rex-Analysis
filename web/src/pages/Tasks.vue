<template>
  <TopBar :bench="benchId" :version="version" />
  <main class="shell page">
    <p class="kicker">{{ benchName }} · Tasks</p>
    <h1>{{ t("任务") }}</h1>
    <p class="lede">{{ en ? bench?.tasks_lede_en || bench?.tasks_lede : bench?.tasks_lede }}</p>
    <TaskList
      :bench="benchId"
      :version="version"
      :tasks="visible"
      :domains="domains"
      :domain="domain"
      :total="pack.tasks.length"
      @update:domain="domain = $event"
    />
  </main>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import TopBar from "../components/TopBar.vue";
import TaskList from "../components/TaskList.vue";
import { getTasks } from "../data/client";
import { useBench } from "../data/useBench";
import { useI18n } from "../i18n/useI18n";

const { t, en } = useI18n();
const benchName = computed(() => (bench.value ? (en.value ? bench.value.name_en || bench.value.name : bench.value.name) : ""));

const { route, benchId, version, bench } = useBench();
const domain = ref(typeof route.query.domain === "string" ? route.query.domain : "all");
const pack = computed(() => getTasks(benchId.value, version.value));

watch([benchId, version], () => {
  domain.value = typeof route.query.domain === "string" ? route.query.domain : "all";
});

const domains = computed(() => {
  const map = new Map();
  for (const task of pack.value.tasks) map.set(task.domain, en.value ? task.domain_label_en || task.domain_label : task.domain_label);
  return [...map.entries()].map(([id, label]) => ({ id, label }));
});

const visible = computed(() => {
  if (domain.value === "all") return pack.value.tasks;
  return pack.value.tasks.filter((task) => task.domain === domain.value);
});
</script>
