#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALD Genesis-Manifest verifizieren
===================================
Prüft die Echtheit des Genesis-Manifests OHNE den privaten Schlüssel.
Jeder kann das ausführen — Vertrauen ohne Vertrauensvorschuss.

Versionen:
  v0 — historischer Stand (vor Audit-Fix), siehe CHANGELOG.md
  v1 — aktuell gültige Version (Default)

Lauf:
    python3 scripts/verify_manifest.py                  # v1 (Default)
    python3 scripts/verify_manifest.py --version v0     # explizit v0
    python3 scripts/verify_manifest.py --version v1     # explizit v1
    python3 scripts/verify_manifest.py --all            # beide
"""
import sys, json, hashlib, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.wallet import Wallet


GENESIS_DIR = ROOT / "genesis"

VERSIONS = {
    "v0": {
        "manifest": GENESIS_DIR / "MANIFEST_v0.md",
        "envelope": GENESIS_DIR / "manifest_envelope_v0.json",
        "label": "v0 (historisch, durch v1 abgelöst)",
    },
    "v1": {
        "manifest": GENESIS_DIR / "MANIFEST.md",
        "envelope": GENESIS_DIR / "manifest_envelope.json",
        "label": "v1 (aktuell gültig)",
    },
}

# Whitelist erlaubter Algorithmen — verhindert "alg: none"-Angriffe
ALLOWED_SIG_ALGS = {"ed25519"}
ALLOWED_HASH_ALGS = {"blake2b-256"}

# Felder, die im signierten Payload mit dem Envelope übereinstimmen müssen
PAYLOAD_BOUND_FIELDS = (
    "manifest_hash_hex",
    "manifest_hash_alg",
    "signer_address",
    "signer_public_key_hex",
    "signature_alg",
    "timestamp_utc",
    "manifest_file",
)


def verify_one(version):
    cfg = VERSIONS[version]
    manifest_file = cfg["manifest"]
    envelope_file = cfg["envelope"]
    label = cfg["label"]

    print("=" * 64)
    print(f"  ALD GENESIS-MANIFEST VERIFIKATION — {label}")
    print("=" * 64)

    if not manifest_file.exists() or not envelope_file.exists():
        print(f"❌ Manifest oder Envelope fehlt:")
        print(f"   {manifest_file.name}: {'OK' if manifest_file.exists() else 'FEHLT'}")
        print(f"   {envelope_file.name}: {'OK' if envelope_file.exists() else 'FEHLT'}")
        return False

    try:
        env = json.loads(envelope_file.read_text())
    except json.JSONDecodeError as e:
        print(f"❌ Envelope ist kein gültiges JSON: {e}")
        return False

    manifest_bytes = manifest_file.read_bytes()

    print(f"\n→ Manifest:           {env.get('manifest_file', '?')} ({len(manifest_bytes)} Bytes)")
    print(f"→ Signiert von:       {env.get('signer_address', '?')}")
    print(f"→ Signaturzeit (UTC): {env.get('timestamp_utc', '?')}")
    print()

    # Schritt 0: Algorithmen-Whitelist
    print(f"Schritt 0: Algorithmen prüfen")
    sig_alg = env.get("signature_alg")
    hash_alg = env.get("manifest_hash_alg")
    if sig_alg not in ALLOWED_SIG_ALGS:
        print(f"   ❌ Signatur-Algorithmus '{sig_alg}' nicht erlaubt (erwartet: {ALLOWED_SIG_ALGS}).")
        return False
    if hash_alg not in ALLOWED_HASH_ALGS:
        print(f"   ❌ Hash-Algorithmus '{hash_alg}' nicht erlaubt (erwartet: {ALLOWED_HASH_ALGS}).")
        return False
    print(f"   ✅ Signatur: {sig_alg}, Hash: {hash_alg}")
    print()

    # Schritt 1: Hash neu berechnen
    computed_hash = hashlib.blake2b(manifest_bytes, digest_size=32).hexdigest()
    print(f"Schritt 1: Hash des Manifests neu berechnen")
    print(f"   Erwartet:   {env['manifest_hash_hex']}")
    print(f"   Berechnet:  {computed_hash}")
    if computed_hash != env['manifest_hash_hex']:
        print("   ❌ HASH STIMMT NICHT — Manifest wurde verändert!")
        return False
    print(f"   ✅ Hash passt — Manifest ist unverändert.")
    print()

    # Schritt 2: Signatur prüfen
    print(f"Schritt 2: Ed25519-Signatur prüfen")
    try:
        pub = bytes.fromhex(env["signer_public_key_hex"])
        sig = bytes.fromhex(env["signature_hex"])
    except (KeyError, ValueError) as e:
        print(f"   ❌ Public Key oder Signatur fehlt/ungültig: {e}")
        return False

    payload_str = env.get("payload_canonical_json")
    if not isinstance(payload_str, str):
        print(f"   ❌ Feld 'payload_canonical_json' fehlt oder ist kein String.")
        return False
    payload = payload_str.encode("utf-8")

    valid = Wallet.verify_signature(pub, payload, sig)
    if not valid:
        print("   ❌ SIGNATUR UNGÜLTIG!")
        return False
    print(f"   ✅ Signatur gültig.")
    print()

    # Schritt 3: Payload-Inhalt gegen Envelope cross-checken
    # Verhindert, dass ein Angreifer einen gültig signierten Payload mit
    # manipulierten Top-Level-Metadaten umhüllt.
    print(f"Schritt 3: Payload-Bindung an Envelope prüfen")
    try:
        payload_obj = json.loads(payload_str)
    except json.JSONDecodeError as e:
        print(f"   ❌ Signierter Payload ist kein gültiges JSON: {e}")
        return False

    if not isinstance(payload_obj, dict):
        print(f"   ❌ Signierter Payload ist kein JSON-Objekt.")
        return False

    mismatches = []
    for field in PAYLOAD_BOUND_FIELDS:
        env_val = env.get(field)
        pl_val = payload_obj.get(field)
        if env_val != pl_val:
            mismatches.append((field, env_val, pl_val))

    if mismatches:
        print(f"   ❌ Envelope-Felder weichen vom signierten Payload ab:")
        for field, env_val, pl_val in mismatches:
            print(f"      {field}:")
            print(f"        Envelope: {env_val!r}")
            print(f"        Payload:  {pl_val!r}")
        return False
    print(f"   ✅ Alle {len(PAYLOAD_BOUND_FIELDS)} gebundenen Felder stimmen überein.")
    print()

    # Schritt 4: Adresse ableiten
    print(f"Schritt 4: Adresse aus Public Key ableiten")
    derived_addr = Wallet.address_from_pubkey(pub)
    print(f"   Erwartet:   {env['signer_address']}")
    print(f"   Abgeleitet: {derived_addr}")
    if derived_addr != env['signer_address']:
        print("   ❌ ADRESSE PASST NICHT zum Public Key!")
        return False
    print(f"   ✅ Adresse korrekt.")
    print()

    print("=" * 64)
    print(f"  ✅ MANIFEST {version.upper()} IST ECHT")
    print("=" * 64)
    print()
    print(f"  Signiert von:        {env['signer_address']}")
    print(f"  Signatur-Algorithmus: {env['signature_alg']}")
    print(f"  Hash-Algorithmus:     {env['manifest_hash_alg']}")
    if 'version_note' in env:
        print(f"  Hinweis:              {env['version_note']}")
    print()
    return True


def main():
    parser = argparse.ArgumentParser(description="ALD Genesis-Manifest verifizieren")
    parser.add_argument("--version", choices=["v0", "v1"], default="v1",
                        help="Welche Version prüfen (Default: v1)")
    parser.add_argument("--all", action="store_true",
                        help="Beide Versionen (v0 und v1) prüfen")
    args = parser.parse_args()

    if args.all:
        ok_v0 = verify_one("v0")
        print()
        ok_v1 = verify_one("v1")
        print()
        print("=" * 64)
        print("  ZUSAMMENFASSUNG")
        print("=" * 64)
        print(f"  v0 (historisch):  {'✅ ECHT' if ok_v0 else '❌ UNGÜLTIG'}")
        print(f"  v1 (aktuell):     {'✅ ECHT' if ok_v1 else '❌ UNGÜLTIG'}")
        print()
        print(f"  Beide Versionen wurden vom IDENTISCHEN Genesis-Wallet signiert.")
        print(f"  v0 wurde nie veröffentlicht (interner Audit-Stand).")
        print(f"  v1 ist die kanonische, veröffentlichte Version.")
        print(f"  Siehe CHANGELOG.md für vollständige Begründung.")
        sys.exit(0 if (ok_v0 and ok_v1) else 1)
    else:
        ok = verify_one(args.version)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
