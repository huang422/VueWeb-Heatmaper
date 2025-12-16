<template>
  <div class="age-chart">
    <div class="chart-header">
      <h3 class="chart-title">年齡分布</h3>
      <div v-if="loading" class="chart-loading">載入中...</div>
    </div>

    <div v-if="error" class="chart-error">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="!hasData" class="chart-empty">
      <p>暫無數據</p>
    </div>

    <v-chart
      v-else
      class="chart-container"
      :option="chartOption"
      autoresize
    />
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

// ECharts option for bar chart
const chartOption = computed(() => {
  if (!hasData.value) return {}

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      position: function(point) {
        // Position tooltip below cursor
        return [point[0], point[1] + 20]
      },
      formatter: (params) => {
        const data = params[0]
        return `${data.name}: ${data.value.toFixed(2)}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: props.data.map(item => item.name),
      axisLabel: {
        rotate: 45,
        fontSize: 11,
        color: '#6b7280',
        interval: 0,
        formatter: (value) => {
          // Shorten labels on small screens
          if (window.innerWidth < 480) {
            return value.replace('歲', '').replace('以下', '-').replace('以上', '+')
          }
          return value
        }
      },
      axisLine: {
        lineStyle: {
          color: '#e5e7eb'
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '百分比 (%)',
      nameTextStyle: {
        color: '#6b7280',
        fontSize: 12
      },
      axisLabel: {
        formatter: '{value}%',
        fontSize: 11,
        color: '#6b7280'
      },
      axisLine: {
        show: false
      },
      splitLine: {
        lineStyle: {
          color: '#f3f4f6'
        }
      }
    },
    series: [
      {
        name: '年齡分布',
        type: 'bar',
        data: props.data.map((item) => ({
          value: item.value,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: '#60a5fa' },
                { offset: 1, color: '#3b82f6' }
              ]
            },
            borderRadius: [4, 4, 0, 0]
          }
        })),
        barWidth: '60%',
        label: {
          show: false,
          position: 'top',
          formatter: '{c}%',
          fontSize: 10,
          color: '#374151'
        },
        emphasis: {
          label: {
            show: true
          },
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: '#93c5fd' },
                { offset: 1, color: '#60a5fa' }
              ]
            }
          }
        }
      }
    ]
  }
})
</script>

<style scoped>
.age-chart {
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

.chart-container {
  flex: 1;
  min-height: 280px;
  width: 100%;
}

/* Responsive design */
@media (max-width: 768px) {
  .age-chart {
    padding: 12px;
  }

  .chart-title {
    font-size: 0.9375rem;
  }

  .chart-container {
    min-height: 240px;
  }
}

@media (max-width: 480px) {
  .chart-container {
    min-height: 200px;
  }
}
</style>
