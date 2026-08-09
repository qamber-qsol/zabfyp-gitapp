<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <div class="bg-blue-900 text-white py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl">SZABIST FYP Git Help Portal</h1>
        <p class="mt-4 text-xl max-w-2xl mx-auto text-blue-100">Your central hub for GitHub organization onboarding, repository management, and technical support.</p>
      </div>
    </div>

    <!-- Notification Banner -->
    <div v-if="notification.show" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
      <div :class="notification.type === 'error' ? 'bg-red-50 text-red-800 border-red-200' : 'bg-green-50 text-green-800 border-green-200'" class="p-4 border rounded-md text-sm font-bold shadow-sm">
        {{ notification.message }}
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Top Row: Access & Support -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <!-- SECTION 1: Re-Invite & Account Setup -->
        <div class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden flex flex-col hover:shadow-lg transition">
          <div class="bg-blue-600 p-4 border-b border-blue-700">
            <h2 class="text-xl font-bold text-white flex items-center"><i class="fab fa-github mr-2"></i> GitHub Access Portal</h2>
          </div>
          <div class="p-6 flex-grow flex flex-col justify-between">
            <div>
              <p class="text-gray-600 mb-4 font-medium">Haven't received your organization invite? Need to resend it or link your GitHub account?</p>
              <ul class="text-sm text-gray-500 space-y-2 mb-6 list-disc pl-5">
                <li>Verify your identity securely via email OTP</li>
                <li>View your assigned FYP Repository link</li>
                <li>Dispatch a fresh GitHub invite to yourself</li>
              </ul>
            </div>
            <router-link to="/student-portal" class="w-full inline-flex justify-center items-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 transition">
              Enter Access Portal &rarr;
            </router-link>
          </div>
        </div>

        <!-- SECTION 3: Support & Email Change -->
        <div class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden flex flex-col hover:shadow-lg transition">
          <div class="bg-red-600 p-4 border-b border-red-700">
            <h2 class="text-xl font-bold text-white flex items-center"><i class="fas fa-life-ring mr-2"></i> Report Issue / Change Email</h2>
          </div>
          <div class="p-6 flex-grow flex flex-col justify-between">
            <div>
              <p class="text-gray-600 mb-4 font-medium">Are you facing issues with your group configuration, or need to change your registered email address?</p>
              <ul class="text-sm text-gray-500 space-y-2 mb-6 list-disc pl-5">
                <li>Request an email address update</li>
                <li>Report wrong group assignments</li>
                <li>Direct ticketing to FYP Administration</li>
              </ul>
            </div>
            <button @click="showContactModal = true" class="w-full inline-flex justify-center items-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-bold text-white bg-red-600 hover:bg-red-700 transition">
              Open Support Ticket &rarr;
            </button>
          </div>
        </div>
      </div>

      <!-- Bottom Row: Git Setup Guide -->
      <div class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
        <div class="bg-gray-900 p-5 border-b border-gray-800">
          <h2 class="text-2xl font-bold text-white flex items-center"><i class="fas fa-terminal mr-3 text-green-400"></i> Code Deployment Guide</h2>
        </div>
        <div class="p-6 md:p-8 space-y-8">
          <!-- Step 1 -->
          <div>
            <h3 class="font-extrabold text-gray-900 text-xl border-b-2 border-gray-100 pb-2 flex items-center">
              <span class="bg-blue-100 text-blue-800 rounded-full h-8 w-8 inline-flex items-center justify-center mr-3 text-sm">1</span> 
              Install Git on Your Machine
            </h3>
            <p class="text-base text-gray-600 mt-3">Before you can push code to the SZABIST organization, you must have the Git CLI installed on your operating system.</p>
            <div class="mt-4 flex flex-wrap gap-4">
              <a href="https://git-scm.com/downloads" target="_blank" class="inline-flex items-center px-4 py-2 border border-gray-300 rounded text-sm font-bold text-gray-700 bg-gray-50 hover:bg-gray-100">
                <i class="fas fa-download mr-2"></i> Official Git Downloads (Windows/Mac/Linux)
              </a>
              <a href="https://docs.github.com/en/get-started/getting-started-with-git/set-up-git" target="_blank" class="inline-flex items-center px-4 py-2 border border-gray-300 rounded text-sm font-bold text-gray-700 bg-gray-50 hover:bg-gray-100">
                <i class="fab fa-github mr-2"></i> GitHub Setup Guide
              </a>
            </div>
          </div>

          <!-- Step 2: Configuration & Code Push -->
          <div>
            <h3 class="font-extrabold text-gray-900 text-lg md:text-xl border-b-2 border-gray-100 pb-2 flex items-center break-words">
              <span class="bg-blue-100 text-blue-800 rounded-full h-8 w-8 inline-flex items-center justify-center mr-3 text-sm flex-shrink-0">2</span> 
              Push Your Code (Resolving Conflicts & Auth)
            </h3>
            <p class="text-sm md:text-base text-gray-600 mt-3 mb-4">Open your terminal in your project folder. We have included the exact commands to bypass the most common student errors (like rejected pushes and main/master branch conflicts).</p>
            
            <div class="bg-gray-900 text-green-400 p-4 md:p-6 rounded-lg font-mono text-xs md:text-sm overflow-x-auto shadow-inner space-y-3 border border-gray-700">
              
              <p><span class="text-gray-500 select-none"># 1. First, tell Git who you are (prevents commit errors)</span><br>
              <span class="font-bold text-white">git config --global user.name "Your Name"</span><br>
              <span class="font-bold text-white">git config --global user.email "your_email@szabist.pk"</span></p>
              
              <div class="border-t border-gray-700 my-2"></div>

              <p><span class="text-gray-500 select-none"># 2. Initialize repo and force the branch name to 'main'</span><br>
              <span class="font-bold text-white">git init -b main</span></p>
              
              <p><span class="text-gray-500 select-none"># 3. Stage and commit your project files</span><br>
              <span class="font-bold text-white">git add .</span><br>
              <span class="font-bold text-white">git commit -m "Initial FYP code push"</span></p>
              
              <div class="border-t border-gray-700 my-2"></div>

              <p><span class="text-gray-500 select-none"># 4. Link your local code to your specific SZABIST FYP repository</span><br>
              <span class="font-bold text-yellow-300">git remote add origin https://github.com/szabist-karachi-campus/YOUR_REPO_NAME.git</span></p>
              
              <p><span class="text-gray-500 select-none"># 5. PULL FIRST! This prevents "updates were rejected" errors if your repo has a README.</span><br>
              <span class="font-bold text-white">git pull origin main --rebase</span></p>
              
              <p><span class="text-gray-500 select-none"># 6. Finally, push your code. (A browser window will pop up asking you to log into GitHub).</span><br>
              <span class="font-bold text-white">git push -u origin main</span></p>
            </div>
            
            <div class="mt-4 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-r-md">
              <p class="text-xs md:text-sm text-yellow-800 font-bold"><i class="fas fa-key mr-1"></i> Authentication Note:</p>
              <p class="text-xs md:text-sm text-yellow-700 mt-1">If the terminal asks for a password instead of opening a browser, GitHub no longer accepts account passwords. You must generate a <strong>Personal Access Token (Classic)</strong> from your GitHub Developer Settings and paste that in as your password.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: Support Ticket -->
    <div v-if="showContactModal" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-2xl max-w-md w-full p-6 space-y-4">
        <h3 class="text-xl font-bold text-gray-900 border-b pb-2">Submit Support Ticket</h3>
        <p class="text-sm text-gray-600">Need to change your email or fix a group issue? This will be sent directly to Administration.</p>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-bold text-gray-700">Full Name</label>
            <input v-model="form.student_name" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm" placeholder="Ali Raza">
          </div>
          <div>
            <label class="block text-sm font-bold text-gray-700">Group ID</label>
            <input v-model="form.group_no" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm" placeholder="P605">
          </div>
        </div>
        <div>
          <label class="block text-sm font-bold text-gray-700">Current / New Email Address</label>
          <input v-model="form.email" type="email" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm" placeholder="email@szabist.pk">
        </div>
        <div>
          <label class="block text-sm font-bold text-gray-700">Issue Description</label>
          <textarea v-model="form.issue_description" rows="4" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm" placeholder="Please explain your issue clearly..."></textarea>
        </div>

        <div class="flex justify-end space-x-3 mt-4 pt-2">
          <button @click="showContactModal = false" class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium bg-white hover:bg-gray-50">Cancel</button>
          <button @click="submitTicket" :disabled="isLoading || !form.email || !form.issue_description" class="px-4 py-2 bg-red-600 text-white rounded-md text-sm font-bold disabled:opacity-50 hover:bg-red-700 transition">
            {{ isLoading ? 'Sending...' : 'Submit Ticket' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const showContactModal = ref(false)
const isLoading = ref(false)
const notification = ref({ show: false, message: '', type: 'info' })

const form = ref({
  student_name: '',
  email: '',
  group_no: '',
  issue_description: ''
})

const showMessage = (msg, type = 'error') => {
  notification.value = { show: true, message: msg, type }
  window.scrollTo({ top: 0, behavior: 'smooth' })
  setTimeout(() => { notification.value.show = false }, 6000)
}

const submitTicket = async () => {
  isLoading.value = true
  try {
    await api.post('/students/contact-admin', form.value)
    showMessage("Success: Your support ticket has been sent to the Administrator.", "success")
    showContactModal.value = false
    form.value = { student_name: '', email: '', group_no: '', issue_description: '' }
  } catch (err) {
    showMessage("Failed to submit ticket. Please try again later.", "error")
  } finally {
    isLoading.value = false
  }
}
</script>
