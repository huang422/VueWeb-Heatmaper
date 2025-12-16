/**
 * useAutoplay Composable
 * Manages automatic hour cycling with 3-second intervals
 */

import { ref, computed, watch, onUnmounted } from 'vue'

export function useAutoplay(initialHour = 0) {
  // State
  const currentHour = ref(initialHour)
  const isPlaying = ref(false)
  const intervalId = ref(null)
  const intervalDuration = 3000 // 3 seconds per FR-005

  // Computed
  const canPlay = computed(() => !isPlaying.value)
  const canPause = computed(() => isPlaying.value)

  // Methods
  function play() {
    if (isPlaying.value) return

    isPlaying.value = true

    // Start interval to cycle through hours
    intervalId.value = setInterval(() => {
      currentHour.value = (currentHour.value + 1) % 24
    }, intervalDuration)
  }

  function pause() {
    if (!isPlaying.value) return

    isPlaying.value = false

    if (intervalId.value) {
      clearInterval(intervalId.value)
      intervalId.value = null
    }
  }

  function reset() {
    pause()
    currentHour.value = 0
  }

  function setHour(hour) {
    // Pause auto-play when user manually sets hour (per FR-009)
    pause()
    currentHour.value = hour
  }

  function resume() {
    play()
  }

  // Cleanup on unmount
  onUnmounted(() => {
    pause()
  })

  return {
    // State
    currentHour,
    isPlaying,
    intervalDuration,

    // Computed
    canPlay,
    canPause,

    // Methods
    play,
    pause,
    reset,
    setHour,
    resume
  }
}
