<template>
    <div class="wallet-login">
      <button @click="loginWithMetaMask">
        Mit MetaMask einloggen
      </button>
      <p v-if="address">Adresse: {{ address }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { ethers } from 'ethers'
  import axios from 'axios'
  
  const address = ref(null)
  const error   = ref(null)
  
  async function loginWithMetaMask() {
    error.value = null
  
    try {
      // 1) MetaMask bereitstellen
      if (!window.ethereum) {
        throw new Error('MetaMask benötigt')
      }
      const provider = new ethers.BrowserProvider(window.ethereum)
      await provider.send('eth_requestAccounts', [])
      const signer = await provider.getSigner()
      const addr   = await signer.getAddress()
      address.value = addr
  
      // 2) Nonce vom Flask-Backend
      const { data: nonceData } = await axios.get('/login/nonce', {
        params: { address: addr }
      })
      const nonce = nonceData.nonce
      if (!nonce) {
        throw new Error('Nonce vom Server nicht erhalten')
      }
  
      // 3) Nachricht signieren
      const signature = await signer.signMessage(nonce)
      if (!signature) {
        throw new Error('Signatur fehlgeschlagen')
      }
  
      // 4) Login per Backend
      const { data: loginData } = await axios.post(
        '/login/wallet',
        { address: addr, signature }
      )
      console.log('Login erfolgreich:', loginData.message)
  
      // 5) Weiterleitung
      window.location.href = '/profile'
    }
    catch (e) {
    console.error('Login error response:', e.response?.data);
    error.value = e.response?.data?.error || e.message;
    }
  }
  </script>
  
  <style scoped>
  .wallet-login {
    margin: 1em 0;
  }
  
  button {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    border-radius: 8px;
    background-color: #22d3ee;
    color: white;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }
  button:hover {
    background-color: #6366f1;
    transform: scale(1.02);
  }
  
  .error {
    color: red;
    margin-top: 0.5rem;
  }
  </style>
  