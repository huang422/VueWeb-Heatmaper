<template>
  <div class="heatmap-container">
    <div ref="mapContainer" class="map-view"></div>
    <MapTooltip
      v-if="tooltipVisible"
      :position="tooltipPosition"
      :data="tooltipData"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import Map from 'ol/Map'
import View from 'ol/View'
import { Tile as TileLayer, Heatmap as HeatmapLayer, Vector as VectorLayer } from 'ol/layer'
import { OSM, Vector as VectorSource } from 'ol/source'
import Feature from 'ol/Feature'
import Point from 'ol/geom/Point'
import { fromLonLat } from 'ol/proj'
import { Circle as CircleStyle, Fill, Stroke, Style } from 'ol/style'
import MapTooltip from './MapTooltip.vue'

// Register proj4 for TWD97 support
import '../../services/proj4Config'

const props = defineProps({
  dataPoints: {
    type: Array,
    default: () => []
  },
  blur: {
    type: Number,
    default: 15
  },
  radius: {
    type: Number,
    default: 8
  },
  minWeight: {
    type: Number,
    default: 0
  },
  maxWeight: {
    type: Number,
    default: 100
  }
})

const emit = defineEmits(['mapReady'])

// Refs
const mapContainer = ref(null)
const map = ref(null)
const heatmapLayer = ref(null)
const vectorSource = ref(null)
const isInitialLoad = ref(true) // Flag for initial data load

// Tooltip state
const tooltipVisible = ref(false)
const tooltipPosition = ref({ x: 0, y: 0 })
const tooltipData = ref(null)

// Initialize map
function initMap() {
  // Create vector source for heatmap and points
  vectorSource.value = new VectorSource()

  // Create heatmap layer
  heatmapLayer.value = new HeatmapLayer({
    source: vectorSource.value,
    blur: props.blur,
    radius: props.radius,
    weight: function (feature) {
      return feature.get('weight')
    },
    gradient: [
      '#00f', // blue - low values
      '#0ff', // cyan
      '#0f0', // green
      '#ff0', // yellow
      '#f00'  // red - high values
    ]
  })

  // Create a layer for the actual points
  const pointsLayer = new VectorLayer({
    source: vectorSource.value,
    style: new Style({
      image: new CircleStyle({
        radius: 4,
        fill: new Fill({ color: 'rgba(255, 255, 255, 0.6)' }),
        stroke: new Stroke({ color: '#d10000', width: 2 })
      })
    })
  })

  // Create map
  map.value = new Map({
    target: mapContainer.value,
    layers: [
      new TileLayer({
        source: new OSM()
      }),
      heatmapLayer.value,
      pointsLayer // Add points layer on top
    ],
    view: new View({
      center: fromLonLat([121.5, 23.9]), // Center of Taiwan
      zoom: 7,
      minZoom: 6,
      maxZoom: 18
    })
  })

  // Setup hover interaction
  map.value.on('pointermove', handlePointerMove)
  map.value.on('pointerout', handlePointerOut)

  emit('mapReady', map.value)
}

// Update heatmap data
function updateHeatmap() {
  if (!vectorSource.value) return

  // Clear existing features
  vectorSource.value.clear()

  if (!props.dataPoints || props.dataPoints.length === 0) {
    return
  }

  // Calculate min/max for normalization if not provided
  const weights = props.dataPoints.map(p => p.weight)
  const minW = props.minWeight || Math.min(...weights)
  const maxW = props.maxWeight || Math.max(...weights)
  const weightRange = maxW - minW || 1

  // Create features from data points with normalized weights
  const features = props.dataPoints.map(point => {
    // Normalize weight to 0-1 range for proper color gradient
    const normalizedWeight = (point.weight - minW) / weightRange

    const feature = new Feature({
      geometry: new Point(fromLonLat([point.lng, point.lat])),
      weight: normalizedWeight,
      rawWeight: point.weight,
      gx: point.gx,
      gy: point.gy,
      lat: point.lat,
      lng: point.lng
    })
    return feature
  })

  // Add features to source
  vectorSource.value.addFeatures(features)

  // Auto-fit the view on the initial data load
  if (features.length > 0 && isInitialLoad.value) {
    const extent = vectorSource.value.getExtent()
    map.value.getView().fit(extent, {
      padding: [80, 80, 80, 80], // Add some padding
      maxZoom: 16, // Zoom in a bit closer
      duration: 1000 // Animate the zoom
    })
    isInitialLoad.value = false // Ensure this only runs once
  }
}

// Handle mouse move over map
function handlePointerMove(event) {
  const pixel = map.value.getEventPixel(event.originalEvent)
  const feature = map.value.forEachFeatureAtPixel(pixel, (feat) => feat)

  if (feature) {
    tooltipData.value = {
      weight: feature.get('rawWeight') || feature.get('weight'),
      gx: feature.get('gx'),
      gy: feature.get('gy'),
      lat: feature.get('lat').toFixed(6),
      lng: feature.get('lng').toFixed(6)
    }
    tooltipPosition.value = {
      x: event.pixel[0],
      y: event.pixel[1]
    }
    tooltipVisible.value = true
  } else {
    tooltipVisible.value = false
  }
}

// Handle mouse leaving map
function handlePointerOut() {
  tooltipVisible.value = false
}

// Lifecycle hooks
onMounted(() => {
  nextTick(() => {
    initMap()
    updateHeatmap()
  })
})

// Watch for data changes
watch(() => props.dataPoints, () => {
  updateHeatmap()
}, { deep: true })

// Watch for blur/radius changes
watch([() => props.blur, () => props.radius], () => {
  if (heatmapLayer.value) {
    heatmapLayer.value.setBlur(props.blur)
    heatmapLayer.value.setRadius(props.radius)
  }
})
</script>

<style scoped>
.heatmap-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.map-view {
  width: 100%;
  height: 100%;
}

/* OpenLayers default styles */
:deep(.ol-zoom) {
  top: 0.5rem;
  left: auto;
  right: 0.5rem;
}

:deep(.ol-attribution) {
  right: 0.5rem;
  bottom: 0.5rem;
  max-width: calc(100% - 1rem);
}
</style>
