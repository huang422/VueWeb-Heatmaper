/**
 * Vue Application Entry Point
 * Initializes Vue app with ECharts registration
 */

import { createApp } from 'vue'
import App from './App.vue'

// Import ECharts components for tree-shaking
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'

// Register only needed ECharts components
use([
  CanvasRenderer,
  PieChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

// Import global styles
import './assets/styles/main.css'

// Create and mount app
const app = createApp(App)
app.mount('#app')
