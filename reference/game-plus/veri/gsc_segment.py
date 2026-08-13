# -*- coding: utf-8 -*-
"""Game+ GSC - Brand / Non-brand / GFN aylık seri (Tem'25 - Tem'26).

Kaynak: mcp__gsc__get_advanced_search_analytics · sc-domain:gameplus.com.tr
        dimensions=date,device · 2025-07-01..2026-07-31

Segment tanımı (gsc-dashboard/src/lib/services/gsc/etl.ts ile aynı yöntem):
  brand    = includingRegex  gameplus|game ?plus|game\\+          → ölçülür
  nonbrand = toplam - brand  (click ve impression)                → çıkarma
  gfn      = includingRegex  gfn|geforce now|geforcenow|ge ?force ?now
Anonim sorgular query filtresinde düştüğü için non-brand'e yazılır; repo da
bu yöntemi kullanıyor.

GFN, brand ve non-brand'in üzerine binen ayrı bir mercektir - üç grup toplamı
toplama eşit değildir.
"""
import re
from pathlib import Path

TR = {1: "Oca", 2: "Şub", 3: "Mar", 4: "Nis", 5: "May", 6: "Haz",
      7: "Tem", 8: "Ağu", 9: "Eyl", 10: "Eki", 11: "Kas", 12: "Ara"}

D = Path("/Users/Erdo/.claude/projects/-Users-Erdo-Desktop-Claude-Projects-sunum--rnekleri"
         "/0207f43a-132e-425b-9b0f-f6ad91b2f665/tool-results")
KAYNAK = {
    "total": D / "mcp-gsc-get_advanced_search_analytics-1786636400207.txt",
    "brand": D / "mcp-gsc-get_advanced_search_analytics-1786636410753.txt",
    "gfn":   D / "mcp-gsc-get_advanced_search_analytics-1786636418919.txt",
    # non-brand pozisyonu: excludingRegex ile ayrica olculur. Click/impression
    # icin kullanilmaz - query filtresi anonim sorgulari dusurdugu icin hacim
    # eksik cikar; hacim "toplam - brand" ile hesaplanir.
    "nb_poz": D / "mcp-gsc-get_advanced_search_analytics-1786651173127.txt",
}

SATIR = re.compile(
    r"^(\d{4}-\d{2}-\d{2})\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*"
    r"([\d.]+)%\s*\|\s*([\d.]+)\s*$")


def oku(path):
    """(yil_ay) -> [click, impression, impression*pozisyon]"""
    ay = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = SATIR.match(line.strip())
        if not m:
            continue
        tarih, _dev, click, impr, _ctr, poz = m.groups()
        y, mo = int(tarih[:4]), int(tarih[5:7])
        a = ay.setdefault(y * 100 + mo, [0, 0, 0.0])
        a[0] += int(click)
        a[1] += int(impr)
        a[2] += int(impr) * float(poz)
    return ay


def etiket(ym):
    return f"{TR[ym % 100]}'{str(ym // 100)[2:]}"


def seriler():
    ham = {k: oku(p) for k, p in KAYNAK.items()}
    aylar = sorted(ham["total"])
    out = {}
    for seg in ("total", "brand", "gfn"):
        out[seg] = {y: dict(click=ham[seg].get(y, [0, 0, 0])[0],
                            impr=ham[seg].get(y, [0, 0, 0])[1],
                            poz=(ham[seg][y][2] / ham[seg][y][1]) if ham[seg].get(y, [0, 0, 0])[1] else None)
                    for y in aylar}
    # non-brand = toplam - brand (etl.ts ile aynı); pozisyon ayrı ölçülür
    nbp = ham["nb_poz"]
    out["nonbrand"] = {y: dict(click=out["total"][y]["click"] - out["brand"][y]["click"],
                               impr=out["total"][y]["impr"] - out["brand"][y]["impr"],
                               poz=(nbp[y][2] / nbp[y][1]) if nbp.get(y, [0, 0, 0])[1] else None)
                       for y in aylar}
    return aylar, out


def k(v):
    return f"{v/1_000_000:.2f}M" if v >= 1_000_000 else f"{v/1000:.1f}K"


if __name__ == "__main__":
    aylar, s = seriler()
    print(f"{len(aylar)} ay: {etiket(aylar[0])} - {etiket(aylar[-1])}\n")
    print(f"{'Ay':8}" + "".join(f"{n:>22}" for n in ("TOPLAM", "BRAND", "NON-BRAND", "GFN")))
    print(f"{'':8}" + "".join(f"{'click':>10}{'impr':>12}" for _ in range(4)))
    for y in aylar:
        row = f"{etiket(y):8}"
        for seg in ("total", "brand", "nonbrand", "gfn"):
            row += f"{s[seg][y]['click']:>10,}{k(s[seg][y]['impr']):>12}"
        print(row)

    def d(seg, a, b, m):
        x, y = s[seg][a][m], s[seg][b][m]
        return f"{(x/y-1)*100:+.1f}%" if y else "-"

    print("\nTemmuz 2026 karşılaştırma:")
    for seg, ad in (("total", "Toplam"), ("brand", "Brand"),
                    ("nonbrand", "Non-brand"), ("gfn", "GFN")):
        print(f"  {ad:10} click MoM {d(seg,202607,202606,'click'):>8}  YoY {d(seg,202607,202507,'click'):>8}"
              f"   impr MoM {d(seg,202607,202606,'impr'):>8}  YoY {d(seg,202607,202507,'impr'):>8}")

    t = s["total"][202607]["click"]
    print("\nTemmuz 2026 click payı:")
    for seg, ad in (("brand", "Brand"), ("nonbrand", "Non-brand"), ("gfn", "GFN (mercek)")):
        print(f"  {ad:14} %{s[seg][202607]['click']/t*100:.1f}")
