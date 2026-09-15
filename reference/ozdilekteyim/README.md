# Özdilekteyim aylık deste kuralları

Özdilekteyim (ozdilekteyim.com) aylık SEO değerlendirme destesinin markaya
özgü kuralları. Genel akış `slayt-katalogu.md` → "M1 varyant - e-ticaret sayfa
gruplu aylık (Özdilekteyim tipi)".

## Deste iskeleti

```
Kapak · Akış
01 Genel Görünüm      yönetici özeti (4 KPI: click, impression, brand click,
                      non-brand click + KRİTİK TESPİT) · segment ve sayfa
                      grubu tanımları
02 Google Search Console Metrikleri
                      aylık click · aylık impression · dönem karşılaştırması
                      (click / impression / CTR / pozisyon)
                      marka arama hacmi ve brand click (C04d)
                      brand Query değişimleri (YoY)
                      Mağaza · Market · Marka + Kategori (her biri ayrı slayt, C54)
                      non-brand Query değişimleri (MoM) · Sayfa değişimleri (MoM)
03 GA4 Trafik         web-only; export gelince (GA4_HAZIR bayrağı)
04 Görünürlük ve Rakipler
                      rakip visibility Google + AI Overview (C20c)
                      organik Share of Voice · kategori visibility + hacim (C22)
05 Yapay Zeka Görünürlüğü
06 Değerlendirme · Teşekkürler
```

## Segment ve sayfa grupları

| Ad | Tanım | Not |
|---|---|---|
| Brand | query `özdilek\|ozdilek` (includingRegex) | doğrudan ölçülür |
| Non-Brand | toplam − brand | pozisyon excludingRegex ile ayrıca ölçülür; anonim hacim bu satırda |
| Mağaza | page `/magaza/` | Marka + Kategori sayfalarını da kapsar |
| Market | page `ozdilekteyim.com/market` | |
| Marka + Kategori | page `-cp2/?$` | Eylül 2025'te açıldı; YoY yerine `yeni` |

## Marka arama hacmi

- Satırlar **ayrı**: `özdilek` ve `özdilekteyim`. Toplam satırı yazılmaz.
- **`ozdilekteyim` (ASCII yazım) alınmaz.**
- `ozdilek`, `öz dilek`, `özdikek` Google Ads'te `özdilek` ile aynı seriyi
  döndürür (yakın varyant); ayrı satır açılmaz, dipnotta belirtilir.
- Grafik: iki terim ayrı bar serisi, brand click sağ eksende çizgi.

## Sayfa grupları

Mağaza, Market ve Marka + Kategori **her biri ayrı slayt** alır (C54). Her
slaytta tek grafikte click (bar, sol eksen), impression (çizgi, sağ eksen) ve
ortalama pozisyon (çizgi, `axis: "own"`, ters eksen, değer etiketli); altında
aynı üç metriğin 13 aylık tablosu.

## SEOmonitor

- Kampanya: 333234, 9.4K keyword, birincil cihaz mobil.
- Rakip seti (panel Competition sırası): trendyol.com, hepsiburada.com,
  boyner.com.tr, amazon.com.tr, lcw.com, englishhome.com, flo.com.tr, n11.com.
- Rakip visibility (C20c): Google desktop + mobile, AI Overview mention +
  citation (mobil), ay başı → ay sonu.
- Kategori visibility (C22): üst düzey kategori klasörleri, keyword sayısı +
  rapor ayı arama hacmi + visibility + ortalama pozisyon.
- Uzun dönem visibility serisi kullanılmaz: Aralık 2025 - Ocak 2026 arasında
  keyword seti genişlediği için seri kırılımlı.

## GA4

Web-only. Bölüm üretici betikte `GA4_HAZIR` bayrağının arkasında durur;
export gelmeden bölüm destede yer almaz, ajanda numaraları ayraçlardan
otomatik türetilir.

## Bağlam notları

- Eylül 2025 sonrası Search Console'da derin sıralardaki impression'lar
  daha sınırlı raporlanır; yıllık impression ve pozisyon karşılaştırmasında
  dipnot zorunlu.
- Ağustos 2026 itibarıyla brand click düşüşü talep kaynaklı değil (hacim ↑,
  pozisyon korunuyor, CTR ↓); sonraki destelerde aynı eksen izlenir.
