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
      
      <div v-if="stats && !stats.error">
        <p><strong>🧾 Gesamtzahl der Notarisierungen:</strong> {{ stats.total }}</p>
        <p><strong>📅 Erste Notarisierung:</strong> {{ stats.firstDate }}</p>
        <p><strong>🧬 Hash der ersten Notarisierung:</strong> {{ stats.firstHash }}</p>
        <p><strong>📅 Letzte Notarisierung:</strong> {{ stats.latestDate }}</p>
        <p><strong>🧬 Hash der letzten Notarisierung:</strong> {{ stats.latestHash }}</p>
      </div>

      <div v-if="documents && documents.length > 0">
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
              <td>{{ shortenHash(doc.txHash) }}</td>
              <td>{{ shortenHash(doc.documentHash) }}</td>
              <td>
                <!-- Use full backend URL for download and style as clickable link -->
                <a
                  :href="`http://localhost:5001/api/documents/${doc.idHash}/download`"
                  target="_blank"
                  download
                  class="download-link"
                >
                  Download
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p class="dashboard-placeholder">Keine Notarisierungen gefunden.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()
const stats = ref(null)
const pdfFiles = ref([])
const pdfUrls = ref([])
const checkResult = ref(null)
const checkPdfFile = ref(null)
const currentDocumentId = ref(null)
let intervalId = null
const documents = ref([])

// Funktion zum Laden der Statistiken
async function loadStats() {
  try {
    const response = await fetch('http://localhost:5001/api/stats', {
      method: 'GET',
      credentials: 'include'
    })

    if (!response.ok) throw new Error('Fehler beim Laden der Statistiken')

    const data = await response.json()

    const first = data.firstNotarization
    const latest = data.latestNotarization
    let firstDate = '—'
    let firstHash = '—'
    let latestDate = '—'
    let latestHash = '—'

    if (first && first.timestamp) {
      firstDate = new Date(first.timestamp * 1000).toLocaleString()
      firstHash = first.documentHash
    }

    if (latest && latest.timestamp) {
      latestDate = new Date(latest.timestamp * 1000).toLocaleString()
      latestHash = latest.documentHash
    }

    stats.value = {
      total: data.totalNotarizations || 0,
      firstDate,
      firstHash,
      latestDate,
      latestHash
    }
  } catch (err) {
    console.error('Dashboard-Fehler:', err)
    stats.value = { error: 'Fehler beim Laden der Statistiken.' }
  }
}

/// Timestamps formatieren
function formatTimestamp(ts) {
  const date = new Date(ts * 1000)
  return date.toLocaleString()
}

function shortenHash(hash) {
  return `${hash.slice(0, 6)}...${hash.slice(-4)}`
}

// Dokumente laden (angepasst auf /api/documents-Endpoint)
async function loadDocuments() {
  try {
    const res = await fetch('http://localhost:5001/api/documents',
      { method: 'GET', credentials: 'include' }
    )
    if (!res.ok) throw new Error(`Fehler beim Laden der Dokumente: ${res.status}`)
    const data = await res.json()
    documents.value = data.documents.sort((a, b) => b.timestamp - a.timestamp)
  } catch (err) {
    console.error(err)
    toast.error('Konnte Dokumentliste nicht laden: ' + err.message)
  }
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

// Funktion zum Senden der Datei an das Backend zur Signierung

async function submitToBackend() {
  if (pdfFiles.value.length === 0) {
    toast.warning('Bitte lade eine PDF-Datei zum Signieren hoch.')
    return
  }

  const file = pdfFiles.value[0]
  const documentId = file.name
  currentDocumentId.value = documentId

  // Schritt 1: Prüfung auf vorhandene Signatur via /api/verify
  const formDataCheck = new FormData()
  formDataCheck.append('file', file)

  try {
    const verifyRes = await fetch('http://localhost:5001/api/verify', {
      method: 'POST',
      body: formDataCheck,
      credentials: 'include'
    })

    let verifyData = {}
    try {
      verifyData = await verifyRes.json()
    } catch (e) {
      toast.error('Fehler beim Lesen der Prüfantwort.')
      return
    }

    if (verifyRes.ok && verifyData.verified) {
      const date = new Date(verifyData.timestamp * 1000).toLocaleString()
      toast.warning(`Dieses Dokument wurde bereits am ${date} signiert.`)
      return
    }

    // Schritt 2: Datei hochladen & signieren
    const formData = new FormData()
    formData.append('file', file)
    formData.append('documentId', documentId)

    const res = await fetch('http://localhost:5001/api/notarize', {
      method: 'POST',
      body: formData,
      credentials: 'include'
    })

    if (!res.ok) {
      let result = {}
      try {
        result = await res.json()
      } catch (e) {
        toast.error('Serverfehler: Antwort konnte nicht gelesen werden.')
        return
      }

      if (result.error === 'Document already signed') {
        toast.warning('Das Dokument wurde bereits signiert.')
      } else {
        toast.error(result.error || 'Unbekannter Fehler beim Signieren.')
      }
      return
    }

    const result = await res.json()
    toast.success('Dokument erfolgreich signiert!')
    await loadDocuments(currentDocumentId.value)

  } catch (err) {
    console.error('Fehler beim Signieren:', err)
    toast.error('Netzwerkfehler oder Server nicht erreichbar.')
  }
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
    toast.warning('Bitte lade eine PDF-Datei zum Prüfen hoch.');
    return;
  }

  const formData = new FormData();
  formData.append('file', checkPdfFile.value);

  try {
    const response = await fetch('http://localhost:5001/api/verify', {
      method: 'POST',
      body: formData,
      credentials: 'include'
    });

    let result = {};
    try {
      result = await response.json();
    } catch (e) {
      toast.error('Serverantwort konnte nicht gelesen werden.');
      return;
    }

    if (response.ok && result.verified) {
      const date = new Date(result.timestamp * 1000).toLocaleString();
      toast.success(`Dokument wurde am ${date} verifiziert.`);
    } else if (response.status === 404) {
      toast.warning('Dokument nicht in der Blockchain gefunden.');
    } else if (response.status === 403) {
      toast.error('Nicht berechtigt, dieses Dokument zu prüfen.');
    } else {
      toast.error(result.error || 'Unbekannter Fehler bei der Prüfung.');
    }

  } catch (err) {
    console.error('Netzwerkfehler:', err);
    toast.error('Netzwerkfehler oder Server nicht erreichbar.');
  }
}

</script>

<style>
.main-layout {
  display: flex;
  align-items: stretch;
  gap: 2.5rem;
  padding: 3rem 2rem 2rem 2rem;
  min-height: 100vh;
  background: linear-gradient(90deg, #fff 0%, #e7d6fb 35%, #cdb6ec 70%, #eab6d8 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  justify-content: center;
}

.left-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Damit Signieren + Prüfen den gesamten Platz nutzen */
  gap: 2rem;
  width: 40%;
  flex: 1;
}

.dashboard-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  flex-grow: 1;
  justify-content: space-between;
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
