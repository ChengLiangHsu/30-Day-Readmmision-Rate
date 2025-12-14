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
    background-color: #0f172a; /* slate-900 */
}
</style>
