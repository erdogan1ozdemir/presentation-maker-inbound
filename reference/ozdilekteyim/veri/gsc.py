# -*- coding: utf-8 -*-
"""Özdilekteyim GSC - aylık seri (Ağu'25 - Ağu'26), segment ve sayfa grupları.

Kaynak: Search Console · https://www.ozdilekteyim.com/ · dimensions=date,device
Segmentler:
  brand     = query includingRegex  özdilek|ozdilek        -> ölçülür
  nonbrand  = toplam - brand (click/impression)             -> çıkarma
              pozisyon: query excludingRegex ile ayrıca ölçülür
  mağaza    = page includingRegex /magaza/
  market    = page includingRegex ozdilekteyim.com/market
  cp2       = page includingRegex -cp2/?$  (marka + kategori sayfaları)
Query filtresi uygulandığında anonim sorgular düştüğü için non-brand hacmi
toplamdan çıkarılarak bulunur; anonim hacim non-brand satırında yer alır.
"""
import re
from pathlib import Path

HAM = Path(__file__).parent / "ham"
TR = {1: "Oca", 2: "Şub", 3: "Mar", 4: "Nis", 5: "May", 6: "Haz",
      7: "Tem", 8: "Ağu", 9: "Eyl", 10: "Eki", 11: "Kas", 12: "Ara"}
SATIR = re.compile(r"^(\d{4}-\d{2}-\d{2})\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|"
                   r"\s*([\d.]+)%\s*\|\s*([\d.]+)\s*$")
KAYNAK = {"toplam": "gsc_toplam_gunluk.txt", "brand": "gsc_brand_gunluk.txt",
          "nb_poz": "gsc_nonbrand_regex_gunluk.txt", "magaza": "gsc_magaza_gunluk.txt",
          "market": "gsc_market_gunluk.txt", "cp2": "gsc_cp2_gunluk.txt"}


def oku(dosya):
    ay, son = {}, None
    for ln in (HAM / dosya).read_text(encoding="utf-8").splitlines():
        m = SATIR.match(ln.strip())
        if not m:
            continue
        t, _d, c, i, _ctr, p = m.groups()
        y = int(t[:4]) * 100 + int(t[5:7])
        a = ay.setdefault(y, [0, 0, 0.0])
        a[0] += int(c); a[1] += int(i); a[2] += int(i) * float(p)
        son = max(son or t, t)
    return ay, son


def etiket(y):
    return f"{TR[y % 100]}'{str(y // 100)[2:]}"


def seriler():
    ham = {k: oku(v) for k, v in KAYNAK.items()}
    aylar = sorted(ham["toplam"][0])
    out = {}
    for k in ("toplam", "brand", "magaza", "market", "cp2"):
        d = ham[k][0]
        out[k] = {y: dict(click=d.get(y, [0, 0, 0])[0], impr=d.get(y, [0, 0, 0])[1],
                          poz=(d[y][2] / d[y][1]) if d.get(y, [0, 0, 0])[1] else None)
                  for y in aylar}
    nbp = ham["nb_poz"][0]
    out["nonbrand"] = {y: dict(click=out["toplam"][y]["click"] - out["brand"][y]["click"],
                               impr=out["toplam"][y]["impr"] - out["brand"][y]["impr"],
                               poz=(nbp[y][2] / nbp[y][1]) if nbp.get(y, [0, 0, 0])[1] else None)
                       for y in aylar}
    for k in out:
        for y in aylar:
            r = out[k][y]
            r["ctr"] = r["click"] / r["impr"] * 100 if r["impr"] else None
    son_gun = {k: v[1] for k, v in ham.items()}
    return aylar, out, son_gun


def k(v):
    return f"{v/1_000_000:.2f}M" if v >= 1_000_000 else f"{v/1000:.1f}K"


if __name__ == "__main__":
    aylar, s, son = seriler()
    print("son gün:", son)
    print(f"{len(aylar)} ay: {etiket(aylar[0])} - {etiket(aylar[-1])}\n")
    for seg in ("toplam", "brand", "nonbrand", "magaza", "market", "cp2"):
        print(f"== {seg}")
        print("  " + "  ".join(f"{etiket(y)} {k(s[seg][y]['click'])}" for y in aylar))
    def pct(a, b): return f"{(a/b-1)*100:+.1f}%" if b else "yeni"
    print("\n== Ağu'26 özet (click · impr · poz · MoM click · YoY click)")
    for seg in ("toplam", "brand", "nonbrand", "magaza", "market", "cp2"):
        a, m, yo = s[seg][202608], s[seg][202607], s[seg][202508]
        pz = f"{a['poz']:.1f}" if a['poz'] else "-"
        print(f"  {seg:9} {a['click']:>8,} {a['impr']:>11,} {pz:>6}  "
              f"MoM {pct(a['click'], m['click']):>8}  YoY {pct(a['click'], yo['click']):>8}")
