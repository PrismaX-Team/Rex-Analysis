<template>
  <div class="cm">
    <section v-for="g in groups" :key="g.id" class="cm-group">
      <header class="cm-head">
        <h3>{{ pick(g.label, g.label_en) }}</h3>
        <p v-if="g.desc">{{ pick(g.desc, g.desc_en) }}</p>
      </header>
      <Marquee :seconds="g.members.length * 5">
        <a v-for="m in g.members" :key="m.name" class="cm-card" :href="m.url" target="_blank" rel="noreferrer">
          <img v-if="m.photo" :src="`${base}committee/${m.photo}`" :alt="pick(m.name, m.name_en)" loading="lazy" />
          <span v-else class="cm-initial" aria-hidden="true">{{ pick(m.name, m.name_en).slice(0, 1) }}</span>
          <b>{{ pick(m.name, m.name_en) }}</b>
          <span class="cm-title">{{ pick(m.title, m.title_en) }}</span>
          <span v-if="m.affiliation" class="cm-aff">{{ pick(m.affiliation, m.affiliation_en) }}</span>
        </a>
      </Marquee>
    </section>
  </div>
</template>

<script setup>
import Marquee from "./Marquee.vue";
import { getCommittee } from "../data/client";
import { useI18n } from "../i18n/useI18n";

const base = import.meta.env.BASE_URL;
const { en } = useI18n();
// English when the data carries it, Chinese otherwise.
const pick = (zh, enText) => (en.value && enText ? enText : zh);
// A group with no members yet (academic committee) stays hidden until its list arrives.
const groups = getCommittee().groups.filter((g) => g.members.length);
</script>
