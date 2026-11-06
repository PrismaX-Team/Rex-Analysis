<template>
  <p v-if="meta" class="note">{{ meta.score_name }} · {{ meta.score_note }}</p>
</template>

<script setup>
import { computed } from "vue";
import { getVersion } from "../data/client";

const props = defineProps({
  bench: { type: String, required: true },
  version: { type: String, required: true },
});

const meta = computed(() => getVersion(props.bench, props.version));
</script>
