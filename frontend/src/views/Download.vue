<template>
    <div class="container">
      <div class="download-section">
        <h1>Downloads</h1>
        <p>Hier kannst du die neuesten Versionen unserer Software herunterladen:</p>
        <div class="download-links">
          <a href="/downloads/software-v1.0.zip" class="download-btn">Download Version 1.0</a>
          <a href="/downloads/software-v2.0.zip" class="download-btn">Download Version 2.0</a>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  // Hier kannst du später Funktionen für die Downloadseite hinzufügen
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
  
  .download-section {
    margin-bottom: 2rem;
  }
  
  h1 {
    font-size: 2rem;
    text-align: center;
    color: #22d3ee;
    margin-bottom: 1rem;
  }
  
  p {
    font-size: 1rem;
    color: #e2e8f0;
  }
  
  .download-links {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin-top: 1rem;
  }
  
  .download-btn {
    padding: 0.75rem 1.5rem;
    background-color: #6366f1;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    text-decoration: none;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }
  
  .download-btn:hover {
    background-color: #4f46e5;
    transform: scale(1.05);
  }
  
  a {
    text-decoration: none;
    color: inherit;
  }
  
  /* Responsive Anpassung */
  @media (max-width: 768px) {
    .download-links {
      flex-direction: column;
      align-items: center;
    }
  }
  </style>
  