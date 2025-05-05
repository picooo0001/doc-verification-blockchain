// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'
import FileUpload from 'primevue/fileupload'
import Toast from 'primevue/toast'
import axios from 'axios'

// MetaMask-Auth: alle Requests gehen an Flask und senden das Session‐Cookie mit
axios.defaults.baseURL        = 'http://localhost:5001'
axios.defaults.withCredentials = true

const app = createApp(App)

app.use(router)
app.use(PrimeVue, { ripple: true })
app.component('FileUpload', FileUpload)
app.component('Toast', Toast)

app.mount('#app')
