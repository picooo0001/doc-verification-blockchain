<template>
  <div class="profile-container" v-if="user">
    <h1>Profil</h1>

    <div class="profile-info">
      <p><strong>Mail:</strong> {{ user.email }}</p>
      <p><strong>Organisation:</strong> {{ user.organization }}</p>
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

    <div class="profile-actions">
      <button class="change-password-btn" @click="changePassword">Passwort ändern</button>
   
    </div>

    <h2>Deine Aktivitäten</h2>
    <p>Du hast noch keine Aktivitäten durchgeführt.</p>
  </div>
  <div v-else>
    <p>Lade Benutzerdaten...</p>
  </div>
</template>
<script>
export default {
  data() {
    return {
      user: null,
      otpEnabled: false,
      otpQRCodeUrl: null,
    };
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      try {
        const response = await fetch("http://localhost:5001/user/profile", {
          method: "GET",
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
          this.user = data;
          this.otpEnabled = data["2faEnabled"]; // ⬅️ Diese Zeile war vorher gefehlt!
        } else {
          console.error("Fehler beim Abrufen der Benutzerdaten");
        }
      } catch (error) {
        console.error("Fehler:", error);
      }
    },
    editProfile() {
      // TODO
    },
    changePassword() {
      // TODO
    },
    async toggleOTP() {
      console.log("Toggle OTP wird ausgelöst");

      try {
        const response = await fetch("http://localhost:5001/user/2fa", {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ enable: this.otpEnabled }),
        });

        if (response.ok) {
          const data = await response.json();
          console.log("Antwort vom Backend:", data);

          if (this.otpEnabled && data.qr_code_png_base64) {
            this.otpQRCodeUrl = `data:image/png;base64,${data.qr_code_png_base64}`;
          } else {
            this.otpQRCodeUrl = null;
          }

          alert(`2FA wurde ${this.otpEnabled ? "aktiviert" : "deaktiviert"}.`);
        } else {
          alert("Fehler beim Ändern des 2FA-Status");
          this.otpEnabled = !this.otpEnabled;
        }
      } catch (error) {
        console.error("Fehler:", error);
        this.otpEnabled = !this.otpEnabled;
      }
    },
  },
};
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
