<template>
  <div class="daytype-selector">
    <label class="selector-label">平日/假日</label>
    <div class="selector-buttons">
      <button
        :class="['daytype-button', { active: modelValue === '平日' }]"
        @click="selectDayType('平日')"
        aria-label="選擇平日"
      >
        <span class="daytype-icon">📅</span>
        <span class="daytype-label">平日</span>
      </button>
      <button
        :class="['daytype-button', { active: modelValue === '假日' }]"
        @click="selectDayType('假日')"
        aria-label="選擇假日"
      >
        <span class="daytype-icon">🎉</span>
        <span class="daytype-label">假日</span>
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

function selectDayType(dayType) {
  if (dayType !== props.modelValue) {
    emit('update:modelValue', dayType)
    emit('change', dayType)
  }
}
</script>

<style scoped>
.daytype-selector {
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
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.daytype-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  background-color: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.daytype-button:hover {
  border-color: #6366f1;
  background-color: #eef2ff;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.daytype-button.active {
  background-color: #6366f1;
  border-color: #4f46e5;
  color: white;
  box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3);
}

.daytype-button:active {
  transform: translateY(0);
}

.daytype-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.daytype-label {
  font-size: 0.875rem;
  font-weight: 600;
}

.daytype-button.active .daytype-label {
  color: white;
}

/* Responsive design */
@media (max-width: 768px) {
  .daytype-button {
    padding: 0.75rem 0.875rem;
    gap: 0.375rem;
  }

  .daytype-icon {
    font-size: 1.125rem;
  }

  .daytype-label {
    font-size: 0.8125rem;
  }
}

@media (max-width: 480px) {
  .daytype-button {
    padding: 0.625rem 0.75rem;
  }

  .daytype-label {
    font-size: 0.75rem;
  }
}
</style>
