# -*- coding: utf-8 -*-
"""Game+ marka ve GFN aylık arama hacmi (TR, Tem'25 - Tem'26).

Kaynak: Ahrefs Keywords Explorer - volume history · country=tr
Segment tanımı GSC regex'leriyle aynı terim kümesini kullanır:
  brand = gameplus + game plus + game+
  gfn   = geforce now + gfn + geforcenow

Terim toplamı, aynı aramanın farklı yazımlarını tek seride birleştirir;
kesişen sorgular (ör. "gameplus geforce now") her iki kümede de sayılabilir,
bu yüzden seriler mutlak talep değil yön göstergesi olarak okunur.
"""

AYLAR = [202507, 202508, 202509, 202510, 202511, 202512,
         202601, 202602, 202603, 202604, 202605, 202606, 202607]

TERIM = {
    "gameplus":    [5271, 5128, 5562, 5417, 6040, 6925, 6918, 7471, 6969, 6056, 5617, 5658, 5088],
    "game plus":   [1020, 1155, 839, 940, 1486, 1762, 1696, 2746, 1442, 1075, 1270, 1639, 1355],
    "game+":       [968, 961, 937, 957, 1190, 1204, 1220, 960, 1182, 834, 246, 236, 821],
    "geforce now": [102712, 119784, 93403, 97373, 105098, 101411, 97461, 144280, 122245,
                    92280, 91255, 92140, 81441],
    "gfn":         [1861, 1841, 1819, 1856, 1874, 2284, 1846, 1547, 1803, 1529, 1525, 1728, 1476],
    "geforcenow":  [1614, 1798, 1246, 1219, 1220, 1687, 1577, 2862, 2457, 1366, 887, 1173, 1075],
}

GRUP = {
    "brand": ("gameplus", "game plus", "game+"),
    "gfn": ("geforce now", "gfn", "geforcenow"),
}


def seri(grup):
    """grup -> {yil_ay: hacim}"""
    return {y: sum(TERIM[t][i] for t in GRUP[grup]) for i, y in enumerate(AYLAR)}


if __name__ == "__main__":
    b, g = seri("brand"), seri("gfn")
    print(f"{'Ay':8}{'Brand':>10}{'GFN':>10}")
    for y in AYLAR:
        print(f"{y:<8}{b[y]:>10,}{g[y]:>10,}")
    print(f"\nBrand YoY: {(b[202607]/b[202507]-1)*100:+.1f}%")
    print(f"GFN   YoY: {(g[202607]/g[202507]-1)*100:+.1f}%")
