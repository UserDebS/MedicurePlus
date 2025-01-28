import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, "./src"),
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/login': {
        target: 'http://127.0.0.1:5500/',
        changeOrigin: true,
        secure: false
      },
      '/register': {
        target: 'http://127.0.0.1:5500/',
        changeOrigin: true,
        secure: false
      },
      '/suggestions' : {
        target : 'http://127.0.0.1:5500/',
          changeOrigin : true,
          secure : false
      },
      '/find' : {
        target : 'http://127.0.0.1:5500/',
          changeOrigin : true,
          secure : false
      },
      '/order' : {
        target : 'http://127.0.0.1:5500/',
          changeOrigin : true,
          secure : false
      },
      '/upload': {
        target: 'http://127.0.0.1:5500/',
        changeOrigin: true,
        secure: false
      },
      '/medicines': {
        target: 'http://127.0.0.1:5500/',
        changeOrigin: true,
        secure: false
      },
      '/recommendation': {
        target: 'http://127.0.0.1:5500/',
        changeOrigin: true,
        secure: false
      }
    },
  },
  preview: {
    port: 3000
  }
})
