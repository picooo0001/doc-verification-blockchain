import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'  
import FileUpload from 'primevue/fileupload'  
import axios from 'axios'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)

axios.defaults.baseURL         = 'http://localhost:5001'
axios.defaults.withCredentials = true

app.use(Toast, {
  position: 'bottom-right',
  timeout: 4000,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  showCloseButtonOnHover: true
})
app.use(router)
app.use(PrimeVue, { ripple: true })
app.component('FileUpload', FileUpload)

// **Diese Zeile löschen!**  
// app.component('Toast', Toast)

app.mount('#app')
