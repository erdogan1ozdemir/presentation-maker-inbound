# -*- coding: utf-8 -*-
"""Game+ marka ve GFN aylık arama hacmi (TR, Tem'25 - Tem'26).

Kaynak: DataForSEO · keywords_data/google_ads/search_volume/live
        location_code=2792 (Türkiye) · language_code=tr · search_partners=false
        date_from=2025-07-01 · date_to=2026-07-31 · çekim: 14.08.2026

Terim kümesi GSC segment regex'leriyle aynı:
  brand = gameplus + game plus + game+
  gfn   = geforce now + gfn + geforcenow

YAKIN VARYANT BİRLEŞMESİ - toplama dahil edilmeyen terimler
-----------------------------------------------------------
Google Ads yakın varyantları tek keyword sayıyor; DataForSEO bu yüzden
"gameplus" ile "game plus" için ve "geforce now" ile "geforcenow" için
13 ayın tamamında BİREBİR AYNI seriyi döndürüyor. İki seriyi toplamak
hacmi iki kat gösterir, bu yüzden her çiftten yalnızca biri sayılır:

  brand toplamı = gameplus + game+           ("game plus" mükerrer)
  gfn toplamı   = geforce now + gfn          ("geforcenow" mükerrer)

BANT (BUCKET) ETKİSİ
--------------------
Google Ads hacmi bant halinde döndürür; değerler 2.900 / 3.600 / 4.400 /
5.400 ve 60.500 / 74.000 / 90.500 / 110.000 gibi basamaklarda kümelenir.
Bu yüzden ay bazında YoY yazılmaz, ısı haritası kullanılmaz; değişim dönem
uçları üzerinden verilir ve bandın varlığı dipnotta belirtilir.
"""

AYLAR = [202507, 202508, 202509, 202510, 202511, 202512,
         202601, 202602, 202603, 202604, 202605, 202606, 202607]

# DataForSEO ham çıktısı (monthly_searches), terim başına 13 ay
TERIM = {
    "gameplus":    [4400, 4400, 4400, 4400, 5400, 5400, 4400, 3600, 3600, 2900, 3600, 2900, 2900],
    "game plus":   [4400, 4400, 4400, 4400, 5400, 5400, 4400, 3600, 3600, 2900, 3600, 2900, 2900],
    "game+":       [1000, 1000, 1000, 1000, 1300, 1000, 1300, 1000, 1000, 880, 1000, 1000, 880],
    "geforce now": [90500, 90500, 74000, 74000, 90500, 110000, 90500, 60500, 74000,
                    60500, 60500, 60500, 60500],
    "gfn":         [1900, 1900, 1900, 1900, 1900, 2400, 1900, 1600, 1900, 1600, 1600, 1300, 1000],
    "geforcenow":  [90500, 90500, 74000, 74000, 90500, 110000, 90500, 60500, 74000,
                    60500, 60500, 60500, 60500],
}

# Toplama giren terimler: yakın varyant çiftlerinden yalnızca biri
GRUP = {
    "brand": ("gameplus", "game+"),
    "gfn": ("geforce now", "gfn"),
}
MUKERRER = {"game plus": "gameplus", "geforcenow": "geforce now"}


def seri(grup):
    """grup -> {yil_ay: hacim}"""
    return {y: sum(TERIM[t][i] for t in GRUP[grup]) for i, y in enumerate(AYLAR)}


def mukerrer_denetimi():
    """Yakın varyant çiftleri gerçekten aynı seriyi mi taşıyor? Yeni çekimde
    ayrışırlarsa toplama dahil edilme kararı yeniden verilmelidir."""
    ayni = {k: TERIM[k] == TERIM[v] for k, v in MUKERRER.items()}
    return ayni


if __name__ == "__main__":
    print("yakın varyant denetimi:", mukerrer_denetimi())
    b, g = seri("brand"), seri("gfn")
    print(f"\n{'Ay':8}{'Brand':>10}{'GFN':>10}")
    for y in AYLAR:
        print(f"{y:<8}{b[y]:>10,}{g[y]:>10,}")
    print(f"\nBrand Tem'25 -> Tem'26: {b[202507]:,} -> {b[202607]:,} "
          f"({(b[202607]/b[202507]-1)*100:+.1f}%)")
    print(f"GFN   Tem'25 -> Tem'26: {g[202507]:,} -> {g[202607]:,} "
          f"({(g[202607]/g[202507]-1)*100:+.1f}%)")
