<template>
  <div class="min-h-screen bg-slate-50 flex flex-col font-sans">
    <!-- Top Navigation Bar -->
    <header class="bg-white border-b border-slate-100 shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <!-- Logo / Application Title -->
        <div class="flex items-center space-x-3">
          <div class="w-9 h-9 rounded-lg bg-primary flex items-center justify-center text-white font-bold text-lg shadow-sm">
            Z
          </div>
          <div>
            <h1 class="text-lg font-bold text-primary tracking-tight">SZABIST FYP Portal</h1>
            <p class="text-xs text-slate-400 font-medium">GitHub & Project Management System</p>
          </div>
        </div>

        <!-- Navigation Links -->
        <div v-if="authStore.isAuthenticated" class="flex items-center space-x-6">
          <nav class="hidden md:flex items-center space-x-1">
            <router-link
              to="/student/dashboard"
              class="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-600 hover:text-primary hover:bg-slate-50 transition-colors"
              active-class="text-primary bg-primary-light/60"
            >
              Student Portal
            </router-link>

            <router-link
              v-if="['coordinator', 'admin'].includes((authStore.user_role || '').toLowerCase())"
              to="/coordinator/dashboard"
              class="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-600 hover:text-primary hover:bg-slate-50 transition-colors"
              active-class="text-primary bg-primary-light/60"
            >
              Coordinator Panel
            </router-link>

            <router-link
              v-if="(authStore.user_role || '').toLowerCase() === 'admin'"
              to="/admin/dashboard"
              class="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-600 hover:text-red-600 hover:bg-red-50 transition-colors"
              active-class="text-red-600 bg-red-50"
            >
              Admin Controls
            </router-link>
          </nav>

          <!-- Navigation Right (User Info & Logout) -->
          <div class="flex items-center space-x-3">
            <div class="hidden sm:flex items-center space-x-2 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200/60">
              <div class="w-2 h-2 rounded-full bg-emerald-500"></div>
              <span class="text-xs font-medium text-slate-600">
                {{ authStore.student_data?.email || authStore.user_email }}
              </span>
            </div>

            <button
              @click="handleLogout"
              class="inline-flex items-center justify-center px-4 py-2 text-xs font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 hover:text-slate-900 rounded-lg transition-all duration-200 ease-in-out cursor-pointer"
            >
              <svg class="w-4 h-4 mr-1.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-100 py-4 text-center text-xs text-slate-400">
      &copy; {{ new Date().getFullYear() }} SZABIST Karachi Campus. All rights reserved.
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
