<template>
  <div class="navbar">
    <div class="nav-links">
      <RouterLink to="/sign-pdf" class="nav-link">Sign PDF</RouterLink>
      <div class="logo">
      <span>📝</span>
    </div>
      <RouterLink to="/about" class="nav-link">About</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center; /* vertikal zentriert */
  justify-content: center; /* horizontal zentriert */
  padding: 1rem 2rem;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 80px;
  border-radius: 16px;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue",
    Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 0;
}

.logo {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.logo span {
  font-size: 3rem;
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-link {
  font-size: 2rem; /* Alternativ: calc(100% - etwas) oder vh/vw nutzen */
  font-weight: bold;
  text-decoration: none;
  color: #333;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

/* Kein Lila + keine Unterstreichung bei visited */
.nav-link:visited {
  color: #333;
  text-decoration: none;
}

/* Hover Effekt */
.nav-link:hover {
  background-color: #e0e0e0;
}

/* Klick- bzw. active-Effekt */
.nav-link:active {
  background-color: #cfcfcf;
}
.router-link-exact-active {
  background-color: #f0f0f0; /* Dauerhaft ausgegrauter Hintergrund */
  border-radius: 8px;
}
</style>
