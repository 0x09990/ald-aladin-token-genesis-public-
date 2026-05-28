# ALD Genesis-Manifest — Änderungs-Historie

Dieses Dokument dokumentiert ALLE Versionen des ALD-Genesis-Manifests
mit vollständigen kryptografischen Beweisen.

**Prinzip:** Vertrauen entsteht durch SICHTBARKEIT der Historie, nicht durch
deren Verstecken. Bitcoin-Whitepaper hatte mehrere Drafts. Linux-Kernel zeigt
jeden Commit. Dasselbe Prinzip gilt hier.

---

## Versionen im Überblick

| Version | Datum (UTC) | Größe | BLAKE2b-Hash | Status |
|---|---|---|---|---|
| **v0** | 2026-05-28T13:48:35 | 4314 Bytes | `5baa2d3954093e342575ceac310e1a1bdc968d01cd1c2450f87ef39862ad313e` | historisch (abgelöst) |
| **v1** | 2026-05-28T14:10:21 | 4381 Bytes | `49b44aeb1fa00978e3f7498da8f58e2dcaddbd7c315e48f47468b139a2f6ce9a` | **aktuell gültig** |

**Beide Versionen wurden vom IDENTISCHEN Genesis-Wallet signiert:**
- Adresse: `ald1jrrvknsy0r8kllg280elfzqarfk8lerr`
- Public Key: `6d7492d9046a466dcfb920285109e731096d46d7be702bb311b66f807f6b96a8`
- Kurve: Ed25519

---

## v1 — 2026-05-28T14:10:21.819981+00:00 (aktuell gültig)

**Dateien:**
- `MANIFEST.md` — der signierte Text
- `MANIFEST.sig` — Signatur in lesbarer Form
- `manifest_envelope.json` — Maschinen-lesbarer Wrapper

**Kryptografische Daten:**
- BLAKE2b-256-Hash: `49b44aeb1fa00978e3f7498da8f58e2dcaddbd7c315e48f47468b139a2f6ce9a`
- Ed25519-Signatur: `45236634d7b0e97c926570060d55d5a6f430023e95219df87828f0339fc64d48cf090b98ddbb4fbcfaa5658b3132f95b1ecdb1b66be6717d3a95f21551052d0f`
- Größe: 4381 Bytes

**Verifikation:**
```bash
python3 scripts/verify_manifest.py --version v1
# → ✅ MANIFEST v1 IST ECHT
```

---

## v0 — 2026-05-28T13:48:35.353053+00:00 (historisch, durch v1 abgelöst)

**Dateien:**
- `MANIFEST_v0.md` — rekonstruierter Text (siehe Forensik-Hinweis unten)
- `MANIFEST_v0.sig` — Signatur aus Audit-Protokoll
- `manifest_envelope_v0.json` — maschinen-lesbarer v0-Wrapper

**Kryptografische Daten:**
- BLAKE2b-256-Hash: `5baa2d3954093e342575ceac310e1a1bdc968d01cd1c2450f87ef39862ad313e`
- Ed25519-Signatur: `d7eb76e42545f94e2c306d78313e729a93e4e87a41a85e3d608d3e60ed5061e45fddfc7ba559a5d7bc73982c3b846d279fc37bdbf54f16c62c1df6f1b36b7b01`
- Größe: 4314 Bytes

**Verifikation:**
```bash
python3 scripts/verify_manifest.py --version v0
# → ✅ MANIFEST v0 IST ECHT
```

**Forensik-Hinweis zur v0-Datei:**
Die ursprüngliche `MANIFEST.md` (v0) wurde am 28.05.2026 gegen 14:10 UTC durch v1
überschrieben (Audit-Fix Stufe D — siehe unten). Die exakten v0-Bytes sind aus
der dokumentierten Hash- und Signatur-Information **forensisch rekonstruiert**:

1. Der einzige Unterschied zwischen v0 und v1 war Zeile 9, die in v0
   einen Platzhalter `*wird beim Signieren eingesetzt*` enthielt statt
   der echten Adresse + Public Key.
2. Aus den dokumentierten Größen (v0: 4314 Bytes, v1: 4381 Bytes, Differenz
   exakt 67 Bytes) und dem bekannten Platzhalter-Wortlaut wurde v0 rekonstruiert.
3. Der BLAKE2b-Hash der rekonstruierten Bytes ergibt EXAKT
   `5baa2d3954093e342575ceac310e1a1bdc968d01cd1c2450f87ef39862ad313e`
   — also den dokumentierten Original-Hash.
4. Die dokumentierte Ed25519-Signatur verifiziert gegen die rekonstruierten Bytes.
5. **Daraus folgt mathematisch:** die rekonstruierten v0-Bytes sind bit-identisch
   zur ursprünglichen v0-Datei. Es gibt keinen anderen Inhalt, der genau diesen
   Hash und diese gültige Signatur erzeugen könnte (Kollisionsresistenz BLAKE2b
   + EdDSA-Sicherheit).

---

## Warum v0 → v1? (Audit-Begründung)

**Im internen Code-Audit am 28.05.2026 nachmittags wurde Fehler F4 identifiziert:**

Die ursprüngliche `MANIFEST.md` (v0) enthielt in Zeile 9 einen unersetzten
Platzhalter-Text:

```
**Genesis-Adresse (siehe `genesis_address.txt`):** *wird beim Signieren eingesetzt*
```

Das Signing-Skript `sign_manifest.py` ersetzte diesen Platzhalter nicht — die
echte Adresse stand nur in der separaten Datei `genesis_address.txt` und im
`manifest_envelope.json`. Aus rein-menschlicher Lesesicht wirkte das Manifest
dadurch unfertig.

**Fix in v1:** Platzhalter durch echte Adresse + Public Key direkt im Manifest
ersetzt:

```
**Genesis-Adresse:** `ald1jrrvknsy0r8kllg280elfzqarfk8lerr`
**Genesis-Public-Key:** `6d7492d9046a466dcfb920285109e731096d46d7be702bb311b66f807f6b96a8`
```

Da jeder Byte-Unterschied einen komplett anderen kryptografischen Hash erzeugt,
musste das Manifest neu signiert werden. Die Signatur erfolgte mit dem
IDENTISCHEN Genesis-Wallet wie zuvor — es wurde KEIN neuer Schlüssel erzeugt.

**Was sich NICHT geändert hat:**
- Genesis-Wallet (Adresse + Public Key + Private Key)
- Selbstverpflichtungs-Inhalt (Punkte 1–10 sind in v0 und v1 identisch)
- Operator-Stammdaten (Rabbit-Marketing OÜ, Tornimäe tn 5)
- Algorithmen (BLAKE2b-256 für Hash, Ed25519 für Signatur)
- Rechtliche Aussagen

---

## Wer kann was prüfen?

**Jeder, ohne uns vertrauen zu müssen:**

```bash
# 1. v0-Bytes selbst hashen
python3 -c "import hashlib; print(hashlib.blake2b(open('MANIFEST_v0.md','rb').read(), digest_size=32).hexdigest())"
# → 5baa2d39…313e ✅

# 2. v1-Bytes selbst hashen
python3 -c "import hashlib; print(hashlib.blake2b(open('MANIFEST.md','rb').read(), digest_size=32).hexdigest())"
# → 49b44aeb…ce9a ✅

# 3. Beide Signaturen verifizieren
python3 scripts/verify_manifest.py --all
# → ✅ v0 echt · ✅ v1 echt

# 4. Adressableitung selbst nachrechnen
python3 -c "
import hashlib
pub = bytes.fromhex('6d7492d9046a466dcfb920285109e731096d46d7be702bb311b66f807f6b96a8')
print('BLAKE2b(pub,20) =', hashlib.blake2b(pub, digest_size=20).hexdigest())
# Bech32-Encoded wird zu ald1jrrvknsy0r8kllg280elfzqarfk8lerr
"
```

---

## Zukünftige Versionen

Sollte das Manifest jemals weiter geändert werden:
1. Diese CHANGELOG.md bekommt einen v2-Eintrag mit Hash, Signatur, Begründung.
2. Die alte Version wird NICHT überschrieben, sondern parallel beibehalten.
3. Das `verify_manifest.py`-Skript wird um die neue Version erweitert.
4. Die `verify.html`-Seite zeigt alle Versionen mit ihrer jeweiligen Gültigkeit.

**Regel ab 28.05.2026:** Niemand-überschreibt-mehr. Jede Version bleibt
forensisch zugänglich. Audit-Trail ist heilig.

---

*Diese Datei ist Teil des Genesis-Anker-Verzeichnisses und wird mit dem
Manifest selbst veröffentlicht. Sie ist NICHT signiert (würde Zirkularität
einführen), sondern dokumentiert die Signatur-Geschichte des Manifests.*
