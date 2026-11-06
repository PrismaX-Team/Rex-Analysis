<template>
  <div class="mq" :class="{ rev: reverse }" :style="{ '--mq-t': `${seconds}s` }">
    <div class="mq-track">
      <div class="mq-group"><slot /></div>
      <!-- Second copy makes the -50% loop seamless; hidden from keyboard and screen readers. -->
      <div class="mq-group" aria-hidden="true" inert><slot /></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  seconds: { type: Number, default: 50 },
  reverse: { type: Boolean, default: false },
});
</script>
