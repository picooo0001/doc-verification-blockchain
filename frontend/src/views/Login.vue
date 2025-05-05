<!-- src/views/Login.vue -->
<template>
    <div class="login-container">
      <h1>Login</h1>
      <p class="subtitle">Melde dich mit deinen Organisations-Credentials an.</p>
  
      <form @submit.prevent="login">
        <!-- E-Mail / Passwort -->
        <div class="form-group">
          <label for="email">E-Mail</label>
          <input type="email" id="email" v-model="email" placeholder="name@example.com" />
        </div>
  
        <div class="form-group">
          <label for="password">Passwort</label>
          <input type="password" id="password" v-model="password" placeholder="••••••••" />
        </div>
  
        <!-- 2FA-Code, wenn nötig -->
        <div v-if="is2FARequired" class="form-group">
          <label for="otp">2FA-Code</label>
          <input
            type="text" id="otp" v-model="otp"
            placeholder="6-stellig" maxlength="6"
          />
        </div>
  
        <div class="action-container">
          <button class="backend-btn" type="submit">
            {{ is2FARequired ? '2FA prüfen & einloggen' : 'Login' }}
          </button>
        </div>
      </form>
  
      <hr />
  
      <h3>Alternativ: Wallet-Login</h3>
      <WalletLogin />
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  import WalletLogin from '@/components/WalletLogin.vue'
  
  const email = ref('')
  const password = ref('')
  const otp = ref('')
  const is2FARequired = ref(false)
  const router = useRouter()
  
  async function login() {
    if (!email.value || !password.value) {
      alert('Bitte fülle alle Felder aus.')
      return
    }
  
    const payload = { email: email.value, password: password.value }
    if (is2FARequired.value) payload.otp = otp.value
  
    try {
      const res = await axios.post('/login', payload)
      // Backend antwortet entweder mit "2FA erforderlich" oder "Login erfolgreich"
      if (res.data.error === '2FA erforderlich') {
        is2FARequired.value = true
        alert('Bitte gib deinen 2FA-Code ein.')
        return
      }
      // erfolgreich
      router.push('/profile')
    } catch (e) {
      const err = e.response?.data?.error
      if (err === '2FA erforderlich') {
        is2FARequired.value = true
        alert('Bitte gib deinen 2FA-Code ein.')
      } else if (err === 'Ungültiges OTP') {
        alert('Falscher 2FA-Code.')
      } else if (err === 'Ungültige E-Mail oder Passwort') {
        alert('E-Mail oder Passwort falsch.')
      } else {
        alert('Login fehlgeschlagen: ' + (err || e.message))
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
  