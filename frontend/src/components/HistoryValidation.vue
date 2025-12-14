<template>
  <div class="mt-12 bg-white rounded-3xl p-8 border border-slate-200 shadow-sm">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">歷史模型驗證 (Model Validation)</h2>
        <p class="text-slate-500 mt-1">對比歷年真實數據與模型預測結果</p>
      </div>
      <div v-if="loading" class="text-blue-500 font-medium">載入中...</div>
    </div>

    <div v-if="error" class="bg-red-50 text-red-600 p-4 rounded-xl">
      {{ error }}
    </div>

    <div v-else-if="!loading && historyData.length > 0">
      <!-- Controls -->
      <div class="mb-6 flex gap-4">
        <select v-model="selectedCounty" 
                class="bg-slate-50 border border-slate-200 text-slate-700 h-10 px-4 rounded-xl focus:outline-none focus:border-blue-500 transition-colors">
          <option v-for="county in counties" :key="county" :value="county">
            {{ county }}
          </option>
        </select>
        
        <div class="flex items-center gap-6 ml-auto">
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 rounded-full bg-blue-500"></div>
            <span class="text-sm font-medium text-slate-600">真實值 (Actual)</span>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 rounded-full bg-red-400 border-2 border-white shadow-sm"></div>
            <span class="text-sm font-medium text-slate-600">預測值 (Predicted)</span>
          </div>
        </div>
      </div>

      <!-- Chart Container -->
      <div class="relative h-64 w-full bg-slate-50 rounded-2xl border border-slate-100 p-4">
        <!-- Y-Axis Labels -->
        <div class="absolute left-0 top-0 bottom-0 w-12 flex flex-col justify-between text-xs text-slate-400 py-4 text-right pr-2">
          <span>20%</span>
          <span>15%</span>
          <span>10%</span>
          <span>5%</span>
          <span>0%</span>
        </div>

        <!-- SVG Chart -->
        <svg viewBox="0 0 100 100" preserveAspectRatio="none" class="absolute left-12 right-4 top-4 bottom-8 h-[calc(100%-3rem)] w-[calc(100%-4rem)] overflow-visible">
          <!-- Grid Lines -->
          <line x1="0" y1="0" x2="100" y2="0" stroke="#e2e8f0" vector-effect="non-scaling-stroke" stroke-dasharray="4"/>
          <line x1="0" y1="25" x2="100" y2="25" stroke="#e2e8f0" vector-effect="non-scaling-stroke" stroke-dasharray="4"/>
          <line x1="0" y1="50" x2="100" y2="50" stroke="#e2e8f0" vector-effect="non-scaling-stroke" stroke-dasharray="4"/>
          <line x1="0" y1="75" x2="100" y2="75" stroke="#e2e8f0" vector-effect="non-scaling-stroke" stroke-dasharray="4"/>
          <line x1="0" y1="100" x2="100" y2="100" stroke="#e2e8f0" vector-effect="non-scaling-stroke"/>

          <!-- Actual Line -->
          <path :d="actualPath" fill="none" stroke="#3b82f6" stroke-width="3" stroke-linecap="round" vector-effect="non-scaling-stroke"/>
          
          <!-- Predicted Line -->
          <path :d="predictedPath" fill="none" stroke="#f87171" stroke-width="3" stroke-dasharray="6 4" stroke-linecap="round" vector-effect="non-scaling-stroke"/>

          <!-- Points -->
          <g v-for="(point, idx) in chartPoints" :key="'p'+idx">
            <!-- Actual Point -->
            <circle :cx="point.x" :cy="point.actualY" r="4" fill="white" stroke="#3b82f6" stroke-width="2" 
                    class="hover:r-6 transition-all cursor-pointer">
              <title>{{ point.year }} Actual: {{ point.actualVal }}%</title>
            </circle>
            
            <!-- Predicted Point -->
            <circle :cx="point.x" :cy="point.predY" r="4" fill="white" stroke="#f87171" stroke-width="2"
                    class="hover:r-6 transition-all cursor-pointer">
              <title>{{ point.year }} Pred: {{ point.predVal }}%</title>
            </circle>
          </g>
        </svg>

        <!-- X-Axis Labels -->
        <div class="absolute left-12 right-4 bottom-0 h-6 flex justify-between text-xs text-slate-400">
          <span v-for="point in chartPoints" :key="'l'+point.year">{{ point.year }}</span>
        </div>
      </div>
      
      <!-- Stats -->
      <div class="mt-6 grid grid-cols-3 gap-4">
         <div class="bg-blue-50 p-4 rounded-xl border border-blue-100">
             <div class="text-xs text-blue-400 uppercase font-bold">平均誤差 (MAE)</div>
             <div class="text-2xl font-bold text-blue-600">{{ mae }}%</div>
         </div>
         <div class="bg-slate-50 p-4 rounded-xl border border-slate-100">
             <div class="text-xs text-slate-400 uppercase font-bold">資料筆數</div>
             <div class="text-2xl font-bold text-slate-700">{{ countyData.length }}</div>
         </div>
         <div class="bg-slate-50 p-4 rounded-xl border border-slate-100">
             <div class="text-xs text-slate-400 uppercase font-bold">平均預測變動</div>
             <div class="text-2xl font-bold text-slate-700">{{ trendDirection }}</div>
         </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';

const historyData = ref([]);
const loading = ref(true);
const error = ref(null);
const selectedCounty = ref('');

const counties = computed(() => {
  return [...new Set(historyData.value.map(d => d.County))].sort();
});

const countyData = computed(() => {
  return historyData.value
    .filter(d => d.County === selectedCounty.value)
    .sort((a, b) => a.Year - b.Year); 
});

const chartPoints = computed(() => {
  if (countyData.value.length === 0) return [];
  const data = countyData.value;
  const count = data.length;
  
  // Calculate X positions (percentage)
  // Calculate Y positions (scale 0-20%)
  const maxY = 20;
  
  return data.map((d, i) => {
    const x = i / (count - 1 || 1) * 100;
    const actualY = 100 - (d['30-day Readmission Rate (Consolidated)'] / maxY * 100);
    const predY = 100 - (d['Predicted_Rate'] / maxY * 100);
    
    return {
      x: x, // Number 0-100
      actualY: actualY,
      predY: predY,
      actualVal: d['30-day Readmission Rate (Consolidated)'],
      predVal: d['Predicted_Rate']?.toFixed(1),
      year: d.Year
    };
  });
});

const actualPath = computed(() => {
  return generatePath(chartPoints.value, 'actualY');
});

const predictedPath = computed(() => {
  return generatePath(chartPoints.value, 'predY');
});

const mae = computed(() => {
    const data = countyData.value;
    if (!data.length) return 0;
    const sumDiff = data.reduce((acc, d) => acc + Math.abs(d['30-day Readmission Rate (Consolidated)'] - (d.Predicted_Rate || 0)), 0);
    return (sumDiff / data.length).toFixed(2);
});

const trendDirection = computed(() => {
    // Simple slope check of last point vs first
    if (!countyData.value.length) return '-';
    // Use predictions to see model trend
    const first = countyData.value[0].Predicted_Rate;
    const last = countyData.value[countyData.value.length - 1].Predicted_Rate;
    if (last > first + 1) return '上升 ↗';
    if (last < first - 1) return '下降 ↘';
    return '持平 →';
});

function generatePath(points, yKey) {
  if (points.length === 0) return '';
  // Convert percentages to roughly svg viewbox units if needed, but SVG supports percentage in d? 
  // No, path 'd' needs absolute coordinates relative to viewBox typically or percentages are tricky.
  // BUT: We can use viewBox="0 0 100 100" and use numeric coordinates without %.
  
  // Let's refactor computed logic to return numbers for viewBox logic
  // We used '%' strings in chartPoints, which works for cx/cy but not path d.
  // Let's fix chartPoints calculation slightly in logic below:
  return points.map((p, i) => {
    return `${i === 0 ? 'M' : 'L'} ${p.x} ${p[yKey]}`;
  }).join(' ');
}

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/history');
    if (!res.ok) throw new Error('API Failed');
    historyData.value = await res.json();
    
    // Default select
    if (counties.value.length > 0) {
      selectedCounty.value = 'Alameda'; // Or counties.value[0]
    }
  } catch (e) {
    console.error(e);
    error.value = "無法載入歷史數據，請確認後端服務正常運作 (Port 5000)。";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* SVG setup */
svg {
    /* Use percentage coordinate space via viewBox if possible, or just default user units 0-100 */
    /* If we assume the svg width is 100 units */
}
</style>
