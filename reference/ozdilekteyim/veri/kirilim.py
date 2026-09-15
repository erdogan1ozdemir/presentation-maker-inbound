# -*- coding: utf-8 -*-
"""Sorgu ve sayfa kırılımları: Ağu'26 / Tem'26 / Ağu'25 (GSC, ilk 5000 sorgu / 2000 sayfa)."""
import re
from pathlib import Path

HAM = Path(__file__).parent / "ham"
BRAND = re.compile(r"özdilek|ozdilek", re.I)


def tablo(dosya):
    d = {}
    for ln in (HAM / dosya).read_text(encoding="utf-8").splitlines():
        p = [x.strip() for x in ln.split("|")]
        if len(p) != 5 or p[0] in ("Query", "Page"):
            continue
        try:
            d[p[0]] = dict(click=int(p[1]), impr=int(p[2]),
                           poz=float(p[4]))
        except ValueError:
            continue
    return d


Q = {"a26": tablo("gsc_query_2026-08.txt"), "t26": tablo("gsc_query_2026-07.txt"),
     "a25": tablo("gsc_query_2025-08.txt")}
P = {"a26": tablo("gsc_sayfa_2026-08.txt"), "t26": tablo("gsc_sayfa_2026-07.txt"),
     "a25": tablo("gsc_sayfa_2025-08.txt")}


def yol(u):
    return re.sub(r"^https?://[^/]+", "", u) or "/"


def hareketler(kume, simdi, onceki, filtre=lambda x: True, n=10, alan="click", esik=0):
    s, o = kume[simdi], kume[onceki]
    anahtar = [x for x in set(s) | set(o) if filtre(x)]
    satir = []
    for x in anahtar:
        a = s.get(x, {}).get(alan, 0) if alan != "poz" else s.get(x, {}).get("poz")
        b = o.get(x, {}).get(alan, 0) if alan != "poz" else o.get(x, {}).get("poz")
        if alan == "poz":
            if a is None or b is None:
                continue
            if s[x]["impr"] < esik or o[x]["impr"] < esik:
                continue
            satir.append((x, b, a, b - a))          # pozitif = iyileşme
        else:
            satir.append((x, b, a, a - b))
    satir.sort(key=lambda r: -r[3])
    return satir[:n], sorted(satir, key=lambda r: r[3])[:n]


if __name__ == "__main__":
    for ad, d in Q.items():
        b = sum(v["click"] for q, v in d.items() if BRAND.search(q))
        print(f"sorgu {ad}: {len(d)} satır · toplam click {sum(v['click'] for v in d.values()):,} · brand {b:,}")
    for ad, d in P.items():
        print(f"sayfa {ad}: {len(d)} satır · toplam click {sum(v['click'] for v in d.values()):,}")

    print("\n== Non-brand sorgu click artış / düşüş (Ağu'26 vs Ağu'25)")
    art, dus = hareketler(Q, "a26", "a25", lambda q: not BRAND.search(q), 8)
    for q, b, a, d in art: print(f"  +  {q[:40]:42}{b:>7,} → {a:>7,}  {d:+,}")
    for q, b, a, d in dus: print(f"  -  {q[:40]:42}{b:>7,} → {a:>7,}  {d:+,}")

    print("\n== Brand sorgu click (Ağu'26 vs Ağu'25)")
    art, dus = hareketler(Q, "a26", "a25", lambda q: bool(BRAND.search(q)), 8)
    for q, b, a, d in dus: print(f"  -  {q[:40]:42}{b:>7,} → {a:>7,}  {d:+,}")
    for q, b, a, d in art[:4]: print(f"  +  {q[:40]:42}{b:>7,} → {a:>7,}  {d:+,}")

    print("\n== Sayfa click artış / düşüş (Ağu'26 vs Ağu'25)")
    art, dus = hareketler(P, "a26", "a25", n=8)
    for u, b, a, d in art: print(f"  +  {yol(u)[:48]:50}{b:>7,} → {a:>7,}  {d:+,}")
    for u, b, a, d in dus: print(f"  -  {yol(u)[:48]:50}{b:>7,} → {a:>7,}  {d:+,}")
