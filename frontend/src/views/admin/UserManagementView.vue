<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">System Users</h1>
      <button @click="openAddModal" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700 transition">
        + Add New User
      </button>
    </div>

    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID / Reg #</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">GitHub</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              <span class="font-bold">#{{ user.id }}</span> <br/>
              <span class="text-gray-500">{{ user.reg_id || 'N/A' }}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ user.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.email }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <span :class="roleColor(user.role)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                {{ user.role }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.github_username || 'Missing' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="editUser(user)" class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit User Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-md p-6">
        <h2 class="text-xl font-bold mb-4">{{ isEditing ? 'Edit User' : 'Add New User' }}</h2>
        
        <form @submit.prevent="saveUser" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Name</label>
            <input v-model="formData.name" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input v-model="formData.email" type="email" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Reg ID</label>
              <input v-model="formData.reg_id" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Role</label>
              <select v-model="formData.role" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
                <option value="STUDENT">Student</option>
                <option value="COORDINATOR">Coordinator</option>
                <option value="ADMIN">Admin</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">GitHub Username</label>
            <input v-model="formData.github_username" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
          </div>

          <div class="flex justify-end space-x-3 mt-6">
            <button type="button" @click="closeModal" class="px-4 py-2 border border-gray-300 rounded shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">Cancel</button>
            <button type="submit" class="px-4 py-2 border border-transparent rounded shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const users = ref([]);
const showModal = ref(false);
const isEditing = ref(false);
const editingUserId = ref(null);

const formData = ref({
  name: '',
  email: '',
  reg_id: '',
  role: 'STUDENT',
  github_username: '',
  group_id: null
});

const fetchUsers = async () => {
  try {
    const response = await api.get('/admin/users');
    users.value = response.data;
  } catch (error) {
    console.error("Failed to load users:", error);
  }
};

const roleColor = (role) => {
  if (role === 'ADMIN') return 'bg-red-100 text-red-800';
  if (role === 'COORDINATOR') return 'bg-purple-100 text-purple-800';
  return 'bg-green-100 text-green-800';
};

const openAddModal = () => {
  isEditing.value = false;
  editingUserId.value = null;
  formData.value = { name: '', email: '', reg_id: '', role: 'STUDENT', github_username: '', group_id: null };
  showModal.value = true;
};

const editUser = (user) => {
  isEditing.value = true;
  editingUserId.value = user.id;
  formData.value = { ...user };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const saveUser = async () => {
  try {
    if (isEditing.value) {
      await api.put(`/admin/users/${editingUserId.value}`, formData.value);
    } else {
      await api.post('/admin/users', formData.value);
    }
    closeModal();
    fetchUsers(); // Refresh table
  } catch (error) {
    console.error("Error saving user:", error);
    alert("Failed to save user details.");
  }
};

onMounted(() => {
  fetchUsers();
});
</script>
