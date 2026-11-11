<template>
  <p v-if="meta" class="note">{{ meta.score_name }} · {{ en ? meta.score_note_en || meta.score_note : meta.score_note }}</p>
</template>

<script setup>
import { computed } from "vue";
import { getVersion } from "../data/client";
import { useI18n } from "../i18n/useI18n";

const { en } = useI18n();

const props = defineProps({
  bench: { type: String, required: true },
  version: { type: String, required: true },
});

const meta = computed(() => getVersion(props.bench, props.version));
</script>
