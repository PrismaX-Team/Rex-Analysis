<template>
  <TopBar :bench="''" />
  <main class="shell page">
    <p class="kicker">Rex-Analysis · Leaderboard</p>
    <h1>{{ t("排行榜") }}</h1>
    <p class="lede">{{ t("每个 bench 一张榜。这里是各榜的前五名，点一行进入该 bench 的完整榜。") }}</p>
    <p class="note">{{ t("各 bench 的分数只在同一个 bench 内可比，不合成总分。") }}</p>

    <OverallBoard />

    <h2 class="site-h">{{ t("各 bench 的完整榜") }}</h2>
    <div class="site-cards">
      <router-link
        v-for="b in live"
        :key="b.id"
        class="site-card"
        :to="`${b.entry}/${b.version || '1.0'}/leaderboard`"
        :style="{ '--c': accentOf(b) }"
      >
        <span class="site-card-k">{{ b.short }} · {{ en ? b.scoring_en || b.scoring : b.scoring }}</span>
        <span class="site-card-name">{{ en ? b.name_en || b.name : b.name }}</span>
        <span class="site-card-go">{{ t("完整榜 →") }}</span>
      </router-link>
    </div>
  </main>
</template>

<script setup>
import TopBar from "../components/TopBar.vue";
import OverallBoard from "../components/OverallBoard.vue";
import { useTheme } from "../theme/useTheme";
import { getBenches } from "../data/client";
import { useI18n } from "../i18n/useI18n";

const { t, en } = useI18n();

const { theme } = useTheme();
const live = getBenches().filter((b) => b.status === "live");
const accentOf = (b) => (theme.value === "dark" ? b.accent_dark || b.accent : b.accent);
</script>
