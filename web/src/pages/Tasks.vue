<template>
  <TopBar :bench="benchId" :version="version" />
  <main class="shell page">
    <p class="kicker">{{ bench?.name }} · Tasks</p>
    <h1>任务</h1>
    <p class="lede">{{ bench?.tasks_lede }}</p>
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

const { route, benchId, version, bench } = useBench();
const domain = ref(typeof route.query.domain === "string" ? route.query.domain : "all");
const pack = computed(() => getTasks(benchId.value, version.value));

watch([benchId, version], () => {
  domain.value = typeof route.query.domain === "string" ? route.query.domain : "all";
});

const domains = computed(() => {
  const map = new Map();
  for (const task of pack.value.tasks) map.set(task.domain, task.domain_label);
  return [...map.entries()].map(([id, label]) => ({ id, label }));
});

const visible = computed(() => {
  if (domain.value === "all") return pack.value.tasks;
  return pack.value.tasks.filter((task) => task.domain === domain.value);
});
</script>
