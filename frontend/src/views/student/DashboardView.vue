<template>
  <div class="space-y-8">
    <!-- Welcome Header -->
    <div class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <div class="inline-flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-primary mb-1">
          <span class="w-2 h-2 rounded-full bg-primary"></span>
          <span>Student Dashboard</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight">
          Welcome back, {{ student?.name || student?.email || 'Student' }}
        </h2>
        <p class="text-sm text-slate-500 mt-1">
          Manage your FYP Project Group and GitHub Organization repository access.
        </p>
      </div>

      <div class="flex items-center space-x-3 bg-slate-50 p-3 rounded-lg border border-slate-200/60">
        <div class="text-right">
          <p class="text-xs text-slate-400 font-medium">Verification Status</p>
          <p class="text-xs font-bold text-emerald-600 flex items-center justify-end mt-0.5">
            <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Verified Account
          </p>
        </div>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Group Status Card -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-slate-100 space-y-6">
          <div class="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h3 class="text-lg font-bold text-slate-900 tracking-tight">FYP Project Group</h3>
              <p class="text-xs text-slate-500">Current project proposal and membership status</p>
            </div>

            <!-- Group Status Badge -->
            <div v-if="group">
              <span
                :class="[
                  'px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wider',
                  group.status === 'approved' ? 'bg-emerald-100 text-emerald-700 border border-emerald-200' :
                  group.status === 'rejected' ? 'bg-red-100 text-red-700 border border-red-200' :
                  'bg-amber-100 text-amber-700 border border-amber-200'
                ]"
              >
                {{ group.status }}
              </span>
            </div>
          </div>

          <!-- If Student is in a Group -->
          <div v-if="group" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-slate-50 p-4 rounded-lg border border-slate-100">
              <div>
                <p class="text-xs text-slate-400 font-medium">Group ID</p>
                <p class="text-sm font-bold text-slate-800">Group #{{ group.id }}</p>
              </div>
              <div>
                <p class="text-xs text-slate-400 font-medium">Group Name</p>
                <p class="text-sm font-bold text-slate-800">{{ group.name }}</p>
              </div>
            </div>

            <div>
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Project Title</p>
              <p class="text-base font-semibold text-slate-900 mt-1">{{ group.project_title || 'N/A' }}</p>
            </div>

            <div>
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Proposal Description</p>
              <p class="text-sm text-slate-600 mt-1 whitespace-pre-line">{{ group.description || 'No description provided.' }}</p>
            </div>

            <div>
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Team Members</p>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="email in group.member_emails"
                  :key="email"
                  class="px-3 py-1 bg-slate-100 text-slate-700 rounded-lg text-xs font-medium border border-slate-200 flex items-center"
                >
                  <svg class="w-3.5 h-3.5 mr-1 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  {{ email }}
                </span>
              </div>
            </div>
          </div>

          <!-- If Student Has No Group: Show Creation Form -->
          <div v-else class="space-y-6">
            <div class="bg-blue-50 border border-blue-100 rounded-lg p-4 text-xs text-blue-800">
              You are currently not a member of any project group. Fill out the form below to propose a new project group.
            </div>

            <form @submit.prevent="handleCreateGroup" class="space-y-4">
              <div>
                <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Group Name</label>
                <input
                  v-model="groupForm.name"
                  type="text"
                  required
                  placeholder="e.g. AI Vision Team"
                  class="w-full px-4 py-2 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
                />
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Project Title</label>
                <input
                  v-model="groupForm.project_title"
                  type="text"
                  required
                  placeholder="e.g. Autonomous Traffic Analytics"
                  class="w-full px-4 py-2 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
                />
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Description</label>
                <textarea
                  v-model="groupForm.description"
                  rows="3"
                  required
                  placeholder="Describe your project goals and methodology..."
                  class="w-full px-4 py-2 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
                ></textarea>
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Member Emails (Comma separated)</label>
                <input
                  v-model="groupForm.member_emails_raw"
                  type="text"
                  placeholder="peer1@szabist.pk, peer2@szabist.pk"
                  class="w-full px-4 py-2 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
                />
              </div>

              <button
                type="submit"
                :disabled="groupLoading"
                class="px-6 py-2.5 bg-primary hover:bg-primary-hover text-white text-xs font-bold rounded-lg shadow-sm transition-all duration-200 disabled:opacity-50"
              >
                Submit Group Proposal
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- GitHub Organization & Repository Invite Card -->
      <div class="space-y-6">
        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100 space-y-6">
          <div class="border-b border-slate-100 pb-4">
            <h3 class="text-lg font-bold text-slate-900 tracking-tight flex items-center">
              <svg class="w-5 h-5 mr-2 text-slate-700" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
              </svg>
              GitHub Org Access
            </h3>
            <p class="text-xs text-slate-500 mt-1">Repository invite status and access management</p>
          </div>

          <!-- Alert for Unapproved Group -->
          <div v-if="!group || group.status !== 'approved'" class="p-4 bg-slate-50 rounded-lg border border-slate-100 text-xs text-slate-500 leading-relaxed">
            GitHub repository invitations can only be requested after your group proposal is marked as <strong class="text-slate-700">Approved</strong> by a coordinator.
          </div>

          <!-- If Group is Approved -->
          <div v-else class="space-y-5">
            
            <!-- Invite Pending / Active Badge -->
            <div v-if="githubStatus && ['sent', 'active', 'pending'].includes(githubStatus.invite_status)" class="space-y-4">
              <div class="p-4 bg-slate-50 rounded-lg border border-slate-200/80 space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Invite Status</span>
                  <span
                    :class="[
                      'px-2.5 py-0.5 text-xs font-bold rounded-full uppercase tracking-wider',
                      githubStatus.invite_status === 'sent' || githubStatus.invite_status === 'active'
                        ? 'bg-emerald-100 text-emerald-700 border border-emerald-200'
                        : 'bg-amber-100 text-amber-700 border border-amber-200'
                    ]"
                  >
                    {{ githubStatus.invite_status }}
                  </span>
                </div>

                <div>
                  <p class="text-xs text-slate-400 font-medium">GitHub Username</p>
                  <p class="text-sm font-bold text-slate-800 font-mono">@{{ githubStatus.github_username }}</p>
                </div>

                <div v-if="githubStatus.repo_name">
                  <p class="text-xs text-slate-400 font-medium">Repository Name</p>
                  <p class="text-xs font-semibold text-primary font-mono">{{ githubStatus.repo_name }}</p>
                </div>
              </div>

              <div class="p-3 bg-emerald-50 border border-emerald-100 rounded-lg text-xs text-emerald-800">
                An invitation has been dispatched to your GitHub account. Check your email or GitHub notifications to accept the invitation.
              </div>
            </div>

            <!-- Request Invite Form (If not yet sent) -->
            <div v-else class="space-y-4">
              <form @submit.prevent="handleRequestInvite" class="space-y-4">
                <div>
                  <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                    Your GitHub Username
                  </label>
                  <input
                    v-model="githubUsername"
                    type="text"
                    required
                    placeholder="octocat"
                    class="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary placeholder:text-slate-300 font-mono"
                  />
                </div>

                <button
                  type="submit"
                  :disabled="inviteLoading"
                  class="w-full py-3 px-4 bg-primary hover:bg-primary-hover text-white text-xs font-bold rounded-lg shadow-md hover:shadow-lg transition-all duration-200 disabled:opacity-50 flex items-center justify-center cursor-pointer"
                >
                  <span v-if="inviteLoading">Processing...</span>
                  <span v-else class="flex items-center">
                    <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                    Request Repository Invite
                  </span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()

const student = ref(null)
const group = ref(null)
const githubStatus = ref(null)

const groupForm = ref({
  name: '',
  project_title: '',
  description: '',
  member_emails_raw: '',
})
const groupLoading = ref(false)

const githubUsername = ref('')
const inviteLoading = ref(false)

const fetchData = async () => {
  student.value = await authStore.fetchStudentData()

  // Fetch group details
  try {
    const groupRes = await axios.get('/api/v1/groups/me', {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    group.value = groupRes.data
  } catch (err) {
    group.value = null
  }

  // Fetch GitHub invite status
  try {
    const ghRes = await axios.get('/api/v1/github/status', {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    githubStatus.value = ghRes.data
    if (ghRes.data?.github_username) {
      githubUsername.value = ghRes.data.github_username
    }
  } catch (err) {
    githubStatus.value = null
  }
}

const handleCreateGroup = async () => {
  groupLoading.value = true
  try {
    const emails = groupForm.value.member_emails_raw
      .split(',')
      .map((e) => e.trim())
      .filter((e) => e.length > 0)

    const payload = {
      name: groupForm.value.name,
      project_title: groupForm.value.project_title,
      description: groupForm.value.description,
      member_emails: emails,
    }

    const res = await axios.post('/api/v1/groups/', payload, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    group.value = res.data
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to create project group.')
  } finally {
    groupLoading.value = false
  }
}

const handleRequestInvite = async () => {
  if (!githubUsername.value) return
  inviteLoading.value = true
  try {
    const res = await axios.post(
      '/api/v1/github/invite',
      { github_username: githubUsername.value },
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    )
    githubStatus.value = res.data
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to request GitHub invite.')
  } finally {
    inviteLoading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>
