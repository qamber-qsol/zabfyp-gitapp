<template>
  <div class="space-y-8">
    <!-- Navigation Back Link & Header -->
    <div class="flex items-center justify-between">
      <router-link
        to="/coordinator/dashboard"
        class="inline-flex items-center text-xs font-semibold text-slate-500 hover:text-primary transition-colors"
      >
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Coordinator Dashboard
      </router-link>

      <span
        v-if="details?.group_info"
        :class="[
          'px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wider',
          details.group_info.status === 'approved' ? 'bg-emerald-100 text-emerald-700 border border-emerald-200' :
          details.group_info.status === 'rejected' ? 'bg-red-100 text-red-700 border border-red-200' :
          'bg-amber-100 text-amber-700 border border-amber-200'
        ]"
      >
        Status: {{ details.group_info.status }}
      </span>
    </div>

    <!-- Error / Loading -->
    <div v-if="loading" class="bg-white p-12 rounded-xl shadow-sm border border-slate-100 text-center text-slate-400">
      Loading group details...
    </div>

    <div v-else-if="!details" class="bg-white p-12 rounded-xl shadow-sm border border-slate-100 text-center text-red-500 font-semibold">
      Group details not found.
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Left Column: Proposal Details & Review Action Card -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Proposal Info Card -->
        <div class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-slate-100 space-y-6">
          <div>
            <span class="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">Group #{{ details.group_info.id }}</span>
            <h2 class="text-2xl font-bold text-slate-900 tracking-tight mt-1">{{ details.group_info.name }}</h2>
          </div>

          <div class="bg-slate-50 p-4 rounded-lg border border-slate-100 space-y-1">
            <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Project Title</p>
            <p class="text-base font-bold text-slate-900">{{ details.group_info.project_title || 'N/A' }}</p>
          </div>

          <div>
            <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Proposal Description</p>
            <p class="text-sm text-slate-600 leading-relaxed whitespace-pre-line bg-slate-50/50 p-4 rounded-lg border border-slate-100">
              {{ details.group_info.description || 'No description provided.' }}
            </p>
          </div>

          <!-- Coordinator Action Form (Approve / Reject) -->
          <div class="border-t border-slate-100 pt-6 space-y-4">
            <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider">Coordinator Decision & Feedback</h3>
            
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Feedback Comment (Optional)</label>
              <textarea
                v-model="feedbackInput"
                rows="3"
                placeholder="Provide feedback or notes to the students regarding approval/rejection..."
                class="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary placeholder:text-slate-300"
              ></textarea>
            </div>

            <div class="flex items-center space-x-4">
              <button
                @click="handleStatusUpdate('approved')"
                :disabled="actionLoading"
                class="flex-1 py-2.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg shadow-sm transition-all duration-200 disabled:opacity-50 flex items-center justify-center cursor-pointer"
              >
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Approve Proposal
              </button>

              <button
                @click="handleStatusUpdate('rejected')"
                :disabled="actionLoading"
                class="flex-1 py-2.5 px-4 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-lg shadow-sm transition-all duration-200 disabled:opacity-50 flex items-center justify-center cursor-pointer"
              >
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                Reject Proposal
              </button>
            </div>
          </div>
        </div>

        <!-- Discussion Thread Card -->
        <div class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-slate-100 space-y-6">
          <h3 class="text-base font-bold text-slate-900 tracking-tight flex items-center">
            <svg class="w-5 h-5 mr-2 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
            </svg>
            Coordinator Discussion & Comments History
          </h3>

          <div v-if="details.comments.length === 0" class="p-4 bg-slate-50 rounded-lg text-xs text-slate-400 text-center">
            No system comments or feedback recorded yet.
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="comment in details.comments"
              :key="comment.id"
              class="p-4 bg-slate-50 rounded-lg border border-slate-100 space-y-1"
            >
              <div class="flex items-center justify-between text-xs text-slate-400">
                <span class="font-semibold text-slate-700">Coordinator Remark</span>
                <span>{{ new Date(comment.created_at).toLocaleString() }}</span>
              </div>
              <p class="text-sm text-slate-700 whitespace-pre-line">{{ comment.content }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Team Members & GitHub Invite Statuses Card -->
      <div class="space-y-6">
        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100 space-y-6">
          <div class="border-b border-slate-100 pb-4">
            <h3 class="text-base font-bold text-slate-900 tracking-tight">Team Members</h3>
            <p class="text-xs text-slate-500">Student accounts & GitHub invitation statuses</p>
          </div>

          <div class="space-y-4">
            <div
              v-for="member in details.members"
              :key="member.id"
              class="p-4 bg-slate-50 rounded-lg border border-slate-100 space-y-2"
            >
              <div class="flex items-center justify-between">
                <p class="text-sm font-bold text-slate-900">{{ member.name || 'Unnamed Student' }}</p>
                <span
                  :class="[
                    'px-2 py-0.5 text-[10px] font-bold rounded uppercase',
                    member.is_verified ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                  ]"
                >
                  {{ member.is_verified ? 'Verified' : 'Unverified' }}
                </span>
              </div>

              <p class="text-xs text-slate-500 font-mono">{{ member.email }}</p>

              <!-- GitHub Invite Status for member -->
              <div class="pt-2 border-t border-slate-200/60 flex items-center justify-between text-xs">
                <span class="text-slate-400 font-medium">GitHub Status</span>
                <span
                  :class="[
                    'px-2 py-0.5 text-[10px] font-bold rounded uppercase tracking-wider',
                    getInviteStatus(member.id) === 'sent' || getInviteStatus(member.id) === 'active'
                      ? 'bg-emerald-100 text-emerald-700'
                      : 'bg-slate-200 text-slate-600'
                  ]"
                >
                  {{ getInviteStatus(member.id) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Repository Info Card -->
        <div v-if="details.repository_info" class="bg-white p-6 rounded-xl shadow-sm border border-slate-100 space-y-4">
          <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider border-b border-slate-100 pb-3">
            Group Repository
          </h3>

          <div>
            <p class="text-xs text-slate-400 font-medium">Repo Name</p>
            <p class="text-sm font-bold text-primary font-mono mt-0.5">{{ details.repository_info.repo_name }}</p>
          </div>

          <div>
            <p class="text-xs text-slate-400 font-medium">Creation Status</p>
            <span class="inline-block mt-1 px-2.5 py-0.5 text-xs font-bold rounded bg-blue-100 text-blue-700 uppercase">
              {{ details.repository_info.status }}
            </span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const route = useRoute()
const authStore = useAuthStore()

const details = ref(null)
const loading = ref(true)
const feedbackInput = ref('')
const actionLoading = ref(false)

const groupId = route.params.id

const fetchDetails = async () => {
  loading.value = true
  try {
    const res = await axios.get(`/api/v1/coordinator/groups/${groupId}/details`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    details.value = res.data
  } catch (err) {
    console.error('Failed to load group details:', err)
  } finally {
    loading.value = false
  }
}

const getInviteStatus = (studentId) => {
  if (!details.value?.invite_statuses) return 'not_requested'
  const inv = details.value.invite_statuses.find((i) => i.student_id === studentId)
  return inv ? inv.invite_status : 'not_requested'
}

const handleStatusUpdate = async (newStatus) => {
  actionLoading.value = true
  try {
    const payload = {
      status: newStatus,
      feedback: feedbackInput.value,
    }
    await axios.patch(`/api/v1/coordinator/groups/${groupId}/status`, payload, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    feedbackInput.value = ''
    await fetchDetails()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to update group status.')
  } finally {
    actionLoading.value = false
  }
}

onMounted(() => {
  fetchDetails()
})
</script>
