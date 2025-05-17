<template>
  <div class="admin-panel">
    <h2>Admin Panel</h2>

    <!-- Contract Address anzeigen -->
    <div class="contract-header">
    <p v-if="contractAddress">
      <strong>Contract deployed:</strong>
      <a
        :href="`https://sepolia.etherscan.io/address/${contractAddress}`"
        target="_blank"
      >
        {{ contractAddress }}
      </a>
    </p>
    <button
      v-if="!contractAddress"
      @click="deployContract"
      class="deploy-button"
    >
      Deploy Contract
    </button>
  </div>

    <!-- Benutzerverwaltungstabelle -->
    <table class="user-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Wallet</th>
          <th>Admin</th>
          <th>Aktionen</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id" :class="{ 'owner-row': user.isOwner }">
          <td>{{ user.id }}</td>
          <td>{{ user.email }}</td>
          <td>
            <input
              v-model="user.wallet"
              placeholder="0x..."
              :disabled="user.isOwner"
            />
            <button
              v-if="!user.isOwner"
              @click="updateWallet(user)"
            >
              Speichern
            </button>
          </td>
          <td>{{ user.isAdmin ? 'Ja' : 'Nein' }}</td>
          <td>
            <button
              v-if="!user.isOwner && !user.isAdmin && user.wallet"
              @click="addAdmin(user)"
            >
              Add Admin
            </button>
            <button
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
.admin-panel {
  max-width: 800px;
  margin: 1rem auto;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
.user-table th,
.user-table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
}
.user-table th {
  background: #f5f5f5;
  text-align: left;
}
.user-table input:disabled {
  background: #f0f0f0;
}
.user-table button {
  margin-left: 0.5rem;
}
.owner-row {
  opacity: 0.6;
  pointer-events: none;
}
</style>
