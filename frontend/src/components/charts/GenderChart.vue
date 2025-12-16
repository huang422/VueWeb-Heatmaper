<template>
  <div class="gender-chart">
    <div class="chart-header">
      <h3 class="chart-title">性別分布</h3>
      <div v-if="loading" class="chart-loading">載入中...</div>
    </div>

    <div v-if="error" class="chart-error">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="!hasData" class="chart-empty">
      <p>暫無數據</p>
    </div>

    <div v-else class="chart-content">
      <v-chart
        class="chart-container"
        :option="chartOption"
        autoresize
      />
      <div class="percentage-display">
        <div
          v-for="(item, index) in percentages"
          :key="item.name"
          class="percentage-item"
        >
          <span class="percentage-color" :style="{ backgroundColor: index === 0 ? '#3b82f6' : '#ec4899' }"></span>
          <span class="percentage-label">{{ item.name }}:</span>
          <span class="percentage-value">{{ item.percentage }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})

// Check if there's valid data
const hasData = computed(() => {
  return props.data && props.data.length > 0 &&
         props.data.some(item => item.value > 0)
})

// Calculate total for percentages
const total = computed(() => {
  return props.data.reduce((sum, item) => sum + item.value, 0)
})

// Calculate percentages
const percentages = computed(() => {
  if (total.value === 0) return []
  return props.data.map(item => ({
    name: item.name,
    percentage: ((item.value / total.value) * 100).toFixed(2)
  }))
})

// ECharts option for pie chart
const chartOption = computed(() => {
  if (!hasData.value) return {}

  return {
    tooltip: {
      trigger: 'item',
      position: function(point) {
        // Position tooltip below cursor
        return [point[0], point[1] + 20]
      },
      formatter: (params) => {
        return `${params.name}: ${params.value.toFixed(2)} (${params.percent.toFixed(2)}%)`
      }
    },
    legend: {
      show: false
    },
    series: [
      {
        name: '性別分布',
        type: 'pie',
        radius: ['45%', '75%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 15,
            fontWeight: 'bold',
            formatter: '{d}%'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        labelLine: {
          show: false
        },
        data: props.data.map((item, index) => ({
          value: item.value,
          name: item.name,
          itemStyle: {
            color: index === 0 ? '#3b82f6' : '#ec4899' // Blue for male, pink for female
          }
        }))
      }
    ]
  }
})
</script>

<style scoped>
.gender-chart {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.chart-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.chart-loading {
  font-size: 0.875rem;
  color: #6b7280;
}

.chart-error {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ef4444;
  font-size: 0.875rem;
}

.chart-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  font-size: 0.875rem;
}

.chart-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chart-container {
  flex: 1;
  min-height: 200px;
  width: 100%;
}

.percentage-display {
  display: flex;
  justify-content: center;
  gap: 24px;
  padding: 8px 0;
}

.percentage-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.875rem;
}

.percentage-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.percentage-label {
  color: #6b7280;
  font-weight: 500;
}

.percentage-value {
  color: #1f2937;
  font-weight: 700;
}

/* Responsive design */
@media (max-width: 768px) {
  .gender-chart {
    padding: 12px;
  }

  .chart-title {
    font-size: 0.9375rem;
  }

  .chart-container {
    min-height: 200px;
  }
}

@media (max-width: 480px) {
  .chart-container {
    min-height: 180px;
  }
}
</style>
