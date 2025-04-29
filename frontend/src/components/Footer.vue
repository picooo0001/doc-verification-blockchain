<template>
  <footer class="footer">
    <div class="footer-content">
      <p>© 2025 PDF-Sign with Blockchain</p>
      <div class="footer-links">
        <a href="/contact">Contact & Legal</a>
        <a href="/download">Downloads</a>
      </div>
    </div>
  </footer>
</template>

<script setup>
// keine Logik nötig, außer du willst dynamisches Jahr etc.
</script>

<style scoped>
.footer {
  background-color: rgba(10, 15, 44, 0.75); /* Dunkler halbtransparenter Hintergrund */
  backdrop-filter: blur(8px); /* Glassmorphism */
  color: white;
  padding: 1.5rem 2rem;
    text-align: center;
  width: 1000px;
  margin: 3rem auto 1rem auto;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue",
    Helvetica, Arial, sans-serif;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.footer-links {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.footer-links a {
  color: #22d3ee; /* Cyan wie bei aktiven Links */
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #38bdf8; /* helleres Cyan beim Hover */
}
</style>
