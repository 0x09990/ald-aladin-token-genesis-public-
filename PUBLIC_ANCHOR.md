# ALD Genesis — Öffentliche Verankerung der Manifest-Hashes

**Stand:** 28.05.2026
**Zweck:** Dieser Text dokumentiert die kryptografischen Identitäts-Anker
von ALD ALADIN TOKEN. Er soll an mehreren öffentlichen, unveränderlichen
Stellen verteilt werden — analog zum Verteilen eines PGP-Public-Keys auf
mehreren Keyservern.

**Warum verteilt veröffentlichen?** Wenn nur EIN Server die Wahrheit kennt,
kann ein Angreifer (oder ein Behördenzugriff) sie überschreiben. Wenn 5
voneinander unabhängige Server denselben Hash zeigen, ist eine Manipulation
mathematisch unmöglich, ohne dass mindestens 4 davon kompromittiert werden.

---

## Genesis-Identität

```
Adresse:    ald1jrrvknsy0r8kllg280elfzqarfk8lerr
Public Key: 6d7492d9046a466dcfb920285109e731096d46d7be702bb311b66f807f6b96a8
Kurve:      Ed25519 (RFC 8032)
```

---

## Manifest-Hashes (BLAKE2b-256)

```
v1 (aktuell):    49b44aeb1fa00978e3f7498da8f58e2dcaddbd7c315e48f47468b139a2f6ce9a
v0 (historisch): 5baa2d3954093e342575ceac310e1a1bdc968d01cd1c2450f87ef39862ad313e
```

---

## Signaturen (Ed25519)

**v1:** `45236634d7b0e97c926570060d55d5a6f430023e95219df87828f0339fc64d48cf090b98ddbb4fbcfaa5658b3132f95b1ecdb1b66be6717d3a95f21551052d0f`

**v0:** `d7eb76e42545f94e2c306d78313e729a93e4e87a41a85e3d608d3e60ed5061e45fddfc7ba559a5d7bc73982c3b846d279fc37bdbf54f16c62c1df6f1b36b7b01`

---

## Manifest-Quellen (Spiegel)

Die signierten Manifest-Dateien selbst (und ihre Verifikations-Werkzeuge)
sind erreichbar unter:

1. **Offizielle Domain:** https://aladin-crypto.com/genesis/
2. **GitHub (sollte angelegt werden):** github.com/ald-aladin-token/genesis
3. **IPFS (sollte gepinnt werden):** ipfs://<HASH-NACH-UPLOAD>
4. **OpenTimestamps (sollte gestempelt werden):** siehe ANCHOR_INSTRUCTIONS.md
5. **Internet Archive (Wayback):** sollte gecrawlt werden, sobald Site live

---

## Selbst-Verifikation (jeder kann das)

```bash
# 1. Hashes neu berechnen
python3 -c "
import hashlib
print('v1:', hashlib.blake2b(open('MANIFEST.md','rb').read(), digest_size=32).hexdigest())
print('v0:', hashlib.blake2b(open('MANIFEST_v0.md','rb').read(), digest_size=32).hexdigest())
"
# → muss exakt mit obigen Werten übereinstimmen

# 2. Signaturen prüfen
python3 scripts/verify_manifest.py --all
# → ✅ v0 echt, ✅ v1 echt

# 3. Adresse aus Public Key ableiten
python3 -c "
import hashlib
pub = bytes.fromhex('6d7492d9046a466dcfb920285109e731096d46d7be702bb311b66f807f6b96a8')
print('BLAKE2b(pub,20) =', hashlib.blake2b(pub, digest_size=20).hexdigest())
"
```

---

## Veränderungs-Prinzip

**Sollte ein Hash auf einem der Spiegel JEMALS anders aussehen als hier
gezeigt — ist dieser Spiegel manipuliert.** Bei jeglicher Diskrepanz:
- Den abweichenden Spiegel als kompromittiert behandeln
- Die Mehrheits-Wahrheit der anderen Spiegel akzeptieren
- Die Diskrepanz öffentlich dokumentieren

Dieses Prinzip funktioniert wie bei Bitcoin-Block-Hashes: jeder kann die
ganze Kette nachrechnen, niemand kann sie heimlich verändern.

---

## Twitter/X-fertige Kurzfassung

```
ALD Genesis-Anker (28.05.2026)
Pub: 6d7492d9046a466dcfb920285109e731096d46d7be702bb311b66f807f6b96a8
Adr: ald1jrrvknsy0r8kllg280elfzqarfk8lerr
v1:  49b44aeb1fa00978e3f7498da8f58e2dcaddbd7c315e48f47468b139a2f6ce9a
Verify: aladin-crypto.com/verify
```

---

## Versions-Historie dieser Datei

| Datum | Änderung |
|---|---|
| 28.05.2026 | Initial — beide Versionen v0+v1 dokumentiert |

Sollte sich diese PUBLIC_ANCHOR.md jemals ändern, MUSS hier ein neuer
Eintrag stehen — sonst ist die Datei selbst kompromittiert.
