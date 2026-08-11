# Veri Brief ve Export Talimatları

> Faz 0 ve Faz 1'de okunur. Amaç: üretime girmeden önce neyin elde olduğunu,
> neyin istenmesi gerektiğini ve istenenin **tam olarak nasıl alınacağını** netleştirmek.
> Belirsiz istek ("GA4 verisi lazım") yanlış export'a, yanlış export yanlış dönem
> etiketine, yanlış dönem etiketi de teslimden sonra yakalanan hataya dönüşüyor.

## İçindekiler

1. [Brief soru seti](#1-brief-soru-seti)
2. [Kaynak bazlı export talimatları](#2-kaynak-bazlı-export-talimatları)
3. [Dönem matrisi: hangi modda hangi aralıklar](#3-dönem-matrisi)
4. [Canlı çekilebilenler](#4-canlı-çekilebilenler)
5. [Eksik veri karar ağacı](#5-eksik-veri-karar-ağacı)
6. [Brief özeti şablonu](#6-brief-özeti-şablonu)

---

## 1. Brief soru seti

Dört blok, tek turda gruplu sorulur. Cevabı zaten bilinen soru tekrar sorulmaz.

### Blok A - Sunum kimliği

1. Sunum hangi dönem için: ay, çeyrek, yarıyıl, yoksa belirli bir değişimin etkisi mi?
2. Marka ve hangi property'ler? Tek domain mi, alt property'ler de var mı?
3. İş modeli: e-ticaret (revenue + transaction), lead-gen (form success),
   abonelik-servis (üyelik, paket sayfaları)?
4. Organik trafik **web-only mu, web+app mi** raporlanacak? (Deste genelinde tek
   kapsam; karar burada verilir.)
5. Sunum kime yapılacak: marka SEO ekibi, pazarlama yönetimi, üst yönetim? Yönetici
   özetinin biçimi buna göre seçilir.

### Blok B - Veri kaynakları

"Aşağıdakilerden hangileri dahil olsun?" diye sor ve her birinin hangi bölümü
açtığını yaz. Kullanıcı neyi kapattığını bilerek kapatsın.

| # | Kaynak | Açtığı bölümler | Kapatılırsa |
|---|---|---|---|
| 1 | Google Search Console | Click/impression/CTR/pozisyon, brand-non-brand kırılımı, sayfa ve query hareketleri | Destenin omurgası gider; sunum yapılamaz |
| 2 | GA4 | Organik session, kanal dağılımı, revenue/transaction, ürün funnel, AI referral | Trafik ve ticari sonuç katmanı çıkar |
| 3 | Keyword Planner | Marka, marka+kategori, non-brand ve rakip arama hacmi | **Talep-performans ayrıştırması yapılamaz**, düşüş yorumları bağlamsız kalır |
| 4 | SEOmonitor | Visibility (mobil/desktop), Share of Clicks, AI Overview SoV, kategori bazlı visibility, kelime bazlı sıra | Rakip karşılaştırma ve görünürlük bölümü çıkar |
| 5 | Ahrefs | İlk 3/10/100 sıralama dağılımı trendi, backlink, DR | Sıralama trendi slaytı çıkar |
| 6 | AI visibility izleme | Mention, citation, prompt coverage, sentiment, AI Overview tetiklenme | GEO bölümü çıkar |
| 7 | CrUX | LCP, INP, CLS | Core Web Vitals slaytı çıkar |
| 8 | DataForSEO | Yedek SERP ve hacim doğrulama | Doğrulama katmanı zayıflar |

### Blok C - Opsiyonel bölümler

Bunlar veri değil, kullanıcının elindeki bilgi. Sorulmazsa deste eksik çıkar.

1. **"Neler Yaptık / Devam Eden Çalışmalar"** eklenecek mi?
   Eklenecekse: dönemde iletilen işler + devam eden işler listesi.
   **Proje planı dokümanı varsa istenir** - iş kalemleri oradan çıkarılır, ayrıca
   yazdırmaya gerek kalmaz.
2. **"Sonraki Dönem Planı"** eklenecek mi? Eklenecekse plan maddeleri.
   Tarih/gün/hafta yazılmaz; `Öncelik 1/2/3` veya `Faz 1/2/3` kullanılır.
3. **Yönetici Özeti** eklenecek mi, hangi biçimde?
   - *Başta tez slaytı*: 5 madde, her biri tek cümlelik iddia. Üst yönetim için.
   - *Sonda kırılımlı özet*: en çok click alan 5 query, artan ilk 5, kaybeden ilk 5,
     ardından stratejik çıkarımlar bloğu. SEO ekibi için.
4. **Çalışma etkisi kanıt slaytı** var mı? Yapılan bir çalışmanın somut sonucu
   (yeni içeriğin AI Overview'da kaynak alınması, sıralama sıçraması) ekran
   görüntüsüyle konur. Görsel varsa istenir; bulgunun özü metinde de yazılır.
5. **Blog / içerik bölümü** açılacak mı? Açılacaksa GA4 landing page export'u ve
   blog URL deseni istenir.
6. **Ürün funnel bölümü** (e-ticaret) açılacak mı?

### Blok D - Bağlam ve sabitler

1. **Dönem içinde olay var mı?** Domain geçişi, SSR geçişi, site/tema değişikliği,
   kampanya dönemi, Google core/spam update. Her biri tarihiyle alınır ve ilgili
   tüm slaytlara yıldızlı dipnot üretir.
2. **Rakip seti:** hangi markalar, hangi sırayla. Marketplace'ler ve direkt
   rakipler ayrılıyor mu? Sıra tüm destede sabit kalır.
3. **Brand kelime seti:** marka yazım varyantları (yanlış yazımlar dahil), üçüncü
   parti markalar brand'e mi non-brand'e mi yazılacak.
4. **Takip edilen kelime sayısı:** SEOmonitor kampanyasının `keywords_count`
   alanından okunur, slayt metnine birebir girer ("599 hedef anahtar kelime takip
   edilmektedir"). Uydurulmaz.
5. **Kategori seti:** kategori kırılımlı tabloların satır seti ve URL→kategori
   eşleme kuralı.
6. **Önceki dönem destesi var mı?** Varsa metrik tanımları, brand kelime seti ve
   kategori eşlemesi oradan alınır. Ayrım tanımı dönemler arası değişmemeli;
   değiştiyse önceki dönem yeniden hesaplanır.
7. **Marka yazımı:** tek biçim seçilir (VitrA/Vitra, SEOmonitor/SEOMonitor gibi
   varyantlar aynı destede karışmaz).

---

## 2. Kaynak bazlı export talimatları

Aşağıdakiler kullanıcıya **birebir iletilebilecek** talimatlardır. Dönem
placeholder'larını Bölüm 3'teki matristen doldur.

### 2.1. GA4

**Genel kurallar - hepsinde geçerli:**
- **Compare kullanma, her dönemi ayrı indir.** Compare'li export tek dosyada iki
  dönemi üst üste yazıyor; hangi satırın hangi döneme ait olduğu kolon adlarından
  ayrılamıyor ve dönem başlıkları karışıyor.
- **CSV indir**, dosya başındaki `# Property`, `# Start date`, `# End date`
  satırlarını silme. Hangi dosyanın hangi property ve döneme ait olduğu oradan
  okunuyor; silinirse dosya elle etiketlenmek zorunda kalır.
- Dosya adına dönemi yaz: `ga4_kanal_2026-06.csv`.
- Alt property'ler varsa her biri için ayrı export.

**A1 - Traffic acquisition, kanal bazlı** (zorunlu)
> Reports > Acquisition > Traffic acquisition.
> Birincil boyut: **Session default channel group**.
> Metrikler: Sessions, Total users, Engagement rate, Key events,
> Total revenue (e-ticarette), Transactions (e-ticarette).
> Dönemler: `{DÖNEM}`, `{ÖNCEKİ}`, `{GEÇEN YIL}` - üç ayrı CSV.

**A2 - Organik aylık seri** (zorunlu)
> Aynı rapor, Session default channel group = **Organic Search** filtresi.
> Tarih aralığı: son **15 ay** (tek export, aylık kırılım).
> Trend grafikleri bu seriyi kullanıyor; tek ay export'u trend slaytını üretmez.

**A3 - Revenue & transaction** (e-ticaret)
> Reports > Monetization > Overview veya Ecommerce purchases.
> Total ve Organic ayrı: Revenue, Transactions, AOV, Conversion rate.
> Üç dönem ayrı.
> **Önce kontrol et:** bazı property'lerde revenue GA'da track edilmiyor ve tüm
> kanallar ₺0 geliyor. O durumda revenue analizi destedan çıkarılır, session
> odaklı gidilir ve bu dipnotla belirtilir.

**A4 - AI referral** (opsiyonel)
> Traffic acquisition, boyut: **Session source / medium**.
> Şu kaynaklar filtrelenir: `chatgpt.com`, `chat.openai.com`, `perplexity.ai`,
> `gemini.google.com`, `copilot.microsoft.com`, `claude.ai`, `bing.com/chat`,
> `you.com`.
> Liste sabit tutulur ve dipnotta yazılır; dönemler arası kıyas aynı listeyle yapılır.

**A5 - Ürün funnel** (e-ticaret, opsiyonel)
> Reports > Monetization > Ecommerce purchases.
> Boyut: **Item name**. Metrikler: Items viewed, Items added to cart,
> Items purchased, Item revenue.

**A6 - Lead / form event** (lead-gen)
> Reports > Engagement > Events, `form_success` veya markanın lead event adı.
> Kanal kırılımı ile birlikte; ayrıca kanal bazlı ortalama session süresi.

**A7 - Landing page** (blog/içerik bölümü açıksa)
> Reports > Engagement > Landing page. Organic Search filtresi.
> Metrikler: Sessions, Average engagement time, Key events.
> Not: organik landing raporunda büyük bir `(not set)` kovası app oturumlarını
> gösterir; app ağırlıklı organiği işaret eder ve dipnotta belirtilir.

### 2.2. Google Search Console

MCP bağlıysa **canlı çekilir**, kullanıcıdan istenmez (bkz. Bölüm 4). Elle
export gerekiyorsa:

> Search Console > Performance > Search results.
> Tarih aralığını `{DÖNEM}` olarak ayarla, sonra:
> - **Queries** sekmesi > Export > Excel. Satır limitini yükselt (1000).
> - **Pages** sekmesi > Export > Excel.
> - **Dates** sekmesi > Export (15-16 aylık seri için tarih aralığını genişlet).
> Her dönem için ayrı dosya, dosya adına dönemi yaz.
> `{ÖNCEKİ}` ve `{GEÇEN YIL}` için aynı üç export tekrarlanır.

**16 ay sınırı - baştan kontrol edilir.** GSC verisi 16 ay saklıyor. Geçen yılın
aynı çeyreği pencere dışına taşmış olabilir. İki çıkış yolu:
- Ajansın/müşterinin **Excel arşivi** varsa o dönemin tek kaynağı odur, istenir.
- Arşiv yoksa karşılaştırma dönemi pencere içinde geçerli ve eşit uzunlukta bir
  döneme çevrilir (örneğin H1 2026 vs H2 2025) ve bu slaytta yazılır.

**Alt property varsa** (URL regex ile filtreleme) iki export zorunlu: regex'li ve
aynı query seti üzerinde filtresiz. Sebebi `tuzaklar-ve-qa.md`'de.

### 2.3. Keyword Planner

> Google Ads > Tools > Keyword Planner > Get search volume and forecasts.
> Kelime setini yükle, location: **Türkiye**, dil: Türkçe.
> Aylık arama hacmi kırılımını **son 24 ay** olarak indir (CSV/Excel).
> Dört ayrı set: `brand_only`, `brand_category`, `non_brand`, `competitor`.

Hacimler bucket'lı gelir (27.1K, 33.1K, 40.5K). Bu yüzden değişimler %0, %18, %22
gibi tekrar eden değerlerde kümelenir; normaldir, her rakip için ayrı sebep aranmaz.
Bucket'lar olduğu gibi kullanılır, yeniden hesaplanmaz.

**MCP alternatifi ve kaynak seçimi.** Keyword Planner MCP bağlı değilse DataForSEO
`kw_data_google_ads_search_volume` (`location_name: "Turkiye"`, `language_code: "tr"`)
aynı Google Ads verisini canlı verir - tek çağrıda birden çok kelime, son 12 ayın
`monthly_searches` kırılımıyla.

Ancak bucket'lama **aylık YoY karşılaştırmasını taşımaz**: tek terim için seri
yalnızca 74000 / 90500 / 110000 basamaklarında hareket eder, bu da gerçek olmayan
sıfır değişimler ve sıçramalar üretir. Bu nedenle:

- **Aylık trend tablosu / grafiği (C04, C04b):** Ahrefs
  `keywords-explorer-volume-history` (`keyword`, `country`, `date_from`, `date_to`)
  kullanılır - sürekli seri verir, YoY karşılaştırmasına uygundur.
- **Set bazlı toplam ve göreli büyüklük (C05-C08):** Keyword Planner / Google Ads
  verisi kullanılır.
- İki kaynak **aynı metrik için tek tabloda birleştirilmez**. Aynı terim iki blokta
  farklı değerle görünecekse çekirdek terim ikinci bloktan çıkarılır ve her blok
  kendi kaynak dipnotunu taşır.

### 2.4. SEOmonitor

**Canlı çekilebilir** (`mcp__*__seomonitor_*`). Kullanıcıdan export istenmez.

**İlk adım her zaman campaign kimliği:** `seomonitor_get_tracked_campaigns` ile
kampanya listesi çekilir ve markanın `campaign_id`'si bulunur. Aynı çağrı
`campaign_info` içinde kritik iki alanı da verir:

- `primary_device` - raporun hangi cihazı esas alacağı
- `max_tracked_position_desktop` / `max_tracked_position_mobile` - iki cihaz
  **farklı derinlikte** takip edilebiliyor (ör. mobil 100, desktop 20). Sığ takip
  edilen cihazda tavana oturan kelime "o sırada" değil **takip dışı** demektir;
  cihazın kötü performansı olarak okunmaz.

`keywords_count` slayt metnindeki "N hedef anahtar kelime takip edilmektedir"
ifadesine birebir girer.

**Çekim listesi:**

| # | Tool | Ne verir | Kullanıldığı slayt |
|---|---|---|---|
| S1 | `get_tracked_campaigns` | campaign_id, keywords_count, primary_device, takip derinliği, güncel visibility (desktop/mobile/blended + 7/30 gün trend) | Görünürlük KPI |
| S2 | `get_share_of_voice` (tarih başına) | Organic SoV + AI Overview SoV + AI Search SoV, domain bazında; AI tarafında `brand_mentions` / `brand_citations` / `website_citations` kırılımı | Rakip görünürlük, AI Overview rekabeti |
| S3 | `get_daily_share_of_clicks` | Günlük Share of Clicks, domain bazında | Share of Clicks |
| S4 | `get_daily_group_visibility` | Grup (kategori) bazında günlük visibility | Kategori bazında visibility |
| S5 | `get_keyword_groups` | Kategori/klasör ağacı - kategori slaytlarının satır seti | Kategori kırılımı |
| S6 | `get_daily_keyword_ranks` | Kelime bazlı günlük sıra (before→after) | Kelime hareketleri |

`get_share_of_voice`'ta `metrics_weighted_by_search_volume: 1` verilir; ağırlıksız
değer kelime sayısına göre hesaplanır ve hacim farkını görmezden gelir.

**Bu kaynakta yaşanmış iki tuzak:**

1. **Organic Share of Voice ile Share of Clicks aynı metriktir.** İki ayrı endpoint
   aynı değeri döndürüyor (Flormar 31 Tem 2026: SoV `0.076279` / traffic `34369.54`
   ve SoC `0.0763` / monthly_clicks `34370`). Destede **tek başlık altında** verilir;
   ikisini ayrı metrik gibi sunmak aynı veriyi iki kez göstermek olur.
2. **AI Search SoV günlük seri değil, snapshot olabilir.** Flormar'da 30 Haz ve
   31 Tem çağrıları birebir aynı değerleri döndürdü (impression_score 188033,
   508 mention, total 1164798). Dönemsel kıyas yapılmadan önce iki tarihin
   değerleri karşılaştırılır; aynıysa yalnızca mevcut durum olarak sunulur.
   AI Overview SoV bu sorunu göstermiyor, günlük değişiyor.

**Dönem bazlı çekim reçetesi (rakip karşılaştırma slaytı için):**

1. **Share of Click - dönem ortalaması.** `get_daily_share_of_clicks` ·
   `device` = kampanyanın `primary_device`'ı · her ay iki çağrı (1-15, 16-30;
   uç nokta 15 günlük pencere sınırı uygular). Üç dönem çekilir: cari ay,
   önceki ay, önceki yılın aynı ayı. Ortalama, domain başına yalnızca **değeri
   bulunan günler** üzerinden alınır - günlük yanıt o günün top 10'unu döndürdüğü
   için listeye girmeyen rakip sıfır değil ölçüm dışıdır; kapsam dipnota yazılır.
2. **Visibility - dönem sonu.** `get_daily_group_visibility` · dönem sonu tek gün
   (ay sonu) · kampanya için `group_id: 0`, her rakip için `domain: <rakip>`.
   Bu taban bilinçli seçilir: SEOmonitor panelinin gösterimiyle örtüşür.
   Dönem ortalaması isteniyorsa aynı uç nokta tam ay çekebilir (burada 15 gün
   sınırı yok), ancak rakip × dönem sayısıyla maliyet hızla büyür.
3. İki tablo **ayrı** verilir; Visibility ile Share of Click aynı tabloya
   konmaz (bkz. tuzaklar 2.7 ve slayt kataloğu C20b).

`get_campaign_widgets` bir çağrıda özet verir (visibility, avg rank, SERP feature
kırılımı, AIO/AIS mention yüzdesi, organic/AIO/AIS SoV) ama **`visibility` alanı
aralığın son günüdür, ortalama değildir** ve `share_of_voice` tek tarihlik
kesittir (`as_of.sov_date`). Özet kartlar için elverişli, dönem ortalaması için
değil (bkz. tuzaklar 2.8).

Panel ekran görüntüsü kullanılacaksa slayda yapıştırılmaz, **tabloya çevrilir**.

### 2.5. Ahrefs

MCP bağlıysa canlı. Değilse:
> Site Explorer > Organic keywords: ilk 3 / ilk 10 / ilk 100 sıralama dağılımı
> trendi (grafik veya export). Google update işaretleri varsa korunur.
> Rakip benchmark için aynı metrikler rakip domainler için de alınır.

### 2.6. AI visibility izleme

`mcp__inbound-db__*` üzerinden çekilir. Üç filtreye **baştan karar verilir ve tüm
sorgularda sabit uygulanır**, karar dipnota yazılır:
1. Tarih: tüm platformların düzgün koştuğu ilk tarihten itibaren.
2. Soru tipi: brand / non-brand ayrımı. İkisi birleştirilerek "genel visibility"
   verilmez - ayrı soru evrenleridir.
3. Klasör/segment hariç tutmaları (pazaryeri veya rakip-hedefli soru grupları).

Kapsam karışması gerçek bir destede dört ayrı hataya yol açtı.

### 2.7. CrUX

> cruxvis.withgoogle.com üzerinden LCP, INP, CLS dağılımları.
> Kaynak notu birebir yazılır: `Kaynak: CrUX Vis https://cruxvis.withgoogle.com/`

---

## 3. Dönem matrisi

`{DÖNEM}`, `{ÖNCEKİ}`, `{GEÇEN YIL}` placeholder'ları moda göre şöyle doldurulur:

| Mod | `{DÖNEM}` | `{ÖNCEKİ}` | `{GEÇEN YIL}` | Trend serisi |
|---|---|---|---|---|
| **M1 Aylık** | ilgili ayın 1'i - son günü | önceki ay | geçen yıl aynı ay | son 15 ay |
| **M2 Çeyreklik** | çeyrek başı - sonu | önceki çeyrek | geçen yıl aynı çeyrek | son 8 çeyrek + son 15 ay |
| **M3 Yarıyıl** | 6 ay | (opsiyonel önceki yarıyıl) | geçen yıl aynı yarıyıl | son 3 yarıyıl + son 18 ay |
| **M4 Etki analizi** | geçiş sonrası N hafta | simetrik geçiş öncesi N hafta | - | geçiş öncesi + sonrası |

**Dönem etiketi standardı** - alt başlıkta parantezle beyan edilir:
```
2026 Q1 (1 Oca - 31 Mar 2026) & 2025 Q1 (1 Oca - 31 Mar 2025) | YoY karşılaştırma
```

**M4'te geçiş haftası analiz dışı bırakılır ve bu yazılır:**
```
Before: 23 Kas 2025 - 7 Şub 2026 (11 hafta) | Geçiş haftası: 8-14 Şub 2026
(analiz dışı) | After: 15 Şub - 2 May 2026 (11 hafta)
```

**M3'te iki gösterim birlikte verilir:** aylık ortalama (`2026'H1 Avg.`) ve
gerekirse toplam. Hangisi olduğu kolon başlığında yazar.

**Araç-özel istisna:** bazı araçlar (SEOmonitor visibility gibi) "önceki döneme
göre" çalışır; H1 sunumunda bile kıyas önceki yarıyıla göredir. Bu dipnotta
açıkça yazılır.

---

## 4. Canlı çekilebilenler

Bunları kullanıcıdan isteme, kendin çek. Ama **canlı çekim olduğunu ve kapsamını**
kullanıcıya söyle.

| Kaynak | Araçlar | Sınır |
|---|---|---|
| GSC | `mcp__gsc__get_advanced_search_analytics`, `compare_search_periods`, `list_properties` | 16 ay retention. Query ve page kırılımı ayrı çekilir. **Page URL'leri 100 karakterde kesilir** - uzun ürün URL'leri için bkz. `tuzaklar-ve-qa.md` 2.6 |
| SEOmonitor | `seomonitor_get_tracked_campaigns` ile campaign_id, sonra `get_share_of_voice` · `get_daily_share_of_clicks` · `get_daily_group_visibility` · `get_keyword_groups` | Cihaz takip derinliği farklı olabilir; `primary_device` esas alınır |
| Ahrefs | `mcp__bc3c...__site-explorer-*`, `rank-tracker-*`, `gsc-*` | Abonelik limitleri |
| AI visibility | `mcp__inbound-db__*` (`visibility_stats`, `competitor_stats`, `top_citations`, `query`) | Hazır fonksiyonlar önce denenir, elle formül kurulmaz |
| DataForSEO | `mcp__dataforseo__*` | location_name **"Turkiye"** (Turkey değil) |

GSC brand/non-brand ayrımı: `filter_dimension: query`, `filter_operator: notContains`,
`filter_expression: <marka kökü>`. Türkçe karakter sorununu bypass etmek için kök
kullanılır (örneğin "Özdilek" için "zdilek"). Bu yöntem ajansın kendi split'iyle
~%3 içinde örtüşür; sapma varsa dipnotta belirtilir.

**Otomasyon araçlarının adı müşteri çıktısında görünmez.** Veri kaynağı araçları
(GSC, GA4, SEOmonitor, Ahrefs, Keyword Planner) kaynak notunda yazılabilir.
DataForSEO jenerikleştirilir. AI visibility izleme sistemi "Inbound AI Visibility
izleme sistemi" olarak anılır.

---

## 5. Eksik veri karar ağacı

```
Veri elde var mı?
├── VAR  -> veri_tara.py ile dönem ve property teyidi al
│           Dönem belirsizse veya mükerrer dosya varsa SOR, tahmin etme
├── CANLI ÇEKİLEBİLİR -> çek, kapsamı kullanıcıya bildir
└── YOK
    ├── Zorunlu mu? -> Export talimatını ver, BEKLE. Slayt üretimine geçme.
    └── Opsiyonel mi?
        ├── Kullanıcı sağlayacak -> bekle
        └── Sağlanamıyor -> İlgili bölümü destedan KOMPLE ÇIKAR
                            + chat'te ÖNEMLİ olarak bildir
                            + rapora hiçbir iz bırakma
```

**Rapora yazılmayacaklar** (bunlar chat'e gider):
- "Bu bölüm için ek veri toplanması planlanabilir"
- "Detaylı ölçüm bir sonraki aşamada derinleştirilebilir"
- "X bu turda erişime kapalıydı"
- "LCP iframe üzerinden ölçülemiyor"
- Placeholder metrik, boş bölüm, "sonraki aşamada eklenecek" vaadi

Örneklem üzerinden çalışıldıysa dürüst ve sade beyan yapılır: "Bu bölüm tüm veriler
değil, mevcut örnek üzerinden değerlendirilmiştir."

**Araçlar arası fark varsa** dramatik kıyas dili kullanılmaz ("X kat küçümsüyor",
"aracın verisi güvenilmez"). Sayılar yorumsuz yan yana verilir veya tek kaynak
seçilip diğeri çıkarılır. İki analitik kaynağı bir arada kullanılıyorsa aylık oran
tablosu kurulur: oran dar bantta ise yüzdesel kıyas anlamlı, geniş bantta ise
yalnızca yön göstergesi olarak okunur ve bu yazılır.

---

## 6. Brief özeti şablonu

Brief tamamlandığında kullanıcıya tek blokta özetle ve teyit al:

```
SUNUM
  Marka / property : ...
  Mod ve dönem     : M1 Aylık · Haziran 2026 (1 - 30 Haz 2026)
  Karşılaştırma    : MoM (Mayıs 2026) + YoY (Haziran 2025)
  İş modeli        : e-ticaret
  Kapsam           : web + app (tüm destede tek kapsam)
  Hedef okuyucu    : marka SEO ekibi

AÇIK BÖLÜMLER
  Arama hacmi · GA4 organik · GSC brand/non-brand · Görünürlük & rakip ·
  Neler Yaptık · Sonraki Dönem Planı
KAPALI BÖLÜMLER
  Core Web Vitals (veri yok) · Ürün funnel (bu dönem istenmedi)

BEN ÇEKECEĞİM
  GSC: query, page, tarih serisi - 3 dönem (canlı, 16 ay penceresi içinde)
  AI visibility: brand + non-brand, 1 Haz - 30 Haz

SEN GÖNDERECEKSİN
  1. GA4 Traffic acquisition, Session default channel group
     -> 3 ayrı CSV: Haziran 2026 / Mayıs 2026 / Haziran 2025
     -> compare kullanma, # Property ve # Start date satırlarını silme
  2. GA4 organik aylık seri, son 15 ay, Organic Search filtresi -> 1 CSV
  3. Keyword Planner, 4 kelime seti, son 24 ay, location Türkiye -> 4 dosya
  4. SEOmonitor: visibility (mobil+desktop), SoC, AI Search SoV, kategori
     visibility + takip edilen kelime sayısı
  5. Neler Yaptık listesi veya proje planı dokümanı
  6. Sonraki dönem plan maddeleri

BAĞLAM
  Olaylar: 2026 Nisan kategori ağacı güncellemesi
  Rakip sırası: ...
  Brand seti: ...
  Takip edilen kelime: 2.300
```

Bu özet teyit edilmeden Faz 4'e geçilmez.
