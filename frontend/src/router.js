import { createRouter, createWebHistory } from 'vue-router'
import SignPdfView from './views/SignPDF.vue'
import AboutView   from './views/AboutProject.vue'
import Contact     from './views/Contact.vue'
import Download    from './views/Download.vue'
import Login       from './views/Login.vue'
import Profile     from './views/Profile.vue'

const routes = [
  {
    path: '/sign-pdf',
    component: SignPdfView,
    meta: { requiresAuth: true },
  },
  { path: '/about',    component: AboutView },
  { path: '/contact',  component: Contact },
  { path: '/download', component: Download },
  { path: '/login',    component: Login },
  {
    path: '/profile',
    component: Profile,
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Globaler Guard: blockiert geschützte Routen
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  if (to.meta.requiresAuth && !isLoggedIn) {
    // nicht authentifiziert → Login mit optionalem Redirect
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
