<!-- src/views/Profile.vue -->
<template>
    <div class="profile-container">
      <h1>Profil</h1>
  
      <div v-if="loading" class="loading">Lade Benutzerdaten...</div>
      <div v-else-if="error" class="error">Fehler: {{ error }}</div>
      <div v-else class="profile-details">
        <div class="profile-info">
          <p><strong>E-Mail:</strong> {{ user.email }}</p>
          <p><strong>Organisation:</strong> {{ user.organization }}</p>
        </div>
  
        <div class="otp-toggle">
          <span><strong>2FA aktiviert:</strong></span>
          <label class="switch">
            <input type="checkbox" v-model="otpEnabled" @change="toggleOTP" />
            <span class="slider round"></span>
          </label>
        </div>
  
        <div v-if="otpQRCodeUrl" class="qr-code-section">
          <p>Scanne diesen QR-Code:</p>
          <img :src="otpQRCodeUrl" alt="QR-Code für 2FA" class="qr-code-image" />
        </div>
  
        <div class="profile-actions">
          <button @click="changePassword">Passwort ändern</button>
        </div>
  
        <h2>Aktivitäten</h2>
        <p v-if="!activities.length">Noch keine Aktivitäten.</p>
        <!-- activities-Logik falls vorhanden -->
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        user: null,
        otpEnabled: false,
        otpQRCodeUrl: null,
        loading: true,
        error: null,
        activities: []
      }
    },
    async mounted() {
      await this.fetchUserData()
    },
    methods: {
      async fetchUserData() {
        this.loading = true
        try {
          const { data } = await axios.get('/user/profile')
          this.user = data
          this.otpEnabled = data['2faEnabled']
        } catch (e) {
          this.error = e.response?.data?.error || e.message
        } finally {
          this.loading = false
        }
      },
      changePassword() {
        // euer bestehender Flow
      },
      async toggleOTP() {
        try {
          const { data } = await axios.post('/user/2fa', { enable: this.otpEnabled })
          if (this.otpEnabled) {
            this.otpQRCodeUrl = `data:image/png;base64,${data.qr_code_png_base64}`
          } else {
            this.otpQRCodeUrl = null
          }
          alert(`2FA ${this.otpEnabled ? 'aktiviert' : 'deaktiviert'}.`)
        } catch (e) {
          alert('Fehler beim Umschalten der 2FA.')
          this.otpEnabled = !this.otpEnabled
        }
      }
    }
  }
  </script>
  
  <style scoped>
    .profile-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    .profile-container h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    }

    .profile-info {
    margin-top: 1rem;
    }

    .profile-info p {
    font-size: 1.125rem;
    margin-bottom: 1rem;
    }

    .profile-actions {
    margin-top: 2rem;
    display: flex;
    gap: 1rem;
    justify-content: flex-start;
    }

    .profile-actions button {
    padding: 0.75rem 1.5rem;
    background-color: #22d3ee;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
    }

    .profile-actions button:hover {
    background-color: #6366f1;
    }

    h2 {
    margin-top: 3rem;
    font-size: 1.75rem;
    }

    .switch {
    position: relative;
    display: inline-block;
    width: 48px;
    height: 24px;
    margin-right: 10px;
    }

    .switch input {
    opacity: 0;
    width: 0;
    height: 0;
    }

    .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 24px;
    }

    .slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
    }

    input:checked + .slider {
    background-color: #10b981;
    }

    input:checked + .slider:before {
    transform: translateX(24px);
    }

    .otp-toggle {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    }

    .qr-code-section {
    margin-top: 1.5rem;
    text-align: center;
    }

    .qr-code-image {
    margin-top: 0.5rem;
    max-width: 200px;
    }  
</style>
  