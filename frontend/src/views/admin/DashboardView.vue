<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <div class="inline-flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-red-600 mb-1">
          <span class="w-2 h-2 rounded-full bg-red-600"></span>
          <span>System Administrator Panel</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight">System Controls & Overrides</h2>
        <p class="text-sm text-slate-500 mt-1">
          Provision staff accounts, execute student record manual overrides, force GitHub invites, and perform system cleanups.
        </p>
      </div>
    </div>

    <!-- Alert Messages -->
    <div v-if="successMsg" class="p-4 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold rounded-xl">
      {{ successMsg }}
    </div>
    <div v-if="errorMsg" class="p-4 bg-red-50 border border-red-200 text-red-700 text-xs font-semibold rounded-xl">
      {{ errorMsg }}
    </div>

    <!-- Main Admin Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <!-- Card 1: Provision New Staff -->
      <div class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-slate-100 space-y-6">
        <div class="border-b border-slate-100 pb-4">
          <h3 class="text-lg font-bold text-slate-900 tracking-tight flex items-center">
            <svg class="w-5 h-5 mr-2 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
            Provision Staff User
          </h3>
          <p class="text-xs text-slate-500 mt-0.5">Create a new Coordinator or Administrator account</p>
        </div>

        <form @submit.prevent="handleProvisionStaff" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Official Email</label>
            <input
              v-model="staffForm.email"
              type="email"
              required
              placeholder="coordinator@szabist.pk"
              class="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Temporary Password</label>
            <input
              v-model="staffForm.password"
              type="password"
              required
              minlength="8"
              placeholder="Minimum 8 characters"
              class="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Assign Role</label>
            <select
              v-model="staffForm.role"
              required
              class="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary bg-white"
            >
              <option value="coordinator">Coordinator</option>
              <option value="admin">System Administrator</option>
            </select>
          </div>

          <button
            type="submit"
            :disabled="staffLoading"
            class="w-full py-3 px-4 bg-primary hover:bg-primary-hover text-white text-xs font-bold rounded-lg shadow-md transition-all duration-200 cursor-pointer disabled:opacity-50"
          >
            Provision Staff Account
          </button>
        </form>
      </div>

      <!-- Card 2: Force GitHub Invite Override -->
      <div class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-slate-100 space-y-6">
        <div class="border-b border-slate-100 pb-4">
          <h3 class="text-lg font-bold text-slate-900 tracking-tight flex items-center">
            <svg class="w-5 h-5 mr-2 text-primary" fill="currentColor" viewBox="0 0 24 24">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
            </svg>
            Force GitHub Invite
          </h3>
          <p class="text-xs text-slate-500 mt-0.5">Bypass group status checks to dispatch an immediate org invitation</p>
        </div>

        <form @submit.prevent="handleForceInvite" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Student ID</label>
            <input
              v-model.number="inviteForm.student_id"
              type="number"
              required
              placeholder="e.g. 42"
              class="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">GitHub Username (Optional)</label>
            <input
              v-model="inviteForm.github_username"
              type="text"
              placeholder="Leave blank to use student's stored username"
              class="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary font-mono"
            />
          </div>

          <button
            type="submit"
            :disabled="inviteLoading"
            class="w-full py-3 px-4 bg-primary hover:bg-primary-hover text-white text-xs font-bold rounded-lg shadow-md transition-all duration-200 cursor-pointer disabled:opacity-50"
          >
            Dispatch Force Invitation
          </button>
        </form>
      </div>

      <!-- Card 3: Student Manual Record Override -->
      <div class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-slate-100 space-y-6">
        <div class="border-b border-slate-100 pb-4">
          <h3 class="text-lg font-bold text-slate-900 tracking-tight flex items-center">
            <svg class="w-5 h-5 mr-2 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Student Record Manual Override
          </h3>
          <p class="text-xs text-slate-500 mt-0.5">Edit email typos, link/unlink group IDs, or fix GitHub handles</p>
        </div>

        <form @submit.prevent="handleOverrideStudent" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Target Student ID</label>
            <input
              v-model.number="overrideForm.student_id"
              type="number"
              required
              placeholder="e.g. 1"
              class="w-full px-4 py-2.5 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Full Name</label>
              <input
                v-model="overrideForm.name"
                type="text"
                placeholder="Updated Name"
                class="w-full px-4 py-2 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Email</label>
              <input
                v-model="overrideForm.email"
                type="email"
                placeholder="student@szabist.pk"
                class="w-full px-4 py-2 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">Group ID (Blank = Unlink)</label>
              <input
                v-model.number="overrideForm.group_id"
                type="number"
                placeholder="e.g. 5"
                class="w-full px-4 py-2 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">GitHub Username</label>
              <input
                v-model="overrideForm.github_username"
                type="text"
                placeholder="octocat"
                class="w-full px-4 py-2 text-sm rounded-lg border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary font-mono"
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="overrideLoading"
            class="w-full py-3 px-4 bg-primary hover:bg-primary-hover text-white text-xs font-bold rounded-lg shadow-md transition-all duration-200 cursor-pointer disabled:opacity-50"
          >
            Apply Record Override
          </button>
        </form>
      </div>

      <!-- Card 4: Dangerous Action - Force Group Deletion -->
      <div class="bg-red-50/40 p-6 sm:p-8 rounded-xl shadow-sm border border-red-200 space-y-6">
        <div class="border-b border-red-200 pb-4">
          <h3 class="text-lg font-bold text-red-700 tracking-tight flex items-center">
            <svg class="w-5 h-5 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Dangerous Action: Delete Group
          </h3>
          <p class="text-xs text-red-600 mt-0.5">Unlinks all student members and permanently deletes project group record</p>
        </div>

        <form @submit.prevent="handleDeleteGroup" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-red-800 uppercase tracking-wider mb-1">Target Group ID</label>
            <input
              v-model.number="deleteGroupId"
              type="number"
              required
              placeholder="e.g. 12"
              class="w-full px-4 py-2.5 text-sm rounded-lg border border-red-300 focus:ring-2 focus:ring-red-500/20 focus:border-red-500 bg-white"
            />
          </div>

          <div class="p-3 bg-red-100/60 rounded-lg text-xs text-red-800 leading-relaxed font-medium">
            Warning: This operation cannot be undone. Member students will be unlinked and set to no group.
          </div>

          <button
            type="submit"
            :disabled="deleteLoading"
            class="w-full py-3 px-4 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-lg shadow-md transition-all duration-200 cursor-pointer disabled:opacity-50"
          >
            Force Delete Group Record
          </button>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()

const successMsg = ref('')
const errorMsg = ref('')

// Staff form
const staffForm = ref({ email: '', password: '', role: 'coordinator' })
const staffLoading = ref(false)

// Force invite form
const inviteForm = ref({ student_id: null, github_username: '' })
const inviteLoading = ref(false)

// Override form
const overrideForm = ref({ student_id: null, name: '', email: '', group_id: null, github_username: '' })
const overrideLoading = ref(false)

// Delete group form
const deleteGroupId = ref(null)
const deleteLoading = ref(false)

const clearMessages = () => {
  successMsg.value = ''
  errorMsg.value = ''
}

const handleProvisionStaff = async () => {
  clearMessages()
  staffLoading.value = true
  try {
    const res = await axios.post('/api/v1/admin/users', staffForm.value, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    successMsg.value = `Staff account (${res.data.email}) created successfully with role '${res.data.role}'.`
    staffForm.value = { email: '', password: '', role: 'coordinator' }
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to provision staff account.'
  } finally {
    staffLoading.value = false
  }
}

const handleForceInvite = async () => {
  clearMessages()
  inviteLoading.value = true
  try {
    const payload = {
      student_id: inviteForm.value.student_id,
      github_username: inviteForm.value.github_username || null,
    }
    const res = await axios.post('/api/v1/admin/github/force-invite', payload, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    successMsg.value = res.data.message
    inviteForm.value = { student_id: null, github_username: '' }
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to dispatch force invitation.'
  } finally {
    inviteLoading.value = false
  }
}

const handleOverrideStudent = async () => {
  clearMessages()
  overrideLoading.value = true
  try {
    const studentId = overrideForm.value.student_id
    const payload = {}
    if (overrideForm.value.name) payload.name = overrideForm.value.name
    if (overrideForm.value.email) payload.email = overrideForm.value.email
    if (overrideForm.value.github_username) payload.github_username = overrideForm.value.github_username
    payload.group_id = overrideForm.value.group_id // can be null or number

    const res = await axios.patch(`/api/v1/admin/students/${studentId}`, payload, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    successMsg.value = `Student record #${res.data.id} updated successfully.`
    overrideForm.value = { student_id: null, name: '', email: '', group_id: null, github_username: '' }
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to override student record.'
  } finally {
    overrideLoading.value = false
  }
}

const handleDeleteGroup = async () => {
  clearMessages()
  if (!confirm(`Are you sure you want to force delete group #${deleteGroupId.value}?`)) return
  deleteLoading.value = true
  try {
    const res = await axios.delete(`/api/v1/admin/groups/${deleteGroupId.value}`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    successMsg.value = res.data.message
    deleteGroupId.value = null
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to delete group.'
  } finally {
    deleteLoading.value = false
  }
}
</script>
