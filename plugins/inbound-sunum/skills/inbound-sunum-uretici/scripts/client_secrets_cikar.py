#!/usr/bin/env python3
"""
client_secrets_cikar.py - Mevcut token.json'dan client_secrets.json uretir.

Ne ise yarar: bir OAuth client daha once olusturulmus ve elde yalnizca
token dosyasi kalmissa, Google Cloud'da yeni client acmaya gerek yok.
Token dosyasi client_id ve client_secret'i de tasidigi icin ekibe
dagitilacak client_secrets.json bu dosyadan yeniden kurulabilir.

Kullanim:
    python3 client_secrets_cikar.py /yol/token.json -o client_secrets.json

Uretilen dosya bir SIRDIR: repoya konmaz, kasadan dagitilir.
"""
import argparse
import json
import pathlib
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("token", help="mevcut token.json / gsc_token.json")
    ap.add_argument("-o", "--cikti", default="client_secrets.json")
    a = ap.parse_args()

    t = json.loads(pathlib.Path(a.token).read_text(encoding="utf-8"))
    cid, csec = t.get("client_id"), t.get("client_secret")
    if not cid or not csec:
        sys.exit("HATA: token dosyasinda client_id / client_secret yok. "
                 "Bu token servis hesabiyla ya da farkli bir akisla uretilmis "
                 "olabilir; Google Cloud'dan yeni bir Desktop app client "
                 "olusturmak gerekir.")

    kapsam = t.get("scopes") or []
    beklenen = "https://www.googleapis.com/auth/webmasters.readonly"
    if kapsam and kapsam != [beklenen]:
        print(f"UYARI: token kapsami {kapsam}. Salt okunur olmayan bir client "
              f"ile devam etmeyin; kapsam yalnizca {beklenen} olmali.",
              file=sys.stderr)

    govde = {"installed": {
        "client_id": cid,
        "client_secret": csec,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": t.get("token_uri") or "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "redirect_uris": ["http://localhost"],
    }}
    p = pathlib.Path(a.cikti)
    p.write_text(json.dumps(govde, indent=2) + "\n", encoding="utf-8")
    try:
        p.chmod(0o600)
    except OSError:
        pass
    print(f"-> {p}  (client_id ...{cid[-30:]})")
    print("Bu dosya bir sirdir: repoya konmaz, kasadan dagitilir.")


if __name__ == "__main__":
    main()
