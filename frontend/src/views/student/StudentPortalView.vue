<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Student Onboarding</h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        
        <!-- State 1: Group Selection -->
        <div v-if="currentState === 1">
          <label class="block text-sm font-medium text-gray-700 mb-2">Select your Project Group</label>
          <div class="relative">
            <select v-model="selectedGroupId" class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md shadow-sm border" :disabled="isSubmitting">
              <option disabled value="">Choose a group...</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">
                {{ group.group_no }} - {{ group.group_name }}
              </option>
            </select>
          </div>
          <button @click="proceedToMembers" :disabled="!selectedGroupId || isSubmitting" class="mt-4 w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
            Next
          </button>
        </div>

        <!-- State 2: Member Selection -->
        <div v-if="currentState === 2">
          <button @click="currentState = 1" class="text-sm text-blue-600 mb-4 hover:underline">&larr; Back to Groups</button>
          <label class="block text-sm font-medium text-gray-700 mb-2">Select your email address</label>
          <div class="space-y-2 mt-4">
            <button v-for="member in members" :key="member.id" @click="requestOtp(member)" :disabled="isSubmitting" class="w-full text-left px-4 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50">
              {{ member.name || 'Unknown' }} ({{ member.email }})
            </button>
          </div>
        </div>

        <!-- State 3: OTP Verification -->
        <div v-if="currentState === 3">
          <button @click="currentState = 2" class="text-sm text-blue-600 mb-4 hover:underline">&larr; Back to Members</button>
          <p class="text-sm text-gray-600 mb-4">An OTP has been sent to <strong>{{ selectedMember?.email }}</strong>.</p>
          
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Enter 6-digit OTP</label>
            <input v-model="otpCode" type="text" maxlength="6" class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" :disabled="isSubmitting" />
          </div>
          
          <button @click="verifyOtp" :disabled="otpCode.length !== 6 || isSubmitting" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50">
            {{ isSubmitting ? 'Verifying...' : 'Verify OTP' }}
          </button>
          
          <div class="mt-4 text-center border-t pt-4">
            <button @click="openChangeEmailModal" class="text-sm font-medium text-gray-600 hover:text-gray-900 border border-gray-300 rounded px-4 py-2 bg-gray-50 hover:bg-gray-100 transition-colors">
              Change Email
            </button>
          </div>
        </div>

        <!-- State 4: Group Dashboard -->
        <div v-if="currentState === 4 && dashboardData">
          <div class="bg-gray-50 p-4 rounded-md border border-gray-200 mb-6">
            <h3 class="text-lg font-medium text-gray-900">{{ dashboardData.group.group_name }}</h3>
            <dl class="mt-2 divide-y divide-gray-200 text-sm">
              <div class="py-2 flex justify-between">
                <dt class="text-gray-500">Group ID</dt>
                <dd class="font-medium text-gray-900">{{ dashboardData.group.group_no || dashboardData.group.id }}</dd>
              </div>
              <div class="py-2 flex justify-between">
                <dt class="text-gray-500">GitHub Repo</dt>
                <dd class="font-medium text-blue-600">
                  <a v-if="dashboardData.group.github_repo_url" :href="dashboardData.group.github_repo_url" target="_blank" rel="noopener noreferrer">View Repository</a>
                  <span v-else class="text-gray-500 italic">Not set up yet</span>
                </dd>
              </div>
            </dl>
          </div>

          <button @click="showInviteModal = true" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gray-900 hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900">
            Send Invite to Yourself
          </button>
        </div>

      </div>
    </div>

    <!-- Modals -->
    
    <!-- Change Email Modal -->
    <div v-if="showChangeEmailModal" class="fixed inset-0 z-10 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showChangeEmailModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">Request Email Change</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">New Email Address</label>
                <input v-model="changeEmailData.new_email" type="email" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Name</label>
                <input v-model="changeEmailData.name" type="text" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Reg ID</label>
                <input v-model="changeEmailData.reg_id" type="text" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Group Name</label>
                <input v-model="changeEmailData.group_name" type="text" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-6 sm:flex sm:flex-row-reverse">
            <button @click="submitEmailChange" :disabled="!changeEmailData.new_email || isSubmitting" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50">
              Submit Request
            </button>
            <button @click="showChangeEmailModal = false" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:w-auto sm:text-sm">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- GitHub Invite Modal -->
    <div v-if="showInviteModal" class="fixed inset-0 z-10 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showInviteModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">Important Notice</h3>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  You must first create a GitHub account using exactly: <strong>{{ selectedMember?.email }}</strong>.
                </p>
                
                <div class="mt-4">
                  <label class="block text-sm font-medium text-gray-700">Enter your GitHub Username</label>
                  <input v-model="githubUsername" type="text" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                </div>

                <div class="mt-4 flex items-start">
                  <div class="flex items-center h-5">
                    <input id="confirm-github" v-model="confirmGithub" type="checkbox" class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded" />
                  </div>
                  <div class="ml-3 text-sm">
                    <label for="confirm-github" class="font-medium text-gray-700">I confirm my GitHub account is created with this email.</label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
            <button @click="dispatchInvite" :disabled="!confirmGithub || !githubUsername || isSubmitting" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50">
              Dispatch Invite
            </button>
            <button @click="showInviteModal = false" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:w-auto sm:text-sm">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const currentState = ref(1);
const isSubmitting = ref(false);

const groups = ref([]);
const selectedGroupId = ref('');

const members = ref([]);
const selectedMember = ref(null);

const otpCode = ref('');

const dashboardData = ref(null);

const showChangeEmailModal = ref(false);
const changeEmailData = ref({
  new_email: '',
  name: '',
  reg_id: '',
  group_name: ''
});

const showInviteModal = ref(false);
const confirmGithub = ref(false);
const githubUsername = ref('');

onMounted(async () => {
  try {
    const res = await fetch('/api/v1/student/groups');
    if (res.ok) {
      groups.value = await res.json();
    }
  } catch (error) {
    console.error('Failed to load groups', error);
  }
});

const proceedToMembers = async () => {
  if (!selectedGroupId.value) return;
  isSubmitting.value = true;
  try {
    const res = await fetch(`/api/v1/student/groups/${selectedGroupId.value}/members`);
    if (res.ok) {
      members.value = await res.json();
      currentState.value = 2;
    } else {
      alert('Failed to load members');
    }
  } catch (error) {
    console.error(error);
  } finally {
    isSubmitting.value = false;
  }
};

const requestOtp = async (member) => {
  selectedMember.value = member;
  isSubmitting.value = true;
  try {
    const res = await fetch('/api/v1/student/request-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: member.email })
    });
    if (res.ok) {
      currentState.value = 3;
    } else {
      const data = await res.json();
      alert(`Error: ${data.detail || 'Failed to send OTP'}`);
    }
  } catch (error) {
    console.error(error);
  } finally {
    isSubmitting.value = false;
  }
};

const verifyOtp = async () => {
  isSubmitting.value = true;
  try {
    const res = await fetch('/api/v1/student/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: selectedMember.value.email, otp: otpCode.value })
    });
    const data = await res.json();
    if (res.ok) {
      dashboardData.value = data;
      currentState.value = 4;
    } else {
      alert(`Error: ${data.detail || 'Invalid OTP'}`);
    }
  } catch (error) {
    console.error(error);
  } finally {
    isSubmitting.value = false;
  }
};

const openChangeEmailModal = () => {
  const selectedGroup = groups.value.find(g => g.id === selectedGroupId.value);
  changeEmailData.value = {
    new_email: '',
    name: selectedMember.value.name || '',
    reg_id: selectedMember.value.reg_id || '',
    group_name: selectedGroup?.group_name || selectedGroup?.group_no || ''
  };
  showChangeEmailModal.value = true;
};

const submitEmailChange = async () => {
  isSubmitting.value = true;
  try {
    const res = await fetch('/api/v1/student/change-email-request', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        old_email: selectedMember.value.email,
        new_email: changeEmailData.value.new_email,
        student_name: changeEmailData.value.name,
        student_id: selectedMember.value.id,
        group_id: selectedGroupId.value,
        group_name: changeEmailData.value.group_name
      })
    });
    if (res.ok) {
      alert('Support request sent successfully');
      showChangeEmailModal.value = false;
    } else {
      alert('Failed to send request');
    }
  } catch (error) {
    console.error(error);
  } finally {
    isSubmitting.value = false;
  }
};

const dispatchInvite = async () => {
  isSubmitting.value = true;
  try {
    const res = await fetch('/api/v1/student/github-invite', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: selectedMember.value.email,
        github_username: githubUsername.value
      })
    });
    if (res.ok) {
      alert('Invite dispatched successfully');
      showInviteModal.value = false;
    } else {
      const data = await res.json();
      alert(`Error: ${data.detail || 'Failed to dispatch invite'}`);
    }
  } catch (error) {
    console.error(error);
  } finally {
    isSubmitting.value = false;
  }
};
</script>
