<template>
  <div class="navbar">
    <!-- Container für die Links, wird mittig ausgerichtet -->
    <div class="nav-links">
      <RouterLink to="/sign-pdf" class="nav-link">Sign PDF</RouterLink>
      <div class="logo">
        <img :src="logoSrc" alt="Logo" class="logo-img" />
      </div>
      <RouterLink to="/about" class="nav-link">About</RouterLink>
    </div>
    <!-- Rechter Container für den Login-Button -->
    <div class="auth-container">
      <template v-if="isLoggedIn">
        <span class="logged-in-text">Signed in</span>
        <div class="profile-dropdown" @mouseenter="showDropdown = true" @mouseleave="showDropdown = false">
          <img :src="profileSrc" alt="Profil" class="profile-icon" />
          <div v-if="showDropdown" class="dropdown-menu">
            <RouterLink to="/profile" class="dropdown-item">Konto</RouterLink>
            <a href="#" class="dropdown-item" @click.prevent="logout">Abmelden</a>
          </div>
        </div>
      </template>
      <template v-else>
        <RouterLink to="/login" class="auth-link">Login</RouterLink>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
// use Vite alias @ to load assets in src/assets
import logoSrc from '@/assets/logo.png'
import profileSrc from '@/assets/profile.png'

const router = useRouter()
const showDropdown = ref(false)
const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true')

function logout() {
  localStorage.removeItem('isLoggedIn')
  isLoggedIn.value = false
  router.push('/login')
}

watch(
  () => router.currentRoute.value.fullPath,
  () => {
    isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true'
  }
)
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  background-color: rgba(10, 15, 44, 0.75);
  backdrop-filter: blur(8px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
  border-radius: 16px;
  margin: 2rem auto;
  padding: 0 2rem;
  width: 1000px;
  font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  z-index: 10;
}

.nav-links {
  display: flex;
  gap: 30px;
  align-items: center;
  flex-grow: 1;
  justify-content: center;
}

.logo-img {
  width: 80px;
  height: auto;
  display: block;
}

.nav-link {
  font-size: 1.25rem;
  font-weight: bold;
  text-decoration: none;
  color: #e2e8f0;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(56, 189, 248, 0.1);
}

.router-link-exact-active {
  background-color: rgba(56, 189, 248, 0.3);
  color: #0a0f2c;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
  transition: all 0.3s ease;
}

.auth-container {
  display: flex;
  align-items: center;
}

.auth-link {
  font-size: 1rem;
  font-weight: bold;
  text-decoration: none;
  color: #e2e1e1;
  padding: 0.25rem 0.75rem;
  border-radius: 8px;
  background-color: #22d3ee;
  transition: background-color 0.3s ease;
}

.auth-link:hover {
  background-color: #4f46e5;
}

.logged-in-text {
  color: #e2e1e1;
  margin-right: 0.5rem;
  font-size: 0.8rem;
}

.profile-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
}

.profile-dropdown {
  position: relative;
  display: flex;
  align-items: center;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #1e293b;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 0.5rem 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  z-index: 20;
  min-width: 120px;
}

.dropdown-item {
  display: block;
  padding: 0.5rem 1rem;
  color: #e2e8f0;
  text-decoration: none;
  font-size: 0.85rem;
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background-color: #334155;
}
</style>
