<script setup>
import { computed } from 'vue';

const props = defineProps({
  risk: {
    type: Number,
    required: true // 0 to 1
  },
  loading: Boolean
});

const percentage = computed(() => Math.round(props.risk * 100));

const colorClass = computed(() => {
  if (props.loading) return 'text-gray-400';
  if (props.risk < 0.3) return 'text-green-400 shadow-green-400/50';
  if (props.risk < 0.6) return 'text-yellow-400 shadow-yellow-400/50';
  return 'text-red-500 shadow-red-500/50';
});

const statusText = computed(() => {
  if (props.loading) return 'Calculating...';
  if (props.risk < 0.3) return 'Low Readmission Risk';
  if (props.risk < 0.6) return 'Moderate Risk';
  return 'High Readmission Risk';
});
</script>

<template>
  <div class="flex flex-col items-center justify-center p-8 transition-all duration-500">
    <div class="text-xl font-medium tracking-wide opacity-80 mb-2">30-Day Readmission Risk</div>
    
    <div v-if="loading" class="animate-pulse text-6xl font-thin text-white/50">
      --%
    </div>
    <div v-else class="text-8xl font-light tracking-tighter drop-shadow-lg" :class="colorClass">
      {{ percentage }}%
    </div>

    <div class="mt-4 text-lg font-medium tracking-wide text-white/90">
      {{ statusText }}
    </div>
  </div>
</template>
