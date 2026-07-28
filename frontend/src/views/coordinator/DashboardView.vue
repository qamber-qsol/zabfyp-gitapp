<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <div class="inline-flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-primary mb-1">
          <span class="w-2 h-2 rounded-full bg-primary"></span>
          <span>Coordinator Panel</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight">Global Overview & Proposals</h2>
        <p class="text-sm text-slate-500 mt-1">
          Review FYP project proposals, monitor GitHub organization access, and manage team approvals.
        </p>
      </div>

      <div class="flex items-center space-x-2">
        <button
          @click="fetchData"
          class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition-all duration-200 flex items-center"
        >
          <svg class="w-3.5 h-3.5 mr-1.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh Overview
        </button>
      </div>
    </div>

    <!-- Metrics Grid (6 Stats Cards) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <!-- Total Students -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Total Students</p>
          <h3 class="text-3xl font-bold text-slate-900 mt-1">{{ metrics.total_students }}</h3>
        </div>
        <div class="w-12 h-12 rounded-xl bg-primary-light text-primary flex items-center justify-center">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
      </div>

      <!-- Total Groups -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Total Groups</p>
          <h3 class="text-3xl font-bold text-slate-900 mt-1">{{ metrics.total_groups }}</h3>
        </div>
        <div class="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
      </div>

      <!-- Approved Groups -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Approved Groups</p>
          <h3 class="text-3xl font-bold text-emerald-600 mt-1">{{ metrics.approved_groups }}</h3>
        </div>
        <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>

      <!-- Rejected Groups -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Rejected Groups</p>
          <h3 class="text-3xl font-bold text-red-500 mt-1">{{ metrics.rejected_groups }}</h3>
        </div>
        <div class="w-12 h-12 rounded-xl bg-red-50 text-red-500 flex items-center justify-center">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>

      <!-- Pending GitHub Invites -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Pending Invites</p>
          <h3 class="text-3xl font-bold text-amber-500 mt-1">{{ metrics.pending_github_invites }}</h3>
        </div>
        <div class="w-12 h-12 rounded-xl bg-amber-50 text-amber-500 flex items-center justify-center">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </div>
      </div>

      <!-- Active Repositories -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Active Repositories</p>
          <h3 class="text-3xl font-bold text-primary mt-1">{{ metrics.active_repositories }}</h3>
        </div>
        <div class="w-12 h-12 rounded-xl bg-primary-light text-primary flex items-center justify-center">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Groups List Table -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
      <!-- Section Header & Filter Tabs -->
      <div class="p-6 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h3 class="text-lg font-bold text-slate-900 tracking-tight">Project Proposals & Groups</h3>
          <p class="text-xs text-slate-500">Filter and select a group to review details and approve proposals</p>
        </div>

        <div class="flex items-center bg-slate-100 p-1 rounded-lg">
          <button
            v-for="filter in ['all', 'pending_approval', 'approved', 'rejected']"
            :key="filter"
            @click="currentFilter = filter"
            :class="[
              'px-3 py-1.5 text-xs font-semibold rounded-md capitalize transition-all duration-200',
              currentFilter === filter ? 'bg-white text-primary shadow-sm' : 'text-slate-500 hover:text-slate-800'
            ]"
          >
            {{ filter.replace('_', ' ') }}
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-100 text-xs font-semibold text-slate-400 uppercase tracking-wider">
              <th class="py-3.5 px-6">ID</th>
              <th class="py-3.5 px-6">Group Name</th>
              <th class="py-3.5 px-6">Project Title</th>
              <th class="py-3.5 px-6">Members</th>
              <th class="py-3.5 px-6">Status</th>
              <th class="py-3.5 px-6 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-sm">
            <tr v-if="filteredGroups.length === 0">
              <td colspan="6" class="py-8 text-center text-xs text-slate-400">
                No project groups found for the selected filter.
              </td>
            </tr>
            <tr
              v-for="group in filteredGroups"
              :key="group.id"
              class="hover:bg-slate-50/80 transition-colors duration-150"
            >
              <td class="py-4 px-6 font-mono font-bold text-xs text-slate-500">#{{ group.id }}</td>
              <td class="py-4 px-6 font-semibold text-slate-900">{{ group.name }}</td>
              <td class="py-4 px-6 text-slate-600 max-w-xs truncate">{{ group.project_title || 'N/A' }}</td>
              <td class="py-4 px-6 text-xs text-slate-500">
                <span class="px-2 py-1 bg-slate-100 rounded text-slate-700 font-medium">
                  {{ group.member_emails ? group.member_emails.length : 0 }} member(s)
                </span>
              </td>
              <td class="py-4 px-6">
                <span
                  :class="[
                    'px-2.5 py-0.5 text-xs font-bold rounded-full uppercase tracking-wider',
                    group.status === 'approved' ? 'bg-emerald-100 text-emerald-700 border border-emerald-200' :
                    group.status === 'rejected' ? 'bg-red-100 text-red-700 border border-red-200' :
                    'bg-amber-100 text-amber-700 border border-amber-200'
                  ]"
                >
                  {{ group.status }}
                </span>
              </td>
              <td class="py-4 px-6 text-right">
                <router-link
                  :to="`/coordinator/groups/${group.id}`"
                  class="inline-flex items-center px-3 py-1.5 bg-primary/10 hover:bg-primary text-primary hover:text-white text-xs font-bold rounded-lg transition-all duration-200"
                >
                  Review Details
                  <svg class="w-3.5 h-3.5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()

const metrics = ref({
  total_students: 0,
  total_groups: 0,
  approved_groups: 0,
  rejected_groups: 0,
  pending_github_invites: 0,
  active_repositories: 0,
})

const groups = ref([])
const currentFilter = ref('pending_approval')

const filteredGroups = computed(() => {
  if (currentFilter.value === 'all') return groups.value
  return groups.value.filter((g) => g.status === currentFilter.value)
})

const fetchData = async () => {
  try {
    const headers = { Authorization: `Bearer ${authStore.token}` }
    
    // Metrics overview
    const overviewRes = await axios.get('/api/v1/dashboard/overview', { headers })
    metrics.value = overviewRes.data

    // All groups list
    const groupsRes = await axios.get('/api/v1/coordinator/groups', { headers })
    groups.value = groupsRes.data
  } catch (err) {
    console.error('Failed to load coordinator dashboard data:', err)
  }
}

onMounted(() => {
  fetchData()
})
</script>
