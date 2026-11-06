import { computed } from "vue";
import { useRoute } from "vue-router";
import { getBench } from "./client";

// Bench + version from the URL, plus the base path every inner link is built from.
export function useBench() {
  const route = useRoute();
  const benchId = computed(() => route.params.bench);
  const version = computed(() => route.params.version);
  const bench = computed(() => getBench(benchId.value));
  const base = computed(() => `/${benchId.value}/${version.value}`);
  return { route, benchId, version, bench, base };
}
