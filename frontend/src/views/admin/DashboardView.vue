<template>
  <div class="admin-dashboard space-y-8 animate-fade-in">
    <!-- Welcome / Header Section -->
    <div class="header-card">
      <div class="flex flex-col md:flex-row justify-between items-center gap-6">
        <div>
          <div class="header-label">
            <span class="pulse-dot"></span>
            Admin Workspace - God Mode
          </div>
          <h2 class="header-title">Full System Control</h2>
          <p class="header-sub">Manage teams, assign students, and monitor activity.</p>
        </div>
        <div>
          <button @click="showCreateTeamModal = true" class="btn-primary">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Create New Team
          </button>
        </div>
      </div>
    </div>

    <!-- GitHub Sync Control Panel -->
    <div class="mb-6 p-6 bg-white rounded-2xl shadow-sm border border-gray-200 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      <div>
        <h3 class="text-lg font-bold text-gray-900">GitHub Bulk Provisioning</h3>
        <p class="text-sm text-gray-500">Automatically generate private repositories and dispatch organization invites to all approved project groups.</p>
      </div>
      
      <button 
        @click="triggerBulkSync" 
        :disabled="isSyncing"
        class="btn-primary flex items-center shrink-0"
      >
        <svg v-if="isSyncing" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span v-if="isSyncing">Syncing to GitHub...</span>
        <span v-else>
          <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Sync All to GitHub
        </span>
      </button>
    </div>

    <!-- Sync Log Results -->
    <div v-if="syncResults?.details?.length > 0" class="mb-6 p-5 bg-gray-50 rounded-xl border border-gray-200 text-sm font-mono text-gray-700 overflow-y-auto max-h-64 shadow-inner">
      <div class="flex justify-between items-center mb-3">
        <p class="font-bold text-gray-900">Sync Execution Log:</p>
        <button @click="syncResults = null" class="text-gray-400 hover:text-gray-600 text-xs font-sans font-bold">Clear</button>
      </div>
      <ul class="space-y-1">
        <li v-for="(detail, index) in syncResults.details" :key="index" 
            :class="{'text-red-600': detail.includes('Failed') || detail.includes('Exception'), 'text-emerald-600': detail.includes('Success')}">
          > {{ detail }}
        </li>
        <li v-if="syncResults.details.length === 0" class="text-gray-500 italic">No operations performed.</li>
      </ul>
    </div>

    <!-- Metrics Row -->
    <div v-if="metrics" class="metrics-grid">
      <div class="metric-card group hover:-translate-y-1 transition-transform duration-300">
        <div class="metric-icon-box bg-blue-100 text-[#124f9f] group-hover:bg-[#124f9f] group-hover:text-white transition-colors duration-300">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <div class="metric-info">
          <p class="metric-label">Total Teams</p>
          <p class="metric-value">{{ metrics.total_groups }}</p>
        </div>
      </div>

      <div class="metric-card group hover:-translate-y-1 transition-transform duration-300">
        <div class="metric-icon-box bg-indigo-100 text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors duration-300">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
        <div class="metric-info">
          <p class="metric-label">Total Students</p>
          <p class="metric-value">{{ metrics.total_students }}</p>
        </div>
      </div>

      <div class="metric-card group hover:-translate-y-1 transition-transform duration-300">
        <div class="metric-icon-box bg-emerald-100 text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition-colors duration-300">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
          </svg>
        </div>
        <div class="metric-info">
          <p class="metric-label">GitHub Sync Status</p>
          <p class="metric-value">
            {{ metrics.active_repositories }} <span class="text-gray-400 text-sm font-medium">/ {{ metrics.approved_groups }} Synced</span>
          </p>
        </div>
      </div>
    </div>
    
    <div v-else-if="loadingMetrics" class="animate-pulse flex space-x-4">
      <div class="h-24 bg-gray-200 rounded-2xl w-1/3"></div>
      <div class="h-24 bg-gray-200 rounded-2xl w-1/3"></div>
      <div class="h-24 bg-gray-200 rounded-2xl w-1/3"></div>
    </div>

    <!-- Data Table -->
    <div class="table-card">
      <div class="table-header">
        <h3 class="table-title">Project Teams Directory</h3>
        <div class="search-box">
          <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input type="text" v-model="searchQuery" placeholder="Search teams..." class="search-input" />
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Group Name</th>
              <th>Team Name</th>
              <th>Status</th>
              <th>Members</th>
              <th class="text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="team in filteredTeams" :key="team.id">
              <tr class="table-row group cursor-pointer" @click="toggleRow(team.id)">
                <td class="font-medium text-gray-900">#{{ team.id }}</td>
                <td class="font-semibold text-[#124f9f]">{{ team.group_name }}</td>
                <td>{{ team.team_name || '—' }}</td>
                <td>
                  <span :class="statusBadgeClass(team.status)">{{ team.status }}</span>
                </td>
                <td>
                  <div class="flex -space-x-2 overflow-hidden">
                    <div v-for="(p, i) in team.partners.slice(0, 3)" :key="i" class="inline-block h-8 w-8 rounded-full ring-2 ring-white bg-gradient-to-br from-[#124f9f] to-blue-400 flex items-center justify-center text-white text-xs font-bold" :title="p.name || p.email">
                      {{ (p.name || p.email).charAt(0).toUpperCase() }}
                    </div>
                    <div v-if="team.partners.length > 3" class="inline-block h-8 w-8 rounded-full ring-2 ring-white bg-gray-200 flex items-center justify-center text-gray-600 text-xs font-bold">
                      +{{ team.partners.length - 3 }}
                    </div>
                  </div>
                </td>
                <td class="text-right">
                  <button class="expand-btn">
                    {{ expandedRows.includes(team.id) ? 'Hide' : 'Manage' }}
                    <svg :class="{'rotate-180': expandedRows.includes(team.id)}" class="w-4 h-4 ml-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                </td>
              </tr>
              
              <!-- Expanded Row Details (God Mode Controls) -->
              <tr v-if="expandedRows.includes(team.id)" class="expanded-row-bg">
                <td colspan="6" class="p-0">
                  <div class="expanded-content">
                    <div class="flex justify-between items-center mb-6 border-b border-gray-200 pb-4">
                      <h4 class="text-lg font-bold text-[#124f9f]">Team God Mode</h4>
                      <div class="flex space-x-3">
                        <button @click="openLogsModal(team.id)" class="btn-outline">
                          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                          View Logs
                        </button>
                        <button @click="openAddStudentModal(team.id)" class="btn-primary-sm">
                          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                          </svg>
                          Add Student
                        </button>
                      </div>
                    </div>
                    
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      <!-- Repo Details -->
                      <div class="detail-card">
                        <h4 class="detail-title">Repository Information</h4>
                        <div class="detail-grid">
                          <div>
                            <p class="detail-label">Repository Name</p>
                            <p class="detail-value font-mono text-[#124f9f]">{{ team.repo_name || 'Pending Creation' }}</p>
                          </div>
                          <div>
                            <p class="detail-label">GitHub URL</p>
                            <a v-if="team.github_repo_url" :href="team.github_repo_url" target="_blank" class="text-[#124f9f] hover:underline text-sm font-medium">Open in GitHub ↗</a>
                            <p v-else class="text-gray-400 text-sm">Not Available</p>
                          </div>
                        </div>
                      </div>

                      <!-- Student List with Action -->
                      <div class="detail-card lg:row-span-2">
                        <h4 class="detail-title">Team Members ({{ team.partners.length }})</h4>
                        <div class="space-y-4 mt-4">
                          <div v-for="partner in team.partners" :key="partner.id" class="student-card">
                            <div class="flex justify-between items-center">
                              <div>
                                <p class="font-bold text-gray-900">{{ partner.name || 'Unknown' }}</p>
                                <p class="text-xs text-gray-500">{{ partner.email }}</p>
                                <p class="text-xs text-gray-500 mt-1">
                                  GitHub: <span class="font-mono text-[#124f9f]">{{ partner.github_username || 'Not linked' }}</span>
                                </p>
                              </div>
                              <div class="text-right flex flex-col items-end space-y-2">
                                <span :class="inviteBadgeClass(partner.invite_status)">
                                  {{ partner.invite_status || 'Pending' }}
                                </span>
                                <button @click="forceInvite(partner.id, partner.github_username)" class="text-xs font-semibold text-blue-600 hover:text-blue-800 transition-colors border border-blue-200 hover:bg-blue-50 px-2 py-1 rounded">
                                  Force Invite
                                </button>
                              </div>
                            </div>
                          </div>
                          <div v-if="team.partners.length === 0" class="text-sm text-gray-400 py-4 text-center">
                            No students assigned yet. Use 'Add Student' above.
                          </div>
                        </div>
                      </div>
                      
                    </div>
                  </div>
                </td>
              </tr>
            </template>
            <tr v-if="filteredTeams.length === 0 && !loadingTeams">
              <td colspan="6" class="text-center py-12 text-gray-400">No teams found.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="loadingTeams" class="py-12 flex justify-center">
        <svg class="animate-spin h-8 w-8 text-[#124f9f]" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
      </div>
    </div>

    <!-- Modals -->

    <!-- Create Team Modal -->
    <div v-if="showCreateTeamModal" class="modal-overlay" @click.self="showCreateTeamModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="text-lg font-bold text-gray-900">Create New Team</h3>
          <button @click="showCreateTeamModal = false" class="text-gray-400 hover:text-gray-600">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-field">
            <label class="field-label">Group Name</label>
            <input v-model="newTeamForm.group_name" type="text" placeholder="e.g. AI Vision Team" class="field-input" />
          </div>
          <div class="form-field mt-4">
            <label class="field-label">Team Name <span class="font-normal text-gray-400">(GitHub repo ref)</span></label>
            <input v-model="newTeamForm.team_name" type="text" placeholder="e.g. ai-vision-team" class="field-input" />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCreateTeamModal = false" class="btn-outline mr-3">Cancel</button>
          <button @click="createTeam" :disabled="creatingTeam" class="btn-primary">
            {{ creatingTeam ? 'Creating...' : 'Create Team' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Add Student Modal -->
    <div v-if="showAddStudentModal" class="modal-overlay" @click.self="showAddStudentModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="text-lg font-bold text-gray-900">Assign Student to Team #{{ targetTeamId }}</h3>
          <button @click="showAddStudentModal = false" class="text-gray-400 hover:text-gray-600">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-field">
            <label class="field-label">Student ID</label>
            <input v-model="addStudentId" type="number" placeholder="Enter student ID" class="field-input" />
            <p class="text-xs text-gray-500 mt-1">This student will be removed from any current team and placed into Team #{{ targetTeamId }}.</p>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAddStudentModal = false" class="btn-outline mr-3">Cancel</button>
          <button @click="assignStudent" :disabled="assigningStudent" class="btn-primary">
            {{ assigningStudent ? 'Assigning...' : 'Assign Student' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Logs Modal -->
    <div v-if="showLogsModal" class="modal-overlay" @click.self="showLogsModal = false">
      <div class="modal-content !max-w-2xl">
        <div class="modal-header">
          <h3 class="text-lg font-bold text-gray-900">Push Event Logs</h3>
          <button @click="showLogsModal = false" class="text-gray-400 hover:text-gray-600">&times;</button>
        </div>
        <div class="modal-body max-h-[60vh] overflow-y-auto">
          <div v-if="loadingLogs" class="py-12 flex justify-center">
            <svg class="animate-spin h-8 w-8 text-[#124f9f]" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
            </svg>
          </div>
          <div v-else-if="logs.length === 0" class="text-center py-8 text-gray-500">
            No push events recorded for this team.
          </div>
          <div v-else class="space-y-4">
            <div v-for="log in logs" :key="log.id" class="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <div class="flex justify-between items-start">
                <div>
                  <p class="text-sm font-bold text-gray-900">Commit: <span class="font-mono text-[#124f9f]">{{ log.commit_hash }}</span></p>
                  <p class="text-xs text-gray-500 mt-1">Timestamp: {{ log.timestamp }}</p>
                </div>
                <div>
                  <span :class="statusBadgeClass(log.approval_status)">{{ log.approval_status }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showLogsModal = false" class="btn-outline">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'

// Data
const metrics = ref(null)
const teams = ref([])
const loadingMetrics = ref(true)
const loadingTeams = ref(true)
const searchQuery = ref('')
const expandedRows = ref([])

// Modals State
const showCreateTeamModal = ref(false)
const newTeamForm = ref({ group_name: '', team_name: '' })
const creatingTeam = ref(false)

const showAddStudentModal = ref(false)
const targetTeamId = ref(null)
const addStudentId = ref('')
const assigningStudent = ref(false)

const showLogsModal = ref(false)
const logs = ref([])
const loadingLogs = ref(false)

// Bulk Sync State
const isSyncing = ref(false)
const syncResults = ref(null)

const triggerBulkSync = async () => {
  if (!confirm("Are you sure you want to provision GitHub repositories for all approved teams? This may take several minutes.")) {
    return
  }

  isSyncing.value = true
  syncResults.value = null

  try {
    const response = await api.post('/admin/github/bulk-sync')
    syncResults.value = response.data
    
    // Check if it was an early exit message, otherwise show the full stats
    if (response.data.message) {
        alert(response.data.message)
    } else {
        alert(`GitHub Sync Complete!\nSuccessfully provisioned: ${response.data.successful}\nFailed: ${response.data.failed}`)
    }
    
    // Refresh dashboard metrics
    await fetchDashboardData()
  } catch (error) {
    console.error("Bulk sync failed:", error)
    alert(error.response?.data?.detail || "An error occurred while communicating with the server during the bulk sync.")
  } finally {
    isSyncing.value = false
  }
}

const fetchDashboardData = async () => {
  try {
    const res = await api.get('/admin/dashboard')
    metrics.value = res.data.metrics
    teams.value = res.data.teams
  } catch (error) {
    console.error("Failed to load dashboard data", error)
  } finally {
    loadingMetrics.value = false
    loadingTeams.value = false
  }
}

const filteredTeams = computed(() => {
  if (!searchQuery.value) return teams.value
  const query = searchQuery.value.toLowerCase()
  return teams.value.filter(t => 
    t.group_name?.toLowerCase().includes(query) || 
    t.team_name?.toLowerCase().includes(query) ||
    t.id.toString() === query
  )
})

const toggleRow = (id) => {
  if (expandedRows.value.includes(id)) {
    expandedRows.value = expandedRows.value.filter(rowId => rowId !== id)
  } else {
    expandedRows.value.push(id)
  }
}

// Action: Create Team
const createTeam = async () => {
  if (!newTeamForm.value.group_name) return alert('Group name is required.')
  creatingTeam.value = true
  try {
    await api.post('/admin/groups', {
      group_name: newTeamForm.value.group_name,
      team_name: newTeamForm.value.team_name || undefined
    })
    showCreateTeamModal.value = false
    newTeamForm.value = { group_name: '', team_name: '' }
    await fetchDashboardData()
  } catch (error) {
    alert(error.response?.data?.detail || 'Failed to create team')
  } finally {
    creatingTeam.value = false
  }
}

// Action: Add Student
const openAddStudentModal = (teamId) => {
  targetTeamId.value = teamId
  addStudentId.value = ''
  showAddStudentModal.value = true
}

const assignStudent = async () => {
  if (!addStudentId.value) return alert('Student ID is required.')
  assigningStudent.value = true
  try {
    await api.patch(`/admin/students/${addStudentId.value}`, {
      group_id: targetTeamId.value
    })
    showAddStudentModal.value = false
    await fetchDashboardData()
  } catch (error) {
    alert(error.response?.data?.detail || 'Failed to assign student')
  } finally {
    assigningStudent.value = false
  }
}

// Action: Force Invite
const forceInvite = async (studentId, githubUsername) => {
  if (!githubUsername) {
    const customUsername = prompt('Student has no GitHub username linked. Enter GitHub username to send invite to:')
    if (!customUsername) return
    githubUsername = customUsername
  }
  
  if (!confirm(`Force send GitHub organization invite to ${githubUsername}?`)) return
  
  try {
    await api.post('/admin/github/force-invite', {
      student_id: studentId,
      github_username: githubUsername
    })
    alert('Invite dispatched successfully.')
    await fetchDashboardData()
  } catch (error) {
    alert(error.response?.data?.detail || 'Failed to dispatch invite')
  }
}

// Action: View Logs
const openLogsModal = async (teamId) => {
  showLogsModal.value = true
  loadingLogs.value = true
  logs.value = []
  try {
    const res = await api.get(`/admin/groups/${teamId}/logs`)
    logs.value = res.data
  } catch (error) {
    console.error("Failed to load logs", error)
  } finally {
    loadingLogs.value = false
  }
}

const statusBadgeClass = (statusVal) => {
  const base = 'px-2.5 py-1 text-xs font-bold rounded-md uppercase tracking-wider border inline-block'
  if (statusVal === 'approved') return `${base} bg-emerald-50 text-emerald-700 border-emerald-200`
  if (statusVal === 'rejected') return `${base} bg-red-50 text-red-700 border-red-200`
  if (statusVal === 'pending') return `${base} bg-amber-50 text-amber-700 border-amber-200`
  return `${base} bg-slate-50 text-slate-700 border-slate-200`
}

const inviteBadgeClass = (inviteVal) => {
  const base = 'px-2 py-0.5 text-[0.65rem] font-bold rounded-full uppercase tracking-wider border inline-block'
  if (['sent', 'active'].includes(inviteVal)) return `${base} bg-emerald-100 text-emerald-700 border-emerald-200`
  if (inviteVal === 'pending') return `${base} bg-amber-100 text-amber-700 border-amber-200`
  return `${base} bg-slate-100 text-slate-500 border-slate-200`
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
/* Typography & Common */
.admin-dashboard {
  font-family: 'Inter', system-ui, sans-serif;
}

/* Header */
.header-card {
  @apply bg-white border border-gray-200 rounded-2xl p-6 md:p-8 shadow-sm relative overflow-hidden;
  background: linear-gradient(120deg, #ffffff 0%, #fffbf8 100%);
}
.header-card::after {
  content: '';
  position: absolute;
  top: 0; right: 0; bottom: 0;
  width: 30%;
  background: radial-gradient(circle at top right, rgba(159, 18, 18, 0.03), transparent 70%);
  pointer-events: none;
}
.header-label {
  @apply inline-flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-red-600 mb-2;
}
.pulse-dot {
  @apply w-2 h-2 rounded-full bg-red-600;
  animation: pulse 2s infinite;
}
.header-title {
  @apply text-2xl md:text-3xl font-extrabold text-gray-900 tracking-tight;
}
.header-sub {
  @apply text-sm md:text-base text-gray-500 mt-2;
}

/* Metrics Grid */
.metrics-grid {
  @apply grid grid-cols-1 md:grid-cols-3 gap-6;
}
.metric-card {
  @apply bg-white border border-gray-100 rounded-2xl p-6 flex items-center gap-5 shadow-sm hover:shadow-md transition-all duration-300 relative overflow-hidden;
}
.metric-icon-box {
  @apply w-12 h-12 rounded-xl flex items-center justify-center shrink-0;
}
.metric-info {
  @apply flex flex-col;
}
.metric-label {
  @apply text-xs font-bold text-gray-400 uppercase tracking-wider mb-1;
}
.metric-value {
  @apply text-2xl font-black text-gray-900;
}

/* Table Card */
.table-card {
  @apply bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden;
}
.table-header {
  @apply p-6 border-b border-gray-100 flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gray-50/50;
}
.table-title {
  @apply text-lg font-bold text-gray-900;
}
.search-box {
  @apply relative w-full md:w-72;
}
.search-icon {
  @apply absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400;
}
.search-input {
  @apply w-full pl-9 pr-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#124f9f] focus:border-transparent transition-shadow;
}
.data-table {
  @apply w-full text-left border-collapse;
}
.data-table th {
  @apply px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider border-b border-gray-200 bg-gray-50;
}
.data-table td {
  @apply px-6 py-4 text-sm border-b border-gray-100;
}
.table-row {
  @apply transition-colors hover:bg-slate-50;
}
.expand-btn {
  @apply inline-flex items-center justify-end w-full text-sm font-semibold text-gray-600 hover:text-gray-900 transition-colors focus:outline-none;
}

/* Expanded Content */
.expanded-row-bg {
  @apply bg-slate-50/80 border-b border-gray-300 shadow-inner;
}
.expanded-content {
  @apply p-6 border-l-4 border-red-500;
  animation: slideDown 0.3s ease-out;
}
.detail-card {
  @apply bg-white border border-gray-200 rounded-xl p-5 shadow-sm;
}
.detail-title {
  @apply text-sm font-bold text-gray-400 uppercase tracking-wider mb-4 border-b border-gray-100 pb-2;
}
.detail-grid {
  @apply grid grid-cols-2 gap-4;
}
.detail-label {
  @apply text-xs font-semibold text-gray-500 mb-1;
}
.detail-value {
  @apply text-sm font-medium text-gray-900;
}

.student-card {
  @apply bg-gray-50 border border-gray-100 rounded-lg p-4 hover:border-gray-200 hover:shadow-sm transition-all;
}

/* Modals */
.modal-overlay {
  @apply fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4;
  animation: fadeIn 0.2s ease-out;
}
.modal-content {
  @apply bg-white rounded-2xl w-full max-w-md overflow-hidden shadow-2xl;
  animation: slideUp 0.3s ease-out;
}
.modal-header {
  @apply px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50;
}
.modal-body {
  @apply p-6;
}
.modal-footer {
  @apply px-6 py-4 border-t border-gray-100 flex justify-end bg-gray-50/50;
}
.form-field {
  @apply flex flex-col;
}
.field-label {
  @apply text-sm font-bold text-gray-700 mb-1;
}
.field-input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#124f9f] focus:border-transparent;
}

/* Buttons */
.btn-primary {
  @apply inline-flex items-center justify-center bg-[#124f9f] text-white font-bold text-sm px-5 py-2.5 rounded-xl hover:bg-blue-800 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#124f9f] disabled:opacity-50;
}
.btn-primary-sm {
  @apply inline-flex items-center justify-center bg-[#124f9f] text-white font-semibold text-xs px-3 py-1.5 rounded-lg hover:bg-blue-800 transition-colors shadow-sm focus:outline-none disabled:opacity-50;
}
.btn-outline {
  @apply inline-flex items-center justify-center border border-gray-300 bg-white text-gray-700 font-semibold text-xs md:text-sm px-4 py-2 rounded-xl hover:bg-gray-50 transition-colors shadow-sm focus:outline-none disabled:opacity-50;
}

/* Animations */
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.2); }
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(10px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
