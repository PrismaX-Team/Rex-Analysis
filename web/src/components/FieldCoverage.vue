<template>
  <div class="fc">
    <div class="fc-top">
      <div class="fc-lead">
        <dl class="fc-nums">
          <div><dd>{{ domains.length }}</dd><dt>科学领域</dt></div>
          <div><dd>{{ subfieldCount }}</dd><dt>二级领域</dt></div>
        </dl>
        <p>覆盖从基础科学到医学与工程的主要学科。</p>
      </div>
      <div class="fc-chart">
        <ul class="fc-bars" aria-label="各领域在每个数据集中的任务数">
          <li v-for="d in domains" :key="d.name" :title="breakdown(d)">
            <span class="fc-name">{{ d.name }}</span>
            <span class="fc-bar">
              <i
                v-for="ds in datasets"
                v-show="d.counts[ds.id]"
                :key="ds.id"
                :class="ds.id"
                :style="{ width: `${(d.counts[ds.id] / maxTotal) * 100}%` }"
              ></i>
            </span>
            <span class="fc-val">{{ d.total }}</span>
          </li>
        </ul>
        <p class="fc-legend">
          <span v-for="ds in datasets" :key="ds.id"><i :class="ds.id"></i>{{ ds.legend }}</span>
        </p>
      </div>
    </div>

    <div class="fc-bottom">
      <div class="fc-rows">
        <Marquee v-for="(row, i) in rows" :key="i" :seconds="110 + i * 14" :reverse="i % 2 === 1">
          <span v-for="s in row" :key="s.name" class="fc-sub" :title="s.domain">{{ s.name }}</span>
        </Marquee>
      </div>
      <div class="fc-side">
        <strong>{{ covered }}</strong>
        <b>已有任务的领域</b>
        <p>{{ summary }}</p>
      </div>
    </div>

    <p class="fc-foot">统计范围随版本更新 · 更新于 {{ updated }}</p>
  </div>
</template>

<script setup>
import Marquee from "./Marquee.vue";
import { getFields } from "../data/client";

const { domains, datasets, updated } = getFields();
const subfieldCount = domains.reduce((n, d) => n + d.subfields.length, 0);
const maxTotal = Math.max(1, ...domains.map((d) => d.total));
// Count domains, not directions: how many of the domains each live dataset already has tasks in.
const live = datasets.filter((ds) => ds.status === "live");
const covered = domains.filter((d) => live.some((ds) => d.counts[ds.id] > 0)).length;
const summary = live.map((ds) => `${ds.short} ${domains.filter((d) => d.counts[ds.id] > 0).length} 个领域`).join(" · ");
const breakdown = (d) => datasets.map((ds) => `${ds.short} ${d.counts[ds.id]}`).join(" · ");

// The moving rows list sub-fields only (no task titles). Deal them across three rows so
// neighbours in a row come from different domains.
const all = domains.flatMap((d) => d.subfields.map((name) => ({ name, domain: d.name })));
const rows = [0, 1, 2].map((r) => all.filter((_, i) => i % 3 === r));
</script>
