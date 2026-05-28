# ALD ALADIN TOKEN — Genesis-Manifest

**Datum:** 28. Mai 2026
**Betreiber:** Rabbit-Marketing OÜ
**Adresse:** Tornimäe tn 5, 10145 Tallinn, Estland
**Registrikood:** 17397243
**Domain:** aladin-crypto.com
**Kontakt:** hello@aladin-crypto.com
**Genesis-Adresse (siehe `genesis_address.txt`):** *wird beim Signieren eingesetzt*

---

## Selbstverpflichtung der Gründer

Wir — die Gründer von ALD ALADIN TOKEN — erklären mit diesem mathematisch
signierten Dokument folgende Grundsätze für die Phase 1 und alle nachfolgenden
Phasen:

### 1. Was ALD ist

ALD ist ein dezentrales, mathematisch verifizierbares Utility- und
Zugangssystem für eine wachsende Gemeinschaft. Es besteht aus genau
**22.222.222 Einheiten**, die nicht verkauft, sondern durch Teilnahme,
Aktivität und Zeit erarbeitet werden (Proof of Effort).

### 2. Was ALD nicht ist

ALD ist **kein** Investment, **kein** Wertpapier, **kein** Finanzinstrument
im Sinne von WpHG/KWG/MiCA, **kein** Zahlungsmittel. Es werden **keine**
Rendite-, Gewinn- oder Wertsteigerungsversprechen gemacht. Die Einheiten
werden in Phase 1 und Phase 2 weder verkauft noch gehandelt. Sie haben
keinen Geldwert.

### 3. Technische Architektur

Die technische Spezifikation des ALD-Protokolls ist im beiliegenden Dokument
`PROTOKOLL.md` (Version 0.1, 28.05.2026) festgehalten. Es basiert auf:

- **Wallet-Identität:** Ed25519-Schlüsselpaare, lokal erzeugt, niemals
  zentral gespeichert.
- **Effort-Beweise:** sequenzielle Hash-Iteration (BLAKE3) — keine
  Hash-Lotterie wie bei Bitcoin, kein Hardware-Wettrüsten, kein Megawatt-Strom.
- **Konsens:** ≥ 2/3 Validator-Mehrheit (Threshold-Signaturen, BLS12-381
  heute, post-quantum-Migration zu Dilithium/SPHINCS+ vorgesehen).
- **Markenzahl 2:** algorithmischer Kern — Schwierigkeitsstufen 2²², 2²²×22,
  2²²×222, 2²²×2.222 — mathematisch in das System eingebaut, nicht nur als
  Symbol.

### 4. Sybil-Resistenz

Drei Schichten verhindern, dass ein Konzern oder Rechenzentrum das System
übernehmen kann:

1. **Wirtschaftlich:** Phase 1 hat keinen Geldwert — kein Anreiz für
   Sybil-Attacken.
2. **Mathematisch:** sequenzielle Hash-Iteration — mehr Hardware bringt
   keinen Pro-Beweis-Vorteil.
3. **Strukturell:** Threshold ≥ 2/3 — das Netz als Ganzes ist das Schloss.

### 5. Open Source und Transparenz

Die Referenz-Implementierung des Protokolls wird in Phase 2 als Open
Source veröffentlicht. Bis dahin liegt der vollständig getestete Python-Code
im Repository `protokoll/` mit 16/16 bestandenen Tests.

### 6. Phasen-Roadmap

- **Phase 1 (jetzt, 2026):** Vorbereitung, Erklärseite, Community-Aufbau,
  Pre-Registration. Kein Live-Netz, kein Geldwert.
- **Phase 2 (2027):** Rust-Port der Referenz-Implementierung, Test-Netz,
  Open-Source-Audit.
- **Phase 3 (2028+):** Mainnet, Post-Quantum-Migration der Wallets,
  rechtlich begleitete Diskussion möglicher Monetarisierung.

### 7. Was nicht geschieht

- Kein Vorverkauf, kein ICO, kein Token-Sale, keine Crowdfunding-Runde
  während Phase 1.
- Keine Versprechen über zukünftigen Geldwert.
- Keine Behauptung über künftige Eintragungen, Listings, Börsen oder
  Partnerschaften.

### 8. Rechtlicher Rahmen

Betreiber: Rabbit-Marketing OÜ (Estland), gegründet 17397243.
Kontaktperson nach §631 Äriseadustik: ENTYTECH OÜ (Registrikood 16080939).
Anwendbares Recht: Estland. Datenschutz: DSGVO/EU.

Sollte ALD je in eine Phase eintreten, in der Einheiten einen Geldwert
darstellen könnten, wird dies vorher öffentlich angekündigt, rechtlich
begleitet und in Abstimmung mit den zuständigen Aufsichtsbehörden gestaltet.

### 9. Markenstand

Die Wortmarke „ALADIN" befindet sich aktuell im EUIPO-Widerspruchsverfahren
(B 003249185). Bis zur formalen Eintragung wird kein ®-Zeichen verwendet,
um keinen falschen Eindruck zu erwecken.

### 10. Echtheits-Anker

Dieses Manifest ist mit dem **Genesis-Wallet** (Ed25519) signiert. Die
Signatur kann von jedem mit dem beiliegenden Skript `verify_manifest.py`
geprüft werden — ohne Vertrauensvorschuss, rein mathematisch.

Wer den privaten Schlüssel zur Genesis-Adresse besitzt, ist die einzige
Quelle, die berechtigt ist, künftige offizielle Nachrichten unter dem
Namen ALD ALADIN TOKEN zu unterzeichnen.

---

**Tallinn, 28. Mai 2026**

Rabbit-Marketing OÜ
