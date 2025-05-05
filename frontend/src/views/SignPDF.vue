<template>
  <div class="main-layout">
    <!-- Linke Spalte -->
    <div class="left-column">
      <!-- PDF Signieren -->
      <div class="sign-container">
        <h1>PDF Signieren</h1>
        <p class="subtitle">Lade ein oder mehrere PDF-Dateien hoch, um sie mit der Blockchain zu verknüpfen.</p>

        <div class="p-4">
          <input type="file" accept="application/pdf" multiple @change="handleFileUpload" />

          <div v-if="pdfFiles.length > 0" class="mt-4">
            <p><strong>Vorschau:</strong> {{ pdfFiles[0].name }}</p>
            <iframe :src="pdfUrls[0]" width="100%" height="300px"></iframe>
          </div>
        </div>

        <div class="action-container">
          <button @click="submitToBackend" class="backend-btn">⛓️ Mit Blockchain signieren</button>
        </div>
      </div>

      <!-- PDF Prüfen -->
      <div class="check-container">
        <h1>PDF Prüfen</h1>
        <p class="subtitle">Prüfe, ob eine PDF bereits in der Blockchain hinterlegt ist.</p>

        <div class="p-4">
          <input type="file" accept="application/pdf" @change="checkPdf" />

          <div class="action-container">
            <button class="backend-btn" @click="verifyPdf">✅ Prüfen</button>
          </div>

          <div v-if="checkResult">
            <p><strong>Ergebnis:</strong> {{ checkResult }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Dashboard -->
    <div class="dashboard-container">
      <h1>📊 Dashboard</h1>
      <p>Statistiken über signierte und überprüfte Dokumente erscheinen hier.</p>
      <div v-if="stats && !stats.error">
        <p><strong>🧾 Gesamtzahl der Signaturen:</strong> {{ stats.total }}</p>
        <p><strong>📅 Letzte Signatur:</strong> {{ stats.latestDate }}</p>
        <p><strong>🧬 Hash:</strong> {{ stats.latestHash }}</p>
      </div>

      <!-- Notarisierungshistorie -->
      <div v-if="history && history.length > 0">
        <h2>🕓 Notarisierungshistorie</h2>
        <table style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr style="background-color: #f0f0f0;">
              <th style="text-align: left; padding: 0.5rem;">Block</th>
              <th style="text-align: left; padding: 0.5rem;">Zeitpunkt</th>
              <th style="text-align: left; padding: 0.5rem;">Tx Hash</th>
              <th style="text-align: left; padding: 0.5rem;">Dokumentenhash</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entry, index) in history" :key="index" style="border-top: 1px solid #ddd;">
              <td style="padding: 0.5rem;">{{ entry.blockNumber }}</td>
              <td style="padding: 0.5rem;">{{ formatTimestamp(entry.timestamp) }}</td>
              <td style="padding: 0.5rem; overflow-wrap: break-word;">{{ entry.txHash }}</td>
              <td style="padding: 0.5rem; overflow-wrap: break-word;">{{ entry.documentHash }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>Keine Historie gefunden.</p>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'

const stats = ref(null)
const pdfFiles = ref([])
const pdfUrls = ref([])
const checkResult = ref(null)
const checkPdfFile = ref(null)
const documentId = ref(null)  // Variable für die Dokument-ID, die beim Signieren zurückgegeben wird
const history = ref([])  // Variable für die Notarisierungshistorie

// Funktion zum Laden der Statistiken
async function loadStats() {
  try {
    const response = await fetch('http://localhost:5001/api/stats', {
      method: 'GET',
      credentials: 'include'
    })

    if (!response.ok) throw new Error('Fehler beim Laden der Statistiken')

    const data = await response.json()

    const latest = data.latestNotarization
    let latestDate = '—'
    let latestHash = '—'

    if (latest && latest.timestamp) {
      latestDate = new Date(latest.timestamp * 1000).toLocaleString()
      latestHash = latest.documentHash
    }

    stats.value = {
      total: data.totalNotarizations || 0,
      latestDate,
      latestHash,
      timestamps: data.timestamps || []
    }

  } catch (err) {
    console.error('Dashboard-Fehler:', err)
    stats.value = { error: 'Fehler beim Laden der Statistiken.' }
  }
}

// Funktion zum Laden der Notarisierungshistorie für ein Dokument
// Funktion zum Laden der Notarisierungshistorie für ein Dokument
async function loadHistory(documentId) {
  try {
    const res = await fetch(`http://localhost:5001/api/documents/${documentId}/history`, {
      credentials: 'include'
    })
    if (!res.ok) throw new Error('Fehler beim Laden der Notarisierungshistorie')
    const data = await res.json()
    console.log('History:', data)
    history.value = data // ✅ Hier fehlte die Zuweisung
  } catch (err) {
    console.error('Fehler beim Laden der Historie:', err)
  }
}

// Funktion zur Formatierung des Timestamps
function formatTimestamp(ts) {
  const date = new Date(ts * 1000)
  return date.toLocaleString()
}



onMounted(() => {
  loadStats()
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
const currentDocumentId = ref(null)

async function submitToBackend() {
  const file = pdfFiles.value[0]
  const documentId = file.name   // oder eine UUID etc.
  currentDocumentId.value = documentId

  const formData = new FormData()
  formData.append('file', file)
  formData.append('documentId', documentId)

  const res = await fetch('http://localhost:5001/api/notarize', {
    method: 'POST',
    body: formData,
    credentials: 'include'
  })

  const result = await res.json()

  if (res.ok) {
    alert('Erfolgreich signiert')
    await loadHistory(currentDocumentId.value)
  } else {
    alert(result.error)
  }
}




// Funktion zum Prüfen von PDFs
function checkPdf(event) {
  checkPdfFile.value = event.target.files[0]
}

// Funktion zur Verifikation des PDFs
async function verifyPdf() {
  if (!checkPdfFile.value) {
    alert('Bitte lade eine PDF-Datei zum Prüfen hoch.')
    return
  }

  const formData = new FormData()
  formData.append('file', checkPdfFile.value)

  try {
    const response = await fetch('http://localhost:5001/api/verify', {
      method: 'POST',
      body: formData,
      credentials: 'include'
    })

    const result = await response.json()

    if (response.ok && result.verified) {
      const date = new Date(result.timestamp * 1000).toLocaleString()
      checkResult.value = `✅ Dokument wurde am ${date} verifiziert.`
    } else if (response.status === 404) {
      checkResult.value = '❌ Dokument nicht in der Blockchain gefunden.'
    } else if (response.status === 403) {
      checkResult.value = '⛔ Nicht berechtigt, dieses Dokument zu prüfen.'
    } else {
      checkResult.value = '❌ Unbekannter Fehler bei der Prüfung.'
    }

  } catch (err) {
    console.error('Fehler beim Prüfen:', err)
    checkResult.value = '🌐 Netzwerkfehler oder Server nicht erreichbar.'
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.left-column {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 50%; /* Linksbereich hat nun 50% der Breite */
}

.left-column > div {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  background-color: rgba(255, 255, 255, 0.9); /* Gleicher Hintergrund wie im rechten Container */
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Gleicher Schatten wie im rechten Container */
}

.dashboard-container {
  width: 50%; /* Dashboard Container nimmt 50% der Breite ein */
  background-color: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

h1 {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1rem;
  color: #555;
  margin-bottom: 1.5rem;
}

.p-4 {
  padding: 1rem;
}

.action-container {
  margin-top: 1rem;
}

.backend-btn {
  background-color: #4CAF50;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.backend-btn:hover {
  background-color: #45a049;
}

iframe {
  border-radius: 8px;
  border: 1px solid #ddd;
}

.error-msg {
  color: red;
  font-weight: bold;
}

.dashboard-placeholder {
  text-align: center;
  font-size: 1.2rem;
  color: #888;
}

hr {
  margin: 1rem 0;
}

ul {
  padding-left: 20px;
}

ul li {
  padding: 1rem;
  border-radius: 8px;
  background-color: #f7f7f7;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

ul li p {
  margin: 0.2rem 0;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .main-layout {
    flex-direction: column;
    padding: 1rem;
  }
  
  .left-column, .dashboard-container {
    width: 100%;
    max-width: 100%;
  }

  h1 {
    font-size: 1.2rem;
  }
}
</style>
