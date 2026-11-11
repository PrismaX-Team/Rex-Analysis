<template>
  <div class="version-select" @keydown.esc="open = false">
    <button type="button" :aria-expanded="open" @click="open = !open">
      <strong>{{ current?.label }}</strong>
      <span class="status">{{ statusText[current?.status] }}</span>
      <i class="caret"></i>
    </button>
    <div v-if="open" class="menu" role="listbox">
      <button
        v-for="item in versions"
        :key="item.id"
        type="button"
        :aria-current="item.id === version"
        @click="choose(item.id)"
      >
        <span>{{ item.label }}</span>
        <span class="status">{{ statusText[item.status] }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getVersions } from "../data/client";
import { useI18n } from "../i18n/useI18n";

const props = defineProps({
  bench: { type: String, required: true },
  version: { type: String, required: true },
});


const open = ref(false);
const route = useRoute();
const router = useRouter();
const versions = getVersions(props.bench);
const { t } = useI18n();
const statusText = computed(() => ({ current: t("当前"), history: t("历史"), planned: t("规划中") }));
const current = computed(() => versions.find((item) => item.id === props.version));

function choose(id) {
  open.value = false;
  if (id === props.version) return;
  const name = route.name === "task" || route.name === "run" ? sectionHome(route.name) : route.name;
  const params = { ...route.params, version: id };
  if (name !== route.name) {
    router.push({ name, params: { bench: props.bench, version: id } });
    return;
  }
  router.push({ name, params });
}

function sectionHome(name) {
  if (name === "task") return "tasks";
  if (name === "run") return "leaderboard";
  return name;
}
</script>
