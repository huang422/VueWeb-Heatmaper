<template>
  <div class="month-selector">
    <label class="selector-label">月份選擇</label>
    <div class="selector-buttons">
      <button
        v-for="month in availableMonths"
        :key="month.value"
        :class="['month-button', { active: modelValue === month.value }]"
        @click="selectMonth(month.value)"
        :aria-label="`選擇${month.label}`"
      >
        <span class="month-label">{{ month.label }}</span>
        <span class="month-sublabel">{{ month.sublabel }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  },
  availableMonths: {
    type: Array,
    default: () => [
      { value: 202412, label: '2024年12月', sublabel: '12月' },
      { value: 202502, label: '2025年2月', sublabel: '2月' },
      { value: 202505, label: '2025年5月', sublabel: '5月' },
      { value: 202508, label: '2025年8月', sublabel: '8月' }
    ]
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

function selectMonth(month) {
  if (month !== props.modelValue) {
    emit('update:modelValue', month)
    emit('change', month)
  }
}
</script>

<style scoped>
.month-selector {
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
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.month-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 0.5rem;
  background-color: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 4rem;
}

.month-button:hover {
  border-color: #3b82f6;
  background-color: #eff6ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.month-button.active {
  background-color: #3b82f6;
  border-color: #2563eb;
  color: white;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
}

.month-button:active {
  transform: translateY(0);
}

.month-label {
  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1.2;
}

.month-sublabel {
  font-size: 0.75rem;
  opacity: 0.8;
  margin-top: 0.25rem;
}

.month-button.active .month-label,
.month-button.active .month-sublabel {
  color: white;
}

/* Responsive design */
@media (max-width: 768px) {
  .selector-buttons {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.375rem;
  }

  .month-button {
    padding: 0.625rem 0.375rem;
    min-height: 3.5rem;
  }

  .month-label {
    font-size: 0.8125rem;
  }

  .month-sublabel {
    font-size: 0.6875rem;
  }
}

@media (max-width: 480px) {
  .selector-buttons {
    grid-template-columns: 1fr;
  }

  .month-button {
    flex-direction: row;
    justify-content: flex-start;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    min-height: auto;
  }

  .month-sublabel {
    display: none;
  }
}
</style>
