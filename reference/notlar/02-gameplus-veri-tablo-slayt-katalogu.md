# SEO Değerlendirme Sunumu Üretici Skill - Veri ve Süreç Notları

> **Bu dosya nedir:** Herhangi bir marka için aylık / çeyreklik / yarıyıl SEO değerlendirme sunumu üretebilecek jenerik bir skill'in **veri katmanı, tablo şemaları, slayt kataloğu ve üretim süreci** notudur.
> **Kaynak:** 7 gerçek deste satır satır analiz edilerek çıkarılmıştır (bkz. Bölüm 15 - Kaynak Deste Envanteri).
> **Dil:** İç doküman. Üretilen sunumun dili `/Users/Erdo/.claude/icerik-dili-rehberi-final.md` (Rejim [A]) kurallarına tabidir.

---

## 0. BİRLEŞTİRME NOTU (birden fazla md birleştirilecekse önce bunu oku)

Bu dosya, skill'in **"ne veriyle, nasıl, hangi sırayla"** kısmını kapsar. Bölümler `S1`-`S14` ID'leriyle numaralandırılmıştır ki başka sohbetlerden gelen md'lerle çakışmasın.

**Bu dosyanın kapsadığı alanlar:**

| Alan | Bölüm |
|---|---|
| Skill kimliği, tetikleyiciler, mod seçimi | S1 |
| Marka konfigürasyonu (brand config şeması) | S2 |
| Veri kaynakları ve çekme yöntemi | S3 |
| Ortak veri işleme kuralları (brand/non-brand, dönem, delta) | S4 |
| Sunum tipleri ve slayt iskeletleri (aylık / çeyreklik / yarıyıl / özel) | S5 |
| Slayt kataloğu (28 slayt tipi, her biri veri + tablo + insight) | S6 |
| **Zorunlu GSC & GA4 metrik tabloları (T1-T14 şemaları)** | S7 |
| Insight ve yorum üretim kuralları | S8 |
| Görsel sistem ve şablon kullanımı | S9 |
| Üretim akışı (pipeline, adım adım) | S10 |
| Kalite kontrol / teslim öncesi self-check | S11 |
| Bilinen tuzaklar ve metodolojik şerhler | S12 |
| Çıktı dosya yapısı | S13 |
| Genişletme noktaları (bu dosyada bilinçli boş bırakılanlar) | S14 |
| Kaynak deste envanteri | S15 |

**Bu dosyanın kapsamadığı, başka md'den gelmesi beklenen alanlar** (S14'te işaretlendi): PPTX şablon dosyası ve layout ID eşlemesi, renk/tipografi token'ları, grafik üretim kodu (pptxgenjs / python-pptx), SEOmonitor & Ahrefs API çağrı detayları, marka bazlı geçmiş dönem arşivi.

**Birleştirme kuralı:** Başka bir md aynı konuyu kapsıyorsa, **tablo şemaları (S7) bu dosyadan alınmalıdır** - gerçek destelerden birebir çıkarıldı. Slayt kataloğu (S6) ise birleştirilebilir, çakışan slayt tipleri tek isim altında toplanmalıdır.

---

## S1. Skill Kimliği ve Mod Seçimi

### S1.1. Ne yapar

Bir marka, bir dönem ve bir veri paketi alır; ajans standardında SEO değerlendirme sunumu (PPTX) üretir. Sunum, marka ekibine sunulacak varsayımıyla hazırlanır (iç sürüm yoktur).

### S1.2. Tetikleyiciler

`aylık SEO sunumu`, `çeyreklik SEO değerlendirme`, `Q1/Q2/Q3/Q4 sunumu`, `H1/H2 değerlendirme`, `SEO performans sunumu hazırla`, `<marka> <ay> sunumu`, `deste hazırla`, `SEO deck`, `değerlendirme sunumu`.

### S1.3. Mod matrisi

Skill dört modda çalışır. Mod, kullanıcının verdiği dönem ifadesinden otomatik seçilir; belirsizse sorulur.

| Mod | Tetikleyen dönem | Ana kıyas ekseni | Tipik slayt sayısı |
|---|---|---|---|
| **M1 - Aylık** | "Haziran 2026", "Temmuz ayı" | MoM + YoY | 20-32 |
| **M2 - Çeyreklik** | "2026 Q1", "ilk çeyrek" | QoQ + Q-YoY | 30-55 |
| **M3 - Yarıyıl** | "H1 2026", "ilk 6 ay" | H-YoY (6 aylık ortalama + toplam) | 22-35 |
| **M4 - Özel / etki analizi** | "SSR etkisi", "domain geçişi", "migrasyon sonrası" | Simetrik pencere (N hafta vs N hafta) | 15-25 |

**Birleşik mod (M1+M2):** Çeyreğin son ayında aylık deste hazırlanırken çeyreklik bölüm **aynı destenin sonuna ayrı kapak + ayrı ajanda ile** eklenir. Gerçek örnek: VitrA Mart 2026 destesi 21 slayt aylık + slayt 22'de "VitrA | 2026 Q1 SEO Değerlendirme" ara kapağı + 25 slayt çeyreklik bölüm. Bu, çeyreklik için ayrı deste açmaya tercih edilen ev pratiğidir.

### S1.4. Ölçek eksenleri (mod'dan bağımsız iki değişken)

1. **Property sayısı:** Tek domain (Enerjisa, KIKO, Gameplus) / çift domain (VitrA: online.vitra + vitra.com.tr) / çok property (Turkcell: com.tr + Telco + Superonline + Pasaj). Çok property'de her property kendi bölümü, kendi ajandası ve kendi "Neler Yaptık" + "Q+1 Plan" slaytlarıyla tekrarlanır; başa ortak bir Executive Summary + genel trafik bölümü konur.
2. **İş modeli:** E-ticaret (revenue, transaction, ürün funnel) / lead-gen (form success, ortalama session süresi) / abonelik-servis (üyelik, iptal sorguları, paket sayfaları). Bu seçim GA4 slaytlarının hangi metrik setini alacağını belirler (bkz. S7 / T8-T11).

---

## S2. Marka Konfigürasyonu (brand config)

Skill her marka için tek bir config nesnesiyle çalışır. Yeni marka eklemek = yeni config yazmak.

```yaml
brand:
  name: "VitrA"                      # sunum başlıklarında görünen yazım (tek yazım, tüm destede sabit)
  display_name: "VitrA | Aylık SEO Değerlendirme"
  properties:                        # birden fazlaysa her biri ayrı bölüm olur
    - key: "main"
      label: "vitra.com.tr"
      gsc_property: "sc-domain:vitra.com.tr"
      ga4_property_id: "XXXXXXX"
      url_regex: null                # alt-property ise GSC page regex'i
  business_model: "ecommerce"        # ecommerce | leadgen | subscription
  currency: "TRY"

brand_terms:                         # brand/non-brand ayrımının tek doğru kaynağı
  include: ["vitra", "vitrA", "vitra.com.tr"]
  exclude: []                        # 3. parti markalar (ör. Gameplus'ta GFN/Ubisoft)
  note: "GFN terimleri 3. parti marka olarak non-brand'e dahil edildi."

competitors:                         # arama hacmi + visibility + SoC + AI SoV tablolarında sabit sıra
  direct: ["Kale", "Creavit", "Artema", "Geberit", "Grohe"]
  marketplace: ["Trendyol", "Hepsiburada", "Koçtaş", "Bauhaus", "IKEA"]

categories:                          # kategori kırılımlı hacim ve visibility tablolarının satır seti
  - "Armatürler"
  - "Banyo Aksesuarları"
  - "Banyo Mobilyaları"
  - "Duşlar"
  - "Karo Seramik Ürünleri"
  - "Rezervuarlar"
  - "Vitrifiyeler"
  - "Yıkanma Alanları"

keyword_sets:
  brand_only: "kw/vitra_brand.csv"
  brand_category: "kw/vitra_brand_category.csv"
  non_brand: "kw/vitra_nonbrand.csv"
  kpi1: null                         # Turkcell tipi KPI kelime havuzu
  kpi2: null

tracking:
  seomonitor_project: "VitrA"
  tracked_keyword_count: 2300        # slayt metninde birebir kullanılır
  ahrefs_domain: "vitra.com.tr"

events:                              # dipnot ve yıldızlı şerh üretimi için
  - date: "2025-12"
    label: "Domain geçişi gerçekleşmiştir."
  - date: "2026-02-12"
    label: "SSR geçişi"

sections:                            # bu markada hangi opsiyonel bölümler açık
  search_volume: true
  ga4: true
  gsc: true
  visibility: true
  ai_sov: true
  core_web_vitals: false
  product_funnel: true
  what_we_did: false
  executive_summary: false
  next_quarter_plan: false
```

**Config kuralları:**

- `tracked_keyword_count` slayt metnine birebir girer ("marka özelinde belirlenen 2.300 hedef anahtar kelime takip edilmektedir"). Uydurulmaz, SEOmonitor projesinden okunur.
- `events` her veri slaytının altına yıldızlı dipnot üretir: `*2025 Aralık ayında domain geçişi gerçekleşmiştir.` Dönem, olayın etkilediği tüm slaytlarda tekrarlanır.
- `sections` açık/kapalı bayrakları, aynı skill'in KIKO tipi (CWV var, GA4 yok) ile Enerjisa tipi (Neler Yaptık + Executive Summary var, e-ticaret yok) desteleri üretebilmesini sağlar.

---

## S3. Veri Kaynakları ve Çekme Yöntemi

| Kaynak | Ne için | Erişim | Not |
|---|---|---|---|
| **Google Search Console** | Click, impression, CTR, pozisyon; query & page kırılımı; brand/non-brand ayrımı | `mcp__gsc__*` (get_search_analytics, get_advanced_search_analytics, compare_search_periods) | 16 aylık pencere sınırı. Query+page kırılımı ayrı çekilir. |
| **Google Analytics 4** | Session, user, revenue, transaction, kanal dağılımı, ürün funnel, AI referral | Manuel export veya bağlı MCP | Kanal adları GA4 varsayılan channel group'tan alınır, çevrilmez |
| **Google Keyword Planner** | Marka, marka+kategori, non-brand arama hacmi; rakip marka hacmi | Manuel export (aylık, 12-24 ay) | Hacimler bucket'lı gelir (33.1K, 40.5K); olduğu gibi kullanılır |
| **SEOmonitor** | Visibility (mobil/desktop), Share of Clicks, AI Search SoV, AI Overview SoV, kategori bazlı visibility, kelime bazlı sıralama | Panel export | Takip edilen kelime sayısı config'ten |
| **Ahrefs** | Sıralama alınan kelime dağılımı (ilk 3 / ilk 10 / ilk 100) trendi, Google update işaretlemesi | `mcp__bc3c...__site-explorer-*`, `rank-tracker-*` | Update işaretleri grafiğin altında "G" harfleriyle |
| **CrUX / CrUX Vis** | LCP, INP, CLS | cruxvis.withgoogle.com | Kaynak notu birebir yazılır |
| **DataForSEO** | Yedek SERP / hacim doğrulama | `mcp__dataforseo__*` | Müşteri çıktısında adı jenerikleştirilir |

### S3.1. GSC çekim listesi (her deste için standart)

Aşağıdaki 8 sorgu her destede çekilir; mod'a göre tarih aralıkları değişir.

| # | Boyut | Aralık | Kullanıldığı slayt |
|---|---|---|---|
| G1 | date | Son 15-16 ay | Trend grafiği, T1 |
| G2 | query | Dönem + karşılaştırma dönemi (MoM/QoQ) | T2, T3 |
| G3 | query | Dönem + geçen yıl aynı dönem (YoY) | T2, T3 |
| G4 | page | Dönem + karşılaştırma dönemi | T4 |
| G5 | query + page | Dönem | Sayfa-sorgu eşleşmesi, cannibalization kontrolü |
| G6 | date + device | Dönem | Mobil/desktop ayrımı gerekiyorsa |
| G7 | page (regex filtreli) | Dönem + karşılaştırma | Alt-property destelerinde (Telco, Pasaj tipi) |
| G8 | query (filtresiz, aynı query seti) | Dönem + karşılaştırma | **G7 ile kıyas için zorunlu** (bkz. S12.1) |

### S3.2. GA4 çekim listesi

| # | Rapor | Boyut / metrik | Kullanıldığı slayt |
|---|---|---|---|
| A1 | Traffic acquisition | Session default channel group x Sessions, Users, Revenue, Transactions | T6, kanal slaytları |
| A2 | Traffic acquisition | Organic Search, aylık seri (13-15 ay) | T7 |
| A3 | Monetization | Total + Organic revenue, transaction | T8 |
| A4 | Traffic acquisition | Source/medium filtresi: AI referral kaynakları | T9 |
| A5 | Ecommerce purchases | Item name x views, add to cart, purchases, revenue | T10 |
| A6 | Events | form_success / lead event (leadgen modelinde) | T11 |
| A7 | Pages | Landing page x sessions, engagement time (blog bölümü varsa) | Blog slaytları |

**AI referral kaynak listesi** (A4 filtresi, sabit tutulur ve dipnotta belirtilir): `chatgpt.com`, `chat.openai.com`, `perplexity.ai`, `gemini.google.com`, `copilot.microsoft.com`, `claude.ai`, `bing.com/chat`, `you.com`. Liste değişirse dipnot güncellenir; dönemler arası kıyas aynı liste ile yapılır.

---

## S4. Ortak Veri İşleme Kuralları

### S4.1. Brand / Non-Brand ayrımı

- Ayrım `brand_terms.include` regex'i ile query üzerinden yapılır. Total = Branded + Non-Branded + eşleşmeyen artık; artık ayrıca gösterilmez, "Total" satırı ham toplamdır.
- `brand_terms.exclude` içindeki 3. parti markalar non-brand'e yazılır ve **slaytta şeffaf belirtilir**: "Brand: gameplus, game+, game plus, gameplis (GFN/Ubisoft hariç)".
- Yanlış yazımlar (gameplis, vitrA, kiko milano/kiko) brand'e dahil edilir.
- Aynı deste içinde ayrım tanımı değişmez; değişmişse önceki dönem yeniden hesaplanır.

### S4.2. Dönem tanımları

| Mod | Dönem | Karşılaştırma 1 | Karşılaştırma 2 |
|---|---|---|---|
| M1 Aylık | 1-son gün, tek ay | MoM: önceki ay | YoY: geçen yıl aynı ay |
| M2 Çeyreklik | Q başı - Q sonu | QoQ: önceki çeyrek | Q-YoY: geçen yıl aynı çeyrek |
| M3 Yarıyıl | 6 ay | H-YoY: geçen yıl aynı yarıyıl | Opsiyonel: HoH (önceki yarıyıl) |
| M4 Özel | N hafta after | Simetrik N hafta before | Geçiş haftası analiz dışı |

- Dönem, alt başlıkta parantezle beyan edilir: `2026 Q1 (1 Oca - 31 Mar 2026) & 2025 Q1 (1 Oca - 31 Mar 2025) | YoY karşılaştırma`.
- **M4'te geçiş haftası analiz dışı bırakılır ve bu yazılır**: "Before: 23 Kas 2025 - 7 Şub 2026 (11 hafta) | Geçiş haftası: 8-14 Şub 2026 (analiz dışı) | After: 15 Şub - 2 May 2026 (11 hafta)".
- M3'te iki gösterim birlikte verilir: **aylık ortalama** (`2026'H1 Avg.`) ve gerekirse toplam. Hangisi olduğu kolon başlığında yazar.

### S4.3. Delta ve format kuralları

- Yüzde: `%18`, `+%6.9`, `-%37`. İşaret %'den önce, ondalık ayırıcı her yerde nokta.
- Pozisyon değişimi puan olarak ve pozitif iyileşme: `11.6 → 8.5 (+3.1 iyileşme ↑)`.
- CTR değişimi hem oransal hem puan verilebilir; puan verilirken `p` eki: `%2.23 → %2.97 (+0.73p)`.
- Büyük sayı K/M: `595.4K`, `1.2M`. Para: `₺1.49M`, `₺152K`.
- Çarpan: `3.6x`, `~3x`. Bant: `150-250K`.
- 0'dan yükselen değerlerde `+%100` yerine **"yeni"** etiketi kullanılır (Gameplus tablolarındaki pratik).
- Matematiksel olarak imkansız yüzde üretilmez; bin üzeri yüzdelerde mutlak değer de verilir: `+%1362 (+395 click)`.

### S4.4. Yuvarlama ve gösterim

| Metrik | Gösterim |
|---|---|
| Click, impression (tablo) | Tam sayı, binlik ayraç nokta: `17.637` |
| Click, impression (KPI kutusu) | K/M: `595.4K` |
| CTR | 2 ondalık: `%2.97` |
| Pozisyon | 1 ondalık: `8.5` |
| Arama hacmi | Keyword Planner bucket'ı olduğu gibi: `33.1K`, `4.400` |
| Revenue | K/M + ₺: `₺1.30M` |
| Session | K/M: `158.3K` |

---

## S5. Sunum Tipleri ve Slayt İskeletleri

Slayt tipleri S6'daki katalog ID'leriyle (`C##`) referanslanır.

### S5.1. M1 - Aylık deste (tek property, e-ticaret) - referans iskelet

```
01  Kapak                                    C01
02  SUNUM AKIŞI (numaralı ajanda)            C02
03  Bölüm ayracı: 01 Arama Hacmi & Rekabet   C03
04  Marka (only brand) arama hacmi           C04
05  Marka + kategori arama hacmi             C05
06  Non-branded arama hacmi                  C06
07  Kategori kırılımlı hacim (4 tablo)       C07
08  Rakip arama hacmi değişimi               C08
09  Bölüm ayracı: 02 GA4 Trafik              C03
10  GA4 organik trafik + session YoY/MoM     C09
11  GA4 revenue & transaction                C10
12  GA4 AI referral trafik                   C12
13  Bölüm ayracı: 03 GSC Trafik & Sıralama   C03
14  GSC brand & non-brand tablosu            C14
15  GSC organik trafik trendi                C15
16  Competitor visibility comparison         C20
17  Total Click Share + AI Search SoV        C21
18  Kategori bazında visibility değişimi     C22
19  Visibility'yi en çok etkileyen kelimeler C23
20  En iyi artış yaşayan kelimeler           C24
21  Ahrefs sıralama alınan kelime değişimi   C25
22  Teşekkürler                              C28
```

### S5.2. M1 varyant - lead-gen / kurumsal (Enerjisa tipi)

```
01  Kapak
02  SUNUM AKIŞI
03  Bölüm: 01 Neler Yaptık / Yapıyoruz
04  Neler Yaptık - İletilen + Devam Eden      C26
05  Çalışma etkisi kanıt slaytı (AI Overview) C26b
06  Bölüm: 02 Marka Aranma Hacmi
07  Marka hacmi + brand keyword değişimi      C04/C05
08  Bölüm: 03 Organik Trafik Ölçümlemesi
09  GA4 organik trafik                        C09
10  GSC click verileri                        C15
11  15 aylık brand vs non-brand session       C13
12  Bölüm: 04 Blog Performansı
13  Blog trafik YoY karşılaştırma             C18
14  Blog en çok vakit geçirilen sayfalar      C19
15  Bölüm: 05 Kelime Sıralamaları & Rekabet
16  Visibility + rakip                        C20/C21
17  Kelime performansı (artan/düşen/en iyi)   C24
18  Bölüm: 06 Executive Summary
19  Executive Summary                         C27
20  Teşekkürler
```

### S5.3. M2 - Çeyreklik deste (çok property, Turkcell tipi)

```
01  Kapak: "<Marka> <Yıl> Q<N> SEO Değerlendirme Sunumu"
02  SUNUM AKIŞI (property'ler)
03  Executive Summary (5 madde, tek slayt)          C27
04  Overall trafik: kanal bazlı YoY + QoQ tablosu   C11
05  Kanal payı trendi (5 çeyrek)                    C11b
06  Aylık kanal davranışı                           C11c
07  AI Overview'ın CTR'a etkisi                     C16
08  Marka arama talebi uzun dönem trendi            C04
--- her property için tekrarlanan blok ---
0X  Bölüm ayracı: property adı                      C03
0X  Property ajandası                               C02b
0X  Genel performans metrikleri (KPI kutuları)      C14b
0X  Branded trafik değişimi                         C14
0X  Non-branded trafik değişimi                     C14
0X  [gerekiyorsa] Impression metodoloji slaytı      C17
0X  [gerekiyorsa] Regex vs filtresiz rakam kıyası   C17b
0X  KPI anahtar kelime highlight'ları               C23b
0X  En çok trafik getiren sayfalar                  C19
0X  Sayfa kümesi / kategori bazlı performans        C19b
0X  Neler Yaptık                                    C26
0X  Rakiplerle kıyaslama - Görünürlük & SoC         C20/C21
0X  Rakiplerle kıyaslama - AI SoV                   C21b
0X  Q+1 için genel iş maddeleri                     C26c
--- blok sonu ---
XX  Teşekkürler
```

### S5.4. M3 - Yarıyıl deste

Aylık iskeleti korur, üç farkla:

1. Tüm karşılaştırmalar H-YoY'a çevrilir; MoM kolonları kaldırılır.
2. GSC ve GA4 tablolarında **aylık ortalama** satırı esas alınır (`2025'H1 Avg.` vs `2026'H1 Avg.`), toplam ikinci satır olarak eklenebilir.
3. Araya iki slayt girer: yarıyıl içindeki aylık dalgalanma grafiği (hangi ay ne oldu) ve dönemin olay çizelgesi (Google update'ler, kampanya dönemleri, site değişiklikleri).

### S5.5. M4 - Özel / etki analizi deste (Gameplus SSR tipi)

```
01  Kapak: "<Marka> SEO Performans Değerlendirmesi - <Etki> Etkisi"
02  Sunum Akışı
03  Bölüm: 01 Brand Performansı
04  Brand 15 aylık trend + anahtar bulgular      C13
05  Brand MoM (Top 10 artış / Top 10 düşüş)      C30
06  Brand YoY (Top 10 artış / Top 10 düşüş)      C30
07  Bölüm: 02 Non-Brand Performansı
08  Non-brand MoM                                C30
09  Non-brand YoY                                C30
10  Bölüm: 03 <Etki> Geçişi Etkisi
11  Genel özet: 4 segment KPI kartı              C31
12  Brand detayı (query + page tablosu)          C31b
13  Non-brand detayı                             C31b
14  Blog / içerik detayı                         C31b
15  Bölüm: 04 Hedef Takibi
16  Faz hedefi - neredeyiz + öncelikli aksiyonlar C32
17  Bölüm: 05 Sorgu & Hacim Tabloları
18  Brand sorguları: click + hacim birleşik       C33
19  <İkincil küme> sorguları: click + hacim       C33
20  Grup özeti (küme A vs küme B)                 C34
21  Teşekkürler
```

---

## S6. Slayt Kataloğu

Her slayt için: **amaç → veri girdisi → görsel yapı → insight kalıbı → kaynak notu**.

### C01 - Kapak
Marka adı + deste tipi + dönem. Format: `<Marka> | Aylık SEO Değerlendirme` / alt satır `Haziran 2026`. Çeyreklikte: `<Marka> <Yıl> Q<N> SEO Değerlendirme Sunumu`.

### C02 - SUNUM AKIŞI
Numaralı ajanda (01, 02, 03...). **Ajandadaki bölüm sayısı destedeki bölüm ayracı sayısına eşit olmalıdır** (bilinen hata: 3 bölüm ajanda, 4 bölüm deste). Başlık "SUNUM AKIŞI" veya "NELER KONUŞACAĞIZ?" olabilir; deste içinde tek varyant.

### C02b - Property ajandası
Çok property'li destelerde her property bölümünün başında, o property'nin alt başlıkları listelenir (numarasız, sade liste).

### C03 - Bölüm ayracı
Büyük numara (01/02/03) + bölüm adı. Koyu zemin. Ajandadaki numara ve adla birebir eşleşir.

### C04 - Marka (only brand) arama hacmi
- **Veri:** Keyword Planner, brand_only kelime seti, aylık, son 2-3 yıl.
- **Tablo:** satırlar = yıllar (2024/2025/2026), kolonlar = Jan-Dec, son satır `26 vs '25 Change`. Çeyreklikte ek mini tablo: `QoQ | Q-YoY`.
- **Insight:** "VitrA only brand arama hacmi Mart ayında geçtiğimiz yıla göre aynı kalmıştır."
- **Kaynak:** `Kaynak: Keyword Planner`

### C05 - Marka + kategori arama hacmi
C04 ile aynı yapı, `brand_category` kelime seti. Insight kalıbı YoY + MoM birlikte: "VitrA + keyword arama hacmi Mart ayında YoY kıyasladığımızda %13.8 artmıştır."

### C06 - Non-branded arama hacmi
C04 ile aynı yapı, `non_brand` seti. Bu slayt pazar talebinin kendisini ölçer; sonraki tüm performans yorumlarının bağlamı olur.

### C07 - Kategori kırılımlı hacim (4 tablo tek slayt)
- **Tablolar:** NonBrand YoY, NonBrand MoM, Brand+Kategori YoY, Brand+Kategori MoM. Çeyreklikte YoY + QoQ.
- **Kolonlar:** `Kategori | <Önceki dönem> Avg. | <Dönem> Avg. | Change`. Son satır `Grand Total`.
- **Insight:** en yüksek artış + en yüksek düşüş kategorileri isimle, yüzdeyle; dört tablo için ayrı paragraf.

### C08 - Rakip arama hacmi değişimi
- **Tablo:** satırlar = marka (marketplace'ler üstte, direkt rakipler altta, kendi markamız arada kendi sırasında), kolonlar = son 14-15 ay + `YoY` + `MoM` (çeyreklikte `QoQ` + `Q-YoY`).
- **Insight:** 3 cümle: (1) kendi markamız, (2) YoY artan rakipler isimle, (3) MoM hareketi.
- **Not:** Keyword Planner bucket'lı olduğu için değişimler %0 / %22 / %18 gibi tekrar eden değerler üretir; bu normaldir, yorumda tek tek her rakip için sebep aranmaz.

### C08b - Pazar yeri / kanal ayrı slaytı (KIKO tipi)
Marketplace ve perakende zincirleri ayrı slaytta gösterilir; marka rakipleriyle aynı tabloda karışmaz.

### C08c - Kelime bazında hacim artan / azalan (KIKO tipi)
- **Kolonlar:** `Keyword | <Önceki yıl dönem> | <Dönem> | Change | YoY change | Generic Keyword Search Volume YoY`.
- Son kolon imzadır: marka+kelime hacmindeki değişimin, jenerik kelimedeki değişimden ayrıştırılmasını sağlar. Marka hacmi düşerken jenerik sabitse, bu marka özelinde bir daralmadır.

### C09 - GA4 organik trafik ölçümlemesi
- **Veri:** A1 + A2.
- **Görsel:** kanal dağılımı grafiği + toplam session rakamı + organik pay yüzdesi.
- **Mini tablolar:** `Organic Sessions YoY` ve `Organic Sessions MoM` (bkz. T7).
- **Insight:** "Mart ayında gelen toplam ziyaretin (333K) %52.4'ünü (174.7K) organik kanal oluşturmaktadır." + delta cümlesi.

### C10 - GA4 revenue & transaction (e-ticaret)
Bkz. T8. Dört mini tablo: Revenue YoY, Revenue MoM/QoQ, Transaction YoY, Transaction MoM/QoQ. Her tabloda `Total`, `Organic`, `Organic/Total %` satırları.
- **Insight:** organik payın yönü ana mesajdır: "Organik kanalın toplam işlem içindeki payı %42.6'ya ulaşmıştır (+11.3 puan)."

### C10b - GA4 lead / form (leadgen modeli)
Revenue yerine: form success event sayısı, organik payı, kanal bazlı ortalama session süresi. VitrA kurumsal sitesi örneği: "Organik kanalda 122K Session'a karşılık 31 Form Success eventi atılmıştır. Sitedeki toplam başarılı formun %14'ü organikten gelmiştir."

### C11 - Kanal bazlı genel trafik (Turkcell tipi)
- **Tablo:** iki yan yana blok: `YIL (YoY)` ve `ÇEYREK (QoQ)`. Kolonlar: `Kanal | <Önceki dönem> | <Dönem> | %  | Δ session`.
- **YORUM kutusu:** toplam büyüme bağlamı: "Q1 2025: ~504.4M, Q1 2026: ~582.9M, YoY +~78.5M session, yaklaşık +%15.6 büyüme."
- Bu slayt, organik düşüşü toplam büyüme bağlamına oturtur; organik tek başına yorumlanmaz.

### C11b - Kanal payı trendi
Son 5 çeyrek (veya 12-15 ay) x ana kanallar. Cannibalization argümanının veri temeli.

### C11c - Aylık kanal davranışı
Dönem içindeki tek bir ayın (ör. Şubat) tüm kanallarda benzer davranıp davranmadığını gösterir. Tek kanala özgü olmayan düşüşün mevsimsel/sistemik olduğunu göstermek için kullanılır.

### C12 - GA4 AI referral trafik performansı
Bkz. T9. İki KPI kutusu (Sessions, Users) x iki delta (MoM/QoQ + YoY). Trend grafiği eşlik eder.
- **Insight:** yüksek yüzdeler düşük tabandan geldiği için mutlak değer de verilir.

### C13 - Uzun dönem trend (15 ay, brand vs non-brand)
- **Tablo:** satırlar `Non-Brand Sessions` / `Brand Sessions` / `Brand % Total`, kolonlar 15-23 ay.
- **Anahtar bulgular kutusu:** 3-4 madde, her biri kalın başlık + tek cümle açıklama.
- Yapısal kırılmaların (kampanya, PR, site değişikliği) görüldüğü slayt.

### C14 - GSC brand & non-brand
Bkz. T2. Ana tablo + sol tarafta 4-6 satırlık düz metin özet.
- **Insight sırası:** Total → Branded → Non-Branded; her biri impression, click, CTR sırasıyla.

### C14b - Genel performans KPI kutuları
Dört büyük rakam: `Impression (YoY)`, `Click (YoY)`, `Impression (QoQ)`, `Click (QoQ)`. Altında iki kolon: `YILLIK BÜYÜME ÖNCÜLERİ` ve `CLICK DÜŞÜŞÜNÜN KAYNAKLARI` - her biri sorgu kümesi etiketleriyle.

### C15 - GSC organik trafik trendi
Impression + click çift eksenli trend grafiği + 3-5 cümlelik okuma. Çeyreklikte grafik yerine iki mini tablo (`Impressions QoQ | Q-YoY`, `Clicks QoQ | Q-YoY`).
- **Zorunlu:** `events` config'inden gelen yıldızlı dipnot.

### C16 - AI Overview'ın CTR'a etkisi
AI Overview yayına alınma tarihi işaretli CTR trendi. Tarih net yazılır: "18 Şubat'ta AI Overview'ın yayına alınmasıyla CTR düşüşleri gözlenmeye başlanmıştır."

### C17 - Impression düşüşü metodoloji slaytı
Bkz. S12.1. Üç kutu: `Aggregation Yöntemi Farkı`, `Hedef Odaklı Impression Dağılımı`, `GSC Impression Bug`. Altında `➔ SONUÇ:` satırı.
- **İnceleme kapsamı kutusu zorunlu:** kaç ortak query, hangi iki export karşılaştırıldı.

### C17b - Regex vs filtresiz rakam kıyası
- **Tablo:** `Keyword | REGEX'Lİ Q4→Q1 | Δ% | FİLTRESİZ Q4→Q1 | Δ%`.
- Yanda iki büyük rakam: regex'li toplam değişim vs filtresiz toplam değişim.
- **Kanıt cümlesi:** "Click +%7.3 artmış; impression düşerken click artması aggregation etkisini göstermektedir."

### C18 - Blog / içerik bölümü trafiği
Dönem vs geçen yıl aynı dönem, tek büyük rakam + yüzde değişim. Düşüşse trend süresi de verilir ("2025'ten beri süregelen bir trend").

### C19 - En çok trafik getiren sayfalar
- **Tablo:** `URL | Click | Impression | Pozisyon | Kategori`. 9-20 satır.
- **Kategori dağılımı kutusu:** sayfa kümelerinin toplam click payı.
- **KEY INSIGHT satırı:** "iOS kategorisi tek başına toplam click'in ~%50'sini üretmektedir."

### C19b - Sayfa kümesi / kategori bazlı performans
- **Tablo:** `Kategori | <Dönem> Click | <Dönem> Imp | QoQ % | YoY %`. Sayfa URL'lerinin kategoriye eşlenmesi gerekir; eşleme kuralı config'te tutulur.

### C20 - Competitor visibility comparison
- **Tablo:** `Domain | Mobile Visibility | Δ Mobile | Desktop Visibility | Δ Desktop`.
- **Zorunlu tanım kutusu:** "Visibility score, <marka> projesi özelinde takip edilen kelimelerin görünürlük oranını yüzdesel olarak gösterir. <N> hedef anahtar kelime takip edilmektedir."
- **Insight:** kendi hareketimiz → pozitif ayrışan rakip → en yüksek düşüş yaşayanlar.

### C21 - Total Click Share (SoC) + AI Search SoV
- İki grafik yan yana: Share of Clicks pastası + AI Search SoV pastası.
- **Zorunlu dipnot:** "*AI Share of Voice takip edilen kelimelerin arama hacimlerine ve bu kelimelerdeki AI yanıtlarında bahsedilme ve linklenme oranına göre hesaplanır."
- **Insight:** lider marka → kendi sıramız → 3. marka → AI tarafında ayrışma.

### C21b - AI Overview SoV sıralaması
Domain x SoV x sıra tablosu veya sıralı kartlar. **Bağlam kutusu zorunlu:** AI Overview'ın ilgili pazarda ne zaman yayına alındığı.
- **AI Overview SoV ile AI Search SoV ayrı metriklerdir**, ikisi birden kullanılıyorsa ikisinin de tanımı dipnotta verilir.

### C22 - Kategori bazında visibility değişimi
Kategori x visibility Δ. Insight: artan kategoriler, sonra düşen kategoriler; ikisi de isimle ve yüzdeyle.

### C23 - Visibility'yi en çok etkileyen kelimeler
`Top Search Vol. Keywords` tablosu (SEOmonitor export'u görsel olarak yerleştirilir). Konuşmacı notu değil, slaytta okunur bir özet cümle bulunur.

### C23b - KPI anahtar kelime highlight'ları
KPI1 / KPI2 kelime havuzlarının pozisyon ve click değişimi. Havuz config'ten gelir.

### C24 - En iyi artış yaşayan kelimeler / en çok düşen
İki-üç panel: `En İyi Artış Yaşayan Kelimeler`, `YoY Aranma Hacmi En Çok Artan Kelimeler`, `En Çok Düşüş Yaşayan`.

### C24b - Keyword rank MoM tablosu (KIKO tipi)
`Keyword | Volume | <Önceki ay> Rank | <Ay> Rank | MoM Change`. Kategori başına ayrı slayt. 100 = takipte ilk 100'de yok anlamındadır ve bu dipnotta belirtilir.

### C25 - Ahrefs sıralama alınan kelime değişimi
İlk 3 / ilk 10 / ilk 100 kelime sayısı trendi.
- **Zorunlu okuma kılavuzu:** "Tablo altındaki G ifadeleri Google update'lerini, yeşil daireler büyük çaplı içerik değişikliklerini göstermektedir."

### C26 - Neler Yaptık / Devam Eden Çalışmalar
İki kolon: `İletilen Çalışmalar` ve `Devam Eden Çalışmalar`. İsim cümlesi listesi ("Kategori içerikleri", "Schema markup çalışmaları"). Efor kanıtı slaytıdır; tarih verilmez, statü etiketi Türkçe ve şeffaf olur.

### C26b - Çalışma etkisi kanıt slaytı
Yapılan bir çalışmanın somut sonucu (ör. yeni içeriğin AI Overview'da kaynak olarak alınması + sıralama ekran görüntüsü). Ekran görüntüsü kullanılır ama bulgunun özü metinde de yazılır.

### C26c - Q+1 / sonraki dönem iş maddeleri
Madde listesi. Tarih veya gün/hafta verilmez; gerekirse `Öncelik 1/2/3` veya `Faz 1/2/3` kullanılır. Emir kipi kullanılmaz, isim-fiil yapısı tercih edilir ("Cannibalization yaşayan sayfaların optimize edilmesi").

### C27 - Executive Summary
İki biçimde kullanılır:
1. **Başta, 5 maddelik tez slaytı** (Turkcell): her madde tek cümlelik iddia. Detay konuşmacı notunda.
2. **Sonda, kırılımlı özet** (Enerjisa): en çok tıklama alan 5 query, tıklama artan ilk 5, tıklama kaybeden ilk 5, ardından `Stratejik Çıkarımlar` bloğu (4-5 paragraf, her biri bir bulguyu aksiyona bağlar).

### C28 - Teşekkürler
Kapanış. İstenirse öncesine "sonraki adım" slaytı eklenir: özet dolgusuyla değil bir sonraki adımla bitirilir.

### C30 - Top 10 artış / Top 10 düşüş query tablosu (Gameplus imzası)
- **Yapı:** tek slaytta iki tablo yan yana. Kolonlar: `Query | <Önceki dönem> | <Dönem> | Δ Click | Δ %`.
- **Üst satır:** toplam click değişimi: "Toplam click: 1.646 → 1.443 (Δ -203 | -%12.3)".
- **Kapsam şerhi:** "Top 1364 query üzerinden, long-tail kapsam dışı".
- **Altta:** kalın başlıklı tek paragraf yorum + `Sayfa Bazında MoM Top 5 Düşüş:` satırı (URL → before→after (Δ) formatında, `•` ile ayrılmış).

### C31 - Etki analizi genel özet (M4)
4 segment kartı (GENEL / BRAND / NON-BRAND / BLOG), her kartta: dönem sonu değer, Δ mutlak + Δ%, `Before:` referans değeri. Altında `Anahtar Bulgular` bloğu: 4 madde, kalın başlık + açıklama.

### C31b - Etki analizi segment detayı
Query bazında ve sayfa bazında iki tablo (`Before | After | Δ Click | Δ %`), altında kalın başlıklı yorum paragrafı.

### C32 - Faz / hedef takibi
Faz çizelgesi (geçmiş fazlar gerçekleşen, gelecek fazlar forecast etiketli) + mevcut konum yüzdesi + kalan mesafe + numaralı öncelikli aksiyonlar (1-4).
- **Zorunlu:** forecast rakamlarının forecast olduğu etiketle belirtilir.

### C33 - Sorgu performansı: click + arama hacmi birleşik tablo
- **Kolonlar:** `Sorgu | Click <Ay1..Ay4> | ΔClick <A→B> | ΔClick <A→C> | Hacim <Ay1..Ay4> | ΔHacim <A→B> | ΔHacim <A→C>`.
- **İki bölüm:** `▲ TOP 10 ARTIŞ` ve `▼ TOP 10 DÜŞÜŞ`, sıralama kriteri başlıkta yazılır.
- **Altında 3 madde yorum:** talep yönü, trafik yönü, ikisinin ilişkisi.
- Bu slayt tipi, **trafik kaybının performanstan mı talepten mi geldiğini** ayırmak için kullanılır. Ajansın en güçlü savunma aracıdır.
- **Dipnot:** "- : Keyword Planner'da ayrı veri yok", yazım varyantlarının hangi ana terim altında sayıldığı.

### C34 - Sorgu grubu özeti
İki küme (ör. Brand vs GFN) x 4 metrik (Click, Impression, Arama Hacmi, Pozisyon) x aylık kolonlar + Δ kolonları. Sonuç cümlesi: hangi kümede talep-trafik ayrışması var.

### C35 - Core Web Vitals
LCP, INP, CLS dağılım grafikleri. `Kaynak: CrUX Vis https://cruxvis.withgoogle.com/`.

### C36 - Ürün funnel performansı (e-ticaret)
Bkz. T10. `EN ÇOK GÖRÜNTÜLENEN / EN ÇOK SEPETE EKLENEN / EN ÇOK SATILAN / EN YÜKSEK REVENUE` dörtlüsü, her biri Top 5.

### C36b - Funnel conversion analizi
Üç panel: `PDP OPTİMİZASYON ADAYLARI` (yüksek view, düşük conversion), `CART ABANDONMENT` (sepete eklenmiş, satın alınmamış), `EN VERİMLİ ÜRÜNLER`. Kolonlar: `Ürün | V/C/P | oran %`. Eşikler slaytta yazılır (`<%0.3`, `cart→purch <%2`, `≥5 satış`).

### C37 - Kanal bazlı geçiş karşılaştırması (M4 / migrasyon)
`Kanal | Sess before | Sess after | Sess Δ% | Rev before | Rev after | Rev Δ% | Prch before | Prch after | Prch Δ%`. Üstte 4 KPI kartı (Sessions, Users, Purchases, Revenue).

---

## S7. GSC ve GA4 Metrik Tabloları - Kanonik Şemalar

> Bu bölüm skill'in çekirdeğidir. **Her marka destesinde T1, T2, T4, T6, T7 zorunludur.** Diğerleri iş modeline ve moda göre açılır.

### T1 - GSC aylık genel seri

Kullanım: trend grafiği ve 15 aylık tablolar.

| Alan | Tip | Not |
|---|---|---|
| `month` | YYYY-MM | 15-16 ay |
| `clicks` | int | |
| `impressions` | int | |
| `ctr` | % 2 ondalık | |
| `position` | float 1 ondalık | |

Aylık modda son 15 ay, çeyreklikte son 8 çeyrek + son 15 ay, yarıyılda son 3 yarıyıl + son 18 ay.

### T2 - GSC brand / non-brand kırılımı (deste omurgası)

Yatay yapı, mod'a göre kolon grubu değişir:

```
        | Impressions <DELTA> |            | Clicks <DELTA>  |            | CTR <DELTA>     |
        | P0    | P1    | %Chg | P0   | P1   | %Chg | P0   | P1   | %Chg
Total            |
Branded Queries  |
Non-Branded Queries |
```

| Mod | `<DELTA>` | P0 | P1 |
|---|---|---|---|
| M1 | YoY | geçen yıl aynı ay | dönem ayı |
| M1 (ek) | MoM | önceki ay | dönem ayı |
| M2 | QoQ + YoY (iki tablo alt alta) | önceki çeyrek / geçen yıl aynı çeyrek | dönem çeyreği |
| M3 | H-YoY | geçen yıl aynı yarıyıl ortalaması | dönem yarıyıl ortalaması |

**Kurallar:**
- Satır sırası sabit: Total → Branded → Non-Branded.
- CTR değişimi puan farkı olarak da verilebilir; hangisi olduğu net olmalıdır.
- Bu tablo aynı destede birden fazla property için tekrarlanıyorsa kolon yapısı aynı kalır.

### T3 - GSC query bazlı Top artış / Top düşüş

| Alan | Tip |
|---|---|
| `query` | text |
| `clicks_p0` | int |
| `clicks_p1` | int |
| `delta_clicks` | int, işaretli |
| `delta_pct` | %, işaretli; p0=0 ise `yeni` |

- Her yönde 10 satır. Sıralama `delta_clicks` mutlak değerine göre.
- Tablo üstünde toplam: `Toplam click: <p0> → <p1> (Δ <n> | <%>)`.
- Kapsam şerhi zorunlu: kaç query üzerinden çalışıldı, long-tail dahil mi.

### T4 - GSC page bazlı performans

| Alan | Tip | Not |
|---|---|---|
| `url` | text | tam URL veya path |
| `clicks` | int | |
| `impressions` | int | |
| `position` | float | |
| `category` | text | config'teki path→kategori eşlemesinden |
| `clicks_p0` / `delta` | int | karşılaştırma isteniyorsa |

İki gösterim: (a) Top N sayfa listesi, (b) kategori bazında toplulaştırılmış tablo (`Kategori | Click | Imp | QoQ % | YoY %`).

### T5 - GSC sorgu + arama hacmi birleşik tablo (C33'ün veri şeması)

| Alan | Tip | Kaynak |
|---|---|---|
| `query` | text | GSC |
| `click_m1..m4` | int | GSC, ay ay |
| `delta_click_m1_m3` | % | hesaplanır |
| `delta_click_m1_m4` | % | hesaplanır |
| `volume_m1..m4` | int | Keyword Planner, ay ay |
| `delta_vol_m1_m3` | % | hesaplanır |
| `delta_vol_m1_m4` | % | hesaplanır |

Keyword Planner'da ayrı veri olmayan yazım varyantları için hücre `-` bırakılır ve dipnotta hangi ana terim altında sayıldığı yazılır.

### T6 - GA4 kanal bazlı trafik

| Alan | Tip |
|---|---|
| `channel` | GA4 default channel group, çevrilmez |
| `sessions_p0`, `sessions_p1`, `sessions_delta_pct`, `sessions_delta_abs` | |
| `users_p0`, `users_p1`, `users_delta_pct` | opsiyonel |
| `revenue_p0`, `revenue_p1`, `revenue_delta_pct` | e-ticaret |
| `purchases_p0`, `purchases_p1`, `purchases_delta_pct` | e-ticaret |

İki blok halinde gösterilir: YoY bloğu ve QoQ/MoM bloğu. `Δ session` mutlak kolonu zorunludur (yüzde tek başına yanıltıcıdır).

### T7 - GA4 organik session özeti (zorunlu)

İki mini tablo, aynı slaytta:

```
Organic Sessions <YoY>
         | <P0>   | <P1>   | % Change
Sessions | 47.9K  | 174.7K | 264.7%

Organic Sessions <MoM/QoQ>
         | <P0>   | <P1>   | % Change
Sessions | 158.3K | 174.7K | 10.4%
```

Yanına toplam trafik ve organik pay cümlesi: "Toplam ziyaretin (333K) %52.4'ünü (174.7K) organik kanal oluşturmaktadır."

### T8 - GA4 revenue & transaction (e-ticaret)

Dört mini tablo, ikişerli:

```
Revenue <YoY>                       Transaction <YoY>
                 | P0 | P1 | %Chg                    | P0 | P1 | %Chg
Total Revenue    |    |    |        Total Transaction|    |    |
Organic Revenue  |    |    |        Organic Transaction|  |    |
Organic/Total %  |    |    |        Organic/Total %  |    |    |

Revenue <QoQ/MoM>                   Transaction <QoQ/MoM>
(aynı yapı)
```

`Organic/Total %` satırındaki değişim **puan farkı**dır, yüzde değişimi değildir; metinde "puan" yazılır.

### T9 - GA4 AI referral

| Alan | Tip |
|---|---|
| `metric` | Sessions / Users |
| `p0`, `p1` | int |
| `delta_mom_or_qoq` | % |
| `delta_yoy` | % |

Kaynak filtresi listesi dipnotta verilir (bkz. S3.2). Düşük tabandan gelen yüksek yüzdelerde mutlak değer de yazılır.

### T10 - GA4 ürün funnel (e-ticaret)

| Alan | Tip |
|---|---|
| `item_name` | text |
| `views` | int |
| `add_to_cart` | int |
| `purchases` | int |
| `revenue` | ₺ |
| `view_to_purchase_pct` | % 2 ondalık |
| `cart_to_purchase_pct` | % 2 ondalık |

Türetilmiş üç liste: PDP optimizasyon adayları (`view_to_purchase < %0.3`, yüksek view), cart abandonment (`cart_to_purchase < %2`), en verimli ürünler (yüksek conv + `purchases >= 5`). Eşikler slaytta yazılır.

### T11 - GA4 lead / event (leadgen)

| Alan | Tip |
|---|---|
| `channel` | |
| `sessions` | int |
| `lead_events` | int |
| `lead_share_pct` | % (kanalın toplam lead içindeki payı) |
| `avg_session_duration` | mm:ss |

### T12 - Arama hacmi serisi (Keyword Planner)

| Alan | Tip |
|---|---|
| `set` | brand_only / brand_category / non_brand / competitor |
| `entity` | marka adı veya kategori |
| `year` | int |
| `m01..m12` | int (bucket'lı) |
| `delta_yoy`, `delta_mom`, `delta_qoq` | % |

### T13 - Visibility & SoC (SEOmonitor)

| Alan | Tip |
|---|---|
| `domain` | |
| `visibility_mobile`, `delta_mobile` | % |
| `visibility_desktop`, `delta_desktop` | % |
| `soc_p0`, `soc_p1`, `soc_delta` | % |
| `monthly_volume` | int |
| `ai_sov` | % |
| `ai_overview_sov` | % |

Domain sırası config'teki rakip sırasıyla sabit; kendi domainimiz `★` ile işaretlenebilir.

### T14 - Kategori bazlı visibility

| Alan | Tip |
|---|---|
| `category` | config'teki kategori seti |
| `visibility_p0`, `visibility_p1`, `delta` | % |

---

## S8. Insight ve Yorum Üretim Kuralları

Detaylı dil kuralları `icerik-dili-rehberi-final.md`'dedir. Burada yalnızca **sunum üretimine özgü** ek kurallar:

### S8.1. Her veri slaytında olması gerekenler

1. **Ne oldu** (sayısal cümle) - gözlem, net kip: "-mıştır / -maktadır".
2. **Ne anlama geliyor** (yorum cümlesi) - ihtiyatlı kip: "işaret etmektedir / olarak değerlendirilebilir".
3. **Opsiyonel: ne yapılabilir** - öneri kipi: "değerlendirilebilir / önerilebilir".
4. **Kaynak notu.**

Yorumsuz tablo bırakılmaz.

### S8.2. Kontrast kalıbı (ev imzası)

Negatif metrik tek başına bırakılmaz, dayanıklı metrikle yan yana verilir:
- "Session -%11 daralırken Revenue +%19 artmıştır."
- "Impression -%16.5 düşmesine rağmen click +%10.9 artmıştır; CTR +0.73p iyileşmiştir."
- "Talep -%31 daralırken click kaybı -%14 seviyesinde kalmıştır."

### S8.3. Talep-performans ayrıştırması (en kritik kural)

Trafik düşüşü yorumlanırken **arama hacmi verisi olmadan performans yorumu yapılmaz.** Üç senaryo:

| Hacim | Click | Yorum |
|---|---|---|
| ↓ | ↓ benzer oranda | Sektörel/kategorik talep daralması. Performans kaybı değil. |
| ↓ | ↓ daha az | Daralan pazarda pay korunuyor, pozitif okuma. |
| → veya ↑ | ↓ | Performans veya SERP kompozisyonu kaynaklı; incelenmesi gerekir. |

Bu ayrıştırma C33/C34 slaytlarının varlık sebebidir.

### S8.4. Insight biçimi

- Ok karakteri `➔`, tek boşluk, her insight tek okla.
- 1-2 cümle ideal, 3. cümle sebep-sonuç için.
- Vurgu: düşüş kırmızı, artış yeşil, anahtar terim coral, rakamlar bold.
- Tablo altı telegrafik insight'larda ` | ` ile çoklu madde ayrılabilir.

### S8.5. Konuşmacı notu politikası

Konuşmacı notu **kullanılabilir** ancak teslim öncesi taranır. İç değerlendirme, araç kısıtı, ajans içi yorum notlarda bırakılmaz. Notlarda yalnızca sunumu yapan kişinin sözlü olarak açacağı detay (uzun query listeleri, ek bağlam) durur.

---

## S9. Görsel Sistem ve Şablon Kullanımı

> Bu bölüm bilinçli olarak kısa tutulmuştur; tam şablon/token tanımı S14'te işaretlendiği gibi ayrı md'den gelmelidir.

- Deste, mevcut ajans PPTX şablonundan türetilir. Yeni deste sıfırdan kurulmaz; şablon slaytları çoğaltılır.
- Sabit slayt tipleri: kapak, ajanda, bölüm ayracı, tek tablo, çift tablo, tablo + yorum, KPI kartları, grafik + yorum, üç panel, teşekkürler.
- Bölüm ayracı ve kapak koyu zemin; içerik slaytları açık zemin.
- Tablo başlıkları İngilizce metrik adlarıyla kalır, yorum kolonu Türkçedir.
- Grafik ve tablo görselleri panelden export edilip yerleştirilebilir; ancak **bulgunun özü metinde de yazılır**, görsele delege edilmez.
- Şablondan kalan `SECTION TITLE`, `Lorem`, `xxx` gibi placeholder metinler teslim öncesi taranır (bilinen hata: gerçek destelerde `SECTION TITLE` kalmış).

---

## S10. Üretim Akışı

```
1. MOD ve KAPSAM
   1.1 Dönem ifadesinden mod seç (M1/M2/M3/M4). Belirsizse sor.
   1.2 Marka config'ini yükle. Yoksa oluştur (S2 şeması).
   1.3 Property sayısı ve iş modelini belirle → slayt iskeletini seç (S5).

2. VERİ TOPLAMA
   2.1 GSC: G1-G8 sorguları (S3.1). Alt-property varsa G7+G8 zorunlu.
   2.2 GA4: A1-A7 (S3.2), iş modeline göre.
   2.3 Keyword Planner export'ları (brand_only, brand_category, non_brand, competitor).
   2.4 SEOmonitor: visibility, SoC, AI SoV, kategori visibility, kelime bazlı.
   2.5 Ahrefs: sıralama dağılımı trendi.
   2.6 EKSİK VERİ: rapora yazılmaz. Chat'ten bildirilir, manuel istenir,
       gelmezse ilgili slayt komple çıkarılır ve bu chat'te "önemli" olarak belirtilir.

3. VERİ İŞLEME
   3.1 Brand/non-brand ayrımı (S4.1).
   3.2 Dönem eşleştirme ve delta hesapları (S4.2, S4.3).
   3.3 T1-T14 tablolarını üret (S7).
   3.4 Sağlama: Total >= Branded + Non-Branded; toplamlar tutuyor mu;
       imkansız yüzde var mı; 0 tabanlı deltalar "yeni" olarak işaretlendi mi.
   3.5 Alt-property destelerinde regex'li vs filtresiz karşılaştırmasını çalıştır (S12.1).

4. YORUM ÜRETİMİ
   4.1 Her tablo için gözlem cümlesi (net kip).
   4.2 Her tablo için yorum cümlesi (ihtiyatlı kip).
   4.3 Talep-performans ayrıştırması (S8.3) uygulanabilir mi kontrol et.
   4.4 Bölüm sonu sentez cümleleri.
   4.5 Executive Summary / Stratejik Çıkarımlar (açıksa).

5. DESTE ÜRETİMİ
   5.1 Şablondan slayt çoğaltma (yapısal işler önce: ekle, sil, sırala).
   5.2 İçerik doldurma.
   5.3 events config'inden yıldızlı dipnotları yerleştir.
   5.4 Kaynak notlarını yerleştir.

6. KALİTE KONTROL
   6.1 S11 self-check listesi.
   6.2 Görsel QA: PDF'e çevir, her slaytı incele (taşma, çakışma, boş placeholder).
   6.3 Dosya QA: validate.

7. TESLİM
   7.1 Deste + chat'te: eksik veriler, çıkarılan bölümler, iç kısıtlar (rapora yazılmayanlar).
```

---

## S11. Teslim Öncesi Self-Check

### S11.1. Veri tutarlılığı
- [ ] Total >= Branded + Non-Branded, her tabloda.
- [ ] Dönem tanımları destede tek biçim (hepsi Q1 2026 mı, hepsi 2026 Q1 mi).
- [ ] Aynı metriğin farklı slaytlardaki değerleri çelişmiyor.
- [ ] İmkansız yüzde yok (-%131 düşüş gibi).
- [ ] Bin üzeri yüzdelerin yanında mutlak değer var.
- [ ] 0 tabanlı deltalar "yeni" olarak işaretlendi, `+%100` yazılmadı.
- [ ] Forecast rakamları forecast olarak etiketlendi.
- [ ] Kapsam şerhleri (Top N query, long-tail hariç, örneklem) yazıldı.

### S11.2. Yapı
- [ ] Ajandadaki bölüm sayısı = destedeki bölüm ayracı sayısı.
- [ ] Bölüm numaraları tekrarlanmıyor (iki kez "02" yok).
- [ ] `SECTION TITLE` / placeholder metin kalmadı.
- [ ] Her veri slaytında kaynak notu var, format `Kaynak:` (tek dil).
- [ ] `events` dipnotları ilgili tüm slaytlarda var.
- [ ] Konuşmacı notları tarandı; iç yorum kalmadı.
- [ ] `(Shared)` gibi iç dosya adı sızıntısı yok.

### S11.3. Dil (`icerik-dili-rehberi-final.md` Bölüm 17 tam listesi ayrıca çalıştırılır)
- [ ] Em dash yok.
- [ ] Emoji yok (✓ ▲ ↑ ↓ ➔ serbest).
- [ ] Emir kipi yok, kesin vaat yok.
- [ ] Yüzde formatı tek: `+%X`, ondalık nokta - tabloda da aynı.
- [ ] Otomasyon aracı adı (Claude, MCP, skill, Playwright) sızmadı.
- [ ] İç kısıt ifadesi ("veri çekilemedi", "ölçülemiyor") rapora yazılmadı.
- [ ] Terimler tekilleştirildi (gösterim/Impression karışımı yok).
- [ ] Marka yazımı tüm destede tek biçim.

### S11.4. Görsel
- [ ] Metin taşması yok.
- [ ] Tablo hücreleri kesilmemiş.
- [ ] Grafik etiketleri okunur.
- [ ] Ekran görüntüsü kullanılan yerde bulgunun özü metinde de var.

---

## S12. Bilinen Tuzaklar ve Metodolojik Şerhler

### S12.1. GSC impression aggregation tuzağı (alt-property destelerinde zorunlu kontrol)

Bir alt-property (Telco, Pasaj gibi) URL regex'i ile filtrelendiğinde GSC **page-level aggregation** yapar: aynı query için o property'nin her sayfası ayrı impression sayılır. Filtresiz görünümde ise **property-level**: aynı query için tek impression.

Sonuç: regex'li görünümde impression toplamı doğal olarak şişkin görünür ve dönemler arası düşüş abartılı okunur. Gerçek örnekler: Telco'da regex'li -%47.5 vs filtresiz -%7.9; Pasaj'da regex'li -%67.7 vs filtresiz -%11.6.

**Kural:** Alt-property destesinde impression düşüşü raporlanmadan önce, aynı query seti üzerinden filtresiz export ile karşılaştırılır (G7 + G8). Fark anlamlıysa C17 + C17b slaytları eklenir.

**Doğrulayıcı sinyal:** Aynı dönemde click artmışsa (Telco'da +%7.3), düşüş performans kaybı değil aggregation etkisidir.

**Ek faktör:** Google'ın 3 Nisan 2026 tarihli resmi logging hatası bildirimi (13 Mayıs 2025'ten itibaren impression şişkin raporlandı, click etkilenmedi). Bu kaynağa atıfla verilir, iddia olarak değil.

### S12.2. Keyword Planner bucket etkisi
Hacimler bucket'lı gelir (27.1K, 33.1K, 40.5K...). Bu yüzden değişimler %0, %18, %22, %23 gibi tekrar eden değerlerde kümelenir. Her rakip için ayrı sebep aranmaz; tablo genel yön için okunur.

### S12.3. Domain geçişi / site değişikliği dönemleri
Geçiş dönemi kıyaslamaları simetrik pencerelerle yapılır, geçiş haftası/ayı analiz dışı bırakılır ve bu yazılır. YoY karşılaştırmalarda geçiş ayının etkisi her ilgili slaytta yıldızlı dipnotla hatırlatılır.

### S12.4. AI SoV metrik karmaşası
`AI Overview SoV` ve `AI Search SoV` farklı metriklerdir. İkisi birden kullanılıyorsa ikisinin de tanımı dipnotta verilir. Tek metrik kullanılıyorsa hangisi olduğu başlıkta net yazılır.

### S12.5. Cannibalization ve kanal kayması
Organik düşüşü tek başına yorumlanmaz; toplam trafik ve diğer kanalların hareketi ile birlikte verilir. Paid yoğunlaşması organik tıklamanın bir kısmını kaydırabilir; bu "yatırım artışı" olarak ifade edilir, "talep artışı" olarak değil.

### S12.6. Google update dönemleri
Dönem içinde core/spam update varsa, sıralama dalgalanması slaytında belirtilir: "Mart ayı içerisinde Spam Update ve Core Update olmak üzere iki algoritma güncellemesi yayına alınmıştır. Roll out esnasında ve sonraki 3 haftalık süreçte sıralamalarda dalgalanma görülebilmektedir."

### S12.7. Kaynak destelerde tespit edilen gerçek hatalar (tekrarlanmamalı)
- Ajanda-bölüm uyumsuzluğu (ajandada 3, destede 4 bölüm; "03" numarası iki kez).
- `SECTION TITLE` placeholder'ı silinmemiş.
- Aynı slaytta "MoM kıyaslandığında %10.4 düşüş" yazarken tabloda +%10.4 artış olması (yön ters yazımı).
- Yüzde format karışıklığı: `+%197` ile `+248.1%` aynı destede.
- Ondalık ayırıcı karışıklığı: metinde nokta, tabloda virgül.
- Typo yoğunluğu ("sodlaki", "kıyasalamada", "eleneceğin", "ARTIŞA GEÇEM").
- Konuşmacı notunda iç değerlendirme kalması.

---

## S13. Çıktı Dosya Yapısı

```
<marka>-seo-sunum-<donem>/
├── <Marka> SEO Değerlendirme <Dönem>.pptx     # ana çıktı
├── veri/
│   ├── gsc_date_15m.csv
│   ├── gsc_query_<p0>_<p1>.csv
│   ├── gsc_query_yoy.csv
│   ├── gsc_page_<p0>_<p1>.csv
│   ├── gsc_query_page.csv
│   ├── gsc_regex_vs_unfiltered.csv            # alt-property varsa
│   ├── ga4_channels.csv
│   ├── ga4_organic_monthly.csv
│   ├── ga4_revenue_transaction.csv
│   ├── ga4_ai_referral.csv
│   ├── ga4_items.csv                          # e-ticaret
│   ├── kwp_brand.csv / kwp_brand_category.csv / kwp_nonbrand.csv / kwp_competitors.csv
│   ├── seomonitor_visibility.csv / soc.csv / ai_sov.csv / keywords.csv
│   └── ahrefs_rank_distribution.csv
├── tablolar/                                   # T1-T14 işlenmiş hali
└── notlar/
    ├── eksik-veri.md                           # chat'te bildirilecek maddeler
    └── ic-kisitlar.md                          # rapora yazılmayan, sözlü iletilecek
```

---

## S14. Genişletme Noktaları (bu dosyada bilinçli boş)

Aşağıdaki başlıklar başka bir md'den gelmelidir. Birleştirmede bu bölümler yerine geçecek içerik konur.

| # | Başlık | Beklenen içerik |
|---|---|---|
| X1 | PPTX şablon ve layout eşlemesi | Şablon dosya yolu, slayt layout ID'leri, hangi C## hangi layout'a düşer |
| X2 | Renk ve tipografi token'ları | Inbound Design System slayt token'ları, insight vurgu renkleri |
| X3 | Grafik üretim kodu | pptxgenjs / python-pptx ile native chart üretimi, chart tipi seçim kuralları |
| X4 | SEOmonitor & Ahrefs API çağrı detayı | Endpoint, parametre, rate limit |
| X5 | GA4 API bağlantısı | Property ID yönetimi, rapor tanımları |
| X6 | Marka arşivi | Her marka için geçmiş dönem verileri ve önceki deste referansları |
| X7 | Blog / içerik bölümü derinleştirmesi | İçerik performansı metodolojisi, yeni-eski URL ayrımı |
| X8 | Teknik SEO bölümü | CWV dışında teknik denetim slaytları |

---

## S15. Kaynak Deste Envanteri

Bu notun çıkarıldığı gerçek desteler ve her birinin öğrettiği yapı:

| # | Deste | Mod | Öğrettiği |
|---|---|---|---|
| 1 | VitrA SEO Değerlendirme Haziran 2025 (22 slayt) | M1, çift property | Çift domain iskeleti (online.vitra + vitra.com.tr), her property için aynı slayt setinin tekrarı; lead-gen (form success) + e-ticaret metriklerinin bir arada kullanımı |
| 2 | VitrA SEO Değerlendirme Şubat 2026 (22 slayt) | M1, tek property | Domain geçişi sonrası tek property'ye dönüş; kategori bazlı visibility; AI Search SoV'nin SoC ile aynı slayta girmesi; `*domain geçişi` dipnot pratiği |
| 3 | VitrA SEO Değerlendirme Mart 2026 & Q1 (47 slayt) | M1+M2 birleşik | Aylık destenin sonuna ayrı kapak + ayrı ajanda ile çeyreklik bölüm eklenmesi; ürün funnel ve funnel conversion slaytları; geçiş sonrası kanal karşılaştırması |
| 4 | Gameplus SEO Sunumu Mayıs 2026 (21 slayt) | M4 | Etki analizi iskeleti; simetrik 11+11 hafta; Top 10 artış/düşüş query tabloları; **click + arama hacmi birleşik tablo (C33)**; faz hedefi takibi |
| 5 | Turkcell 2026 Q1 SEO Değerlendirme (54 slayt) | M2, çok property | 4 property'lik blok yapısı; başta Executive Summary + genel trafik bölümü; **GSC impression aggregation metodoloji slaytları (C17/C17b)**; Neler Yaptık + Q+1 iş maddeleri her property için |
| 6 | Enerjisa Üretim Haziran 2026 (25 slayt) | M1, kurumsal | "Neler Yaptık" ile başlama; blog bölümü; sonda kırılımlı Executive Summary + Stratejik Çıkarımlar; çalışma etkisi kanıt slaytı |
| 7 | KIKO Milano Temmuz 2026 (32 slayt) | M1 + H1 | Kategori bazlı derin hacim analizi (4 yıllık seri); marka+kelime hacminin jenerik kelime hacmiyle ayrıştırılması; **H1 avg tabloları (M3'ün tek gerçek örneği)**; keyword rank MoM tabloları; AI Overview SoV kategori bazlı; Core Web Vitals |
