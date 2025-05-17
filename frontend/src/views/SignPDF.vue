<template>
  <div class="main-layout">
    <!-- Linke Spalte -->
    <div class="left-column">
      <!-- PDF Signieren -->
      <div class="sign-container">
        <div class="center-content">
          <h1>PDF Signieren</h1>
        </div>
        <p class="subtitle">Lade ein oder mehrere PDF-Dateien hoch, um sie mit 
der Blockchain zu verknüpfen.</p>
      
        <div class="p-4">
          <input type="file" accept="application/pdf" multiple @change="handleFileUpload" />

          <div v-if="pdfFiles.length > 0" class="mt-4">
            <p><strong>Vorschau:</strong> {{ pdfFiles[0].name }}</p>
            <iframe :src="pdfUrls[0]" width="100%" height="300px"></iframe>
          </div>
        </div>

        <div class="action-container">
          <div class="center-content">
            <button @click="submitToBackend" class="trial-btn">Signieren</button>
          </div>
        </div>
      </div>

      <!-- PDF Prüfen -->
      <div class="check-container">
        <div class="center-content">
          <h1>PDF Prüfen</h1>
        </div>
        <p class="subtitle">Prüfe, ob eine PDF bereits in der Blockchain 
hinterlegt ist.</p>

        <div class="p-4">
          <input type="file" accept="application/pdf" @change="checkPdf" />

          <div class="action-container">
            <div class="center-content">
              <button class="trial-btn" @click="verifyPdf">Prüfen</button>
            </div>
          </div>

          <div v-if="checkResult">
            <p><strong>Ergebnis:</strong> {{ checkResult }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Dashboard -->
    <div class="dashboard-container">
      <div class="center-content">
        <h1>📊 Dashboard</h1>
      </div>
      <p>Statistiken über signierte und überprüfte Dokumente erscheinen hier.</p>
      
      <!-- Statistiken -->
      <div v-if="stats && !stats.error" class="stats">
        <p>
          <strong>🔗 Contract-Adresse:</strong>
          <a
            :href="`https://sepolia.etherscan.io/address/${stats.contractAddress}`"
            target="_blank"
            class="text-blue-600 underline"
          >{{ stats.contractAddress }}</a>
        </p>
        <p v-if="stats.contractCreator">
          <strong>👤 Contract-Creator:</strong>
          <a
            :href="`https://sepolia.etherscan.io/address/${stats.contractCreator}`"
            target="_blank"
            class="text-blue-600 underline"
          >{{ stats.contractCreator }}</a>
        </p>
        <p><strong>📦 Deploy-Block:</strong> {{ stats.deployBlock }}</p>
        <p><strong>🧾 Gesamtzahl der Notarisierungen:</strong> {{ stats.totalNotarizations }}</p>
        <p>
          <strong>🏁 Erste Notarisierung:</strong> {{ stats.firstDate }}
          <code class="ml-2">{{ stats.firstHash }}</code>
        </p>
        <p>
          <strong>🏁 Letzte Notarisierung:</strong> {{ stats.latestDate }}
          <code class="ml-2">{{ stats.latestHash }}</code>
        </p>
      </div>

      <!-- Notarisierungshistorie -->
      <div v-if="documents && documents.length > 0" class="history">
        <h2>🕓 Notarisierungshistorie</h2>
        <table>
          <thead>
            <tr>
              <th>Block</th>
              <th>Zeitpunkt</th>
              <th>Tx Hash</th>
              <th>Dokumentenhash</th>
              <th>Herunterladen</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in documents" :key="doc.idHash">
              <td>{{ doc.blockNumber }}</td>
              <td>{{ formatTimestamp(doc.timestamp) }}</td>
              <!-- hier transactionHash, nicht txHash -->
              <td>{{ shortenHash(doc.txHash) }}</td>
              <!-- hier documentHash -->
              <td>{{ shortenHash(doc.documentHash) }}</td>
              <td>
                <a :href="`http://localhost:5001${doc.downloadUrl}`" target="_blank">
                  Download
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="dashboard-placeholder">
        <p>Keine Notarisierungen gefunden.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useToast } from 'vue-toastification'
import { ethers }        from 'ethers'
import NotaryArtifact     from '@artifacts/Notary.json'
import api from '@/api'

const toast = useToast()
const pdfFiles = ref([])
const pdfUrls = ref([])
const checkResult = ref(null)
const checkPdfFile = ref(null)
const currentDocumentId = ref(null)
const stats = ref({
  contractAddress:    '',
  contractCreator:    '',
  deployBlock:        null,
  totalNotarizations: 0,
  firstDate:          '—',
  firstHash:          '—',
  latestDate:         '—',
  latestHash:         '—',
})
let intervalId = null
const documents = ref([])
const txHash = ref(null)


async function loadStats() {
  try {
    const { data } = await api.get('/stats')
    stats.value = {
      contractAddress:    data.contractAddress,
      contractCreator:    data.contractCreator,
      deployBlock:        data.deployBlock,
      totalNotarizations: data.totalNotarizations || 0,
      firstDate:  data.firstNotarization.timestamp
        ? new Date(data.firstNotarization.timestamp * 1000).toLocaleString()
        : '—',
      firstHash:  data.firstNotarization.documentHash || '—',
      latestDate: data.latestNotarization.timestamp
        ? new Date(data.latestNotarization.timestamp * 1000).toLocaleString()
        : '—',
      latestHash: data.latestNotarization.documentHash || '—',
    }
  } catch (err) {
    console.error('Dashboard-Fehler:', err)
    toast.error('Fehler beim Laden der Statistiken.')
  }
}

async function loadDocuments() {
  try {
    const { data } = await api.get('/documents')
    documents.value = data.documents
      .sort((a, b) => b.timestamp - a.timestamp)
      .map(doc => ({
        ...doc,
        date: new Date(doc.timestamp * 1000).toLocaleString()
      }))
  } catch (e) {
    console.error('Dokument-Fehler:', e)
    toast.error('Konnte Dokumentliste nicht laden.')
  }
}

/// Timestamps formatieren
function formatTimestamp(ts) {
  const date = new Date(ts * 1000)
  return date.toLocaleString()
}

function shortenHash(hash = '') {
  if (typeof hash !== 'string' || hash.length === 0) return '—'
  return `${hash.slice(0,8)}…${hash.slice(-4)}`
}

onMounted(() => {
  loadStats()
  loadDocuments()
  intervalId = setInterval(() => {
    loadStats()
    loadDocuments()
  }, 15000)
})
onUnmounted(() => {
  clearInterval(intervalId)
})

// Funktion zum Hochladen von PDF-Dateien
function handleFileUpload(event) {
  const files = Array.from(event.target.files).filter(file => file.type === 'application/pdf')
  if (files.length === 0) {
    alert('Bitte nur gültige PDF-Dateien auswählen.')
    return
  }
  pdfFiles.value = files
  pdfUrls.value = files.map(file => URL.createObjectURL(file))
}

async function submitToBackend() {
  // ───────────────────────────────────────
  // 0️⃣ Datei vorhanden?
  if (pdfFiles.value.length === 0) {
    toast.warning('Bitte lade eine PDF-Datei zum Signieren hoch.')
    return
  }
  const file       = pdfFiles.value[0]
  const documentId = file.name
  currentDocumentId.value = documentId

  // ───────────────────────────────────────
  // 1️⃣ Hashes vom Backend holen
  let idHash, docHash
  try {
    const form = new FormData()
    form.append('file', file)
    form.append('documentId', documentId)
    const { data: prep } = await api.post('/hashes', form)
    idHash  = prep.idHash
    docHash = prep.docHash
  } catch (err) {
    console.error('Hashes-Endpoint Fehler:', err)
    toast.error(err.response?.data?.error || 'Fehler beim Vorbereiten der Hashes.')
    return
  }

  // ───────────────────────────────────────
  // 2️⃣ MetaMask & Sepolia switch
  if (!window.ethereum) {
    toast.error('MetaMask nicht gefunden.')
    return
  }
  const ethereum = window.ethereum
  try {
    await ethereum.request({ method: 'wallet_switchEthereumChain', params: [{ chainId: '0xaa36a7' }] })
  } catch (err) {
    if (err.code === 4902) {
      // Chain hinzufügen und nochmal switchen
      try {
        await ethereum.request({
          method: 'wallet_addEthereumChain',
          params: [{
            chainId: '0xaa36a7',
            chainName: 'Sepolia Testnetz',
            rpcUrls: ['https://sepolia.infura.io/v3/3bdc1b0ecd9f49fb8da028965c9683cb'],
            nativeCurrency: { name: 'SepoliaETH', symbol: 'SEP', decimals: 18 },
            blockExplorerUrls: ['https://sepolia.etherscan.io'],
          }],
        })
        await ethereum.request({ method: 'wallet_switchEthereumChain', params: [{ chainId: '0xaa36a7' }] })
      } catch (addErr) {
        console.error('Sepolia hinzufügen fehlgeschlagen:', addErr)
        toast.error('Konnte Sepolia nicht hinzufügen.')
        return
      }
    } else {
      console.error('Netzwerkwechsel-Fehler:', err)
      toast.error('Fehler beim Netzwerkwechsel: ' + err.message)
      return
    }
  }

  const provider = new ethers.BrowserProvider(ethereum)
  try {
    await provider.send('eth_requestAccounts', [])
  } catch (err) {
    console.error('Accounts-Request fehlgeschlagen:', err)
    toast.error('Zugriff auf MetaMask-Konten verweigert.')
    return
  }
  const signer     = await provider.getSigner()
  const signerAddr = await signer.getAddress()

  // ───────────────────────────────────────
  // 2.1️⃣ Contract-Address von Backend holen
  let contractAddress
  try {
    const { data } = await api.get('/get_contract_address')
    contractAddress = data.contractAddress
  } catch (err) {
    console.error('Fehler beim Laden der Contract-Adresse:', err)
    toast.error('Konnte Contract-Adresse nicht laden.')
    return
  }

  // ───────────────────────────────────────
  // 3️⃣ Contract-Instanz erstellen
  const contract = new ethers.Contract(
    contractAddress,
    NotaryArtifact.abi,
    signer
  )

  // ───────────────────────────────────────
  // Debug: prüfen, ob die richtigen Werte kommen
  console.log('▶️ verwende Contract @', contractAddress)
  console.log('▶️ orgAdmins[thisAccount] =', await contract.orgAdmins(signerAddr))
  console.log('▶️ notarized[docHash] =', await contract.notarized(docHash))

  // ───────────────────────────────────────
  // 4️⃣ Simulation
  try {
    await provider.call({
      to:   contractAddress,
      from: signerAddr,
      data: contract.interface.encodeFunctionData('notarize', [idHash, docHash]),
    })
    console.log('Simulation OK – kein Revert erwartet.')
  } catch (simErr) {
    console.error('Simulation reverted:', simErr)
    const reason = simErr.reason || simErr.data || simErr.message
    toast.error(`Vorab-Simulation fehlgeschlagen: ${reason}`)
    return
  }

  // ───────────────────────────────────────
  // 5️⃣ On-Chain senden
  let tx
  try {
    toast.info('Sende Transaktion …')
    tx = await contract.notarize(idHash, docHash)
    toast.success(`On-Chain gesendet! TxHash: ${tx.hash.slice(0,10)}…`)
    await tx.wait(1)
  } catch (err) {
    console.error('On-Chain Error:', err)
    const reason = err.reason
                 || (err.message?.includes('execution reverted')
                     ? 'Transaktion abgelehnt oder schon signiert.'
                     : err.message)
    toast.error(reason)
    return
  }

  // ───────────────────────────────────────
  // 6️⃣ DB-Commit
  try {
    await api.post('/notarize/commit', {
      idHash,
      txHash: tx.hash
    })
    toast.success('Dokument in der DB gespeichert.')
  } catch (err) {
    console.error('DB-Commit fehlgeschlagen:', err)
    toast.error('Fehler beim Speichern in der DB.')
    return
  }

  // ───────────────────────────────────────
  // 7️⃣ Historie neu laden
  await loadHistory(currentDocumentId.value)
}

function checkPdf(event) {
  const file = event.target.files[0];
  if (file && file.type === 'application/pdf') {
    checkPdfFile.value = file;  // Datei korrekt zuweisen
  } else {
    toast.warning('Bitte lade eine gültige PDF-Datei hoch.');
  }
}
async function verifyPdf() {
  if (!checkPdfFile.value) {
    toast.warning('Bitte lade eine PDF-Datei zum Prüfen hoch.')
    return
  }
  const verifyForm = new FormData()
  verifyForm.append('file', checkPdfFile.value)
  try {
    const { data: verifyData } = await api.post('/verify', verifyForm)
    if (verifyData.verified) {
      const date = new Date(verifyData.timestamp * 1000).toLocaleString()
      toast.success(`Dokument wurde am ${date} verifiziert.`)
    }
  } catch (e) {
    if (e.response?.status === 404) toast.warning('Dokument nicht in der Blockchain gefunden.')
    else if (e.response?.status === 403) toast.error('Nicht berechtigt, dieses Dokument zu prüfen.')
    else {
      console.error(e)
      toast.error(e.response?.data?.error || 'Unbekannter Fehler bei der Prüfung.')
    }
  }
}

async function loadHistory(documentId) {
  if (!documentId) return
  try {
    // ruft alle Dokument-Events der Organisation ab
    const { data } = await api.get('/documents')
    // filtert nur den Eintrag mit genau dem idHash
    history.value = data.documents.filter(doc => doc.idHash === documentId)
  } catch (err) {
    console.error('Fehler beim Laden der Dokument-Historie:', err)
    toast.error('Dokument-Historie konnte nicht geladen werden.')
  }
}

</script>

<style>
.main-layout {
  display: flex;
  gap: 2.5rem;
  padding: 3rem 2rem 2rem 2rem;
  min-height: 100vh;
  background: linear-gradient(90deg, #fff 0%, #e7d6fb 35%, #cdb6ec 70%, #eab6d8 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  justify-content: center;  /* Zentriert die Container */
  height: 100%; /* Stellt sicher, dass die Layout-Container volle Höhe einnehmen */
}

.left-column {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 40%; /* Linke Spalte */
  max-height: 100%; /* Maximale Höhe für die linke Spalte */
}

.dashboard-container {
  width: 50%; /* Breite des rechten Containers */
  max-height: 100%; /* Maximale Höhe, gleich wie die linke Spalte */
  overflow-y: auto; /* Scrollen erlauben, falls der Inhalt zu groß ist */
}

.sign-container, .check-container, .dashboard-container {
  background: linear-gradient(180deg, #fff 0%, #f6eefd 60%, #f2e4f4 100%);
  border-radius: 6px;
  box-shadow: 0 8px 32px rgba(31, 35, 40, 0.12);
  padding: 2.5rem 2rem 2rem 2rem;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.3rem;
  backdrop-filter: blur(6px);
  transition: box-shadow 0.18s;
  width: 100%; /* Container nimmt volle Breite ein */
}

.sign-container:hover,
.check-container:hover,
.dashboard-container:hover {
  transform: translateY(-5px); 
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dashboard-container {
  width: 50%;
}

h1, h2 {
  color: #232150;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.subtitle {
  font-size: 1.1rem;
  color: #000000;
  margin-bottom: 1.5rem;
}

.p-4 {
  padding: 1rem 0;
}

.action-container {
  margin-top: 1.1rem;
}

.backend-btn {
  background-color: #6c4ae2;
  color: #fff;
  padding: 0.65rem 1.3rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 1.08rem;
  transition: background-color 0.18s, box-shadow 0.18s;
  box-shadow: 0 2px 8px rgba(108,74,226,0.09);
}
.backend-btn:hover {
  background-color: #4d38b0;
}

input[type="file"] {
  background: #f5f5fa;
  color: #232150;
  border: 1px solid #e0c3fc;
  border-radius: 6px;
  padding: 0.55em;
  font-size: 1em;
  width: 100%;
  margin-bottom: 0.8rem;
}

iframe {
  border-radius: 12px;
  border: 1.5px solid #e0c3fc;
  background: #fff;
  margin-top: 0.7rem;
}

.error-msg {
  color: #e24329;
  font-weight: bold;
}

.dashboard-placeholder {
  text-align: center;
  font-size: 1.2rem;
  color: #a2a1a6;
}

hr {
  margin: 1rem 0;
  border: none;
  border-top: 1.5px solid #e0c3fc;
}

ul {
  padding-left: 20px;
}

ul li {
  padding: 1rem;
  border-radius: 10px;
  background-color: #f5f5fa;
  margin-bottom: 1rem;
  box-shadow: 0 1px 4px rgba(31,35,40,0.08);
  color: #232150;
}

ul li p {
  margin: 0.2rem 0;
}

/* Tabellenkopf und Zellen */
table {
  background: none;
  color: #232150;
  border-collapse: collapse;
  width: 100%;
  font-size: 1em;
}
th {
  background: #f5f5fa;
  color: #6c4ae2;
  font-weight: 700;
  padding: 0.6rem;
  border-bottom: 2px solid #e0c3fc;
  text-align: left;
}
td {
  background: none;
  color: #232150;
  border-top: 1px solid #e0c3fc;
  padding: 0.6rem;
  word-break: break-word;
  text-align: left;
}

/* Mobile Styles */
@media (max-width: 900px) {
  .main-layout {
    flex-direction: column;
    padding: 1.2rem;
  }
  .left-column, .dashboard-container {
    width: 100%;
    max-width: 100%;
  }
  h1 {
    font-size: 1.18rem;
  }
  .sign-container,
  .check-container,
  .dashboard-container {
    padding: 1.3rem 0.8rem;
  }
}

.trial-btn {
  background: #1a1726;
  color: #fff;
  border: 2px solid transparent; /* <-- hier */
  border-radius: 7px;              /* Weniger stark abgerundet */
  padding: 0.7rem 1.7rem;          /* Weniger hoch und schmaler */
  font-size: 1.15rem;              /* Kleinere Schrift */
  font-weight: 700;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
"Helvetica Neue", Arial, sans-serif;
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

.center-content {
  display: flex;
  justify-content: center;
  align-items: center; /* vertikal, falls gewünscht */
  width: 100%;
}

.download-link {
  color: var(--link-color);
  text-decoration: underline;
  cursor: pointer;
}
</style>
