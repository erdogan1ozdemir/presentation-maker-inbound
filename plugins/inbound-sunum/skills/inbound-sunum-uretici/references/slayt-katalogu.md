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

**Kaynak seçimi (aylık trend için bağlayıcı):** Keyword Planner hacimleri
kovalanmış döner (tek terim için yalnızca 74000 / 90500 / 110000 gibi basamaklar).
Ay bazında YoY karşılaştırması bu seriyle güvenilir kurulamaz. Aylık trend tablosu
için sürekli seri veren **Ahrefs `keywords-explorer-volume-history`** kullanılır
(keyword + country + tarih aralığı). Keyword Planner, marka + ürün terimlerinin
**göreli büyüklüğü** için ikinci blokta kullanılabilir; bu durumda iki kaynak tek
tabloda birleştirilmez, her blok kendi dipnotunu taşır ve aynı terim iki blokta
farklı değerle görünecekse çekirdek terim ikinci bloktan çıkarılır.

**C04b Marka hacmi + marka/ürün kırılımı (tek slayt)**
`grid: [52, 48]`. `table` (col `full`, başlık "Aylık Arama Hacmi") = yıl × ay
matrisi + YoY satırı; `table` (col 0, başlık "Marka + Ürün Terimleri") = keyword |
aylık ortalama hacim; `insights` (col 1).
Insight üçlüsü: dönem toplamı + YoY bandı → cari ay YoY → hacmin yoğunlaştığı
marka + ürün başlıkları.
Bu slayt branded impression daralmasının talep kaynaklı olup olmadığını
sınamak için GSC brand/non-brand slaytının hemen ardına konur.

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
