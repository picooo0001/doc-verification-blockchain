import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'  // Importiere PrimeVue-Konfiguration
import FileUpload from 'primevue/fileupload'  // Importiere FileUpload
import axios from 'axios'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)

axios.defaults.baseURL         = 'http://localhost:5001'
axios.defaults.withCredentials = true

app.use(Toast, {
    position: 'top-right',
    timeout: 4000,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    showCloseButtonOnHover: true
  })
app.use(router)
app.use(PrimeVue, { ripple: true })  // PrimeVue mit Ripple-Effekt aktivieren
app.component('FileUpload', FileUpload)  // FileUpload global registrieren
app.component('Toast', Toast)  // Toast global registrieren

app.mount('#app')
