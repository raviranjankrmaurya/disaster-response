import axios from 'axios'

// Dev: VITE_API_BASE_URL is unset -> requests go relative, Vite's dev
// proxy forwards /api/* to localhost:8000.
// Prod (Vercel): set VITE_API_BASE_URL to your deployed backend URL.
const api = axios.create({
  baseURL: '',
})

export default api
