import axios from 'axios'
import router from '@/router'

const api = axios.create({
  // Use Vercel URL in production, keep localhost for your local testing
  baseURL: isProduction 
    ? 'https://zabfyp-backend.vercel.app/api/v1' 
    : 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  }
});

const getToken = () => localStorage.getItem('access_token')

const clearAuthState = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_email')
  localStorage.removeItem('user_role')
}

api.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status
    const currentPath = router.currentRoute.value?.path

    if (status === 401 && currentPath !== '/login') {
      clearAuthState()
      router.push('/login')
    }

    return Promise.reject(error)
  }
)

export default api
