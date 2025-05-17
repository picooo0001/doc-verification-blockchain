<template>
  <div class="main-layout">
    <div v-if="loadingUser">
      <p>Lade Benutzerdaten...</p>
    </div>
    <div v-else class="profile-container">
      <h1>Profil</h1>

      <div class="profile-info">
        <p><strong>Mail:</strong> {{ user.email }}</p>
        <p><strong>Organisation:</strong> {{ user.organization }}</p>
        <p><strong>Wallet Address:</strong> {{ user.walletAddress }}</p>
        <p><strong>Owner:</strong> {{ user.isOwner }}</p>
      </div>

      <div class="otp-toggle">
        <span><strong>Activate 2FA:</strong></span>
        <label class="switch">
          <input type="checkbox" v-model="otpEnabled" @change="toggleOTP">
          <span class="slider round"></span>
        </label>
      </div>
      <div v-if="otpQRCodeUrl" class="qr-code-section">
        <p>Scanne diesen QR-Code mit deiner Authenticator-App:</p>
        <img :src="otpQRCodeUrl" alt="QR-Code zur 2FA-Aktivierung" class="qr-code-image" />
      </div>

      <h2>Deine Aktivitäten</h2>
      <div v-if="activities.length">
        <table class="activity-table">
          <thead>
            <tr>
              <th>Block</th>
              <th>Zeitpunkt</th>
              <th>Tx Hash</th>
              <th>Dokumentenhash</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="act in activities" :key="act.txHash">
              <td>{{ act.blockNumber }}</td>
              <td>{{ formatTimestamp(act.timestamp) }}</td>
              <td>{{ shortenHash(act.txHash) }}</td>
              <td>{{ shortenHash(act.documentHash) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else>Du hast noch keine Aktivitäten durchgeführt.</p>
    </div>
  </div>
</template>

<script>
import api from '@/api'

export default {
  data() {
    return {
      user: null,
      loadingUser: true,
      otpEnabled: false,
      otpQRCodeUrl: null,
      activities: []
    }
  },
  async mounted() {
    await this.fetchUserData()
    await this.fetchActivities()
  },
  methods: {
    async fetchUserData() {
      try {
        const { data } = await api.get('/user/profile')
        this.user = {
          email:          data.email,
          organization:   data.organization_name || data.organization,
          walletAddress:  data.wallet_address,
          isOwner:        data.is_owner
        }
        this.otpEnabled = data['2faEnabled']
      } catch (error) {
        console.error('Fehler beim Abrufen der Benutzerdaten:', error)
      } finally {
        this.loadingUser = false
      }
    },
    async toggleOTP() {
      try {
        const { data } = await api.post('/user/2fa', { enable: this.otpEnabled })
        if (this.otpEnabled && data.qr_code_png_base64) {
          this.otpQRCodeUrl = `data:image/png;base64,${data.qr_code_png_base64}`
        } else {
          this.otpQRCodeUrl = null
        }
        alert(`2FA wurde ${this.otpEnabled ? 'aktiviert' : 'deaktiviert'}.`)
      } catch (error) {
        console.error('Fehler beim Ändern des 2FA-Status:', error)
        this.otpEnabled = !this.otpEnabled
        alert('Fehler beim Ändern des 2FA-Status.')
      }
    },
    async fetchActivities() {
      try {
        const { data } = await api.get('/users/me/activities')
        this.activities = data.activities || []
      } catch (error) {
        console.error('Fehler beim Laden der Aktivitäten:', error)
      }
    },
    formatTimestamp(ts) {
      return new Date(ts * 1000).toLocaleString('de-DE', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    },
    shortenHash(hash) {
      return hash.slice(0, 6) + '…' + hash.slice(-4)
    }
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  gap: 2.5rem;
  padding: 3rem 2rem 2rem 2rem;
  min-height: 100vh;
  background: linear-gradient(45deg, #ffffff 0%, #ffffff 60%, #e7d6fb 75%, #cdb6ec 90%, #eab6d8 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
.profile-container {
  max-width: 1200px;
  border-radius: 6px; /* wie der Button im Screenshot */
  margin: 2rem auto;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.95);
  
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
  border-radius: 6px;
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

.trial-btn {
  background: #1a1726;
  color: #fff;
  border: 2px solid transparent; /* <-- hier */
  border-radius: 7px;              /* Weniger stark abgerundet */
  padding: 0.7rem 1.7rem;          /* Weniger hoch und schmaler */
  font-size: 1.15rem;              /* Kleinere Schrift */
  font-weight: 700;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  cursor: pointer;
  transition: background 0.18s, transform 0.18s;
  box-shadow: none;
  outline: none;
  display: inline-block;
  letter-spacing: 0.01em;
}

.trial-btn:hover,
.trial-btn:focus {
  background: #ffffff;        /* weißer Hintergrund */
  color: #000000;             /* schwarze Schrift */
  border: 2px solid #000000;  /* schwarzer Rand */
  transform: translateY(-2px) scale(1.03);
}

</style>
