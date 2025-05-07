<template>
<footer class="footer-wrapper">
  <div class="footer-new">
    <div class="footer-column logo-column">
      <p>PDF-Sign with Blockchain</p>
    </div>

    <div class="footer-column">
      <h4>Platform</h4>
      <a href="#">DevSecOps platform</a>
      <h4>Pricing</h4>
      <a href="#">View plans</a>
      <a href="#">Why Premium?</a>
      <a href="#">Why Ultimate?</a>
    </div>

    <div class="footer-column">
      <h4>Solutions</h4>
      <a href="#">Digital transformation</a>
      <a href="#">Security & Compliance</a>
      <a href="#">Automated Delivery</a>
      <a href="#">Agile Delivery</a>
      <a href="#">CI/CD</a>
    </div>

    <div class="footer-column">
      <h4>Resources</h4>
      <a href="#">Install</a>
      <a href="#">Quick start guides</a>
      <a href="#">Blog</a>
    </div>

    <div class="footer-column">
      <h4>Contact</h4>
      <a href="#">Contact an expert</a>
      <a href="#">Customer portal</a>
      <a href="#">Terms of use</a>
    </div>
  </div>
</footer>


</template>

<script setup>
import { ref } from 'vue'
const currentYear = ref(new Date().getFullYear())
</script>

<style>
.footer-wrapper {
  background-color: #171321; /* dunkler Hintergrund */
  color: #fff;
  width: 100%;
  padding: 4rem 2rem;
}

.footer-new {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 2.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.footer-column h4 {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #ffffff;
}

.footer-column a {
  display: block;
  color: #d1d1d1;
  text-decoration: none;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.footer-column a:hover {
  text-decoration: underline;
  color: #ffffff;
}

.footer-logo {
  width: 40px;
  height: auto;
  margin-bottom: 1rem;
}

.logo-column p {
  color: #cccccc;
  font-size: 0.95rem;
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
</style>
