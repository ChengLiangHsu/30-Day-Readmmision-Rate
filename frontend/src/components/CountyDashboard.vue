<script setup>
import { ref, onMounted, computed } from 'vue';

const props = defineProps(['loading']);
const emit = defineEmits(['predict', 'county-selected']);

// Mock Data for California Counties "Weather"
const counties = [
    {
        id: 'SF', name: '舊金山郡 (San Francisco)',
        data: {
            readmits_prop: 0.00420,
            icd_version: 1,
            pcpi_log: 11.95, // Wealthier 
            total_admits_log: 9.8,
            last_year_rate: 11.2,
            PCPI: 155000,
            Population: 870000,
            '30-day Readmission Rate (Consolidated)': 11.2
        },
        temp: 11.2
    },
    {
        id: 'FR', name: '弗雷斯諾郡 (Fresno)',
        data: {
            readmits_prop: 0.00550,
            icd_version: 1,
            pcpi_log: 10.20, // Lower income
            total_admits_log: 9.5,
            last_year_rate: 17.2,
            PCPI: 27000,
            Population: 100000,
            '30-day Readmission Rate (Consolidated)': 17.2
        },
        temp: 17.2
    },
    {
        id: 'IN', name: '因約郡 (Inyo County)',
        data: {
            readmits_prop: 0.00500,
            icd_version: 1,
            pcpi_log: 10.90,
            total_admits_log: 7.5,
            last_year_rate: 14.5,
            PCPI: 54000,
            Population: 18000, // Small population < 150k
            '30-day Readmission Rate (Consolidated)': 14.5
        },
        temp: 14.5
    },
    {
        id: 'LA', name: '洛杉磯郡 (Los Angeles)',
        data: {
            readmits_prop: 0.00512,
            icd_version: 1,
            pcpi_log: 10.85,
            total_admits_log: 11.2,
            last_year_rate: 16.5,
            // Raw for clustering heuristic
            PCPI: 51200, 
            Population: 9800000,
            '30-day Readmission Rate (Consolidated)': 16.5 
        },
        temp: 16.5 // Display "temp" (rate) for list
    },
    {
        id: 'SD', name: '聖地牙哥郡 (San Diego)',
        data: {
            readmits_prop: 0.00480,
            icd_version: 1,
            pcpi_log: 11.20,
            total_admits_log: 10.5,
            last_year_rate: 13.8,
            PCPI: 72000,
            Population: 3300000,
            '30-day Readmission Rate (Consolidated)': 13.8
        },
        temp: 13.8
    },
    {
        id: 'OC', name: '橘郡 (Orange County)',
        data: {
            readmits_prop: 0.00450,
            icd_version: 1,
            pcpi_log: 11.60,
            total_admits_log: 10.8,
            last_year_rate: 12.5,
            PCPI: 110000,
            Population: 3100000,
            '30-day Readmission Rate (Consolidated)': 12.5
        },
        temp: 12.5
    }
];

const selectedCounty = ref(counties[0]);
const riskScore = ref(null);
const clusterName = ref('');
const clusterStrategy = ref('');
const isLoading = ref(false);

const selectCounty = async (county) => {
    selectedCounty.value = county;
    emit('county-selected', county);
    isLoading.value = true;
    riskScore.value = null;
    clusterName.value = '';
    clusterStrategy.value = '';

    // Simulate network delay for "Weather Data Fetch"
    await new Promise(r => setTimeout(r, 600));

    // Call Backend
    // Call Backend for Prediction
    try {
        const payload = {
            '30-day Readmits (Proportion)': county.data.readmits_prop,
            'ICD Version(Ordinal)': county.data.icd_version,
            'PCPI_log': county.data.pcpi_log,
            'Total Admits people(log)': county.data.total_admits_log,
            'last_year_rate': county.data.last_year_rate,
            // Add extra for clustering
            'Population': county.data.Population,
            'Total Admits (Consolidated)': county.data.total_admits_log ? 0 : 0, // Mock or need raw? 
            'Total Admits people(log)': county.data.total_admits_log
        };

        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const resData = await response.json();

        if (resData.risk_score !== undefined) {
            riskScore.value = resData.risk_score.toFixed(2);
        }
        
        // Fetch Cluster Info
        const clusterRes = await fetch('/cluster', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const clusterData = await clusterRes.json();
        if (clusterData.cluster_name) {
            clusterName.value = clusterData.cluster_name;
            clusterStrategy.value = clusterData.cluster_strategy || "尚無具體建議。";
        }

    } catch (e) {
        console.error(e);
        riskScore.value = "Error";
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    selectCounty(counties[0]);
});


const clusterColorClass = computed(() => {
    if (!clusterName.value) return 'text-slate-400 border-slate-600';
    if (clusterName.value.includes('醫療中心')) return 'text-blue-400 border-blue-500 bg-blue-900/20';
    if (clusterName.value.includes('醫療弱勢區')) return 'text-orange-400 border-orange-500 bg-orange-900/20';
    if (clusterName.value.includes('小型流量區') || clusterName.value.includes('Low Volume')) return 'text-green-400 border-green-500 bg-green-900/20';
    return 'text-slate-400 border-slate-600';
});

</script>

<template>
    <div class="flex flex-col md:flex-row gap-6 h-full min-h-[500px] mb-8">

        <!-- SIDEBAR: County List -->
        <div
            class="w-full md:w-1/3 bg-slate-800 rounded-3xl overflow-hidden border border-slate-700 shadow-xl flex flex-col">
            <div class="p-5 border-b border-slate-700 bg-slate-800">
                <h3 class="font-bold text-lg text-white">加州各郡監測</h3>
                <p class="text-xs text-slate-500">California Counties Data</p>
            </div>
            <div class="flex-1 overflow-y-auto p-3 space-y-2">
                <button v-for="c in counties" :key="c.id" @click="selectCounty(c)"
                    class="w-full text-left p-3 rounded-xl transition-all duration-200 flex justify-between items-center group border"
                    :class="selectedCounty.id === c.id ? 'bg-indigo-600 text-white border-indigo-500 shadow-md' : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border-transparent hover:border-slate-600'">
                    <div>
                        <div class="font-bold">{{ c.name.split(' ')[0] }}</div>
                        <div class="text-[10px]"
                            :class="selectedCounty.id === c.id ? 'text-indigo-100' : 'text-slate-500'">{{
                                c.name.split('(')[1].replace(')', '') }}</div>
                    </div>
                    <div class="text-xl font-medium"
                        :class="selectedCounty.id === c.id ? 'text-white' : 'text-slate-500 group-hover:text-indigo-400'">
                        {{ c.temp }}%
                    </div>
                </button>
            </div>
        </div>

        <!-- MAIN: Weather Report -->
        <div
            class="w-full md:w-2/3 bg-slate-800 rounded-3xl p-8 border border-slate-700 shadow-xl relative overflow-hidden flex flex-col justify-between">

            <!-- Background Decor (Subtle) -->
            <div
                class="absolute top-0 right-0 w-64 h-64 bg-indigo-900/30 rounded-full blur-3xl -z-0 opacity-50 translate-x-1/3 -translate-y-1/3">
            </div>

            <!-- Header -->
            <div class="relative z-10 text-center mt-2">
                <h2 class="text-3xl font-bold text-white mb-1">
                    {{ selectedCounty.name.split(' (')[0] }}
                    <span v-if="clusterName" 
                          class="text-lg font-normal ml-2 border-l pl-2 px-2 py-0.5 rounded-md"
                          :class="clusterColorClass">
                        {{ clusterName }}
                    </span>
                </h2>
                <span
                    class="inline-block px-3 py-1 bg-indigo-900/50 text-indigo-300 rounded-full text-xs font-bold tracking-wider uppercase border border-indigo-500/30">
                    30 天再入院預測
                </span>
            </div>

            <!-- BIG NUMBER -->
            <div class="relative z-10 text-center my-6">
                <div v-if="isLoading" class="animate-pulse text-6xl text-slate-600">...</div>
                <div v-else class="flex flex-col items-center">
                    <div class="text-8xl font-light text-white tracking-tighter">
                        {{ riskScore }}<span class="text-4xl text-slate-500 font-normal">%</span>
                    </div>
                    <div class="mt-2 text-sm font-medium"
                        :class="riskScore > 15 ? 'text-orange-400' : 'text-emerald-400'">
                        {{ riskScore > 15 ? '⚠ 高於平均風險 (High Risk)' : '✓ 風險控制良好 (Low Risk)' }}
                    </div>
                </div>
            </div>
                
            <!-- Strategy Recommendation -->
            <div v-if="clusterStrategy" class="mt-4 px-4 py-3 bg-indigo-900/40 rounded-xl text-xs text-indigo-200 font-medium text-center border border-indigo-700/50 max-w-sm mx-auto">
                💡 改善建議：{{ clusterStrategy }}
            </div>

            <!-- Grid Stats -->
            <div class="relative z-10 grid grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
                <div
                    class="bg-slate-700/50 p-4 rounded-2xl border border-slate-600 hover:border-indigo-500/50 transition-colors">
                    <div class="text-xs text-slate-400 uppercase mb-1 font-semibold">去年比率 (Last Year)</div>
                    <div class="text-xl font-bold text-slate-200">{{ selectedCounty.data.last_year_rate }}%</div>
                </div>
                <div
                    class="bg-slate-700/50 p-4 rounded-2xl border border-slate-600 hover:border-indigo-500/50 transition-colors">
                    <div class="text-xs text-slate-400 uppercase mb-1 font-semibold">人均收入 (PCPI Log)</div>
                    <div class="text-xl font-bold text-slate-200">{{ selectedCounty.data.pcpi_log }}</div>
                </div>
                <div
                    class="bg-slate-700/50 p-4 rounded-2xl border border-slate-600 hover:border-indigo-500/50 transition-colors">
                    <div class="text-xs text-slate-400 uppercase mb-1 font-semibold">當前比率 (Current Prop)</div>
                    <div class="text-xl font-bold text-slate-200">{{ selectedCounty.data.readmits_prop }}</div>
                </div>
                <div
                    class="bg-slate-700/50 p-4 rounded-2xl border border-slate-600 hover:border-indigo-500/50 transition-colors">
                    <div class="text-xs text-slate-400 uppercase mb-1 font-semibold">總住院 (Admits Log)</div>
                    <div class="text-xl font-bold text-slate-200">{{ selectedCounty.data.total_admits_log }}</div>
                </div>
                <div
                    class="bg-slate-700/50 p-4 rounded-2xl border border-slate-600 hover:border-indigo-500/50 transition-colors">
                    <div class="text-xs text-slate-400 uppercase mb-1 font-semibold">編碼版本 (ICD)</div>
                    <div class="text-xl font-bold text-slate-200">
                        {{ selectedCounty.data.icd_version === 0 ? 'ICD-9' : 'ICD-10' }}
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>
