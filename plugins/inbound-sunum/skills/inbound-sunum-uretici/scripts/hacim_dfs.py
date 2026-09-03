#!/usr/bin/env python3
"""
hacim_dfs.py - Arama hacmi zincirinin son halkası: DataForSEO (Google Ads).

Kaynak sırası SEOmonitor -> Ahrefs -> DataForSEO'dur (bkz.
references/hacim-kaynagi-ve-fallback.md). İlk ikisi MCP araçlarıyla çekilir;
bu betik yalnızca üçüncü halkayı, MCP sunucusu bağlı olmasa da çalışacak
biçimde REST üzerinden alır.

Kullanim:
    python3 hacim_dfs.py --kelime-dosyasi sorgular.txt --ulke 2792 --dil tr
    python3 hacim_dfs.py -k "geforce now" -k "gfn" --json cikti.json

Kimlik bilgisi sırası:
    1. DATAFORSEO_USERNAME / DATAFORSEO_PASSWORD ortam değişkenleri
    2. ~/.claude/settings.json içindeki dataforseo MCP kaydının env bloğu

Notlar:
    - Google Ads hacmi BANTLI döner (2.900 / 3.600 / 4.400 ...). Ay bazında
      değişim yazılmaz, ısı haritası kullanılmaz.
    - Yakın varyantlar tek keyword sayılabilir; iki terim aynı seriyi
      döndürüyorsa toplamaya yalnızca biri girer. Betik bunu tespit edip
      "mukerrer" listesinde bildirir.
"""

import argparse
import base64
import json
import os
import pathlib
import subprocess
import sys

API = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
TR = {1: "Oca", 2: "Şub", 3: "Mar", 4: "Nis", 5: "May", 6: "Haz",
      7: "Tem", 8: "Ağu", 9: "Eyl", 10: "Eki", 11: "Kas", 12: "Ara"}


def kimlik():
    u = os.environ.get("DATAFORSEO_USERNAME")
    p = os.environ.get("DATAFORSEO_PASSWORD")
    if u and p:
        return u, p
    ayar = pathlib.Path.home() / ".claude" / "settings.json"
    if ayar.exists():
        def ara(n):
            if isinstance(n, dict):
                for k, v in n.items():
                    if k == "mcpServers" and isinstance(v, dict):
                        for ad, cfg in v.items():
                            if "dataforseo" in ad.lower() or "dfs" in ad.lower():
                                e = cfg.get("env") or {}
                                if e.get("DATAFORSEO_USERNAME"):
                                    return e["DATAFORSEO_USERNAME"], e.get("DATAFORSEO_PASSWORD")
                    r = ara(v)
                    if r:
                        return r
            return None
        r = ara(json.loads(ayar.read_text(encoding="utf-8")))
        if r:
            return r
    sys.exit("HATA: DataForSEO kimlik bilgisi bulunamadi. DATAFORSEO_USERNAME ve "
             "DATAFORSEO_PASSWORD ortam degiskenlerini tanimla.")


def cek(kelimeler, ulke, dil, ilk_tarih=None, son_tarih=None):
    """curl ile cagrilir: kurumsal SSL araya girdiginde urllib sertifika
    dogrulamasinda dusuyor, curl sistem anahtar zincirini kullaniyor."""
    u, p = kimlik()
    auth = base64.b64encode(f"{u}:{p}".encode()).decode()
    govde = {"keywords": list(kelimeler), "location_code": ulke,
             "language_code": dil, "search_partners": False}
    if ilk_tarih:
        govde["date_from"] = ilk_tarih
    if son_tarih:
        govde["date_to"] = son_tarih
    ck = subprocess.run(
        ["curl", "-s", "--max-time", "120", "-X", "POST", API,
         "-H", f"Authorization: Basic {auth}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps([govde])],
        capture_output=True, text=True)
    if ck.returncode != 0:
        sys.exit(f"HATA: istek basarisiz - {ck.stderr[:200]}")
    d = json.loads(ck.stdout)
    if d.get("status_code") != 20000:
        sys.exit(f"HATA: {d.get('status_code')} {d.get('status_message')}")
    t = d["tasks"][0]
    if t.get("status_code") != 20000:
        sys.exit(f"HATA (task): {t.get('status_code')} {t.get('status_message')}")
    return t.get("result") or []


def mukerrer_bul(seriler):
    """Ayni aylik seriyi tasiyan terim ciftleri - yakin varyant birlesmesi."""
    ciftler, adlar = [], list(seriler)
    for i, a in enumerate(adlar):
        for b in adlar[i + 1:]:
            if seriler[a] and seriler[a] == seriler[b]:
                ciftler.append((a, b))
    return ciftler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--kelime", action="append", default=[])
    ap.add_argument("--kelime-dosyasi")
    ap.add_argument("--ulke", type=int, default=2792, help="location_code (TR=2792)")
    ap.add_argument("--dil", default="tr")
    ap.add_argument("--ilk-tarih")
    ap.add_argument("--son-tarih")
    ap.add_argument("--json", help="sonucu bu dosyaya yaz")
    a = ap.parse_args()

    kelimeler = list(a.kelime)
    if a.kelime_dosyasi:
        kelimeler += [s.strip() for s in
                      pathlib.Path(a.kelime_dosyasi).read_text(encoding="utf-8").splitlines()
                      if s.strip()]
    if not kelimeler:
        sys.exit("HATA: kelime verilmedi (-k veya --kelime-dosyasi)")

    out, seriler = {}, {}
    # DataForSEO tek istekte 1000 kelimeye kadar kabul ediyor
    for i in range(0, len(kelimeler), 700):
        for it in cek(kelimeler[i:i + 700], a.ulke, a.dil, a.ilk_tarih, a.son_tarih):
            kw = it.get("keyword")
            aylik = {m["year"] * 100 + m["month"]: m["search_volume"]
                     for m in (it.get("monthly_searches") or [])}
            out[kw] = {"hacim": it.get("search_volume"), "aylik": aylik,
                       "kaynak": "DataForSEO"}
            seriler[kw] = [aylik[x] for x in sorted(aylik)]

    mk = mukerrer_bul(seriler)
    print(f"{'Kelime':32}{'Hacim':>10}  kaynak")
    for kw in kelimeler:
        v = out.get(kw)
        print(f"{kw[:31]:32}{(v['hacim'] if v and v['hacim'] is not None else '-'):>10}  "
              f"{v['kaynak'] if v else 'bulunamadi'}")
    if mk:
        print("\nYAKIN VARYANT UYARISI - ayni seriyi tasiyan terimler, "
              "toplamaya yalnizca biri girmeli:")
        for x, y in mk:
            print(f"  {x}  ==  {y}")
    eksik = [k for k in kelimeler if not out.get(k) or out[k]["hacim"] is None]
    if eksik:
        print(f"\nHacim bulunamayan {len(eksik)} kelime - tabloda '-' yazilir, "
              f"sifir yazilmaz: {eksik[:8]}")

    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
        print(f"\n-> {a.json}")


if __name__ == "__main__":
    main()
