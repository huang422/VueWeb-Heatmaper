<template>
  <div
    class="map-tooltip"
    :style="tooltipStyle"
  >
    <div class="tooltip-header">位置資訊</div>
    <div class="tooltip-content">
      <div class="tooltip-row">
        <span class="label">用戶數:</span>
        <span class="value">{{ data.weight.toFixed(2) }}</span>
      </div>
      <div class="tooltip-row">
        <span class="label">網格座標:</span>
        <span class="value">({{ data.gx }}, {{ data.gy }})</span>
      </div>
      <div class="tooltip-row">
        <span class="label">經緯度:</span>
        <span class="value">({{ data.lat }}, {{ data.lng }})</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  position: {
    type: Object,
    required: true
  },
  data: {
    type: Object,
    required: true
  }
})

const tooltipStyle = computed(() => {
  return {
    left: `${props.position.x + 15}px`,
    top: `${props.position.y + 15}px`
  }
})
</script>

<style scoped>
.map-tooltip {
  position: absolute;
  background: rgba(0, 0, 0, 0.85);
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  pointer-events: none;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  min-width: 200px;
}

.tooltip-header {
  font-weight: 600;
  margin-bottom: 6px;
  padding-bottom: 4px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.tooltip-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tooltip-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.label {
  color: rgba(255, 255, 255, 0.7);
}

.value {
  font-weight: 500;
  color: #4fc3f7;
}
</style>
