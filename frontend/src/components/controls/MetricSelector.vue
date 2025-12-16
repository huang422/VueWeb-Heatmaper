<template>
  <div class="metric-selector">
    <label class="selector-label">停留時長指標</label>
    <div class="selector-buttons">
      <button
        v-for="metric in availableMetrics"
        :key="metric.value"
        :class="['metric-button', { active: modelValue === metric.value }]"
        @click="selectMetric(metric.value)"
        :aria-label="`選擇${metric.label}`"
      >
        <span class="metric-icon">{{ metric.icon }}</span>
        <span class="metric-label">{{ metric.label }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  },
  availableMetrics: {
    type: Array,
    default: () => [
      { value: 'avg_total_users', label: '全部停留人數', icon: '👥' },
      { value: 'avg_users_under_10min', label: '停留10分鐘以下', icon: '⚡' },
      { value: 'avg_users_10_30min', label: '停留10-30分鐘', icon: '⏱️' },
      { value: 'avg_users_above_30min', label: '停留30分鐘以上', icon: '🕐' }
    ]
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

function selectMetric(metric) {
  if (metric !== props.modelValue) {
    emit('update:modelValue', metric)
    emit('change', metric)
  }
}
</script>

<style scoped>
.metric-selector {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.selector-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
}

.selector-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.metric-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background-color: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.metric-button:hover {
  border-color: #10b981;
  background-color: #f0fdf4;
  transform: translateX(2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metric-button.active {
  background-color: #10b981;
  border-color: #059669;
  color: white;
  box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);
}

.metric-button:active {
  transform: translateX(0);
}

.metric-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
  width: 1.5rem;
  text-align: center;
}

.metric-label {
  font-size: 0.875rem;
  font-weight: 500;
  flex: 1;
  line-height: 1.3;
}

.metric-button.active .metric-label {
  color: white;
  font-weight: 600;
}

/* Responsive design */
@media (max-width: 768px) {
  .metric-button {
    padding: 0.75rem 0.875rem;
    gap: 0.625rem;
  }

  .metric-icon {
    font-size: 1.125rem;
    width: 1.375rem;
  }

  .metric-label {
    font-size: 0.8125rem;
  }
}

@media (max-width: 480px) {
  .selector-buttons {
    gap: 0.375rem;
  }

  .metric-button {
    padding: 0.625rem 0.75rem;
  }

  .metric-label {
    font-size: 0.75rem;
  }
}
</style>
