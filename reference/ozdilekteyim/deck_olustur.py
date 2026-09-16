# -*- coding: utf-8 -*-
"""Özdilekteyim Ağustos 2026 aylık SEO değerlendirme destesi (M1).

GA4 bölümü GA4_HAZIR bayrağının arkasındadır. Export'lar gelene kadar bölüm
destede yer almaz; ajanda ve bölüm numaraları ayraçlardan otomatik türetildiği
için bayrak açıldığında numaralandırma kendiliğinden kayar.

GA4 export'ları (web-only, Organic Search + tüm kanallar) geldiğinde:
  veri/ham/ga4_kanal_2026-08.csv, ga4_kanal_2026-07.csv, ga4_kanal_2025-08.csv
  veri/ham/ga4_aylik_13ay.csv       (Year + Month, toplam ve organik session)
  veri/ham/ga4_lp_organik_2026-08.csv, ga4_lp_organik_2026-07.csv
  veri/ham/ga4_ai_referral_13ay.csv
okunacak ve ga4_bolumu() doldurulacak.
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE / "veri"))
from gsc import etiket, seriler  # noqa: E402
from hacim import AYLAR as H_AYLAR, TERIM, hacim  # noqa: E402
from kirilim import BRAND, P, Q, hareketler, yol  # noqa: E402

GA4_HAZIR = False

AYLAR, SEG, _SON = seriler()
assert AYLAR == H_AYLAR, "GSC ve hacim ay dizileri eşleşmiyor"
ET = [etiket(y) for y in AYLAR]
ET_KISA = [e[:3] for e in ET]
SIMDI, ONCEKI, GECEN_YIL = 202608, 202607, 202508
KAYNAK_GSC = "Google Search Console - ozdilekteyim.com"
KAYNAK_HACIM = "Google Ads arama hacmi (Ağu 2026)"


def k(v):
    if v is None:
        return "-"
    if v < 1000:
        return n(v)
    return f"{v/1_000_000:.2f}M" if v >= 1_000_000 else f"{v/1000:.1f}K"


def n(v):
    return "-" if v is None else f"{v:,}".replace(",", ".")


def pct(a, b, kucuk_taban=10):
    if not b:
        return "yeni" if a else "-"
    if b < kucuk_taban:
        return f"{a - b:+d}"
    v = (a / b - 1) * 100
    return f"{'+' if v >= 0 else '-'}%{abs(v):.1f}"


def sifirla(s):
    """'-0.0' / '+0.00' gibi yuvarlama artıklarını işaretsiz sıfıra çevirir."""
    return s.lstrip("+-") if float(s.rstrip("p")) == 0 else s


def renk(s, ters=False):
    """Yüzde/delta metnini işaretine göre yeşil/kırmızı işaretler."""
    neg = s.startswith("-")
    if ters:
        neg = not neg
    return f"{{{'r' if neg else 'g'}:{s}}}"


def d(seg, metrik, a=SIMDI, b=ONCEKI):
    return pct(SEG[seg][a][metrik], SEG[seg][b][metrik])


ET_SIMDI, ET_ONCEKI, ET_GECEN = etiket(SIMDI), etiket(ONCEKI), etiket(GECEN_YIL)


def degisim_notu(kalemler, metrik="click", puan=False):
    """Tablo altına MoM ve YoY için ayrı birer ok üretir.

    kalemler: (etiket, seri) çiftleri. `puan=True` ise fark puan olarak yazılır
    (ortalama pozisyon gibi toplanamayan metrikler).
    """
    out = []
    for ad, a, b in (("MoM", ONCEKI, SIMDI), ("YoY", GECEN_YIL, SIMDI)):
        parca = []
        for et, seri in kalemler:
            if puan:
                fark = seri[a][metrik] - seri[b][metrik]
                parca.append(f"{et} {renk(sifirla(f'{fark:+.1f}'), ters=True)}")
            else:
                parca.append(f"{et} {renk(pct(seri[b][metrik], seri[a][metrik]))}")
        don = f"{etiket(a)} → {etiket(b)}"
        out.append(f"{ad} ({don}): " + " · ".join(parca))
    return out


T = dict(font_pt=10.5, row_h=20, head_h=24)
S = []
S.append({"type": "cover", "title": "Özdilekteyim SEO Değerlendirme", "subtitle": "Ağustos 2026"})
S.append({"type": "agenda", "kicker": "Ağustos 2026", "title_lines": ["SUNUM", "AKIŞI"], "items": []})

TOP, BR, NB = SEG["toplam"], SEG["brand"], SEG["nonbrand"]
HZ = {t: dict(zip(H_AYLAR, TERIM[t])) for t in ("özdilek", "özdilekteyim")}
HB = "Hacim (Ağu 2026)"

# ============================================================ genel görünüm
S.append({"type": "separator", "no": "", "title": "Genel Görünüm"})
S.append({
    "type": "content",
    "breadcrumb": ["GENEL GÖRÜNÜM", "Yönetici Özeti"],
    "title": "Aylık Toparlanma, Yıllık Bazda Marka Sorgularında Daralma",
    "subtitle": "Ağustos 2026 & Temmuz 2026 (MoM) & Ağustos 2025 (YoY) | Search Console tüm cihazlar",
    "source": KAYNAK_GSC,
    "grid": [100],
    "blocks": [
        {"type": "kpi", "col": "full", "cols": 4, "h": 112, "cards": [
            {"value": k(TOP[SIMDI]["click"]), "label": "Organik click",
             "deltas": [{"label": "MoM", "value": d("toplam", "click")},
                        {"label": "YoY", "value": d("toplam", "click", b=GECEN_YIL)}]},
            {"value": k(TOP[SIMDI]["impr"]), "label": "Impression",
             "deltas": [{"label": "MoM", "value": d("toplam", "impr")},
                        {"label": "YoY", "value": d("toplam", "impr", b=GECEN_YIL)}]},
            {"value": k(BR[SIMDI]["click"]), "label": "Brand click",
             "deltas": [{"label": "MoM", "value": d("brand", "click")},
                        {"label": "YoY", "value": d("brand", "click", b=GECEN_YIL)}],
             "accent": "coral"},
            {"value": k(NB[SIMDI]["click"]), "label": "Non-Brand click",
             "deltas": [{"label": "MoM", "value": d("nonbrand", "click")},
                        {"label": "YoY", "value": d("nonbrand", "click", b=GECEN_YIL)}],
             "accent": "coral"},
        ]},
        {"type": "insights", "col": "full", "mt": 14, "font_pt": 10.5, "items": [
            f"Organik click Ağustos'ta {{b:{k(TOP[SIMDI]['click'])}}} ile aylık bazda {renk(d('toplam', 'click'))} artmıştır; "
            f"artışın kaynağı {{c:brand}} sorgularıdır ({renk(d('brand', 'click'))}), non-brand click yatay seyretmiştir.",
            f"Yıllık bazda toplam click {renk(d('toplam', 'click', b=GECEN_YIL))} geridedir. Kaybın "
            f"{{b:%{(BR[GECEN_YIL]['click'] - BR[SIMDI]['click']) / (TOP[GECEN_YIL]['click'] - TOP[SIMDI]['click']) * 100:.0f}}}'i "
            f"brand sorgularından gelmektedir: brand click {renk(d('brand', 'click', b=GECEN_YIL))}, non-brand click "
            f"{renk(d('nonbrand', 'click', b=GECEN_YIL))}.",
            f"Aynı dönemde \"özdilek\" arama hacmi {{b:{k(HZ['özdilek'][GECEN_YIL])} → {k(HZ['özdilek'][SIMDI])}}} ile yatay kalmış, "
            f"\"özdilekteyim\" {{g:{k(HZ['özdilekteyim'][GECEN_YIL])} → {k(HZ['özdilekteyim'][SIMDI])}}} artmıştır; brand sorgularında "
            f"ortalama pozisyon {{b:{BR[GECEN_YIL]['poz']:.1f} → {BR[SIMDI]['poz']:.1f}}} ile korunmuştur.",
        ]},
        {"type": "note", "col": "full", "mt": 14, "label": "KRİTİK TESPİT",
         "text": f"Brand sorgularında talep ve sıralama korunurken CTR %{BR[GECEN_YIL]['ctr']:.1f} seviyesinden "
                 f"%{BR[SIMDI]['ctr']:.1f} seviyesine gerilemiştir. Yıllık click kaybı sıralamadan değil, marka "
                 f"aramalarında organik sonuca düşen tıklama payından kaynaklanmaktadır; ücretli arama ve sonuç "
                 f"sayfası yerleşimiyle birlikte değerlendirilmesi önerilir."},
    ],
})

S.append({
    "type": "content",
    "breadcrumb": ["GENEL GÖRÜNÜM", "Yöntem"],
    "title": "Segment ve Sayfa Grubu Tanımları",
    "subtitle": "Sorgu segmentleri ve sayfa grupları tüm destede aynı tanımla kullanılmaktadır",
    "source": KAYNAK_GSC,
    "grid": [100],
    "blocks": [
        {"type": "panels", "col": "full", "cols": 3, "items": [
            {"title": "Brand", "sub": "doğrudan ölçülür",
             "lines": ["Query içinde şu ifadeler geçen sorgular:",
                       "\"özdilek\" · \"ozdilek\"",
                       "\"özdilekteyim\" ve marka + ürün sorguları bu kümeye dahildir."]},
            {"title": "Non-Brand", "sub": "toplamdan çıkarılır",
             "lines": ["Toplam eksi brand olarak hesaplanır.",
                       "Query filtresi uygulandığında anonim sorgular sonuç kümesinden düştüğü için bu hacim non-brand satırında yer alır.",
                       "Pozisyon değeri marka ifadeleri dışlanarak ayrıca ölçülür."]},
            {"title": "Sayfa grupları", "sub": "URL yapısına göre",
             "lines": ["Mağaza: /magaza/ altındaki kategori ve ürün sayfaları.",
                       "Market: /market altındaki sayfalar.",
                       "Marka + Kategori: -cp2 ile biten, marka ve kategoriyi birlikte hedefleyen sayfalar."]},
        ]},
        {"type": "insights", "col": "full", "mt": 16, "font_pt": 11, "items": [
            "Brand ve Non-Brand birbirini tamamlar, toplamları toplam click'i verir. Sayfa grupları sorgu segmentlerinden bağımsızdır; bir sayfa grubu hem brand hem non-brand trafik alabilir.",
            "Marka + Kategori sayfaları Eylül 2025'ten itibaren yayına alındığı için bu grupta yıllık karşılaştırma yapılmamaktadır.",
        ]},
    ],
})

# ================================================ Google Search Console
S.append({"type": "separator", "no": "", "title": "Google Search Console Metrikleri"})

DIPNOT_NUM = ("Eylül 2025'te Google sonuç sayfası sorgularında yapılan değişiklikten sonra ilk 20 sıranın "
              "dışındaki sonuçların impression'ları Search Console raporlarına daha sınırlı yansımaktadır; "
              "bu nedenle yıllık impression ve ortalama pozisyon karşılaştırması bu değişiklikle birlikte "
              "okunmalıdır.")


def seg_seri(metrik, baslik, yorum, dipnot):
    return {
        "type": "content",
        "breadcrumb": ["SEARCH CONSOLE", "Aylık Seri"],
        "title": baslik,
        "subtitle": "Ağu 2025 - Ağu 2026 | 13 aylık seri | Search Console",
        "source": KAYNAK_GSC,
        "grid": [100],
        "footnotes": [dipnot, "Isı haritasında satırın en yüksek ayı yeşil, en düşük ayı kırmızı gösterilmektedir."],
        "blocks": [
            {"type": "combo", "col": "full", "h": 196, "bar_w": 44, "cats": ET, "series": [
                {"kind": "bar", "name": "Toplam", "data": [TOP[y][metrik] for y in AYLAR],
                 "color": "gray_bar", "axis": "left", "labels": "inside",
                 "labels_text": [k(TOP[y][metrik]) for y in AYLAR]},
                {"kind": "line", "name": "Non-Brand", "data": [NB[y][metrik] for y in AYLAR],
                 "color": "teal", "axis": "left"},
                {"kind": "line", "name": "Brand", "data": [BR[y][metrik] for y in AYLAR],
                 "color": "coral", "axis": "left" if metrik == "click" else "right"},
            ]},
            dict({"type": "table", "col": "full", "mt": 10, "first_col_max": 0.10, "heat": True,
                  "head": ["Segment"] + ET,
                  "rows": [["Brand"] + [k(BR[y][metrik]) for y in AYLAR],
                           ["Non-Brand"] + [k(NB[y][metrik]) for y in AYLAR],
                           ["Toplam"] + [k(TOP[y][metrik]) for y in AYLAR]],
                  "bold_rows": [-1]}, **{**T, "font_pt": 9.5}),
            {"type": "insights", "col": "full", "mt": 8, "font_pt": 10,
             "items": degisim_notu([("Toplam", TOP), ("Brand", BR), ("Non-Brand", NB)],
                                   metrik) + [yorum]},
        ],
    }


tepe = max(AYLAR, key=lambda y: TOP[y]["click"])
S.append(seg_seri(
    "click", "Brand ve Non-Brand Aylık Click",
    f"Toplam click {{b:{etiket(tepe)}}} döneminde {{b:{k(TOP[tepe]['click'])}}} ile serinin en yüksek seviyesine ulaşmış, "
    f"Şubat 2026'dan itibaren {{b:163-212K}} bandında seyretmiştir. Ağustos'ta {{b:{k(TOP[SIMDI]['click'])}}} ile "
    f"Temmuz'a göre {renk(d('toplam', 'click'))} toparlanmıştır; Nisan'daki brand artışı dışında iki segment benzer eğilim göstermektedir.",
    "Toplam satırı Brand ile Non-Brand'in toplamıdır."))
S.append(seg_seri(
    "impr", "Brand ve Non-Brand Aylık Impression",
    f"Yıllık impression kaybının tamamına yakını non-brand tarafındadır; brand impression "
    f"{{b:{k(BR[GECEN_YIL]['impr'])} → {k(BR[SIMDI]['impr'])}}} ile dar bir aralıkta kalmıştır.",
    "Brand ölçeği grafikte sağ eksendedir. " + DIPNOT_NUM))

# --- siralama ve CTR serisi: pozisyon toplam, CTR segment bazinda (click / impression)
S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Aylık Seri"],
    "title": "Ortalama Sıralama ve CTR",
    "subtitle": "Ağu 2025 - Ağu 2026 | 13 aylık seri | Search Console",
    "source": KAYNAK_GSC,
    "grid": [100],
    "footnotes": [
        "Segment CTR değerleri her segmentin kendi click / impression oranıdır; toplam CTR'dan çıkarılarak bulunmaz. "
        "Pozisyon çizgisi ters eksenlidir (yükselen çizgi iyileşme), ısı haritasında pozisyon satırı ters okunur. "
        "Yıllık pozisyon karşılaştırması Eylül 2025 değişikliğiyle birlikte okunmalıdır.",
    ],
    "blocks": [
        {"type": "combo", "col": "full", "h": 164, "bar_w": 44, "cats": ET, "series": [
            {"kind": "bar", "name": "CTR (Toplam)", "data": [round(TOP[y]["ctr"], 2) for y in AYLAR],
             "color": "gray_bar", "axis": "left", "fmt": "pct", "labels": "inside",
             "labels_text": [f"%{TOP[y]['ctr']:.1f}" for y in AYLAR]},
            {"kind": "line", "name": "Ort. pozisyon (Toplam)", "data": [round(TOP[y]["poz"], 1) for y in AYLAR],
             "color": "coral", "axis": "right", "invert": True, "fmt": "pos", "labels": "above",
             "labels_text": [f"{TOP[y]['poz']:.1f}" for y in AYLAR]},
        ]},
        dict({"type": "table", "col": "full", "mt": 10, "first_col_max": 0.13, "heat": True,
              "heat_invert_rows": [0],
              "head": ["Metrik"] + ET,
              "rows": [["Ort. pozisyon"] + [f"{TOP[y]['poz']:.1f}" for y in AYLAR],
                       ["CTR Brand"] + [f"%{BR[y]['ctr']:.1f}" for y in AYLAR],
                       ["CTR Non-Brand"] + [f"%{NB[y]['ctr']:.1f}" for y in AYLAR],
                       ["CTR Toplam"] + [f"%{TOP[y]['ctr']:.1f}" for y in AYLAR]],
              "bold_rows": [-1]}, **{**T, "font_pt": 9.5}),
        {"type": "insights", "col": "full", "mt": 8, "font_pt": 10, "items": [
            f"MoM ({ET_ONCEKI} → {ET_SIMDI}): Ort. pozisyon "
            f"{renk(sifirla(f'{TOP[ONCEKI]['poz'] - TOP[SIMDI]['poz']:+.1f}'), ters=True)} · CTR Toplam "
            f"{renk(sifirla(f'{TOP[SIMDI]['ctr'] - TOP[ONCEKI]['ctr']:+.1f}') + 'p')} · Brand "
            f"{renk(sifirla(f'{BR[SIMDI]['ctr'] - BR[ONCEKI]['ctr']:+.1f}') + 'p')} · Non-Brand "
            f"{renk(sifirla(f'{NB[SIMDI]['ctr'] - NB[ONCEKI]['ctr']:+.1f}') + 'p')}",
            f"YoY ({ET_GECEN} → {ET_SIMDI}): Ort. pozisyon "
            f"{renk(sifirla(f'{TOP[GECEN_YIL]['poz'] - TOP[SIMDI]['poz']:+.1f}'), ters=True)} · CTR Toplam "
            f"{renk(sifirla(f'{TOP[SIMDI]['ctr'] - TOP[GECEN_YIL]['ctr']:+.1f}') + 'p')} · Brand "
            f"{renk(sifirla(f'{BR[SIMDI]['ctr'] - BR[GECEN_YIL]['ctr']:+.1f}') + 'p')} · Non-Brand "
            f"{renk(sifirla(f'{NB[SIMDI]['ctr'] - NB[GECEN_YIL]['ctr']:+.1f}') + 'p')}",
            f"Toplam CTR {{g:%{TOP[GECEN_YIL]['ctr']:.1f} → %{TOP[SIMDI]['ctr']:.1f}}} yükselirken brand CTR "
            f"{{r:%{BR[GECEN_YIL]['ctr']:.1f} → %{BR[SIMDI]['ctr']:.1f}}} gerilemiştir; artış non-brand tarafından "
            f"({{g:%{NB[GECEN_YIL]['ctr']:.1f} → %{NB[SIMDI]['ctr']:.1f}}}) gelmektedir.",
        ]},
    ],
})

HEAD = ["Ağu 25", "Tem 26", "Ağu 26", "MoM", "YoY"]
SEGLER = (("brand", "Brand"), ("nonbrand", "Non-Brand"), ("toplam", "Toplam"))


def seg_rows(metrik):
    return [[ad, k(SEG[s][GECEN_YIL][metrik]), k(SEG[s][ONCEKI][metrik]), k(SEG[s][SIMDI][metrik]),
             d(s, metrik), d(s, metrik, b=GECEN_YIL)] for s, ad in SEGLER]


def oran_rows(metrik, fmt, ters=False):
    out = []
    for s, ad in SEGLER:
        a = SEG[s]
        v5, vt, va = a[GECEN_YIL][metrik], a[ONCEKI][metrik], a[SIMDI][metrik]
        f = (lambda x, y: sifirla(f"{x - y:+.1f}")) if ters else (lambda x, y: sifirla(f"{y - x:+.1f}") + "p")
        out.append([ad, fmt(v5), fmt(vt), fmt(va), f(vt, va), f(v5, va)])
    return out


S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Dönem Karşılaştırması"],
    "title": "Brand ve Non-Brand Ağustos Karşılaştırması",
    "subtitle": "Ağustos 2026 & Temmuz 2026 (MoM) & Ağustos 2025 (YoY)",
    "source": KAYNAK_GSC,
    "grid": [50, 50],
    "footnotes": [
        "Pozisyonda pozitif değer iyileşmedir; CTR değişimi puan (p) olarak verilmiştir. Non-Brand pozisyonu, "
        "marka ifadelerinin regex ile dışlandığı ayrı bir ölçümden alınmıştır. " + DIPNOT_NUM,
    ],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.26,
              "head": ["Click"] + HEAD, "rows": seg_rows("click"), "bold_rows": [-1]}, **T),
        dict({"type": "table", "col": 1, "first_col_max": 0.26,
              "head": ["Impression"] + HEAD, "rows": seg_rows("impr"), "bold_rows": [-1]}, **T),
        dict({"type": "table", "col": 0, "mt": 8, "first_col_max": 0.26,
              "head": ["CTR"] + HEAD, "rows": oran_rows("ctr", lambda v: f"%{v:.1f}"),
              "bold_rows": [-1]}, **T),
        dict({"type": "table", "col": 1, "mt": 8, "first_col_max": 0.26,
              "head": ["Ort. pozisyon"] + HEAD, "rows": oran_rows("poz", lambda v: f"{v:.1f}", ters=True),
              "bold_rows": [-1]}, **T),
        {"type": "insights", "col": "full", "mt": 8, "font_pt": 10.5, "items": [
            f"Brand CTR yıllık bazda {{r:%{BR[GECEN_YIL]['ctr']:.1f} → %{BR[SIMDI]['ctr']:.1f}}} gerilerken pozisyon "
            f"{{g:{BR[GECEN_YIL]['poz']:.1f} → {BR[SIMDI]['poz']:.1f}}} ile korunmuştur. Non-Brand tarafında CTR "
            f"{{g:%{NB[GECEN_YIL]['ctr']:.1f} → %{NB[SIMDI]['ctr']:.1f}}} yükselmiş, click kaybı brand'e göre sınırlı kalmıştır "
            f"({renk(d('nonbrand', 'click', b=GECEN_YIL))}).",
        ]},
    ],
})

# ------------------------------------------------------------ marka talebi
OZ, OZT = HZ["özdilek"], HZ["özdilekteyim"]
S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Marka Talebi"],
    "title": "Marka Arama Hacmi ve Brand Click",
    "subtitle": "Ağu 2025 - Ağu 2026 | Türkiye | marka terimleri ayrı satırlarda, organik click ile yan yana",
    "source": "Google Ads arama hacmi & Google Search Console",
    "grid": [100],
    "footnotes": [
        "\"ozdilek\", \"öz dilek\" ve \"özdikek\" yakın varyant olarak \"özdilek\" ile aynı seriyi taşıdığından ayrı satır "
        "açılmamıştır. Hacim bant halinde döndüğü için dönem uçları karşılaştırılmıştır. Click sol, hacimler sağ eksendedir.",
    ],
    "blocks": [
        {"type": "combo", "col": "full", "h": 170, "bar_w": 26, "cats": ET, "series": [
            {"kind": "bar", "name": "Brand click", "data": [BR[y]["click"] for y in AYLAR],
             "color": "gray_bar", "axis": "left"},
            {"kind": "line", "name": "\"özdilek\" arama hacmi", "data": [OZ[y] for y in AYLAR],
             "color": "teal", "axis": "right"},
            {"kind": "line", "name": "\"özdilekteyim\" arama hacmi", "data": [OZT[y] for y in AYLAR],
             "color": "coral", "axis": "right"},
        ]},
        dict({"type": "table", "col": "full", "mt": 10, "first_col_max": 0.15,
              "head": ["Metrik"] + ET,
              "rows": [["özdilek hacmi"] + [k(OZ[y]) for y in AYLAR],
                       ["özdilekteyim hacmi"] + [k(OZT[y]) for y in AYLAR],
                       ["Brand click"] + [k(BR[y]["click"]) for y in AYLAR],
                       ["Brand CTR"] + [f"%{BR[y]['ctr']:.1f}" for y in AYLAR]]}, **T),
        {"type": "insights", "col": "full", "mt": 10, "font_pt": 10, "items": [
            f"MoM ({ET_ONCEKI} → {ET_SIMDI}): Brand click {renk(d('brand', 'click'))} · "
            f"\"özdilek\" hacmi {renk(pct(OZ[SIMDI], OZ[ONCEKI]))} · "
            f"\"özdilekteyim\" hacmi {renk(pct(OZT[SIMDI], OZT[ONCEKI]))}",
            f"YoY ({ET_GECEN} → {ET_SIMDI}): Brand click {renk(d('brand', 'click', b=GECEN_YIL))} · "
            f"\"özdilek\" hacmi {renk(pct(OZ[SIMDI], OZ[GECEN_YIL]))} · "
            f"\"özdilekteyim\" hacmi {renk(pct(OZT[SIMDI], OZT[GECEN_YIL]))}",
            f"İki marka teriminde de talep korunurken brand click {{r:{k(BR[GECEN_YIL]['click'])} → {k(BR[SIMDI]['click'])}}} "
            f"gerilemiştir; düşüşün talep kaynaklı olmadığına işaret etmektedir.",
        ]},
    ],
})

# ------------------------------------------------------------ brand sorguları
_, br_dus = hareketler(Q, "a26", "a25", lambda q: bool(BRAND.search(q)), 7)
br_art, _ = hareketler(Q, "a26", "a25", lambda q: bool(BRAND.search(q)), 7)
S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Query Değişimleri"],
    "title": "Brand Sorgularında Yıllık Click Değişimi",
    "subtitle": "Ağustos 2026 & Ağustos 2025 | YoY | click değişimine göre sıralı",
    "source": KAYNAK_GSC + " · Query kırılımı & Google Ads arama hacmi",
    "grid": [50, 50],
    "footnotes": [
        "Arama hacmi Ağustos 2026 aylık değeridir. ASCII yazımlarda (\"ozdilek\", \"ozdilekteyim\") hacim Türkçe karakterli "
        "yazımla birlikte değerlendirildiği için ayrıca verilmemiştir. Query tablosu Search Console'un ilk 5.000 sorgusundan oluşturulmuştur.",
    ],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.40,
              "head": ["Click azalan", HB, "Ağu 25", "Ağu 26", "Δ"],
              "rows": [[q, k(hacim(q)), n(b), n(a), n(x)] for q, b, a, x in br_dus]}, **T),
        dict({"type": "table", "col": 1, "first_col_max": 0.40,
              "head": ["Click artan", HB, "Ağu 25", "Ağu 26", "Δ"],
              "rows": [[q, k(hacim(q)), n(b), n(a), f"+{n(x)}"] for q, b, a, x in br_art]}, **T),
        {"type": "insights", "col": "full", "mt": 12, "font_pt": 10.5, "items": [
            f"Düşüş kısa marka sorgularında toplanmaktadır: {{c:\"özdilek\"}} {{r:{n(br_dus[0][3])}}}, {{c:\"özdilekteyim\"}} "
            f"{{r:{n(br_dus[1][3])}}} click. Bu sorguların ağırlıkla anasayfaya indiği görülmektedir; anasayfa click'i aynı dönemde "
            f"{{r:{n(P['a25']['https://www.ozdilekteyim.com/']['click'])} → {n(P['a26']['https://www.ozdilekteyim.com/']['click'])}}} gerilemiştir.",
            "Marka + ürün sorguları ise artış göstermektedir ({c:özdilek bornoz}, {c:özdilek avm}, {c:özdilek nevresim takımı}); "
            "ürün niyetli marka aramalarında organik görünürlüğün korunduğu görülmektedir.",
        ]},
    ],
})

# ------------------------------------------------------------ sayfa grupları
GRUP_TANIM = {
    "magaza": ("Mağaza", "/magaza/ altındaki kategori ve ürün sayfaları. Grup Marka + Kategori sayfalarını da kapsamaktadır."),
    "market": ("Market", "/market altındaki sayfalar."),
    "cp2": ("Marka + Kategori", "-cp2 ile biten, marka ve kategoriyi birlikte hedefleyen sayfalar. Eylül 2025'te yayına "
                                "alındığı için yıllık değişim yerine \"yeni\" yazılmıştır."),
}


def grup_slayt(g, yorum):
    ad, tanim = GRUP_TANIM[g]
    a = SEG[g]
    yoy = (lambda m: "yeni") if g == "cp2" else (lambda m: d(g, m, b=GECEN_YIL))
    return {
        "type": "content",
        "breadcrumb": ["SEARCH CONSOLE", "Sayfa Grupları"],
        "title": f"{ad} Sayfaları: Click, Impression ve Sıralama",
        "subtitle": f"Ağu 2025 - Ağu 2026 | aylık | Ağustos 2026 click MoM {d(g, 'click')} · YoY {yoy('click')}",
        "source": KAYNAK_GSC + " · Page filtresi",
        "grid": [100],
        "footnotes": [
            f"{ad}: {tanim}",
            "Grafikte click sol eksende bar, impression sağ eksende çizgi; ortalama pozisyon kendi ölçeğinde ve ters eksenlidir "
            "(yükselen çizgi iyileşme). Isı haritasında pozisyon satırı ters okunur.",
        ],
        "blocks": [
            {"type": "combo", "col": "full", "h": 200, "bar_w": 44, "cats": ET, "series": [
                {"kind": "bar", "name": "Click", "data": [a[y]["click"] for y in AYLAR],
                 "color": "gray_bar", "axis": "left", "pad": 1.8, "labels": "inside",
                 "labels_text": [k(a[y]["click"]) for y in AYLAR]},
                {"kind": "line", "name": "Impression", "data": [a[y]["impr"] for y in AYLAR],
                 "color": "teal", "axis": "right", "pad": 1.8, "labels": "uclar",
                 "labels_text": [k(a[y]["impr"]) for y in AYLAR]},
                {"kind": "line", "name": "Ort. pozisyon", "data": [round(a[y]["poz"], 1) for y in AYLAR],
                 "color": "coral", "axis": "own", "band": [0.56, 0.80], "invert": True, "fmt": "pos", "labels": "above",
                 "labels_text": [f"{a[y]['poz']:.1f}" for y in AYLAR]},
            ]},
            dict({"type": "table", "col": "full", "mt": 8, "first_col_max": 0.11, "heat": True,
                  "heat_invert_rows": [2],
                  "head": ["Metrik"] + ET,
                  "rows": [["Click"] + [k(a[y]["click"]) for y in AYLAR],
                           ["Impression"] + [k(a[y]["impr"]) for y in AYLAR],
                           ["Ort. poz."] + [f"{a[y]['poz']:.1f}" for y in AYLAR],
                           ["CTR"] + [f"%{a[y]['ctr']:.2f}" for y in AYLAR]]}, **{**T, "font_pt": 9.5}),
            {"type": "insights", "col": "full", "mt": 6, "font_pt": 10,
             "items": [f"MoM ({ET_ONCEKI} → {ET_SIMDI}): Click {renk(d(g, 'click'))} · "
                       f"Impression {renk(d(g, 'impr'))} · Ort. pozisyon "
                       f"{renk(sifirla(f'{a[ONCEKI]['poz'] - a[SIMDI]['poz']:+.1f}'), ters=True)}",
                       f"YoY ({ET_GECEN} → {ET_SIMDI}): Click "
                       f"{'yeni' if g == 'cp2' else renk(d(g, 'click', b=GECEN_YIL))} · "
                       f"Impression {'yeni' if g == 'cp2' else renk(d(g, 'impr', b=GECEN_YIL))} · "
                       f"Ort. pozisyon "
                       f"{'-' if g == 'cp2' else renk(sifirla(f'{a[GECEN_YIL]['poz'] - a[SIMDI]['poz']:+.1f}'), ters=True)}"]
                      + yorum},
        ],
    }


MG, MK, CP = SEG["magaza"], SEG["market"], SEG["cp2"]
S.append(grup_slayt("magaza", [
    f"Impression yıllık {renk(d('magaza', 'impr', b=GECEN_YIL))} daralırken CTR "
    f"{{g:%{MG[GECEN_YIL]['ctr']:.2f} → %{MG[SIMDI]['ctr']:.2f}}} yükselmiş, click kaybı sınırlı kalmıştır.",
]))
S.append(grup_slayt("market", [
    f"Click Nisan 2026'dan bu yana {{b:9-10K}} bandındadır; ortalama pozisyon Ekim-Kasım 2025'teki {{b:7.2-7.4}} "
    f"seviyesinden {{r:{MK[SIMDI]['poz']:.1f}}} seviyesine gerilemiştir.",
]))
S.append(grup_slayt("cp2", [
    f"Impression Eylül 2025'ten bu yana her ay artmıştır; click Nisan 2026'da {{b:{k(CP[202604]['click'])}}} ile zirve "
    f"yapmış, ortalama pozisyon {{b:7.3-8.4}} bandında kalmıştır.",
]))

# ------------------------------------------------------------ non-brand sorgu MoM
nb_art, nb_dus = hareketler(Q, "a26", "t26", lambda q: not BRAND.search(q), 7)
S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Query Değişimleri"],
    "title": "Non-Brand Sorgularda Click Değişimi",
    "subtitle": "Ağustos 2026 & Temmuz 2026 | MoM | click değişimine göre sıralı",
    "source": KAYNAK_GSC + " · Query kırılımı & Google Ads arama hacmi",
    "grid": [50, 50],
    "footnotes": [
        "Arama hacmi Ağustos 2026 aylık değeridir; hacim verisi dönmeyen sorgularda \"-\" yazılmıştır.",
    ],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.42,
              "head": ["Click artan", HB, "Tem", "Ağu", "Δ"],
              "rows": [[q, k(hacim(q)), n(b), n(a), f"+{n(x)}"] for q, b, a, x in nb_art]}, **T),
        dict({"type": "table", "col": 1, "first_col_max": 0.42,
              "head": ["Click azalan", HB, "Tem", "Ağu", "Δ"],
              "rows": [[q, k(hacim(q)), n(b), n(a), n(x)] for q, b, a, x in nb_dus]}, **T),
        {"type": "insights", "col": "full", "mt": 12, "font_pt": 10.5, "items": [
            "Artış ev tekstili ve çanta sorgularında yoğunlaşmaktadır: {c:benetton çanta} {g:+184}, {c:çeyiz seti} {g:+166}, "
            "{c:banyo paspası} {g:+150}, {c:bornoz takımı} {g:+128}. Okul dönemi yaklaşırken {c:chimola okul çantası} {g:+123} click eklemiştir.",
            "Düşüşler sezon ve kampanya ürünlerinde yoğunlaşmaktadır: {c:plaj havlusu} hacmi {r:33.1K → 18.1K} ile daralmış, "
            "{c:crocs ballet} ve {c:dünya kupası albümü} Ağustos'ta click almamıştır. {c:valiz} sorgusunda hacim {b:74.0K} ile "
            "değişmezken pozisyon {r:7.2 → 8.6} gerilemiştir; {c:kabin boy valiz} tarafında da pozisyon {r:7.6 → 9.2} gerilemiştir.",
        ]},
    ],
})

# ------------------------------------------------------------ sayfa MoM
s_art, s_dus = hareketler(P, "a26", "t26", n=7)
S.append({
    "type": "content",
    "breadcrumb": ["SEARCH CONSOLE", "Sayfa Değişimleri"],
    "title": "Click Değişimi En Yüksek Sayfalar",
    "subtitle": "Ağustos 2026 & Temmuz 2026 | MoM | click değişimine göre sıralı",
    "source": KAYNAK_GSC + " · Page kırılımı",
    "grid": [50, 50],
    "footnotes": ["URL'ler kök alan adı çıkarılarak kısaltılmıştır; tamamı ozdilekteyim.com altındadır."],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.56,
              "head": ["Click artan sayfa", "Tem", "Ağu", "Δ"],
              "rows": [[(yol(u) if yol(u) != "/" else "/ (anasayfa)")[:40], n(b), n(a), f"+{n(x)}"]
                       for u, b, a, x in s_art]}, **T),
        dict({"type": "table", "col": 1, "first_col_max": 0.56,
              "head": ["Click azalan sayfa", "Tem", "Ağu", "Δ"],
              "rows": [[yol(u)[:40], n(b), n(a), n(x)] for u, b, a, x in s_dus]}, **T),
        {"type": "insights", "col": "full", "mt": 12, "font_pt": 10.5, "items": [
            "{c:/magaza/bornoz-2} {g:+1.558} click ile en yüksek artışı göstermiştir; {c:nevresim}, {c:çeyiz setleri} ve "
            "{c:aile seti} kategori sayfaları da ev tekstili tarafındaki toparlanmayı taşımaktadır.",
            "Azalan sayfaların önemli bölümü dönemsel ürün ve kampanya sayfalarıdır (dünya kupası albümü, anında indirim, "
            "plaj havlusu, mayo-bikini). {c:/magaza/pike-pike-takimi} ve tek kişilik pike takımı sayfalarındaki gerileme ise "
            "yaz sezonunun kapanmasıyla ilişkilendirilebilir.",
        ]},
    ],
})


# ================================================================= GA4
def ga4_bolumu():
    """GA4 export'ları gelince doldurulur: aylık toplam/organik session, kanal
    dağılımı (Ağu'26 / Tem'26 / Ağu'25), organik landing page ve AI referral."""
    raise NotImplementedError("GA4 export'ları henüz işlenmedi")


if GA4_HAZIR:
    S.append({"type": "separator", "no": "", "title": "GA4 Trafik"})
    S.extend(ga4_bolumu())

# ======================================================== görünürlük & rakip
SOV = json.loads((BASE / "veri/ham/seom_sov_ornek.json").read_text(encoding="utf-8"))
RV = json.loads((BASE / "veri/ham/seom_rakip_visibility.json").read_text(encoding="utf-8"))
S.append({"type": "separator", "no": "", "title": "Görünürlük ve Rakipler"})


def yuzde_fark(a, b):
    """Ay sonu değeri ile önceki döneme göre değişim (puan farkı, % biçiminde)."""
    v = sifirla(f"{b - a:+.1f}")
    return v if v == "0.0" else f"{v[0]}%{v[1:]}"


rv_satir = []
for dom in sorted(RV["google"], key=lambda dm: (dm != "ozdilekteyim.com", -RV["google"][dm]["m"][1])):
    g_, ai = RV["google"][dom], RV["aio_mobil"][dom]
    me, ci = [x * 100 for x in ai["mention"]], [x * 100 for x in ai["citation"]]
    rv_satir.append([dom, f"%{g_['d'][1]:.1f}", yuzde_fark(*g_["d"]),
                     f"%{g_['m'][1]:.1f}", yuzde_fark(*g_["m"]),
                     f"%{me[1]:.1f}", yuzde_fark(*me),
                     f"%{ci[1]:.1f}", yuzde_fark(*ci)])
S.append({
    "type": "content",
    "breadcrumb": ["GÖRÜNÜRLÜK", "Rakip Visibility"],
    "title": "Rakiplerle Google ve AI Overview Visibility Karşılaştırması",
    "subtitle": "Ağustos 2026 | 9.4K takip edilen keyword | ay sonu değeri ve önceki döneme göre değişim",
    "source": "SEOmonitor",
    "grid": [100],
    "footnotes": [
        "Visibility, takip edilen keyword'lerde domainin arama hacmine göre ağırlıklandırılmış sıralama görünürlüğüdür. "
        "AIO Mention: AI Overview yanıt metninde anılma; AIO Citation: AI Overview'da kaynak olarak link verilme. AI Overview "
        "kolonları mobil ölçümdür. Rakipler Google mobil visibility'ye göre sıralanmıştır.",
    ],
    "blocks": [
        dict({"type": "table", "col": "full", "first_col_max": 0.20,
              "head": ["Domain", "Google Desktop", "Değişim", "Google Mobil", "Değişim",
                       "AIO Mention", "Değişim", "AIO Citation", "Değişim"],
              "rows": rv_satir, "highlight_rows": [0]}, **{**T, "font_pt": 9.5, "row_h": 16}),
        {"type": "insights", "col": "full", "mt": 6, "font_pt": 9.5, "items": [
            "Özdilekteyim'in Google visibility'si desktop {g:%3.9} ({g:+%0.6}), mobil {g:%3.8} ({g:+%1.0}) ile artmıştır.",
            "Google tarafında {c:boyner.com.tr} ({g:+%1.7} / {g:+%1.2}) ve {c:lcw.com} ({g:+%1.5} / {g:+%1.1}) payını artırırken "
            "{c:hepsiburada.com} ({r:-%3.3} / {r:-%4.6}) ve {c:n11.com} gerilemiştir.",
            "AI Overview'da {c:trendyol.com} {b:%56.0} citation ile ilk sıradadır; {c:hepsiburada.com} "
            "Google'da gerilerken burada citation {g:+%12.9} artmıştır.",
        ]},
    ],
})


def ort(v, i, j):
    return sum(v[i:j]) / (j - i) * 100


sov_satir = []
for dom, v in sorted(SOV["sov"].items(), key=lambda kv: -ort(kv[1], 3, 6)):
    t_, a_ = ort(v, 0, 3), ort(v, 3, 6)
    sov_satir.append([dom, f"%{t_:.2f}", f"%{a_:.2f}", sifirla(f"{a_ - t_:+.2f}") + "p", f"%{v[5]*100:.2f}"])
oz_i = next(i for i, r in enumerate(sov_satir) if r[0] == "ozdilekteyim.com")
oz = SOV["sov"]["ozdilekteyim.com"]
S.append({
    "type": "content",
    "breadcrumb": ["GÖRÜNÜRLÜK", "Share of Voice"],
    "title": "Organik Share of Voice ve Rakip Dağılımı",
    "subtitle": "Temmuz 2026 & Ağustos 2026 | 9.368 takip edilen keyword | mobil",
    "source": "SEOmonitor",
    "grid": [58, 42],
    "footnotes": [
        "Share of Voice, takip edilen keyword'lerde sonuç sayfasında yer alan tüm domainlerin tahmini organik trafiği "
        "içindeki paydır. Aylık değer 10, 20 ve ayın son günü ölçümlerinin ortalamasıdır. Değişim puan (p) olarak verilmiştir.",
    ],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.36,
              "head": ["Domain", "Tem 26 ort.", "Ağu 26 ort.", "Δ", "31 Ağu"],
              "rows": sov_satir, "highlight_rows": [oz_i]}, **{**T, "font_pt": 9.5, "row_h": 17, "head_h": 21}),
        {"type": "insights", "col": 1, "font_pt": 10.5, "items": [
            f"Özdilekteyim'in payı Ağustos ortalamasında {{b:%{ort(oz, 3, 6):.2f}}} seviyesindedir; ay sonu ölçümünde "
            f"{{g:%{oz[5]*100:.2f}}} ile dönemin en yüksek değerine ulaşmıştır.",
            "Takip edilen set giyim, ayakkabı ve elektronik gibi geniş kategorileri kapsadığı için pazar yerleri ve fiyat "
            "karşılaştırma siteleri ilk sıralarda yer almaktadır; {c:trendyol.com} tek başına {b:%21} civarında pay almaktadır.",
            f"{{c:mediamarkt.com.tr}} Ağustos'ta {renk(sov_satir[[r[0] for r in sov_satir].index('mediamarkt.com.tr')][3])} ile "
            f"payını en çok artıran domain olmuştur; {{c:hepsiburada.com}} gerilemiştir.",
        ]},
    ],
})

G8 = json.loads((BASE / "veri/ham/seom_grup_2026-08.json").read_text(encoding="utf-8"))
G7 = {g["group_id"]: g for g in json.loads((BASE / "veri/ham/seom_grup_2026-07.json").read_text(encoding="utf-8"))}
def ay_hacim(g, ay="August", yil="2026"):
    return next(m["search_volume"] for m in g["search_data"]["monthly_searches"]
                if m["month"] == ay and m["year"] == yil)


kat = []
for g in sorted(G8, key=lambda g: -ay_hacim(g)):
    o = G7[g["group_id"]]
    vt, va = float(o["visibility"]["mobile"]["latest"]), float(g["visibility"]["mobile"]["latest"])
    rt, ra = float(o["average_rank"]["mobile"]["latest"]), float(g["average_rank"]["mobile"]["latest"])
    kat.append([g["group_name"], n(g["keywords_counters"]["main_keywords"]), k(ay_hacim(g)), f"%{vt:.1f}", f"%{va:.1f}",
                sifirla(f"{va - vt:+.1f}") + "p", f"{rt:.1f}", f"{ra:.1f}", sifirla(f"{rt - ra:+.1f}")])
S.append({
    "type": "content",
    "breadcrumb": ["GÖRÜNÜRLÜK", "Kategori Görünürlüğü"],
    "title": "Takip Edilen Kategorilerde Visibility",
    "subtitle": "31 Temmuz 2026 & 31 Ağustos 2026 | mobil | kategori klasörleri",
    "source": "SEOmonitor",
    "grid": [100],
    "footnotes": [
        "Arama hacmi, kategorideki takip edilen keyword'lerin Ağustos 2026 aylık toplamıdır; kategoriler hacme göre sıralıdır. "
        "Visibility: arama hacmine göre ağırlıklandırılmış sıralama görünürlüğü. Pozisyonda pozitif değer iyileşmedir.",
    ],
    "blocks": [
        dict({"type": "table", "col": "full", "first_col_max": 0.26,
              "head": ["Kategori", "Keyword", HB, "Visibility Tem", "Visibility Ağu", "Δ", "Ort. poz. Tem", "Ort. poz. Ağu", "Δ"],
              "rows": kat}, **{**T, "font_pt": 9, "row_h": 14, "head_h": 20}),
        {"type": "insights", "col": "full", "mt": 6, "font_pt": 9.5, "items": [
            "Görünürlük ev tekstilinde yoğunlaşmaktadır: {c:Havlu & Bornoz} {g:%64.3}, {c:Setler} {g:%56.3}; en çok kazananlar "
            "{c:Mutfak Tekstili} {g:+9.4p} ve {c:Kadın Aksesuar} {g:+3.7p}.",
            "En yüksek hacimli {c:Erkek Giyim} ({b:2.94M}), {c:Kadın Giyim} ({b:2.28M}) ve {c:Kadın Aksesuar} ({b:1.89M}) "
            "kategorilerinden yalnızca Kadın Aksesuar {b:%18.8} görünürlüğe ulaşmaktadır; giyim ve ayakkabıda {b:%1-4} bandındaki "
            "görünürlük büyüme potansiyeli taşımaktadır.",
        ]},
    ],
})

# ================================================================ yapay zeka
AI = json.loads((BASE / "veri/ham/ai_gorunurluk.json").read_text(encoding="utf-8"))
SAG = (("gemini", "Gemini"), ("google_ai_overview", "Google AI Overview"), ("chatgpt", "ChatGPT"))


def ai_satir(kod, ad):
    t_, a_ = AI["saglayici"]["2026-07"][kod], AI["saglayici"]["2026-08"][kod]
    ot, oa = t_[1] / t_[0] * 100, a_[1] / a_[0] * 100
    return [ad, f"{n(a_[1])} / {n(a_[0])}", f"%{ot:.1f}", f"%{oa:.1f}", f"{oa - ot:+.1f}p", f"{a_[2]:.1f}"]


def ai_top(ay):
    v = AI["saglayici"][ay].values()
    return sum(x[1] for x in v), sum(x[0] for x in v)


at, att = ai_top("2026-08"), ai_top("2026-07")
ai_rows = [ai_satir(kd, ad) for kd, ad in SAG]
ai_rows.append(["Toplam", f"{n(at[0])} / {n(at[1])}", f"%{att[0]/att[1]*100:.1f}", f"%{at[0]/at[1]*100:.1f}",
                f"{at[0]/at[1]*100 - att[0]/att[1]*100:+.1f}p", "-"])
rakip = sorted(list(AI["rakip_2026-08"].items()) + [("ozdilekteyim.com", at[0])], key=lambda kv: -kv[1])[:8]
oz_r = [r[0] for r in rakip].index("ozdilekteyim.com")

S.append({"type": "separator", "no": "", "title": "Yapay Zeka Görünürlüğü"})
S.append({
    "type": "content",
    "breadcrumb": ["YAPAY ZEKA", "Görünürlük Metrikleri"],
    "title": "Yapay Zeka Yanıtlarında Marka Görünürlüğü",
    "subtitle": "Ağustos 2026 & Temmuz 2026 | 124 prompt | Gemini, Google AI Overview ve ChatGPT",
    "source": "Inbound AI Görünürlük İzleme",
    "grid": [58, 42],
    "footnotes": [
        "Mention oranı: markanın anıldığı yanıtların izlenen toplam yanıt içindeki payı. Brand Position: markanın yanıt "
        "içinde kaçıncı sırada anıldığı; küçük değer daha öndedir. Aylar arasında yanıt sayısı farklı olduğu için "
        "karşılaştırma oran üzerinden yapılmıştır.",
        "Rakip tablosu, Ağustos yanıtlarında her domainin anıldığı yanıt sayısını gösterir.",
    ],
    "blocks": [
        dict({"type": "table", "col": 0, "first_col_max": 0.28,
              "head": ["Sağlayıcı", "Mention / Yanıt", "Tem 26", "Ağu 26", "Δ", "Brand Position"],
              "rows": ai_rows, "bold_rows": [-1]}, **{**T, "font_pt": 9.5, "row_h": 18, "head_h": 22}),
        dict({"type": "table", "col": 1, "first_col_max": 0.55,
              "head": ["Anılan marka", "Yanıt Ağu 26"],
              "rows": [[dom, n(v)] for dom, v in rakip], "highlight_rows": [oz_r]},
             **{**T, "font_pt": 9.5, "row_h": 17, "head_h": 21}),
        {"type": "insights", "col": "full", "mt": 10, "font_pt": 10.5, "items": [
            f"Marka Ağustos'ta {{b:{n(at[1])} yanıtın {n(at[0])}'ünde}} anılmıştır ({{g:%{at[0]/at[1]*100:.1f}}}). "
            f"En belirgin artış {{c:Google AI Overview}} tarafındadır ({renk(ai_rows[1][4])}); {{c:Gemini}} {{b:{ai_rows[0][3]}}} ile en yüksek orandadır.",
            f"Anılma sayısında Özdilekteyim {{b:{oz_r + 1}. sıradadır}}; {{c:karaca.com}} ev ve mutfak prompt'larında öne çıkmaktadır. "
            "ChatGPT tarafında oran %24 bandında kalmakta ve kategori içeriklerinde geliştirme alanı sunmaktadır.",
        ]},
    ],
})

# ================================================================ değerlendirme
S.append({"type": "separator", "no": "", "title": "Değerlendirme"})
S.append({
    "type": "content",
    "breadcrumb": ["DEĞERLENDİRME", "Öne Çıkan Başlıklar"],
    "title": "Önümüzdeki Dönemde Öne Çıkan Üç Başlık",
    "subtitle": "Ağustos 2026 bulgularından türetilen çalışma alanları",
    "source": "Google Search Console, SEOmonitor ve Inbound AI Görünürlük İzleme",
    "grid": [100],
    "footnotes": [
        "Başlıkların önceliklendirilmesi Özdilekteyim ekibinin stratejik tercihleri ve öncelikleriyle güncellenebilir.",
    ],
    "blocks": [
        {"type": "panels", "col": "full", "cols": 3, "items": [
            {"title": "Marka aramalarında organik tıklama payı", "sub": "izleme başlığı",
             "lines": [f"Brand click yıllık %{abs((BR[SIMDI]['click']/BR[GECEN_YIL]['click']-1)*100):.1f} geriledi; \"özdilek\" hacmi yatay, \"özdilekteyim\" hacmi %{(HZ['özdilekteyim'][SIMDI]/HZ['özdilekteyim'][GECEN_YIL]-1)*100:.1f} arttı.",
                       "Pozisyon korunurken CTR %25.8 seviyesinden %16.1 seviyesine indi.",
                       "Marka sorgularında ücretli sonuç ve sonuç sayfası yerleşiminin birlikte incelenmesi değerlendirilebilir."]},
            {"title": "Ev tekstili kategorilerindeki büyüme", "sub": "büyüme alanı",
             "lines": ["Bornoz, nevresim, çeyiz ve aile seti sayfaları Ağustos'ta en çok click kazanan sayfalar oldu.",
                       "Marka + Kategori sayfaları 7.9K click ile büyümesini sürdürüyor.",
                       "Sonbahar sezonuna yönelik yatak odası ve battaniye kategorilerinin önceliklendirilmesi değerlendirilebilir."]},
            {"title": "Giyim ve ayakkabıda görünürlük", "sub": "fırsat alanı",
             "lines": ["Kadın Giyim, Erkek Giyim ve ayakkabı kategorilerinde visibility %1-4 bandında.",
                       "Kadın ve Erkek Giyim birlikte 5.2M aylık arama hacmi taşıyor (2026 Ağustos).",
                       "Marka + Kategori sayfa yapısının bu kategorilere genişletilmesi değerlendirilebilir."]},
        ]},
        {"type": "insights", "col": "full", "mt": 14, "font_pt": 11, "items": [
            "Dönemin genel tablosu, ev tekstili ve Marka + Kategori sayfalarında organik kazanımın sürdüğünü; yıllık "
            "click kaybının ise marka aramalarındaki tıklama payı değişiminden kaynaklandığını göstermektedir.",
        ]},
    ],
})

S.append({"type": "closing", "title": "Teşekkürler"})

# ayraç numaraları ve ajanda, destedeki ayraç sırasından türetilir
seps = [s for s in S if s.get("type") == "separator"]
for i, s in enumerate(seps, 1):
    s["no"] = f"{i:02d}"
next(s for s in S if s["type"] == "agenda")["items"] = [{"no": s["no"], "label": s["title"]} for s in seps]

out = BASE / "deck.json"
out.write_text(json.dumps({"meta": {"brand": "Özdilekteyim", "period": "Ağustos 2026"}, "slides": S},
                          ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(S)} slayt -> {out}")
