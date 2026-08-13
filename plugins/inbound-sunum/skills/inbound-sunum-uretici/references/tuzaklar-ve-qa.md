# Tuzaklar ve Teslim Denetimi

> Faz 2 ve Faz 5'te okunur. Buradaki her madde gerçek destelerde **fiilen yaşanmış**
> bir hatadır. Liste teorik bir risk envanteri değil, tekrarlanmaması gereken olaylar
> kaydı.

## İçindekiler

1. [Metodolojik tuzaklar](#1-metodolojik-tuzaklar)
2. [Ölçüm ve kapsam tuzakları](#2-ölçüm-ve-kapsam-tuzakları)
3. [Teknik üretim tuzakları](#3-teknik-üretim-tuzakları)
4. [Tespit edilmiş teslim hataları](#4-tespit-edilmiş-teslim-hataları)
5. [Teslim öncesi self-check](#5-teslim-öncesi-self-check)
6. [Çıktı klasörü yapısı](#6-çıktı-klasörü-yapısı)

---

## 1. Metodolojik tuzaklar

### 1.1. GSC impression aggregation (alt-property destelerinde zorunlu kontrol)

Bir alt-property URL regex'i ile filtrelendiğinde GSC **page-level aggregation**
yapar: aynı query için o property'nin her sayfası ayrı impression sayılır. Filtresiz
görünümde ise **property-level**: aynı query için tek impression.

Sonuç: regex'li görünümde impression toplamı doğal olarak şişkin görünür ve dönemler
arası düşüş abartılı okunur. Gerçek örnekler: bir alt property'de regex'li **-%47.5**
vs filtresiz **-%7.9**; başka birinde regex'li **-%67.7** vs filtresiz **-%11.6**.

**Kural:** alt-property destesinde impression düşüşü raporlanmadan önce aynı query
seti üzerinden filtresiz export ile karşılaştırılır. Fark anlamlıysa C17 + C17b
metodoloji slaytları eklenir.

**Doğrulayıcı sinyal:** aynı dönemde click artmışsa (bir örnekte +%7.3), düşüş
performans kaybı değil aggregation etkisidir.

**Ek faktör:** Google'ın resmi impression logging hatası bildirimi varsa kaynağa
atıfla verilir, iddia olarak değil.

### 1.2. Keyword Planner bucket etkisi

Hacimler bucket'lı gelir (27.1K, 33.1K, 40.5K). Bu yüzden değişimler %0, %18, %22,
%23 gibi tekrar eden değerlerde kümelenir. Normaldir; her rakip için ayrı sebep
aranmaz, tablo genel yön için okunur.

### 1.3. Ölçüm kapsamı değişikliğini büyüme sanmak

Gerçek olay: AI görünürlüğü 20 günde %3 → %31'e çıkmış görünüyordu. Üç platformda
eşzamanlı sıçrama organik olamaz; incelemede marka tespitine ana marka alias'ının
eklendiği görüldü (Temmuz'daki 367 anılmanın 318'i yeni alias'tan). Dönemsel kıyas
iptal edildi.

**Kural:** keskin sıçramada önce ölçüm setini ve tanımını kontrol et, sonra sonucu
yorumla.

### 1.3b. Share of Voice / endeks metriklerinde taban değişimi

Ahrefs Share of Voice gibi endeks metrikleri, takip edilen kelime havuzunun toplam
tıklama potansiyeline göre normalize edilir. Havuz değişirse SoV değerleri dönemler
arası karşılaştırılamaz hale gelir - ama bu değişim veride görünmez.

**Kontrol yöntemi:** aynı tarih kesitinde SoV ile tahmini trafik arasındaki oran tüm
domainlerde sabittir. Bu oranı iki dönem için hesapla:

- Oran dönemler arası yakınsa (±%10) SoV karşılaştırılabilir.
- Oran belirgin biçimde kaymışsa ve **tüm domainlerde aynı oranda** kaymışsa, bu
  organik bir değişim değil taban değişimidir.

Gerçek örnek (Flormar Temmuz 2026): MoM'da oran 515.8 → 544.5 (%5.6 fark, geçerli);
YoY'da 3899.8 → 544.5 (~7x, tüm domainlerde aynı). YoY SoV karşılaştırması iptal
edildi, YoY için karşılaştırılabilir kalan **tahmini organik trafik** kullanıldı ve
gerekçe dipnota yazıldı.

**Kural:** endeks metriklerinde dönemsel kıyas yapmadan önce taban kontrolü çalıştır.
Tüm aktörlerin aynı yönde ve aynı oranda hareket etmesi organik değildir.

### 1.3c. Aynı metriğin iki endpoint'te tekrarlanması

SEOmonitor'de `get_share_of_voice` (organic) ile `get_daily_share_of_clicks` aynı
değeri döndürüyor. Destede iki ayrı tablo olarak vermek aynı veriyi iki kez
göstermek olur; tek başlık altında verilir.

**Kural:** yeni bir kaynak kullanılırken iki endpoint'in aynı tarihteki değerleri
karşılaştırılır. Birebir aynıysa aynı metriktir, farklı isimlerle sunulmaz.

### 1.3d. Snapshot metriği dönemsel seri sanmak

SEOmonitor AI Search SoV, iki farklı tarih için sorulduğunda birebir aynı değerleri
döndürebiliyor (Flormar: 30 Haz ve 31 Tem çağrıları impression_score 188033,
508 mention, total 1164798 - tamamen aynı). Bu bir günlük seri değil snapshot.

**Kural:** dönemsel kıyas yapmadan önce iki tarihin değerleri karşılaştırılır.
Aynıysa yalnızca mevcut durum olarak sunulur ve dipnotta belirtilir.

### 1.4. Aynı isimli metriğin farklı formülü

Aracın "Source Visibility" metriği **yanıt bazlıydı** (kaynak gösterildiği yanıt ÷
toplam yanıt), elle kurulan hesap **atıf bazlıydı** (atıf ÷ toplam atıf). Fark 10 kat.

**Kural:** sunumda araç adıyla anılan her metrik, **aracın kendi formülüyle**
hesaplanır. Formülü doğrulamak için aracın CSV export'u istenip ters mühendislik
yapılır.

### 1.5. Filtre farkını dönem farkı sanmak

Araç ekranıyla tutmayan değerlerde önce **filtreleri** kontrol et (brand/non-brand,
segment hariç tutmaları), sonra dönemi. Gerçek bir projede uyumsuzluğun tamamı
brand/non-brand + segment filtresindendi.

### 1.6. Koşu günü ile koşu turu karışması

Otomatik ölçümler bir güne sığmayabilir; tur 1-3 güne yayılır. Gün bazlı kesit yanlış
trend gösterir. **Tur bazında grupla.**

### 1.7. Tek kayıttan metrik üretmek

"İlk 3 payı %100" değeri tek bir kayıttan geliyordu. **X/Y formatı** (pay ve payda
birlikte) bu hatayı görünür kılar; tablolarda ham sayı + yüzde birlikte verilir ya da
payda dipnotta yazılır.

### 1.8. Yuvarlanmış veriden yüzde hesaplama

Deck tablosundaki 1.2K / 3.3M değerlerinden hesaplanan değişim, ham veriden ±3 puan
sapabilir. Dönemsel yüzdeler **ham veriden** hesaplanır.

### 1.9. Kanal kayması ve organiğin tek başına yorumlanması

Organik düşüşü tek başına yorumlanmaz; toplam trafik ve diğer kanalların hareketiyle
birlikte verilir. Paid yoğunlaşması organik tıklamanın bir kısmını kaydırabilir; bu
**"yatırım artışı"** olarak ifade edilir, "talep artışı" olarak değil.

### 1.10. Google update dönemleri

Dönem içinde core/spam update varsa sıralama dalgalanması slaytında belirtilir:
"Mart ayı içerisinde Spam Update ve Core Update olmak üzere iki algoritma güncellemesi
yayına alınmıştır. Roll out esnasında ve sonraki üç haftalık süreçte sıralamalarda
dalgalanma görülebilmektedir."

### 1.11. Domain geçişi ve site değişikliği dönemleri

Geçiş dönemi kıyaslamaları **simetrik pencerelerle** yapılır, geçiş haftası/ayı analiz
dışı bırakılır ve bu yazılır. YoY karşılaştırmalarda geçiş ayının etkisi her ilgili
slaytta yıldızlı dipnotla hatırlatılır.

### 1.12. İki analitik kaynağı arasındaki seviye farkı

Marka kendi analitiğini kullanıyorsa aylık oran tablosu kurulur ve oranın istikrarlı
olup olmadığına bakılır:
- Session oranı dar bantta (4.7x-5.2x) → yüzdesel değişim kıyasları anlamlı.
- Transaction/Revenue oranı geniş bantta (5.0x-7.8x) → yalnızca **yön göstergesi**
  olarak okunur, mutlak kıyas yapılmaz.

Bu bulgu ayrı bir slayt olur ve dipnotta metodoloji farkları (session tanımı,
attribution, consent) belirtilir. Dramatik kıyas dili kullanılmaz.

---

## 2. Ölçüm ve kapsam tuzakları

### 2.1. web+app ile web-only karışması

Property/subproperty toplamı genelde **web + app birlikte**. "Web-only organik" ayrı
bir export gerektirir (Web platform filtresi); toplam × platform-payı ile **türetilemez**.

Gerçek olay: bir destede slayt 8 web-only iken slayt 5 web+app kaldı; aynı metrik iki
farklı değerle göründü. **Önlem: kapsam kararı Faz 0'da verilir, her tabloda kapsam
etiketi yazılır.**

### 2.2. Revenue bazı property'lerde ₺0

Bazı property'lerde gelir GA'da track edilmez (tüm kanallar 0). O zaman revenue
analizi **çıkarılır**, session odaklı gidilir, dipnotla belirtilir.

### 2.3. Organik landing raporunda "(not set)"

Büyük bir `(not set)` kovası app oturumlarını gösterir; app ağırlıklı organiği işaret
eder ve dipnotta belirtilir.

### 2.4. GSC 16 ay retention

Bugünden ~16 ay öncesine kadar. Tam "geçen yıl aynı dönem" karşılaştırması pencere
dışına taşabilir. İki çıkış: müşterinin/ajansın Excel arşivi, ya da pencere içinde
geçerli ve **eşit uzunlukta** bir önceki dönem seçmek (H1 2026 vs H2 2025) - ve bunu
slaytta yazmak.

### 2.5. Kapsam tutarlılık denetimi (AI ve çok kaynaklı bölümlerde)

Her tablo için üç soruyu yanıtla ve **tüm slaytlarda aynı cevabı ver**:
1. Hangi tarih aralığı?
2. Hangi soru/segment evreni (brand/non-brand, hariç tutulanlar)?
3. Payda ne (yanıt mı, atıf mı, soru mu)?

Bir slaytta bile farklıysa dipnot ile tablo çelişir. Gerçek bir denetimde bu şekilde
dört hata yakalandı.

### 2.6. GSC page URL'lerinin kesilmesi

GSC MCP sayfa URL'lerini **100 karakterde kesiyor** (hem `get_advanced_search_analytics`
hem `compare_search_periods`). Uzun ürün URL'lerinde slug'ın sonu ve barkod
kayboluyor; dahası birden fazla ürün varyantı aynı 100 karakterlik ön eki
paylaşabiliyor.

Kesilen URL'in eksik kısmını tamamlamak **uydurmadır** - varyantlar arasında
seçim yapılamaz. Doğru yol üç adım:

1. Ahrefs `site-explorer-top-pages` ile tam URL adaylarını çıkar
   (`select: "raw_url,sum_traffic"`, gerekiyorsa `where` ile slug filtresi).
2. Her aday için GSC'ye `filter_dimension: page`, `filter_operator: equals`,
   `filter_expression: <tam URL>` ile sor; `dimensions: device` kullanılırsa üç
   satırın toplamı o URL'in dönem toplamıdır.
3. Hangi adayın aradığın click değerini verdiği böyle kesinleşir.

Gerçek örnek: `sheer-up-...-ruj-pembe-8682536012` ön ekini dört farklı ürün
paylaşıyordu; nokta sorgu ile `...8682536012096/` doğrulandı (Tem 26: 1.023 click,
Tem 25: 1.801 click).

**Kural:** sayfa tablosunda kısaltılmış URL kullanılmaz. Tam URL doğrulanamıyorsa
o satır tablodan çıkarılır.

### 2.7. Visibility Score ile Share of Click'in karıştırılması

SEOmonitor'de bu iki metrik aynı kampanyadan gelir ama farklı şeyi ölçer:

| Metrik | Ne ölçer | Tipik büyüklük |
|---|---|---|
| Visibility Score | Takip edilen kelime setinde markanın görünürlük oranı | 40-90 |
| Share of Click | Aynı kelime setinde tahmini organik tıklamaların domainler arasındaki dağılımı | %1-25 |

Panelde görülen değer **Visibility**'dir. Aynı marka için Visibility 53 iken
Share of Click %8 olması çelişki değildir: ikinci metrik 800'ü aşan domain
arasında paylaşılan bir paydır.

Gerçek örnek: bir destede iki metrik "Rakip Görünürlük ve Share of Clicks"
başlığı altında yan yana verildi; marka panelde %53 görürken destede %7.63
yazdığı için ölçüm hatası şüphesi doğdu. Hata sayıda değil sunumdaydı.

**Kural:** iki metrik tek tabloda veya tek başlık altında birleştirilmez. Ayrı
tablolar, ayrı başlıklar ("Share of Click" / "Visibility Score"), her biri kendi
dönem tabanı dipnotuyla verilir (bkz. slayt kataloğu C20b).

### 2.8. SEOmonitor dönem çekiminde üç sınır

1. **Widget `visibility` alanı dönem ortalaması değildir.**
   `get_campaign_widgets` bir tarih aralığıyla çağrıldığında `visibility_source`
   alanı `daily_visibility_requested_range` yazsa da dönen değer **aralığın son
   günüdür**. Gerçek örnek: 1-31 Temmuz aralığı için mobil 53.3 döndü; günlük
   serinin ortalaması 56.1, son gün değeri 53.3. Ortalama gerekiyorsa
   `get_daily_group_visibility` ile günlük seri çekilip elde hesaplanır.
   Aynı şey `share_of_voice` için de geçerli: yanıtın `as_of.sov_date` alanı tek
   tarih verir, yani anlık kesittir.
2. **`get_daily_share_of_clicks` 15 günlük pencere sınırı uygular.**
   Aşıldığında HTTP 422 "The timeframe is restricted to 15 days" döner. Aylık
   seri iki çağrıda toplanır (1-15, 16-30). Karşılaştırılan dönemler eşit gün
   sayısıyla kurulur; 31. gün alınmayacaksa üç dönem de ilk 30 gün üzerinden
   hesaplanır.
3. **Günlük yanıt yalnızca o günün top 10'unu döndürür** (artı kampanya domaini,
   `sum_top_10` ve `others`). Listeye girmeyen rakip o gün **sıfır değil ölçüm
   dışıdır**; ortalama yalnızca değeri bulunan günler üzerinden alınır ve kapsam
   (kaç gün) dipnotta belirtilir. Sıfır sayılırsa küçük rakiplerin payı sistematik
   olarak olduğundan düşük çıkar.

**Rakip visibility çekimi:** `get_daily_group_visibility` + `domain=<rakip>`
kampanya domaini yerine o rakibin serisini verir; kampanyanın kendisi için
`group_id=0` kullanılır. Bu uç noktada 15 gün sınırı yoktur, tam ay çekilebilir;
ancak rakip × dönem sayısı arttıkça çekim maliyeti hızla büyür, tablo kapsamı
(kaç rakip, kaç dönem) baştan belirlenir.

**Kapsamı çekim maliyeti belirlemez.** Visibility rakip başına ayrı çağrı
gerektirdiği için tabloyu Share of Click'ten daha az domainle bırakmak kolaydır;
bu bir veri sınırı değil tercihtir ve iki tablo yan yana konduğunda okunurluğu
bozar. Aynı slayttaki iki tablo aynı domain setini taşır (bkz. slayt kataloğu
C20b). Domain sayısı azaltılacaksa **iki tabloda birlikte** azaltılır.

### 2.8b. Gösterilmeyen metrikler

Aşağıdaki alanlar veri kaynaklarından gelse bile **müşteri çıktısına girmez**:

| Alan | Neden |
|---|---|
| **Keyword difficulty / KD** | Araç bazlı ve araçlar arasında tutarsız bir skor; kelime önceliklendirmesi hacim, mevcut sıralama ve görünürlük açığı üzerinden kurulur. Skill'de de KD üretilmez, tablolarda kolon açılmaz. |
| CPC / avg. cpc / bütçe | Gerçek maliyet verisi olmadığı için maliyet dili kullanılmaz (bkz. Bölüm 10 - gerçek maliyet yoksa trafik bazlı yüzde). |
| Araç iç skorları (`opportunity.difficulty` vb.) | Yöntemi şeffaf olmayan türetilmiş skorlar sunulmaz; skorun dayandığı ham metrikler (hacim, sıra) verilir. |

`get_top_keywords`, `get_group_data` gibi uçlar bu alanları yanıt içinde
döndürür; tabloya taşınırken **elenir**.

### 2.9b. Brand/Non-Brand ayrımında anonim sorgu kaçağı

GSC'de query filtresi uygulandığında **anonim sorgular sonuç kümesinden düşer**
(düşük hacimli, kişi tespitine yol açabilecek sorgular). Dolayısıyla:

`contains "marka"` + `notContains "marka"` **≠** property toplamı

Gerçek örnek (Flormar, Tem 2026): total 63.6K click, `contains` 34.0K,
`notContains` 8.3K - aradaki **21.3K (%33.5)** anonim sorgudur.

**Yaşanmış hata:** branded = total − non-brand olarak hesaplanınca anonim
sorguların tamamı brand'e yazıldı; branded click 34.0K yerine 55.3K göründü ve
"click'in %87'si markalı" gibi yanlış bir çıkarım üretildi. Gerçek pay %53.5.

**Kural:** her iki segment de **ayrı ayrı ölçülür** (`contains` ve
`notContains`), fark **"Anonim sorgu" satırı** olarak tabloda gösterilir ve
Total satırı üçün toplamıdır. Segment payları bu üç satır birlikte okunur.
Anonim satırında pozisyon türetilemez, `-` bırakılır.

Pozisyon segment bazında da verilir: `dimensions=device` ile üç satır çekilir,
pozisyon **impression ağırlıklı** ortalanır (aritmetik ortalama yanlış sonuç
verir). Doğrulama: total için hesaplanan ağırlıklı pozisyon, filtresiz property
değeriyle örtüşmeli.

**İstisna - müşteride yerleşik bir hesap varsa.** Marka tarafında çalışan bir
dashboard/ETL zaten "non-brand = toplam − brand" kabulüyle raporluyorsa, sunum
o hesabı takip eder; iki kaynak arasında yüzde farkı çıkması müşteri için daha
maliyetlidir. Bu durumda:

- yöntem kaynak koddan (repo, ETL, sorgu tanımı) **doğrulanır**, sözlü
  aktarımla yetinilmez; regex ifadeleri birebir alınır,
- anonim hacmin non-brand'e yazıldığı **segment tanımları slaytında beyan
  edilir** (bkz. slayt kataloğu C44),
- brand ayrıca ölçülür ve iki yöntemin farkı en az bir kez kontrol edilir.

Kesişen üçüncü bir grup varsa (ör. GFN gibi bir 3. parti marka kümesi) bu grup
brand ve non-brand'in üzerine biner; **Toplam satırına dahil edilmez** ve
"üç grubun toplamı toplam click'e eşit değildir" cümlesi slayta yazılır.

**GSC regex desteği:** `get_advanced_search_analytics` araç açıklamasında yalnızca
contains/equals/notContains/notEquals listelense de `includingRegex` /
`excludingRegex` operatörleri çalışır. Çok yazımlı segmentler (`gameplus|game
plus|game\+`) tek çağrıda ölçülebilir; yazım varyantı başına ayrı çağrı
gerekmez.

### 2.9. Tek terimde Google Ads bant etkisi

Google Ads / Keyword Planner arama hacmini bant halinde döndürür. Bir kelime
setinde bu etki toplamda dengelenir, ancak **tek terimde** seri yalnızca birkaç
basamakta hareket eder. Gerçek örnek: `flormar` için 24 ayın tamamında sadece
üç değer görüldü (74.0K / 90.5K / 110.0K), dolayısıyla ay bazında YoY yalnızca
+%0.0, +%22.3 ve -%18.2 üretiyordu.

**Kural:** tek terimli marka hacmi slaytında ay bazında YoY satırı yazılmaz.
Aylık değerler matriste gösterilir, değişim **dönem toplamı** üzerinden verilir,
bandın varlığı dipnotta nötr dille belirtilir. Sürekli seri gerekiyorsa Ahrefs
`keywords-explorer-volume-history` çapraz kontrol olarak kullanılabilir; iki
kaynak hem seviye hem yön olarak ayrışabildiği için **tek metrik tek kaynak**
kuralı korunur, ikisi yan yana konmaz.

Ayrıca Google Ads verisi cari aya kadar gelmez: rapor dönemi Temmuz'ken tablo
Haziran'da bitebilir. Oluşmamış aylar `-` ile bırakılır ve dipnotta belirtilir;
tahmin yazılmaz.

---

## 3. Teknik üretim tuzakları

### 3.1. Canvas boyutu varsayma

Bu üretici 1280×720 px sahne = 13.333×7.5 inch kullanır. **Mevcut bir desteyi
düzenliyorsan önce `sldSz` oku.** Google Slides'ta düzenlenmiş dosyalar 10×5.625 inch'e
geçer; eski ajans desteleri 26.67×15 inch olabilir. Yanlış varsayım tüm içeriğin
köşede minik kalmasına yol açar.

### 3.2. Tablo yüksekliği `ext.cy` ile kısalmaz

PPTX'te gerçek tablo yüksekliği = satır sayısı × satır yüksekliği. Yerleşim buna göre
hesaplanır; `cy` değerini küçültmek tabloyu kısaltmaz, satırlar taşar ve alttaki
kutunun üstüne biner. Bu üretici satır yüksekliklerini ölçüp toplar - `--check`
uyarısını ciddiye al.

### 3.3. Native PPTX bar chart

PowerPoint kategori eksenini "1, 2, 3" gösteriyor. Bu yüzden grafikler düzenlenebilir
vektör şekil olarak çizilir.

### 3.4. Mevcut desteyi düzenlerken

Kullanıcı desteyi Google Slides'ta düzenlemişse dosya build pipeline'ından diverge
eder. **Her turda onun son export'unu baz al**; ikisini paralel yürütmek iki farklı
gerçeklik üretir. Tek kaynak üzerinden ilerlemek için baştan anlaş.

Slayt eklerken: `add_slide` sona ekler, `slides._sldIdLst` üzerinde reorder ile doğru
yere taşınır; mirasla gelen placeholder'lar silinir; `p:bg` ile zemin verilir.
Kopyalanan rels'ten `notesSlide` referansı silinir - aksi halde iki slayt aynı nota
bağlanır ve doğrulayıcı hata verir.

### 3.5. UTF-8 düzeltmesi

Türkçe karakterler doğrudan temiz UTF-8 yazılır. `sed`/`perl` ile UTF-8 bilinçsiz
düzeltme yapılmaz - `Â·` tipi çift kodlama üretir. Düzeltme Python ile yapılır.

### 3.6. HTML önizleme ile PPTX arasında sessiz ayrışma

İki çıktı aynı `deck.json`'dan üretiliyor ama farklı yerleşim motorları kullanıyor:
PPTX mutlak konumlandırma, HTML akış. Ayrışma yaşanmış üç nokta ve çözümleri:

- **Tablo satır yüksekliği.** HTML satır yüksekliğini padding + içerikten türetir,
  PPTX hesaplanan sabit değeri kullanır. 9 satırlı bir tabloda ~45px fark ölçüldü.
  Çözüm: `table_layout()` tek kaynak, HTML `<colgroup>` ve satır `height` ile
  aynı geometriyi uygular.
- **Ayraç numerali.** HTML sabit CSS punto, PPTX hesaplanan punto kullanıyordu.
  Çözüm: `separator_layout()` tek kaynak; satır kırılması da Python'da yapılıp
  HTML'e `<br>` olarak veriliyor (tarayıcının sarma davranışına bırakılmıyor).
- **Metin sarma noktası.** PIL'in advance genişlikleri ile tarayıcı yerleşimi
  arasında kerning kaynaklı küçük fark var; tarayıcı bazen bir kelime önce sarar.
  Çözüm: `WRAP_SAFETY = 0.985` ile ölçüm muhafazakâr tarafa çekildi, üretici
  tarayıcıdan önce uyarıyor.

- **Sayı biçimleyicisinin üç kopyası.** K/M kısaltmasını yapan fonksiyon üç yerde
  ayrı ayrı duruyordu: `inbound_deck._fmt_val`, `inbound_deck._fmt_axis` (bar
  bloğu) ve `build_html_preview._fmt`. Üçünde de `.replace(".0K", "K")` vardı ve
  bu, aynı seride **"665K" ile "711.7K" karışımı** üretiyordu (665000 tam sayıya
  denk geldiği için ondalığı düşüyor). Rehber tek rakam formatı istiyor
  (Bölüm 6.1). Çözüm: `_fmt_val` tek kaynak, diğer ikisi ona delege ediyor ve
  K/M her zaman tek ondalıklı basılıyor. Bir biçim değişikliği yapıldığında
  `grep -n '\.0K\|\.0M' scripts/*.py` ile kopya kalmadığı doğrulanır.

**Kural:** yeni bir blok tipi eklenirken geometri hesabı **ve sayı biçimlemesi**
tek fonksiyonda tutulur ve her iki renderer onu çağırır. Önizlemedeki taşma
işaretleyicisi ile üreticinin uyarısı aynı slaytlarda çıkmıyorsa ayrışma vardır.
Rakam biçimi ayrışması taşma uyarısı üretmez, bu yüzden teslim öncesi aynı değer
iki çıktıda karşılaştırılır (`grep` ile PPTX XML ve HTML üzerinde).

### 3.6b. Çakışma koruması (üç katman)

Taşma denetimi bir bloğun gövde alt sınırını aşmasını yakalar; **bir etiketin
başka bir etiketin üzerine binmesini yakalamaz.** Gerçek örnek: bar grafiğinde
`h` küçültülünce en yüksek barın değer etiketi legend satırının üzerine bindi
(17px örtüşme) ve hiçbir uyarı çıkmadı. Üç katman eklendi:

1. **Bant hesabı tek kaynak.** Bar bloğunda dikey bantlar sabitlerle tanımlıdır:
   `CB_BAR_LEGEND_H` (20) + `CB_VAL_H` (16, değer etiketi) + `CB_CAT_H` (20,
   kategori etiketi). Plot alanı `h` eksi bu üç bant. Önizleme aynı sabitleri
   kullanır ve `.chart` bloğuna `margin-top: CB_VAL_H` verir - bu bant
   ayrılmazsa yüksek barın etiketi kutunun dışına, legend üzerine taşar.
2. **Python tarafı ölçüm** (`--check`, tarayıcısız çalışır):
   - Plot yüksekliği 90px altına düşerse `GRAFIK` uyarısı: değer etiketleri
     sıkışıyor, gereken minimum `h` bildirilir.
   - `_label_fit_check` kategori ve değer etiketlerinin genişliğini slot
     genişliğiyle karşılaştırır. Etiketler `wrap=False` çizildiği için slot'a
     sığmayan etiket sessizce komşusunun üzerine taşar; `CAKISMA` uyarısı çıkar.
3. **Önizleme çakışma tarayıcısı** (son savunma hattı). Gömülü
   `inboundClashCheck()` her slaytta veri taşıyan öğeleri (`.vl`, `.cat`,
   `.lg span`, `.kpi-v`, `.ins li`, `.dt td/th`, eksen etiketleri, pill) ikili
   karşılaştırır; ata-torun çiftleri ve 2px altı kenar temasları hariç her
   kesişimi coral çerçeveyle işaretler ve slayta "N etiket cakismasi" rozeti
   basar. Teslim öncesi önizlemede rozet aranır; `document.querySelectorAll('.clash').length`
   sıfır olmalıdır.

**Kural:** yeni bir grafik veya blok tipi eklenirken (a) dikey bantlar sabit
olarak tanımlanır ve iki renderer aynı sabiti kullanır, (b) `wrap=False` çizilen
her etiket için genişlik kontrolü eklenir, (c) önizlemede çakışma rozeti
kontrol edilir.

### 3.6c. Sessizce boş çizilen grafik

`combo` bloğunda seri-eksen bağlantısı **`axis: "left"` / `axis: "right"`** ile
kurulur. Kod eşleşmeyen değeri sessizce eler (`if s_.get("axis","left") != side:
continue`), dolayısıyla `"l"` / `"r"` gibi kısaltma yazıldığında:

- hiçbir seri hiçbir eksene bağlanmaz,
- grafik yalnızca ızgara ve kategori etiketleriyle çizilir,
- **hiçbir denetimden uyarı çıkmaz** - blok yüksekliği doğrudur, taşma yoktur,
  çakışma yoktur, QA dil denetimi de bir şey görmez.

Gerçek olay: Enerjisa Üretim destesinde iki combo grafiği bu şekilde boş
üretildi; hata ancak önizleme gözle açıldığında fark edildi.

**Eklenen koruma** (`block_combo`, `--check` ile çalışır):
1. Her seri için `axis` değeri `left`/`right` dışındaysa uyarı, seri adıyla.
2. Serinin `data` dizisi boşsa ya da tamamı `None` ise uyarı.
3. Hiçbir seri eksene bağlanmadıysa "grafik yalnızca ızgara olarak çizilecek"
   uyarısı.

**Kural:** görsel çıktı üreten her blok için "hiç mark çizilmedi" durumu bir
uyarıya bağlanır. Geometri doğrulaması bir bloğun *yerini* denetler, *içeriğinin
oluştuğunu* denetlemez; ikisi ayrı kontrollerdir. Yeni bir grafik tipi eklerken
seri sayısı, veri uzunluğu ve eksen bağlantısı doğrulanır.

Teslim öncesi refleks: önizleme açılıp **her grafik gözle görülür**. Tablo ve
metin bloklarında ölçüm denetimi yeterli, grafiklerde değildir.

### 3.6d. Boş çizilen not, panel ve metin bloğu (alan adı sapması)

Her blok tipinin içerik alanı sabittir ve **takma ad kabul etmez**:

| Blok | İçeriğin yazıldığı alan |
|---|---|
| `note` | `text` |
| `panels` | `items[].lines` |
| `text` | `paras` (veya `text`) |
| `insights` | `items` |
| `kpi` | `cards[].value` |
| `table` | `rows` |
| `bar` / `line` / `combo` | `cats` + `series` |
| `image` | `src` |

`body` / `content` / `desc` / `metin` / `govde` / `icerik` yazıldığında blok
çerçevesi, etiketi ve dolgusu çizilir, **içi boş kalır**. Geometri denetimi
temiz görünür: blok yerindedir, taşma yoktur.

Gerçek olay: üç destede birden "KRİTİK TESPİT" kutusu ve panel maddeleri boş
teslim edildi (`note` bloğuna `body`, `panels` maddelerine `body` yazılmıştı).

**Eklenen koruma** (`blok_icerik_denetimi`, her blok için `--check`'te çalışır):
1. Zorunlu içerik alanı yoksa ya da boşsa uyarı - blok tipi ve beklenen alan adı
   yazılır.
2. Blokta takma ad (`body`, `content`, `desc`, …) varsa "alan adı sapması"
   uyarısı; doğru ad önerilir.
3. `panels` ve `kpi` için öğe düzeyinde de denetlenir (`lines`, `value`).

**Kural:** çerçevesi çizilen her blok içerik denetiminden geçer. Geometri
denetimi *nerede*, içerik denetimi *ne* sorusuna bakar. Yeni blok tipi eklenirken
`BLOKICERIK` sözlüğüne satır eklenmesi zorunludur.

### 3.6e. Tam genişlik blok yığını alt sınırı aşarsa

İçerik alanının alt sınırı 589px'dir. Üst üste binen tam genişlik blokları
(tablo + tablo + insights gibi) bu sınırı birkaç piksel aşabilir. Sıra:

1. Dipnot slayta ait mi kontrol edilir - başka slaytın dipnotu buraya
   düşmüşse taşınır (bir dipnot satırı ~14px).
2. Tablo satır yüksekliği düşürülür: `dict({...}, **{**T, "row_h": 17,
   "head_h": 21})` - 9 satırlık bir yığında ~25px kazandırır.
3. Blok arası `mt` 10 → 6 çekilir.
4. Grafik yüksekliği (`h`) 182 → 158 düşürülür.
5. Insight metni kısaltılır - **yorum katmanı kaldırılmaz**, sayısal açılış
   cümlesi korunarak ikinci cümle sadeleştirilir.

Font küçültme son çaredir; 10 pt'nin altına inilmez.

### 3.7. Önizleme self-check'i font yerleşmeden ölçüm alırsa

Gömülü self-check `document.fonts.ready` beklemeden çalışırsa fallback font
yüksekliğiyle ölçüm alıp yanlış taşma alarmı üretir. Beklemeyle çözüldü; kendi
ölçümünü yaparken de fonts.ready + iki `requestAnimationFrame` bekle.

### 3.8. Scratchpad kalıcı değil

Ara dosyalar (script, unpacked klasör) silinebilir. Yeniden kullanılacak kod ve
`deck.json` **proje klasörüne** kopyalanır.

---

## 4. Tespit edilmiş teslim hataları

Gerçek destelerde yakalanmış hata sınıfları. `qa_deck.py` bunların çoğunu tarar; yine
de son okuma yapılır.

**Rakam ve format**
1. Yüzde formatı karışıklığı: aynı destede `+%197`, `+248.1%`, `%-3,3`.
2. Ondalık ayırıcı karışıklığı: metinde nokta, tabloda virgül.
3. İmkansız rakam: `-%131 düşüş`; çelişen hedef rakamları (500K vs 650K); kapakta
   yanlış yıl.
4. Aynı slaytta "MoM kıyaslandığında %10.4 düşüş" yazarken tabloda `+%10.4` artış
   olması (yön ters yazımı).
5. Kaynaksız çarpıcı istatistik: "AI Overview çıktığında 1. sıra CTR'ı %34 düşüyor".
6. `+%100` yazılması (0 tabanlı delta - "yeni" olmalı).

**Yapı**
7. Ajanda-bölüm uyumsuzluğu: ajandada 3 bölüm, destede 4 bölüm; "02" numarasının iki
   kez kullanılması.
8. Silinmemiş `SECTION TITLE` placeholder'ı.
9. Yarım cümle: "… ile " diye biten cümle; kopyalanan slaytta kalan eski başlık;
   çift slayt.
10. Q1 verisinin Q2 başlığı altında durması; tablo başlığında mükerrer ay etiketi
    (Jan/Feb/Mar iki kez).
11. Grafiğin yanlış seriyi göstermesi.

**Denetleyici yanlış pozitifleri (gerçek kullanımda çıktı)**
Bunlar destede hata değil; `qa_deck.py` içinde muafiyetleri tanımlı:
- Marka adının **tablo hücrelerinde** küçük harfle geçmesi (query metni
  "flormar maskara", domain "flormar.com.tr") yazım varyantı değildir.
- Marka adının **tırnak içinde** geçmesi literal filtre ifadesidir
  ("query içinde \"flormar\" geçmesine göre").
- "zayıflama / zayıflamıştır" rehberin nötr teknik fiil sözlüğünde yer alır;
  yasak olan sıfat kullanımıdır ("zayıf halka").

**Dil**
12. Register kayması: resmi "-mektedir" akışı içinde tek slaytta konuşma dili
    ("çiziyor", "diyebiliriz").
13. Marka/araç adı yazım tutarsızlığı: VitrA/Vitra, SEOmonitor/SEOMonitor,
    Non-branded/Nonbranded.
14. Typo yoğunluğu: "sııralama", "avantaklı", "araştrması", "sodlaki", "kıyasalamada",
    "3th party".
15. Hal eki - edilgen çatı uyumsuzluğu: "kodları kaldırılabilir" → "kodlar
    kaldırılabilir".
16. Mantık ters dönmesi: "kaymalardan dolayı site açılış hızı artmaktadır" (azalma
    kastedilmiş). Kopyala-yapıştır sonrası anlam kontrolü.
17. Dönüşümlü terim kullanımı: aynı destede "gösterim/Impression", "oturum/session"
    karışık.
18. Çift boşluk salgını: "968  keyword", "Audit  |".
19. Sembol enflasyonu: `➔ → ⇒ ➜ ⬆` karışık kullanımı.

**Sızıntı**
20. Konuşmacı notunda iç değerlendirme kalması.
21. İç etiket sızıntısı: "Blocked / In Progress / Not Started"; slayt içi linklerde
    "(Shared) … // Inbound" gibi iç adlandırmalar.
22. Görünmez karakter: ZWNBSP bulaşması ("JavaS criptHTML/CSS"), yapışık metin blokları.
23. Mojibake: Ã, Ä±, Â·.

---

## 5. Teslim öncesi self-check

`icerik-dili-rehberi`'nin kendi self-check listesi ayrıca çalıştırılır. Bu liste
sunuma özgü kalemleri kapsar.

```bash
python3 scripts/qa_deck.py deck.json --pptx cikti.pptx
```

**Veri tutarlılığı**
- [ ] Total ≥ Branded + Non-Branded, her tabloda
- [ ] Dönem tanımları destede tek biçim (hepsi "2026 Q1")
- [ ] Aynı metriğin farklı slaytlardaki değerleri çelişmiyor
- [ ] İmkansız yüzde yok
- [ ] Bin üzeri yüzdenin yanında mutlak değer var
- [ ] 0 tabanlı deltalar "yeni" olarak işaretlendi
- [ ] Forecast rakamları forecast olarak etiketlendi
- [ ] Kapsam şerhleri (Top N query, long-tail hariç, örneklem) yazıldı
- [ ] Yüzdeler ham veriden hesaplandı, yuvarlanmış deck değerinden değil

**Yapı**
- [ ] Ajandadaki bölüm sayısı = destedeki ayraç sayısı
- [ ] Bölüm numaraları tekrarlanmıyor
- [ ] Placeholder metin kalmadı
- [ ] Her veri slaytında kaynak notu var, format "Kaynak:"
- [ ] Olay dipnotları ilgili tüm slaytlarda var
- [ ] Her tabloda yorum katmanı var
- [ ] Kapanış bir sonraki adımla bitiyor
- [ ] Konuşmacı notları tarandı, iç yorum kalmadı
- [ ] `(Shared)` gibi iç dosya adı sızıntısı yok

**Dil**
- [ ] Em dash yok
- [ ] Emoji yok (`✓ ▲ ↑ ↓ ➔` serbest)
- [ ] Emir kipi yok, kesin vaat yok
- [ ] Yüzde formatı tek: `+%X`, ondalık nokta - tabloda da aynı
- [ ] Otomasyon aracı adı sızmadı
- [ ] İç kısıt ifadesi ("veri çekilemedi", "ölçülemiyor") rapora yazılmadı
- [ ] Terimler tekilleştirildi
- [ ] Marka yazımı tüm destede tek biçim

**Görsel**
- [ ] `--check` uyarısı sıfır (taşma, sağ kenar aşımı)
- [ ] HTML önizlemede her slayt gözle kontrol edildi
- [ ] Önizlemede kırmızı kesikli taşma işareti yok
- [ ] Hiçbir grafikte "yalnızca ızgara" durumu yok - her seri çizildi
- [ ] Not, panel ve metin bloklarının içi dolu (alan adı `text` / `lines`)
- [ ] Çakışma denetimi çalıştırıldı, `.clash` işareti sıfır
- [ ] Tablo hücreleri kesilmemiş, grafik etiketleri okunur
- [ ] Ekran görüntüsü kullanılan yerde bulgunun özü metinde de var
- [ ] Yalnızca Bricolage Grotesque ve Outfit kullanıldı

**Teslim**
- [ ] Font klasörü deste ile birlikte iletildi
- [ ] FLAG listesi chat'e yazıldı (eksik veri, çıkarılan bölüm, kapsam kısıtı)
- [ ] Gidişat kaydı güncellendi

---

## 6. Çıktı klasörü yapısı

```
<marka>-seo-sunum-<donem>/
├── <Marka> SEO Değerlendirme <Dönem>.pptx     # ana çıktı
├── onizleme.html                              # görsel doğrulama, kullanıcıya da gider
├── deck.json                                  # deste tanımı, sonraki dönemde yeniden kullanılır
├── fonts/                                     # Bricolage + Outfit, teslimle birlikte
├── veri/                                      # ham export'lar, izlenebilirlik için
│   ├── gsc_date_15m.csv
│   ├── gsc_query_<p0>_<p1>.csv
│   ├── gsc_page_<p0>_<p1>.csv
│   ├── gsc_regex_vs_unfiltered.csv            # alt-property varsa
│   ├── ga4_kanal_<donem>.csv
│   ├── ga4_organik_15m.csv
│   ├── ga4_revenue.csv / ga4_items.csv
│   ├── kwp_brand.csv / kwp_brand_category.csv / kwp_nonbrand.csv / kwp_competitors.csv
│   ├── seomonitor_*.csv
│   └── ahrefs_rank_distribution.csv
├── tablolar/                                  # T1-T14 işlenmiş hali
└── notlar/
    ├── eksik-veri.md                          # chat'te bildirilen maddeler
    └── ic-kisitlar.md                          # rapora yazılmayan, sözlü iletilecek
```

`deck.json` saklanması önemli: sonraki dönemin destesi sıfırdan kurulmaz, bu dosyanın
rakamları güncellenir. Metrik tanımları, brand kelime seti ve kategori eşlemesi
dönemler arası aynı kalmalı.

**Gidişat kaydı:** çalışma klasörünün kökündeki `<proje-adi>-claude.md` dosyasına
tarihli madde eklenir - ne istendi, ne yapıldı.
