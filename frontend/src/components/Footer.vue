<template>
  <div class="main-layout">
  <footer class="footer">
    <div class="footer-content">
      <p>© {{ currentYear }} PDF-Sign with Blockchain</p>
      <div class="footer-links">
        <a href="/contact">Contact & Legal</a>
        <a href="/download">Downloads</a>
      </div>
    </div>
  </footer>
</div>
</template>

<script setup>
import { ref } from 'vue'
const currentYear = ref(new Date().getFullYear())
</script>

<style>
.main-layout {
  display: flex;
  gap: 2.5rem;
  padding: 3rem 2rem 2rem 2rem;
  min-height: 100vh;
  background: #ffffff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
html, body {
  min-height: 100vh;
  background: #ffffff;
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
body {
  min-height: 100vh;
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
.footer {
  background: transparent; /* oder rgba(255,255,255,0.8) für leichten Weißton */


  padding: 1.3rem 2rem;
  width: 100%;
  max-width: 1100px;
  margin: 3rem auto 1.5rem auto;
  border-radius: 14px;
  box-shadow: 0 4px 24px 0 rgba(31, 35, 40, 0.06);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 1.05rem;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
}

.footer-links {
  display: flex;
  gap: 2.2rem;
  flex-wrap: wrap;
}

.footer-links a {
  color: #6c6c6c;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
  border-radius: 0.3rem;
  padding: 0.1rem 0.6rem;
}

.footer-links a:hover,
.footer-links a:focus {
  color: #111;
  background: #f5f5fa;
}

@media (max-width: 700px) {
  .footer {
    padding: 1.1rem 0.7rem;
    max-width: 98vw;
  }
  .footer-links {
    gap: 1.2rem;
  }
}
</style>
