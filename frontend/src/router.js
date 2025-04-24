import { createRouter, createWebHistory } from 'vue-router'
import SignPdfView from './views/SignPDF.vue'
import AboutView from './views/AboutProject.vue'

const routes = [
  { path: '/sign-pdf', component: SignPdfView }, 
  { path: '/about', component: AboutView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
