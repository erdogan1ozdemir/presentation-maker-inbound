# -*- coding: utf-8 -*-
"""Özdilekteyim arama hacmi (TR, Haz'25 - Ağu'26) - destede tek hacim kaynağı.

Kaynak: DataForSEO · keywords_data/google_ads/search_volume/live
        location_code=2792 (Türkiye) · language_code=tr · search_partners=false
        78 keyword tek talepte · çekim: 15.09.2026 · ham: ham/dfs_hacim.json
        Haz-Tem 2025 (yalnız marka terimleri, 15 aylık GSC serisiyle eşleşme için):
        ham/dfs_hacim_ek.json · çekim 24.09.2026 · örtüşen aylar birebir aynı

YAKIN VARYANT BİRLEŞMESİ
------------------------
Google Ads yakın varyantları tek keyword sayar. "özdilek", "ozdilek", "öz dilek"
ve "özdikek" 13 ayın tamamında birebir aynı seriyi döndürdüğü için marka
satırında yalnızca "özdilek" kullanılır. "özdilekteyim" ayrı satırdır;
"ozdilekteyim" ASCII yazımı destede kullanılmaz.

BANT ETKİSİ
-----------
Değerler bant halinde döner (60.500 / 74.000 / 90.500 ...). Ay bazında YoY
yazılmaz; dönem uçları karşılaştırılır. Hacmi 0 dönen keyword'ler (kabin boy
valiz, orta boy valiz) tabloda "-" gösterilir.
"""
import json
from pathlib import Path

HAM = Path(__file__).parent / "ham" / "dfs_hacim.json"
AYLAR = [202506, 202507, 202508, 202509, 202510, 202511, 202512, 202601, 202602,
         202603, 202604, 202605, 202606, 202607, 202608]


def _yukle():
    t = HAM.read_text(encoding="utf-8")
    d = json.loads(t[t.find("{"):])
    res = d["tasks"][0]["result"] if "tasks" in d else d["result"]
    out = {}
    for r in res:
        ms = {m["year"] * 100 + m["month"]: (m["search_volume"] or 0)
              for m in (r["monthly_searches"] or [])}
        out[r["keyword"]] = [ms.get(y, 0) for y in AYLAR]
    ek = json.loads((HAM.parent / "dfs_hacim_ek.json").read_text(encoding="utf-8"))["aylik"]
    for kw, aylar in ek.items():
        if kw in out:
            for y, v in aylar.items():
                out[kw][AYLAR.index(int(y))] = v
    return out


TERIM = _yukle()
# Marka terimleri ayrı satırda verilir, toplanmaz. "ozdilekteyim" (ASCII yazım)
# markanın tercihiyle destede kullanılmaz (reference/ozdilekteyim/README.md).
MARKA = ("özdilek", "özdilekteyim")
HARIC = {"ozdilek", "ozdilekteyim"}
MUKERRER = {"ozdilek": "özdilek", "öz dilek": "özdilek", "özdikek": "özdilek"}


def seri(terimler=MARKA):
    return {y: sum(TERIM[t][i] for t in terimler) for i, y in enumerate(AYLAR)}


def hacim(kw, ay=202608):
    """Keyword'ün ilgili aydaki hacmi; veri yoksa None."""
    v = TERIM.get(kw)
    if not v or kw in HARIC:
        return None
    x = v[AYLAR.index(ay)]
    return x or None


def mukerrer_denetimi():
    return {k: TERIM[k] == TERIM[v] for k, v in MUKERRER.items()}


if __name__ == "__main__":
    print("yakın varyant:", mukerrer_denetimi())
    m = seri()
    for y in AYLAR:
        print(y, f"{m[y]:,}", {t: TERIM[t][AYLAR.index(y)] for t in MARKA})
    print(f"marka Ağu'25 -> Ağu'26: {m[202508]:,} -> {m[202608]:,} ({(m[202608]/m[202508]-1)*100:+.1f}%)")
