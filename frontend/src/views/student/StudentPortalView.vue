<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8 flex items-center justify-center">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg border border-gray-100">
      <div class="text-center border-b pb-4">
        <h2 class="text-3xl font-extrabold text-gray-900">Student Portal</h2>
        <p class="mt-2 text-sm text-gray-600">SZABIST FYP Authentication</p>
      </div>

      <!-- STATE 1: Select Group -->
      <div v-if="currentState === 1" class="space-y-4">
        <label class="block text-sm font-medium text-gray-700">Select Your Project Group</label>
        <div class="relative">
          <input 
            v-model="searchQuery" 
            @focus="showDropdown = true" 
            type="text" 
            placeholder="Search by Group ID (e.g., P605) or Name..." 
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-gray-50"
          />
          <ul v-if="showDropdown && filteredGroups.length" class="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg max-h-60 overflow-auto">
            <li 
              v-for="g in filteredGroups" 
              :key="g.id" 
              @click="selectGroup(g)" 
              class="px-4 py-3 hover:bg-blue-50 cursor-pointer text-sm text-gray-800 border-b border-gray-50 last:border-0"
            >
              <span class="font-bold">{{ g.group_no || `ID: ${g.id}` }}</span> - {{ g.group_name }}
            </li>
          </ul>
        </div>
      </div>

      <!-- STATE 2: Select Email -->
      <div v-if="currentState === 2" class="space-y-4">
        <button @click="currentState = 1" class="text-sm text-blue-600 hover:text-blue-800 font-medium">&larr; Change Group</button>
        <label class="block text-sm font-medium text-gray-700">Select Your Email Address</label>
        <div class="space-y-2 mt-2">
          <button v-for="m in members" :key="m.id" @click="requestOtp(m)" class="w-full text-left px-4 py-3 border border-gray-200 rounded-md hover:border-blue-500 hover:bg-blue-50 transition font-medium text-gray-800">
            {{ m.email }}
          </button>
        </div>
        <p v-if="members.length === 0" class="text-red-500 text-sm mt-2">No students assigned to this group yet.</p>
      </div>

      <!-- STATE 3: Verify OTP -->
      <div v-if="currentState === 3" class="space-y-5">
        <button @click="currentState = 2" class="text-sm text-blue-600 hover:text-blue-800 font-medium">&larr; Change Email</button>
        <div class="bg-green-50 p-4 rounded-md border border-green-100">
          <p class="text-sm text-green-800">OTP Sent! Check the terminal/email for <strong>{{ selectedMember.email }}</strong></p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Enter 6-Digit OTP</label>
          <input v-model="otpInput" type="text" maxlength="6" class="mt-1 block w-full px-3 py-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-lg text-center tracking-widest font-mono" placeholder="------">
        </div>
        <button @click="verifyOtp" :disabled="isLoading || otpInput.length !== 6" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition">
          {{ isLoading ? 'Verifying...' : 'Verify Identity' }}
        </button>
        <div class="text-center pt-2">
          <button @click="showEmailModal = true" class="text-sm text-gray-500 hover:text-gray-900 underline decoration-gray-300">Change Email / I lost access</button>
        </div>
      </div>

      <!-- STATE 4: Final Dashboard -->
      <div v-if="currentState === 4" class="space-y-6">
        <div class="bg-blue-50 rounded-lg p-4 border border-blue-100">
          <h3 class="text-lg font-bold text-blue-900">Welcome, {{ selectedMember.name || 'Student' }}</h3>
          <p class="text-sm text-blue-700 mt-1">Your identity is verified.</p>
        </div>
        <dl class="grid grid-cols-1 gap-x-4 gap-y-4 sm:grid-cols-2 bg-gray-50 p-4 rounded-lg border border-gray-200">
          <div class="sm:col-span-1">
            <dt class="text-xs font-bold text-gray-500 uppercase">Group ID</dt>
            <dd class="mt-1 text-sm text-gray-900 font-medium">{{ groupDetails.group_no }}</dd>
          </div>
          <div class="sm:col-span-2">
            <dt class="text-xs font-bold text-gray-500 uppercase">Project Name</dt>
            <dd class="mt-1 text-sm text-gray-900 font-medium">{{ groupDetails.group_name }}</dd>
          </div>
          <div class="sm:col-span-2">
            <dt class="text-xs font-bold text-gray-500 uppercase">GitHub Repository</dt>
            <dd class="mt-1 text-sm font-medium break-words">
              <a v-if="groupDetails.github_repo_url" :href="groupDetails.github_repo_url" target="_blank" class="text-blue-600 hover:underline">{{ groupDetails.github_repo_url }}</a>
              <span v-else class="text-red-500">Repository Pending Creation</span>
            </dd>
          </div>
        </dl>
        <button @click="showGithubModal = true" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-bold text-white bg-gray-900 hover:bg-gray-800 transition">
          <i class="fab fa-github mr-2 mt-0.5"></i> Send GitHub Invite to Yourself
        </button>
      </div>
    </div>

    <!-- MODAL: GitHub Verification -->
    <div v-if="showGithubModal" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-2xl max-w-md w-full p-6 space-y-5">
        <div class="border-b pb-3">
          <h3 class="text-xl font-extrabold text-gray-900">GitHub Verification Required</h3>
        </div>
        <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4">
          <p class="text-sm text-yellow-800">You must have a registered GitHub account using EXACTLY this email address:</p>
          <p class="text-base font-bold text-black mt-1">{{ selectedMember.email }}</p>
        </div>
        <div>
          <label class="block text-sm font-bold text-gray-700">Enter your exact GitHub Username</label>
          <input v-model="githubUsername" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm" placeholder="e.g., octocat">
        </div>
        <div class="flex items-start mt-4 bg-gray-50 p-3 rounded border border-gray-200">
          <div class="flex items-center h-5">
            <input v-model="githubConfirmed" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer">
          </div>
          <div class="ml-3 text-sm">
            <label class="font-medium text-gray-700 cursor-pointer" @click="githubConfirmed = !githubConfirmed">I confirm my GitHub account is already created and linked to the email above.</label>
          </div>
        </div>
        <div class="flex justify-end space-x-3 pt-2">
          <button @click="showGithubModal = false" class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">Cancel</button>
          <button @click="dispatchInvite" :disabled="!githubConfirmed || !githubUsername || isLoading" class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-bold disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-700 transition">
            {{ isLoading ? 'Sending...' : 'Dispatch Invite' }}
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: Change Email Request -->
    <div v-if="showEmailModal" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-2xl max-w-md w-full p-6 space-y-4">
        <h3 class="text-xl font-bold text-gray-900 border-b pb-2">Request Email Change</h3>
        <p class="text-sm text-gray-600">This form sends a direct request to Admin (qambar.ali@szabist.pk).</p>
        <div>
          <label class="block text-sm font-medium text-gray-700">Your Current Bound Email</label>
          <input :value="selectedMember?.email || 'N/A'" disabled type="text" class="mt-1 block w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-md text-gray-500 sm:text-sm">
        </div>
        <div>
          <label class="block text-sm font-bold text-gray-700">New Desired Email</label>
          <input v-model="newEmail" type="email" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm" placeholder="new.email@example.com">
        </div>
        <div class="flex justify-end space-x-3 mt-4 pt-2">
          <button @click="showEmailModal = false" class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium bg-white hover:bg-gray-50">Cancel</button>
          <button @click="requestEmailChange" :disabled="!newEmail || isLoading" class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-bold disabled:opacity-50">
            {{ isLoading ? 'Submitting...' : 'Submit Request' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api' 

const currentState = ref(1)
const isLoading = ref(false)

// State Data
const groups = ref([])
const members = ref([])
const selectedGroup = ref(null)
const selectedMember = ref(null)
const otpInput = ref('')
const groupDetails = ref(null)

const searchQuery = ref('')
const showDropdown = ref(false)

const filteredGroups = computed(() => {
  if (!searchQuery.value) return groups.value;
  const lower = searchQuery.value.toLowerCase();
  return groups.value.filter(g => 
    (g.group_no && g.group_no.toLowerCase().includes(lower)) || 
    (g.group_name && g.group_name.toLowerCase().includes(lower))
  );
});

const selectGroup = (g) => {
  selectedGroup.value = g;
  searchQuery.value = `${g.group_no || 'ID: ' + g.id} - ${g.group_name}`;
  showDropdown.value = false;
  fetchMembers();
};

// Modal Data
const showGithubModal = ref(false)
const githubConfirmed = ref(false)
const githubUsername = ref('')
const showEmailModal = ref(false)
const newEmail = ref('')

onMounted(async () => {
  try {
    const res = await api.get('/students/groups')
    groups.value = res.data
  } catch (err) {
    console.error("API Error: Make sure backend is running.", err)
  }
})

const fetchMembers = async () => {
  if (!selectedGroup.value) return
  isLoading.value = true
  try {
    const res = await api.get(`/students/groups/${selectedGroup.value.id}/members`)
    members.value = res.data
    currentState.value = 2
  } catch (err) {
    alert("Failed to fetch group members.")
  } finally {
    isLoading.value = false
  }
}

const requestOtp = async (member) => {
  selectedMember.value = member
  isLoading.value = true
  try {
    await api.post('/students/request-otp', { email: member.email })
    currentState.value = 3
  } catch (err) {
    alert("Error triggering OTP.")
  } finally {
    isLoading.value = false
  }
}

const verifyOtp = async () => {
  isLoading.value = true
  try {
    const res = await api.post('/students/verify-otp', {
      email: selectedMember.value.email,
      otp: otpInput.value
    })
    groupDetails.value = res.data.group
    currentState.value = 4
  } catch (err) {
    alert(err.response?.data?.detail || "Invalid OTP code.")
  } finally {
    isLoading.value = false
  }
}

const dispatchInvite = async () => {
  isLoading.value = true
  try {
    await api.post('/students/github-invite', {
      email: selectedMember.value.email,
      github_username: githubUsername.value
    })
    alert("Success! The GitHub Invite has been sent to your email.")
    showGithubModal.value = false
  } catch (err) {
    alert(err.response?.data?.detail || "Failed to dispatch invite.")
  } finally {
    isLoading.value = false
  }
}

const requestEmailChange = async () => {
  isLoading.value = true
  try {
    await api.post('/students/change-email-request', {
      old_email: selectedMember.value?.email || 'Unknown',
      new_email: newEmail.value,
      student_name: selectedMember.value?.name || 'Unknown',
      student_id: selectedMember.value?.id || 0,
      group_id: selectedGroup.value?.id || 0,
      group_name: selectedGroup.value?.group_name || 'Unknown'
    })
    alert("Your email change request has been securely dispatched to the Administrator.")
    showEmailModal.value = false
    newEmail.value = ''
  } catch (err) {
    alert("Failed to send request.")
  } finally {
    isLoading.value = false
  }
}
</script>