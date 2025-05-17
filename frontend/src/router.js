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
    path: '/admin',
    component: () => import('@/views/AdminPanel.vue'),
    meta: { requiresAuth: true, requiresOwner: true }
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

router.beforeEach((to, _from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  const isOwner    = localStorage.getItem('isOwner') === 'true'

  console.log('isLoggedIn:', isLoggedIn)
  console.log('isOwner:', isOwner)
  
  if (to.meta.requiresAuth && !isLoggedIn) {
    return next({ path: '/login', query: { redirect: to.fullPath } })
  }

  if (to.meta.requiresOwner && !isOwner) {
    return next('/403')
  }

  next()
})




export default router
