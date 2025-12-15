<script setup>
import { ref, onMounted } from 'vue';
import CountyDashboard from './components/CountyDashboard.vue';
import InputForm from './components/InputForm.vue';

const risk = ref(0);
const loading = ref(false);
const features = ref([]);
const showManualInput = ref(false); // Collapsible state

// We'll fallback to some common features if API fails just to show the UI
const fallbackFeatures = ['30-day Readmits (Proportion)', 'ICD Version(Ordinal)', 'PCPI_log', 'Total Admits people(log)', 'last_year_rate'];

const fetchFeatures = async () => {
    try {
        const response = await fetch('/features');
        const data = await response.json();
        if (data.features) {
            features.value = data.features;
        } else {
            console.warn("No features returned, using fallback");
            features.value = fallbackFeatures;
        }
    } catch (e) {
        console.error("Failed to fetch features", e);
        features.value = fallbackFeatures;
    }
};

const handlePredict = async (formData) => {
    loading.value = true;
    try {
        // 1. Get Risk Score
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const data = await response.json();
        if (data.risk_score !== undefined) {
            risk.value = typeof data.risk_score === 'number' ? data.risk_score : 0;
        }

        // 2. Refresh Cluster based on Manual Input (Optional if user wanted it, but current request is removing CMS dashboard)
        // However, user might still want clustering on InputForm even if Dashboard is gone?
        // User said "CMS ... block can be removed".
        // Code here just updates autoSelectedClusterId which was used by StrategyDashboard.
        // So we can remove the clustering logic here IF it was only for StrategyDashboard.
        // BUT, InputForm relies on `risk` state passed down.
        // CountyDashboard does its own clustering Fetch.
        // Manual Input might want clustering displayed? Maybe not. User didn't ask to remove Manual Input clustering, just the block.
        // We can keep the logic or remove if unused. Since StrategyDashboard is gone, autoSelectedClusterId is unused in App.vue.

    } catch (e) {
        console.error("Prediction failed", e);
        alert("Prediction failed. Check backend.");
    } finally {
        loading.value = false;
    }
};

const handleCountySelect = async (county) => {
    // This was used to update Strategy Dashboard. Since removed, we can simplify.
    // We keep it empty or remove if not needed.
};

onMounted(() => {
    fetchFeatures();
});
</script>

<template>
    <div class="min-h-screen w-full bg-slate-900 text-slate-100 font-sans selection:bg-indigo-500 selection:text-white">
        <div class="max-w-5xl mx-auto min-h-screen flex flex-col pt-8 px-6 pb-12">

            <!-- HEADER with Logo -->
            <div class="flex items-center gap-3 mb-10 pb-6 border-b border-slate-700">
                <!-- Logo Container -->
                <div
                    class="w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-900/20 overflow-hidden border border-slate-700">
                    <img src="/logo.png" alt="EquiCare Logo" class="w-full h-full object-cover opacity-90" />
                </div>
                <div>
                    <h1 class="text-2xl font-bold tracking-tight text-white">EquiCare Lens</h1>
                    <p class="text-xs font-semibold text-slate-400 tracking-wider uppercase">公平透鏡系統 • Protocol 11</p>
                </div>

                <!-- Model Score Badge -->
                <div class="ml-auto flex items-center gap-3">
                    <div
                        class="bg-indigo-500/10 border border-indigo-500/30 rounded-lg px-3 py-2 backdrop-blur-sm flex flex-col items-end">
                        <span
                            class="text-[10px] text-indigo-400 font-medium uppercase tracking-wider leading-none mb-1">Model
                            Accuracy</span>
                        <span class="text-base font-bold text-indigo-100 leading-none">R² = 0.611</span>
                    </div>
                </div>
            </div>

            <!-- California County Dashboard (Weather App Style) -->
            <CountyDashboard @county-selected="handleCountySelect" />

            <!-- Collapsible Manual Input -->
            <div
                class="mb-12 bg-slate-800 rounded-2xl border border-slate-700 shadow-sm overflow-hidden transition-all duration-300">
                <button @click="showManualInput = !showManualInput"
                    class="w-full flex items-center justify-between p-4 bg-slate-800 hover:bg-slate-700/50 transition-colors text-left">
                    <span class="font-semibold text-slate-200 flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 opacity-50" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                        </svg>
                        進階測試：手動輸入變數 (Manual Input)
                    </span>
                    <svg xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4 text-slate-400 transform transition-transform"
                        :class="showManualInput ? 'rotate-180' : ''" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                </button>

                <div v-show="showManualInput" class="p-6 border-t border-slate-700">
                    <InputForm :modelFeatures="features" :risk="risk" :loading="loading" @predict="handlePredict" />
                </div>
            </div>

            <!-- Project Info Section -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12 animate-fade-in-up">
                <!-- Left Column -->
                <div
                    class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700/50 backdrop-blur-sm hover:border-indigo-500/30 transition-colors">
                    <div class="mb-8">
                        <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" viewBox="0 0 20 20"
                                fill="currentColor">
                                <path fill-rule="evenodd"
                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0 1 1 0 002 0zm-1 4a1 1 0 00-1 1v3a1 1 0 002 0v-3a1 1 0 00-1-1z"
                                    clip-rule="evenodd" />
                            </svg>
                            開發目的
                        </h3>
                        <p class="text-slate-400 leading-relaxed">模仿天氣 App 介面</p>
                        <p class="text-slate-400 leading-relaxed">將複雜的醫療數據轉化為民眾易懂的「風險預報」。</p>
                    </div>
                </div>

                <!-- Right Column -->
                <div
                    class="bg-slate-800/50 rounded-2xl p-6 border border-slate-700/50 backdrop-blur-sm hover:border-indigo-500/30 transition-colors">
                    <div class="mb-8">
                        <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" viewBox="0 0 20 20"
                                fill="currentColor">
                                <path fill-rule="evenodd"
                                    d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"
                                    clip-rule="evenodd" />
                            </svg>
                            核心功能
                        </h3>
                        <ul class="space-y-2 text-slate-400">
                            <li class="flex items-start gap-2">
                                <span class="text-indigo-500 mt-1.5">•</span>
                                查看各郡縣的 30 天再入院率趨勢
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-indigo-500 mt-1.5">•</span>
                                以視覺化方式呈現地區醫療品質
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-indigo-500 mt-1.5">•</span>
                                提供風險等級與建議
                            </li>
                        </ul>
                    </div>

                    <div>
                        <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" viewBox="0 0 20 20"
                                fill="currentColor">
                                <path fill-rule="evenodd"
                                    d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                    clip-rule="evenodd" />
                            </svg>
                            應用價值
                        </h3>
                        <ul class="space-y-2 text-slate-400">
                            <li class="flex items-start gap-2">
                                <span class="text-indigo-500 mt-1.5">•</span>
                                提升民眾對醫療資源分布的認知
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-indigo-500 mt-1.5">•</span>
                                促進醫療透明度與可近性
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-indigo-500 mt-1.5">•</span>
                                為政策制定者提供溝通工具
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Footer Info -->
            <div class="mt-auto pt-12 text-center text-xs text-slate-500">
                © 2025 EquiCare System. Based on CA Open Data.
            </div>

        </div>
    </div>
</template>

<style>
/* Clean Base */
body {
    background-color: #0f172a;
    /* slate-900 */
}
</style>
