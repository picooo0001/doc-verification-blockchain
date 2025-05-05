<template>
  <div class="about-container">
    <h1>Über dieses Projekt</h1>

    <!-- 🔽 Download-Buttons -->
    <div class="download-buttons">
      <a href="/downloads/seminararbeit.pdf" download class="download-btn">📄 Seminararbeit herunterladen</a>
      <a href="/downloads/praesentation.pdf" download class="download-btn">📊 Präsentation herunterladen</a>
    </div>

    <p>
      Dieses Projekt mit dem Arbeitstitel <strong>„Blockchain-basierte Dokumentenverifikation und Notarisierung“</strong> befasst sich mit der Entwicklung eines webbasierten Prototyps [...]
    </p>
    <h2>Einleitung</h2>
    <p>
      Die Blockchain-Technologie gewinnt zunehmend an Bedeutung im Bereich der Cyber-Security. Insbesondere für Szenarien wie Dokumentenverifikation und Notarisierung bietet sie Vorteile wie Transparenz, Unveränderbarkeit und Dezentralität. Dieses Projekt nutzt genau diese Eigenschaften, um einen Prototypen zur sicheren Dokumentensignatur zu realisieren.
    </p>

    <h2>Projektaufbau</h2>
    <ul>
      <li><strong>Frontend:</strong> Vue.js mit PrimeVue-Komponenten für ein intuitives UI</li>
      <li><strong>Backend:</strong> Node.js API für Upload, Hashing und Kommunikation mit der Blockchain</li>
      <li><strong>Blockchain-Schnittstelle:</strong> Interaktion über Web3 mit einem Smart Contract in Solidity</li>
      <li><strong>Systemarchitektur:</strong> Klare Trennung von UI, Logik und Blockchain-Komponenten</li>
    </ul>

    <h2>Technologie-Stack</h2>
    <ul>
      <li>Ethereum Testnetz (z. B. Sepolia)</li>
      <li>Smart Contracts in Solidity</li>
      <li>IPFS zur optionalen dezentralen Dateiablage</li>
      <li>Node.js + Express im Backend</li>
      <li>Vue 3 mit PrimeVue im Frontend</li>
    </ul>

    <h2>Use Case</h2>
    <p>
      Der Hauptanwendungsfall liegt in der Signierung von PDF-Dokumenten, z. B. Verträgen oder Zertifikaten, durch Erzeugung eines Hash-Wertes und dessen Speicherung auf der Blockchain. Eine spätere Verifikation erfolgt durch Vergleich des aktuellen Dokument-Hashes mit dem gespeicherten Eintrag.
    </p>

    <h2>Fazit & Ausblick</h2>
    <p>
      Die entwickelte Lösung zeigt, wie Blockchain-Technologie zur digitalen Vertrauensbildung beitragen kann. In Zukunft könnten Erweiterungen wie Mehrfachsignaturen, NFT-basierte Besitznachweise oder eine Einbindung in Behördenprozesse denkbar sein.
    </p>
  </div>
</template>

<style scoped>
.about-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.95); /* Weiß mit 85% Deckkraft */
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  backdrop-filter: blur(8px); /* Glassmorphism */
}

.about-container h1 {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.about-container h2 {
  margin-top: 2rem;
  font-size: 1.75rem;
  color: #333;
}

.about-container p, li {
  font-size: 1.125rem;
  line-height: 1.6;
  color: #555;
}

.download-buttons {
  display: flex;
  flex-direction: row; /* nebeneinander */
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap; /* falls bei kleinen Bildschirmen nötig */
}

.download-btn {
  flex: 1 1 auto;
  padding: 0.75rem 1.5rem;
  background-color: #22d3ee; /* Cyan wie bei aktiven Links */
  color: white;
  text-decoration: none;
  font-weight: bold;
  border-radius: 8px;
  text-align: center;
  transition: background-color 0.3s ease;
  min-width: 200px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.download-btn:hover {
  background-color: #6366f1;
}

ul {
  padding-left: 20px;
}

ul li {
  padding: 1rem;
  background-color: rgba(245, 245, 245, 0.9);
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

ul li p {
  margin: 0.2rem 0;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .about-container {
    padding: 1rem;
  }

  .download-buttons {
    flex-direction: column;
    gap: 1rem;
  }

  .download-btn {
    min-width: unset;
  }

  h1 {
    font-size: 2rem;
  }

  h2 {
    font-size: 1.5rem;
  }
}
</style>
