
<template>
  <header class="navbar">
    <div class="navbar-content">
      <RouterLink to="/about" class="logo" aria-label="Zur Startseite">
        <img :src="logoOrg" alt="App Logo" />
      </RouterLink>

      <nav class="nav-links" aria-label="Hauptnavigation">
        <RouterLink to="/sign-pdf" class="nav-item" @click="closeMenu">Dashboard</RouterLink>
        <RouterLink to="/about" class="nav-item" @click="closeMenu">About</RouterLink>
        <RouterLink to="/slides" class="nav-item" @click="closeMenu">Slides</RouterLink>
<a href="#" class="nav-item" @click.prevent="handleAdminClick">Admin</a>
            <RouterLink to="" class="nav-item" @click="closeMenu">Get started!</RouterLink>

      </nav>

    <div class="actions">
  <!-- Lupe-Symbol -->
  <button class="search-btn" @click="openSearch" aria-label="Suche">
    <i class="ri-search-line"></i> <!-- Icon für die Lupe -->
  </button>

  <div v-if="isLoggedIn" class="profile-wrapper">
    <button class="profile-btn" @click="toggleDropdown" :aria-expanded="showDropdown" aria-haspopup="true" ref="profileBtnRef">
      <img src="../assets/profile.png" alt="Profil" />
    </button>
    <transition name="dropdown-slide">
      <div v-if="showDropdown" class="dropdown" ref="dropdownRef">
        <RouterLink to="/profile" class="dropdown-item" @click="closeMenu">
          <i class="ri-user-line"></i> Konto
        </RouterLink>
        <a href="#" class="dropdown-item" @click.prevent="logout">
          <i class="ri-logout-box-line"></i> Abmelden
        </a>
      </div>
    </transition>
  </div>
  <RouterLink v-else to="/login" class="trial-btn">Sign in</RouterLink>
</div>


      <button
        class="menu-btn"
        @click="toggleMobileMenu"
        :aria-expanded="mobileMenuOpen"
        aria-label="Menü öffnen/schließen"
      >
        <i class="icon" :class="mobileMenuOpen ? 'ri-close-line' : 'ri-menu-line'"></i>
      </button>
    </div>

    <!-- Mobile Drawer -->
    <transition name="drawer">
      <aside v-if="mobileMenuOpen" class="mobile-drawer" @click.self="closeMenu">
        <nav class="mobile-nav" aria-label="Mobile Navigation">
          <RouterLink to="/sign-pdf" class="nav-item" @click="closeMenu">Dashboard</RouterLink>
          <RouterLink to="/about" class="nav-item" @click="closeMenu">About</RouterLink>
          <div class="mobile-auth">
            <template v-if="isLoggedIn">
              <RouterLink to="/profile" class="nav-item" @click="closeMenu">Konto</RouterLink>
              <a href="#" class="nav-item" @click.prevent="logout">Abmelden</a>
            </template>
            <template v-else>
              <RouterLink to="/login" class="login-btn" @click="closeMenu">Sign in</RouterLink>
            </template>
          </div>
        </nav>
      </aside>
    </transition>
  </header>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import logoOrg from '../assets/logo_orange.png'
import profileSrc from '../assets/profile.png'
import logoPink from '../assets/logo_pink.png'
import { useToast } from 'vue-toastification' 

const toast = useToast() 


const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true')
const showDropdown = ref(false)
const mobileMenuOpen = ref(false)
const router = useRouter()
const dropdownRef = ref(null)
const profileBtnRef = ref(null)

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
  showDropdown.value = false
}

function closeMenu() {
  mobileMenuOpen.value = false
  showDropdown.value = false
}

function logout() {
  localStorage.removeItem('isLoggedIn')
  isLoggedIn.value = false
  router.push('/login')
  closeMenu()
}

function handleClickOutside(event) {
  if (
    showDropdown.value &&
    dropdownRef.value &&
    !dropdownRef.value.contains(event.target) &&
    !profileBtnRef.value.contains(event.target)
  ) {
    showDropdown.value = false
  }
}function handleAdminClick() {
  const isAdmin = localStorage.getItem('isOwner') === 'true'


  if (!isAdmin) {
    toast.warning('Du benötigst Adminrechte, um diesen Bereich zu betreten.', {
      timeout: 3000,
      position: 'bottom-right',
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      style: {
        backgroundColor: '#ffa726',
        color: 'black',
      },
    })
    return // kein Routing!
  }

  // Admin ist erlaubt → navigieren
  router.push('/admin')
}


onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

watch(() => router.currentRoute.value.fullPath, () => {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true'
  closeMenu()
})
</script>

<style>
@import url('https://cdn.jsdelivr.net/npm/remixicon/fonts/remixicon.css');

body {
  background: #fafafd !important;
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.navbar {
  background: #fff !important;
  color: #222 !important;
  width: 100vw;
  border-bottom: 1px solid #eaeaea;
  box-shadow: 0 4px 24px 0 rgba(31, 35, 40, 0.04);
  font-size: 1.08rem;
  font-weight: 500;
  letter-spacing: 0.01em;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-content {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2.5rem;
  height: 68px;
}
.logo img {
  height: 135px;
  margin-right: 0.5rem; /* oder ganz weglassen */
}

.nav-links {
  display: flex;
  gap: 2.2rem;
  align-items: center;
  flex: 1;
}

.nav-item,
.login-btn,
.dropdown-item {
  color: #5e5e5e; /* dunkelgrau */
  font-size: 1.35rem; /* etwas größer */
  font-weight: 500;
  background: none;
  border: none;
  outline: none;
  text-decoration: none;
  border-radius: 0.4rem;
  padding: 0.3rem 0.9rem;
  display: flex;
  align-items: center;
  transition: color 0.18s, background 0.18s;
  position: relative;
}

.nav-item:hover,
.nav-item:focus,
.dropdown-item:hover,
.dropdown-item:focus {
  color: #000 !important;  /* schwarz */
  background: none !important; /* kein Hintergrund */
}
.login-btn {
  background: #222;
  color: #fff;
  border-radius: 0.4rem;
  font-weight: 600;
  padding: 0.3rem 1.2rem;
  margin-left: 0.7rem;
  transition: background 0.18s, color 0.18s;
  box-shadow: 0 2px 8px 0 rgba(31, 35, 40, 0.08);
}
.login-btn:hover,
.login-btn:focus {
  background: #ffffff;
  color: #ffffff;
}

.actions {
  display: flex;
  align-items: center;
  gap: 1.3rem;
}

.profile-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.profile-btn {
  background: none;
  border: none;
  padding: 0;
  border-radius: 50%;
  cursor: pointer;
  outline: none;
  display: flex;
  align-items: center;
}
.profile-btn img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1.5px solid #eaeaea;
  background: #ffffff;
}
.profile-btn:focus img,
.profile-btn:hover img {
  box-shadow: 0 0 0 2px #6c4ae2;
}

.dropdown {
  position: absolute;
  top: 120%;
  right: 0;
  background: #fff;
  box-shadow: 0 8px 32px rgba(31,35,40,0.10);
  min-width: 170px;
  z-index: 200;
  border-radius: 6px;
  overflow: hidden;
  border: 1.5px solid #eaeaea;
}

.menu-btn {
  display: none;
  background: none;
  border: none;
  font-size: 2rem;
  color: #222;
  cursor: pointer;
  z-index: 102;
  border-radius: 50%;
  padding: 0.2em 0.4em;
  transition: background 0.18s, color 0.18s;
}
.menu-btn:focus,
.menu-btn:hover {
  background: #f5f5fa;
  color: #6c4ae2;
}

.mobile-drawer {
  position: fixed;
  top: 0; right: 0; bottom: 0; left: 0;
  background: #fff;
  z-index: 101;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.mobile-nav {
  background: #fff;
  width: 80vw;
  max-width: 340px;
  height: 100vh;
  box-shadow: -8px 0 32px rgba(31,35,40,0.10);
  padding: 3.5rem 2.2rem 2.2rem 2.2rem;
  border-radius: 0;
  display: flex;
  flex-direction: column;
  gap: 2.2rem;
  align-items: flex-start;
}
.mobile-auth {
  margin-top: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  width: 100%;
  align-items: flex-start;
}

@media (max-width: 1200px) {
  .navbar-content {
    max-width: 100vw;
    padding: 0 1.2rem;
  }
}
@media (max-width: 900px) {
  .nav-links {
    gap: 1.1rem;
  }
}
@media (max-width: 768px) {
  .menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .nav-links, .actions {
    display: none;
  }
  .navbar-content {
    height: 60px;
  }
  .logo img {
    height: 32px;
  }
}

/* Überschreibt die Standardfarbe für aktive Router-Links */
.router-link-active,
.router-link-exact-active {
  color: #5e5e5e !important; /* gleiche Farbe wie normaler Link */
  background: none !important; /* kein Hintergrund */
}

/* Nur bei Hover/Fokus soll die Schrift schwarz werden */
.nav-item:hover,
.nav-item:focus,
.dropdown-item:hover,
.dropdown-item:focus {
  color: #111 !important; /* Schwarz bei Hover */
  background: #f5f5fa; /* Heller Hintergrund */
}


.trial-btn {
  background: #1a1726;
  text-decoration: none;
  color: #fff;
  border: 2px solid transparent; /* <-- hier */
  border-radius: 7px;              /* Weniger stark abgerundet */
  padding: 0.7rem 1.7rem;          /* Weniger hoch und schmaler */
  font-size: 1.15rem;              /* Kleinere Schrift */
  font-weight: 700;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  cursor: pointer;
  transition: background 0.18s, transform 0.18s;
  box-shadow: none;
  outline: none;
  display: inline-block;
  letter-spacing: 0.01em;
}

.trial-btn:hover,
.trial-btn:focus {
  background: #ffffff;        /* weißer Hintergrund */
  color: #000000;             /* schwarze Schrift */
  border: 2px solid #000000;  /* schwarzer Rand */
  transform: translateY(-2px) scale(1.03);
}

.search-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.18s, color 0.18s;
}

.search-btn i {
  font-size: 1.4rem;
  color: #5e5e5e;
}

.search-btn:hover,
.search-btn:focus {
  background:none;
  color: #6c4ae2;
}

.search-btn:focus i,
.search-btn:hover i {
  color: #222;
}

</style>
