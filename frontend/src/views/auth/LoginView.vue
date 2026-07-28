<template>
  <div class="flex items-center justify-center min-h-[calc(100vh-12rem)] py-12 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-md space-y-8 bg-white p-8 sm:p-10 rounded-xl shadow-md border border-slate-100 transition-all duration-300">
      
      <!-- Card Header -->
      <div class="text-center">
        <div class="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-primary-light text-primary mb-4">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight">Student Portal Sign In</h2>
        <p class="mt-2 text-sm text-slate-500">
          Enter your official SZABIST email address to receive a verification code.
        </p>
      </div>

      <!-- Mode Selector (OTP Request vs Password Login) -->
      <div class="flex bg-slate-100 p-1 rounded-lg">
        <button
          type="button"
          @click="authMode = 'otp'"
          :class="[
            'flex-1 py-1.5 text-xs font-semibold rounded-md transition-all duration-200',
            authMode === 'otp' ? 'bg-white text-primary shadow-sm' : 'text-slate-500 hover:text-slate-800'
          ]"
        >
          Request OTP
        </button>
        <button
          type="button"
          @click="authMode = 'password'"
          :class="[
            'flex-1 py-1.5 text-xs font-semibold rounded-md transition-all duration-200',
            authMode === 'password' ? 'bg-white text-primary shadow-sm' : 'text-slate-500 hover:text-slate-800'
          ]"
        >
          Password Login
        </button>
      </div>

      <!-- Error Alert -->
      <div v-if="errorMessage" class="p-3.5 bg-red-50 border border-red-200 rounded-lg text-xs text-red-600 font-medium">
        {{ errorMessage }}
      </div>

      <!-- Form -->
      <form class="mt-6 space-y-5" @submit.prevent="handleSubmit">
        <div>
          <label for="email" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
            SZABIST Email
          </label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="student@szabist.pk"
            class="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-200 placeholder:text-slate-300"
          />
        </div>

        <div v-if="authMode === 'password'">
          <label for="password" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
            Password
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
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
              Processing...
            </span>
            <span v-else>
              {{ authMode === 'otp' ? 'Send OTP Code' : 'Sign In' }}
            </span>
          </button>
        </div>
      </form>

      <!-- Footer Note -->
      <div class="text-center text-xs text-slate-400">
        First time user? Enter your SZABIST email above to request a verification OTP.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const authMode = ref('otp')
const loading = ref(false)
const errorMessage = ref('')

const handleSubmit = async () => {
  if (!email.value) return
  loading.value = true
  errorMessage.value = ''

  try {
    if (authMode.value === 'otp') {
      await authStore.login(email.value)
      router.push({ path: '/verify-otp', query: { email: email.value } })
    } else {
      await authStore.directLogin(email.value, password.value)
      router.push('/student/dashboard')
    }
  } catch (err) {
    errorMessage.value = err.message || 'An error occurred during sign in.'
  } finally {
    loading.value = false
  }
}
</script>
