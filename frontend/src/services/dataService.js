/**
 * Data Service
 * API calls with caching for heatmap and demographic data
 */

import apiClient from './api'

// Simple in-memory cache
const cache = {
  metadata: null,
  heatmapData: new Map(),
  demographicData: new Map()
}

/**
 * Get metadata (months, hours, metrics)
 * Cached as it rarely changes
 */
export async function getMetadata() {
  if (cache.metadata) {
    return cache.metadata
  }

  try {
    const data = await apiClient.get('/metadata')
    cache.metadata = data
    return data
  } catch (error) {
    console.error('Failed to fetch metadata:', error)
    throw error
  }
}

/**
 * Get heatmap data for specific time period
 * @param {number} month - Month in YYYYMM format
 * @param {number} hour - Hour (0-23)
 * @param {string} metric - Metric name
 * @param {string} dayType - Day type (平日 or 假日)
 * @returns {Promise<Object>} Heatmap data with lat/lng/weight points
 */
export async function getHeatmapData(month, hour, metric = 'avg_total_users', dayType = '平日') {
  const cacheKey = `${month}-${hour}-${metric}-${dayType}`

  // Return cached data if available
  if (cache.heatmapData.has(cacheKey)) {
    return cache.heatmapData.get(cacheKey)
  }

  try {
    const data = await apiClient.get('/heatmap', {
      params: { month, hour, metric, day_type: dayType }
    })

    // Cache the result
    cache.heatmapData.set(cacheKey, data)

    // Limit cache size to prevent memory issues
    if (cache.heatmapData.size > 100) {
      const firstKey = cache.heatmapData.keys().next().value
      cache.heatmapData.delete(firstKey)
    }

    return data
  } catch (error) {
    console.error('Failed to fetch heatmap data:', error)
    throw error
  }
}

/**
 * Get demographic statistics for specific time period
 * @param {number} month - Month in YYYYMM format
 * @param {number} hour - Hour (0-23)
 * @param {string} metric - Metric name for weighting
 * @param {string} dayType - Day type (平日 or 假日)
 * @returns {Promise<Object>} Demographic statistics
 */
export async function getDemographics(month, hour, metric = 'avg_total_users', dayType = '平日') {
  const cacheKey = `${month}-${hour}-${metric}-${dayType}`

  // Return cached data if available
  if (cache.demographicData.has(cacheKey)) {
    return cache.demographicData.get(cacheKey)
  }

  try {
    const data = await apiClient.get('/demographics', {
      params: { month, hour, metric, day_type: dayType }
    })

    // Cache the result
    cache.demographicData.set(cacheKey, data)

    // Limit cache size
    if (cache.demographicData.size > 100) {
      const firstKey = cache.demographicData.keys().next().value
      cache.demographicData.delete(firstKey)
    }

    return data
  } catch (error) {
    console.error('Failed to fetch demographics:', error)
    throw error
  }
}

/**
 * Clear all caches (useful for testing or forcing refresh)
 */
export function clearCache() {
  cache.metadata = null
  cache.heatmapData.clear()
  cache.demographicData.clear()
}

/**
 * Prefetch data for better performance
 * @param {number} month - Month to prefetch
 * @param {string} metric - Metric to prefetch
 */
export async function prefetchHeatmapData(month, metric = 'avg_total_users') {
  const promises = []

  // Prefetch all 24 hours for the given month/metric
  for (let hour = 0; hour < 24; hour++) {
    promises.push(getHeatmapData(month, hour, metric))
  }

  try {
    await Promise.all(promises)
    console.log(`Prefetched heatmap data for month ${month}, metric ${metric}`)
  } catch (error) {
    console.error('Prefetch failed:', error)
  }
}
