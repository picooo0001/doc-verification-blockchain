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
  align-items: center;
  justify-content: center;
  height: 60px; /* Weniger hoch */
  background-color: #4f46e5; /* Indigo-Blau */
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue",
    Helvetica, Arial, sans-serif;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* Stärkerer, weicher Schatten */
  border-radius: 16px; /* Sanfte Rundungen */
  margin: 2rem auto; /* Abstand oben/unten, mittig */
  padding: 0 2rem;
  width: 90%; /* Nicht Full-Width */
  max-width: 1200px; /* Maximal 1200px breit */
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
}

.nav-link {
  font-size: 1.25rem; /* Kleiner, dafür edler */
  font-weight: bold;
  text-decoration: none;
  color: white;
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
  background-color: #6366f1;
}

/* Aktive Seite */
.router-link-exact-active {
  background-color: #6366f1;
  border-radius: 8px;
}
</style>
