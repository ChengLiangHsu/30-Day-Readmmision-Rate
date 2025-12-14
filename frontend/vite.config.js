import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/predict': 'http://localhost:5000',
      '/features': 'http://localhost:5000',
      '/cluster': 'http://localhost:5000',
      '/health': 'http://localhost:5000',
      '/history': 'http://localhost:5000'
    }
  }
})
