# ALD ALADIN TOKEN — Genesis Authenticity Anchor

> **Cryptographically signed identity & manifest of the ALD ALADIN TOKEN project.**
> Anyone can independently verify — no trust required.

🌐 Website: [aladin-crypto.com](https://aladin-crypto.com) · [Verify Page](https://aladin-crypto.com/verify.html)
📢 Community: [Telegram](https://t.me/ALDALADINtoken) · [YouTube](https://www.youtube.com/channel/UCS79reGGTY5EhlEJnMOHLyQ)

🇩🇪 Deutsche Version dieser README: [README_DE.md](./README_DE.md)

---

## What this repository is

This repository holds the **Genesis Anchor** of ALD ALADIN TOKEN — the cryptographic root of trust from which all future official ALD announcements are signed.

- **Genesis Address:** `ald1jrrvknsy0r8kllg280elfzqarfk8lerr`
- **Genesis Public Key (Ed25519):** `6d7492d9046a466dcfb920285109e731096d46d7be702bb311b66f807f6b96a8`
- **Manifest Hash (BLAKE2b-256, v1):** `49b44aeb1fa00978e3f7498da8f58e2dcaddbd7c315e48f47468b139a2f6ce9a`

If anyone ever claims to speak for ALD ALADIN TOKEN, their message must be signed by this Genesis Wallet — otherwise it is not authentic.

---

## What's inside

| File | Purpose |
|---|---|
| `MANIFEST.md` | v1 — current signed manifesto (founders' commitments, 10 points) |
| `MANIFEST.sig` | Detached Ed25519 signature (human readable) |
| `manifest_envelope.json` | Machine-readable wrapper (hash + signature + metadata) |
| `MANIFEST_v0.md` | v0 — historical version (superseded, see CHANGELOG) |
| `MANIFEST_v0.sig` | v0 signature |
| `manifest_envelope_v0.json` | v0 envelope |
| `CHANGELOG.md` | Full audit trail: why v0 → v1, both still verifiable |
| `PUBLIC_ANCHOR.md` | Publicly shareable hash summary (Twitter/Reddit-ready) |
| `ANCHOR_INSTRUCTIONS.md` | How to anchor the hash on Bitcoin / IPFS / Wayback Machine |
| `genesis_address.txt` | The ALD address (derivable from public key) |
| `genesis_public_key.txt` | The Ed25519 public key (safe to share) |
| `verify_manifest.py` | Python script — verifies signature locally |
| `verify_qr.svg` | QR code linking to verification URL |
| `LICENSE` | CC0 1.0 Universal — see file for details |

**What is NOT in this repository:**
- Private keys (would defeat the entire purpose — the Genesis private key never leaves the founders' offline backups)
- Live ALD protocol code (Phase 2 — separate repository when ready)

---

## How to verify (without trusting us)

### Quick proof (one command)

```bash
git clone https://github.com/<owner>/ald-aladin-token.git
cd ald-aladin-token
pip install cryptography
python3 verify_manifest.py --all
```

Expected output:
```
✅ v0 (historical):  AUTHENTIC
✅ v1 (current):     AUTHENTIC
  Both versions were signed by the IDENTICAL Genesis Wallet.
```

### Step-by-step proof

**1. Recompute hash yourself:**
```bash
python3 -c "import hashlib; print(hashlib.blake2b(open('MANIFEST.md','rb').read(), digest_size=32).hexdigest())"
# Must equal: 49b44aeb1fa00978e3f7498da8f58e2dcaddbd7c315e48f47468b139a2f6ce9a
```

**2. Verify Ed25519 signature:**
```bash
python3 verify_manifest.py --version v1
# → ✅ MANIFEST v1 IS AUTHENTIC
```

**3. Derive address from public key:**
The address shown above must equal `BLAKE2b(public_key, 20 bytes)` base32-encoded with prefix `ald1`. The verify script does this automatically.

---

## What ALD ALADIN TOKEN actually is

- A **utility & access system**, not a financial product
- Fixed supply: **22,222,222 units** — earned through participation, never sold
- Phase 1 (now, 2026): community building, reservation open, no monetary value
- Phase 2 (planned 2027): Rust port, testnet, open-source protocol release
- Phase 3 (planned 2028+): mainnet, post-quantum migration of wallets

**ALD is NOT:** an investment, a security, a payment instrument, or a financial product (per WpHG / KWG / MiCA). No yield, profit, or value increase is promised. Units are not tradable in Phase 1 or Phase 2.

---

## Distributed verification (mirrors)

So that no one can manipulate the hash later, it is anchored on multiple independent stores:

| Mirror | Tamper-proof via |
|---|---|
| This repository (GitHub) | Git commit history + GitHub audit log |
| `aladin-crypto.com/genesis/` | Operator domain |
| OpenTimestamps (Bitcoin blockchain) | Cryptographic blockchain proof |
| IPFS | Content addressing — hash IS the address |
| Internet Archive (Wayback) | Permanent web snapshots |

See `ANCHOR_INSTRUCTIONS.md` for the full distribution procedure.

**The principle:** If the hash on one mirror ever differs from the others, *that mirror* is compromised — not the real hash. Majority truth from the other mirrors wins.

---

## Legal & contact

- **Operator:** Rabbit-Marketing OÜ · Tornimäe tn 5 · 10145 Tallinn · Estonia
- **Registry code:** 17397243
- **Email:** hello@aladin-crypto.com
- **Trademark status:** "ALADIN" is currently in EUIPO opposition proceedings (case B 003249185). No ® mark is used until formal registration — using ® prematurely would be misleading under §5 UWG (German Unfair Competition Act).

---

## License

The contents of this repository are dedicated to the public domain under **Creative Commons CC0 1.0 Universal** (see `LICENSE`).

You may freely copy, verify, mirror, and redistribute everything here. You may NOT use the ALD ALADIN TOKEN brand name to issue your own signed manifestos — the Genesis private key remains the sole signing authority, and the brand is separately protected under trademark / unfair-competition law.

---

*Last updated: 2026-05-28 · See `CHANGELOG.md` for full version history.*
