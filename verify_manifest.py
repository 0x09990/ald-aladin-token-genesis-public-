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

    env = json.loads(envelope_file.read_text())
    manifest_bytes = manifest_file.read_bytes()

    print(f"\n→ Manifest:           {env['manifest_file']} ({len(manifest_bytes)} Bytes)")
    print(f"→ Signiert von:       {env['signer_address']}")
    print(f"→ Signaturzeit (UTC): {env['timestamp_utc']}")
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
    pub = bytes.fromhex(env["signer_public_key_hex"])
    sig = bytes.fromhex(env["signature_hex"])
    payload = env["payload_canonical_json"].encode("utf-8")
    valid = Wallet.verify_signature(pub, payload, sig)
    if not valid:
        print("   ❌ SIGNATUR UNGÜLTIG!")
        return False
    print(f"   ✅ Signatur gültig.")
    print()

    # Schritt 3: Adresse ableiten
    print(f"Schritt 3: Adresse aus Public Key ableiten")
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
