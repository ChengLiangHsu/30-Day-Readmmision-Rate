<script setup>
import { computed } from 'vue';

const props = defineProps({
    selectedCluster: Object,
    clusters: Array
});

const emit = defineEmits(['select-cluster']);

const selectCluster = (cluster) => {
    emit('select-cluster', cluster);
};
</script>

<template>
    <div class="step-container">
        <div class="step-header">
            <div class="step-badge">第一步</div>
            <h3 class="text-xl font-bold text-slate-900">用「分群」建立公平的考核標準</h3>
        </div>
        <p class="text-sm text-slate-500 mb-4 font-medium">
            CMS 價值：確保監管的公平性 (Fairness)。
            <br>分群的作用是「定義賽道」，不同環境 = 不同閾值。
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <button v-for="cluster in clusters" :key="cluster.id" @click="selectCluster(cluster)"
                class="cluster-card relative overflow-hidden p-4 rounded-xl text-left transition-all duration-300 border"
                :class="selectedCluster?.id === cluster.id ? 'bg-blue-50 border-blue-500 shadow-md ring-1 ring-blue-200' : 'bg-slate-50 border-slate-200 hover:border-blue-300 hover:bg-white'">
                <div class="z-10 relative">
                    <div class="font-bold text-lg mb-1 text-slate-800">{{ cluster.name }}</div>
                    <div class="text-xs text-slate-500 mb-2">{{ cluster.desc }}</div>
                    <div class="flex items-center space-x-2">
                        <div
                            class="text-xs bg-white border border-slate-200 px-2 py-1 rounded shadow-sm text-slate-600">
                            基準線 (Threshold): <span class="font-mono font-bold text-blue-600">{{ cluster.threshold
                                }}%</span>
                        </div>
                    </div>
                </div>

                <!-- Decoration -->
                <div class="absolute -bottom-4 -right-4 w-20 h-20 rounded-full opacity-10" :class="cluster.colorClass">
                </div>
            </button>
        </div>

        <div v-if="selectedCluster" class="mt-4 p-4 rounded-lg bg-slate-50 border border-slate-200 text-sm">
            <span class="font-semibold text-blue-600">背後邏輯：</span>
            <span class="text-slate-600">{{ selectedCluster.logic }}</span>
        </div>
    </div>
</template>

<style scoped>
.step-badge {
    @apply text-xs font-bold uppercase tracking-wider text-blue-300 mb-1;
}

.cluster-card:hover {
    transform: translateY(-2px);
}
</style>
