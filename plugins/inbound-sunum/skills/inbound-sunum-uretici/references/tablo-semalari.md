# Kanonik Tablo Şemaları (T1-T14)

> Faz 2'de okunur. Gerçek destelerden birebir çıkarılmış tablo yapıları.
> **T1, T2, T4, T6, T7 her destede zorunludur.** Diğerleri iş modeline ve moda göre
> açılır.
>
> Bu şemalar kolon sırasını ve isimlendirmeyi sabitler. Aynı tabloyu her markada aynı
> biçimde kurmak, dönemler arası ve markalar arası karşılaştırmayı mümkün kılıyor.

## Format kuralları - tüm tablolarda geçerli

| Kural | Doğru | Yanlış |
|---|---|---|
| Yüzde | `%18`, `+%6.9`, `-%37` | `34.8%`, `%-3,3`, `+248.1%` |
| Ondalık ayırıcı | nokta: `2.75` | virgül: `2,75` |
| Binlik ayırıcı (tablo) | nokta: `17.637` | boşluk, virgül |
| Büyük sayı (KPI) | `595.4K`, `1.2M` | `595400` |
| CTR | 2 ondalık: `%2.97` | `%3` |
| Pozisyon | 1 ondalık: `8.5` | `8` |
| Pozisyon değişimi | `11.6 → 8.5 (+3.1 iyileşme ↑)` | `-3.1` |
| CTR puan değişimi | `%2.23 → %2.97 (+0.73p)` | `+%33` |
| Para | `₺1.49M`, `₺152K` | `1490000 TL` |
| Çarpan | `3.6x`, `~3x` | `3,6 kat` |
| Bant | `150-250K`, `%73-74` | tek sayı tahmin |
| 0'dan yükselen | **"yeni"** | `+%100` |
| Bin üzeri yüzde | `+%1362 (+395 click)` | `+%1362` |
| Veri yok | `-` | boş bırakma, `0`, `n/a` |

Tablo başlıkları ve metrik adları İngilizce kalır; yorum kolonu Türkçe olabilir.
Tek tabloda TR/EN karışımı yapılmaz.

---

## T1 - GSC aylık genel seri (zorunlu)

Trend grafiği ve 15 aylık tabloların kaynağı.

| Alan | Tip | Not |
|---|---|---|
| `month` | YYYY-MM | 15-16 ay |
| `clicks` | int | |
| `impressions` | int | |
| `ctr` | % 2 ondalık | |
| `position` | float 1 ondalık | |

Kapsam: aylık modda son 15 ay · çeyreklikte son 8 çeyrek + son 15 ay · yarıyılda
son 3 yarıyıl + son 18 ay.

**Dönem toplamı satırı:** CTR = toplam click ÷ toplam impression (ortalamaların
ortalaması **değil**). Avg. Position **impression ağırlıklı** hesaplanır.

---

## T2 - GSC brand / non-brand kırılımı (zorunlu, deste omurgası)

```
                    | Impressions <Δ>      | Clicks <Δ>          | CTR <Δ>
                    | P0    | P1    | %Chg | P0   | P1   | %Chg | P0   | P1   | Δp
Total               |
Branded Queries     |
Non-Branded Queries |
```

| Mod | `<Δ>` | P0 | P1 |
|---|---|---|---|
| M1 | YoY | geçen yıl aynı ay | dönem ayı |
| M1 (ek tablo) | MoM | önceki ay | dönem ayı |
| M2 | QoQ + YoY (iki tablo alt alta) | önceki çeyrek / geçen yıl aynı çeyrek | dönem çeyreği |
| M3 | H-YoY | geçen yıl aynı yarıyıl ortalaması | dönem yarıyıl ortalaması |

**Kurallar:**
- Satır sırası sabit: Total → Branded → Non-Branded.
- Total satırı **ham toplamdır**; brand ve non-brand ayrımına girmeyen artık ayrıca
  gösterilmez ama Total ≥ Branded + Non-Branded olmalı.
- CTR değişimi puan farkı olarak verilebilir; hangisi olduğu net olmalı.
- Aynı destede birden fazla property için tekrarlanıyorsa kolon yapısı aynı kalır.

---

## T3 - GSC query bazlı Top artış / Top düşüş

| Alan | Tip |
|---|---|
| `query` | text |
| `clicks_p0` | int |
| `clicks_p1` | int |
| `delta_clicks` | int, işaretli |
| `delta_pct` | %, işaretli; p0=0 ise **"yeni"** |

- Her yönde 10 satır. Sıralama `delta_clicks` mutlak değerine göre.
- Tablo üstünde toplam: `Toplam click: <p0> → <p1> (Δ <n> | <%>)`.
- **Kapsam şerhi zorunlu:** kaç query üzerinden çalışıldı, long-tail dahil mi.

---

## T4 - GSC page bazlı performans (zorunlu)

| Alan | Tip | Not |
|---|---|---|
| `url` | text | tam URL veya path |
| `clicks` | int | |
| `impressions` | int | |
| `position` | float | |
| `category` | text | path→kategori eşlemesinden |
| `clicks_p0` / `delta` | int | karşılaştırma isteniyorsa |

İki gösterim: (a) Top N sayfa listesi, (b) kategori bazında toplulaştırılmış tablo
(`Kategori | Click | Imp | QoQ % | YoY %`).

---

## T5 - GSC sorgu + arama hacmi birleşik tablo (C33'ün şeması)

| Alan | Tip | Kaynak |
|---|---|---|
| `query` | text | GSC |
| `click_m1..m4` | int | GSC, ay ay |
| `delta_click_m1_m3` | % | hesaplanır |
| `delta_click_m1_m4` | % | hesaplanır |
| `volume_m1..m4` | int | Keyword Planner, ay ay |
| `delta_vol_m1_m3` | % | hesaplanır |
| `delta_vol_m1_m4` | % | hesaplanır |

Keyword Planner'da ayrı verisi olmayan yazım varyantları için hücre `-` bırakılır ve
dipnotta hangi ana terim altında sayıldığı yazılır.

Bu tablo **talep-performans ayrıştırmasının** veri temelidir. Trafik kaybının
pazardan mı performanstan mı geldiğini gösterir.

---

## T6 - GA4 kanal bazlı trafik (zorunlu)

| Alan | Tip | Not |
|---|---|---|
| `channel` | text | GA4 default channel group, **çevrilmez** |
| `sessions_p0`, `sessions_p1`, `sessions_delta_pct` | | |
| `sessions_delta_abs` | int | **zorunlu** - yüzde tek başına yanıltıcı |
| `users_p0`, `users_p1`, `users_delta_pct` | | opsiyonel |
| `revenue_p0`, `revenue_p1`, `revenue_delta_pct` | | e-ticaret |
| `purchases_p0`, `purchases_p1`, `purchases_delta_pct` | | e-ticaret |

İki blok halinde gösterilir: YoY bloğu ve QoQ/MoM bloğu.

**Düşük bazlı kanallarda** (5 → 20.000 gibi) yüzde anlamsızlaşır; mutlak değer veya
`Nx` çarpan kullanılır ve dipnot düşülür.

---

## T7 - GA4 organik session özeti (zorunlu)

İki mini tablo, aynı slaytta:

```
Organic Sessions <YoY>
         | <P0>   | <P1>   | % Change
Sessions | 47.9K  | 174.7K | +%264.7

Organic Sessions <MoM/QoQ>
         | <P0>   | <P1>   | % Change
Sessions | 158.3K | 174.7K | +%10.4
```

Yanına toplam trafik ve organik pay cümlesi: "Toplam ziyaretin (333K) %52.4'ünü
(174.7K) organik kanal oluşturmaktadır."

---

## T8 - GA4 revenue & transaction (e-ticaret)

Dört mini tablo, ikişerli:

```
Revenue <YoY>                        Transaction <YoY>
                  | P0 | P1 | %Chg                      | P0 | P1 | %Chg
Total Revenue     |                  Total Transaction  |
Organic Revenue   |                  Organic Transaction|
Organic/Total %   |                  Organic/Total %    |

Revenue <QoQ/MoM>                    Transaction <QoQ/MoM>
(aynı yapı)
```

`Organic/Total %` satırındaki değişim **puan farkıdır**, yüzde değişimi değildir;
metinde "puan" yazılır.

**Önce kontrol:** bazı property'lerde revenue GA'da track edilmiyor ve tüm kanallar
₺0 geliyor. O durumda revenue analizi **çıkarılır**, session odaklı gidilir, dipnotla
belirtilir.

Türetilmiş metrikler: `AOV = Revenue ÷ Transaction`, `CR = Transaction ÷ Session`.

---

## T9 - GA4 AI referral

| Alan | Tip |
|---|---|
| `metric` | Sessions / Users |
| `p0`, `p1` | int |
| `delta_mom_or_qoq` | % |
| `delta_yoy` | % |

Kaynak filtresi listesi dipnotta verilir ve dönemler arası sabit tutulur. Düşük
tabandan gelen yüksek yüzdelerde mutlak değer de yazılır.

---

## T10 - GA4 ürün funnel (e-ticaret)

| Alan | Tip |
|---|---|
| `item_name` | text |
| `views` | int |
| `add_to_cart` | int |
| `purchases` | int |
| `revenue` | ₺ |
| `view_to_purchase_pct` | % 2 ondalık |
| `cart_to_purchase_pct` | % 2 ondalık |

Türetilmiş üç liste: PDP optimizasyon adayları (`view_to_purchase < %0.3`, yüksek
view), cart abandonment (`cart_to_purchase < %2`), en verimli ürünler (yüksek
conversion + `purchases >= 5`). **Eşikler slaytta yazılır.**

---

## T11 - GA4 lead / event (lead-gen)

| Alan | Tip |
|---|---|
| `channel` | text |
| `sessions` | int |
| `lead_events` | int |
| `lead_share_pct` | % (kanalın toplam lead içindeki payı) |
| `avg_session_duration` | mm:ss |

---

## T12 - Arama hacmi serisi (Keyword Planner)

| Alan | Tip |
|---|---|
| `set` | brand_only / brand_category / non_brand / competitor |
| `entity` | marka adı veya kategori |
| `year` | int |
| `m01..m12` | int (bucket'lı, olduğu gibi) |
| `delta_yoy`, `delta_mom`, `delta_qoq` | % |

Hacimler bucket'lı gelir; yeniden hesaplanmaz, olduğu gibi kullanılır.

---

## T13 - Visibility & SoC (SEOmonitor)

| Alan | Tip |
|---|---|
| `domain` | text |
| `visibility_mobile`, `delta_mobile` | % |
| `visibility_desktop`, `delta_desktop` | % |
| `soc_p0`, `soc_p1`, `soc_delta` | % |
| `monthly_volume` | int |
| `ai_sov` | % |
| `ai_overview_sov` | % |

Domain sırası config'teki rakip sırasıyla sabit; kendi domain `highlight_rows` ile
işaretlenir. `ai_sov` ve `ai_overview_sov` **farklı metriklerdir**; ikisi birden
kullanılıyorsa ikisinin de tanımı dipnotta verilir.

---

## T14 - Kategori bazlı visibility

| Alan | Tip |
|---|---|
| `category` | config'teki kategori seti |
| `visibility_p0`, `visibility_p1`, `delta` | % |

---

## AI görünürlük metrik sözlüğü

Bu tanımlar slayt altına aynen yazılır (tanım kutusu). **Araç adıyla anılan her
metrik, aracın kendi formülüyle hesaplanır** - kendi formülünü kurup araç adını
vermek gerçek bir projede 10 kat sapmaya yol açtı.

| Metrik | Formül | Not |
|---|---|---|
| **Mention** | markanın anıldığı yanıt sayısı | Ham sayı |
| **Visibility** | Mention ÷ toplam yanıt | Rakipleri hesaba katmaz |
| **Share of Voice** | marka anılma ÷ (marka + tüm rakip anılmaları) | Rekabet yoğunluğu |
| **Citation** | yanıtta kaynak gösterilen bağlantı sayısı | Mention ≠ Citation |
| **Citation Payı** | domain atıf ÷ toplam atıf | Atıf bazlı |
| **Source Visibility** | kaynak gösterildiği yanıt ÷ toplam yanıt | **YANIT BAZLI** |
| **Citation Visibility** | aynı hesabın her domain için hali | Rakip kıyası |
| **Avg. Position** | marka anıldığında ortalama sırası | AI Overview'da hesaplanamaz |
| **Prompt Coverage** | markanın anıldığı soru ÷ takip edilen soru | Konu yayılımı |
| **AIO tetiklenme oranı** | AIO yanıtı üretilen koşu ÷ toplam koşu | |

**Mention ile Citation ayrımı sunumda mutlaka açıklanır.** Mention marka adının yanıt
metninde geçmesi; Citation yanıtın o siteye kaynak olarak bağlanması. Bir marka çok
anılıp hiç kaynak gösterilmeyebilir - GEO'nun en önemli bulgusu bu.

**Brand / non-brand ayrımı zorunludur.** Brand sorularda görünürlük doğal olarak
yüksek; oradaki asıl metrik sentiment. Non-brand sorular rekabetin asıl alanı; rakip
kıyası ve kategori kırılımı orada yapılır. İkisi birleştirilerek "genel visibility"
verilmez - ayrı soru evrenleridir. Tablolarda "Toplam" yerine **"Tüm Platformlar"**
yazılır (aynı evren içinde platform toplamı).

---

## GSC metrik tanımları

Slayt altı tanım kutusuna aynen yazılır:

| Metrik | Tanım |
|---|---|
| Impression | Markaya ait reklam dışı bir linkin görüntülenmesi |
| Click | Markaya ait linke reklam harici gelen tıklama |
| CTR | Click ÷ Impression |
| Avg. Position | Ağırlıklı ortalama sıra (impression ağırlıklı) |
