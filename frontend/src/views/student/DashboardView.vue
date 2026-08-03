<template>
  <div class="space-y-8">

    <!-- ═══════════════════════════════════════════════════════════
         Welcome Header
    ════════════════════════════════════════════════════════════════ -->
    <div class="welcome-card">
      <div>
        <div class="welcome-label">
          <span class="label-dot"></span>
          <span>Student Dashboard</span>
        </div>
        <h2 class="welcome-title">
          Welcome back, {{ student?.name || student?.email || 'Student' }}
        </h2>
        <p class="welcome-sub">
          Manage your FYP Project Group and GitHub Organization repository access.
        </p>
      </div>

      <div class="verification-badge">
        <p class="badge-label">Verification Status</p>
        <p class="badge-value">
          <svg class="badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          Verified Account
        </p>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════
         Main Grid
    ════════════════════════════════════════════════════════════════ -->
    <div class="main-grid">

      <!-- ── LEFT COLUMN (2/3) ── -->
      <div class="left-col">

        <!-- ─── BRANCH A: Student has an assigned group ─── -->
        <div v-if="student?.group" class="panel group-panel">

          <!-- Panel Header -->
          <div class="panel-header">
            <div>
              <h3 class="panel-title">
                <svg class="panel-title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                FYP Project Group
              </h3>
              <p class="panel-sub">Your assigned group details and team members</p>
            </div>
            <span :class="statusBadgeClass(student.group.status)">
              {{ student.group.status }}
            </span>
          </div>

          <!-- Group Metadata Grid -->
          <div class="meta-grid">
            <div class="meta-item">
              <p class="meta-label">Group ID</p>
              <p class="meta-value">#{{ student.group.id }}</p>
            </div>
            <div class="meta-item">
              <p class="meta-label">Group Name</p>
              <p class="meta-value">{{ student.group.group_name || '—' }}</p>
            </div>
            <div class="meta-item" v-if="student.group.group_no">
              <p class="meta-label">Group No.</p>
              <p class="meta-value">{{ student.group.group_no }}</p>
            </div>
            <div class="meta-item">
              <p class="meta-label">Status</p>
              <p class="meta-value capitalize">{{ student.group.status }}</p>
            </div>
            <div class="meta-item" v-if="student.group.team_name">
              <p class="meta-label">Team Name</p>
              <p class="meta-value">{{ student.group.team_name }}</p>
            </div>
            <div class="meta-item" v-if="student.group.repo_name">
              <p class="meta-label">Repository</p>
              <p class="meta-value repo-name">{{ student.group.repo_name }}</p>
            </div>
          </div>

          <!-- Partners -->
          <div class="info-block" v-if="student.group.partners?.length">
            <p class="info-label">Team Partners</p>
            <div class="partner-list">
              <div
                v-for="partner in student.group.partners"
                :key="partner.id"
                class="partner-card"
              >
                <div class="partner-avatar">
                  {{ (partner.name || partner.email).charAt(0).toUpperCase() }}
                </div>
                <div class="partner-info">
                  <p class="partner-name">{{ partner.name || 'Unknown' }}</p>
                  <p class="partner-email">{{ partner.email }}</p>
                </div>
                <span
                  v-if="partner.invite_status"
                  :class="inviteBadgeClass(partner.invite_status)"
                >
                  {{ partner.invite_status }}
                </span>
              </div>
            </div>
          </div>

          <!-- No partners note -->
          <div v-else class="info-block">
            <p class="info-label">Team Partners</p>
            <p class="info-value muted">No other members assigned to this group yet.</p>
          </div>

          <!-- GitHub Repo Link -->
          <div v-if="student.group.github_repo_url" class="repo-link-block">
            <a :href="student.group.github_repo_url" target="_blank" rel="noopener noreferrer" class="repo-link-btn">
              <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" clip-rule="evenodd"
                  d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
              </svg>
              View GitHub Repository
            </a>
          </div>
        </div>

        <!-- ─── BRANCH B: Student has NO group — show proposal form ─── -->
        <div v-else class="panel proposal-panel">
          <div class="panel-header">
            <div>
              <h3 class="panel-title">FYP Project Group</h3>
              <p class="panel-sub">Submit your project proposal to get started</p>
            </div>
          </div>

          <div class="info-notice">
            <svg class="notice-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            You are currently not a member of any project group. Fill out the form below to propose a new group.
          </div>

          <form @submit.prevent="handleCreateGroup" class="proposal-form">
            <div class="form-field">
              <label class="field-label">Group Name</label>
              <input
                v-model="groupForm.group_name"
                type="text"
                required
                placeholder="e.g. AI Vision Team"
                class="field-input"
              />
            </div>

            <div class="form-field">
              <label class="field-label">Team Name <span class="field-hint">(used for GitHub team, optional)</span></label>
              <input
                v-model="groupForm.team_name"
                type="text"
                placeholder="e.g. ai-vision-team"
                class="field-input"
              />
            </div>

            <div class="form-field">
              <label class="field-label">Partner Emails <span class="field-hint">(comma-separated)</span></label>
              <input
                v-model="groupForm.member_emails_raw"
                type="text"
                placeholder="peer1@szabist.pk, peer2@szabist.pk"
                class="field-input"
              />
            </div>

            <button
              type="submit"
              :disabled="groupLoading"
              class="btn-primary"
            >
              <svg v-if="groupLoading" class="btn-spinner" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
              </svg>
              <span>{{ groupLoading ? 'Submitting...' : 'Submit Group Proposal' }}</span>
            </button>
          </form>
        </div>
      </div>

      <!-- ── RIGHT COLUMN (1/3) — GitHub Org Access ── -->
      <div class="right-col">
        <div class="panel github-panel">
          <div class="panel-header">
            <div>
              <h3 class="panel-title">
                <svg class="panel-title-icon github-icon" fill="currentColor" viewBox="0 0 24 24">
                  <path fill-rule="evenodd" clip-rule="evenodd"
                    d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
                </svg>
                GitHub Org Access
              </h3>
              <p class="panel-sub">Repository invite status and access management</p>
            </div>
          </div>

          <!-- Guard: No group or not approved -->
          <div v-if="!student?.group" class="github-notice pending">
            <svg class="notice-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            You must be assigned to a project group before requesting a GitHub invite.
          </div>

          <div v-else-if="student.group.status !== 'approved'" class="github-notice pending">
            GitHub repository invitations can only be sent once your group proposal is marked
            <strong>Approved</strong> by a coordinator. Current status:
            <span :class="statusBadgeClass(student.group.status)" style="display: inline-flex; margin-left: 4px;">
              {{ student.group.status }}
            </span>
          </div>

          <!-- Approved group — invite section -->
          <div v-else class="space-y-5">

            <!-- Already invited badge -->
            <div v-if="githubInviteStatus && ['sent','active'].includes(githubInviteStatus.invite_status)" class="invite-sent-card">
              <div class="invite-sent-header">
                <svg class="invite-sent-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Invite Dispatched</span>
              </div>
              <p class="invite-sent-sub">
                An invitation has been sent to <strong>{{ student.email }}</strong>.<br>
                Check your GitHub notifications or email to accept.
              </p>
              <div class="invite-meta">
                <div>
                  <p class="meta-label">Invite Status</p>
                  <span :class="inviteBadgeClass(githubInviteStatus.invite_status)">
                    {{ githubInviteStatus.invite_status }}
                  </span>
                </div>
                <div v-if="githubInviteStatus.repo_name">
                  <p class="meta-label">Repository</p>
                  <p class="meta-value repo-name">{{ githubInviteStatus.repo_name }}</p>
                </div>
              </div>

              <!-- Re-send button -->
              <button
                @click="handleSendInvite"
                :disabled="inviteLoading"
                class="btn-outline resend-btn"
              >
                <svg v-if="inviteLoading" class="btn-spinner" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
                </svg>
                {{ inviteLoading ? 'Sending...' : 'Re-send Invite' }}
              </button>
            </div>

            <!-- Not yet invited -->
            <div v-else class="send-invite-card">
              <div class="send-invite-illustration">
                <svg class="send-invite-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <p class="send-invite-title">Ready to join the GitHub Org?</p>
              <p class="send-invite-sub">
                Click below to dispatch a GitHub Organization invite to<br>
                <strong>{{ student.email }}</strong>
              </p>

              <button
                @click="handleSendInvite"
                :disabled="inviteLoading"
                class="btn-primary send-invite-btn"
              >
                <svg v-if="inviteLoading" class="btn-spinner" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
                </svg>
                <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                {{ inviteLoading ? 'Sending Invite...' : 'Send GitHub Invite' }}
              </button>

              <p v-if="inviteError" class="invite-error">{{ inviteError }}</p>
            </div>

          </div>
        </div>

        <!-- ── Quick Profile Card ── -->
        <div class="panel profile-card" v-if="student">
          <h4 class="profile-card-title">Your Profile</h4>
          <div class="profile-rows">
            <div class="profile-row">
              <span class="profile-row-label">Email</span>
              <span class="profile-row-value">{{ student.email }}</span>
            </div>
            <div class="profile-row" v-if="student.reg_id">
              <span class="profile-row-label">Reg. ID</span>
              <span class="profile-row-value">{{ student.reg_id }}</span>
            </div>
            <div class="profile-row" v-if="student.github_username">
              <span class="profile-row-label">GitHub</span>
              <span class="profile-row-value github-handle">@{{ student.github_username }}</span>
            </div>
            <div class="profile-row">
              <span class="profile-row-label">Role</span>
              <span class="profile-row-value capitalize">{{ student.role }}</span>
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
import api from '@/services/api'

const authStore = useAuthStore()

// ─── State ────────────────────────────────────────────────────────────────
const student = ref(null)           // full StudentProfileResponse incl. group + partners
const githubInviteStatus = ref(null) // InviteStatusResponse from /github/status or /students/me/github-invite

const groupForm = ref({
  group_name: '',
  team_name: '',
  member_emails_raw: '',
})
const groupLoading = ref(false)
const inviteLoading = ref(false)
const inviteError = ref('')

// ─── Helpers ──────────────────────────────────────────────────────────────
const statusBadgeClass = (statusVal) => {
  const base = 'px-2.5 py-0.5 text-xs font-bold rounded-full uppercase tracking-wider border'
  if (statusVal === 'approved') return `${base} bg-emerald-100 text-emerald-700 border-emerald-200`
  if (statusVal === 'rejected') return `${base} bg-red-100 text-red-700 border-red-200`
  return `${base} bg-amber-100 text-amber-700 border-amber-200`
}

const inviteBadgeClass = (inviteVal) => {
  const base = 'px-2 py-0.5 text-xs font-bold rounded-full uppercase tracking-wider border'
  if (['sent', 'active'].includes(inviteVal)) return `${base} bg-emerald-100 text-emerald-700 border-emerald-200`
  if (inviteVal === 'pending') return `${base} bg-amber-100 text-amber-700 border-amber-200`
  return `${base} bg-slate-100 text-slate-500 border-slate-200`
}

// ─── Data Fetching ────────────────────────────────────────────────────────
const fetchData = async () => {
  // Single source of truth: GET /students/me returns group + partners inline
  student.value = await authStore.fetchStudentData()

  // Fetch existing GitHub invite status once we know the group is approved
  if (student.value?.group?.status === 'approved') {
    try {
      const ghRes = await api.get('/github/status')
      githubInviteStatus.value = ghRes.data
    } catch {
      githubInviteStatus.value = null
    }
  }
}

// ─── Group Proposal ───────────────────────────────────────────────────────
const handleCreateGroup = async () => {
  groupLoading.value = true
  try {
    const emails = groupForm.value.member_emails_raw
      .split(',')
      .map((e) => e.trim())
      .filter((e) => e.length > 0)

    await api.post('/groups/', {
      group_name: groupForm.value.group_name,
      team_name: groupForm.value.team_name || undefined,
      member_emails: emails,
    })

    // Refresh full student profile so the group view renders immediately
    student.value = await authStore.fetchStudentData()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to create project group.')
  } finally {
    groupLoading.value = false
  }
}

// ─── GitHub Invite ────────────────────────────────────────────────────────
const handleSendInvite = async () => {
  inviteError.value = ''
  inviteLoading.value = true
  try {
    const res = await api.post('/students/me/github-invite', {})
    githubInviteStatus.value = res.data
  } catch (err) {
    inviteError.value = err.response?.data?.detail || 'Failed to dispatch GitHub invite.'
  } finally {
    inviteLoading.value = false
  }
}

// ─── Lifecycle ───────────────────────────────────────────────────────────
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* ── Layout ──────────────────────────────────────────────────── */
.main-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}
@media (min-width: 1024px) {
  .main-grid {
    grid-template-columns: 2fr 1fr;
  }
}
.left-col  { display: flex; flex-direction: column; gap: 1.5rem; }
.right-col { display: flex; flex-direction: column; gap: 1.5rem; }

/* ── Welcome Card ────────────────────────────────────────────── */
.welcome-card {
  background: #fff;
  border: 1px solid #e8edf3;
  border-radius: 1rem;
  padding: 1.75rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-shadow: 0 1px 4px rgba(18, 79, 159, 0.06);
}
@media (min-width: 640px) {
  .welcome-card { flex-direction: row; align-items: center; justify-content: space-between; }
}
.welcome-label {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #124f9f;
  margin-bottom: 0.25rem;
}
.label-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #124f9f;
  flex-shrink: 0;
}
.welcome-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
}
.welcome-sub {
  font-size: 0.8125rem;
  color: #64748b;
  margin-top: 0.2rem;
}
.verification-badge {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 0.75rem 1rem;
  white-space: nowrap;
  flex-shrink: 0;
}
.badge-label { font-size: 0.7rem; color: #94a3b8; font-weight: 500; }
.badge-value {
  display: flex; align-items: center; justify-content: flex-end;
  font-size: 0.75rem; font-weight: 700; color: #059669; margin-top: 0.2rem;
}
.badge-icon { width: 14px; height: 14px; margin-right: 4px; }

/* ── Panels ──────────────────────────────────────────────────── */
.panel {
  background: #fff;
  border: 1px solid #e8edf3;
  border-radius: 1rem;
  padding: 1.75rem;
  box-shadow: 0 1px 4px rgba(18, 79, 159, 0.06);
}
.group-panel  { border-top: 3px solid #124f9f; }
.github-panel { border-top: 3px solid #1a1a2e; }

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.panel-title {
  display: flex; align-items: center;
  font-size: 1.0625rem;
  font-weight: 700; color: #0f172a;
  letter-spacing: -0.01em;
}
.panel-title-icon {
  width: 18px; height: 18px;
  margin-right: 0.5rem; color: #124f9f; flex-shrink: 0;
}
.github-icon { color: #1a1a2e; }
.panel-sub { font-size: 0.75rem; color: #94a3b8; margin-top: 0.2rem; }

/* ── Meta Grid ───────────────────────────────────────────────── */
.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 0.75rem;
  padding: 1rem;
  margin-bottom: 1.25rem;
}
.meta-item {}
.meta-label { font-size: 0.68rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.meta-value { font-size: 0.875rem; font-weight: 700; color: #0f172a; margin-top: 0.15rem; }
.repo-name  { font-family: monospace; color: #124f9f; font-size: 0.8rem; }
.capitalize { text-transform: capitalize; }

/* ── Info Blocks ─────────────────────────────────────────────── */
.info-block { margin-bottom: 1.25rem; }
.info-label {
  font-size: 0.68rem; font-weight: 700; color: #94a3b8;
  text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.35rem;
}
.info-value { font-size: 0.9rem; color: #1e293b; }
.project-title { font-size: 1rem; font-weight: 700; color: #124f9f; }
.desc-text  { font-size: 0.8125rem; color: #475569; white-space: pre-line; line-height: 1.6; }
.muted      { color: #94a3b8; font-size: 0.8125rem; }

/* ── Partner Cards ───────────────────────────────────────────── */
.partner-list { display: flex; flex-direction: column; gap: 0.625rem; }
.partner-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #f8fafc;
  border: 1px solid #e8edf3;
  border-radius: 0.625rem;
  padding: 0.75rem 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.partner-card:hover {
  border-color: #bfdbfe;
  box-shadow: 0 0 0 3px rgba(18, 79, 159, 0.06);
}
.partner-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, #124f9f, #1e6fcf);
  color: #fff;
  font-size: 0.875rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.partner-info { flex: 1; min-width: 0; }
.partner-name  { font-size: 0.8125rem; font-weight: 600; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.partner-email { font-size: 0.75rem; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ── Repo Link ────────────────────────────────────────────────── */
.repo-link-block { margin-top: 1rem; }
.repo-link-btn {
  display: inline-flex; align-items: center;
  font-size: 0.8rem; font-weight: 600; color: #124f9f;
  text-decoration: none;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  transition: background 0.2s, box-shadow 0.2s;
}
.repo-link-btn:hover { background: #dbeafe; box-shadow: 0 2px 6px rgba(18,79,159,0.12); }

/* ── Proposal Form ───────────────────────────────────────────── */
.proposal-panel { border-top: 3px solid #64748b; }
.info-notice {
  display: flex; align-items: flex-start; gap: 0.625rem;
  background: #eff6ff; border: 1px solid #bfdbfe;
  border-radius: 0.625rem; padding: 0.875rem 1rem;
  font-size: 0.8125rem; color: #1d4ed8;
  margin-bottom: 1.5rem;
}
.notice-icon { width: 16px; height: 16px; flex-shrink: 0; margin-top: 0.1rem; }
.proposal-form { display: flex; flex-direction: column; gap: 1rem; }
.form-field { display: flex; flex-direction: column; gap: 0.3rem; }
.field-label {
  font-size: 0.7rem; font-weight: 700; color: #475569;
  text-transform: uppercase; letter-spacing: 0.06em;
}
.field-hint { font-size: 0.68rem; color: #94a3b8; font-weight: 400; text-transform: none; letter-spacing: 0; }
.field-input {
  width: 100%; padding: 0.625rem 0.875rem;
  font-size: 0.875rem; color: #0f172a;
  border: 1.5px solid #e2e8f0; border-radius: 0.5rem;
  outline: none; transition: border-color 0.2s, box-shadow 0.2s;
  background: #fff;
}
.field-input:focus { border-color: #124f9f; box-shadow: 0 0 0 3px rgba(18,79,159,0.1); }
.field-textarea { resize: vertical; }

/* ── Buttons ─────────────────────────────────────────────────── */
.btn-primary {
  display: inline-flex; align-items: center; justify-content: center;
  background: #124f9f;
  color: #fff;
  font-size: 0.8125rem; font-weight: 700;
  border: none; border-radius: 0.625rem;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
  box-shadow: 0 2px 8px rgba(18,79,159,0.25);
}
.btn-primary:hover:not(:disabled) { background: #0e3d7a; box-shadow: 0 4px 12px rgba(18,79,159,0.35); transform: translateY(-1px); }
.btn-primary:active:not(:disabled) { transform: translateY(0); }
.btn-primary:disabled { opacity: 0.55; cursor: not-allowed; }

.btn-outline {
  display: inline-flex; align-items: center; justify-content: center;
  background: transparent;
  border: 1.5px solid #124f9f; color: #124f9f;
  font-size: 0.75rem; font-weight: 700;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
}
.btn-outline:hover:not(:disabled) { background: #eff6ff; }
.btn-outline:disabled { opacity: 0.55; cursor: not-allowed; }

.btn-spinner {
  width: 16px; height: 16px; margin-right: 0.5rem;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── GitHub Panel Content ────────────────────────────────────── */
.github-notice {
  display: flex; align-items: flex-start; gap: 0.625rem;
  background: #f8fafc; border: 1px solid #e2e8f0;
  border-radius: 0.625rem; padding: 0.875rem 1rem;
  font-size: 0.8125rem; color: #64748b; line-height: 1.55;
}
.github-notice strong { color: #0f172a; }

/* Invite Sent */
.invite-sent-card {
  background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
  border: 1px solid #a7f3d0;
  border-radius: 0.75rem;
  padding: 1.25rem;
}
.invite-sent-header {
  display: flex; align-items: center; gap: 0.5rem;
  font-size: 0.9rem; font-weight: 700; color: #047857;
  margin-bottom: 0.5rem;
}
.invite-sent-icon { width: 18px; height: 18px; color: #059669; }
.invite-sent-sub { font-size: 0.8rem; color: #065f46; line-height: 1.55; margin-bottom: 1rem; }
.invite-meta { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem; }
.resend-btn { width: 100%; }

/* Send Invite */
.send-invite-card {
  text-align: center;
  padding: 1rem 0.5rem;
}
.send-invite-illustration {
  width: 56px; height: 56px;
  background: linear-gradient(135deg, #e0eeff, #c7d9f8);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1rem;
}
.send-invite-icon { width: 28px; height: 28px; color: #124f9f; }
.send-invite-title { font-size: 1rem; font-weight: 700; color: #0f172a; margin-bottom: 0.4rem; }
.send-invite-sub { font-size: 0.8rem; color: #64748b; line-height: 1.55; margin-bottom: 1.25rem; }
.send-invite-btn { width: 100%; }
.invite-error { font-size: 0.75rem; color: #dc2626; margin-top: 0.5rem; text-align: center; }

/* ── Profile Card ────────────────────────────────────────────── */
.profile-card { border-top: 3px solid #94a3b8; }
.profile-card-title {
  font-size: 0.8rem; font-weight: 700; color: #64748b;
  text-transform: uppercase; letter-spacing: 0.06em;
  margin-bottom: 0.875rem;
}
.profile-rows { display: flex; flex-direction: column; gap: 0.625rem; }
.profile-row { display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
.profile-row-label { font-size: 0.75rem; color: #94a3b8; font-weight: 600; flex-shrink: 0; }
.profile-row-value { font-size: 0.8rem; color: #0f172a; font-weight: 500; text-align: right; word-break: break-all; }
.github-handle { font-family: monospace; color: #124f9f; }
</style>
