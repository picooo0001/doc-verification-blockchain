<template>
  <div class="sign-container">
    <h1>PDF Signieren</h1>
    <p class="subtitle">Lade ein oder mehrere PDF-Dateien hoch, um sie mit der Blockchain zu verknüpfen.</p>

    <div class="p-4">
      <input type="file" accept="application/pdf" multiple @change="handleFileUpload" />

      <div v-if="pdfFiles.length > 0" class="mt-4">
        <p><strong>Vorschau:</strong> {{ pdfFiles[0].name }}</p>
        <iframe :src="pdfUrls[0]" width="100%" height="500px"></iframe>
      </div>
    </div>

    <div class="action-container">
      <button @click="submitToBackend" class="backend-btn">⛓️ Mit Blockchain signieren</button>
    </div>

    <div v-if="pdfFiles.length > 0" class="file-list">
      <h2>Hochgeladene Dateien:</h2>
      <ul>
        <li v-for="(file, index) in pdfFiles" :key="index">{{ file.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const pdfFiles = ref([])
const pdfUrls = ref([])

function handleFileUpload(event) {
  const files = Array.from(event.target.files).filter(file => file.type === 'application/pdf')

  if (files.length === 0) {
    alert('Bitte nur gültige PDF-Dateien auswählen.')
    return
  }

  pdfFiles.value = files
  pdfUrls.value = files.map(file => URL.createObjectURL(file))
}

function signWithBlockchain() {
  if (pdfFiles.value.length === 0) {
    alert('Bitte lade mindestens eine PDF-Datei hoch.')
    return
  }

  console.log('Signiere mit der Blockchain...', pdfFiles.value)
  alert('Das Dokument wurde erfolgreich mit der Blockchain verknüpft!')
}

async function submitToBackend() {
  if (pdfFiles.value.length === 0) {
    alert('Bitte lade mindestens eine PDF-Datei hoch.')
    return
  }

  const formData = new FormData()
  formData.append('file', pdfFiles.value[0]) // nur die erste Datei (kannst du anpassen)
  formData.append('documentId', pdfFiles.value[0].name) // oder z. B. ein eigenes Feld für docId

  try {
    const response = await fetch('http://localhost:5001/api/notarize', {
      method: 'POST',
      body: formData,
      credentials: 'include'
    })

    const result = await response.json()
    if (response.ok) {
      alert(`Erfolgreich signiert! Hash: ${result.txHash}`)
      console.log(result)
    } else {
      alert(`Fehler: ${result.error}`)
    }
  } catch (err) {
    console.error('Fehler beim Senden an Backend:', err)
    alert('Netzwerkfehler')
  }
}

</script>

<style scoped>
:global(body) {
  background-image: url('/Users/meat/doc-verification-blockchain/frontend/pics/blockchain-informationen-flexibel-sicher.1.4.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center center;
  background-attachment: fixed;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* Deine restlichen Styles bleiben unverändert */
.sign-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  color: black;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  text-align: center;
  color: black;
}

.subtitle {
  text-align: center;
  margin-bottom: 2rem;
  color: black;
}

.action-container {
  margin-top: 2rem;
  text-align: center;
}

.backend-btn {
  padding: 0.75rem 1.5rem;
  background-color: #22d3ee;
  color: white;
  font-weight: bold;
  border-radius: 8px;
  text-align: center;
  transition: background-color 0.3s ease, transform 0.2s ease;
  min-width: 200px;
  border: none;
  cursor: pointer;
}

.backend-btn:hover {
  background-color: #6366f1;
  transform: scale(1.02);
}

.file-list {
  margin-top: 1rem;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: #e2e8f0;
}

.file-list h2 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.file-list ul {
  list-style-type: none;
  padding: 0;
}

.file-list li {
  padding: 0.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  margin-bottom: 0.5rem;
  border-radius: 4px;
}
</style>
