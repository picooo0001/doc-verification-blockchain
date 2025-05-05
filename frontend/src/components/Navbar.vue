<template>
  <div class="navbar">
    <!-- Container für die Links, wird mittig ausgerichtet -->
    <div class="nav-links">
      <RouterLink to="/sign-pdf" class="nav-link">Sign PDF</RouterLink>
      <div class="logo">
        <img src="/Users/meat/doc-verification-blockchain/frontend/pics/logo.png" alt="Logo" class="logo-img" />
      </div>
      <RouterLink to="/about" class="nav-link">About</RouterLink>
    </div>
    <!-- Rechter Container für den Login-Button -->
    <div class="auth-container">
      <template v-if="isLoggedIn">
        <div class="profile-dropdown" @mouseenter="showDropdown = true" @mouseleave="showDropdown = false">
          <img src="/Users/meat/doc-verification-blockchain/frontend/pics/profile.png" alt="Profil" class="profile-icon" />
          <div v-if="showDropdown" class="dropdown-menu">
            <RouterLink to="/profile" class="dropdown-item">Konto</RouterLink>
            <a href="#" class="dropdown-item" @click.prevent="logout">Abmelden</a>
          </div>
        </div>
        <span class="logged-in-text">Signed in</span>
      </template>
      <template v-else>
        <RouterLink to="/login" class="auth-link">Login</RouterLink>
      </template>
    </div>
  </div>
</template>

<script>
import image from '/Users/meat/doc-verification-blockchain/frontend/pics/logo.png';
import image1 from '/Users/meat/doc-verification-blockchain/frontend/pics/profile.png';

export default {
  data() {
    return {
      imageSrc: image,
      image1: image1,
      showDropdown: false,
      isLoggedIn: false,  // Der Status, der direkt in Vue gehalten wird
    };
  },
  mounted() {
    // Initialen Status aus localStorage setzen
    this.isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  },
  methods: {
    logout() {
      localStorage.removeItem("isLoggedIn");
      this.isLoggedIn = false;  // Status in Vue anpassen
      this.$router.push("/login"); // Optional: Weiterleitung zur Login-Seite
    }
  },
  watch: {
    // Wenn localStorage aktualisiert wird, den isLoggedIn-Status in Vue neu setzen
    '$route'() {
      this.isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
    }
  }
};
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
  padding: 0 2rem;
  margin: 2rem auto;
  max-width: 1200px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  z-index: 100;
}

.logo-img {
  width: 120px;
  height: auto;
  display: block;
}

.logo span {
  font-size: 2rem;
  color: #0f172a;
  font-weight: 700;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
  flex-grow: 1;
  justify-content: center;
}

.nav-link {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1e293b;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.nav-link:hover {
  background-color: rgba(100, 116, 139, 0.1);
  transform: scale(1.05);
}

.router-link-exact-active {
  background-color: #38bdf8;
  color: #ffffff;
  box-shadow: 0 4px 10px rgba(56, 189, 248, 0.4);
  font-weight: 600;
  transform: scale(1.05);
  transition: all 0.3s ease;
}

.auth-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-left: 4rem; /* Vergrößert den Abstand zwischen dem letzten Link (About) und dem Profilbereich */
}

.auth-link {
  font-size: 0.95rem;
  font-weight: 600;
  background-color: #4f46e5;
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  border: none;
  text-decoration: none;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.auth-link:hover {
  background-color: #4338ca;
  transform: scale(1.03);
}

.logged-in-text {
  color: #475569;
  font-size: 0.8rem;
  margin-right: 0.5rem;
}

.profile-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  cursor: pointer;
}

.profile-dropdown {
  position: relative;
  display: flex;
  align-items: center;
}

.dropdown-menu {
  position: absolute;
  top: 110%;
  right: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 0.5rem 0;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  min-width: 150px;
  z-index: 999;
}

.dropdown-item {
  display: block;
  padding: 0.75rem 1.25rem;
  color: #1e293b;
  font-size: 0.9rem;
  text-decoration: none;
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f1f5f9;
  color: #111827;
}

/* Responsive */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    height: auto;
    padding: 1rem;
  }

  .nav-links {
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
  }

  .auth-container {
    margin-top: 1rem; /* Vergrößert den Abstand bei kleinen Bildschirmen */
  }

  .nav-link, .auth-link {
    width: 100%;
    text-align: center;
  }
}
</style>
