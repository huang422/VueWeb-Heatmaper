import { ref, watch } from 'vue'
import { getDemographics } from '../services/dataService'

/**
 * Composable for managing demographic data
 *
 * Fetches and manages gender and age distribution statistics
 * for the selected time period, metric, and day type.
 */
export function useDemographics(month, hour, metric, dayType) {
  const loading = ref(false)
  const error = ref(null)
  const demographicData = ref(null)

  // Gender distribution data formatted for charts
  const genderData = ref([])

  // Age distribution data formatted for charts
  const ageData = ref([])

  /**
   * Fetch demographic data from API
   */
  async function fetchDemographics() {
    if (!month.value || hour.value === null || !metric.value || !dayType.value) {
      return
    }

    loading.value = true
    error.value = null

    try {
      const data = await getDemographics(
        month.value,
        hour.value,
        metric.value,
        dayType.value
      )

      demographicData.value = data

      // Format gender data for pie chart
      genderData.value = [
        { name: '男性', value: data.demographics.gender.male },
        { name: '女性', value: data.demographics.gender.female }
      ]

      // Format age data for bar chart
      ageData.value = [
        { name: '19歲以下', value: data.demographics.age.under_19 },
        { name: '20-24歲', value: data.demographics.age.age_20_24 },
        { name: '25-29歲', value: data.demographics.age.age_25_29 },
        { name: '30-34歲', value: data.demographics.age.age_30_34 },
        { name: '35-39歲', value: data.demographics.age.age_35_39 },
        { name: '40-44歲', value: data.demographics.age.age_40_44 },
        { name: '45-49歲', value: data.demographics.age.age_45_49 },
        { name: '50-54歲', value: data.demographics.age.age_50_54 },
        { name: '55-59歲', value: data.demographics.age.age_55_59 },
        { name: '60歲以上', value: data.demographics.age.age_60_plus }
      ]

      loading.value = false
    } catch (err) {
      console.error('Failed to fetch demographic data:', err)
      error.value = err.message || '無法載入人口統計資料'
      loading.value = false

      // Set empty data on error
      genderData.value = []
      ageData.value = []
    }
  }

  // Auto-fetch when dependencies change (per FR-014)
  watch([month, hour, metric, dayType], () => {
    fetchDemographics()
  }, { immediate: true })

  return {
    loading,
    error,
    demographicData,
    genderData,
    ageData,
    fetchDemographics
  }
}
