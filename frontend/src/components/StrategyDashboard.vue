<script setup>
import { ref } from 'vue';
import Step1Clustering from './Step1Clustering.vue';
import Step2Regression from './Step2Regression.vue';
import Step3Prescription from './Step3Prescription.vue';

// --- MOCK DATA FOR STEP 1 (Aligned with Backend Models) ---
const clusters = [
    {
        id: 1,
        name: "Cluster 1: 優等生 (High Performance)",
        desc: "高收入，醫療品質優異。",
        threshold: 11,
        colorClass: "bg-emerald-500",
        logic: "基準線較低 (11%)，因為資源充足，應有更高標準。"
    },
    {
        id: 2,
        name: "Cluster 2: 資源匱乏區 (Resource Deprived)",
        desc: "偏鄉或低收入，人口稀少。",
        threshold: 16,
        colorClass: "bg-orange-500",
        logic: "基準線較寬鬆 (16%)，考量地理與資源限制。"
    },
    {
        id: 3,
        name: "Cluster 3: 都市挑戰區 (Urban Challenge)",
        desc: "人口密集，需求高，再入院率偏高。",
        threshold: 18,
        colorClass: "bg-purple-500",
        logic: "基準線最高 (18%)，因應都會區複雜病患結構。"
    },
    {
        id: 4,
        name: "Cluster 4: 待改善 (Needs Improvement)",
        desc: "中等表現，仍有進步空間。",
        threshold: 14,
        colorClass: "bg-blue-400",
        logic: "標準基準線 (14%)，常規監管目標。"
    }
];

// --- MOCK DATA FOR STEP 2 ---
const scenarios = [
    {
        id: 'A',
        name: "情境 A：管理失效",
        type: "management",
        actualRate: 20,
        predictedRate: 15,
        desc: "正殘差大。"
    },
    {
        id: 'B',
        name: "情境 B：結構性困境",
        type: "structural",
        actualRate: 20,
        predictedRate: 20,
        desc: "殘差接近零。"
    }
];

const props = defineProps({
    autoSelectedClusterId: Number
});

const selectedCluster = ref(clusters[0]);
// Ensure we update if prop changes
import { watch } from 'vue';
watch(() => props.autoSelectedClusterId, (newId) => {
    if (newId) {
        const found = clusters.find(c => c.id === newId);
        if (found) selectedCluster.value = found;
    }
});

const selectedScenario = ref(scenarios[0]);

const handleClusterSelect = (cluster) => {
    selectedCluster.value = cluster;
};

const handleScenarioSelect = (scenario) => {
    selectedScenario.value = scenario;
};

// Toggle for showing/hiding the dashboard (optional animation state)
const isOpen = ref(true);
</script>

<template>
    <div class="strategy-dashboard-wrapper w-full mt-12 mb-8 text-slate-800">

        <div class="flex items-center justify-between mb-4 px-1">
            <h2 class="text-xl font-bold text-slate-900 flex items-center gap-2">
                <span class="w-1.5 h-6 bg-blue-600 rounded-full"></span>
                CMS 公平性策略整合
            </h2>
            <button @click="isOpen = !isOpen"
                class="text-xs uppercase tracking-widest text-slate-500 hover:text-blue-600 font-semibold transition-colors">
                {{ isOpen ? '隱藏策略' : '展開策略' }} (Strategy)
            </button>
        </div>

        <div v-show="isOpen" class="bg-white rounded-3xl p-6 sm:p-8 space-y-4 border border-slate-200 shadow-xl">

            <!-- STEP 1 -->
            <Step1Clustering :clusters="clusters" :selectedCluster="selectedCluster"
                @select-cluster="handleClusterSelect" />

            <!-- STEP 2 -->
            <Step2Regression :scenarios="scenarios" :scenario="selectedScenario"
                @select-scenario="handleScenarioSelect" />

            <!-- STEP 3 -->
            <Step3Prescription :cluster="selectedCluster" :scenario="selectedScenario" />

        </div>

    </div>
</template>

<style scoped>
/* Removed heavy glassmorphism for cleaner light/white aesthetic */
</style>
