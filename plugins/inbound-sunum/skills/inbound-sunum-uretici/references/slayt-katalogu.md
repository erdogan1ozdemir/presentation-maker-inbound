# Slayt Kataloğu

> Faz 4'te okunur. Yedi gerçek desteden (VitrA ×3, Turkcell, Gameplus, Enerjisa,
> KIKO, Özdilekteyim, Loft) çıkarılmış slayt tipleri. Her tip: amaç, veri girdisi,
> `deck.json` karşılığı, insight kalıbı.
>
> Kullanım: moda göre iskeleti Bölüm 1'den seç, sonra her slaytın tipini Bölüm 2'den
> bul. Tablo şemaları `tablo-semalari.md`'de (T1-T14).

## İçindekiler

1. [Mod bazlı deste iskeletleri](#1-mod-bazlı-deste-iskeletleri)
2. [Slayt tipleri](#2-slayt-tipleri)
   - [Çatı: C01-C03, C28](#çatı)
   - [Arama hacmi: C04-C08](#arama-hacmi--rekabet)
   - [GA4: C09-C13](#ga4-trafik-ve-ticari-sonuç)
   - [GSC: C14-C19](#gsc-görünürlük-ve-trafik)
   - [Görünürlük ve AI: C20-C25](#görünürlük-rakip-ve-ai)
   - [Süreç ve kapanış: C26-C27](#süreç-özet-ve-plan)
   - [Etki analizi: C30-C34](#etki-analizi-m4)
   - [Ek: C35-C37](#ek-bölümler)

---

## 1. Mod bazlı deste iskeletleri

### M1 - Aylık, tek property, e-ticaret (referans iskelet, 22 slayt)

```
01 Kapak                                  C01
02 SUNUM AKIŞI                            C02
03 Ayraç: 01 Arama Hacmi & Rekabet        C03
04 Marka (only brand) arama hacmi         C04
05 Marka + kategori arama hacmi           C05
06 Non-branded arama hacmi                C06
07 Kategori kırılımlı hacim               C07
08 Rakip arama hacmi değişimi             C08
09 Ayraç: 02 GA4 Trafik                   C03
10 GA4 organik trafik + session delta     C09
11 GA4 revenue & transaction              C10
12 GA4 AI referral trafik                 C12
13 Ayraç: 03 GSC Trafik & Sıralama        C03
14 GSC brand & non-brand tablosu          C14
15 GSC organik trafik trendi              C15
16 Rakip visibility karşılaştırması       C20
17 Share of Clicks + AI Search SoV        C21
18 Kategori bazında visibility            C22
19 Visibility'yi etkileyen kelimeler      C23
20 En iyi artış yaşayan kelimeler         C24
21 Ahrefs sıralama dağılımı               C25
22 Teşekkürler                            C28
```

### M1 varyant - lead-gen / kurumsal (Enerjisa tipi)

"Neler Yaptık" ile başlar, blog bölümü içerir, sonda kırılımlı yönetici özeti:

```
Kapak · Akış · Ayraç 01 Neler Yaptık (C26) · Çalışma etkisi kanıtı (C26b)
Ayraç 02 Marka Aranma Hacmi (C04/C05)
Ayraç 03 Organik Trafik (C09 · C15 · C13)
Ayraç 04 Blog Performansı (C18 · C19)
Ayraç 05 Kelime Sıralamaları & Rekabet (C20/C21 · C24)
Ayraç 06 Yönetici Özeti (C27) · Teşekkürler
```

### M1 varyant - segment kırılımlı aylık (Game+ tipi, 31 slayt)

Marka talebi ile kategori talebinin ayrı okunması gereken, dönem içinde teknik
bir geçiş yaşanmış destelerde kullanılır. Search Console bölümü segment
tanımıyla açılır; GA4 ve içerik bölümleri aynı segment diliyle devam eder.

```
Kapak · Akış
Ayraç 01 Genel Görünüm: yönetici özeti + KRİTİK TESPİT (C27) · Segment
  tanımları (C44)
Ayraç 02 Google Search Console Metrikleri: aylık click serisi (C45) · aylık
  impression serisi (C45) · dönem karşılaştırması pozisyonlu (C46)
  · sorgu hareketleri (C47) · sayfa hareketleri (C47)
Ayraç 03 <Etki> Geçişi: simetrik pencere tablosu (C31) · haftalık grafik (C48)
Ayraç 04 GA4 Trafik: toplam ve organik aylık seri (C09) · kanal kırılımı (C11)
Ayraç 05 İçerik Performansı: blog toplam+organik (C50) · yükselen yazılar (C19)
  · alt kategori performansı GA4+GSC (C49)
Ayraç 06 Yapay Zeka Görünürlüğü: mention & citation (C51) · örnek promptlar
  (C52) · markadan nasıl bahsediliyor (C53) · AI kaynaklı trafik (C11)
Ayraç 07 Yapılan ve Planlanan İşler (C26 · C26c)
Ayraç 08 Değerlendirme (C43) · Teşekkürler
```

### M2 - Çeyreklik, çok property (Turkcell tipi)

```
Kapak · Akış · Yönetici Özeti (C27) · Kanal bazlı genel trafik (C11)
Kanal payı trendi (C11b) · Aylık kanal davranışı (C11c)
AI Overview'ın CTR etkisi (C16) · Marka talebi uzun dönem trendi (C04)
--- her property için tekrarlanan blok ---
  Ayraç: property adı (C03) · Property ajandası (C02b)
  Genel performans KPI (C14b) · Branded trafik (C14) · Non-branded trafik (C14)
  [gerekiyorsa] Impression metodolojisi (C17) + regex/filtresiz kıyas (C17b)
  KPI kelime highlight (C23b) · En çok trafik getiren sayfalar (C19)
  Sayfa kümesi performansı (C19b) · Neler Yaptık (C26)
  Rakip görünürlük & SoC (C20/C21) · AI SoV (C21b) · Q+1 iş maddeleri (C26c)
--- blok sonu ---
Teşekkürler
```

### M3 - Yarıyıl

M1 iskeletini korur, üç farkla: tüm karşılaştırmalar H-YoY'a çevrilir ve MoM
kolonları kalkar; GSC/GA4 tablolarında **aylık ortalama** satırı esas alınır
(`2025'H1 Avg.` vs `2026'H1 Avg.`), toplam ikinci satır olur; araya iki slayt girer -
yarıyıl içi aylık dalgalanma grafiği ve dönemin olay çizelgesi.

### M4 - Etki analizi (Gameplus SSR tipi, 21 slayt)

```
Kapak: "<Marka> SEO Performans Değerlendirmesi - <Etki> Etkisi" · Akış
Ayraç 01 Brand Performansı: 15 aylık trend (C13) · MoM top artış/düşüş (C30)
  · YoY top artış/düşüş (C30)
Ayraç 02 Non-Brand Performansı: MoM (C30) · YoY (C30)
Ayraç 03 <Etki> Geçişi: genel özet 4 segment kartı (C31)
  · brand detayı (C31b) · non-brand detayı (C31b) · blog detayı (C31b)
Ayraç 04 Hedef Takibi: faz hedefi ve öncelikli aksiyonlar (C32)
Ayraç 05 Sorgu & Hacim: click+hacim birleşik tablo (C33) ×2 · grup özeti (C34)
Teşekkürler
```

### Birleşik mod (M1 + M2)

Çeyreğin son ayında aylık deste hazırlanırken çeyreklik bölüm **aynı destenin sonuna
ayrı kapak + ayrı ajanda ile** eklenir. Ev pratiği bu; çeyreklik için ayrı deste
açmaya tercih edilir. Gerçek örnek: 21 slayt aylık + ara kapak + 25 slayt çeyreklik.

---

## 2. Slayt tipleri

### Çatı

**C01 Kapak** · `type: cover`
Format: `<Marka> | Aylık SEO Değerlendirme` + alt satır dönem. Çeyreklikte
`<Marka> <Yıl> Q<N> SEO Değerlendirme Sunumu`.

**C02 SUNUM AKIŞI** · `type: agenda`
Numaralı ajanda (01, 02...). Başlık "SUNUM AKIŞI" veya "NELER KONUŞACAĞIZ?" olabilir,
deste içinde tek varyant. **Madde sayısı ayraç sayısına eşit.**

**C02b Property ajandası** · `type: agenda` (numarasız sade liste)
Çok property'li destelerde her property bölümünün başında o property'nin alt
başlıkları listelenir.

**C03 Bölüm ayracı** · `type: separator`
Büyük numara + bölüm adı. Ajandadaki numara ve adla birebir eşleşir.

**C28 Teşekkürler** · `type: closing`
İstenirse öncesine "sonraki adım" slaytı: özet dolgusuyla değil bir sonraki adımla
bitirilir.

### Arama hacmi & rekabet

**C04 Marka (only brand) arama hacmi**
Veri: Keyword Planner `brand_only`, aylık, son 2-3 yıl.
Tablo: satırlar = yıllar, kolonlar = Oca-Ara, son satır `26 vs '25 Change`.
Cari yılın oluşmamış ayları `-` ile bırakılır; tahmin yazılmaz.
Çeyreklikte ek mini tablo: `QoQ | Q-YoY`.
Insight: "Only brand arama hacmi Mart ayında geçtiğimiz yıla göre aynı kalmıştır."
Kaynak: `Keyword Planner`

**Kelime ve ülke seçimi (bağlayıcı):**
- Kelime **yalnızca marka adının kendisidir**: Flormar için `flormar`, VitrA için
  `vitra`. Ürün kırılımı (`flormar maskara`, `vitra klozet`) brand hacmine
  katılmaz - ölçülen şey marka talebidir, marka + ürün talebi değil.
- Ülke, markanın hizmet ettiği pazardır ve **SEOmonitor kampanyasının takip
  ettiği pazardan** alınır: kelimeler TR'de takip ediliyorsa Türkiye, UK'de
  takip ediliyorsa Birleşik Krallık. Kampanya pazarı ile hacim ülkesi ayrışırsa
  tablo yanlış pazarı ölçer.
- Kaynak: Keyword Planner ya da MCP üzerinden DataForSEO
  `dataforseo_labs_google_historical_keyword_data` (`location_name`,
  `language_code`). Her `history` kaydı bir snapshot'tır ve son 12 ayı taşır;
  uzun seri için snapshot'lar birleştirilir (aynı ay birden çok snapshot'ta
  varsa en yenisi alınır).

**Tek terimde bant sorunu ve YoY satırı.** Google Ads tek bir terim için hacmi
bant halinde döndürür; 24 ayda yalnızca birkaç basamak görülebilir (gerçek örnek:
`flormar` için 74.0K / 90.5K / 110.0K). Bu durumda **ay bazında YoY satırı
yazılmaz** - o satır talep hareketi değil bant geçişi gösterir ve tekrar eden
+%0.0 / +%22.3 / -%18.2 değerleri üretir. Değişim **dönem toplamı** üzerinden
verilir (Oca-Haz 2026 vs Oca-Haz 2025 gibi) ve dipnotta bandın varlığı nötr
biçimde belirtilir. Matriste aylık değerler yine gösterilir; okuyucu seviyeyi ve
mevsimselliği görür.

Sürekli aylık seri gerekiyorsa Ahrefs `keywords-explorer-volume-history` çapraz
kontrol olarak kullanılabilir; ancak iki kaynak hem seviye hem yön olarak
ayrışabilir (aynı terimde Ahrefs ~49K / Google Ads ~85K, bir dönemde biri -%1.7
diğeri +%6.9). **Tek metrik tek kaynak:** ikisi yan yana konmaz, biri seçilir.

**C04b Marka adı arama hacmi (tek slayt)**
`grid: [46, 54]`. `kpi` (col 0, iki kart: dönem toplamı + YoY deltası, aylık
ortalama) · `insights` (col 1) · `table` (col `full`, başlık "Aylık Arama Hacmi")
= yıl × ay matrisi, 2-3 yıl satırı, oluşmamış aylar `-`.
KPI kartı **son ay odaklıdır**: verinin bulunduğu son ayın hacmi, altında
`MoM` ve `YoY` deltaları. Dönem (YTD) karşılaştırması KPI'ya değil **dipnota**
yazılır - kart cari durumu, dipnot kümülatif seyri taşır.
Insight üçlüsü: son ay hacmi ve bandı → aylık ortalama ve en yüksek ay → marka
talebinin GSC branded impression hareketiyle ilişkisi.
Oluşmamış ay için dipnot ifadesi: "… arama hacimleri Google tarafından henüz
yayınlanmamıştır" (iç kısıt dili kullanılmaz).
Bu slayt **"Arama Hacmi ve Pazar Talebi" bölümünde, yönetici özetinin hemen
ardına** konur; performans bölümlerinin bağlamını kurar.

**C04c Non-brand takip edilen kelimelerin arama hacmi (SEOmonitor)**
Brand slaytının eşi. Veri: SEOmonitor `get_group_data`, üst düzey kategori
klasörlerinin `group_ids` listesiyle; Brand grubu için `group_id: -1`.
`grid: [56, 44]`. `table` (col 0, başlık "Kategori Kırılımı") kolonları:
`Kategori | Keyword | Aylık Hacim | YoY | Visibility`, son satır `Toplam`
(`highlight_rows` ile). `insights` (col 1). `bar` (col `full`) = kategori
toplamlarının 13 aylık serisi.

Notlar:
- Grup `search_volume` alanı, gruptaki kelimelerin hacimlerinin **toplamıdır**
  (ortalama değil). Brand grubunda kelime hacimleri toplanarak doğrulanabilir.
- `search_data.year_over_year` oran döner (-0.05 = -%5).
- Kampanyada takip edilen toplam kelime sayısı ile kategori + Brand toplamı
  eşleşmiyorsa fark dipnotta belirtilir (ungrouped ve çalışma grupları).
- Insight üçlüsü: toplam hacim + YoY → hacmin yoğunlaştığı kategori → hacme
  karşılık visibility'nin düşük kaldığı kategori (açık alan) → brand payı.

**C05 Marka + kategori arama hacmi** - C04 yapısı, `brand_category` seti.
Insight YoY + MoM birlikte.

**C06 Non-branded arama hacmi** - C04 yapısı, `non_brand` seti.
Bu slayt pazar talebinin kendisini ölçer; sonraki tüm performans yorumlarının
bağlamı olur.

**C07 Kategori kırılımlı hacim** (tek slaytta dört tablo)
`grid: [50, 50]`, dört `table` bloğu: NonBrand YoY, NonBrand MoM, Brand+Kategori YoY,
Brand+Kategori MoM. Kolonlar: `Kategori | <Önceki> Avg. | <Dönem> Avg. | Change`,
son satır `Grand Total`.
Insight: en yüksek artış + en yüksek düşüş kategorileri isimle, yüzdeyle.

**C08 Rakip arama hacmi değişimi**
Satırlar = markalar (marketplace'ler üstte, direkt rakipler altta, kendi marka kendi
sırasında `highlight_rows` ile), kolonlar = son 14-15 ay + `YoY` + `MoM`.
Insight üç cümle: kendi marka, YoY artan rakipler isimle, MoM hareketi.
Not: bucket etkisiyle değişimler tekrar eden değerlerde kümelenir; her rakip için
ayrı sebep aranmaz.

**C08b Pazar yeri / kanal ayrı slaytı** - marketplace ve perakende zincirleri ayrı
slaytta; marka rakipleriyle aynı tabloda karışmaz.

**C08c Kelime bazında hacim artan/azalan**
Kolonlar: `Keyword | <Önceki yıl> | <Dönem> | Change | YoY | Generic Keyword Volume YoY`.
Son kolon imzadır: marka+kelime hacmindeki değişimi jenerik kelimedeki değişimden
ayrıştırır. Marka hacmi düşerken jenerik sabitse bu marka özelinde bir daralmadır.

**C19b Brand / Non-Brand: Impression, Click, CTR, Pozisyon (2x2)**
`grid: [50, 50]`. Dört tablo: `Impression` (col 0), `Click` (col 1), `CTR`
(col 0, `mt`), `Ortalama Pozisyon` (col 1, `mt`); altında `insights` (col `full`).
Metrik adı ayrı `title` bloğu yerine **`head[0]`'a** yazılır - dört tablo
üst üste geldiğinde başlık blokları 34px×2 yer yiyor.
Satırlar: `Total | Branded | Non-Brand | Anonim sorgu`, `bold_rows: [0]`.
Kolonlar: `<metrik> | <önceki dönem> | <dönem> | YoY`.

Zorunlu kurallar:
- **Anonim sorgu satırı atlanmaz** (bkz. tuzaklar 2.9b): brand = total − non-brand
  hesabı anonim hacmi brand'e yazar ve segment paylarını bozar.
- Pozisyonda **pozitif değer iyileşmedir** (7.1 → 5.1 = +2.1) ve bu dipnotta
  yazılır; anonim satırında pozisyon türetilemez, `-` bırakılır.
- Sıkışma önlemi: `row_h: 20`, `head_h: 24`, tablo `font_pt: 10.5`,
  insights `font_pt: 10.5`, tek dipnot.

### GA4 trafik ve ticari sonuç

**C09 GA4 organik trafik ölçümlemesi**
`kpi` bloğu (organik session, organik payı, revenue, CR) + `bar` (aylık seri) +
`insights`. Mini tablolar: `Organic Sessions YoY` ve `MoM` (T7).
Insight: "Mart ayında gelen toplam ziyaretin (333K) %52.4'ünü (174.7K) organik kanal
oluşturmaktadır." + delta cümlesi.

**C10 GA4 revenue & transaction** (e-ticaret)
Dört mini tablo: Revenue YoY, Revenue MoM/QoQ, Transaction YoY, Transaction MoM/QoQ.
Her tabloda `Total`, `Organic`, `Organic/Total %` satırları.
Insight ana mesajı organik payın yönüdür: "Organik kanalın toplam işlem içindeki payı
%42.6'ya ulaşmıştır (+11.3 puan)." **`Organic/Total %` satırındaki değişim puan
farkıdır**, yüzde değişimi değil; metinde "puan" yazılır.

**C10b GA4 lead / form** (lead-gen)
Revenue yerine form success event sayısı, organik payı, kanal bazlı ortalama session
süresi. Örnek: "Organik kanalda 122K Session'a karşılık 31 Form Success eventi
atılmıştır. Sitedeki toplam başarılı formun %14'ü organikten gelmiştir."

**C11 Kanal bazlı genel trafik**
İki yan yana tablo bloğu: `YIL (YoY)` ve `ÇEYREK (QoQ)`. Kolonlar:
`Kanal | <Önceki> | <Dönem> | % | Δ session`. Altına `note` bloğu ile toplam büyüme
bağlamı. Bu slayt organik düşüşü toplam büyüme bağlamına oturtur; organik tek başına
yorumlanmaz.

**C11b Kanal payı trendi** - son 5 çeyrek (veya 12-15 ay) × ana kanallar. Kanal
kayması argümanının veri temeli.

**C11c Aylık kanal davranışı** - dönem içindeki tek bir ayın tüm kanallarda benzer
davranıp davranmadığını gösterir. Tek kanala özgü olmayan düşüşün mevsimsel/sistemik
olduğunu göstermek için.

**C12 GA4 AI referral trafik**
İki KPI kartı (Sessions, Users) × iki delta + trend grafiği.
Yüksek yüzdeler düşük tabandan geldiği için **mutlak değer de verilir**.
Dipnot: filtrelenen kaynak listesi.

**C13 Uzun dönem trend (15 ay, brand vs non-brand)**
Satırlar `Non-Brand Sessions` / `Brand Sessions` / `Brand % Total`, kolonlar 15-23 ay.
Yanına `panels` veya `insights` ile "Anahtar Bulgular": 3-4 madde, kalın başlık + tek
cümle. Yapısal kırılmaların (kampanya, PR, site değişikliği) görüldüğü slayt.

### GSC görünürlük ve trafik

**C14 GSC brand & non-brand** (deste omurgası)
Ana tablo (T2) + insights. Insight sırası: Total → Branded → Non-Branded; her biri
impression, click, CTR sırasıyla.

**C14b Genel performans KPI kutuları**
Dört büyük rakam: `Impression (YoY)`, `Click (YoY)`, `Impression (QoQ)`, `Click (QoQ)`.
Altında iki `panels` kolonu: `YILLIK BÜYÜME ÖNCÜLERİ` ve `CLICK DÜŞÜŞÜNÜN KAYNAKLARI`,
her biri sorgu kümesi etiketleriyle.

**C15 GSC aylık metrik serisi - iki slayt** (ev standardı)

VitrA ve Özdilekteyim destelerindeki desen. Slayt iskeleti üç katman:
**üstte grafik, ortada değişim notu, en altta tam seri tablosu.**

*C15a - Aylık Impression & Click*
```
bar  (Impression, 13 ay, gold)          h≈84
bar  (Click, 13 ay, gray_bar)           h≈84   ← ayrı grafik, ayrı ölçek
note (label: "Değişim")                        ← MoM ve YoY tek satırda
table (Metrik × 13 ay)                         ← tam seri, slaytın en altı
```
- İki metrik **ayrı grafiklerde** verilir. Ölçekleri farklı olduğu için aynı
  eksende okunmaz; çarpanla ölçeklemek müşteri destesinde hoş durmuyor.
- Değişim notu: `Click MoM +%8.3 · YoY -%18.9 · Impression MoM +%6.8 · YoY -%44.6`
  biçiminde tek `note` bloğu. Ayrı mini tablolara gerek yok; not yeterli.
- Tablo en altta, `font_pt: 10`, `align: "l" + "c"*13`.

*C15b - Aylık CTR & Pozisyon*
- Aynı iskelet; iki bar: CTR (coral) ve Avg. Position (`invert: true`).
- **Pozisyon grafiği ters eksenli çizilir**: pozisyon 1'e yaklaştıkça bar
  yükselir, yani iyileşme yukarı okunur. Dipnotta bu açıkça yazılır - aksi halde
  okuyucu grafiği tersine yorumlar.
- Değişim notu: CTR puan (p) olarak, pozisyon "iyileşme" olarak.
- Ortalama pozisyon cihazlar arasında **impression ağırlıklı** hesaplanır ve bu
  dipnotta belirtilir.

**Neden iki slayt:** dört metriği tek slayta yığmak hem grafiği hem tabloyu
okunmaz hale getiriyor. Karosel olarak ardışık iki slayt ev pratiğidir.

**Zorunlu:** olay dipnotları ve GSC 16 ay penceresi nedeniyle serinin nerede
başladığının belirtilmesi.

**C16 AI Overview'ın CTR'a etkisi**
AI Overview yayına alınma tarihi işaretli CTR trendi. Tarih net yazılır: "18 Şubat'ta
AI Overview'ın yayına alınmasıyla CTR düşüşleri gözlenmeye başlanmıştır."

**C17 Impression düşüşü metodoloji slaytı**
`panels` üç kutu: `Aggregation Yöntemi Farkı`, `Hedef Odaklı Impression Dağılımı`,
`GSC Impression Bug`. Altında `➔ SONUÇ:` satırı.
**İnceleme kapsamı kutusu zorunlu:** kaç ortak query, hangi iki export karşılaştırıldı.

**C17b Regex vs filtresiz rakam kıyası**
Tablo: `Keyword | REGEX'Lİ <Ö>→<D> | Δ% | FİLTRESİZ <Ö>→<D> | Δ%`. Yanda iki büyük
rakam. Kanıt cümlesi: "Click +%7.3 artmış; impression düşerken click artması
aggregation etkisini göstermektedir."

**C18 Blog / içerik bölümü trafiği**
Dönem vs geçen yıl aynı dönem, tek büyük rakam + yüzde değişim. Düşüşse trend süresi
de verilir ("2025'ten beri süregelen bir trend").

**C19 En çok trafik getiren sayfalar**
Tablo: `URL | Click | Impression | Pozisyon | Kategori`, 9-20 satır. Yanına kategori
dağılımı kutusu (`note`) ve KEY INSIGHT satırı: "iOS kategorisi tek başına toplam
click'in ~%50'sini üretmektedir."

**C19b Sayfa kümesi / kategori bazlı performans**
`Kategori | <Dönem> Click | <Dönem> Imp | QoQ % | YoY %`. URL→kategori eşleme kuralı
config'te tutulur ve `note` ile şeffaf yazılır.

### Görünürlük, rakip ve AI

**C20 Rakip visibility karşılaştırması**
Tablo: `Domain | Mobile Visibility | Δ Mobile | Desktop Visibility | Δ Desktop`.
Kendi domain `highlight_rows` ile.
**Zorunlu `note` bloğu:** "Visibility score, <marka> projesi özelinde takip edilen
kelimelerin görünürlük oranını yüzdesel olarak gösterir. <N> hedef anahtar kelime
takip edilmektedir."
Insight sırası: kendi hareketimiz → pozitif ayrışan rakip → en yüksek düşüş yaşayanlar.

**C20b Share of Click + Visibility birlikte (iki tablo, tek slayt)**
`grid: [52, 48]`. `table` (col 0, başlık **"Share of Click"**) ve `table`
(col 1, başlık **"Visibility Score"**), altında `insights` (col `full`).
Kolonlar her iki tabloda aynı: `Domain | <önceki yıl> | <önceki dönem> | <dönem> | MoM | YoY`.
Kendi domain iki tabloda da `highlight_rows` ile işaretlenir.

**İki tablo aynı domain setini ve aynı satır sırasını taşır.** Share of Click
yanıtı günlük top 10 döndürdüğü için domain listesi oradan çıkar; visibility ise
`domain` parametresiyle tek tek çekilir, dolayısıyla listeyi eksik bırakmak
teknik bir zorunluluk değil tercihtir. Satır sırası Share of Click'in cari dönem
değerine göre kurulur ve visibility tablosunda aynen tekrarlanır; böylece iki
tablo satır satır okunur. Sıralama ölçütü dipnotta belirtilir.

**Bağlayıcı kural - iki metrik ayrı tutulur.** Visibility Score, takip edilen
kelime setinde markanın görünürlük oranıdır ve SEOmonitor panelinde görülen
değerdir. Share of Click ise aynı kelime setinde tahmini organik tıklamaların
**tüm domainler arasındaki dağılımıdır**. Aynı markanın Visibility'si 53 iken
Share of Click'i %8 olabilir; bunlar çelişki değil farklı metriklerdir. Tek
tabloda ya da tek başlık altında birleştirilmez, her tablo kendi dönem tabanını
dipnotta beyan eder.

**Dönem tabanı.** Share of Click günlük seriden **dönem ortalaması** olarak alınır
(tek gün anlık değer aylık ortalamadan 1 puana kadar sapabilir). Visibility
**dönem sonu** değeriyle verilir; böylece marka panele baktığında aynı sayıyı
görür. İki farklı taban kullanıldığında her tablonun dipnotunda hangi tabanın
kullanıldığı açıkça yazılır.

**C21 Share of Clicks + AI Search SoV**
İki grafik yan yana (`grid: [50,50]`).
**Zorunlu dipnot:** "*AI Share of Voice takip edilen kelimelerin arama hacimlerine ve
bu kelimelerdeki AI yanıtlarında bahsedilme ve linklenme oranına göre hesaplanır."
Insight: lider marka → kendi sıramız → 3. marka → AI tarafında ayrışma.

**C21b AI Overview SoV sıralaması**
Domain × SoV × sıra tablosu. **Bağlam kutusu zorunlu:** AI Overview'ın ilgili pazarda
ne zaman yayına alındığı. `AI Overview SoV` ve `AI Search SoV` **farklı metriklerdir**;
ikisi birden kullanılıyorsa ikisinin de tanımı dipnotta verilir.

**C22 Kategori bazında visibility değişimi**
Kategori × visibility Δ. Insight: artan kategoriler, sonra düşenler; ikisi de isimle
ve yüzdeyle.

**C23 Visibility'yi en çok etkileyen kelimeler**
`Top Search Vol. Keywords` tablosu. Panel export'u görsel olarak konabilir ama
slaytta okunur bir özet cümle bulunur - bulgu görsele delege edilmez.

**C23b KPI anahtar kelime highlight'ları** - KPI kelime havuzlarının pozisyon ve
click değişimi.

**C24 En iyi artış yaşayan / en çok düşen kelimeler**
İki-üç `panels` veya `table`: `En İyi Artış Yaşayan Kelimeler`, `YoY Aranma Hacmi En
Çok Artan Kelimeler`, `En Çok Düşüş Yaşayan`.

**C24b Keyword rank MoM tablosu**
`Keyword | Volume | <Önceki ay> Rank | <Ay> Rank | MoM Change`. Kategori başına ayrı
slayt. **100 = takipte ilk 100'de yok** anlamındadır ve bu dipnotta belirtilir.

**C25 Ahrefs sıralama alınan kelime değişimi**
İlk 3 / ilk 10 / ilk 100 kelime sayısı trendi.
**Zorunlu okuma kılavuzu:** "Tablo altındaki G ifadeleri Google update'lerini, yeşil
daireler büyük çaplı içerik değişikliklerini göstermektedir."

### Insight slaytları (her ana bölüme bir tane)

Veri slaytları durumu gösterir; insight slaytı **aynı verinin ne anlama geldiğini ve
nereden tutulabileceğini** gösterir. Ev pratiği: her ana bölümün sonuna bir tane.
Hepsinde ortak kural: tablo ölçülmüş veriyi taşır, insight yorumu taşır, aksiyon
"…değerlendirilebilir / ele alınabilir / önceliklendirilebilir" kipiyle verilir.

**C38 Talep ile trafiğin ayrışması** (arama hacmi bölümü)
İki tablo: sol tarafta marka arama hacmi + branded impression / click / CTR /
pozisyon; sağ tarafta click payı dağılımı (Branded / Non-Brand / Anonim sorgu,
önceki ve cari dönem payları). Soru: talep ile marka trafiği aynı yöne mi gidiyor,
kaybedilen tıklama başka bir segmente mi kaydı?
Gerçek örnek çıkarım: marka hacmi yatay, branded impression -%62.8 - paralel
gitmiyor; üç segmentin payı ±2 puan bandında kalmış, yani trafik kaymamış, üçünde
birlikte azalmış.

**C39 İlk sayfada yer alan ve CTR'ı geride kalan sorgular** (Search Console bölümü)
Tablo: `Query | Impression | Pozisyon | CTR | Click`, gösterime göre sıralı,
non-brand. Ortalama pozisyonu ilk sayfa aralığında olduğu halde CTR'ı %1 altında
kalan sorgular. Karşılaştırma satırı olarak anasayfanın pozisyon/CTR değeri verilir -
okuyucu farkı kendi görür.
Aksiyon: ilgili listeleme sayfalarında meta title/description düzenlemesi.

**C40 Pozisyonuna göre CTR'ı geride kalan sayfalar** (Search Console bölümü)
C39'un sayfa karşılığı. Son satır `Anasayfa (karşılaştırma)` ve `highlight_rows`
ile işaretlenir.
**Hipotez kontrolü zorunlu:** "sayfada az ürün olduğu için tıklanmıyor olabilir"
gibi bir açıklama sunulacaksa önce ölçülür (sayfa açılır, ürün sayısı sayılır) ve
sonuç dipnota yazılır - doğrulanmadıysa da yazılır. Gerçek örnek: iki sayfada 31-32
ürün ölçüldü, listeleme derinliği farkı açıklamıyordu; bunun yerine bir sayfanın
H1'inin eksik olduğu tespiti dipnota girdi.

**C41 Rakiplerin önde olduğu kategori kelimeleri** (görünürlük bölümü)
Tablo: `Keyword | Hacim | Mobil sıra | Desktop sıra`. Kaynak: SEOmonitor
`get_top_keywords` (`metric: opportunity`) - yanıttaki `difficulty` ve `avg_cpc`
alanları **tabloya taşınmaz** (bkz. tuzaklar 2.8b).
Cihaz takip derinliği farklıysa dipnota yazılır (mobil 100, desktop 20 → desktop
21 değeri "takip aralığı dışında" demek).
Kapsam dışı ve mevsimsel jenerik kelimeler (black friday vb.) listeye alınmaz.

**C42 Kategori bazında AI Overview görünürlüğü** (AI bölümü)
Tablo: `Kategori | AIO kelime | Marka görünen | Anılma | Citation`. Kaynak:
SEOmonitor `get_group_data` → `aio_data`. Ek çekim gerekmez.
İmza çıkarım: anılma yüksek ama citation düşük olan kategori, "yanıtta adı geçiyor
ama kaynak olarak seçilmiyor" alanını gösterir; aynı destede citation'ı yüksek bir
kategori bunun mümkün olduğunu gösteren karşılaştırma olur.

**C43 Öne çıkan başlıklar (kapanış)**
Matris kurulmaz. `panels` bloğu ile üç kart: her kartta **durum** ve altında
**ne yapılabilir**. Kapanış insight'ı üç başlığın ortak noktasını söyler.
Önceliklendirme müşteriye bırakılır: "Başlıkların önceliklendirilmesi <marka>
ekibinin stratejik tercihleri ve öncelikleriyle güncellenebilir."

### Süreç, özet ve plan

**C26 Neler Yaptık / Devam Eden Çalışmalar**
`panels` iki kolon: `İletilen Çalışmalar` ve `Devam Eden Çalışmalar`. İsim cümlesi
listesi ("Kategori içerikleri", "Schema markup çalışmaları"). Efor kanıtı slaytıdır;
tarih verilmez, statü etiketi Türkçe ve şeffaf olur (Beklemede / Devam Ediyor /
Planlandı - "Blocked / In Progress" değil).

**C26b Çalışma etkisi kanıt slaytı**
Yapılan bir çalışmanın somut sonucu (yeni içeriğin AI Overview'da kaynak alınması +
sıralama ekran görüntüsü). `image` + `insights`. Bulgunun özü metinde de yazılır.

**C26c Q+1 / sonraki dönem iş maddeleri**
`panels`. Tarih veya gün/hafta verilmez; `Öncelik 1/2/3` veya `Faz 1/2/3`. Emir kipi
yok, isim-fiil yapısı ("Cannibalization yaşayan sayfaların optimize edilmesi" değil -
"fırsat kaybı yaşayan sayfaların gözden geçirilmesi").

**C27 Yönetici Özeti** - iki biçim:
1. *Başta, 5 maddelik tez slaytı*: her madde tek cümlelik iddia.
2. *Sonda, kırılımlı özet*: en çok click alan 5 query, artan ilk 5, kaybeden ilk 5,
   ardından `Stratejik Çıkarımlar` bloğu (4-5 paragraf, her biri bir bulguyu aksiyona
   bağlar).

### Etki analizi (M4)

**C30 Top 10 artış / Top 10 düşüş query tablosu**
Tek slaytta iki tablo yan yana (`grid: [50,50]`). Kolonlar:
`Query | <Önceki> | <Dönem> | Δ Click | Δ %`.
Üst satırda toplam: "Toplam click: 1.646 → 1.443 (Δ -203 | -%12.3)".
**Kapsam şerhi zorunlu:** "Top 1364 query üzerinden, long-tail kapsam dışı".
Altta kalın başlıklı tek paragraf yorum + `Sayfa Bazında MoM Top 5 Düşüş:` satırı
(URL → before→after (Δ) formatında, `·` ile ayrılmış).

**C31 Etki analizi genel özet**
Dört `kpi` kartı (GENEL / BRAND / NON-BRAND / BLOG), her kartta dönem sonu değer,
Δ mutlak + Δ%, `Before:` referans değeri. Altında `panels` ile `Anahtar Bulgular`:
4 madde, kalın başlık + açıklama.

**C31b Etki analizi segment detayı**
Query bazında ve sayfa bazında iki tablo (`Before | After | Δ Click | Δ %`), altında
kalın başlıklı yorum paragrafı.

**C32 Faz / hedef takibi**
Faz çizelgesi (geçmiş fazlar gerçekleşen, gelecek fazlar **forecast etiketli**) +
mevcut konum yüzdesi + kalan mesafe + numaralı öncelikli aksiyonlar.
**Zorunlu:** forecast rakamlarının forecast olduğu etiketle belirtilir.

**C33 Sorgu performansı: click + arama hacmi birleşik tablo**
Kolonlar: `Sorgu | Click <Ay1..Ay4> | ΔClick <A→B> | ΔClick <A→C> | Hacim <Ay1..Ay4> |
ΔHacim <A→B> | ΔHacim <A→C>`. İki bölüm: `▲ TOP 10 ARTIŞ` ve `▼ TOP 10 DÜŞÜŞ`,
sıralama kriteri başlıkta.
Altında üç madde yorum: talep yönü, trafik yönü, ikisinin ilişkisi.
Bu slayt tipi **trafik kaybının performanstan mı talepten mi geldiğini** ayırmak için
kullanılır; ajansın en güçlü savunma aracıdır.
Dipnot: "- : Keyword Planner'da ayrı veri yok" + yazım varyantlarının hangi ana terim
altında sayıldığı.

**C34 Sorgu grubu özeti**
İki küme × 4 metrik (Click, Impression, Arama Hacmi, Pozisyon) × aylık kolonlar +
Δ kolonları. Sonuç cümlesi: hangi kümede talep-trafik ayrışması var.

### Segment kırılımlı Search Console bölümü (Game+ tipi)

Marka talebi ile kategori talebini ayırmak gereken destelerde kullanılır. Bölüm
adı **"Google Search Console Metrikleri"** olur; "GSC" kısaltması başlıkta
kullanılmaz.

**C44 Segment tanımları** (bölümün ilk slaytı, veri gelmeden önce)
`panels` üç kolon: her segment için (a) nasıl ölçüldüğü, (b) regex ifadeleri
tırnak içinde birebir (`"gameplus" · "game plus" · "game+"`), (c) diğer
segmentlerle ilişkisi. Altında iki maddelik yorum: hangi ikisi birbirini
tamamlıyor, hangisi kesişiyor ve ayrımın neden kurulduğu.
**Zorunlu:** kesişen segment varsa "üç grubun toplamı toplam click'e eşit
değildir" cümlesi yazılır; tabloda Toplam satırı yalnızca tamamlayıcı
segmentlerin toplamıdır.
Anonim sorgu hacminin hangi segmente yazıldığı burada beyan edilir - query
filtresi uygulandığında anonim sorgular sonuç kümesinden düşer, bu yüzden
"toplam eksi brand" yöntemi anonim hacmi non-brand'e taşır.

**C45 Segment aylık serisi** (click ve impression için birer slayt)
`combo`: Toplam bar (gri) + Non-Brand çizgi (sol eksen), GFN ve Brand çizgi (sağ
eksen - ölçek farkı nedeniyle). Altında `heat: true` segment × ay matrisi
(`first_col_max: 0.10`), son satır Toplam ve `bold_rows: [-1]`.
Dipnot ikilisi: Toplam satırının neyi topladığı + ısı haritasının okunuşu.
Insight: sayısal açılış cümlesi + segment yönlerinin kontrastı.

**C46 Dönem karşılaştırması, pozisyonlu**
`Segment | Click | Impression | CTR | Pozisyon` × (cari ay, önceki ay, geçen yıl
aynı ay) veya Δ kolonlu düz biçim. Pozisyon impression ağırlıklı ortalamadır;
aritmetik ortalama kullanılmaz. Pozisyon satırlarında ısı haritası
`heat_invert_rows` ile ters çevrilir.

**C47 Öne çıkan hareketler** (sorgu ve sayfa için ayrı slaytlar)
Dört blok: `▲ Pozisyonu iyileşen` / `▼ Pozisyonu gerileyen` / `▲ Click artan` /
`▼ Click azalan`. Her tabloda segment etiketi (Brand / Non-Brand / GFN) kolon
olarak yer alır. Kapsam şerhi zorunlu: kaç sorgu/sayfa üzerinden bakıldığı ve
eşik (ör. "≥ 50 impression alan sorgular").

**C48 Haftalık geçiş grafiği** (SSR / migrasyon slaytının yanına)
`combo`, ISO hafta bazında click bar + pozisyon çizgi; geçiş haftası renk
kırılımıyla işaretlenir ve dipnotta tarihiyle yazılır. Simetrik pencere
(geçiş haftası hariç, önce/sonra eşit hafta sayısı) alt başlıkta beyan edilir.
AI Overview notu bu slaytta durur: CTR değişiminin bir bölümünün SERP
kompozisyonundan kaynaklanabileceği belirtilir.

**C49 İçerik kümesi performansı: GA4 + Search Console birlikte**
`Kategori | Session (cari ay) | Session MoM | Click (cari ay) | Click MoM`.
İki kaynak tek tabloda birleştirildiğinde kaynak notu ikisini de yazar ve
kolon başlıklarında metrik adı İngilizce kalır. Session ile click arasındaki
fark yorumlanır (organik dışı kanallar, filtre kapsamı).

**C50 Blog performansı: toplam ve organik**
`combo` ya da iki seri çizgi: toplam session + organik session. Aradaki fark
tek cümleyle açıklanır (hangi kanaldan geldiği). Kapsam dışı bırakılan hacim
varsa (tarama aracı artığı gibi) dipnotta sayısıyla beyan edilir.

**C51 Yapay zeka yanıtlarında marka görünürlüğü**
İki tablo: (a) `Sağlayıcı | Yanıt | Brand Mention | Mention oranı | Brand
Position`, (b) `En çok Citation alan kaynak | Citation | Farklı prompt | Tür`.
Metrik adları **orijinal haliyle** yazılır: Mention ve Citation çevrilmez,
"atıf" kullanılmaz. Dipnotta ikisinin farkı tanımlanır (Mention = yanıt
metninde anılma, Citation = kaynak olarak link verilmesi).

**C52 İzlenen promptlardan örnekler**
`Prompt | Sağlayıcı | Marka anılıyor mu | Anılma sırası`. Kaç prompt izlendiği
ve kaçının markalı olduğu dipnotta yazılır; boş hücre `-` ile geçilir.

**C53 Markadan nasıl bahsediliyor**
`panels` üç kolon: konumlandırma cümlesi, öne çıkan özellikler, tepki tonu
dağılımı. Alıntılar yanıt metinlerinden birebir alınır ve tırnak içinde
verilir; raporun kendi sesi nötr kalır. Etiket üretim oranı düşükse
(ör. yanıtların %20'si) bu oran dipnotta beyan edilir.

### Ek bölümler

**C35 Core Web Vitals** - LCP, INP, CLS dağılımları.
`Kaynak: CrUX Vis https://cruxvis.withgoogle.com/`

**C36 Ürün funnel performansı** (e-ticaret)
`EN ÇOK GÖRÜNTÜLENEN / EN ÇOK SEPETE EKLENEN / EN ÇOK SATILAN / EN YÜKSEK REVENUE`
dörtlüsü, her biri Top 5 (`panels` cols: 4 veya iki satırlı tablo).

**C36b Funnel conversion analizi**
Üç `panels`: `PDP OPTİMİZASYON ADAYLARI` (yüksek view, düşük conversion),
`CART ABANDONMENT`, `EN VERİMLİ ÜRÜNLER`. Eşikler slaytta yazılır (`<%0.3`,
`cart→purch <%2`, `≥5 satış`).

**C37 Kanal bazlı geçiş karşılaştırması** (M4 / migrasyon)
`Kanal | Sess before | Sess after | Sess Δ% | Rev before | Rev after | Rev Δ% |
Prch before | Prch after | Prch Δ%`. Üstte dört KPI kartı.

---

## Her slaytta olması gerekenler

Tip ne olursa olsun:

1. **Dönem beyanı** alt başlıkta, parantezle.
2. **Kapsam etiketi** (web-only / web+app, örneklem, Top N) - ilgiliyse.
3. **Yorum katmanı** - yorumsuz tablo bırakılmaz.
4. **Kaynak notu** - veri varsa zorunlu.
5. **Olay dipnotu** - dönem içinde geçiş/update varsa ilgili tüm slaytlarda.
