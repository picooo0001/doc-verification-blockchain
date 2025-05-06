<template>
    <div class="wallet-login">
        <button class="trial-btn" @click="loginWithMetaMask">
           Mit MetaMask einloggen
       </button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { ethers } from 'ethers'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  
  const address = ref(null)
  const error   = ref(null)
  const router  = useRouter()
  
  async function loginWithMetaMask() {
    error.value = null
    if (!window.ethereum) return error.value = 'MetaMask fehlt'
  
    const provider = new ethers.BrowserProvider(window.ethereum)
    await provider.send('eth_requestAccounts', [])
    const signer = await provider.getSigner()
    const addr   = await signer.getAddress()
    address.value = addr
  
    // 1) Nonce holen
    const { data: { nonce } } = await axios.get('/login/nonce', { params: { address: addr } })
    if (!nonce) throw new Error('Nonce fehlt')
    // 2) Signatur
    const signature = await signer.signMessage(nonce)
    // 3) Login-Request
    await axios.post('/login/wallet', { address: addr, signature })
    // 4) als eingeloggt markieren und weiter
    localStorage.setItem('isLoggedIn','true')
    router.push('/sign-pdf')
  }
  </script>
  
  <style scoped>
    .backend-btn {
    padding: 0.75rem 1.5rem;
    background-color: #22d3ee;
    color: white;
    font-weight: bold;
    font-size: 1.25rem;
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
  