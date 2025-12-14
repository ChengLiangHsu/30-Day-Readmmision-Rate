<script setup>
import { computed } from 'vue';

const props = defineProps({
    scenario: Object,
    scenarios: Array
});

const emit = defineEmits(['select-scenario']);

// Calculate residual for display
const residual = computed(() => {
    if (!props.scenario) return 0;
    return (props.scenario.actualRate - props.scenario.predictedRate).toFixed(1);
});

const isManagementFailure = computed(() => {
    return props.scenario && props.scenario.type === 'management';
});

const barWidth = computed(() => {
    if (!props.scenario) return '0%';
    // Just a visual scaling for the bar
    const max = 25;
    return `${(props.scenario.actualRate / max) * 100}%`;
});

const predictedWidth = computed(() => {
    if (!props.scenario) return '0%';
    const max = 25;
    return `${(props.scenario.predictedRate / max) * 100}%`;
});

</script>

<template>
    <div class="step-container mt-8 pt-8 border-t border-slate-100">
        <div class="step-header">
            <div class="step-badge">第二步</div>
            <h3 class="text-xl font-bold text-slate-900">用「回歸」進行異常偵測</h3>
        </div>
        <p class="text-sm text-slate-500 mb-6 font-medium">
            科學偵測：計算 殘差 (Residual) = 實際再入院率 - 模型預測值。
        </p>

        <!-- Scenario Toggles -->
        <div class="flex space-x-2 mb-6">
            <button v-for="s in scenarios" :key="s.id" @click="emit('select-scenario', s)"
                class="px-3 py-1.5 rounded-full text-xs font-semibold transition-colors border"
                :class="scenario?.id === s.id ? 'bg-blue-600 border-blue-600 text-white shadow-md' : 'bg-white border-slate-200 text-slate-500 hover:border-blue-400 hover:text-blue-600'">
                {{ s.name }}
            </button>
        </div>

        <!-- Visualization -->
        <div v-if="scenario"
            class="bg-slate-50 rounded-xl p-6 border border-slate-200 relative overflow-hidden shadow-inner">

            <!-- Chart Rows -->
            <div class="space-y-4 mb-6 relative z-10">
                <!-- Actual -->
                <div>
                    <div class="flex justify-between text-xs mb-1 text-slate-500 font-semibold">
                        <span>實際再入院率 (Actual)</span>
                        <span>{{ scenario.actualRate }}%</span>
                    </div>
                    <div class="h-3 bg-slate-200 rounded-full overflow-hidden w-full">
                        <div class="h-full bg-red-500 shadow-sm transition-all duration-700 ease-out"
                            :style="{ width: barWidth }"></div>
                    </div>
                </div>

                <!-- Predicted -->
                <div>
                    <div class="flex justify-between text-xs mb-1 text-slate-500 font-semibold">
                        <span>模型預測值 (Predicted)</span>
                        <span>{{ scenario.predictedRate }}%</span>
                    </div>
                    <div class="h-3 bg-slate-200 rounded-full overflow-hidden w-full relative">
                        <div class="h-full bg-blue-500 shadow-sm transition-all duration-700 ease-out"
                            :style="{ width: predictedWidth }"></div>
                        <!-- Dashed line to show delta -->
                        <div class="absolute top-0 bottom-0 border-r-2 border-dashed border-slate-400/50 transition-all duration-700"
                            :style="{ left: predictedWidth }"></div>
                    </div>
                </div>
            </div>

            <!-- Analysis Result -->
            <div class="flex items-center gap-4 p-4 rounded-lg border backdrop-blur-sm transition-all duration-500"
                :class="isManagementFailure ? 'bg-red-50 border-red-200 text-red-900' : 'bg-yellow-50 border-yellow-200 text-yellow-900'">

                <div class="text-3xl">
                    {{ isManagementFailure ? '🚨' : '🛡️' }}
                </div>

                <div>
                    <div class="text-xs uppercase tracking-widest font-bold opacity-70 mb-0.5">
                        分析判定 (Analysis Outcome)
                    </div>
                    <div class="font-bold text-lg leading-tight mb-1">
                        {{ isManagementFailure ? '管理失效 (Management Failure)' : '結構性困境 (Structural Issue)' }}
                    </div>
                    <p class="text-xs opacity-90 leading-relaxed font-medium">
                        <span v-if="isManagementFailure">
                            正殘差大 ({{ residual }}%)。該區表現顯著低於預期。
                            <strong class="text-red-700 font-bold block mt-1">行動：啟動稽核 (Audit)。</strong>
                        </span>
                        <span v-else>
                            殘差接近零 ({{ residual }}%)。數值高是大環境 (SDOH) 造成的。
                            <strong class="text-yellow-700 font-bold block mt-1">行動：不應罰款，應提供資源補助。</strong>
                        </span>
                    </p>
                </div>
            </div>

        </div>
    </div>
</template>

<style scoped>
.step-badge {
    @apply text-xs font-bold uppercase tracking-wider text-blue-600 mb-1;
}
</style>
