<template>
  <header class="topbar">
    <div class="shell topbar-inner">
      <router-link class="brand" to="/">
        <span class="mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
        Rex-Analysis
      </router-link>
      <template v-if="meta">
        <span class="crumb" aria-hidden="true">/</span>
        <router-link class="bench-crumb" :to="meta.entry">{{ meta.name }}</router-link>
        <VersionSelect v-if="version && multi" :bench="bench" :version="version" />
      </template>
      <nav v-if="!meta" class="nav">
        <router-link to="/leaderboard">排行榜</router-link>
        <router-link to="/about">评测说明</router-link>
      </nav>
      <nav v-else-if="version" class="nav">
        <router-link :to="`/${bench}/${version}/leaderboard`">排行榜</router-link>
        <router-link :to="`/${bench}/${version}/tasks`">任务</router-link>
        <router-link :to="`/${bench}/${version}/about`">说明</router-link>
      </nav>
      <a v-if="meta?.github" class="github" :href="meta.github" target="_blank" rel="noreferrer">GitHub ↗</a>
      <ThemeToggle />
    </div>
  </header>
</template>

<script setup>
import { computed } from "vue";
import VersionSelect from "./VersionSelect.vue";
import ThemeToggle from "./ThemeToggle.vue";
import { getBench, getVersions } from "../data/client";

// No bench → site-level bar (排行榜 / 评测说明, no GitHub). With a bench → its own nav and repo.
const props = defineProps({
  bench: { type: String, default: "" },
  version: { type: String, default: "" },
});
const meta = computed(() => (props.bench ? getBench(props.bench) : null));
// Only offer a version switch once a bench actually has more than one version.
const multi = computed(() => getVersions(props.bench).length > 1);
</script>
