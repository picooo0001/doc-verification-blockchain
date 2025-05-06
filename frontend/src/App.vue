<template>
  <div class="app-container">
    <Navbar />
    <main class="content">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

console.log('App.vue geladen')
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background: linear-gradient(90deg, #fff 0%, #f3e7fa 50%, #e0c3fc 80%, #8ec5fc 100%);
}
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
}
</style>
