<template>
  <div class="sign-container">
    <h1>PDF Signieren</h1>
    <p class="subtitle">Lade ein oder mehrere PDF-Dateien hoch, um sie mit der Blockchain zu verknüpfen.</p>

    <FileUpload
      name="demo[]"
      url="/api/upload"
      @upload="onAdvancedUpload"
      :multiple="true"
      accept="application/pdf"
      :maxFileSize="1000000"
    >
      <template #empty>
        <div class="upload-placeholder">
          <span>Drag and drop PDFs here to upload</span>
        </div>
      </template>
    </FileUpload>

    <!-- Button wird nur angezeigt, wenn PDF-Dateien hochgeladen wurden -->
    <div v-if="pdfFiles.length > 0" class="action-container">
      <button @click="signWithBlockchain" class="sign-button">Mit Blockchain signieren</button>
    </div>

    <!-- Optional: Liste der hochgeladenen Dateien anzeigen -->
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

function onAdvancedUpload(event) {
  console.log('Upload Event:', event)
  pdfFiles.value = event.files // Speichert die hochgeladenen PDF-Dateien
}

function signWithBlockchain() {
  if (pdfFiles.value.length === 0) {
    alert('Bitte lade eine PDF-Datei hoch, um sie zu signieren.')
    return
  }

  console.log('Signiere mit der Blockchain...', pdfFiles.value)
  // Hier kommt die Logik für das Signieren mit der Blockchain
  // Zum Beispiel einen Hash der Datei berechnen und an einen Smart Contract senden
  alert('Das Dokument wurde erfolgreich mit der Blockchain verknüpft!')
}
</script>

<style scoped>
.sign-container {
  max-width: 700px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  text-align: center;
  margin-bottom: 2rem;
  color: #666;
}

.upload-placeholder {
  text-align: center;
  padding: 2rem;
  color: #888;
  font-style: italic;
}

.action-container {
  margin-top: 2rem;
  text-align: center;
}

.sign-button {
  background-color: #007bff;
  color: white;
  padding: 1rem 2rem;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.sign-button:hover {
  background-color: #0056b3;
}

.file-list {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 8px;
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
  background-color: #e9e9e9;
  margin-bottom: 0.5rem;
  border-radius: 4px;
}
</style>
