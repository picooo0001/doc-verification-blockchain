<template>
  <div class="navbar">
    <!-- Container für die Links, wird mittig ausgerichtet -->
    <div class="nav-links">
      <RouterLink to="/sign-pdf" class="nav-link">Sign PDF</RouterLink>
      <div class="logo">
        <img src="../assets/blockchain-informationen-flexibel-sicher.1.4" alt="Logo" class="logo-img" />
      </div>
      <RouterLink to="/about" class="nav-link">About</RouterLink>
    </div>
    <!-- Rechter Container für den Login-Button -->
    <div class="auth-container">
      <template v-if="isLoggedIn">
        <span class="logged-in-text">Signed in</span>
        <div class="profile-dropdown" @mouseenter="showDropdown = true" @mouseleave="showDropdown = false">
          <img src="../assets/logo.png" alt="Profil" class="profile-icon" />
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

<script>
import image from '../assets/logo.png';
import image1 from '../assets/profile.png';

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
.logo-img {
  width: 128px;      /* oder z. B. 80px, je nach Wunsch */
  height: auto;
  display: block;
  margin: 0 auto;
}
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Links und Login-Button am Rand */
  height: 64px;
  background-color: rgba(10, 15, 44, 0.75); /* halbtransparentes Dunkelblau */
  backdrop-filter: blur(8px); /* Glassmorphism Effekt */
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue",
    Helvetica, Arial, sans-serif;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
  border-radius: 16px;
  margin: 2rem auto;
  padding: 0 2rem;
  width: 1000px;
  z-index: 10;
}

.logo {
  display: flex;
  align-items: center;
  margin: 0 20px;
}

.logo span {
  font-size: 2.5rem; /* Logo ein kleines bisschen kleiner */
  color: white;
}

.nav-links {
  display: flex;
  gap: 30px;
  align-items: center;
  flex-grow: 1; /* Verhindert, dass der Login-Button die Navigationselemente nach rechts drängt */
  justify-content: center; /* Mittige Ausrichtung der Links */
}

.nav-link {
  font-size: 1.25rem; /* Kleiner, dafür edler */
  font-weight: bold;
  text-decoration: none;
  color: #e2e8f0;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

/* Kein Farbwechsel bei visited */
.nav-link:visited {
  color: white;
}

/* Hover Effekt */
.nav-link:hover {
  background-color: rgba(56, 189, 248, 0.1);
  border-color: #6366f1;
}

/* Aktive Seite */
.router-link-exact-active {
  background-color: rgba(56, 189, 248, 0.3); /* Stärkere Hintergrundfarbe */
  color: #0a0f2c; /* dunkle Schrift für Kontrast */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Leichter Schatten für mehr Fokus */
  transform: scale(1.05); /* Leichte Skalierung für einen "Hervorhebungseffekt" */
  transition: all 0.3s ease; /* Weiche Übergänge */
}

/* Auth Container für den Login Button */
.auth-container {
  display: flex;
  align-items: center;
}

.auth-link {
  font-size: 1rem; /* Kleinere Schriftgröße */
  font-weight: bold;
  text-decoration: none;
  color: #e2e1e1;
  padding: 0.25rem 0.75rem; /* Weniger Padding */
  border-radius: 8px;
  background-color: #22d3ee; /* Cyan wie bei aktiven Links */

  transition: background-color 0.3s ease;
}

.auth-link:hover {
  background-color: #4f46e5;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    padding: 1rem;
  }

  .nav-links {
    flex-direction: column;
    gap: 10px;
  }

  .auth-container {
    margin-top: 10px;
  }

  .nav-link, .auth-link {
    font-size: 1rem;
  }
}

.logged-in-text {
  color: #e2e1e1;
  margin-right: 0.5rem;
  font-weight: normal;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue",
  Helvetica, Arial, sans-serif;
  font-size: 0.6rem; /* oder z.B. 0.8rem für noch kleiner */
}

.profile-icon {
  width: 16px;
  height: 16px;
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