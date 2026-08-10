# Loft SEO Sunum Otomasyon Mapping

> Bu doküman, Loft markası için aylık SEO değerlendirme sunumunun otomatik olarak oluşturulması sürecindeki slide mapping, veri kaynakları ve otomasyon akışını tanımlar.

---

## 1. Slide Mapping

### Slide 4 — Search Console Verileri - Total Impression
| Alan | Detay |
|------|-------|
| **Bölüm** | 01 - Genel Durum & Google Görünürlüğü |
| **Data Source** | Google Search Console (GSC) |
| **Dimension / Metric** | Total Impression (Monthly) — YoY değişim %, MoM değişim %, Yıllık ortalama vs ay bazlı karşılaştırma |
| **Data Processing** | 1. GSC API'den aylık impression verisi çekilir (2024 vs 2025) · 2. YoY % değişim hesaplanır (her ay için) · 3. MoM % değişim hesaplanır · 4. En yüksek/en düşük ay tespiti · 5. En yüksek büyüme oranı olan ay tespiti |
| **Chart / Output** | Bar Chart: 12 aylık YoY kıyaslamalı impression grafiği — X ekseni: Aylar (Jan-Dec), Y ekseni: Impression sayısı, 2 seri: 2024 (koyu) vs 2025 (açık), altında YoY % değişim satırı |
| **Header / Footnote** | Header: Loft \| Search Console Verileri · Footnote: Source: GSC |

**Insight Questions:**
1. Toplam impression geçen seneye göre nasıl değişmiş? (%X artış/azalış)
2. En yüksek impression hangi ayda?
3. En düşük impression hangi ayda?
4. En yüksek YoY büyüme oranı hangi ayda ve yüzde kaç?
5. Önceki aya göre değişim nasıl?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO performans analisti olarak {client} markasının GSC impression verilerini analiz et.

VERİ: Aşağıdaki tabloda {client} markasının 2024 ve 2025 yıllarına ait aylık impression verileri yer almaktadır:
{impression_data_table}

GÖREV:
1. 2025 yılında total impression'ın 2024'e göre yüzde kaç değiştiğini hesapla.
2. Sunum yapılan ay ({current_month}) için bir önceki yılın aynı ayına göre % değişimi belirt.
3. Bir önceki aya göre % değişimi hesapla.
4. En yüksek ve en düşük impression değerlerinin hangi aylarda olduğunu bul.
5. En yüksek YoY büyüme oranını ve ayını belirle.

ÇIKTI FORMATI:
"{current_year} yılında total impression, {previous_year}'e göre %X [artmış/azalmıştır]. Impression {previous_year} {prev_month} ayına göre %X [artmış/azalmış], geçtiğimiz aya göre ise %X [artmıştır/azalmıştır].

- {current_year} yılında, en yüksek Impression değeri [AY] ayında elde edilmiştir. En düşük değer ise [AY] ayında gerçekleşmiştir.
- {current_year} yılında {previous_year} yılına göre en yüksek büyüme oranı ise %X ile [AY] ayında gerçekleşmiştir."
```

---

### Slide 5 — Non-Brand Impression Azalışı Yaşanan Kelimeler
| Alan | Detay |
|------|-------|
| **Bölüm** | 01 - Genel Durum & Google Görünürlüğü |
| **Data Source** | Google Search Console (GSC) |
| **Dimension / Metric** | Non-Brand Keyword Impression — Kelime bazlı impression değişimi, YoY impression karşılaştırma, SERP sıralama pozisyonu |
| **Data Processing** | 1. GSC'den non-brand keyword impression verisi (YoY) · 2. Impression düşüşü yaşanan kelimeleri filtrele · 3. Düşüş yüzdelerini hesapla · 4. Mevcut SERP sıralamalarını çek · 5. Sezonsallık ve rekabet analizi notu ekle |
| **Chart / Output** | Tablo: Kelime \| 2024 Impression \| 2025 Impression \| YoY % Değişim \| Mevcut Sıra — Heatmap renklendirmeli (kırmızı = düşüş) + Kelime bazlı sıralama screenshot'ları |
| **Header / Footnote** | Header: Loft \| Search Console Verileri · Subtitle: Geçen Yıla Göre Non-Brand Impression Azalışı Yaşanan Kelimeler · Footnote: Source: GSC |

**Insight Questions:**
1. Hangi non-brand kelimelerde impression düşüşü yaşanmış?
2. En çok düşüş gösteren kelimeler hangileri?
3. Bu düşüşün sebebi sezonsallık mı yoksa rekabet mi?
4. Bu kelimelerdeki mevcut sıralama pozisyonumuz nedir?
5. Hangi rakipler bu kelimelerde yükselmiş?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO analisti olarak {client} markasının non-brand keyword impression performansını değerlendir.

VERİ: Aşağıda non-brand kelimelerin 2024 vs 2025 impression verileri bulunmaktadır:
{nb_impression_data}

GÖREV:
1. Impression düşüşü yaşanan kelimeleri listele (en çok düşüşten en aza).
2. Her kelime için YoY % değişimi hesapla.
3. Her kelime için mevcut SERP sıralama pozisyonunu belirt.
4. Sezonsallık etkisi olan kelimeleri tespit et.
5. Rekabet kaynaklı düşüş yaşanan kelimeleri ayır.

ÇIKTI FORMATI:
"[Kelime1] ve [Kelime2] gibi sorgularda hem sezonsallığın hem de rekabet tarafındaki ürün sayısının oldukça etkisi olmaktadır.
[Kelime1] kelimesinde [X]. ve [Kelime2] kelimesinde ise [Y]. sırada yer almaktayız."
```

---

### Slide 6-7 — Arama Hacmi Değişimi (Non-Brand Impression Düşüşü Yaşanan Kelimeler)
| Alan | Detay |
|------|-------|
| **Bölüm** | 01 - Genel Durum & Google Görünürlüğü |
| **Data Source** | Google Keyword Planner |
| **Dimension / Metric** | Aylık Arama Hacmi (Monthly Search Volume) — Kelime bazlı 12 aylık trend, YoY toplam arama hacmi değişimi %, Kategori bazlı aggregation |
| **Data Processing** | 1. Keyword Planner API'den ilgili kelimelerin aylık arama hacmi çekilir · 2. 2024 vs 2025 yıllık toplam/ortalama hesaplanır · 3. YoY % değişim hesaplanır (kelime bazlı + toplam) · 4. Bar chart için 12 aylık karşılaştırmalı veri seti oluşturulur · 5. Kelime grubu bazında özet % değişim hesaplanır |
| **Chart / Output** | Slide 6: Kelime bazlı mini bar chart'lar (her kelime için 12-ay YoY) — Salopet: %19 düşüş, Kadın Şort: %46 düşüş, Kadın Bluz: %46 düşüş · Slide 7: Toplam aggregated bar chart — Tüm düşüş gösteren kelimelerin ortalama değişimi: %19 azalma |
| **Header / Footnote** | Header: Loft \| Arama Hacmi Değişimi · Subtitle: Non-Brand Impression Düşüşü Yaşanan Kelimelerin Geçtiğimiz Seneye Göre Arama Hacmi Değişimi · Footnote: Source: Keyword Planner |

**Insight Questions:**
1. Non-brand impression düşüşü yaşanan kelimelerin arama hacimleri de düşmüş mü?
2. Düşüş sezonsallıktan mı yoksa genel pazar trendinden mi kaynaklanıyor?
3. Hangi kelimelerde en çok arama hacmi kaybı var?
4. Bu kelimelerin toplam arama hacmi değişimi yüzde kaç?
5. Arama hacmi düşmeyen ama impression düşen kelimeler var mı?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO analisti olarak {client} markasında impression düşüşü yaşanan kelimelerin arama hacmi değişimini analiz et.

VERİ: Aşağıda ilgili kelimelerin 2024 ve 2025 aylık arama hacimleri bulunmaktadır:
{keyword_volume_data}

GÖREV:
1. Her kelime için yıllık toplam arama hacmi değişimini % olarak hesapla.
2. Kelimeleri en çok düşüşten en aza sırala.
3. Tüm kelimelerin toplamındaki genel düşüş oranını hesapla.
4. Sezonsallık pattern'i olan kelimeleri belirt.

ÇIKTI FORMATI:
"[Kelime1] kelimesinin aranma hacmi geçen seneye göre %X düşmüştür."
(Her kelime için ayrı bir satır)

TOPLAM:
"Non-Brand Impression düşüşü yaşanan keywordler incelendiğinde aranma hacimlerinin geçtiğimiz seneye göre %X azalma yaşandığı görülmüştür."
```

---

### Slide 8 — Non-Brand Impression Artışı Yaşanan Kelimeler
| Alan | Detay |
|------|-------|
| **Bölüm** | 01 - Genel Durum & Google Görünürlüğü |
| **Data Source** | Google Search Console (GSC) |
| **Dimension / Metric** | Non-Brand Keyword Impression (Artış gösteren) — Kelime bazlı impression YoY artış, Sezonsallık korelasyonu |
| **Data Processing** | 1. GSC'den non-brand keyword impression verisi (YoY) · 2. Impression artışı yaşanan kelimeleri filtrele · 3. Artış yüzdelerini hesapla · 4. Sezon bazlı gruplama yap (kış/yaz ürünleri) |
| **Chart / Output** | Tablo: Kelime \| 2024 Impression \| 2025 Impression \| YoY % Artış — Heatmap renklendirmeli (yeşil = artış) + Sezonsallık notu |
| **Header / Footnote** | Header: Loft \| Search Console Verileri · Subtitle: Geçen Yıla Göre Non-Brand Impression Artışı Yaşanan Kelimeler · Footnote: Source: GSC |

**Insight Questions:**
1. Hangi non-brand kelimelerde impression artışı yaşanmış?
2. Bu artış sezonsallıkla mı ilişkili?
3. Yapılan SEO çalışmalarının etkisi var mı?
4. Hangi ürün kategorileri daha iyi performans göstermiş?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO analisti olarak {client} markasının impression artışı yaşanan non-brand kelimelerini analiz et.

VERİ: {nb_impression_increase_data}

GÖREV:
1. Impression artışı yaşanan kelimeleri listele.
2. Artışın sezonsallık mı yoksa organik büyüme mi olduğunu değerlendir.
3. Ürün kategorisi bazında gruplama yap.

ÇIKTI FORMATI:
"[Sezon] sezonuna ait ürünlerde geçen yıla göre impression oranlarında artışlar bulunmaktadır."
```

---

### Slide 9 — Search Console Verileri - Total Click
| Alan | Detay |
|------|-------|
| **Bölüm** | 01 - Genel Durum & Google Görünürlüğü |
| **Data Source** | Google Search Console (GSC) |
| **Dimension / Metric** | Total Click (Monthly) — YoY değişim %, MoM değişim %, En yüksek/düşük click ayları, En yüksek büyüme oranı ayı |
| **Data Processing** | 1. GSC API'den aylık click verisi çekilir (2024 vs 2025) · 2. YoY % değişim hesaplanır · 3. MoM % değişim hesaplanır · 4. En yüksek/en düşük ay ve büyüme oranı tespiti |
| **Chart / Output** | Bar Chart: 12 aylık YoY kıyaslamalı click grafiği — X ekseni: Aylar, Y ekseni: Click sayısı, 2 seri: 2024 vs 2025, YoY % değişim satırı |
| **Header / Footnote** | Header: Loft \| Search Console Verileri · Footnote: Source: GSC |

**Insight Questions:**
1. Toplam click geçen seneye göre nasıl değişmiş?
2. En yüksek click hangi ayda?
3. En düşük click hangi ayda?
4. En yüksek YoY büyüme oranı hangi ayda?
5. Click ile impression arasında orantısızlık var mı?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO performans analisti olarak {client} markasının GSC click verilerini analiz et.

VERİ: {click_data_table}

GÖREV:
1. 2025 yılında total click'in 2024'e göre % değişimini hesapla.
2. Sunum ayı için YoY ve MoM değişimi belirt.
3. En yüksek ve en düşük click aylarını bul.
4. En yüksek YoY büyüme oranını ve ayını belirle.

ÇIKTI FORMATI:
"{current_year} yılında total click, {previous_year}'e göre %X [artmış/azalmıştır]. Click {previous_year} {prev_month} ayına göre %X [artmış/azalmış], geçtiğimiz aya göre ise %X [artmıştır/azalmıştır].

- {current_year} yılında, en yüksek Click değeri [AY] ayında elde edilirken en düşük değer ise [AY] ayında gerçekleşmiştir.
- {current_year} yılında {previous_year} yılına göre en yüksek büyüme oranı ise %X ile [AY] ayında gerçekleşmiştir."
```

---

### Slide 10 — Non-Brand Click Düşüşü & Artışı Yaşanan Kelimeler
| Alan | Detay |
|------|-------|
| **Bölüm** | 01 - Genel Durum & Google Görünürlüğü |
| **Data Source** | Google Search Console (GSC) |
| **Dimension / Metric** | Non-Brand Keyword Click — Düşüş yaşayan kelimeler (sol), Artış yaşayan kelimeler (sağ), YoY % değişim |
| **Data Processing** | 1. GSC'den non-brand keyword click verisi (YoY) · 2. Düşüş ve artış olarak iki gruba ayır · 3. Her grup için YoY % değişim hesapla · 4. İki kolon halinde tablo oluştur |
| **Chart / Output** | İki kolonlu tablo: Sol — Click Düşüşü Yaşayan Kelimeler (kırmızı), Sağ — Click Artışı Yaşayan Kelimeler (yeşil). Her iki tabloda: Kelime \| 2024 Click \| 2025 Click \| YoY % |
| **Header / Footnote** | Header: Loft \| Search Console Verileri · Subtitle: Geçen Yıla Göre Non-Brand Click Düşüşü & Artışı Yaşanan Kelimeler · Footnote: Source: GSC |

**Insight Questions:**
1. Hangi non-brand kelimelerde click düşüşü var?
2. Hangi kelimelerde click artışı var?
3. Click düşüşü ile impression düşüşü paralellik gösteriyor mu?
4. CTR değişimi click düşüşünü açıklayabilir mi?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO analisti olarak {client} markasının non-brand click performansını değerlendir.

VERİ: {nb_click_data}

GÖREV:
1. Click düşüşü yaşayan kelimeleri listele (en çok düşüşten en aza).
2. Click artışı yaşayan kelimeleri listele (en çok artıştan en aza).
3. Impression verileriyle karşılaştırarak CTR değişimi hakkında yorum yap.

ÇIKTI FORMATI:
İki ayrı tablo oluştur:
"Click Düşüşü Yaşayan Kelimeler" ve "Click Artışı Yaşayan Kelimeler"
```

---

### Slide 11 — Marka Arama Hacimleri
| Alan | Detay |
|------|-------|
| **Bölüm** | 01 - Genel Durum & Google Görünürlüğü |
| **Data Source** | Google Keyword Planner |
| **Dimension / Metric** | Marka Arama Hacmi (Branded Search Volume) — {client} + rakip markalar aylık arama hacimleri, YoY % değişim (yıllık ortalama), MoM % değişim, Rakip karşılaştırma tablosu |
| **Data Processing** | 1. Keyword Planner'dan marka + rakip markaların aylık arama hacmi çekilir · 2. Her marka için 12-ay ortalaması hesaplanır · 3. YoY % değişim hesaplanır · 4. MoM değişim hesaplanır · 5. Rakiplerle karşılaştırmalı tablo oluşturulur · 6. Bar chart + tablo kombinasyonu hazırlanır |
| **Chart / Output** | Üst: Bar Chart (marka arama hacmi 12 ay YoY) · Alt: Tablo — Marka \| Tarih \| Avg \| Jan \| Feb \| ... \| Dec (tüm rakipler dahil) |
| **Header / Footnote** | Header: Loft \| Marka Arama Hacimleri · Footnote: Source: Keyword Planner |

**Insight Questions:**
1. {client} markasının arama hacmi geçen seneye göre nasıl değişmiş?
2. Geçtiğimiz aya göre nasıl değişmiş?
3. Rakip markalarda arama hacmi trendi nasıl?
4. Sektörde genel bir düşüş mü var yoksa marka spesifik mi?
5. En çok artış/azalış hangi aylarda?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO analisti olarak {client} markasının ve rakiplerinin marka arama hacimlerini karşılaştır.

VERİ: Aşağıda {client} ve rakip markaların 2024/2025 aylık arama hacimleri bulunmaktadır:
{brand_volume_data}

MARKALAR: {client}, {competitor_list}

GÖREV:
1. {client} markasının yıllık ortalama arama hacmi değişimini hesapla.
2. Geçtiğimiz aya göre değişimi hesapla.
3. Her rakip marka için YoY değişim hesapla.
4. Sektördeki genel trendi değerlendir.

ÇIKTI FORMATI:
"{current_year} yılında marka aranma hacmi, bir önceki yıla kıyasla %X [artış/azalış] göstermiştir. Geçtiğimiz aya göre ise %X [artmış/azalmıştır].
Bir önceki yıla kıyasla arama hacminde diğer markalarda ise [düşüş/artış] yaşanmıştır."
```

---

### Slide 12 — Organik Trafik Ölçümlemesi
| Alan | Detay |
|------|-------|
| **Bölüm** | 01 - Genel Durum & Google Görünürlüğü |
| **Data Source** | Google Analytics (GA4) |
| **Dimension / Metric** | Organik Trafik (Organic Sessions) — Aylık organic session, YoY % değişim, MoM % değişim, En yüksek/düşük trafik ayı, En yüksek büyüme oranı |
| **Data Processing** | 1. GA4'ten aylık organic traffic verisi çekilir · 2. YoY % değişim hesaplanır · 3. MoM değişim hesaplanır · 4. En yüksek/düşük ay tespiti · 5. En yüksek büyüme oranı tespiti |
| **Chart / Output** | Bar Chart: 12 aylık YoY kıyaslamalı organik trafik grafiği — X: Aylar, Y: Organic Sessions, 2 seri: 2024 vs 2025 |
| **Header / Footnote** | Header: Loft \| Organik Trafik Ölçümlemesi · Footnote: Source: Analytics |

**Insight Questions:**
1. Organik trafik geçen seneye göre nasıl değişmiş?
2. En yüksek organik trafik hangi ayda?
3. En düşük trafik hangi ayda?
4. En yüksek YoY büyüme oranı hangi ayda?
5. Trafik düşüşü yaşanan aylarda ne olmuş?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO analisti olarak {client} markasının organik trafik performansını analiz et.

VERİ: {organic_traffic_data}

GÖREV:
1. YoY toplam organik trafik değişimini hesapla.
2. Sunum ayı için MoM ve önceki yıl aynı aya göre değişim belirt.
3. En yüksek ve en düşük trafik aylarını bul.
4. En yüksek YoY büyüme oranını ve ayını belirle.

ÇIKTI FORMATI:
"{current_year} yılında organik trafik, {previous_year}'e göre %X [artmış/azalmıştır]. Organik Trafik {previous_year} {report_month} ayına göre %X [artmış/azalmış], geçtiğimiz aya göre ise %X [artmıştır/azalmıştır].

{current_year} yılında, en yüksek organik trafik değeri [AY] ayında elde edilirken, en düşük organik trafik değeri [AY] ayında kaydedilmiştir.
{current_year} yılında {previous_year} yılına göre en yüksek büyüme oranı ise %X ile [AY] ayında gerçekleşmiştir."
```

---

### Slide 13-14 — Organic Session - Landing Page Bazlı
| Alan | Detay |
|------|-------|
| **Bölüm** | 01 - Genel Durum & Google Görünürlüğü |
| **Data Source** | Google Analytics (GA4) |
| **Dimension / Metric** | Landing Page bazlı Organic Session — Slide 13: Yıllık (2025 full year), Slide 14: Aylık (Sunum ayı), Session sayısı, Total Users, YoY % değişim |
| **Data Processing** | 1. GA4'ten landing page bazlı organic session verisi çekilir · 2. Top landing page'ler sıralanır (session'a göre) · 3. YoY karşılaştırma yapılır · 4. Yıllık ve aylık iki ayrı view hazırlanır |
| **Chart / Output** | Tablo: Landing Page \| Session (2024) \| Session (2025) \| Total Users \| YoY % (Top 10-15 landing page) |
| **Header / Footnote** | Header: Loft \| Organic Session · Subtitle: [2025 Yılı / Aralık] Landing Page Özelinde Organic Session Durumu · Footnote: Source: Analytics |

**Insight Questions:**
1. En çok organik trafik alan landing page'ler hangileri?
2. Hangi landing page'lerde YoY artış var?
3. Hangi landing page'lerde düşüş var?
4. Kategori sayfaları mı yoksa ürün sayfaları mı daha iyi performans gösteriyor?
5. Yeni oluşturulan sayfalar trafik alıyor mu?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO analisti olarak {client} markasının landing page bazlı organik session performansını analiz et.

VERİ: {landing_page_data}
DÖNEM: {report_period} (Yıllık veya Aylık)

GÖREV:
1. Top landing page'leri session'a göre sırala.
2. Her sayfa için YoY % değişim hesapla.
3. En çok büyüyen ve en çok düşen sayfaları belirt.
4. Sayfa tipi bazında (kategori/ürün/blog) gruplama yap.

ÇIKTI: Sıralı tablo + en dikkat çekici değişimlerin kısa özeti
```

---

### Slide 15-16 — Markalar Visibility & Visibility Değişimi
| Alan | Detay |
|------|-------|
| **Bölüm** | 01 - Genel Durum & Google Görünürlüğü |
| **Data Source** | SEOMonitor |
| **Dimension / Metric** | SEO Visibility Score (%) — Desktop & Mobile ayrı ayrı, Rakip karşılaştırma (multi-brand), YoY visibility değişimi, MoM visibility değişimi, 12 aylık trend (Jan-Dec arası toplam değişim) |
| **Data Processing** | 1. SEOMonitor'dan visibility skorları çekilir (Desktop + Mobile) · 2. Rakip markalar için de aynı veriler alınır · 3. YoY, MoM ve 12-aylık kümülatif değişim hesaplanır · 4. Trend grafiği ve karşılaştırma tablosu hazırlanır · 5. Takip edilen kelime listesindeki arama trendi değişimi hesaplanır |
| **Chart / Output** | Slide 15: Multi-brand visibility karşılaştırma tablosu (Marka \| Desktop Visibility \| Mobile Visibility \| Değişim) + Arama trendi değişimi grafiği · Slide 16: 3'lü visibility değişim kartları — 1) Geçen yıl aynı ay vs bir önceki ay, 2) Bu yıl sunum ayı vs bir önceki ay, 3) 12 aylık kümülatif değişim — Her kart: Desktop % ve Mobile % |
| **Header / Footnote** | Header: Loft \| Markalar Visibility / Visibility Değişimi · Footnote: Source: SEOMonitor // SEO Visibility tanımı açıklaması |

**Insight Questions:**
1. Visibility skoru geçen seneye göre nasıl değişmiş?
2. Rakiplere kıyasla visibility durumumuz nasıl?
3. Desktop ve mobile arasında fark var mı?
4. Son 12 ayda toplam ne kadar visibility kazandık/kaybettik?
5. Hangi keyword gruplarında visibility artışı/azalışı var?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO analisti olarak {client} markasının ve rakiplerinin visibility skorlarını analiz et.

VERİ: {visibility_data}
RAKİPLER: {competitor_list}
DÖNEM: {report_month} {report_year}

GÖREV:
1. {client} markasının Desktop ve Mobile visibility değişimini 3 farklı perspektiften hesapla:
   a) Geçen yılın aynı ayı vs bir önceki ay
   b) Bu yılın sunum ayı vs bir önceki ay
   c) Yılın ilk ayı ile son ayı arasındaki kümülatif değişim
2. Rakiplerle karşılaştırmalı tablo oluştur.
3. Takip edilen kelime listesindeki arama trendi değişimini belirt.

ÇIKTI FORMATI:
"{report_year} {report_month} vs {previous_year} {report_month}
Desktop: X%, Mobile: Y% [artmıştır/azalmıştır]

Visibility oranı geçtiğimiz aya göre ise Desktop'ta X% Mobile'da ise Y% [artmıştır/azalmıştır].

{report_year} Ocak-{report_month} arasındaki 12 aylık visibility skorumuz Desktop'ta X% Mobile'da ise Y% [artmıştır/azalmıştır]."
```

---

### Slide 18-19 — Anahtar Kelime Sıralamaları
| Alan | Detay |
|------|-------|
| **Bölüm** | 02 - Keyword Rank |
| **Data Source** | SEOMonitor |
| **Dimension / Metric** | Keyword Rankings — Slide 18: 2025 Top Kelime Sıralamaları (yıllık), Slide 19: Sunum ayı kelime sıralamaları, Kelime \| Desktop Rank \| Mobile Rank \| Değişim, Rank dağılım grafiği (Top 3, 4-10, 11-20, 20+) |
| **Data Processing** | 1. SEOMonitor'dan keyword rank verileri çekilir · 2. Desktop ve Mobile ayrı sıralamalar alınır · 3. Rank değişimi hesaplanır (önceki döneme göre) · 4. Rank dağılım grupları oluşturulur · 5. Yıllık ve aylık iki ayrı view hazırlanır |
| **Chart / Output** | Slide 18: Yıllık Top Keywords tablosu + Rank dağılım pie/bar chart · Slide 19: Aylık keyword rank tablosu — Tablo: Keyword \| Desktop Rank \| Mobile Rank \| Prev Rank \| Değişim (↑↓) — Renk kodlu (yeşil=yükselme, kırmızı=düşme) |
| **Header / Footnote** | Header: Loft \| Anahtar Kelime Sıralamaları · Subtitle: [2025 Top / Aralık] Kelime Sıralamaları · Footnote: Source: SEOMonitor |

**Insight Questions:**
1. En iyi sıralama aldığımız kelimeler hangileri?
2. Hangi kelimelerde sıralama yükselmiş?
3. Hangi kelimelerde sıralama düşmüş?
4. Top 3'e giren kelime sayımız artmış mı?
5. Desktop ve mobile sıralamaları arasında tutarsızlık var mı?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO analisti olarak {client} markasının keyword rank performansını değerlendir.

VERİ: {keyword_rank_data}
DÖNEM: {report_period}

GÖREV:
1. Top kelimeler ve sıralamalarını listele (Desktop + Mobile).
2. Önceki döneme göre rank değişimlerini hesapla.
3. Rank dağılımını grupla (Top 3, 4-10, 11-20, 20+).
4. En çok yükselen ve en çok düşen kelimeleri belirt.

ÇIKTI: Sıralı tablo + rank dağılım özeti + öne çıkan değişimlerin kısa analizi
```

---

### Slide 21 — 2025'te Neler Yaptık?
| Alan | Detay |
|------|-------|
| **Bölüm** | 03 - Planlanan & Devam Eden İşler |
| **Data Source** | İç Proje Yönetim Dokümanları / Task Tracker |
| **Dimension / Metric** | Tamamlanan SEO aksiyonları listesi — Teknik SEO (URL yönlendirme, sitemap, duplicate), On-page SEO (heading tag, H1, meta title/desc), İçerik (kategori içerik optimizasyonu) |
| **Data Processing** | 1. Proje yönetim aracından tamamlanan task listesi çekilir · 2. Kategorilere ayrılır (Teknik / On-page / İçerik) · 3. Bullet-point formatında listelenir |
| **Chart / Output** | Bullet-point liste: Kategori URL Yönlendirme, Kategori URL/Navigasyon Optimizasyonu, Sitemap.xml Optimizasyonu, vb. |
| **Header / Footnote** | Header: Loft \| Next Step · Subtitle: 2025'te Neler Yaptık? |

**Insight Questions:**
1. Bu dönemde hangi SEO aksiyonları tamamlandı?
2. Teknik SEO, on-page ve içerik arasındaki dağılım nasıl?
3. Tamamlanan işlerin performansa etkisi ölçülmüş mü?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO proje yöneticisi olarak {client} markası için {report_year} yılında tamamlanan SEO aksiyonlarını özetle.

VERİ: {completed_tasks}

GÖREV:
1. Tamamlanan aksiyonları kategorilere ayır (Teknik SEO, On-page SEO, İçerik).
2. Her aksiyon için kısa açıklama ekle.
3. Bullet-point formatında listele.

ÇIKTI: Kategorize edilmiş aksiyon listesi
```

---

### Slide 22 — 2026'da Neler Planlıyoruz?
| Alan | Detay |
|------|-------|
| **Bölüm** | 03 - Planlanan & Devam Eden İşler |
| **Data Source** | SEO Roadmap / Strateji Dokümanı |
| **Dimension / Metric** | Planlanan SEO aksiyonları listesi — Teknik SEO (breadcrumb, sitemap, robots.txt, 404/301, site hızı), On-page SEO (schema markup, meta ruleset), İçerik (kategori içerikleri, FAQ), Backlink (toxic backlink, AI referans siteleri), AI Görünürlüğü (structured data, LLMs.txt, FAQ) |
| **Data Processing** | 1. Roadmap dokümanından planlanan aksiyonlar çekilir · 2. Kategorilere ayrılır · 3. Alt detaylar eklenir (özellikle AI görünürlüğü bölümü) |
| **Chart / Output** | Bullet-point liste + AI görünürlüğü alt maddeleri: Breadcrumb Optimizasyonu, Sitemap.xml Optimizasyonu & Kontrolleri, vb. + AI görünürlüğü arttıracak aksiyonlar: Structured Data optimizasyonları, AI referans içerikler, LLMs.txt, FAQ çalışmaları |
| **Header / Footnote** | Header: Loft \| Next Step · Subtitle: 2026'da Neler Planlıyoruz? |

**Insight Questions:**
1. Gelecek dönem hangi SEO aksiyonları planlanıyor?
2. AI görünürlüğü için neler yapılacak?
3. Teknik borç temizliği planları neler?
4. İçerik stratejisi nasıl geliştirilecek?

**Otomasyon Prompt Şablonu:**
```
SEN: SEO strateji danışmanı olarak {client} markası için {next_year} yılı SEO planını özetle.

VERİ: {planned_actions}

GÖREV:
1. Planlanan aksiyonları kategorilere ayır.
2. Her aksiyon için öncelik ve beklenen etki belirt.
3. AI görünürlüğü aksiyonlarını ayrı bir alt bölüm olarak detaylandır.

ÇIKTI: Kategorize edilmiş planlanan aksiyon listesi + AI görünürlüğü detayları
```

---

## 2. Data Sources

| Data Source | İlgili Slaytlar | API / Entegrasyon | Çekilecek Metrikler | Güncelleme Sıklığı |
|---|---|---|---|---|
| **Google Search Console (GSC)** | 4, 5, 8, 9, 10 | GSC API (Search Analytics) | Impression, Click, CTR, Position (Query, Page, Date boyutlarında) | Aylık |
| **Google Keyword Planner** | 6, 7, 11 | Keyword Planner API (WHC entegre - güncellenecek) | Monthly Search Volume (Kelime bazlı, 12 aylık trend) | Aylık |
| **Google Analytics (GA4)** | 12, 13, 14 | GA4 Data API | Organic Sessions, Users (Landing Page, Source/Medium boyutlarında) | Aylık |
| **SEOMonitor** | 15, 16, 18, 19 | SEOMonitor API | Visibility Score (Desktop/Mobile), Keyword Rank, Rank Distribution, Competitor Comparison | Aylık |
| **İç Proje Dokümanları** | 21, 22 | Manuel / Task Tracker API | Tamamlanan ve planlanan SEO aksiyonları listesi | Dönemsel (sunum öncesi) |

---

## 3. Otomasyon Akışı

| Adım | İşlem | Giriş (Input) | Çıkış (Output) | Araç / Teknoloji |
|---|---|---|---|---|
| **1** | Veri Çekme | API credentials, tarih aralığı, kelime listesi | Raw data (JSON/CSV) | Python + API clients (google-api-python-client, seomonitor-api) |
| **2** | Veri İşleme | Raw data | YoY/MoM hesaplamaları, kategorizasyon, sıralama | Python (pandas, numpy) |
| **3** | Insight Üretme | İşlenmiş veri tabloları + prompt şablonları | Doğal dilde insight cümleleri | Claude API (claude-sonnet-4-5) |
| **4** | Grafik Oluşturma | İşlenmiş veri | Bar chart, tablo, heatmap görselleri | Python (matplotlib, plotly) veya pptxgenjs |
| **5** | Sunum Oluşturma | Insight metinleri + grafikler + template | Final PPTX dosyası | python-pptx veya pptxgenjs + template |
| **6** | QA & Review | Final PPTX | Onaylanmış sunum | Claude (visual QA) + manuel kontrol |

---

## 4. Değişken Referansları (Prompt Variables)

Aşağıdaki değişkenler tüm prompt şablonlarında kullanılmaktadır:

| Değişken | Açıklama | Örnek Değer |
|---|---|---|
| `{client}` | Marka adı | Loft |
| `{current_year}` | Raporlanan yıl | 2025 |
| `{previous_year}` | Bir önceki yıl | 2024 |
| `{current_month}` | Sunum yapılan ay | Aralık |
| `{prev_month}` | Bir önceki ay | Kasım |
| `{report_month}` | Rapor ayı | Aralık |
| `{report_year}` | Rapor yılı | 2025 |
| `{report_period}` | Rapor dönemi | 2025 Yılı / Aralık |
| `{next_year}` | Gelecek yıl | 2026 |
| `{competitor_list}` | Rakip marka listesi | Colins, DeFacto, LC Waikiki, Koton |
| `{impression_data_table}` | GSC impression veri tablosu | (CSV/JSON formatında) |
| `{click_data_table}` | GSC click veri tablosu | (CSV/JSON formatında) |
| `{nb_impression_data}` | Non-brand impression verisi | (CSV/JSON formatında) |
| `{nb_impression_increase_data}` | NB impression artış verisi | (CSV/JSON formatında) |
| `{nb_click_data}` | Non-brand click verisi | (CSV/JSON formatında) |
| `{keyword_volume_data}` | Keyword Planner arama hacmi verisi | (CSV/JSON formatında) |
| `{brand_volume_data}` | Marka arama hacmi verisi | (CSV/JSON formatında) |
| `{organic_traffic_data}` | GA4 organik trafik verisi | (CSV/JSON formatında) |
| `{landing_page_data}` | Landing page bazlı session verisi | (CSV/JSON formatında) |
| `{visibility_data}` | SEOMonitor visibility verisi | (CSV/JSON formatında) |
| `{keyword_rank_data}` | SEOMonitor keyword rank verisi | (CSV/JSON formatında) |
| `{completed_tasks}` | Tamamlanan SEO aksiyonları | (Bullet-point liste) |
| `{planned_actions}` | Planlanan SEO aksiyonları | (Bullet-point liste) |
