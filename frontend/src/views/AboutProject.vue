<template>
  <div class="main-layout">
  <div class="about-container">
    <h1>Über dieses Projekt</h1>

    <!-- 🔽 Download-Buttons -->
    <h2>Downloads</h2>
    <div class="download-buttons">
      <a href="/downloads/seminararbeit.pdf" download class="trial-btn">Seminararbeit</a>
      <a href="/downloads/praesentation.pdf" download class="trial-btn">Präsentation</a>
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
</div>
</template>

<style scoped>
.main-layout {
  display: flex;
  gap: 2.5rem;
  padding: 3rem 2rem 2rem 2rem;
  min-height: 100vh;
  background: linear-gradient(45deg, #ffffff 0%, #ffffff 60%, #e7d6fb 75%, #cdb6ec 90%, #eab6d8 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
.about-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2.5rem 2rem 2rem 2rem;
  background: linear-gradient(180deg, #fff 0%, #f6eefd 60%, #f2e4f4 100%);
  border-radius: 6px;
  box-shadow: 0 8px 32px rgba(31, 35, 40, 0.12);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  backdrop-filter: blur(6px);
  display: flex;
  flex-direction: column;
  gap: 1.3rem;
  transition: box-shadow 0.18s;
}

.about-container:hover {
  transform: translateY(-5px);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.about-container h1 {
  font-size: 2.2rem;
  color: #1a1726;
  font-weight: 800;
  margin-bottom: 1rem;
}

.about-container h2 {
  margin-top: 2rem;
  font-size: 1.5rem;
  color: #232150;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.about-container p,
.about-container li {
  font-size: 1.125rem;
  line-height: 1.6;
  color: #232150;
}

.download-buttons {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
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
