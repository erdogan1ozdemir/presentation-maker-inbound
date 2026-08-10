# SEO/GEO Değerlendirme Sunumu Üretici - Süreç Notları

> **Bu doküman ne:** Özdilekteyim 2026 H1 sunumunun (43 slayt, ~30 iterasyon) üretim sürecinden çıkarılmış, **herhangi bir marka için tekrar kullanılabilir** çalışma kılavuzu.
> **Birleştirme notu:** Bu dosya çok parçalı bir skill'in bir modülüdür. Diğer chat'lerden gelen modüllerle birleştirilecek şekilde, kendi içinde kapalı yazılmıştır. Çakışabilecek bölümler: "Dil ve Stil" (İçerik Dili Rehberi ile), "Tasarım Token'ları" (Inbound Design System ile). Çakışma halinde **o skill'ler esas alınır**, buradaki özet yalnızca hatırlatmadır.
> **Bağımlılıklar:** `anthropic-skills:pptx` (paketleme/doğrulama), `anthropic-skills:icerik-dili-rehberi` (metin dili), Inbound Design System (renk/tipografi).

---

## 1. Sunum Tipleri ve Dönem Çerçevesi

Üç sunum tipi vardır. **İlk iş, hangi tip olduğunu ve karşılaştırma eksenini netleştirmektir.**

| Tip | Ana kıyas | İkincil kıyas | Tipik slayt sayısı |
|---|---|---|---|
| **Aylık** | Ay vs önceki ay (MoM) | Ay vs geçen yıl aynı ay (YoY) | 12-18 |
| **Çeyreklik** | Q vs Q-1 | Q vs geçen yıl aynı Q (YoY) | 25-35 |
| **Yarıyıl (H1/H2)** | H vs geçen yıl aynı H | Çeyrek içi kırılım (Q1 vs Q2) | 35-45 |

### 1.1. Dönem çerçeveleme kuralları (en sık hata kaynağı)

1. **Her slaytın dönemi başlıkta yazılır.** "2026 H1 vs 2025 H1", "2026 Q2 vs 2025 Q2", "Temmuz 2026 vs Haziran 2026".
2. **Bir destede birden fazla dönem tipi olabilir** (H1 destesinde Q2 detay slaytı gibi) - ama her slayt kendi dönemini açıkça beyan etmelidir.
3. **Tablodaki veri ile başlıktaki dönem birebir örtüşmelidir.** Bu, denetimde en çok yakalanan hatadır (bkz. Bölüm 9).
4. **Araç-özel istisnalar:** Bazı araçlar (ör. SEOmonitor visibility) "önceki döneme göre" çalışır; H1 sunumunda bile kıyas 2025 H2'ye göredir. Bu, dipnotta açıkça yazılır.
5. **Veri kısıtı varsa dönem daraltılır, uydurulmaz.** Örn. AI visibility ölçümü Temmuz'da başladıysa H1 kıyası yapılmaz; "mevcut durum" olarak sunulur ve dipnotta belirtilir.

---

## 2. Sunum Mimarisi

### 2.1. Standart bölüm akışı

```
01  Kapak (Marka | Dönem)
02  SUNUM AKIŞI (numaralı ajanda: 01, 02, 03...)
03  [Bölüm ayracı] Pazar & Rakip Analizi
      - Marka arama hacimleri (kendi markası + ana marka)
      - Rakip arama hacimleri
      - Takip edilen kelimelerdeki hacim
      - Marka + kategori arama hacimleri
04  [Bölüm ayracı] Google Search Console Metrikleri
      - Aylık Impression & Click
      - Aylık Pozisyon & CTR
      - Çeyreklik Impression & Click
      - [Dönem] vs [Dönem] Aylık karşılaştırma
      - Brand vs Non-Brand click değişimleri (çeyreklik + aylık)
      - Sayfa grubu performansları (/kategori1, /kategori2...)
      - Yeni açılan sayfa tipleri (varsa)
05  [Bölüm ayracı] GA4 - Organik Trafik
      - Kanal bazında Session/Transaction/Revenue
      - Total Session & Transaction & Revenue
      - Organic Search Session & Transaction & Revenue
      - [Varsa] İkinci analitik kaynağı (AEM/Adobe) aylık tablo + chart
      - [Varsa] Organik vs Total pay tablosu
      - [Varsa] İki kaynak karşılaştırması (oran tutarlılığı)
06  [Bölüm ayracı] AI Traffic
      - AI Referral trafik (GA4 referral)
      - AI Görünürlük bölümü (6 slayt - bkz. Bölüm 6)
07  [Bölüm ayracı] Sıralama & Görünürlük
      - Visibility genel (rakip kıyaslı)
      - Görünürlüğü artan kategoriler
      - Görünürlüğü azalan kategoriler
      - Sıralama artışı yaşayan top kelimeler
08  Landing Page & Query Değişimleri
      - En çok click alan sayfalar (artan/azalan)
      - En çok click artışı görülen sayfalar
      - Brand query'ler
      - Non-Brand query'ler
09  Teşekkürler
```

**Aylık sunumda** 03 ve 07 bölümleri kısaltılır veya çıkarılır; ağırlık 04-05'tedir.
**Çeyreklikte** hepsi bulunur, kırılımlar çeyrek bazlıdır.

### 2.2. Slayt tipleri ve iskeletleri

| Tip | Yapı | Kullanım |
|---|---|---|
| **Tablo + insight** | Sol tablo, sağ 3-4 ➔ madde, altta tanım kutusu + kaynak | En yaygın |
| **Chart + insight** | Sol/sağ chart (PNG), karşı tarafta ➔ maddeler | Trend gösterimi |
| **Çift tablo** | Üst/alt iki tablo (ör. Brand + Non-Brand) | Ayrı evrenler |
| **Tablo + chart** | Sol tablo, sağ chart | Aylık seri + özet |
| **Liste slaytı** | İki sütun (artan/azalan), altta 2 yorum | Landing/query hareketleri |
| **Bölüm ayracı** | Büyük numara + bölüm adı | Bölüm geçişleri |

---

## 3. Veri Kaynakları ve Çekme Yöntemleri

### 3.1. Google Search Console (mcp__gsc__*)

```
mcp__gsc__list_properties                    → property listesi (doğru property'yi bul)
mcp__gsc__get_advanced_search_analytics      → asıl iş atı
   site_url, start_date, end_date, dimensions (query|page|date|device), 
   filter_dimension/filter_operator/filter_expression, row_limit
mcp__gsc__compare_search_periods             → iki dönem kıyası (query|page)
```

**Kritik kısıt:** GSC verisi **16 ay** saklar. Geçen yılın aynı çeyreği API'den düşmüş olabilir → o dönemin kıyasları için **müşterinin/ajansın Excel arşivleri tek kaynaktır**. Bunu baştan kontrol et.

**Brand/Non-Brand ayrımı:** `filter_dimension: query`, `filter_operator: notContains`, `filter_expression: <marka kökü>` (ör. "zdilek" - Türkçe karakter sorununu bypass etmek için kök kullanılır). Bu yöntem ajansın kendi split'iyle ~%3 içinde örtüşür; sapma varsa dipnotta belirtilir.

### 3.2. GA4

Doğrudan MCP yoksa **kullanıcının export'u** (Excel/CSV/ekran görüntüsü) esas alınır. Dikkat:
- Deck'teki tablolar yuvarlanmış olabilir (1.2K, 3.3M) → çeyreklik/aylık kesin değerler için ham export iste.
- Kanal bazlı tablolarda "Organic Search" satırı ile "Organic Shopping/Social/Video" ayrıdır; hangisinin kastedildiğini netleştir.

### 3.3. İkinci analitik kaynağı (AEM / Adobe / başka)

Marka kendi analitiğini kullanıyorsa iki kaynak arasında **seviye farkı** olur. Yapılacak:
1. Aylık oran tablosu kur (Kaynak A / Kaynak B).
2. Oranın **istikrarlı olup olmadığına** bak.
   - Session oranı dar bantta (ör. 4.7x-5.2x) → yüzdesel değişim kıyasları anlamlı.
   - Transaction/Revenue oranı geniş bantta (5.0x-7.8x) → yalnızca yön göstergesi olarak okunur, mutlak kıyas yapılmaz.
3. Bu bulgu ayrı bir slayt olur ("X & Y - Veri Karşılaştırması") ve dipnotta metodoloji farkları (session tanımı, attribution, consent) belirtilir.

### 3.4. Arama hacmi (DataForSEO / Keyword Planner)

```
mcp__dfs-mcp__kw_data_google_ads_search_volume
   keywords: [...], location_name: "Turkiye"     ← "Turkey" değil
```
Marka hacimlerini doğrulamak için kullanılır. Slayttaki tabloyla birebir örtüşmeli.

### 3.5. AI Visibility (inbound-db)

**Önce hazır fonksiyonları dene, elle formül kurma:**

```sql
SELECT * FROM get_visibility_trends(project_id::uuid, days_back, 'day');
SELECT * FROM get_competitor_comparison(project_id::uuid, days_back);
SELECT * FROM get_visibility_trend(prompt_ids::uuid[], date_from, date_to, provider);
SELECT * FROM get_citations_aggregated(project_id::uuid, prompt_ids::uuid[], provider, date_from);
```

Yardımcı araçlar: `mcp__inbound-db__list_projects`, `visibility_stats`, `competitor_stats`, `top_citations`, `list_folders`, `query`.

**Tablolar:** `prompts` (is_branded, is_competitor_focused, folder_id, status), `prompt_runs`, `llm_responses` (brand_mentioned, brand_position, sentiment, competitor_mentions jsonb, metadata jsonb), `citation_sources` (domain, domain_type, prompt_run_id).

**`llm_responses.metadata` (AI Overview için kritik):**
- `aio_present` → AI Overview tetiklendi mi
- `brand_in_sources` → marka kaynaklarda var mı
- `references` → kaynak listesi

---

## 4. Metrik Sözlüğü ve Formüller

Bu tanımlar **slaytların altına aynen yazılır** (tanım kutusu), formülde markanın gerçek sayıları verilir.

### 4.1. GSC metrikleri
| Metrik | Tanım |
|---|---|
| Impression | Markaya ait reklam dışı bir linkin görüntülenmesi |
| Click | Markaya ait linke reklam harici gelen tıklama |
| CTR | Click ÷ Impression |
| Avg. Position | Ağırlıklı ortalama sıra (impression ağırlıklı hesaplanır) |

### 4.2. AI Görünürlük metrikleri (tool adlarıyla)
| Metrik | Formül | Not |
|---|---|---|
| **Mention** | markanın anıldığı yanıt sayısı | Ham sayı |
| **Visibility** | Mention ÷ toplam yanıt | Rakipleri hesaba katmaz |
| **Share of Voice** | marka anılma ÷ (marka + tüm rakip anılmaları) | Rekabet yoğunluğu |
| **Citation** | yanıtta kaynak gösterilen bağlantı sayısı | Mention ≠ Citation |
| **Citation Payı** | domain atıf ÷ toplam atıf | Atıf bazlı |
| **Source Visibility** | **kaynak gösterildiği yanıt ÷ toplam yanıt** | **YANIT BAZLI** (bkz. tuzak 10.6) |
| **Citation Visibility** | aynı hesabın her domain için hali | Rakip kıyası |
| **Avg. Position** | marka anıldığında ortalama sırası | AIO'da hesaplanamaz |
| **Prompt Coverage** | markanın anıldığı soru ÷ takip edilen soru | Konu yayılımı |
| **AIO tetiklenme oranı** | AIO yanıtı üretilen koşu ÷ toplam koşu | metadata.aio_present |

**Mention vs Citation farkı (sunumda mutlaka açıklanır):** Mention = marka adının yanıt metninde geçmesi. Citation = yanıtın o siteye kaynak olarak bağlanması. Bir marka çok anılıp hiç kaynak gösterilmeyebilir - bu, GEO'nun en önemli bulgusudur.

---

## 5. GSC & GA4 Aylık Metrik Tabloları (her markada olacak)

Bu iki tablo **her sunumda standarttır**. Aylık sunumda ana içerik, çeyreklik/H1'de temel katmandır.

### 5.1. GSC aylık tablo

| Ay | Click | Impression | CTR | Avg. Position |
|---|---|---|---|---|
| Oca 26 | 214.4K | 6.42M | %3.34 | 10.0 |
| ... | | | | |
| **Dönem Toplamı** | **1.14M** | **32.2M** | **%3.55** | **~9.5** |

- Dönem satırında CTR = toplam click ÷ toplam impression (ortalamaların ortalaması değil).
- Avg. Position dönem satırında **impression ağırlıklı** hesaplanır.
- Yanına aylık chart: bar = Impression, çizgi = Click (veya CTR/Position ikilisi).

### 5.2. GA4 aylık tablo

| Ay | Session | User | Transaction | Revenue | AOV | CR |
|---|---|---|---|---|---|---|
| Oca 26 | 1.9M | 689.4K | 54.9K | 108.8M | 1.982 | %2.89 |
| ... | | | | | | |
| **Dönem** | | | | | | |

- **Organic Search** için ayrı tablo (aynı kolonlar).
- AOV = Revenue ÷ Transaction · CR = Transaction ÷ Session.
- Kanal tablosunda değişim kolonları renklendirilir (pozitif yeşil `34A853`, negatif kırmızı `FF0000`).

### 5.3. Kanal bazında tablo (çeyreklik/H1)

`Kanal | [Dönem1] Session | [Dönem2] Session | Değişim % | [Dönem1] Tx | [Dönem2] Tx | Değişim % | [Dönem1] Revenue | [Dönem2] Revenue | Değişim %`

- Düşük bazlı kanallarda (ör. 5 → 20.000) yüzde anlamsızlaşır → mutlak değer veya "Nx" çarpan kullan, dipnot düş.

---

## 6. AI Görünürlük Bölümü (6 slayt şablonu)

Bu bölüm en çok iterasyon gerektiren kısımdır. Nihai yapı:

| # | Slayt | İçerik |
|---|---|---|
| 1 | **Genel Durum + Koşu Turları** | Brand tablosu + Non-Brand tablosu (Platform / Mention-Yanıt / Visibility / Source Visibility / Avg. Position) + koşu turlarına göre visibility chart'ı |
| 2 | **Non-Brand Rakip Karşılaştırması** | Marka / Visibility / Share of Voice / Citation Visibility |
| 3 | **Non-Brand Kategori Bazında** | Kategori / Visibility / Avg. Position / Yanıt |
| 4 | **AI Overview Özel Görünümü** | Tetiklenme oranı, tetiklenende görünürlük, kaynak olma oranı (Brand vs Non-Brand) + AIO'da rakip görünürlüğü |
| 5 | **Brand Sorgularda Marka Nasıl Anılıyor** | Platform / Visibility / Olumlu-Nötr-Olumsuz ton / Avg. Position |
| 6 | **Citation Kaynakları & Source Visibility** | Kaynak / Citation Payı / Citation Visibility |

### 6.1. Brand / Non-Brand ayrımı zorunludur

- **Brand sorular** (marka adı içeren): görünürlük doğal olarak yüksektir; buradaki asıl metrik **sentiment / nasıl anıldığı**.
- **Non-Brand sorular** (kategori/ürün soruları): **rekabetin asıl alanı**; rakip kıyası ve kategori kırılımı burada yapılır.
- **İkisi birleştirilerek "genel visibility" verilmez** - ayrı soru evrenleridir. Tablolarda "Toplam" yerine "Tüm Platformlar" (aynı evren içinde platform toplamı) yazılır.

### 6.2. Kapsam filtreleri (tek karar, her sorguda aynı)

Sunuma başlarken şu üç filtreye karar ver ve **tüm AI sorgularında sabit uygula**:
1. **Tarih**: tüm platformların düzgün koştuğu ilk tarihten itibaren.
2. **Soru tipi**: brand / non-brand ayrımı.
3. **Klasör/segment hariç tutmaları**: ör. pazaryeri veya rakip-hedefli soru grupları.

Filtre kararını dipnota yaz. **Kapsam karışması bu sunumda 4 ayrı hataya yol açtı** (bkz. Bölüm 9).

---

## 7. Teknik Uygulama (PPTX üretimi)

### 7.1. Yöntem: unpack → XML düzenle → repack

```bash
python3 -c "import zipfile; zipfile.ZipFile('deck.pptx').extractall('unpacked')"
# ...düzenlemeler...
( cd unpacked && zip -Xr ../deck_new.pptx . -x '.*' )
python3 <pptx-skill>/scripts/office/validate.py deck_new.pptx --original deck.pptx
```

**Neden python-pptx değil:** Mevcut destelerin renkli run yapısı (aynı cümlede coral ok + ink gövde + yeşil pozitif) ve Google Slides export'unun parçalı run'ları python-pptx ile korunamıyor. XML düzeyinde çalışmak tasarımı bire bir korur.

### 7.2. Yeniden kullanılabilir kütüphane (`lib_deck.py`)

Fonksiyonlar: `esc`, `run`, `para`, `textbox`, `table`, `tc`, `picture`, `add_image_rel`, `clone_slide`, `register_slide`, `scale`, `lerp`.

```python
STYLE = {  # (renk, bold, font)
  "arrow": ("F4845F","1","Bricolage Grotesque"),   # ➔ ok
  "coral": ("F4845F","1","Bricolage Grotesque"),   # vurgu başlık
  "b":     ("10332F","0","Outfit"),                # gövde
  "nb":    ("10332F","1","Bricolage Grotesque"),   # bold gövde
  "pos":   ("2E7D32","1","Bricolage Grotesque"),   # pozitif
  "neg":   ("D32F2F","1","Bricolage Grotesque"),   # negatif
  "note":  ("434343","0","Outfit"),                # dipnot
}
BORD = düz çizgi, renk B7B7B7, prstDash "solid"     # noktalı çerçeve KULLANILMAZ
```

**Heatmap renklendirme** (kolon içi min→max gradyan):
```python
GREEN="57BB8A"   # Session / Visibility
YELLOW="F5C344"  # Transaction
BLUE="6D9EEB"    # Revenue / Citation
# beyaz→doygun: lerp(base, (v-min)/(max-min))
```
Toplam/özet satırları renklendirilmez, **bold** yapılır.

### 7.3. Yerleşim (canvas'a göre ölçekle!)

**Önce `<p:sldSz>` oku.** Bu destede `24.387.175 × 13.716.000 EMU` (standart 9.14M değil). Yanlış varsayım tüm içeriğin köşede minik kalmasına yol açar.

Referans koordinatlar (bu canvas için):
```
Logo/kaynak hizası x   = 538094      ← turuncu "o" logosunun hizası
İçerik üst sınır y     = ~2.350.000
İçerik alt sınır y     = 12.240.000  ← altında logo alanı
Dipnot kutusu y        = ~11.330.000-11.450.000, yükseklik ~780.000
Tanım kutusu punto     = 1650
Dipnot punto           = 1500
Tablo gövde punto      = 1550-1650
Tablo satır yüksekliği = 430.000-620.000 (satır sayısına göre)
```

**KRİTİK:** PPTX'te tablo yüksekliği `<a:ext cy>` ile **kısalmaz**; gerçek yükseklik = `satır sayısı × satır yüksekliği`. Yerleşimi buna göre hesapla.

### 7.4. Chart üretimi (matplotlib)

```python
fig,ax = plt.subplots(figsize=(9.2,5.0), dpi=300)
# çizgi: linewidth=3, markersize=10, veri etiketleri bold
ax.set_yticks([])                      # eksen değil, veri etiketi
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#F2F2F2")
ax.legend(loc="upper center", bbox_to_anchor=(0.5,1.12), ncol=2, frameon=False)
plt.savefig(path, facecolor="white", bbox_inches="tight")
```
PNG'yi `ppt/media/` altına koy, `add_image_rel` ile slayt rels'ine ekle, `picture()` ile yerleştir.

### 7.5. Yeni slayt ekleme

1. Benzer bir slaytı `clone_slide()` ile klonla (pic'ler ve başlık sp'leri korunur, gövde temizlenir).
2. `register_slide(U, "slideNN.xml", after="slideMM.xml", src_rels)` → `[Content_Types].xml` + `presentation.xml.rels` + `sldIdLst`.
3. **Kopyalanan rels'ten `notesSlide` referansını sil** (aksi halde iki slayt aynı nota bağlanır, validator hata verir).
4. Klon kaynağında resim varsa rels uyumunu kontrol et (r:embed ↔ rels Id).

---

## 8. Kalite Kontrol (teslim öncesi zorunlu)

### 8.1. Şema doğrulaması
```bash
python3 <pptx-skill>/scripts/office/validate.py yeni.pptx --original eski.pptx
```
"All validations PASSED" bekle. Yalnızca **orijinalde de var olan** uyarılar (ör. duplicate authorid) kabul edilebilir; farkı `--original` ile teyit et.

### 8.2. Yerleşim kontrolü (programatik)

Her düzenlenen slayt için:
```python
# graphicFrame yüksekliği = Σ <a:tr h>
# kontrol: (a) shape çakışması, (b) y > 12.240.000 taşması, (c) x > canvas_w taşması
# şablonun kendi alt logoları (y>12M pic) hariç tutulur
```
Çakışma/taşma sıfır olmadan teslim edilmez.

### 8.3. İçerik taraması
- `grep "-"` = 0 (em dash yasak)
- `&amp;amp;` = 0 (çift kaçış)
- Bayat/eski değer taraması: önceki sürümün karakteristik sayıları destede kalmamalı
- Mojibake (Ã, Ä±, Â·) = 0
- Çift boşluk taraması

### 8.4. Kapsam tutarlılık denetimi (AI/çok kaynaklı bölümlerde)

Her tablo için **üç soruyu** yanıtla ve tüm slaytlarda aynı cevabı ver:
1. Hangi tarih aralığı?
2. Hangi soru/segment evreni (brand/non-brand, hariç tutulanlar)?
3. Payda ne (yanıt mı, atıf mı, soru mu)?

Bir slaytta bile farklıysa **dipnot ile tablo çelişir** - bu denetimde 4 hata yakalandı.

---

## 9. Denetim Yöntemi (çok slaytlı destelerde)

Deste büyükse (25+ slayt) slayt-bazlı paralel denetim kur:

1. Deste `markitdown` ile metne dökülür (slayt numaralı).
2. Gömülü grafikler `ppt/media/*.png` olarak okunur (LibreOffice yoksa render edilemez; grafikler zaten PNG'dir).
3. **Doğrulanmış veri referansı** (`REFERANS_VERI.md`) hazırlanır: tüm kesin metrikler tek dosyada.
4. Her slayt için bir denetçi: metin + görsel + referans karşılaştırması → bulgu listesi (claim / observed / severity / fix).
5. Her bulgu için karşıt-doğrulayıcı: confirmed / refuted / adjusted.
6. Yalnızca confirmed + adjusted uygulanır.

**Bu yöntemle yakalanan gerçek hatalar:** mükerrer ay etiketi (tablo başlığında Jan/Feb/Mar iki kez), Q1 verisinin Q2 başlığı altında durması, tek kayıttan hesaplanmış "%100" metriği, grafiğin yanlış seriyi göstermesi.

---

## 10. Tuzaklar (bu projede fiilen yaşananlar)

**10.1. Canvas boyutu varsayma.** Deste standart 9.14M EMU değilse tüm yerleşim bozulur. Her zaman `sldSz` oku.

**10.2. Tablo yüksekliği.** `ext.cy` tabloyu kısaltmaz; satırlar taşar ve alttaki kutunun üstüne biner.

**10.3. Yuvarlanmış veriden yüzde hesaplama.** Deck tablosundaki 1.2K/3.3M değerlerinden hesaplanan değişim, ham veriden ±3 puan sapabilir. Çeyreklik/dönemsel yüzdeler **ham veriden** hesaplanır.

**10.4. "Toplam" satırının anlamı.** Farklı soru evrenlerini (brand+non-brand) toplayan bir "genel" metrik anlamsızdır. Aynı evren içindeki platform toplamı geçerlidir → "Tüm Platformlar".

**10.5. Ölçüm kapsamı değişikliğini büyüme sanmak.** Bu projede AI görünürlüğü 20 günde %3 → %31'e çıkmış görünüyordu. Üç platformda eşzamanlı sıçrama organik olamaz; incelemede marka tespitine ana marka alias'ının eklendiği görüldü (bağlam analizinde Temmuz'daki 367 anılmanın 318'i yeni alias'tan). **Dönemsel kıyas iptal edildi.** Kural: keskin sıçramada önce ölçüm setini/tanımını kontrol et.

**10.6. Aynı isimli metriğin farklı formülü.** Tool'un "Source Visibility"si **yanıt bazlı** (kaynak gösterildiği yanıt ÷ toplam yanıt), bizim ilk hesabımız **atıf bazlıydı** (atıf ÷ toplam atıf) - 10 kat fark. **Kural: sunumda araç adıyla anılan her metrik, aracın formülüyle hesaplanır.** Formülü doğrulamak için aracın CSV export'u istenip ters-mühendislik yapılır.

**10.7. Filtre farkını dönem farkı sanmak.** Tool ekranıyla tutmayan değerlerde önce **filtreleri** (brand/non-brand, segment hariç tutmaları), sonra dönemi kontrol et. Bu projede uyumsuzluğun tamamı brand/non-brand + segment filtresindendi.

**10.8. Koşu günü ≠ koşu turu.** Otomatik ölçümler bir güne sığmayabilir (tur 1-3 güne yayılır). Gün bazlı kesit yanlış trend gösterir. **Tur bazında grupla.**

**10.9. Tek kayıttan metrik üretmek.** "İlk 3 payı %100" değeri tek bir kayıttan geliyordu. **X/Y formatı** (pay/payda birlikte) bu hatayı görünür kılar - tablolarda ham sayı + yüzde birlikte verilmelidir (ya da payda dipnotta).

**10.10. Klon kaynağı rels uyumsuzluğu.** Başka slayttan klonlanan slaytın rels'i resim referanslarını taşımayabilir → "non-existent relationship" hatası. Klonu kendi dosyası üzerinden kurmak daha güvenli.

**10.11. Scratchpad kalıcı değil.** Ara dosyalar (script, unpacked klasör) silinebilir. Yeniden kullanılacak kod `lib_deck.py` olarak yazılmalı ve **proje klasörüne** kopyalanmalı.

---

## 11. Dil ve Stil (özet - detay: İçerik Dili Rehberi)

- **Rejim A** (kurumsal rapor/sunum): pasif ton, 3. tekil şahıs, "-mıştır/-mektedir".
- **➔ insight formatı:** `➔ [metrik + dönem] + [kontrast/yön] + (rakam kanıtı). [Çıkarım cümlesi].`
- Ok sonrası **tek boşluk**; her insight tek okla başlar.
- **Yüzde formatı:** işaret + % + sayı → `+%9`, `-%18`, `%26.1`. Tabloda da aynı.
- Ondalık ayırıcı **nokta**; binlik **nokta** (TR) - tek çıktıda tek sistem.
- **Em dash yasak**, emoji yasak, emir kipi yok.
- Negatif bulgu nötr çerçevelenir: "daralma / gerileme / sınırlı kalmıştır"; en sert ifade "dikkat çekmektedir".
- Rakip zayıflığı marka fırsatı olarak yazılır; agresif fiil kullanılmaz.
- **Araç adı politikası:** veri kaynağı araçları (GSC, GA4, SEOmonitor, Ahrefs) yazılabilir; otomasyon araçları (Claude, MCP, script) müşteri çıktısında **görünmez**. AI görünürlük aracı "Inbound AI Visibility izleme sistemi" olarak anılır.
- Her veri slaytında **kaynak notu**: `Kaynak: [araç] | [dönem] · [kapsam notu]`.

---

## 12. Çalışma Akışı (adım adım)

```
1.  Sunum tipini ve dönem eksenini netleştir (Bölüm 1)
2.  Mevcut deste varsa: unpack + markitdown + slayt haritası çıkar
    → hangi slaytlar güncellenecek, hangileri kullanıcıda
3.  Veri kaynaklarını sırayla doğrula:
    - GSC: property + 16 ay kısıtı
    - GA4/AEM: export var mı, yuvarlanmış mı
    - AI visibility: proje, koşu turları, filtre kararı
4.  REFERANS_VERI.md oluştur (tüm kesin metrikler tek dosyada)
5.  Slaytları üret/güncelle (lib_deck ile, renkli run yapısını koruyarak)
6.  Chart'ları üret (matplotlib → ppt/media)
7.  Paketle + validate
8.  Yerleşim kontrolü (çakışma/taşma) - sıfırlanana kadar iterasyon
9.  İçerik taraması (em dash, bayat değer, mojibake)
10. Kapsam tutarlılık denetimi (Bölüm 8.4)
11. Teslim + FLAG listesi (veri kısıtları, görsel kontrol gerektirenler)
12. Proje günlüğünü güncelle (<proje>-claude.md)
```

### 12.1. Kullanıcıya sorulacaklar (baştan netleştir)

- Sunum tipi ve dönem ekseni?
- Hangi slaytlar sende güncel, hangilerini ben güncelleyeceğim?
- Veri kaynağı önceliği (hangi aracın rakamı esas)?
- Snapshot slaytlar (tek çeyreğe kilitli listeler) dönüştürülecek mi, yoksa etiketi mi düzeltilecek?
- Araç ekranıyla birebir tutarlılık mı, daha geniş örneklem mi?

### 12.2. FLAG raporlama (teslimde)

Her teslimde şunlar ayrıca bildirilir:
- Doğrulanamayan veriler ve nedeni
- Görsel-içi metinler (grafik başlıkları) - yeniden export gerektirenler
- Örneklem/dönem kısıtları
- Deste içinde kalan iç yorumlar (ppt/comments) ve konuşmacı notları

---

## 13. Kontrol Listesi (teslim öncesi)

- [ ] Her slaytın başlığında dönem yazılı ve tabloyla örtüşüyor
- [ ] Tüm yüzdeler `+%X` / `-%X` formatında, ondalık nokta
- [ ] Em dash 0, mojibake 0, emoji 0, çift boşluk 0
- [ ] Her veri slaytında kaynak notu var
- [ ] Metrik tanımları slayt altında, formülde markanın gerçek sayıları
- [ ] Kapsam (tarih/evren/payda) tüm slaytlarda tutarlı
- [ ] Şema doğrulaması PASSED
- [ ] Çakışma/taşma kontrolü temiz
- [ ] Chart'lar deck stilinde (renk paleti, veri etiketli, eksen yok)
- [ ] Tablo çerçeveleri düz çizgi, başlık `#434343` + beyaz bold
- [ ] Otomasyon aracı adı sızmamış
- [ ] Bayat değer taraması temiz (önceki sürüm kalıntısı yok)
- [ ] FLAG listesi hazırlandı
- [ ] Proje günlüğü güncellendi
```
