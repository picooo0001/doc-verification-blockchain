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

function onAdvancedUpload(event) {
  console.log('Upload Event:', event)
  pdfFiles.value = event.files
}

function signWithBlockchain() {
  if (pdfFiles.value.length === 0) {
    alert('Bitte lade eine PDF-Datei hoch, um sie zu signieren.')
    return
  }

  console.log('Signiere mit der Blockchain...', pdfFiles.value)
  alert('Das Dokument wurde erfolgreich mit der Blockchain verknüpft!')
}

function submitToBackend() {
  console.log('Sende Daten ans Backend...');
}
</script>

<style scoped>
/* Neuer Hintergrund für die gesamte Seite */
:global(body) {
  background-color: #f5f7ff;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* Container */
.sign-container {
  max-width: 700px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Überschrift */
h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  text-align: center;
}

/* Untertitel */
.subtitle {
  text-align: center;
  margin-bottom: 2rem;
  color: #666;
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
  color: #888;
  font-style: italic;
}

/* Button Container */
.action-container {
  margin-top: 2rem;
  text-align: center;
}

/* Button Style */
.backend-btn {
  flex: 1 1 auto;
  padding: 0.75rem 1.5rem;
  background-color: #4f46e5; /* Indigo */
  color: white;
  font-weight: bold;
  border-radius: 8px;
  text-align: center;
  transition: background-color 0.3s ease;
  min-width: 200px;
  border: none;
  cursor: pointer;
}

.backend-btn:hover {
  background-color: #6366f1;
}

/* Liste hochgeladener Dateien */
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
