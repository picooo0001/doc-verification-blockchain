import { createRouter, createWebHistory } from 'vue-router'
import SignPdfView from './views/SignPDF.vue'
import AboutView from './views/AboutProject.vue'
import Contact from './views/Contact.vue'
import Download from './views/download.vue'
import Login from './views/Login.vue'

const routes = [
  { path: '/sign-pdf', component: SignPdfView }, 
  { path: '/about', component: AboutView },
  {path: '/contact', component: Contact},
  {path: '/download', component: Download},
  {path: '/login', component: Login}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
