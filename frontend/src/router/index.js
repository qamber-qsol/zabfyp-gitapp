import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/auth/LoginView.vue'
import OtpView from '@/views/auth/OtpView.vue'
import StudentDashboardView from '@/views/student/DashboardView.vue'
import CoordinatorDashboardView from '@/views/coordinator/DashboardView.vue'
import CoordinatorGroupDetailView from '@/views/coordinator/GroupDetailView.vue'
import AdminDashboardView from '@/views/admin/DashboardView.vue'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    redirect: (to) => {
      const authStore = useAuthStore()
      const role = (authStore.user_role || 'student').toLowerCase()
      if (role === 'admin') return '/admin/dashboard'
      if (role === 'coordinator') return '/coordinator/dashboard'
      return '/student/dashboard'
    },
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guestOnly: true },
  },
  {
    path: '/verify-otp',
    name: 'verify-otp',
    component: OtpView,
    meta: { guestOnly: true },
  },
  {
    path: '/student/dashboard',
    name: 'student-dashboard',
    component: StudentDashboardView,
    meta: { requiresAuth: true, roles: ['student', 'coordinator', 'admin'] },
  },
  {
    path: '/coordinator/dashboard',
    name: 'coordinator-dashboard',
    component: CoordinatorDashboardView,
    meta: { requiresAuth: true, roles: ['coordinator', 'admin'] },
  },
  {
    path: '/coordinator/groups/:id',
    name: 'coordinator-group-detail',
    component: CoordinatorGroupDetailView,
    meta: { requiresAuth: true, roles: ['coordinator', 'admin'] },
  },
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: AdminDashboardView,
    meta: { requiresAuth: true, roles: ['admin'] },
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/admin/UserManagementView.vue'),
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/student-portal',
    name: 'StudentPortal',
    component: () => import('../views/student/StudentPortalView.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const userRole = (authStore.user_role || 'student').toLowerCase()

  const getDefaultRoute = (role) => {
    if (role === 'admin') return '/admin/dashboard'
    if (role === 'coordinator') return '/coordinator/dashboard'
    return '/student/dashboard'
  }

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.guestOnly && isAuthenticated) {
    next(getDefaultRoute(userRole))
  } else if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    // RBAC check: Redirect to appropriate role dashboard
    next(getDefaultRoute(userRole))
  } else {
    next()
  }
})

export default router
