import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'  // Importiere PrimeVue-Konfiguration
import FileUpload from 'primevue/fileupload'  // Importiere FileUpload
import Toast from 'primevue/toast'  // Importiere Toast


const app = createApp(App)

app.use(router)
app.use(PrimeVue, { ripple: true })  // PrimeVue mit Ripple-Effekt aktivieren
app.component('FileUpload', FileUpload)  // FileUpload global registrieren
app.component('Toast', Toast)  // Toast global registrieren

app.mount('#app')
