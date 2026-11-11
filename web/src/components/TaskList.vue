<template>
  <div>
    <div class="filters">
      <button type="button" :aria-pressed="domain === 'all'" @click="$emit('update:domain', 'all')">
        {{ t("全部") }}<small>{{ total }}</small>
      </button>
      <button
        v-for="item in domains"
        :key="item.id"
        type="button"
        :aria-pressed="domain === item.id"
        :style="{ '--c': colorOf(item.id) }"
        @click="$emit('update:domain', item.id)"
      ><i class="dot"></i>{{ item.label }}</button>
    </div>
    <div v-if="tasks.length" class="cards">
      <router-link
        v-for="task in tasks"
        :key="task.task_id"
        class="card"
        :style="{ '--c': colorOf(task.domain) }"
        :to="`/${bench}/${version}/tasks/${task.task_id}`"
      >
        <div class="card-top">
          <span class="id">{{ task.task_id }}</span>
          <span class="card-dom"><i class="dot"></i>{{ en ? task.domain_label_en || task.domain_label : task.domain_label }}</span>
        </div>
        <h3>{{ headline(task) }}</h3>
        <p>{{ task.summary }}</p>
        <div class="meta">
          <span class="pill">{{ task.data.length }} {{ t("个数据文件") }}</span>
          <span class="go">{{ t("查看题面 →") }}</span>
        </div>
      </router-link>
    </div>
    <div v-else class="empty">{{ t("这一版还没有公开任务。") }}</div>
  </div>
</template>

<script setup>
import { getTaskMeta } from "../data/client";
import { useI18n } from "../i18n/useI18n";

const { t, en } = useI18n();

const props = defineProps({
  bench: { type: String, required: true },
  version: { type: String, required: true },
  tasks: { type: Array, required: true },
  domains: { type: Array, required: true },
  domain: { type: String, required: true },
  total: { type: Number, default: 0 },
});
defineEmits(["update:domain"]);

const { domains: metaDomains, labels, labelsEn } = getTaskMeta(props.bench, props.version);
const colors = Object.fromEntries(metaDomains.map((d) => [d.id, d.color]));
const colorOf = (id) => colors[id] || "var(--accent)";
// The public title is a long English sentence; prefer the short curated name when there is one.
const headline = (task) => (en.value ? labelsEn[task.task_id] || labels[task.task_id] : labels[task.task_id]) || task.title;
</script>
