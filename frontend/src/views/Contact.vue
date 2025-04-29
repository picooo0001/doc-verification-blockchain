<template>
    <div class="container">
      <div class="contact-section">
        <h1>Kontakt</h1>
        <p>Wenn du Fragen hast oder Unterstützung benötigst, erreichst du uns über die folgenden Kanäle:</p>
        <div class="contact-info">
          <div>
            <h3>📧 E-Mail:</h3>
            <p><a href="mailto:kontakt@deinewebsite.de">kontakt@deinewebsite.de</a></p>
          </div>
          <div>
            <h3>📞 Telefon:</h3>
            <p>+49 123 456 789</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  // Hier kannst du später Funktionen für die Kontaktseite hinzufügen
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: rgba(255, 255, 255, 0.95); /* Weiß mit 85% Deckkraft */
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }
  
  .contact-section {
    margin-bottom: 2rem;
  }
  
  h1 {
    font-size: 2rem;
    text-align: center;
    color: #22d3ee;
    margin-bottom: 1rem;
  }
  
  h3 {
    font-size: 1.25rem;
    color: #6366f1;
    margin-bottom: 0.5rem;
  }
  
  p {
    font-size: 1rem;
    color: #e2e8f0;
  }
  
  .contact-info {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-top: 1rem;
  }
  
  .contact-info div {
    flex: 1;
  }
  
  /* Responsive Anpassung */
  @media (max-width: 768px) {
    .contact-info {
      flex-direction: column;
      align-items: center;
    }
  }
  </style>
  