<template>
  <div class="sign-container">
    <h1>PDF Signieren</h1>
    <p class="subtitle">Lade ein oder mehrere PDF-Dateien hoch, um sie mit der Blockchain zu verknüpfen.</p>

    <div class="file-upload-wrapper">
      <FileUpload
        name="demo[]"
        url="/api/upload"
        @upload="onAdvancedUpload"
        :multiple="true"
        accept="application/pdf"
        :maxFileSize="1000000"
        :showUploadButton="false"
        :showCancelButton="false"
      >
        <template #empty>
          <div class="upload-placeholder">
            <span>Drag and drop PDFs here to upload</span>
          </div>
        </template>
      </FileUpload>
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

async function submitToBackend() {
  if (pdfFiles.value.length === 0) {
    alert('Bitte lade eine PDF-Datei hoch, um sie zu signieren.')
    return
  }

  const formData = new FormData()
  formData.append("file", pdfFiles.value[0])
  formData.append("documentId", "test-document-id")

  try {
    const response = await fetch("/api/notarize", {
      method: "POST",
      body: formData,
    })

    const data = await response.json()
    if (data.txHash) {
      alert(`Dokument erfolgreich notarisiert! Transaktions-Hash: ${data.txHash}`)
    } else {
      alert('Fehler: ' + data.error)
    }
  } catch (err) {
    alert('Ein Fehler ist aufgetreten: ' + err.message)
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
.p-fileupload-button {
  padding: 0.75rem 1.5rem;
  background-color: #22d3ee;  /* Light blue */
  color: white;
  font-weight: bold;
  border-radius: 8px;
  text-align: center;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.p-fileupload-button:hover {
  background-color: #6366f1;  /* Darker blue on hover */
  transform: scale(1.05);
}

.upload-placeholder {
  text-align: center;
  padding: 2rem;
  color: #94a3b8;
  font-style: italic;
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px dashed #38bdf8;
  border-radius: 8px;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.upload-placeholder:hover {
  background-color: rgba(56, 189, 248, 0.1);
  border-color: #6366f1;
}

/* Glassmorphism Container */
.sign-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.95); /* Weiß mit 85% Deckkraft */
  border-radius: 16px;
  color: black; /* Schriftfarbe auf Schwarz setzen */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* Überschrift */
h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  text-align: center;
  color: black; /* Schriftfarbe auf Schwarz setzen */
}

/* Untertitel */
.subtitle {
  text-align: center;
  margin-bottom: 2rem;
  color: black; /* Schriftfarbe auf Schwarz setzen */
}

/* File Upload Bereich */
.file-upload-wrapper {
  max-width: 300px;
  margin: 0 auto;
}

.p-fileupload {
  width: 100%;
}

.upload-placeholder {
  text-align: center;
  padding: 2rem;
  color: #94a3b8;
  font-style: italic;
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px dashed #38bdf8;
  border-radius: 8px;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.upload-placeholder:hover {
  background-color: rgba(56, 189, 248, 0.1);
  border-color: #6366f1;
}

/* Button Container */
.action-container {
  margin-top: 2rem;
  text-align: center;
}

/* Button Style */
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

/* Liste hochgeladener Dateien */
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

