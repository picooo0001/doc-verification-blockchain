<template>
    <div class="profile-container">
      <h1>Dein Profil</h1>
  
      <div class="profile-info">
        <p><strong>Name:</strong> Max Mustermann</p>
        <p><strong>E-Mail:</strong> max.mustermann@example.com</p>
        <p><strong>Organisation:</strong> Beispiel GmbH</p>
      </div>
  
      <div class="profile-actions">
        <button class="edit-btn">Bearbeiten</button>
        <button class="change-password-btn">Passwort ändern</button>
      </div>
  
      <h2>Deine Aktivitäten</h2>
      <p>Du hast noch keine Aktivitäten durchgeführt.</p>
    </div>
  </template>
  
  <style scoped>
  .profile-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }
  
  .profile-container h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }
  
  .profile-info {
    margin-top: 1rem;
  }
  
  .profile-info p {
    font-size: 1.125rem;
    margin-bottom: 1rem;
  }
  
  .profile-actions {
    margin-top: 2rem;
    display: flex;
    gap: 1rem;
    justify-content: flex-start;
  }
  
  .profile-actions button {
    padding: 0.75rem 1.5rem;
    background-color: #22d3ee;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .profile-actions button:hover {
    background-color: #6366f1;
  }
  
  h2 {
    margin-top: 3rem;
    font-size: 1.75rem;
  }
  </style>
  