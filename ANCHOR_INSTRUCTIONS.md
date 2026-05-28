# Wie veröffentliche ich den Genesis-Hash unveränderbar?

**Ziel:** Den ALD-Genesis-Hash auf mehrere voneinander unabhängige öffentliche
Speicher legen — so wie PGP-Public-Keys auf Keyserver gepusht werden. Ohne dass
jemand (auch wir nicht) ihn nachträglich verändern könnte.

---

## Übersicht — die 5 Spiegel

| Methode | Tamper-proof durch | Aufwand | Kosten |
|---|---|---|---|
| **OpenTimestamps** | Bitcoin-Blockchain | 5 Min | gratis |
| **GitHub Repository** | Git-History + GitHub-Audit-Log | 10 Min | gratis |
| **IPFS** | Content-Addressing (Hash = Adresse) | 15 Min | gratis (Pinning kostet ggf.) |
| **Archive.org Wayback** | Internet Archive crawlt + speichert für immer | 0 Min (passiv) | gratis |
| **PGP-Schlüsselserver** | Schlüssel-Replikation weltweit | 10 Min | gratis |

**Empfehlung:** Mache MINDESTENS 3 davon. Je mehr, desto sicherer.

---

## Methode 1: OpenTimestamps (am wichtigsten — Bitcoin-Anker)

**Was es macht:** Erzeugt einen Beweis, dass eine Datei zu einem bestimmten
Zeitpunkt existierte, indem es den Hash in einer Bitcoin-Transaktion verankert.
Niemand kann nachträglich behaupten, der Hash sei früher oder später gewesen —
die Bitcoin-Blockchain ist unverändlich.

**Schritte:**

```bash
# Einmalig: Tool installieren
pip install opentimestamps-client

# Hash stempeln (erzeugt MANIFEST.md.ots)
cd protokoll/genesis
ots stamp MANIFEST.md
ots stamp MANIFEST_v0.md

# WARTEN: 1–6 Stunden, bis die Stempel in einen Bitcoin-Block kommen
# Dann upgraden (holt den endgültigen Beweis):
ots upgrade MANIFEST.md.ots
ots upgrade MANIFEST_v0.md.ots

# Verifizieren (jeder kann das ohne uns):
ots verify MANIFEST.md.ots
# → "Success! Bitcoin block <NUMMER> attests existence as of <ZEITSTEMPEL>"
```

**Was Christian danach hat:** Zwei zusätzliche Dateien (`MANIFEST.md.ots` und
`MANIFEST_v0.md.ots`), die JEDER mit `ots verify` prüfen kann — und die Bitcoin-
Blockchain selbst bestätigt, dass der Hash zu dem Zeitpunkt existierte.

**Diese Dateien sollten dann zu `website/genesis/` kopiert werden.**

---

## Methode 2: GitHub Repository

GitHub-Audit-Log dokumentiert jeden Commit. Jede nachträgliche Änderung wäre
in der History sichtbar.

**Schritte:**

```bash
# 1. Auf github.com einen NEUEN ACCOUNT anlegen (oder bestehenden nutzen)
# 2. Neues Repository erstellen: ald-aladin-token/genesis (public)
# 3. Lokal:
cd protokoll/genesis
git init
git add MANIFEST.md MANIFEST.sig manifest_envelope.json \
        MANIFEST_v0.md MANIFEST_v0.sig manifest_envelope_v0.json \
        CHANGELOG.md PUBLIC_ANCHOR.md genesis_address.txt genesis_public_key.txt \
        ANCHOR_INSTRUCTIONS.md
# WICHTIG: GENESIS_PRIVATE_KEY.SECRET *NIE* committen!
git commit -m "Genesis-Anker v0+v1 — 28.05.2026"
git remote add origin git@github.com:ald-aladin-token/genesis.git
git push -u origin main
```

**Was Christian danach hat:** Öffentliches GitHub-Repository, das jeder
einsehen kann. URL: `github.com/ald-aladin-token/genesis`. Jeder Commit
wird vom GitHub-Audit-Log dokumentiert — Nachträgliches Verändern wäre
nicht heimlich möglich.

---

## Methode 3: IPFS

**Was es macht:** IPFS adressiert Inhalte über ihren Hash. Wer denselben
Inhalt hochlädt, bekommt dieselbe Adresse. Wer den Inhalt verändert,
bekommt eine andere Adresse. Niemand kann unter der gleichen Adresse
verschiedene Inhalte servieren.

**Schritte:**

```bash
# Tool installieren
sudo apt install ipfs   # oder: https://docs.ipfs.tech/install/

# Daemon starten
ipfs init
ipfs daemon &

# Genesis-Ordner hochladen
ipfs add -r protokoll/genesis/
# → liefert einen CID wie QmXXX… — DAS ist die unveränderliche Adresse

# Pinnen (damit es nicht aus dem Cache fällt)
ipfs pin add QmXXX…

# Optional: bei einem öffentlichen Pinning-Service registrieren
# (Pinata, Web3.Storage, Filebase — viele bieten Free-Tiers)
```

**Was Christian danach hat:** Eine IPFS-CID. Jeder mit IPFS-Tool kann
`ipfs get QmXXX…` machen und kriegt EXAKT die selben Dateien — falls auch
nur ein Byte anders wäre, hätte er eine andere CID.

---

## Methode 4: Archive.org Wayback Machine (passiv)

**Was es macht:** Internet Archive crawlt regelmäßig Webseiten und speichert
sie permanent. Sobald `aladin-crypto.com/verify.html` (und damit auch
`/genesis/MANIFEST.md` etc.) live ist, wird sie automatisch archiviert.

**Schritte (manuell anstoßen, falls Wartezeit zu lang):**

1. Browser öffnen: `https://web.archive.org/save/https://aladin-crypto.com/verify.html`
2. Wayback Machine archiviert die Seite sofort
3. Wiederholen für: `/genesis/MANIFEST.md`, `/genesis/PUBLIC_ANCHOR.md`, etc.

**Was Christian danach hat:** Permanente Snapshots der Manifest-Dateien
im Internet Archive. Niemand kann diese Snapshots löschen oder verändern.

---

## Methode 5: PGP-Schlüsselserver (für die Identität, nicht das Manifest)

**Was es macht:** Der Genesis-Public-Key (Ed25519) wird in OpenPGP-Format
gepackt und auf Schlüsselservern hinterlegt. Nicht der Manifest-Hash selbst,
aber die Signier-Identität wird damit weltweit auffindbar.

**Schritte (komplex — überspringen falls 1–4 reichen):**

```bash
# Ed25519-Key in OpenPGP-Format konvertieren
# (gpg --quick-generate-key dann --edit-key import private bytes …)
# Tutorial siehe: https://wiki.gnupg.org/Ed25519

# Auf Keyserver pushen
gpg --send-keys <KEY-ID> --keyserver keys.openpgp.org
```

---

## Anschließend: PUBLIC_ANCHOR.md überall verteilen

Nach Methoden 1–4 sollte die `PUBLIC_ANCHOR.md` (kurze Hash-Zusammenfassung)
zusätzlich an folgenden Stellen kopiert werden:

- Twitter/X-Post mit der Kurzfassung
- LinkedIn-Post (falls relevant)
- Reddit (z.B. r/cryptography oder r/Bitcoin)
- Hacker News (Show HN: ALD authenticity anchor)
- Telegram-Channel (`t.me/ALDALADINtoken` — schon vorhanden)
- Eigene Blog-Posts

Je mehr unabhängige Stellen denselben Hash zeigen, desto schwerer wäre
eine spätere Manipulation.

---

## Prinzip: Niemand kann ALLE Spiegel gleichzeitig manipulieren

Wenn der Hash auf:
- der eigenen Domain steht ✓
- in einem GitHub-Commit steht ✓
- in der Bitcoin-Blockchain via OTS verankert ist ✓
- als IPFS-CID adressiert ist ✓
- im Wayback Machine archiviert ist ✓

… dann müsste ein Angreifer ALLE FÜNF gleichzeitig kompromittieren, um eine
Manipulation durchzuziehen. Die Bitcoin-Blockchain allein erfordert dafür
51 % aller weltweiten Mining-Hashrate. Das ist mathematisch unmöglich.

**Das ist die Schönheit der Verteilten Identität — exakt so wie bei
PGP-Keyservern.**

---

## Was Christian JETZT zuerst tun sollte

1. **Methode 1 (OpenTimestamps)** ausführen — wichtigster Anker
2. **Methode 4 (Wayback)** sofort triggern, sobald die Site live ist
3. **Methode 2 (GitHub)** wenn Account verfügbar
4. **PUBLIC_ANCHOR.md** auf Twitter/X / Telegram posten

**Was Claude (Terminal) NICHT tun kann:**
- Tatsächliche Internet-Calls machen (kein Netzwerk-Zugriff im Sandboxing)
- Bitcoin-Transaktionen senden
- GitHub-Accounts anlegen

→ Christian muss diese Aktionen aus seinem eigenen Browser/Terminal ausführen.
Alle Werkzeuge und Anleitungen sind hier vorbereitet.
