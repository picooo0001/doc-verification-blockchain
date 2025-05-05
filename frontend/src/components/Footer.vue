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
  backdrop-filter: blur(10px); /* Stärkerer Glassmorphism */
  color: white;
  padding: 2rem 3rem;
  text-align: center;
  width: 1000px;
  margin: 3rem auto 1rem auto;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
  position: relative;
  z-index: 10;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.footer-links {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 1rem;
}

.footer-links a {
  color: #22d3ee; /* Cyan für aktive Links */
  font-weight: 600;
  font-size: 1.1rem;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  transition: color 0.3s ease, transform 0.2s ease;
}

.footer-links a:hover {
  color: #38bdf8; /* Helles Cyan beim Hover */
  transform: scale(1.05); /* Leichte Skalierung für Interaktivität */
}

.footer-text {
  font-size: 1rem;
  color: #e2e8f0; /* Helles Grau für den Text */
  font-weight: 400;
  margin-top: 1rem;
}

.footer-text a {
  color: #38bdf8;
  text-decoration: none;
  font-weight: 500;
}

.footer-text a:hover {
  color: #4f46e5; /* Helleres Blau für Links */
}

/* Responsive */
@media (max-width: 768px) {
  .footer {
    padding: 1.5rem;
    width: 90%;
  }

  .footer-links {
    flex-direction: column;
    gap: 1.5rem;
  }

  .footer-text {
    font-size: 0.9rem;
  }

  .footer-links a {
    font-size: 1rem;
  }
}
</style>
