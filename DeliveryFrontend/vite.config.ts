import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server : {
    port : 3001,
    proxy : {
      '/shops/login' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false,
      }, 
      'shops/register' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      },
      'shops/orders' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      },
      'shops/accepted/orders' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      },
      'shops/rejected/orders' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      },
      'deliveries/orders' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      },
      'deliveries/accepted/orders' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      },
      'deliveries/rejected/orders' : {
        target : 'http://127.0.0.1:5500/',
        changeOrigin : true,
        secure : false
      },
    }
  },
})
