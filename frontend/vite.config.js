import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000', // Assuming local python server or similar, but for Vercel Dev it's handled differently. 
        // Actually, for Vercel dev we don't need this if we run `vercel dev`.
        // But if user runs `npm run dev` and `python api/server.py` separately, this helps.
        // Since we are Serverless, we don't have a single entry point easily.
        // So I'll just leave it empty or comment it out unless user asks.
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
