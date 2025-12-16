<template>
  <div class="timeline-slider">
    <div class="slider-header">
      <label class="slider-label">時間軸</label>
      <span class="slider-value">{{ currentHourDisplay }}</span>
    </div>

    <div class="slider-container">
      <input
        type="range"
        :value="modelValue"
        @input="handleInput"
        @change="handleChange"
        min="0"
        max="23"
        step="1"
        class="slider"
        :class="{ active: isDragging }"
        @mousedown="isDragging = true"
        @mouseup="isDragging = false"
        @touchstart="isDragging = true"
        @touchend="isDragging = false"
        aria-label="選擇小時"
      />

      <div class="slider-marks">
        <span
          v-for="mark in hourMarks"
          :key="mark"
          class="slider-mark"
          :style="{ left: `${(mark / 23) * 100}%` }"
        >
          {{ mark }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 23
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'input'])

const isDragging = ref(false)

// Hour marks to display (0, 6, 12, 18, 23)
const hourMarks = [0, 6, 12, 18, 23]

const currentHourDisplay = computed(() => {
  const hour = props.modelValue
  return `${hour.toString().padStart(2, '0')}:00`
})

function handleInput(event) {
  const value = parseInt(event.target.value)
  emit('update:modelValue', value)
  emit('input', value)
}

function handleChange(event) {
  const value = parseInt(event.target.value)
  emit('change', value)
}
</script>

<style scoped>
.timeline-slider {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slider-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.slider-value {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f2937;
  font-variant-numeric: tabular-nums;
  min-width: 3.5rem;
  text-align: right;
}

.slider-container {
  position: relative;
  padding: 1rem 0 2rem;
}

.slider {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(
    to right,
    #dbeafe 0%,
    #3b82f6 50%,
    #dbeafe 100%
  );
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.slider::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #3b82f6;
  border: 3px solid #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  cursor: grab;
  transition: all 0.2s ease;
}

.slider::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #3b82f6;
  border: 3px solid #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  cursor: grab;
  transition: all 0.2s ease;
}

.slider::-webkit-slider-thumb:hover,
.slider.active::-webkit-slider-thumb {
  background: #2563eb;
  transform: scale(1.15);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
  cursor: grabbing;
}

.slider::-moz-range-thumb:hover,
.slider.active::-moz-range-thumb {
  background: #2563eb;
  transform: scale(1.15);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
  cursor: grabbing;
}

.slider-marks {
  position: absolute;
  top: 2.5rem;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  pointer-events: none;
}

.slider-mark {
  position: absolute;
  font-size: 0.75rem;
  color: #6b7280;
  transform: translateX(-50%);
  font-variant-numeric: tabular-nums;
}

/* Responsive design */
@media (max-width: 768px) {
  .timeline-slider {
    padding: 0.875rem;
    gap: 0.625rem;
  }

  .slider-label {
    font-size: 0.8125rem;
  }

  .slider-value {
    font-size: 1rem;
    min-width: 3rem;
  }

  .slider-container {
    padding: 0.875rem 0 1.75rem;
  }

  .slider {
    height: 6px;
  }

  .slider::-webkit-slider-thumb {
    width: 20px;
    height: 20px;
  }

  .slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
  }

  .slider-mark {
    font-size: 0.6875rem;
  }
}

@media (max-width: 480px) {
  .slider-marks {
    display: none;
  }
}
</style>
