import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    user_role: localStorage.getItem('user_role') || 'student',
    student_data: null,
    user_email: localStorage.getItem('user_email') || '',
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/auth/request-otp', { email })
        this.user_email = email
        localStorage.setItem('user_email', email)
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to request OTP code.'
        throw new Error(this.error)
      } finally {
        this.loading = false
      }
    },

    async verifyOtp(email, otp, new_password) {
      this.loading = true
      this.error = null
      try {
        // Step 1: Verify OTP and set password
        await api.post('/auth/verify-otp', {
          email,
          otp,
          new_password,
        })

        // Step 2: Authenticate and fetch JWT token
        const loginResponse = await api.post('/auth/login', {
          email,
          password: new_password,
        })

        const accessToken = loginResponse.data.access_token
        this.token = accessToken
        localStorage.setItem('access_token', accessToken)

        // Step 3: Fetch student profile data
        await this.fetchStudentData()

        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to verify OTP or log in.'
        throw new Error(this.error)
      } finally {
        this.loading = false
      }
    },

    async directLogin(email, password) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/auth/login', { email, password })
        const accessToken = response.data.access_token
        this.token = accessToken
        localStorage.setItem('access_token', accessToken)
        this.user_email = email
        localStorage.setItem('user_email', email)

        await this.fetchStudentData()
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Invalid email or password.'
        throw new Error(this.error)
      } finally {
        this.loading = false
      }
    },

    async fetchStudentData() {
      if (!this.token) return null
      try {
        const response = await api.get('/students/me')
        this.student_data = response.data
        if (response.data.role) {
          this.user_role = response.data.role
          localStorage.setItem('user_role', response.data.role)
        }
        return response.data
      } catch (err) {
        if (err.response?.status === 401) {
          this.logout()
        }
        return null
      }
    },

    logout() {
      this.token = ''
      this.student_data = null
      this.user_email = ''
      this.user_role = 'student'
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_email')
      localStorage.removeItem('user_role')
    },
  },
})
