<template>
  <div class="main-layout">
    <div class="admin-panel">
      <h2>Admin Panel</h2>

      <!-- Vertragsinformationen -->
      <div class="contract-header" v-if="contractAddress" style="display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="display: inline-block; width: 180px; font-weight: bold;">
            Contract deployed on:
          </span>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="background-color: #f0f0f0; padding: 4px 8px; border-radius: 4px; font-family: monospace;">
              Sepolia Testnet
            </span>
            <img src="../assets/sepolia.png" alt="Sepolia Logo" style="width: 28px; height: 28px;" />
          </div>
        </div>

        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="display: inline-block; width: 180px; font-weight: bold;">
            with Contract Address:
          </span>
          <span style="background-color: #f0f0f0; padding: 4px 8px; border-radius: 4px; font-family: monospace; min-width: 300px; color: #000000;">
            <a
              :href="`https://sepolia.etherscan.io/address/${contractAddress}`"
              target="_blank"
              style="text-decoration: none; color: #000000;"
            >
              {{ contractAddress }}
            </a>
          </span>
          <button
            @click="copyToClipboard"
            style="background: none; border: none; padding: 0; cursor: pointer;"
            title="Copy address"
            aria-label="Copy contract address"
          >
            <img src="../assets/copy.svg" alt="Copy Icon" style="width: 20px; height: 20px;" />
          </button>
        </div>
      </div>

      <!-- Deploy Contract Button -->
      <button v-if="!contractAddress" @click="deployContract" class="trial-btn">
        Deploy Contract
      </button>

      <!-- Benutzerverwaltungstabelle -->
      <table class="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th class="email-col">Email</th>
            <th class="wallet-col">Wallet</th>
            <th>Admin</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" :class="{ 'owner-row': user.isOwner }">
            <td>{{ user.id }}</td>
            <td class="email-col">{{ user.email }}</td>
            <td class="wallet-col">
              <div style="display: flex; align-items: center; gap: 8px;">
                <input
                  v-model="user.wallet"
                  placeholder="0x..."
                  :disabled="user.isOwner"
                  class="wallet-input"
                />
                <button
                  class="trial-btn2"
                  v-if="!user.isOwner"
                  @click="updateWallet(user)"
                >
                  Speichern
                </button>
              </div>
            </td>
            <td>{{ user.isAdmin ? 'Ja' : 'Nein' }}</td>
            <td >
              <button
                class="trial-btn1"
                v-if="!user.isOwner && !user.isAdmin && user.wallet"
                @click="addAdmin(user)"
              >
                Add Admin
              </button>
              <button
                class="trial-btn1"
                v-else-if="!user.isOwner && user.isAdmin"
                @click="removeAdmin(user)"
              >
                Remove Admin
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import NotaryArtifact from '@artifacts/Notary.json'
import { ethers } from 'ethers'
import { useToast } from 'vue-toastification'

const toast = useToast()

// Reactive state
const orgId = ref(null)
const contractAddress = ref(null)
const users = ref([])

// Lädt Contract-Adresse und Org-ID der aktuellen Organisation
async function loadContractAddress() {
  try {
    const { data } = await api.get('/get_contract_address')
    contractAddress.value = data.contractAddress
    // falls die Route schon die Org-ID mitliefert
    orgId.value         = data.organization_id || data.orgId || null

  } catch (err) {
    // Wenn kein Contract hinterlegt ist, hol nur die Org-ID
    if (err.response?.status === 404) {
      try {
        const { data: orgData } = await api.get('/get_org_id')
        orgId.value = orgData.organization_id
        contractAddress.value = null
      } catch (e2) {
        console.error('Org-ID holen fehlgeschlagen:', e2)
        toast.error('Fehler beim Laden der Organisation.')
      }
    } else {
      console.error('Konnte Contract-Adresse nicht laden:', err)
      toast.error('Fehler beim Laden der Contract-Adresse.')
    }
  }
}

function copyToClipboard() {
  if (!contractAddress.value) return

  navigator.clipboard.writeText(contractAddress.value)
    .then(() => {
      // Toast oder alert bei Erfolg
      toast.success('Copied to clipboard!')
    })
    .catch((err) => {
      toast.error('Failed to copy contract address.')
      console.error('Copy error:', err)
    })
}


// Lädt alle Nutzer für die aktuelle Organisation
async function loadUsers() {
  if (!orgId.value) {
    console.error('Keine gültige Org-ID vorhanden')
    toast.error('Organisation nicht definiert. Bitte neu laden.')
    return
  }
  try {
    const { data } = await api.get(`/orgs/${orgId.value}/users`)
    // Mappe und initialisiere Flags: isOwner aus DB, isAdmin via Contract
    const fetched = data.users.map(u => ({
      ...u,
      isOwner: u.is_owner || false,
      isAdmin: false
    }))
    // Prüfe Admin-Status on-chain
    if (window.ethereum && contractAddress.value) {
      const provider = new ethers.BrowserProvider(window.ethereum)
      try {
        await provider.send('wallet_switchEthereumChain', [{ chainId: '0xaa36a7' }])
      } catch {}
      const contract = new ethers.Contract(
        contractAddress.value,
        NotaryArtifact.abi,
        provider
      )
      for (const u of fetched) {
        if (u.wallet) {
          try {
            u.isAdmin = await contract.orgAdmins(u.wallet)
          } catch {
            u.isAdmin = false
          }
        }
      }
    }
    users.value = fetched
  } catch (e) {
    console.error('Fehler beim Laden der Nutzer:', e)
    toast.error('Fehler beim Laden der Nutzer.')
  }
}

// Aktualisiert Wallet-Adresse eines Nutzers via API
async function updateWallet(user) {
  if (user.isOwner) {
    return toast.info('Owner kann nicht bearbeitet werden.')
  }
  try {
    const { data } = await api.put(`/users/${user.id}/wallet`, { wallet: user.wallet })
    toast.success(`Wallet aktualisiert: ${data.wallet}`)
  } catch (e) {
    console.error('Wallet-Update fehlgeschlagen:', e)
    toast.error(e.response?.data?.error || 'Fehler beim Speichern der Wallet.')
  }
}

// Fügt einen Nutzer als Org-Admin on-chain hinzu
async function addAdmin(user) {
  if (user.isOwner) return toast.info('Owner kann kein Admin hinzugefügt werden.')
  if (!user.wallet) return toast.error('Dieser User hat keine Wallet-Adresse.')
  if (!contractAddress.value) return toast.error('Keine Contract-Adresse bekannt.')

  if (!window.ethereum) return toast.error('MetaMask nicht gefunden.')
  const provider = new ethers.BrowserProvider(window.ethereum)
  try {
    await provider.send('wallet_switchEthereumChain', [{ chainId: '0xaa36a7' }])
  } catch {}
  await provider.send('eth_requestAccounts', [])
  const signer = await provider.getSigner()
  const contract = new ethers.Contract(
    contractAddress.value,
    NotaryArtifact.abi,
    signer
  )

  try {
    const tx = await contract.addOrgAdmin(user.wallet)
    toast.info(`Tx gesendet: ${tx.hash.slice(0,10)}…`)
    await tx.wait(1)
    user.isAdmin = true
    toast.success(`Admin ${user.wallet} wurde hinzugefügt!`)
  } catch (err) {
    console.error('addAdmin Error:', err)
    toast.error(err.reason || err.message || 'Transaktion fehlgeschlagen.')
  }
}

// Entfernt einen Org-Admin on-chain
async function removeAdmin(user) {
  if (user.isOwner) return toast.info('Owner kann nicht entfernt werden.')
  if (!user.wallet) return toast.error('Dieser User hat keine Wallet-Adresse.')
  if (!contractAddress.value) return toast.error('Keine Contract-Adresse bekannt.')

  if (!window.ethereum) return toast.error('MetaMask nicht gefunden.')
  const provider = new ethers.BrowserProvider(window.ethereum)
  try {
    await provider.send('wallet_switchEthereumChain', [{ chainId: '0xaa36a7' }])
  } catch {}
  await provider.send('eth_requestAccounts', [])
  const signer = await provider.getSigner()
  const contract = new ethers.Contract(
    contractAddress.value,
    NotaryArtifact.abi,
    signer
  )

  try {
    const tx = await contract.removeOrgAdmin(user.wallet)
    toast.info(`Tx gesendet: ${tx.hash.slice(0,10)}…`)
    await tx.wait(1)
    user.isAdmin = false
    toast.success(`Admin ${user.wallet} wurde entfernt!`)
  } catch (err) {
    console.error('removeAdmin Error:', err)
    toast.error(err.reason || err.message || 'Transaktion fehlgeschlagen.')
  }
}

// Lifecycle hook
onMounted(async () => {
  await loadContractAddress()
  await loadUsers()
})

// Deploy Contract on-chain
async function deployContract() {
  if (!window.ethereum) {
    return toast.error('MetaMask nicht gefunden.')
  }
  const provider = new ethers.BrowserProvider(window.ethereum)
  try { await provider.send('wallet_switchEthereumChain', [{ chainId: '0xaa36a7' }]) } catch {}
  await provider.send('eth_requestAccounts', [])
  const signer     = await provider.getSigner()
  const signerAddr = await signer.getAddress()

  // Sicherstellen, dass nur der Owner deployen kann
  const owner = users.value.find(u => u.isOwner)
  if (!owner) {
    return toast.error('Owner nicht gefunden.')
  }
  if (signerAddr.toLowerCase() !== owner.wallet.toLowerCase()) {
    return toast.error('Nur der Organization-Owner darf den Contract deployen.')
  }

  // Constructor erwartet genau einen Parameter: owner-Adresse
  const factory   = new ethers.ContractFactory(
    NotaryArtifact.abi,
    NotaryArtifact.bytecode,
    signer
  )

  try {
    toast.info('Deploying Contract…')
    const contract = await factory.deploy(signerAddr)
    await contract.waitForDeployment()
    const tx         = contract.deploymentTransaction()
    const receipt    = await tx.wait()
    const deployBlock= receipt.blockNumber

    contractAddress.value = contract.target
    // Speichere nur einmal
    await api.post(`/orgs/${orgId.value}/contract`, {
      contractAddress: contract.target,
      deployBlock
    })

    toast.success(`Contract deployed: ${contract.target} (Block ${deployBlock})`)
    await loadUsers()
  } catch (e) {
    console.error('Deploy fehlgeschlagen:', e)
    toast.error(e.message || 'Deploy fehlgeschlagen.')
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

.admin-panel {
  width: 70%;
  max-width: 2000px; /* vorher 1800px → jetzt realistischer breiter */
  margin: 1rem auto;
  padding: 1rem;
  background: linear-gradient(180deg, #fff 0%, #f6eefd 60%, #f2e4f4 100%);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  color: #000000;
}


.admin-panel h2 {
  font-size: 2.5rem; /* viel größer */
  font-weight: 700;
  color: #000000;
  margin-bottom: 1rem;
}

.user-table {
  width: 99%;
  margin: 2rem auto 0 auto; /* Oben 2rem, unten 0, links und rechts auto für Zentrierung */
  border-collapse: collapse;
  font-size: 14px;
  background-color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-radius: 6px;
  overflow: hidden;
  color: #000000;
}
.user-table th.email-col,
.user-table td.email-col {
  width: 200px; /* etwas schmaler */
}

.user-table th.wallet-col,
.user-table td.wallet-col {
  width: 600px; /* etwas breiter */
}


.user-table th,
.user-table td {
  text-align: left;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: middle;
  color: #000000; /* schwarz */
}

.user-table thead {
  background-color: #f3f4f6;
}

.user-table th {
  font-weight: 600;
  color: #000000; /* Header schwarz */
}

.user-table tr:last-child td {
  border-bottom: none;
}

.user-table input {
  padding: 0.4rem 0.6rem;
  font-size: 1.1rem; /* Input Schriftgröße auch größer */
  border: 1px solid #d1d5db;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
  color: #000000;
}

.user-table .trial-btn {
  margin-top: 0.5rem;
}


.trial-btn {
  background: #1a1726;
  color: #fff;
  border: 1px solid transparent;
padding: 0.2rem 0.5rem;
  font-size: 0.85rem;
  border-radius: 3px;
  font-weight: 600;
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
  border: 1px solid #000000;
  transform: translateY(-1px) scale(1.02);
}

.wallet-display {
  background-color: #f0f0f0;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: monospace;
  min-width: 200px;
  font-size: 0.5rem;
}
.wallet-input {
  font-size: 14px !important;   /* oder z.B. 12px */
  width: 400px;
  max-width: 360px;
  padding: 4px 6px;
  height: 28px;
  box-sizing: border-box;
  color: #000000;
}
.trial-btn1 {
  background: #1a1726;
  color: #fff;
  border: 1px solid transparent;
  font-size: 0.8rem;        /* etwas größere Schrift im Button */
  padding: 0.3rem 1rem;     /* breiterer Button */
  min-width: 110px;          /* Mindestbreite für Breite */
  display: inline-block;
  border-radius: 3px;
  font-weight: 600;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  cursor: pointer;
  transition: background 0.18s, transform 0.18s;
  box-shadow: none;
  outline: none;
  letter-spacing: 0.01em;
 
}

.trial-btn1:hover,
.trial-btn1:focus {
  background: #ffffff;
  color: #000000;
  border: 1px solid #000000;
  transform: translateY(-1px) scale(1.02);
}

.trial-btn2 {
  background: #1a1726;
  color: #fff;
  border: 1px solid transparent;
  font-size: 0.8rem;        /* etwas größere Schrift im Button */
  padding: 0.3rem 1rem;     /* breiterer Button */
  min-width: 100px;          /* Mindestbreite für Breite */
  display: inline-block;
  border-radius: 3px;
  font-weight: 600;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  cursor: pointer;
  transition: background 0.18s, transform 0.18s;
  box-shadow: none;
  outline: none;
  letter-spacing: 0.01em;
 
}

.trial-btn2:hover,
.trial-btn2:focus {
  background: #ffffff;
  color: #000000;
  border: 1px solid #000000;
  transform: translateY(-1px) scale(1.02);
}


</style>
