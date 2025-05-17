import axios from 'axios'

const api = axios.create({
  baseURL: '/api',          // alle Requests an /api/... gehen über Vite-Proxy
  withCredentials: true,    // sendet automatisch Session-Cookies mit
})

export default api