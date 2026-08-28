# -*- coding: utf-8 -*-
"""Game+ Temmuz 2026 SEO değerlendirme destesi (revize sürüm)."""
import collections
import datetime as dt
import json
import sys
from pathlib import Path

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE / "veri"))
from ek_veri import ai_segment, etiket as ek_etiket, haftalik, oyun_gsc  # noqa: E402
from ga4 import etiket as ga_etiket, yukle, ym  # noqa: E402
from gsc_segment import etiket as gsc_etiket, seriler  # noqa: E402
from hacim import seri as hacim_seri  # noqa: E402

AYLAR, SEG = seriler()
ET = [gsc_etiket(y) for y in AYLAR]
_HAM = yukle()
G = [r for r in _HAM if not r["kirli"]]
KIRLI = [r for r in _HAM if r["kirli"]]
GA_AYLAR = sorted({ym(r) for r in G})
GA_ET = [ga_etiket(y) for y in GA_AYLAR]


def ga(f):
    c = collections.Counter()
    for r in G:
        if f(r):
            c[ym(r)] += r["session"]
    return c


TOPLAM_S = ga(lambda r: True)
ORGANIK_S = ga(lambda r: r["kanal"] == "Organic Search")
BLOG_S = ga(lambda r: r["lp"].startswith("/blog"))
BLOG_ORG = ga(lambda r: r["lp"].startswith("/blog") and r["kanal"] == "Organic Search")
AI_S = ai_segment()
OYUN_G = oyun_gsc()
HAFTA = haftalik()


def k(v):
    return f"{v/1_000_000:.2f}M" if v >= 1_000_000 else f"{v/1000:.1f}K"


def n(v):
    return f"{v:,}".replace(",", ".")


def pct(a, b, kucuk_taban=10):
    """Yüzde değişim. Taban çok küçükse oran yanıltıcı olur; mutlak fark verilir."""
    if not b:
        return "yeni" if a else "-"
    if b < kucuk_taban:
        return f"{a - b:+d}"
    v = (a / b - 1) * 100
    return f"{'+' if v >= 0 else '-'}%{abs(v):.1f}"


T = dict(font_pt=10.5, row_h=20, head_h=24)
S = []
S.append({"type": "cover", "title": "Game+ SEO Değerlendirme", "subtitle": "Temmuz 2026"})
S.append({"type": "agenda", "kicker": "Temmuz 2026",
          "title_lines": ["SUNUM", "AKIŞI"], "items": []})

# ============================================================ 01 genel görünüm
S.append({"type": "separator", "no": "01", "title": "Genel Görünüm"})
S.append({
    "type": "content",
    "breadcrumb": ["GENEL GÖRÜNÜM", "Yönetici Özeti"],
    "title": "Non-Brand Büyürken Brand ve GFN Talebi Daralıyor",
    "subtitle": "Temmuz 2026 | Search Console tüm cihazlar, GA4 tüm kanallar",
    "source": "Google Search Console & GA4",
    "grid": [100],
    "blocks": [
        {"type": "kpi", "col": "full", "cols": 4, "h": 112, "cards": [
            {"value": k(SEG["total"][202607]["click"]), "label": "Organik click",
             "deltas": [{"label": "MoM", "value": pct(SEG["total"][202607]["click"], SEG["total"][202606]["click"])},
                        {"label": "YoY", "value": pct(SEG["total"][202607]["click"], SEG["total"][202507]["click"])}]},
            {"value": k(SEG["total"][202607]["impr"]), "label": "Impression",
             "deltas": [{"label": "MoM", "value": pct(SEG["total"][202607]["impr"], SEG["total"][202606]["impr"])},
                        {"label": "YoY", "value": pct(SEG["total"][202607]["impr"], SEG["total"][202507]["impr"])}]},
            {"value": k(TOPLAM_S[202607]), "label": "Toplam session",
             "deltas": [{"label": "MoM", "value": pct(TOPLAM_S[202607], TOPLAM_S[202606])},
                        {"label": "YoY", "value": pct(TOPLAM_S[202607], TOPLAM_S[202507])}],
             "accent": "coral"},
            {"value": k(ORGANIK_S[202607]), "label": "Organik session",
             "deltas": [{"label": "MoM", "value": pct(ORGANIK_S[202607], ORGANIK_S[202606])},
                        {"label": "YoY", "value": pct(ORGANIK_S[202607], ORGANIK_S[202507])}],
             "accent": "coral"},
        ]},
        {"type": "insights", "col": "full", "mt": 14, "font_pt": 10.5, "items": [
            "Organik click yıllık bazda {g:+%44.6}, impression {g:+%106.7} artmıştır. Büyümenin tamamı {c:non-brand} tarafından gelmektedir: click {g:+%56.1}, impression {g:+%110.3}.",
            "{c:Brand} sorgularında click {r:-%30.6} gerilemiş, impression {b:yatay} kalmıştır. {c:GFN} tarafında hem click {r:-%64.1} hem impression {r:-%30.8} daralmıştır.",
            "Click'in {b:%93.6}'sı non-brand sorgulardan gelmektedir; GFN grubu toplam click'in {b:%15.0}'ini kapsamaktadır.",
        ]},
        {"type": "note", "col": "full", "mt": 14, "label": "KRİTİK TESPİT",
         "text": "Brand ve GFN daralırken toplam trafiğin artması, büyümenin marka talebinden değil kategori içeriğinden geldiğini göstermektedir. SSR geçişi ve blog çalışmasının etkisi bu eksende okunmaktadır; marka tarafındaki daralma ise ayrı bir izleme başlığıdır."},
    ],
})

S.append({
    "type": "content",
    "breadcrumb": ["GENEL GÖRÜNÜM", "Yöntem"],
    "title": "Segment Tanımları",
    "subtitle": "Sorgu segmentleri, GSC dashboard projesindeki hesapla aynı yöntemle kurulmuştur",
    "source": "Google Search Console - sc-domain:gameplus.com.tr",
    "grid": [100],
    "blocks": [
        {"type": "panels", "col": "full", "cols": 3, "items": [
            {"title": "Brand", "sub": "doğrudan ölçülür",
             "lines": ["Query içinde şu ifadeler geçen sorgular:",
                       "\"gameplus\" · \"game plus\" · \"game+\"",
                       "GSC regex filtresiyle ölçülür."]},
            {"title": "Non-Brand", "sub": "toplamdan çıkarılır",
             "lines": ["Toplam eksi brand olarak hesaplanır.",
                       "Query filtresi uygulandığında anonim sorgular sonuç kümesinden düştüğü için bu hacim non-brand satırında yer alır.",
                       "Pozisyon değeri ayrıca ölçülür."]},
            {"title": "GFN", "sub": "kesişen grup",
             "lines": ["Query içinde şu ifadeler geçen sorgular:",
                       "\"gfn\" · \"geforce now\" · \"geforcenow\"",
                       "Brand ve non-brand'in üzerine biner; üç grubun toplamı toplam click'e eşit değildir."]},
        ]},
        {"type": "insights", "col": "full", "mt": 16, "font_pt": 11, "items": [
            "Brand ve Non-Brand birbirini tamamlar, toplamları toplam click'i verir. GFN ise kesişen bir gruptur: bir sorgu hem brand hem GFN olabilir ({b:\"gameplus geforce now\"} gibi).",
            "Ayrım, marka talebi ile kategori talebini birbirinden ayırmak ve GeForce NOW kaynaklı hareketi ayrıca izleyebilmek için kurulmuştur.",
        ]},
    ],
})

# ================================================ 02 Google Search Console
S.append({"type": "separator", "no": "02", "title": "Google Search Console Metrikleri"})


def seg_seri(metrik, baslik, dipnot, yorum):
    return {
        "type": "content",
        "breadcrumb": ["SEARCH CONSOLE", "Aylık Seri"],
        "title": baslik,
        "subtitle": "Tem 2025 - Tem 2026 | 13 aylık seri | Search Console",
        "source": "Google Search Console - sc-domain:gameplus.com.tr",
        "grid": [100],
        "footnotes": [dipnot,
                      "Isı haritasında satırın en yüksek ayı yeşil, en düşük ayı kırmızı gösterilmektedir."],
        "blocks": [
            {"type": "combo", "col": "full", "h": 158, "bar_w": 24, "cats": ET, "series": [
                {"kind": "bar", "name": "Toplam", "data": [SEG["total"][y][metrik] for y in AYLAR],
                 "color": "gray_bar", "axis": "left"},
                {"kind": "line", "name": "Non-Brand", "data": [SEG["nonbrand"][y][metrik] for y in AYLAR],
                 "color": "teal", "axis": "left"},
                {"kind": "line", "name": "GFN", "data": [SEG["gfn"][y][metrik] for y in AYLAR],
                 "color": "coral", "axis": "right"},
                {"kind": "line", "name": "Brand", "data": [SEG["brand"][y][metrik] for y in AYLAR],
                 "color": "gold", "axis": "right"},
            ]},
            dict({"type": "table", "col": "full", "mt": 10, "first_col_max": 0.10, "heat": True,
                  "head": ["Segment"] + ET,
                  "rows": [["GFN"] + [k(SEG["gfn"][y][metrik]) for y in AYLAR],
                           ["Brand"] + [k(SEG["brand"][y][metrik]) for y in AYLAR],
                           ["Non-Brand"] + [k(SEG["nonbrand"][y][metrik]) for y in AYLAR],
                           ["Toplam"] + [k(SEG["total"][y][metrik]) for y in AYLAR]],
                  "bold_rows": [-1]}, **T),
            {"type": "insights", "col": "full", "mt": 10, "font_pt": 10.5, "items": [yorum]},
        ],
    }


S.append(seg_seri("click", "Brand, Non-Brand ve GFN Aylık Click",
                  "Toplam satırı Brand ile Non-Brand'in toplamıdır; GFN kesişen grup olduğu için toplama dahil değildir.",
                  "Toplam click Mart-Mayıs döneminde {b:25-28K} bandına çıkmış, Temmuz'da {b:23.7K} seviyesindedir. "
                  "Seriyi non-brand taşımaktadır; {c:GFN} {r:16.9K → 3.6K} ve {c:Brand} {r:2.2K → 1.5K} ile daralmaktadır."))
S.append(seg_seri("impr", "Brand, Non-Brand ve GFN Aylık Impression",
                  "Brand ve GFN ölçekleri Non-Brand'in yanında küçük kaldığı için grafikte sağ eksende verilmiştir.",
                  "Toplam impression {g:363.9K → 752.3K} ile iki katından fazla artmıştır; artışın tamamı non-brand tarafındadır. "
                  "{c:Brand} {b:11.8K → 11.6K} ile yatay kalmış, {c:GFN} {r:141.5K → 97.9K} ile daralmıştır."))

HACIM_B, HACIM_G = hacim_seri("brand"), hacim_seri("gfn")
# yari genislikteki grafikte 13 kategori sigmadigi icin yil eki dusurulur;
# donem alt baslikta zaten beyan ediliyor
ET_KISA = [e[:3] for e in ET]
S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Arama Hacmi"],
    "title": "Brand ve GFN Aylık Arama Hacmi",
    "subtitle": "Tem 2025 - Tem 2026 | Türkiye | arama hacmi ile organik click yan yana",
    "source": "Google Ads Keyword Planner & Google Search Console",
    "grid": [50, 50],
    "footnotes": [
        "Terim kümesi Search Console segmentleriyle aynıdır: brand \"gameplus\" · \"game+\", "
        "GFN \"geforce now\" · \"gfn\". Google Ads yakın varyantları tek keyword saydığı için "
        "\"game plus\" ve \"geforcenow\" aynı seriyi taşımaktadır; çift sayım oluşmaması adına "
        "her çiftten biri toplama dahil edilmiştir.",
        "Arama hacmi bant halinde döndüğü için değerler belirli basamaklarda kümelenmektedir; "
        "ay bazında değişim yerine dönem uçları karşılaştırılmıştır. Grafiklerde hacim sol eksende, "
        "click sağ eksendedir.",
    ],
    "blocks": [
        {"type": "combo", "col": 0, "h": 142, "bar_w": 14, "cats": ET_KISA, "series": [
            {"kind": "bar", "name": "Game+ arama hacmi", "data": [HACIM_B[y] for y in AYLAR],
             "color": "gray_bar", "axis": "left"},
            {"kind": "line", "name": "Brand click", "data": [SEG["brand"][y]["click"] for y in AYLAR],
             "color": "gold", "axis": "right"},
        ]},
        {"type": "combo", "col": 1, "h": 142, "bar_w": 14, "cats": ET_KISA, "series": [
            {"kind": "bar", "name": "GFN arama hacmi", "data": [HACIM_G[y] for y in AYLAR],
             "color": "gray_bar", "axis": "left"},
            {"kind": "line", "name": "GFN click", "data": [SEG["gfn"][y]["click"] for y in AYLAR],
             "color": "coral", "axis": "right"},
        ]},
        dict({"type": "table", "col": "full", "mt": 12, "first_col_max": 0.13,
              "head": ["Arama hacmi"] + ET,
              "rows": [["GFN"] + [k(HACIM_G[y]) for y in AYLAR],
                       ["Brand"] + [k(HACIM_B[y]) for y in AYLAR]]}, **T),
        {"type": "insights", "col": "full", "mt": 10, "font_pt": 10, "items": [
            f"GFN arama hacmi {{r:{k(HACIM_G[202507])} → {k(HACIM_G[202607])}}} ile "
            f"{{r:{pct(HACIM_G[202607], HACIM_G[202507])}}} daralmıştır; aynı dönemde GFN click "
            f"{{r:{pct(SEG['gfn'][202607]['click'], SEG['gfn'][202507]['click'])}}} gerilemiştir. "
            f"Talep daralması düşüşün bir bölümünü açıklamaktadır.",
            f"Brand tarafında hacim {{r:{k(HACIM_B[202507])} → {k(HACIM_B[202607])}}} "
            f"({{r:{pct(HACIM_B[202607], HACIM_B[202507])}}}) ile daralırken brand click "
            f"{{r:{pct(SEG['brand'][202607]['click'], SEG['brand'][202507]['click'])}}} gerilemiştir. "
            f"İki oranın örtüşmesi, marka sorgularındaki düşüşün ağırlıkla talep kaynaklı olduğuna "
            f"işaret etmektedir.",
        ]},
    ],
})

HEAD = ["Tem 25", "Haz 26", "Tem 26", "MoM", "YoY"]


def seg_rows(metrik):
    out = []
    for seg, ad in (("gfn", "GFN"), ("brand", "Brand"),
                    ("nonbrand", "Non-Brand"), ("total", "Toplam")):
        a = SEG[seg]
        out.append([ad, k(a[202507][metrik]), k(a[202606][metrik]), k(a[202607][metrik]),
                    pct(a[202607][metrik], a[202606][metrik]),
                    pct(a[202607][metrik], a[202507][metrik])])
    return out


def poz_rows():
    out = []
    for seg, ad in (("gfn", "GFN"), ("brand", "Brand"),
                    ("nonbrand", "Non-Brand"), ("total", "Toplam")):
        a = SEG[seg]
        p5, ph, pt_ = a[202507]["poz"], a[202606]["poz"], a[202607]["poz"]
        out.append([ad, f"{p5:.1f}", f"{ph:.1f}", f"{pt_:.1f}",
                    f"{ph - pt_:+.1f}", f"{p5 - pt_:+.1f}"])
    return out


S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Dönem Karşılaştırması"],
    "title": "Brand, Non-Brand ve GFN Temmuz Karşılaştırması",
    "subtitle": "Temmuz 2026 & Haziran 2026 (MoM) & Temmuz 2025 (YoY)",
    "source": "Google Search Console - sc-domain:gameplus.com.tr",
    "grid": [50, 50],
    "footnotes": [
        "Non-Brand pozisyonu, marka ifadelerinin regex ile dışlandığı ayrı bir ölçümden alınmıştır; click ve impression ise toplamdan çıkarma ile hesaplanır. İki yöntemin kapsamı farklıdır: query filtresi uygulandığında anonim sorgular sonuç kümesinden düşer. Pozisyonda pozitif değer iyileşmedir.",
    ],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.28,
              "head": ["Click"] + HEAD, "rows": seg_rows("click"), "bold_rows": [-1]}, **T),
        dict({"type": "table", "col": 1, "first_col_max": 0.28,
              "head": ["Impression"] + HEAD, "rows": seg_rows("impr"), "bold_rows": [-1]}, **T),
        dict({"type": "table", "col": 0, "mt": 8, "first_col_max": 0.28,
              "head": ["Ort. pozisyon"] + HEAD, "rows": poz_rows(), "bold_rows": [-1]}, **T),
        {"type": "insights", "col": 1, "mt": 8, "font_pt": 10.5, "items": [
            "Toplam click MoM {g:+%5.3}, YoY {g:+%44.6} artmıştır. Brand click MoM {g:+%17.4} toparlanmış olsa da yıllık bazda {r:-%30.6} geridedir.",
            "Ortalama pozisyon toplamda {g:18.8 → 6.9}, non-brand tarafında {g:21.3 → 7.4} ile belirgin iyileşme göstermektedir. Brand tarafında ise gerileme bulunmaktadır; GFN sıralaması yatay seyretmektedir.",
        ]},
    ],
})

BRAND_RE = ("gameplus", "game plus", "game+")
GFN_RE = ("gfn", "geforce now", "geforcenow", "ge force now")


def sinif(q):
    ql = q.lower()
    if any(x in ql for x in BRAND_RE):
        return "Brand"
    if any(x in ql for x in GFN_RE):
        return "GFN"
    return "Non-Brand"


SORGU = [
    ("call of duty serisi", 637, 1063, 2.4, 1.9), ("gameplus", 610, 744, 2.2, 1.9),
    ("oyunlar", 38, 127, 24.1, 10.1), ("ubisoft plus", 21, 93, 4.8, 4.7),
    ("cod serisi", 119, 187, 2.7, 2.1), ("ubisoft+", 14, 63, 4.5, 4.0),
    ("açık dünya oyunları", 49, 85, 4.9, 2.9), ("assassin's creed serisi", 20, 51, 6.8, 4.4),
    ("indie oyunlar", 10, 26, 9.7, 4.5), ("god of war serileri", 9, 24, 4.1, 1.8),
    ("pc oyunları", 333, 237, 5.4, 6.5), ("bilgisayar oyunları", 180, 116, 7.0, 7.3),
    ("resident evil oynama sırası", 75, 25, 2.1, 2.6), ("mmorpg", 467, 417, 2.7, 2.9),
    ("demo oyna", 82, 44, 1.3, 2.0), ("gameplus geforce now", 51, 19, 1.2, 1.2),
    ("geforce now üyelik", 52, 28, 5.2, 6.9),
    ("resident evil kronolojik sıra", 35, 11, 2.1, 5.7),
    ("call of duty black ops serisi", 24, 14, 1.9, 5.0),
]
artan = sorted([s for s in SORGU if s[2] > s[1]], key=lambda s: -(s[2] - s[1]))[:7]
azalan = sorted([s for s in SORGU if s[2] < s[1]], key=lambda s: (s[2] - s[1]))[:7]

S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Sorgu Hareketleri"],
    "title": "Click Değişimi En Yüksek Sorgular",
    "subtitle": "Temmuz 2026 & Haziran 2026 | MoM | segment ayrımlı",
    "source": "Google Search Console - sc-domain:gameplus.com.tr · Query kırılımı",
    "grid": [50, 50],
    "footnotes": [
        "Segment sütunu, sorgunun brand, GFN ya da non-brand ifadelerinden hangisini içerdiğini gösterir.",
    ],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.44,
              "head": ["Click artan", "Segment", "Haz", "Tem", "Δ"],
              "rows": [[q, sinif(q), n(h), n(t), f"+{t-h}"] for q, h, t, _a, _b in artan]}, **T),
        dict({"type": "table", "col": 1, "first_col_max": 0.44,
              "head": ["Click azalan", "Segment", "Haz", "Tem", "Δ"],
              "rows": [[q, sinif(q), n(h), n(t), f"{t-h}"] for q, h, t, _a, _b in azalan]}, **T),
        {"type": "insights", "col": "full", "mt": 12, "font_pt": 10.5, "items": [
            "Artışın merkezinde {c:call of duty serisi} ({g:+426}) ve marka sorgusu {c:gameplus} ({g:+134}) bulunmaktadır. {c:ubisoft plus} ve {c:ubisoft+} birlikte {g:+121} click getirmiş; Temmuz'da tamamlanan Ubisoft+ çalışmasıyla örtüşmektedir.",
            "Düşüşler jenerik oyun sorgularında yoğunlaşmaktadır ({c:pc oyunları} {r:-96}, {c:bilgisayar oyunları} {r:-64}); bu sorgularda pozisyon da gerilemiştir.",
        ]},
    ],
})

poz_iyi = sorted(SORGU, key=lambda s: -(s[3] - s[4]))[:7]
poz_kotu = sorted(SORGU, key=lambda s: (s[3] - s[4]))[:7]
S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Sıralama Hareketleri"],
    "title": "Sıralaması En Çok Değişen Sorgular",
    "subtitle": "Temmuz 2026 & Haziran 2026 | MoM | ortalama pozisyon",
    "source": "Google Search Console - sc-domain:gameplus.com.tr · Query kırılımı",
    "grid": [50, 50],
    "footnotes": [
        "Pozisyonda pozitif değer iyileşmedir (24.1 → 10.1 = +14.1). Tablo, click hareketi en yüksek sorgu kümesi içinden sıralama değişimine göre seçilmiştir.",
    ],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.44,
              "head": ["Sıralaması iyileşen", "Segment", "Haz", "Tem", "Δ"],
              "rows": [[q, sinif(q), f"{a:.1f}", f"{b:.1f}", f"{a-b:+.1f}"]
                       for q, _h, _t, a, b in poz_iyi]}, **T),
        dict({"type": "table", "col": 1, "first_col_max": 0.44,
              "head": ["Sıralaması gerileyen", "Segment", "Haz", "Tem", "Δ"],
              "rows": [[q, sinif(q), f"{a:.1f}", f"{b:.1f}", f"{a-b:+.1f}"]
                       for q, _h, _t, a, b in poz_kotu]}, **T),
        {"type": "insights", "col": "full", "mt": 12, "font_pt": 10.5, "items": [
            "En belirgin sıralama kazanımı {c:oyunlar} sorgusundadır ({g:24.1 → 10.1}); aynı sorguda click {g:+89} artmıştır. {c:indie oyunlar} ve {c:açık dünya oyunları} da ilk sayfaya taşınmıştır.",
            "Gerilemeler kalıcı içerik sorgularında dikkat çekmektedir: {c:resident evil kronolojik sıra} {r:2.1 → 5.7} ve {c:call of duty black ops serisi} {r:1.9 → 5.0}. Bu iki başlığın güncellenmesi ele alınabilir.",
        ]},
    ],
})

SAYFA_H = [
    ("/blog/call-of-duty-oyunlarinin-kronolojik-sirasi", 3341, 3987),
    ("/ (anasayfa)", 3421, 3753), ("/ubisoft", 97, 372),
    ("/blog/en-iyi-zombie-oyunlari-pc", 170, 318),
    ("/blog/2026-turkce-dublajli-ve-altyazili-oyunlar", 269, 408),
    ("/destek", 377, 514), ("/ubisoft/paketler", 23, 111),
    ("/gfn/oyunlar/oynamasi-ucretsiz", 2684, 1941),
    ("/blog/resident-evil-serisi-kronolojik-siralama", 810, 436),
    ("/blog/2026-oyun-takvimi", 787, 539),
    ("/blog/tomb-raider-oyun-sirasi", 344, 254),
    ("/firsatlar", 457, 384), ("/blog/007-first-light-fiyati", 90, 10),
]
s_artan = sorted([s for s in SAYFA_H if s[2] > s[1]], key=lambda s: -(s[2] - s[1]))[:6]
s_azalan = sorted([s for s in SAYFA_H if s[2] < s[1]], key=lambda s: (s[2] - s[1]))[:6]
S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Sayfa Hareketleri"],
    "title": "Click Değişimi En Yüksek Sayfalar",
    "subtitle": "Temmuz 2026 & Haziran 2026 | MoM | click değişimine göre sıralı",
    "source": "Google Search Console - sc-domain:gameplus.com.tr · Page kırılımı",
    "grid": [50, 50],
    "footnotes": [
        "URL'ler kök alan adı çıkarılarak kısaltılmıştır; tamamı gameplus.com.tr altındadır.",
    ],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.50,
              "head": ["Click artan sayfa", "Haz", "Tem", "Δ"],
              "rows": [[p[:42], n(h), n(t), f"+{t-h}"] for p, h, t in s_artan]}, **T),
        dict({"type": "table", "col": 1, "first_col_max": 0.50,
              "head": ["Click azalan sayfa", "Haz", "Tem", "Δ"],
              "rows": [[p[:42], n(h), n(t), f"{t-h}"] for p, h, t in s_azalan]}, **T),
        {"type": "insights", "col": "full", "mt": 12, "font_pt": 10.5, "items": [
            "{c:/ubisoft} sayfası {g:+275} click ile en yüksek oransal artışı göstermiştir ({g:+%283.5}); paketler sayfası da {g:+88} click eklemiştir.",
            "En büyük düşüş {c:/gfn/oyunlar/oynamasi-ucretsiz} sayfasındadır ({r:-743}); aynı sayfada pozisyon {r:9.9 → 11.1} gerilemiştir.",
        ]},
    ],
})

# ============================================================== 03 SSR
S.append({"type": "separator", "no": "03", "title": "SSR Geçişi Etkisi"})
GECIS = dt.date(2026, 2, 9)
h_idx = next(i for i, h in enumerate(HAFTA) if h["hafta"] == GECIS)
pencere = HAFTA[max(0, h_idx - 16):h_idx + 17]
cats, once_c, sonra_c, once_p, sonra_p = [], [], [], [], []
for h in pencere:
    cats.append(ek_etiket(h["hafta"].year * 100 + h["hafta"].month)[:3] if h["hafta"].day <= 7 else "")
    poz = round(h["poz"], 1)
    if h["hafta"] < GECIS:
        once_c.append(h["click"]); sonra_c.append(0)
        once_p.append(poz); sonra_p.append(None)
    else:
        once_c.append(0); sonra_c.append(h["click"])
        once_p.append(None); sonra_p.append(poz)
# iki cizgi gecis haftasinda birlesir: sinir noktasi her iki seride de yer alir
_g = next(i for i, h in enumerate(pencere) if h["hafta"] >= GECIS)
if _g:
    sonra_p[_g - 1] = once_p[_g - 1]

S.append({
    "type": "content",
    "breadcrumb": ["SSR GEÇİŞİ", "Öncesi ve Sonrası"],
    "title": "SSR Geçişi Öncesi ve Sonrası Organik Performans",
    "subtitle": "Geçiş: 8-14 Şubat 2026 | simetrik 180'er günlük pencere, geçiş haftası hariç",
    "source": "Google Search Console - sc-domain:gameplus.com.tr",
    "grid": [50, 50],
    "footnotes": [
        "Öncesi: 12 Ağu 2025 - 7 Şub 2026 (180 gün). Sonrası: 15 Şub - 13 Ağu 2026 (180 gün). Geçiş haftası iki pencereye de dahil edilmemiştir.",
        "Grafik, geçişin 16 hafta öncesi ve 16 hafta sonrasını haftalık toplamlarla gösterir; hem bar hem pozisyon çizgisi rengindeki değişim geçiş haftasını işaretler. Pozisyon çizgisi ters eksenlidir, yükselen çizgi iyileşmedir. Kategori etiketleri ay başlarında verilmiştir.",
    ],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.40,
              "head": ["Metrik", "Öncesi", "Sonrası", "Değişim"],
              "rows": [["Click", "114.2K", "144.1K", "+%26.2"],
                       ["Impression", "2.59M", "4.26M", "+%64.7"],
                       ["CTR", "%4.42", "%3.38", "-1.03p"],
                       ["Ort. pozisyon", "12.09", "7.60", "+4.49"]]}, **T),
        {"type": "insights", "col": 1, "font_pt": 10.5, "items": [
            "Geçiş sonrası impression {g:+%64.7}, click {g:+%26.2} artmış; ortalama pozisyon {g:12.09 → 7.60} ile {g:4.49 puan} iyileşmiştir.",
            "CTR {r:-1.03p} gerilemiştir. Gösterim tıklamadan hızlı büyüdüğü için oran düşmüştür; ayrıca aynı dönemde {c:AI Overview} sonuç sayfalarında yaygınlaşmış ve klasik sonuç listesinin üstünde yer almaya başlamıştır. İki etki birlikte okunmalıdır.",
        ]},
        {"type": "combo", "col": "full", "mt": 12, "h": 178, "bar_w": 11, "cats": cats,
         "series": [
            {"kind": "bar", "name": "Click · SSR öncesi", "data": once_c, "color": "gray_bar", "axis": "left"},
            {"kind": "bar", "name": "Click · SSR sonrası", "data": sonra_c, "color": "coral", "axis": "left"},
            {"kind": "line", "name": "Ort. pozisyon · SSR öncesi", "data": once_p, "color": "ink3",
             "axis": "right", "invert": True, "fmt": "pos"},
            {"kind": "line", "name": "Ort. pozisyon · SSR sonrası", "data": sonra_p, "color": "teal",
             "axis": "right", "invert": True, "fmt": "pos"},
        ]},
    ],
})

# ============================================================== 04 GA4
S.append({"type": "separator", "no": "04", "title": "GA4 Trafik"})
S.append({
    "type": "content",
    "breadcrumb": ["GA4", "Aylık Trafik"],
    "title": "Toplam ve Organik Session Aylık Seyri",
    "subtitle": "Tem 2025 - Tem 2026 | GA4 tüm kanallar ve Organic Search",
    "source": "GA4 - Cloud Gaming",
    "grid": [100],
    "footnotes": [
        "Tarama aracı kaynaklı bozuk landing page kayıtları ayıklanmıştır; ayrıntı blog slaytının dipnotundadır.",
        "Isı haritasında satırın en yüksek ayı yeşil, en düşük ayı kırmızı gösterilmektedir.",
    ],
    "blocks": [
        {"type": "combo", "col": "full", "h": 190, "bar_w": 30, "cats": GA_ET, "series": [
            {"kind": "bar", "name": "Toplam session", "data": [TOPLAM_S[y] for y in GA_AYLAR],
             "color": "gray_bar", "axis": "left"},
            {"kind": "line", "name": "Organik session", "data": [ORGANIK_S[y] for y in GA_AYLAR],
             "color": "coral", "axis": "right"},
        ]},
        dict({"type": "table", "col": "full", "mt": 10, "first_col_max": 0.12, "heat": True,
              "head": ["Metrik"] + GA_ET,
              "rows": [["Toplam"] + [k(TOPLAM_S[y]) for y in GA_AYLAR],
                       ["Organik"] + [k(ORGANIK_S[y]) for y in GA_AYLAR]]}, **T),
        {"type": "insights", "col": "full", "mt": 10, "font_pt": 10.5, "items": [
            f"Toplam session Temmuz'da {{b:{k(TOPLAM_S[202607])}}} ile MoM {{g:{pct(TOPLAM_S[202607], TOPLAM_S[202606])}}}, YoY {{r:{pct(TOPLAM_S[202607], TOPLAM_S[202507])}}} seviyesindedir; organik session {{b:{k(ORGANIK_S[202607])}}} ile YoY {{g:{pct(ORGANIK_S[202607], ORGANIK_S[202507])}}} artmıştır.",
        ]},
    ],
})

KANAL_AY = {}
for _ay in (202607, 202606, 202507):
    c = collections.Counter()
    for r in G:
        if ym(r) == _ay:
            c[r["kanal"]] += r["session"]
    KANAL_AY[_ay] = c
# Hacmi ihmal edilebilir kalan kanallar tablodan cikarilir; Toplam satiri
# GA4'te olculen tum kanallari kapsamaya devam eder.
KANAL_HARIC = {"Mobile Push Notifications", "Email", "Paid Other", "Organic Shopping"}
KANALLAR = sorted((set().union(*[set(c) for c in KANAL_AY.values()]) - KANAL_HARIC),
                  key=lambda kn: -KANAL_AY[202607][kn])
# Toplam satiri GA4'te olculen tum kanallarin toplamidir; AI Assistant satiri
# degistirilmeden once hesaplanir.
ktop = sum(KANAL_AY[202607].values())
ktop6 = sum(KANAL_AY[202606].values())
ktop5 = sum(KANAL_AY[202507].values())
# AI Assistant satiri, GA4'te tanimli yapay zeka kaynakli trafik segmentinden
# alinir; varsayilan kanal grubu etiketi daha dar bir kume olcmektedir.
for _ay in (202607, 202606, 202507):
    KANAL_AY[_ay]["AI Assistant"] = AI_S[_ay]


def _s(v):
    return n(v) if v else "-"


kanal_satir = [[kn, _s(KANAL_AY[202607][kn]), _s(KANAL_AY[202606][kn]), _s(KANAL_AY[202507][kn]),
                pct(KANAL_AY[202607][kn], KANAL_AY[202606][kn]),
                pct(KANAL_AY[202607][kn], KANAL_AY[202507][kn]),
                f"%{KANAL_AY[202607][kn]/ktop*100:.1f}"] for kn in KANALLAR]
kanal_satir.append(["Toplam", n(ktop), n(ktop6), n(ktop5),
                    pct(ktop, ktop6), pct(ktop, ktop5), "%100.0"])
KANAL_BAS = ["Kanal", "Tem'26", "Haz'26", "Tem'25", "MoM", "YoY", "Pay"]

S.append({
    "type": "content",
    "breadcrumb": ["GA4", "Kanal Dağılımı"],
    "title": "Kanal Bazında Session ve Dönem Karşılaştırması",
    "subtitle": "Temmuz 2026 | GA4 varsayılan kanal grubu | tüm oturumlar",
    "source": "GA4 - Cloud Gaming",
    "grid": [100],
    "footnotes": [
        "AI Assistant satırı yapay zeka kaynaklı trafik segmentinden alınmıştır. Toplam satırı GA4'te "
        "ölçülen tüm kanalları kapsar; hacmi 320 session'ın altında kalan dört kanal listelenmemiştir.",
    ],
    "blocks": [
        dict({"type": "table", "col": "full", "first_col_max": 0.26,
              "head": KANAL_BAS, "rows": kanal_satir, "bold_rows": [-1]},
             **{**T, "font_pt": 9, "row_h": 15, "head_h": 19}),
        {"type": "insights", "col": "full", "mt": 6, "font_pt": 9.5, "items": [
            f"Toplam session MoM {{g:{pct(ktop, ktop6)}}}, YoY {{r:{pct(ktop, ktop5)}}}; yıllık daralma "
            f"{{c:Display}} ve {{c:Paid Social}} kaynaklıdır. {{c:Organic Search}} yıllık "
            f"{{g:{pct(KANAL_AY[202607]['Organic Search'], KANAL_AY[202507]['Organic Search'])}}}, "
            f"{{c:AI Assistant}} aylık {{g:{pct(KANAL_AY[202607]['AI Assistant'], KANAL_AY[202606]['AI Assistant'])}}} büyümektedir.",
        ]},
    ],
})

# ================================================== 05 içerik performansı
S.append({"type": "separator", "no": "05", "title": "İçerik Performansı"})
S.append({
    "type": "content",
    "breadcrumb": ["İÇERİK", "Blog"],
    "title": "/blog Aylık Session Performansı",
    "subtitle": "Tem 2025 - Tem 2026 | GA4 | toplam ve organik",
    "source": "GA4 - Cloud Gaming · Landing page kırılımı",
    "grid": [100],
    "footnotes": [
        "Ayıklama: landing page listesindeki 803 satır ve 33.799 session, yol içinde tırnak, açılı parantez ve rastgele token taşıyan varyantlardan oluşmaktadır. Bunlar güvenlik taraması yapan araçların ürettiği isteklerdir; gerçek sayfa olmadıkları ve tek bir yazıyı onlarca satıra böldükleri için kapsam dışı bırakılmıştır.",
    ],
    "blocks": [
        {"type": "combo", "col": "full", "h": 186, "bar_w": 30, "cats": GA_ET, "series": [
            {"kind": "bar", "name": "/blog toplam", "data": [BLOG_S[y] for y in GA_AYLAR],
             "color": "gray_bar", "axis": "left"},
            {"kind": "line", "name": "/blog organik", "data": [BLOG_ORG[y] for y in GA_AYLAR],
             "color": "coral", "axis": "right"},
        ]},
        dict({"type": "table", "col": "full", "mt": 10, "first_col_max": 0.12, "heat": True,
              "head": ["Metrik"] + GA_ET,
              "rows": [["Toplam"] + [k(BLOG_S[y]) for y in GA_AYLAR],
                       ["Organik"] + [k(BLOG_ORG[y]) for y in GA_AYLAR]]}, **T),
        {"type": "insights", "col": "full", "mt": 10, "font_pt": 10.5, "items": [
            f"Blog Temmuz'da {{b:{k(BLOG_S[202607])}}} session almış, yıllık bazda {{g:{pct(BLOG_S[202607], BLOG_S[202507])}}} artmıştır. Organik pay {{b:%{BLOG_ORG[202607]/BLOG_S[202607]*100:.1f}}} seviyesindedir.",
        ]},
    ],
})

blog_lp = collections.defaultdict(collections.Counter)
for r in G:
    lp = r["lp"].split("?")[0].rstrip("/")
    if lp.startswith("/blog/"):
        blog_lp[lp][ym(r)] += r["session"]
yuks = sorted(((lp, s[202607], s[202606]) for lp, s in blog_lp.items() if s[202607] >= 300),
              key=lambda x: -(x[1] - x[2]))[:7]
S.append({
    "type": "content",
    "breadcrumb": ["İÇERİK", "Yükselen Yazılar"],
    "title": "Temmuz'da Yükselen Blog Yazıları",
    "subtitle": "Temmuz 2026 & Haziran 2026 | GA4 session | aylık artışa göre sıralı",
    "source": "GA4 - Cloud Gaming · Landing page kırılımı",
    "grid": [58, 42],
    "footnotes": [
        "Tabloya Temmuz'da en az 300 session alan yazılar dahil edilmiştir. GFN Thursday yazıları haftalık yayınlandığı için önceki ayda karşılığı bulunmaz.",
    ],
    "blocks": [
        dict({"type": "table", "col": "full", "first_col_max": 0.50,
              "head": ["Yazı", "Haz 26", "Tem 26", "Δ"],
              "rows": [[lp.replace("/blog/", "")[:50], n(h), n(t), f"+{n(t-h)}"]
                       for lp, t, h in yuks], "highlight_rows": [0]}, **T),
        {"type": "insights", "col": "full", "mt": 12, "font_pt": 10.5, "items": [
            "Temmuz'un en yüksek katkısı {c:GFN Thursday 23 Temmuz} yazısındandır ({b:14.4K} session); haftalık seri blog trafiğinin ana taşıyıcısıdır.",
            "Kalıcı içerikte {c:Call of Duty kronolojik sıralama} {b:5.2K} ve {c:2026 MMORPG} {b:2.5K} session ile artışını sürdürmüştür.",
        ]},
    ],
})

alt = collections.defaultdict(collections.Counter)
for r in G:
    lp = r["lp"].split("?")[0].rstrip("/")
    if lp.startswith("/gfn/oyunlar/"):
        alt[lp][ym(r)] += r["session"]
alt_s = sorted(alt.items(), key=lambda kv: -kv[1][202607])[:9]
S.append({
    "type": "content",
    "breadcrumb": ["İÇERİK", "Oyun Kategorileri"],
    "title": "/gfn/oyunlar Alt Kategorileri",
    "subtitle": "Temmuz 2026 | GA4 session ve GSC click | session'a göre sıralı",
    "source": "GA4 - Cloud Gaming & Google Search Console",
    "grid": [58, 42],
    "footnotes": [
        "Alt kategoriler bu dönemde açıldığı için önceki yıl karşılığı bulunmamaktadır. GA4 session tüm kanalları, GSC click yalnızca organik aramayı kapsar; iki sütun arasındaki fark diğer kanallardan gelen trafiği gösterir.",
    ],
    "blocks": [
        dict({"type": "table", "col": "full", "first_col_max": 0.32,
              "head": ["Kategori", "Tem 26 GA4 session", "MoM", "Tem 26 GSC click", "MoM"],
              "rows": [[lp.replace("/gfn/oyunlar/", ""), n(s[202607]), pct(s[202607], s[202606]),
                        n(OYUN_G[lp]["2026-07"][0]),
                        pct(OYUN_G[lp]["2026-07"][0], OYUN_G[lp]["2026-06"][0])]
                       for lp, s in alt_s]}, **T),
        {"type": "insights", "col": "full", "mt": 12, "font_pt": 10.5, "items": [
            "Alt kategoriler Temmuz'da GA4 tarafında {b:4.7K} session, GSC tarafında {b:2.3K} click almıştır. {c:Oynaması ücretsiz} her iki ölçüde de kategorinin ana taşıyıcısıdır.",
            "{c:Yarış} ve {c:MMO} kategorilerinde session artışı yüksek olsa da GSC click'i düşük kalmaktadır; bu başlıklara gelen trafiğin büyük bölümü organik aramadan gelmemektedir.",
        ]},
    ],
})

# ==================================================== 06 yapay zeka
S.append({"type": "separator", "no": "06", "title": "Yapay Zeka Görünürlüğü"})
S.append({
    "type": "content",
    "breadcrumb": ["YAPAY ZEKA", "Görünürlük Metrikleri"],
    "title": "Yapay Zeka Yanıtlarında Marka Görünürlüğü",
    "subtitle": "Temmuz 2026 | 72 prompt | ChatGPT, Gemini ve Google AI Overview",
    "source": "Inbound AI Görünürlük İzleme",
    "grid": [100],
    "footnotes": [
        "Brand Mention: markanın anıldığı yanıt sayısı, izlenen toplam yanıt içinde verilmiştir. "
        "Brand Position: markanın yanıt içinde kaçıncı sırada anıldığı; küçük değer daha öndedir. "
        "Source Visibility yanıt bazlı ölçülür: marka sitesinin kaynak gösterildiği yanıtların "
        "toplam yanıt içindeki payı. Alttaki tablodaki Pay kolonu ise citation bazlıdır; iki oran "
        "farklı paydaya sahiptir.",
    ],
    "blocks": [
        dict({"type": "table", "col": "full", "first_col_max": 0.22,
              "head": ["Sağlayıcı", "Brand Mention / Yanıt", "Mention oranı", "Brand Position",
                       "Citation alan yanıt / Yanıt", "Source Visibility"],
              "rows": [["Gemini", "436 / 591", "%73.8", "2.83", "465 / 591", "%78.7"],
                       ["Google AI Overview", "276 / 500", "%55.2", "1.83", "249 / 500", "%49.8"],
                       ["ChatGPT", "254 / 531", "%47.8", "2.47", "143 / 531", "%26.9"],
                       ["Toplam", "966 / 1.622", "%59.6", "2.45", "857 / 1.622", "%52.8"]],
              "bold_rows": [-1]}, **{**T, "row_h": 17, "head_h": 21}),
        dict({"type": "table", "col": "full", "mt": 6, "first_col_max": 0.30,
              "head": ["En çok Citation alan kaynak", "Citation / Toplam", "Pay", "Farklı prompt"],
              "rows": [["gameplus.com.tr", "1.492 / 9.621", "%15.5", "70"],
                       ["nvidia.com", "1.017 / 9.621", "%10.6", "58"],
                       ["youtube.com", "687 / 9.621", "%7.1", "69"],
                       ["reddit.com", "482 / 9.621", "%5.0", "58"]],
              "highlight_rows": [0]}, **{**T, "row_h": 17, "head_h": 21}),
        {"type": "insights", "col": "full", "mt": 6, "font_pt": 10, "items": [
            "Marka {b:1.622 yanıtın 966'sında} anılmaktadır; {c:Gemini} {g:%73.8} ile en yüksek, {c:ChatGPT} {r:%47.8} ile en düşük orandadır.",
            "{c:gameplus.com.tr} {b:1.492 citation} ile ilk sıradadır ve toplam citation'ın {b:%15.5}'ini almaktadır. "
            "Yanıt bazında bakıldığında marka sitesi yanıtların {b:%52.8}'inde kaynak gösterilmektedir.",
        ]},
    ],
})

ORNEK_DIPNOT = ("İzlenen 72 prompt'un 53'ü marka adı geçmeyen kategori sorusudur; bu bölümdeki örnekler "
                "o kümeden seçilmiştir. Yanıt metinleri birebir alınmış, uzunluk nedeniyle markanın geçtiği "
                "bölüm kısaltılarak verilmiştir.")


def ornek_slayt(alt, ornekler, yorum, dipnot_ek=None):
    """İki prompt ve yanıt örneğini yan yana veren slayt."""
    return {
        "type": "content",
        "breadcrumb": ["YAPAY ZEKA", "Örnek Promptlar"],
        "title": "Marka Adı Geçmeyen Promptlarda Yanıt Örnekleri",
        "subtitle": alt,
        "source": "Inbound AI Görünürlük İzleme",
        "grid": [100],
        "footnotes": [ORNEK_DIPNOT] + ([dipnot_ek] if dipnot_ek else []),
        "blocks": [
            {"type": "panels", "col": "full", "cols": 2, "font_pt": 10, "items": [
                {"title": f"Prompt: \"{o['prompt']}\"", "sub": o["sub"],
                 "lines": [o["yanit"], f"Citation: {o['citation']}"]} for o in ornekler
            ]},
            {"type": "insights", "col": "full", "mt": 12, "font_pt": 10.5, "items": [yorum]},
        ],
    }


S.append(ornek_slayt(
    "Temmuz 2026 | Gemini ve ChatGPT | markanın ilk sıralarda anıldığı yanıtlar",
    [
        {"prompt": "oyunlar indirmeden nasıl açılır", "sub": "Gemini · Sıra #1 · olumlu",
         "yanit": "\"1. NVIDIA GeForce NOW (Türkiye'de Game+) - Bu bulut oyun platformu, güçlü bir oyun "
                  "bilgisayarına sahip olmadan yüksek grafikli oyunları oynamanıza olanak tanır. Oyunlar NVIDIA "
                  "sunucularında çalıştırılır ve görüntü cihazınıza aktarılır. Türkiye'de Game+ adıyla hizmet "
                  "vermektedir. Kullanıcılar kendi Steam, Epic Games gibi platformlardaki oyun kütüphanelerini "
                  "bu servis üzerinden oynayabilirler.\"",
         "citation": "poki.com · webtekno.com · gameplus.com.tr · crazygames.com"},
        {"prompt": "geforce now nasıl çalışıyo", "sub": "ChatGPT · yanıt gövdesinde · olumlu",
         "yanit": "\"GeForce NOW, NVIDIA tarafından sunulan bulut tabanlı bir oyun hizmetidir. Bu hizmet "
                  "sayesinde, güçlü bir oyun bilgisayarına sahip olmasanız bile yüksek kaliteli oyunları "
                  "oynayabilirsiniz. (...) Türkiye'de GeForce NOW hizmeti, GAME+ tarafından sunulmaktadır. "
                  "Bu sayede Türk oyuncular da yüksek kaliteli oyun deneyiminden faydalanabilirler.\"",
         "citation": "corsair.com · en.wikipedia.org · gameplus.com.tr · nvidia.com"},
    ],
    "İki yanıtta da marka, bulut oyun kategorisinin ilk seçeneği olarak aktarılmakta ve gameplus.com.tr "
    "kaynak gösterilmektedir. Kategori sorularının marka görünürlüğünü taşıdığı görülmektedir."))

S.append(ornek_slayt(
    "Temmuz 2026 | Gemini ve Google AI Overview | cihaz ve oyun listesi soruları",
    [
        {"prompt": "tabletten bulut oyun oynanır mı", "sub": "Gemini · Sıra #1",
         "yanit": "\"Türkiye'de veya Türkiye'den erişilebilen popüler bulut oyun servisleri şunlardır: "
                  "1. NVIDIA GeForce Now (GAME+) - Türkiye sunucuları üzerinden hizmet veren bu platform, "
                  "güçlü bir internet bağlantısıyla herhangi bir cihazdan yüksek performanslı PC oyunlarını "
                  "oynamanıza olanak tanır. Windows, macOS, iOS, Android ve Nvidia Shield cihazlarını "
                  "destekler.\"",
         "citation": "bluestacks.com · etail.com.tr · gameplus.com.tr · adil.net.tr"},
        {"prompt": "geforce now oyunları neler", "sub": "Google AI Overview · kaynak panelinde",
         "yanit": "\"Nasıl Kontrol Edilir? Tüm güncel ve tam listeyi görmek için resmi GeForce NOW Oyunları "
                  "sayfasını aratabilirsiniz. Türkiye'deki servis detayları için GAME+ GeForce NOW Oyunlar "
                  "kütüphanesine göz atabilirsiniz.\"",
         "citation": "gameplus.com.tr · reddit.com · nvidia.com · technopat.net"},
    ],
    "AI Overview yanıtı, oyun listesi sorusunu doğrudan {b:gameplus.com.tr/gfn/oyunlar} sayfasına "
    "bağlamaktadır; oyun alt kategorilerinin yayına alınmasının karşılığı bu yanıtta görülmektedir."))

S.append(ornek_slayt(
    "Temmuz 2026 | ChatGPT ve Gemini | olumlu ve olumsuz çerçeve örneği",
    [
        {"prompt": "ubisoft+ ta hangi oyunlar var", "sub": "ChatGPT · Sıra #1 · olumlu",
         "yanit": "\"1. Ubisoft+ Classics: PC platformunda mevcut olan bu paket, 30-40 oyun içerir ve standart "
                  "sürümleriyle sunulur. 2. Ubisoft+ Premium: PC ve Xbox platformlarında erişilebilen bu paket, "
                  "120'den fazla oyunu kapsar. (...) Türkiye'de Ubisoft+ Premium aboneliği aylık 399 TL, "
                  "Ubisoft+ Classics ise aylık 199 TL olarak sunulmaktadır.\"",
         "citation": "en.wikipedia.org · gameplus.com.tr"},
        {"prompt": "geforce now mı xbox cloud mu daha iyi", "sub": "Gemini · karşılaştırma yanıtı · olumsuz",
         "yanit": "\"Türkiye Deneyimi: Türkiye'deki Game+ (yerel dağıtıcı) ile ilgili bazı kullanıcı "
                  "şikayetleri bulunmaktadır. Reklamı yapılan 'RTX On' üyeliklerinde bile sıklıkla GTX 1060 "
                  "gibi daha eski ekran kartlarına düşülebildiği belirtilmektedir.\"",
         "citation": "reddit.com · youtube.com · en.wikipedia.org · gameseal.com"},
    ],
    "Ubisoft+ yanıtında paket ve fiyat bilgisi doğrudan marka sayfasından alınmaktadır. Karşılaştırma "
    "sorusunda ise anlatım kullanıcı içeriği kaynaklarına dayanmakta ve donanım beklentisi üzerinden "
    "olumsuz bir çerçeve kurulmaktadır; bu başlıkta marka sayfalarında açıklayıcı içerik değerlendirilebilir.",
    "Olumsuz çerçeveli yanıt, Temmuz'da olumsuz etiketlenen 3 yanıttan biridir."))

S.append({
    "type": "content",
    "breadcrumb": ["YAPAY ZEKA", "Marka Anlatımı"],
    "title": "Yapay Zeka Yanıtlarında Markadan Nasıl Bahsediliyor",
    "subtitle": "Son koşu | markanın anıldığı yanıtlardaki bağlam",
    "source": "Inbound AI Görünürlük İzleme",
    "grid": [100],
    "footnotes": [
        "Alıntılar yanıt metinlerinden birebir alınmıştır.",
        "Tepki tonu etiketi yanıtların %20.5'inde üretilmiştir. Ölçüm Temmuz 2026 başında başladığı için önceki dönemle karşılaştırma yapılmamıştır.",
    ],
    "blocks": [
        {"type": "panels", "col": "full", "cols": 3, "font_pt": 10, "items": [
            {"title": "Konumlandırma", "sub": "en sık kurulan cümle",
             "lines": ["\"Türkiye'de Turkcell'in GAME+ servisi aracılığıyla hizmet vermektedir.\"",
                       "Marka, NVIDIA ile birlikte anılıyor."]},
            {"title": "Öne çıkan özellikler", "sub": "yanıtlarda vurgulananlar",
             "lines": ["Ücretsiz paket ve 1 saatlik oturum",
                       "Android telefon ve tablet uyumluluğu · İstanbul sunucusu"]},
            {"title": "Tepki tonu", "sub": "332 etiketli yanıt",
             "lines": ["263 nötr · 66 olumlu · 3 olumsuz"]},
        ]},
        {"type": "panels", "col": "full", "cols": 2, "mt": 8, "font_pt": 10, "items": [
            {"title": "Olumlu örnek", "sub": "Gemini · \"oyunlar indirmeden nasıl açılır\"",
             "lines": ["\"NVIDIA GeForce NOW (Türkiye'de Game+) - Bu bulut oyun platformu, güçlü bir oyun "
                       "bilgisayarına sahip olmadan yüksek grafikli oyunları oynamanıza olanak tanır.\""]},
            {"title": "Olumsuz örnek", "sub": "Gemini · \"geforce now mı xbox cloud mu daha iyi\"",
             "lines": ["\"Türkiye'deki Game+ (yerel dağıtıcı) ile ilgili bazı kullanıcı şikayetleri "
                       "bulunmaktadır. Reklamı yapılan 'RTX On' üyeliklerinde bile sıklıkla daha eski "
                       "ekran kartlarına düşülebildiği belirtilmektedir.\""]},
        ]},
        {"type": "insights", "col": "full", "mt": 10, "font_pt": 10.5, "items": [
            "Yanıtlar markayı {b:GeForce NOW'ın Türkiye sağlayıcısı} olarak konumlandırmaktadır."
        ]},
    ],
})

AI_AYLAR = sorted(AI_S)
S.append({
    "type": "content",
    "breadcrumb": ["YAPAY ZEKA", "Yapay Zeka Kaynaklı Trafik"],
    "title": "Yapay Zeka Kaynaklı Trafiğin Aylık Seyri",
    "subtitle": "Tem 2025 - Tem 2026 | GA4 segment | session",
    "source": "GA4 - Cloud Gaming",
    "grid": [100],
    "footnotes": [
        "Seri, GA4'te tanımlı yapay zeka kaynaklı trafik segmentinden alınmıştır. Varsayılan kanal grubundaki \"AI Assistant\" etiketi yalnızca Haziran 2026'dan itibaren kayıt taşıdığı için aylık seride bu segment kullanılmıştır.",
    ],
    "blocks": [
        {"type": "combo", "col": "full", "h": 172, "bar_w": 30,
         "cats": [ek_etiket(y) for y in AI_AYLAR], "series": [
            {"kind": "bar", "name": "AI kaynaklı session", "data": [AI_S[y] for y in AI_AYLAR],
             "color": "gray_bar", "axis": "left", "labels": "above",
             "labels_text": [n(AI_S[y]) for y in AI_AYLAR]},
        ]},
        dict({"type": "table", "col": "full", "mt": 10, "first_col_max": 0.12, "heat": True,
              "head": ["Metrik"] + [ek_etiket(y) for y in AI_AYLAR],
              "rows": [["Session"] + [n(AI_S[y]) for y in AI_AYLAR]]}, **T),
        {"type": "insights", "col": "full", "mt": 10, "font_pt": 10.5, "items": [
            f"Yapay zeka kaynaklı trafik Tem 2025'te {{b:{AI_S[202507]}}} session iken Tem 2026'da {{g:{AI_S[202607]}}} session'a ulaşmıştır; yıllık artış {{g:{pct(AI_S[202607], AI_S[202507])}}} seviyesindedir.",
            "Serinin zirvesi Mayıs 2026'da {b:852} session olarak ölçülmüştür. Hacim toplam trafiğin yanında küçük kalmakla birlikte istikrarlı yükseliş göstermekte ve yeni bir giriş kaynağı olarak izlenmeye değer görünmektedir.",
        ]},
    ],
})

# =========================================== 07 yapılan ve planlanan
S.append({"type": "separator", "no": "07", "title": "Yapılan ve Planlanan İşler"})
S.append({
    "type": "content",
    "breadcrumb": ["SÜREÇ", "Tamamlanan"],
    "title": "Tamamlanan İşler",
    "subtitle": "Dönem içinde tamamlanan çalışmalar",
    "source": "Inbound",
    "grid": [100],
    "blocks": [
        {"type": "panels", "col": "full", "cols": 3, "items": [
            {"title": "Ubisoft+ içerikleri", "sub": "tamamlandı",
             "lines": ["Ubisoft+ Temmuz ve Ağustos yazıları tamamlandı.",
                       "/ubisoft sayfası Temmuz'da +275 click ile en yüksek oransal artışı gösterdi (+%283.5).",
                       "AI Overview yanıtlarında ubisoft/oyunlar sayfası kaynak gösterilmeye başlandı."]},
            {"title": "Blog detay tasarımı", "sub": "onaylandı",
             "lines": ["Blog detay tasarımı son haline getirildi.",
                       "Tasarım ekibinden onay alındı.",
                       "Eski yazıların bu tasarıma taşınması Ağustos planındadır."]},
            {"title": "Oyun alt kategorileri", "sub": "içerikler yayında",
             "lines": ["Oyunlar kategorisi altındaki alt kategori içerikleri yayına alındı.",
                       "Temmuz, kategorilerin ilk tam ayı oldu: 4.7K GA4 session, 2.3K GSC click."]},
        ]},
        {"type": "panels", "col": "full", "cols": 1, "mt": 14, "font_pt": 10.5, "items": [
            {"title": "Game+ Ekibinde Bekleyen Maddeler", "sub": "ilerlemek için gereken girdiler",
             "lines": [
                 "Mixpanel ve Microsoft Clarity yetki tanımlamaları · Clarity tarafında AI insight raporlarına da erişilebilmektedir, bu raporlar GEO çalışmaları için kullanılabilir.",
                 "Bloglara eklenen UTM'lerin takip edilip edilmediğinin netleştirilmesi; ilgili bir rapor bulunuyorsa paylaşılması.",
                 "Oyun detay sayfaları için içerik teklifi hazırlanabilmesi adına güncel oyun listesinin (en çok oynanan oyunlar) iletilmesi.",
             ]},
        ]},
    ],
})

S.append({
    "type": "content",
    "breadcrumb": ["SÜREÇ", "Ağustos"],
    "title": "Planlanan İşler",
    "subtitle": "Önümüzdeki dönemde ele alınacak çalışmalar",
    "source": "Inbound",
    "grid": [100],
    "blocks": [
        {"type": "panels", "col": "full", "cols": 4, "items": [
            {"title": "İçerik güncelleme", "sub": "haftalık takvim",
             "lines": ["Eski blog yazılarının yeni blog detay tasarımına göre haftalık takvimle güncellenmesi.",
                       "Oyunlar alt kategori içeriklerinin yeni formata göre güncellenmesi."]},
            {"title": "Oyun detay sayfaları", "sub": "içerik teklifi",
             "lines": ["Test sitesindeki örnek sayfada içerik alanları incelendi.",
                       "Oyun detaya özgü bir içerik teklifi alınacak.",
                       "Arama hacmi en yüksek oyunlar ile en çok oynanan oyunlar kesiştirilerek öncelik listesi belirlenecek."]},
            {"title": "Oyun detay yayın öncesi ruleset", "sub": "teknik hazırlık",
             "lines": ["Yeni oyun detay sayfaları yayına çıkmadan önce meta title, meta description, URL yapısı ve schema alanları için ruleset tanımlanması gerekiyor.",
                       "Ruleset, sayfa sayısı arttıkça tekil düzenleme ihtiyacını ortadan kaldırır."]},
            {"title": "Ölçümleme", "sub": "takip",
             "lines": ["Bloglardaki UTM takibinin durumu netleştirilecek.",
                       "GA4 landing page listesindeki tarama aracı kaynaklı kayıtlar için filtre tanımlanması değerlendirilebilir."]},
        ]},
    ],
})

S.append({
    "type": "content",
    "breadcrumb": ["DEĞERLENDİRME", "Öne Çıkan Başlıklar"],
    "title": "Önümüzdeki Dönemde Öne Çıkan Üç Başlık",
    "subtitle": "Bu dönemin bulgularından türetilen çalışma alanları",
    "source": "Google Search Console, GA4 ve Inbound AI Görünürlük İzleme",
    "grid": [100],
    "footnotes": [
        "Başlıkların önceliklendirilmesi Game+ ekibinin stratejik tercihleri ve öncelikleriyle güncellenebilir.",
    ],
    "blocks": [
        {"type": "panels", "col": "full", "cols": 3, "items": [
            {"title": "GFN ve brand talebindeki daralma", "sub": "izleme başlığı",
             "lines": ["GFN tarafında click yıllık bazda %64.1, brand tarafında %30.6 geriledi.",
                       "Brand ortalama pozisyonu da gerilemiş durumda.",
                       "Marka ve GFN sorgularında sıralama ve içerik durumunun ayrı bir başlıkta ele alınması değerlendirilebilir."]},
            {"title": "Blog trafiğinin haftalık seriye bağlılığı", "sub": "içerik dengesi",
             "lines": ["Temmuz blog trafiğinin belirgin bölümü tek bir GFN Thursday yazısından geliyor (14.4K session).",
                       "Sıralaması gerileyen kalıcı yazılar var: resident evil ve call of duty black ops başlıkları.",
                       "Kalıcı içeriğin güncellenmesi öncelikli tutulabilir."]},
            {"title": "Yapay zeka yanıtlarındaki konum", "sub": "fırsat alanı",
             "lines": ["gameplus.com.tr, yanıtlarda en çok Citation alan kaynak (1.490 citation).",
                       "ChatGPT tarafında anılma oranı %47.7 ile en düşük seviyede.",
                       "Ücretsiz paket, cihaz uyumluluğu ve yerel sunucu başlıklarının içerikte güçlendirilmesi değerlendirilebilir."]},
        ]},
        {"type": "insights", "col": "full", "mt": 14, "font_pt": 11, "items": [
            "Dönemin genel tablosu, SSR geçişi ve içerik çalışmasının non-brand tarafında belirgin bir kazanım ürettiğini; marka ve GFN sorgularındaki daralmanın ise talebe bağlı olabileceğini göstermektedir.",
        ]},
    ],
})

S.append({"type": "closing", "title": "Teşekkürler"})

seps = [s for s in S if s.get("type") == "separator"]
next(s for s in S if s["type"] == "agenda")["items"] = [
    {"no": s["no"], "label": s["title"]} for s in seps]

out = BASE / "deck.json"
out.write_text(json.dumps({"meta": {"brand": "Game+", "period": "Temmuz 2026"},
                           "slides": S}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(S)} slayt -> {out}")
