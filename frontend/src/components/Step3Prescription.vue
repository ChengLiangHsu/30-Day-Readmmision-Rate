<script setup>
import { computed } from 'vue';

const props = defineProps({
    cluster: Object,
    scenario: Object
});

const isStructural = computed(() => props.scenario?.type === 'structural');

const prescriptions = computed(() => {
    if (!isStructural.value) {
        return [
            { id: 99, title: "啟動稽核程序 (Audit Protocol)", source: "CMS Regs", desc: "啟動質量改進計劃與管理審查。" }
        ];
    }

    // Logic based on Cluster
    // Cluster 2 = Resource Deprived (Rural context)
    // Cluster 3 = Urban Challenge
    if (props.cluster?.name.includes("匱乏") || props.cluster?.name.includes("Resource Deprived")) {
        return [
            { id: 1, title: "交通協助 (Transportation Assistance)", source: "Source 28", desc: "擴大偏鄉地區的接駁服務。" },
            { id: 2, title: "流動食物銀行 (Mobile Food Banks)", source: "Source 28", desc: "部署移動營養車至資源匱乏區。" }
        ];
    } else if (props.cluster?.name.includes("都市") || props.cluster?.name.includes("Urban")) {
        return [
            { id: 3, title: "住房援助 (Housing Assistance)", source: "Source 27", desc: "連結患者至臨時庇護所。" },
            { id: 4, title: "街友服務 (Homeless Services)", source: "Source 33", desc: "整合當地街頭醫療團隊資源。" }
        ];
    } else {
        // Default / Wealthy
        return [
            { id: 5, title: "標準照護協調 (Standard Care)", source: "General", desc: "確保出院衛教資訊清晰。" }
        ];
    }
});

</script>

<template>
    <div class="step-container mt-8 pt-8 border-t border-slate-100">
        <div class="step-header mb-6">
            <div class="step-badge">第三步</div>
            <h3 class="text-xl font-bold text-slate-900">整合「Tool 11」給出精準處方</h3>
        </div>

        <div class="bg-indigo-50/50 rounded-xl p-6 border border-indigo-100 shadow-inner">
            <h4 class="text-sm font-bold uppercase tracking-widest text-indigo-600 mb-4 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
                Rx: 建議介入資源 (Recommended Interventions)
            </h4>

            <div class="space-y-3">
                <div v-for="rx in prescriptions" :key="rx.id"
                    class="bg-white hover:bg-white/80 transition-colors p-4 rounded-lg flex items-start gap-3 border border-indigo-100 shadow-sm relative overflow-hidden group">
                    <!-- Hover highlight -->
                    <div
                        class="absolute left-0 top-0 bottom-0 w-1 bg-indigo-500 opacity-0 group-hover:opacity-100 transition-opacity">
                    </div>

                    <div class="mt-1 bg-indigo-50 p-1.5 rounded text-indigo-600">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                        </svg>
                    </div>
                    <div>
                        <div class="font-bold text-slate-800 text-base">
                            {{ rx.title }}
                            <span
                                class="ml-2 text-[10px] bg-indigo-100 px-1.5 py-0.5 rounded text-indigo-700 uppercase font-semibold">{{
                                rx.source }}</span>
                        </div>
                        <div class="text-sm text-slate-500 mt-1 leading-snug">
                            {{ rx.desc }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
.step-badge {
    @apply text-xs font-bold uppercase tracking-wider text-blue-300 mb-1;
}
</style>
