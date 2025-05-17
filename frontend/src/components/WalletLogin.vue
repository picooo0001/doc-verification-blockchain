<template>
  <div class="wallet-login">
    <button class="trial-btn" @click="loginWithMetaMask">
      Mit Wallet einloggen
    </button>
  </div>
</template>

<script setup>
import { ref }       from 'vue'
import { ethers }     from 'ethers'
import api            from '@/api'         
import { useRouter }  from 'vue-router'
import { useToast }   from 'vue-toastification'

const address = ref(null)
const error   = ref(null)
const router  = useRouter()
const toast   = useToast()

async function loginWithMetaMask () {
  error.value = null

  if (!window.ethereum) {
    toast.error('MetaMask fehlt')
    return
  }

  try {
    // Wallet verbinden
    const provider = new ethers.BrowserProvider(window.ethereum)
    await provider.send('eth_requestAccounts', [])
    const signer  = await provider.getSigner()
    const addr    = await signer.getAddress()
    address.value = addr

    // Nonce holen über /api/login/nonce
    const { data: { nonce } } = await api.get('/login/nonce', {
      params: { address: addr }
    })
    if (!nonce) throw new Error('Nonce fehlt')

    // Signatur erzeugen
    const signature = await signer.signMessage(nonce)

    // Wallet-Login über /api/login/wallet
    const { data } = await api.post('/login/wallet', {
      address: addr,
      signature
    })

    const user    = data.user || {}
    const isOwner = Boolean(user.isOwner)

    localStorage.setItem('isLoggedIn',     'true')
    localStorage.setItem('isOwner',        String(isOwner))
    localStorage.setItem('orgId',          String(user.organizationId))
    localStorage.setItem('walletAddress',  user.wallet || '')

    toast.success('Erfolgreich eingeloggt!')
    router.push('/sign-pdf')

  } catch (err) {
    console.error(err)
    toast.error('Fehler beim Einloggen: ' + (err.response?.data?.error || err.message))
  }
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
  border: 2px solid transparent;
  border-radius: 7px;
  padding: 0.7rem 1.7rem;
  font-size: 1.15rem;
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
  background: #ffffff;
  color: #000000;
  border: 2px solid #000000;
  transform: translateY(-2px) scale(1.03);
}
</style>
