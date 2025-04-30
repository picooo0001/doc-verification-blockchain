<template>
  <div class="login-container">
    <h1>Login</h1>
    <p class="subtitle">Melde dich mit deinen Organisations-Credentials an.</p>

    <div class="form-group">
      <label for="email">E-Mail</label>
      <input type="email" id="email" v-model="email" placeholder="name@example.com" />
    </div>

    <div class="form-group">
      <label for="password">Passwort</label>
      <input type="password" id="password" v-model="password" placeholder="••••••••" />
    </div>

    <!-- Optional: 2FA Eingabefeld -->
    <div v-if="is2FARequired" class="form-group">
      <label for="otp">2FA-Code</label>
      <input type="text" id="otp" v-model="otp" placeholder="Gib deinen 2FA-Code ein" />
    </div>

    <div class="action-container">
      <button class="backend-btn" @click="login">Login</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

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

  // Wenn 2FA erforderlich ist, füge den OTP hinzu
  if (is2FARequired.value && otp.value) {
    loginData.otp = otp.value
  }

  try {
    const response = await axios.post('http://localhost:5001/login', loginData, {
      withCredentials: true,  // ermöglicht das Senden von Cookies (wie Session-IDs)
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded', // Formulardaten senden
      }
    })

    console.log(response.data.message)
    alert('Login erfolgreich.')
    localStorage.setItem('isLoggedIn', 'true')  // Loginstatus speichern
    router.push('/sign-pdf')  // Weiterleitung zur nächsten Seite
  } catch (error) {
    console.error('Login fehlgeschlagen', error.response?.data || error)

    // Handhabung von Fehlern je nach Fehlerbeschreibung des Servers
    if (error.response?.data?.error === 'Ungültiges OTP') {
      alert('Der 2FA-Code ist ungültig.')
    } else if (error.response?.data?.error === 'Ungültige E-Mail oder Passwort') {
      alert('Überprüfe deine E-Mail und Passwort.')
    } else {
      alert('Login fehlgeschlagen: ' + (error.response?.data?.error || 'Unbekannter Fehler'))
    }
  }
}
</script>

<style scoped>
  .login-container {
    max-width: 400px;
    margin: 4rem auto;
    padding: 2rem;
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
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
</style>
