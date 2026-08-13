# -*- coding: utf-8 -*-
"""Game+ GA4 analizleri: kanal, /blog, /gfn/oyunlar alt kategorileri, AI Assistant.

Kaynak: veri/ga4.py (Free-form 1.xlsx, yıl kolonlu sürüm).
Tarama aracı artığı satırlar ayıklanır.
"""
import collections

from ga4 import yukle, ym, etiket

D = [r for r in yukle() if not r["kirli"]]
AYLAR = sorted({ym(r) for r in D})


def topla(filtre):
    """ay -> session"""
    out = collections.Counter()
    for r in D:
        if filtre(r):
            out[ym(r)] += r["session"]
    return out


def yoy_mom(seri, cari=202607):
    onceki_ay = 202606
    gecen_yil = 202507
    def d(a, b):
        return f"{(seri[a]/seri[b]-1)*100:+.1f}%" if seri.get(b) else "-"
    return d(cari, onceki_ay), d(cari, gecen_yil)


def rapor(baslik, filtre):
    s = topla(filtre)
    mom, yoy = yoy_mom(s)
    print(f"\n{baslik}")
    print("  " + "  ".join(f"{etiket(y)} {s[y]:,}" for y in AYLAR))
    print(f"  Tem'26: {s[202607]:,}  ·  MoM {mom}  ·  YoY {yoy}")
    return s


if __name__ == "__main__":
    print("=" * 78)
    print("KANAL BAZINDA TEMMUZ 2026")
    kanal = collections.Counter()
    for r in D:
        if ym(r) == 202607:
            kanal[r["kanal"]] += r["session"]
    tot = sum(kanal.values())
    for kn, v in kanal.most_common():
        print(f"  {kn:24} {v:>9,}  %{v/tot*100:5.2f}")
    print(f"  {'TOPLAM':24} {tot:>9,}")

    ai = topla(lambda r: r["kanal"] == "AI Assistant")
    print("\n" + "=" * 78)
    rapor("AI ASSISTANT KANALI (session)", lambda r: r["kanal"] == "AI Assistant")
    ilk = next((y for y in AYLAR if ai[y]), None)
    if ilk:
        print(f"  ilk görüldüğü ay: {etiket(ilk)}  ·  toplam 13 ay: {sum(ai.values()):,}")

    print("\n" + "=" * 78)
    rapor("/blog TOPLAM (session)", lambda r: r["lp"].startswith("/blog"))
    rapor("/gfn/oyunlar TOPLAM (session)", lambda r: r["lp"].startswith("/gfn/oyunlar"))

    print("\n" + "=" * 78)
    print("OYUNLAR ALT KATEGORİLERİ (session, Tem'26 · MoM · YoY)")
    alt = collections.defaultdict(collections.Counter)
    for r in D:
        lp = r["lp"].split("?")[0].rstrip("/")
        if lp.startswith("/gfn/oyunlar/"):
            alt[lp][ym(r)] += r["session"]
    sirali = sorted(alt.items(), key=lambda kv: -kv[1][202607])
    print(f"  {'Kategori':38}{'Tem 26':>9}{'Haz 26':>9}{'Tem 25':>9}{'MoM':>9}{'YoY':>9}")
    for lp, s in sirali[:16]:
        mom = f"{(s[202607]/s[202606]-1)*100:+.1f}%" if s[202606] else "-"
        yoy = f"{(s[202607]/s[202507]-1)*100:+.1f}%" if s[202507] else "yeni"
        print(f"  {lp:38}{s[202607]:>9,}{s[202606]:>9,}{s[202507]:>9,}{mom:>9}{yoy:>9}")
    print(f"  {'toplam alt kategori':38}{sum(s[202607] for _, s in sirali):>9,}")

    print("\n" + "=" * 78)
    print("TEMMUZ'DA YÜKSELEN BLOG YAZILARI (session, MoM artışına göre)")
    blog = collections.defaultdict(collections.Counter)
    for r in D:
        lp = r["lp"].split("?")[0].rstrip("/")
        if lp.startswith("/blog/"):
            blog[lp][ym(r)] += r["session"]
    yukselen = [(lp, s[202607], s[202606], s[202607] - s[202606])
                for lp, s in blog.items() if s[202607] >= 300]
    yukselen.sort(key=lambda x: -x[3])
    print(f"  {'Sayfa':60}{'Tem 26':>8}{'Haz 26':>8}{'Δ':>8}")
    for lp, t, h, d in yukselen[:12]:
        print(f"  {lp[:58]:60}{t:>8,}{h:>8,}{d:>+8,}")
