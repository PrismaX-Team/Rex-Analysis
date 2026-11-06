<template>
  <div class="cm">
    <section v-for="g in groups" :key="g.id" class="cm-group">
      <header class="cm-head">
        <h3>{{ g.label }}</h3>
        <p v-if="g.desc">{{ g.desc }}</p>
      </header>
      <Marquee :seconds="g.members.length * 5">
        <a v-for="m in g.members" :key="m.name" class="cm-card" :href="m.url" target="_blank" rel="noreferrer">
          <img v-if="m.photo" :src="`${base}committee/${m.photo}`" :alt="m.name" loading="lazy" />
          <span v-else class="cm-initial" aria-hidden="true">{{ m.name.slice(0, 1) }}</span>
          <b>{{ m.name }}</b>
          <span class="cm-title">{{ m.title }}</span>
          <span v-if="m.affiliation" class="cm-aff">{{ m.affiliation }}</span>
        </a>
      </Marquee>
    </section>
  </div>
</template>

<script setup>
import Marquee from "./Marquee.vue";
import { getCommittee } from "../data/client";

const base = import.meta.env.BASE_URL;
// A group with no members yet (academic committee) stays hidden until its list arrives.
const groups = getCommittee().groups.filter((g) => g.members.length);
</script>
