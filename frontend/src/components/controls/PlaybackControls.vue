<template>
  <div class="playback-controls">
    <button
      v-if="!isPlaying"
      @click="$emit('play')"
      class="btn btn-primary control-btn"
      :disabled="!canPlay"
      title="開始自動播放"
    >
      <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M8 5v14l11-7z"/>
      </svg>
      <span>播放</span>
    </button>

    <button
      v-else
      @click="$emit('pause')"
      class="btn btn-primary control-btn"
      :disabled="!canPause"
      title="暫停自動播放"
    >
      <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
      </svg>
      <span>暫停</span>
    </button>

    <button
      @click="$emit('reset')"
      class="btn btn-secondary control-btn"
      title="重置到 00:00"
    >
      <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/>
      </svg>
      <span>重置</span>
    </button>

    <div class="playback-info">
      <span class="status-indicator" :class="{ active: isPlaying }">
        {{ isPlaying ? '播放中' : '已暫停' }}
      </span>
      <span class="interval-info">每 {{ intervalDuration / 1000 }} 秒切換</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isPlaying: {
    type: Boolean,
    required: true
  },
  canPlay: {
    type: Boolean,
    default: true
  },
  canPause: {
    type: Boolean,
    default: true
  },
  intervalDuration: {
    type: Number,
    default: 3000
  }
})

defineEmits(['play', 'pause', 'reset'])
</script>

<style scoped>
.playback-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.control-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  min-width: 100px;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.icon {
  width: 18px;
  height: 18px;
}

.playback-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-left: 8px;
  font-size: 0.75rem;
}

.status-indicator {
  color: var(--text-secondary);
  font-weight: 500;
}

.status-indicator.active {
  color: var(--success-color);
}

.interval-info {
  color: var(--text-secondary);
}

@media (max-width: 767px) {
  .playback-controls {
    width: 100%;
  }

  .control-btn {
    flex: 1;
    min-width: 80px;
  }

  .playback-info {
    width: 100%;
    text-align: center;
    margin-left: 0;
    margin-top: 4px;
  }
}
</style>
