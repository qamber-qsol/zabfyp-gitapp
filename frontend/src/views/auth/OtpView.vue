<template>
  <div class="flex items-center justify-center min-h-[calc(100vh-12rem)] py-12 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-md space-y-8 bg-white p-8 sm:p-10 rounded-xl shadow-md border border-slate-100 transition-all duration-300">
      
      <!-- Header -->
      <div class="text-center">
        <div class="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-primary-light text-primary mb-4">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight">Verify Verification OTP</h2>
        <p class="mt-2 text-sm text-slate-500">
          Enter the 6-digit verification code sent to <strong class="text-slate-700">{{ email }}</strong>.
        </p>
      </div>

      <!-- Error Alert -->
      <div v-if="errorMessage" class="p-3.5 bg-red-50 border border-red-200 rounded-lg text-xs text-red-600 font-medium">
        {{ errorMessage }}
      </div>

      <!-- Success Alert -->
      <div v-if="successMessage" class="p-3.5 bg-emerald-50 border border-emerald-200 rounded-lg text-xs text-emerald-600 font-medium">
        {{ successMessage }}
      </div>

      <!-- Form -->
      <form class="mt-6 space-y-5" @submit.prevent="handleVerify">
        <div>
          <label for="otp" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
            6-Digit OTP Code
          </label>
          <input
            id="otp"
            v-model="otp"
            type="text"
            maxlength="6"
            required
            placeholder="123456"
            class="w-full px-4 py-2.5 text-center text-lg font-mono font-bold tracking-widest rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-200 placeholder:text-slate-300"
          />
        </div>

        <div>
          <label for="new_password" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
            New Account Password
          </label>
          <input
            id="new_password"
            v-model="newPassword"
            type="password"
            required
            minlength="8"
            placeholder="Minimum 8 characters"
            class="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-200 placeholder:text-slate-300"
          />
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-3 px-4 rounded-lg text-sm font-semibold text-white bg-primary hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary shadow-md hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Verifying...
            </span>
            <span v-else>
              Verify OTP & Set Password
            </span>
          </button>
        </div>
      </form>

      <!-- Back to Login -->
      <div class="text-center">
        <router-link to="/login" class="text-xs font-semibold text-primary hover:underline">
          &larr; Back to Email Sign In
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const otp = ref('')
const newPassword = ref('')
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

onMounted(() => {
  email.value = route.query.email || authStore.user_email || ''
  if (!email.value) {
    router.push('/login')
  }
})

const handleVerify = async () => {
  if (!otp.value || !newPassword.value) return
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await authStore.verifyOtp(email.value, otp.value, newPassword.value)
    successMessage.value = 'Account verified successfully! Redirecting...'
    setTimeout(() => {
      router.push('/student/dashboard')
    }, 1000)
  } catch (err) {
    errorMessage.value = err.message || 'Invalid OTP code or verification failed.'
  } finally {
    loading.value = false
  }
}
</script>
