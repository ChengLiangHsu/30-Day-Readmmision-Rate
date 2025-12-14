<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  features: {
    type: Array,
    default: () => []
  },
  modelFeatures: {
    type: Array, // Names of features expected by model if known
    default: () => []
  },
  risk: {
    type: Number,
    default: 0
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['predict']);

const formData = ref({});

// Initialize form data when features change
watch(() => props.modelFeatures, (newFeatures) => {
  if (newFeatures && newFeatures.length > 0) {
    const defaults = {
      '30-day Readmits (Proportion)': 0.061295,
      'ICD Version(Ordinal)': 1,
      'PCPI_log': 10.766103,
      'Total Admits people(log)': 7.818028,
      'last_year_rate': 13.55
    };
    newFeatures.forEach(f => {
      if (!(f in formData.value)) {
        formData.value[f] = defaults[f] !== undefined ? defaults[f] : 0; 
      }
    });
  }
}, { immediate: true });

const featureLabels = {
  '30-day Readmits (Proportion)': '30天再入院率 (Proportion)',
  'ICD Version(Ordinal)': 'ICD 版本 (Ordinal)',
  'PCPI_log': '人均收入 (PCPI Log)',
  'Total Admits people(log)': '總住院人數 (Total Admits Log)',
  'last_year_rate': '去年比率 (Last Year Rate)'
};

const getLabel = (key) => featureLabels[key] || key;

const submit = () => {
  emit('predict', formData.value);
};
</script>

<template>
  <div class="w-full">
    <div class="">
      <h3 class="text-sm font-bold uppercase tracking-widest text-slate-400 mb-6 border-b border-slate-700 pb-2">
        手動變數輸入 (Manual Input Features)
      </h3>

      <div v-if="modelFeatures.length === 0" class="text-center py-4 text-slate-500">
        Feature list loading or empty...
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
        <div v-for="feature in modelFeatures" :key="feature" class="flex flex-col gap-1.5">
          <label class="text-xs font-semibold text-slate-400 uppercase tracking-wider ml-1 truncate" :title="feature">
            {{ getLabel(feature) }}
          </label>
          <input v-model="formData[feature]" type="number" step="any"
            class="w-full px-4 py-3 rounded-xl bg-slate-900/50 border border-slate-600 text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all font-mono text-sm"
            :placeholder="getLabel(feature)" />
        </div>
      </div>

      <div class="mt-8 flex items-center justify-between border-t border-slate-700 pt-6">
         <!-- Result Display -->
         <div>
            <div v-if="risk > 0 && !loading" class="flex flex-col animate-pulse-once">
               <span class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">預測風險 Model Prediction</span>
               <span class="text-3xl font-black text-indigo-400 font-mono">{{ risk.toFixed(2) }}%</span>
            </div>
            <div v-else-if="loading" class="text-sm text-slate-400">
               計算中 (Calculating)...
            </div>
            <div v-else class="text-sm text-slate-500">
               等待輸入 (Ready)
            </div>
         </div>

         <button @click="submit" :disabled="loading"
           class="px-8 py-3 bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 disabled:bg-slate-700 disabled:text-slate-500 text-white rounded-xl font-bold transition-all shadow-lg shadow-indigo-900/50 flex items-center gap-2">
           <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
             <path fill-rule="evenodd"
               d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z"
               clip-rule="evenodd" />
           </svg>
           {{ loading ? '計算中...' : '開始預測 (Run)' }}
         </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes pulse-once {
  0% { transform: scale(0.95); opacity: 0.5; }
  100% { transform: scale(1); opacity: 1; }
}
.animate-pulse-once {
  animation: pulse-once 0.3s ease-out forwards;
}
</style>
