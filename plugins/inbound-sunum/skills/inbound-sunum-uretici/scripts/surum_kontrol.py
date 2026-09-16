# -*- coding: utf-8 -*-
"""Kurulu skill sürümü GitHub'daki güncel sürümle karşılaştırılır.

Eski sürümle deste üretmek, düzeltilmiş tuzakları geri getirir (etiket
yerleşimi, tablo başlığı, punto tabanı gibi). Bu yüzden inbound_deck.py ve
qa_deck.py çalışmadan önce bu kontrolü yapar; sürüm geriyse ÜRETİM DURUR.

Atlamak için (ağ yok, bilinçli karar): INBOUND_SURUM_ATLA=1
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
YEREL = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".claude-plugin", "plugin.json"))
UZAK = ("https://raw.githubusercontent.com/erdogan1ozdemir/presentation-maker-inbound/"
        "main/plugins/inbound-sunum/.claude-plugin/plugin.json")


def _surum(t):
    return tuple(int(x) for x in t.strip().split("."))


def kontrol(sessiz=False):
    """(guncel_mi, yerel, uzak). Ağ yoksa (None, yerel, None) döner ve engellemez."""
    try:
        with open(YEREL, encoding="utf-8") as f:
            yerel = json.load(f).get("version", "0.0.0")
    except Exception:
        return None, "?", None
    if os.environ.get("INBOUND_SURUM_ATLA") == "1":
        return None, yerel, None
    uzak = None
    try:
        with urllib.request.urlopen(UZAK, timeout=4) as r:
            uzak = json.load(r).get("version", "0.0.0")
    except Exception:
        # macOS python'da sertifika zinciri eksik olabiliyor; curl sistem
        # sertifikalarini kullanir.
        try:
            import subprocess
            out = subprocess.run(["curl", "-s", "-m", "5", UZAK], capture_output=True,
                                 text=True, timeout=8).stdout
            uzak = json.loads(out).get("version", "0.0.0") if out.strip() else None
        except Exception:
            uzak = None
    if not uzak:
        if not sessiz:
            print(f"[sürüm] ağa ulaşılamadı, kontrol atlandı (yerel {yerel})", file=sys.stderr)
        return None, yerel, None
    return _surum(yerel) >= _surum(uzak), yerel, uzak


def zorunlu():
    """Sürüm geriyse mesaj basıp süreci durdurur."""
    guncel, yerel, uzak = kontrol()
    if guncel is False:
        print(f"\n[sürüm] Kurulu skill {yerel}, güncel sürüm {uzak}. Eski sürümle deste "
              f"üretilmez.\n"
              f"  Claude Code : /plugin menüsünden inbound-sunum'u güncelle "
              f"(ya da: claude plugin update inbound-sunum)\n"
              f"  claude.ai   : dist/ altındaki güncel zip'i Settings → Capabilities → "
              f"Skills'e yeniden yükle\n"
              f"  Ağ yoksa    : INBOUND_SURUM_ATLA=1 ile bilinçli olarak atlanabilir\n",
              file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    g, y, u = kontrol()
    print(f"yerel {y} · uzak {u or '-'} · {'güncel' if g else ('eski' if g is False else 'kontrol edilemedi')}")
    sys.exit(0 if g is not False else 3)
