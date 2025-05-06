<template>
  <div class="main-layout">
  <div class="login-container">
    <h1>Login</h1>
    <p class="subtitle">Melde dich mit deinen Organisations-Credentials an.</p>

    <!-- Form-Element für automatisches Login bei Enter -->
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="email">E-Mail</label>
        <input type="email" id="email" v-model="email" placeholder="name@example.com" />
      </div>

      <div class="form-group">
        <label for="password">Passwort</label>
        <input type="password" id="password" v-model="password" placeholder="••••••••" />
      </div>
      
      <!-- 2FA Eingabefeld nur anzeigen, wenn erforderlich -->
      <div v-if="is2FARequired" class="form-group">
        <label for="otp">2FA-Code</label>
        <input
          type="text"
          id="otp"
          v-model="otp"
          placeholder="Gib deinen 6-stelligen Code ein"
          maxlength="6"
        />
      </div>
      <div class="action-container">
        <button class="trial-btn" type="submit">Login</button>
      </div>
    </form>
      <hr />
      <h3>Oder per Wallet:</h3>
      <WalletLogin />
  </div>
</div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import WalletLogin from '@/components/WalletLogin.vue'

// Reaktive Variablen
const email = ref('')
const password = ref('')
const otp = ref('')  // Variable für den 2FA-Code
const is2FARequired = ref(false)  // Flag, ob 2FA erforderlich ist
const router = useRouter()

// Login-Funktion
async function login() {
  if (!email.value || !password.value) {
    alert('Bitte fülle alle Felder aus.')
    return
  }

  const loginData = {
    email: email.value,
    password: password.value,
  }

  // Wenn 2FA erforderlich ist, müssen wir den OTP hinzufügen
  if (is2FARequired.value) {
    if (!otp.value) {
      alert("Bitte gib deinen 2FA-Code ein.")
      return
    }
    loginData.otp = otp.value  // OTP zur Login-Daten hinzufügen
  }

  try {
    const response = await axios.post('http://localhost:5001/login', loginData, {
      withCredentials: true,  // ermöglicht das Senden von Cookies (wie Session-IDs)
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',  // Achte auf den richtigen Content-Type
      }
    })

    console.log(response.data.message)
    alert('Login erfolgreich.')
    localStorage.setItem('isLoggedIn', 'true')  // Loginstatus speichern
    router.push('/sign-pdf')  // Weiterleitung zur nächsten Seite
  } catch (error) {
    const err = error.response?.data?.error

    if (err === '2FA erforderlich') {
      // Falls 2FA erforderlich ist, zeigen wir das OTP-Eingabefeld
      is2FARequired.value = true
      alert('Bitte gib deinen 2FA-Code ein.')
    } else if (err === 'Ungültiges OTP') {
      alert('Der eingegebene 2FA-Code ist falsch.')
    } else if (err === 'Ungültige E-Mail oder Passwort') {
      alert('Überprüfe deine E-Mail und Passwort.')
    } else {
      alert('Login fehlgeschlagen: ' + (err || 'Unbekannter Fehler'))
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
  .login-container {
    max-width: 400px;
    padding: 2.5rem 2rem 2rem 2rem;
  margin-bottom: 2rem;
    background: linear-gradient(180deg, #fff 0%, #f6eefd 60%, #f2e4f4 100%);    border-radius: 16px;
    color: black;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    text-align: center;
    font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }

  .subtitle {
    color: black;
    margin-bottom: 2rem;
  }

  .form-group {
    margin-bottom: 1.5rem;
    text-align: left;
  }

  label {
    display: block;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    font-size: 1rem;
  }

  input:focus {
    outline: none;
    border-color: #38bdf8;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.3);
  }

  .backend-btn {
    padding: 0.75rem 1.5rem;
    background-color: #22d3ee;
    color: white;
    font-weight: bold;
    font-size: 1.25rem;  /* Schriftgröße vergrößern */
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    min-width: 200px;
  }

  .backend-btn:hover {
    background-color: #6366f1;
    transform: scale(1.02);
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
