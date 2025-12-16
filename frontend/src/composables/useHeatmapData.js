/**
 * useHeatmapData Composable
 * Manages heatmap data fetching and state
 */

import { ref, computed, watch } from 'vue'
import { getHeatmapData, getMetadata } from '../services/dataService'

export function useHeatmapData() {
  // State
  const heatmapData = ref(null)
  const metadata = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Filters
  const selectedMonth = ref(202412)
  const selectedHour = ref(0)
  const selectedMetric = ref('avg_total_users')
  const selectedDayType = ref('平日')

  // Computed
  const dataPoints = computed(() => {
    return heatmapData.value?.data || []
  })

  const statistics = computed(() => {
    if (!heatmapData.value) return null

    return {
      count: heatmapData.value.count,
      minWeight: heatmapData.value.min_weight,
      maxWeight: heatmapData.value.max_weight
    }
  })

  const availableMonths = computed(() => {
    return metadata.value?.months || []
  })

  const availableHours = computed(() => {
    return metadata.value?.hours || []
  })

  const availableMetrics = computed(() => {
    return metadata.value?.metrics || []
  })

  const availableDayTypes = computed(() => {
    return metadata.value?.day_types || ['平日', '假日']
  })

  // Methods
  async function fetchMetadata() {
    try {
      loading.value = true
      error.value = null
      metadata.value = await getMetadata()
    } catch (err) {
      error.value = 'Failed to load metadata: ' + err.message
      console.error('Metadata fetch error:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchHeatmapData() {
    try {
      loading.value = true
      error.value = null

      const data = await getHeatmapData(
        selectedMonth.value,
        selectedHour.value,
        selectedMetric.value,
        selectedDayType.value
      )

      heatmapData.value = data
    } catch (err) {
      error.value = 'Failed to load heatmap data: ' + err.message
      console.error('Heatmap data fetch error:', err)
    } finally {
      loading.value = false
    }
  }

  function setMonth(month) {
    selectedMonth.value = month
  }

  function setHour(hour) {
    selectedHour.value = hour
  }

  function setMetric(metric) {
    selectedMetric.value = metric
  }

  function setDayType(dayType) {
    selectedDayType.value = dayType
  }

  // Watch for changes and auto-fetch
  watch([selectedMonth, selectedHour, selectedMetric, selectedDayType], () => {
    fetchHeatmapData()
  })

  // Initialize
  async function initialize() {
    await fetchMetadata()
    await fetchHeatmapData()
  }

  return {
    // State
    heatmapData,
    metadata,
    loading,
    error,

    // Filters
    selectedMonth,
    selectedHour,
    selectedMetric,
    selectedDayType,

    // Computed
    dataPoints,
    statistics,
    availableMonths,
    availableHours,
    availableMetrics,
    availableDayTypes,

    // Methods
    fetchMetadata,
    fetchHeatmapData,
    setMonth,
    setHour,
    setMetric,
    setDayType,
    initialize
  }
}
