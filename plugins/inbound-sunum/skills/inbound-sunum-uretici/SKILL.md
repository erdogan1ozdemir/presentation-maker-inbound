---
name: inbound-sunum-uretici
description: Inbound ajans standardında SEO/GEO performans değerlendirme sunumu (PPTX) üretir - aylık, çeyreklik, yarıyıl ve etki/migrasyon analizi modlarında. Inbound Design System görselini, icerik-dili-rehberi dil standardını ve GSC/GA4/Keyword Planner/SEOmonitor/Ahrefs/AI visibility veri şemalarını uygular. Üretime başlamadan önce sunumun amacını, dönemini ve hangi verilerin dahil edileceğini sorar; elde olmayan export'ları hangi araçtan hangi ayları kapsayacak şekilde alınması gerektiğiyle birlikte net olarak ister. "Aylık SEO sunumu hazırla", "çeyreklik değerlendirme", "Q1/H1 sunumu", "marka adı + performans sunumu", "GSC verilerini sunumlaştır", "SEO deck", "değerlendirme sunumu", "migrasyon/SSR etkisi sunumu" gibi taleplerde mutlaka bu skill'i kullan. Kullanıcı PPTX demese bile bir markanın dönemsel SEO performansını sunuma dönüştürmek istiyorsa tetikle. Tüketiciye dönük blog içeriği, teknik PageSpeed denetimi veya tek sayfa SEO analizi bu skill'in kapsamı değildir.
---

# Inbound SEO/GEO Sunum Üreticisi

Bir marka, bir dönem ve bir veri paketi alır; marka ekibine sunulacak kalitede
PPTX üretir. Ayrı bir "iç sürüm" yoktur: her deste müşteriye gidecek varsayımıyla
hazırlanır.

## Üç bağımlılık, üç ayrı sorumluluk

| Katman | Nereden | Ne için |
|---|---|---|
| **Dil** | `icerik-dili-rehberi` skill'i | Her cümlenin tonu, kipi, rakam formatı |
| **Görsel** | `assets/design-system/` (bu skill'in içinde) | Renk, tipografi, slayt gramerleri |
| **Veri & yapı** | bu SKILL.md + `references/` | Hangi veri, hangi tablo, hangi slayt |

**İlk iş:** kendi skill listende `icerik-dili-rehberi` var mı diye bak. Varsa metin
yazmaya geçmeden onu çağır - bu skill onun yerine geçmez, sadece nerede
uygulanacağını söyler. Yoksa kur:

```bash
bash scripts/setup_deps.sh
```

Aynı script python-pptx ve Pillow'u da denetler. Pillow önemli: font ölçümü onun
üzerinden yapılıyor, olmadan taşma tespiti tahmine düşer ve geçmiş destelerin en
sık teslim hatası (metin taşması, tablonun dipnot üstüne binmesi) geri gelir.

---

## Akış

Altı fazın sırası önemli. Faz 1 tamamlanmadan Faz 4'e geçilmez; bu, "veri gelsin
diye slaytı uydurma rakamla doldurma" hatasını yapısal olarak imkansız kılar.

```
FAZ 0  Brief          -> ne, hangi dönem, hangi veri, hangi bölümler
FAZ 1  Veri kapısı    -> gelen veriyi tara, eksikleri iste, TEYİT AL
FAZ 2  Veri işleme    -> brand/non-brand, dönem eşleme, delta, sağlama
FAZ 3  Yorum          -> gözlem + çıkarım + öneri katmanları
FAZ 4  Deste          -> deck.json -> PPTX + HTML önizleme
FAZ 5  Denetim        -> qa_deck.py + slayt slayt görsel kontrol
FAZ 6  Teslim         -> dosya + chat'te FLAG listesi
```

---

## FAZ 0 - Brief

**Önce markanın hazır bir formatı var mı diye bak.** `reference/` altında
markaya özel bir klasör varsa (`reference/game-plus/` gibi) yapı yeniden
tasarlanmaz: o klasörün README'si okunur, üretici script dönem değerleriyle
çalıştırılır, bölüm sırası ve segment tanımları korunur. Brief yalnızca eksik
kalan kalemler için yapılır.

| Marka | Klasör | Not |
|---|---|---|
| Game+ / gameplus.com.tr | `reference/game-plus/` | 34 slayt, segment kırılımlı M1 varyantı. Brand/non-brand/GFN tanımı ve AI görünürlük bölümü markaya özgüdür |

Kullanıcı "aylık SEO sunumu hazırla" dediğinde hemen üretime girme. Aşağıdaki dört
bloğu sor. Cevapları biliyorsan tekrar sorma; bir kısmı zaten söylenmişse eksik
kalanı sor.

Soruları tek seferde, gruplu sor - dörtlü ayrı tur yapmak kullanıcıyı yorar.
Tam soru metinleri ve her kaynak için export talimatları:
**`references/veri-brief-ve-export.md`**

### 0.1. Sunum kimliği

- **Mod:** dönem ifadesinden otomatik seç, belirsizse sor.
  | Mod | Tetikleyen | Ana kıyas | Slayt |
  |---|---|---|---|
  | **M1 Aylık** | "Haziran 2026", "geçen ay" | MoM + YoY | 20-32 |
  | **M2 Çeyreklik** | "2026 Q1", "ilk çeyrek" | QoQ + Q-YoY | 30-55 |
  | **M3 Yarıyıl** | "H1 2026", "ilk 6 ay" | H-YoY (aylık ortalama) | 22-35 |
  | **M4 Etki analizi** | "SSR etkisi", "domain geçişi" | Simetrik N hafta | 15-25 |
- **Marka ve property'ler:** tek domain mi, çok property mi. Çok property'de her
  property kendi bölümünü, kendi ajandasını ve kendi "Neler Yaptık" slaytını alır;
  başa ortak yönetici özeti + genel trafik bölümü konur.
- **İş modeli:** e-ticaret / lead-gen / abonelik-servis. Bu seçim GA4 slaytlarının
  metrik setini belirler (revenue+transaction vs form success vs üyelik).
- **Kapsam kararı - baştan verilir:** organik session **web-only mu, web+app mi**.
  Bu karar tüm destede tek kalır. Gerçek bir destede slayt 5 web+app, slayt 8
  web-only olduğu için aynı metrik iki farklı değerle göründü. Karar ne olursa her
  veri tablosunun alt başlığında kapsam etiketi yazılır.

### 0.2. Hangi veri kaynakları dahil olacak

Kullanıcıya listeyi göster, seçmesini iste. Her kaynağın hangi bölümü açtığını
söyle - kullanıcı neyi kapattığını bilerek kapatsın:

| Kaynak | Açtığı bölüm | Erişim |
|---|---|---|
| Google Search Console | Click/impression/CTR/pozisyon, brand-non-brand, sayfa & query | `mcp__gsc__*` ile **canlı çekilebilir** (16 ay sınırı). Kurulu değilse Faz 1.0'daki kurulum önerilir - salt-okunur, tek seferlik |
| GA4 | Session, revenue, kanal, ürün funnel, AI referral | Genelde **kullanıcı export'u** |
| Keyword Planner | Arama hacmi: marka, marka+kategori, non-brand, rakip | Kullanıcı export'u |
| SEOmonitor | Visibility, Share of Clicks, AI Overview SoV, kategori visibility, kelime bazlı sıra | `mcp__*__seomonitor_*` ile **canlı çekilebilir** |
| Ahrefs | Sıralama dağılımı (ilk 3/10/100), backlink, DR, tam URL çözümleme | MCP varsa canlı |
| AI visibility izleme | Mention, citation, prompt coverage, sentiment | `mcp__inbound-db__*` |
| CrUX | LCP, INP, CLS | cruxvis.withgoogle.com |
| DataForSEO | Yedek SERP/hacim doğrulama | MCP |

**Arama hacmi verisi özel bir yer tutar.** Trafik düşüşü yorumlanırken hacim
verisi yoksa performans yorumu yapılamaz - düşüşün pazardan mı performanstan mı
geldiği ayrılamaz. Kullanıcı bu kaynağı kapatmak isterse sonucun ne olacağını
söyle: "arama hacmi olmadan talep-performans ayrıştırması yapılamaz, düşüş
yorumları bağlamsız kalır."

### 0.3. Export talimatları - neyi nasıl alacak

Elde olmayan her kaynak için **tek tek ve net** söyle. "GA4 verisi lazım" yeterli
değil; hangi rapor, hangi kırılım, hangi tarih aralığı, compare açık mı.

Örnek (M1, Haziran 2026, e-ticaret):

> GA4 - Traffic acquisition, "Session default channel group" kırılımı.
> Üç ayrı export: **Haziran 2026** · **Mayıs 2026** (MoM) · **Haziran 2025** (YoY).
> Compare özelliğini kullanma, her dönemi ayrı indir - compare'li export tek
> dosyada iki dönemi üst üste yazıyor ve dönem başlıkları karışıyor.
> CSV indir, dosya başındaki `# Property` ve `# Start date` satırlarını silme;
> hangi dosyanın hangi döneme ait olduğu oradan okunuyor.

Tam liste `references/veri-brief-ve-export.md`'de. Şunları sormayı atlama:

- **Geçmiş dönem arşivi var mı?** GSC 16 ay saklıyor. Geçen yılın aynı çeyreği
  API'den düşmüş olabilir; o dönemin kıyası için ajansın Excel arşivi tek kaynaktır.
- **Hangi aylar elde olmalı?** Trend grafikleri 15-16 aylık seri istiyor; tek ay
  export'u trend slaytını üretmez.
- **Önceki dönem destesi var mı?** Varsa metrik tanımları, brand kelime seti ve
  kategori eşlemesi oradan alınır; ayrım tanımı dönemler arası değişmemeli.

### 0.4. Opsiyonel bölümler - sor, varsayma

Bunlar veri değil, kullanıcının elindeki bilgi. Sorulmazsa deste eksik çıkar:

- **"Neler Yaptık / Devam Eden Çalışmalar"** eklenecek mi? Eklenecekse dönemde
  iletilen ve devam eden işlerin listesi istenir. Varsa **proje planı dokümanı**
  istenir - iş kalemleri oradan çıkarılır.
- **"Sonraki Dönem Planı"** eklenecek mi? Eklenecekse plan maddeleri istenir.
  Tarih/gün/hafta yazılmaz; `Öncelik 1/2/3` veya `Faz 1/2/3` kullanılır.
- **Yönetici Özeti** eklenecek mi? İki biçimi var: başta 5 maddelik tez slaytı,
  ya da sonda kırılımlı özet + stratejik çıkarımlar bloğu. Hangisi olacağı sorulur.
- **Çalışma etkisi kanıt slaytı** var mı? Yapılan bir çalışmanın somut sonucu
  (yeni içeriğin AI Overview'da kaynak alınması gibi) ekran görüntüsüyle konur.
- **Dönem içinde olay var mı?** Domain geçişi, SSR, site değişikliği, kampanya,
  Google update. Her biri ilgili tüm slaytlara yıldızlı dipnot üretir.
- **Rakip seti** hangi markalar, hangi sırayla. Sıra tüm destede sabit kalır.
- **Takip edilen kelime sayısı** kaç. Slayt metnine birebir girer, uydurulmaz.

Brief tamamlandığında kullanıcıya tek paragrafta özetle: mod, dönem, kapsam,
açık bölümler, senin çekeceğin veriler, onun göndereceği export'lar.

---

## FAZ 1 - Veri kapısı

### 1.0. Önce Search Console erişimini kontrol et

Brief biter bitmez, veri istemeden önce **GSC MCP sunucusu bağlı mı** diye bak:

```bash
claude mcp list
```

`gsc: ... ✔ Connected` görünüyorsa veriyi kendin çekersin; kullanıcıdan Search
Console export'u isteme - gereksiz iş yükü ve dönem karışması riski.

**Bağlı değilse ilk öneri canlı erişim kurulumudur, elle export değil.** Sırayı
tersine çevirme: kurulum tek seferliktir, sonrasında bütün destelerde veri
otomatik gelir. Kullanıcıya iki seçeneği şöyle sun:

> Search Console'a canlı erişim kurulu değil. İki yol var:
>
> **1. Tek seferlik erişim kurulumu (önerilen)** - yaklaşık 15 dakika sürüyor,
> bir kez yapılınca bütün sunumlarda veri doğrudan çekiliyor, bir daha export
> göndermenize gerek kalmıyor. Erişim **yalnızca okuma** iznidir: token site
> ekleyemez, sitemap gönderemez, ayar değiştiremez.
>
> **2. Elle export** - bu dönem için CSV'leri siz indirirsiniz. Bu yolda
> brand/non-brand ayrımı regex yerine elle yapılır ve anonim sorgular kümeden
> düştüğü için segment hacimleri eksik kalır.
>
> Hangisiyle ilerleyelim?

Kurulum seçilirse adımları **`references/gsc-erisim-kurulum.md`** dosyasından
sırayla anlat; kullanıcıyı adım adım yürüt, hepsini bir kerede yığma. Sunucu
skill'in içindedir (`scripts/gsc_mcp.py`) - harici bir depo klonlanmaz. Ekip
kullanımında **servis hesabı** yolu önerilir: tek JSON anahtarı, tarayıcı onayı
yok, erişim Search Console'dan tek e-postayla merkezden yönetilir. Kurulum
bittiğinde `claude mcp list` ile doğrulat ve property listesini çekerek markanın
property'sinin göründüğünü teyit et.

Elle export seçilirse `references/veri-brief-ve-export.md` talimatlarına geç ve
segment ölçümündeki kısıtı destenin ilgili dipnotuna yazacağını söyle.

Aynı kontrol diğer canlı kaynaklar için de geçerlidir (SEOmonitor, Ahrefs,
inbound-db): bağlıysa çek, değilse kapsamı kullanıcıyla konuş - bölümü sessizce
boş bırakma.

### 1.1. Gelen dosyaları tara

Veri geldiğinde klasörü tara:

```bash
python3 scripts/veri_tara.py ./veri --mod M1 --donem 2026-06 --model ecommerce
```

Script her dosyanın hangi kaynağa, hangi property'ye ve hangi döneme ait olduğunu
başlık satırlarından okur; mod ve iş modeline göre zorunlu/opsiyonel eksik listesi
üretir. Çıktısını kullanıcıyla paylaş.

Üç durumu ayrı ele al:

1. **Zorunlu eksik** → üretime geçme. Eksik export'u iste.
2. **Dönemi belirsiz mükerrer dosya** → script bunu ayrı uyarı olarak veriyor.
   Aynı ada sahip altı GSC export'unun hangisinin hangi dönemi kapsadığı dosyadan
   okunamıyorsa teyit almadan slayta bağlamak yanlış dönem etiketi üretir. Sor.
3. **Tanımlanamayan dosya** → ne olduğunu sor, tahmin etme.

**Eksik veri politikası - üç adım, istisnasız:**

1. Chat'ten bildir. Rapora "bu bölüm için ek veri toplanabilir" gibi doldurma
   cümlesi yazılmaz.
2. Manuel iste.
3. Gelmiyorsa ilgili bölümü destedan **komple çıkar** ve bunu chat'te ÖNEMLİ
   olarak ayrıca belirt. Placeholder metrik, boş bölüm, "sonraki aşamada
   eklenecek" vaadi bırakılmaz.

Hiçbir sayı uydurulmaz. Varsayım rakamı yazılmaz. Gerçek veri yoksa metrik çıkar.

---

## FAZ 2 - Veri işleme

Detaylı şemalar: **`references/tablo-semalari.md`** (T1-T14).
Bilinen tuzaklar: **`references/tuzaklar-ve-qa.md`**.

Bir sayıyı slayta koymadan önce yedi soruyu yanıtla: hangi property, hangi kanal,
hangi metrik, web-only mi web+app mi, hangi dönem ve karşılaştırma, hangi kaynak
dosya, revenue gerçekten track ediliyor mu (yoksa ₺0 mı).

**Brand / non-brand:** ayrım `brand_terms` regex'iyle query üzerinden yapılır.
Yanlış yazımlar brand'e dahil edilir. Üçüncü parti markalar non-brand'e yazılır ve
slaytta şeffaf belirtilir. Ayrım tanımı deste içinde değişmez; değiştiyse önceki
dönem yeniden hesaplanır. Total satırı ham toplamdır.

**Sağlama - bunlar tutmuyorsa devam etme:**
- Total ≥ Branded + Non-Branded, her tabloda
- Aynı metriğin farklı slaytlardaki değerleri çelişmiyor
- İmkansız yüzde yok (-%131 düşüş olamaz)
- Bin üzeri yüzdenin yanında mutlak değer var: `+%1362 (+395 click)`
- 0 tabanlı delta `+%100` değil **"yeni"** olarak işaretlendi
- Yuvarlanmış deck değerinden yüzde hesaplanmadı; ham veriden hesaplandı
- Forecast rakamları forecast olarak etiketlendi

**Alt-property destelerinde zorunlu kontrol:** URL regex'iyle filtrelenmiş GSC
görünümü page-level aggregation yapar, filtresiz görünüm property-level yapar.
Regex'li impression doğal olarak şişkin görünür ve düşüş abartılı okunur. Gerçek
örnekler: regex'li -%47.5 vs filtresiz -%7.9. Aynı query seti üzerinden filtresiz
export ile karşılaştır; fark anlamlıysa metodoloji slaytı ekle. Aynı dönemde click
artmışsa düşüş performans kaybı değil, aggregation etkisidir.

---

## FAZ 3 - Yorum

Dil kuralları `icerik-dili-rehberi`'nde. Buradaki kurallar sunuma özgü eklerdir.

**Her veri slaytında dört katman:**
1. **Ne oldu** - sayısal cümle, net kip: "-mıştır / -maktadır"
2. **Ne anlama geliyor** - ihtiyatlı kip: "işaret etmektedir / değerlendirilebilir"
3. Opsiyonel **ne yapılabilir** - öneri kipi: "değerlendirilebilir / önerilebilir"
4. **Kaynak notu**

Yorumsuz tablo bırakılmaz. `qa_deck.py` bunu hata olarak yakalar.

**Kontrast kalıbı ev imzasıdır.** Negatif metrik tek başına bırakılmaz, dayanıklı
metrikle yan yana verilir: "Session -%11 daralırken Revenue +%19 artmıştır."

**Talep-performans ayrıştırması** - en kritik yorum kuralı:

| Hacim | Click | Okuma |
|---|---|---|
| ↓ | ↓ benzer oranda | Sektörel talep daralması, performans kaybı değil |
| ↓ | ↓ daha az | Daralan pazarda pay korunuyor, pozitif okuma |
| → veya ↑ | ↓ | Performans veya SERP kompozisyonu kaynaklı, incelenmeli |

**Insight biçimi:** `➔` + tek boşluk, her insight tek okla. 1-2 cümle ideal,
üçüncü cümle sebep-sonuç için. Birinci cümle sayısal, ikinci cümle yorum.

**deck.json içinde vurgu işaretleme** - artış yeşil, düşüş kırmızı, anahtar terim
coral, rakam bold:

```
"Session {g:+%10.4} artarken revenue {r:-%42} düşmüştür; {c:düşük dönüşümlü}
 ziyaretçi ağırlığı {b:333K} hacminde değerlendirilebilir."
```

`{b:}` bold · `{g:}` yeşil · `{r:}` kırmızı · `{c:}` coral · `{n:}` soluk.

---

## FAZ 4 - Deste

Deste `deck.json` üzerinden bildirimsel olarak tanımlanır, iki çıktıya derlenir.
Şema referansı: **`references/deck-spec.md`**. Slayt tipi kataloğu ve her tip için
hazır blok kalıpları: **`references/slayt-katalogu.md`**.

```bash
python3 scripts/inbound_deck.py deck.json -o "Marka SEO Değerlendirme Haziran 2026.pptx"
python3 scripts/build_html_preview.py deck.json -o onizleme.html
```

Neden iki çıktı: Design System slaytı 1280×720 px, bu ölçü 96 DPI'da tam olarak
PPTX'in 13.333×7.5 inch'i. Aynı koordinat sistemi olduğu için HTML önizleme
üretilen destenin birebir görsel karşılığıdır. Ortamda LibreOffice yoksa PPTX
piksel olarak render edilemez; görsel kontrolün tek yolu bu önizlemedir.

Üretici, çizimden önce gerçek TTF üzerinden metin genişliği ölçer. Bunun üç sonucu
var: içerik slaytı başlığı tek satıra sığana kadar puntosu küçülür (Design System
kuralı: içerik başlığı sarmaz), tablo kolon genişlikleri içeriğe göre hesaplanır, ve
gövde alt sınırını aşan blok uyarı üretir.

**Bölüm ayracında kural terstir:** numeral ve başlık puntosu her ayraçta sabittir,
uzun başlık alt satıra kayar ve accent çizgiler çok satırlı bloğa göre açılır. Punto
küçültmek numeral boyutunu başlık uzunluğunun fonksiyonu yapardı ve destede farklı
boyutta numeraller üretirdi. Uyarı çıktıysa blok yüksekliğini düşür,
`font_pt` küçült veya slaytı ikiye böl - uyarıyı görmezden gelme, o blok PPTX'te
logo ve kaynak şeridinin üstüne biner.

**Grafikler düzenlenebilir vektör şekil olarak çizilir**, native PPTX chart
kullanılmaz: PowerPoint native bar chart'ta kategori eksenini "1, 2, 3" olarak
gösteriyor ve tasarım sistemi görünümü tam kontrol edilemiyor. Şekil olarak
çizilen grafik sunum içinden düzenlenebilir kalır ve HTML önizlemeyle birebir olur.

---

## FAZ 5 - Denetim

```bash
python3 scripts/qa_deck.py deck.json --pptx cikti.pptx
```

Üç katman tarar: yerleşim (taşma, başlık sarması), dil (em dash, emoji, emir kipi,
kesin vaat, keskin kelime, otomasyon aracı sızıntısı, iç kısıt ifadesi, terim
denetimi), rakam ve yapı (yüzde formatı, ondalık ayırıcı, imkansız yüzde, kaynak
notu eksikliği, yorumsuz tablo, ajanda-bölüm uyumu, marka yazım tutarlılığı).

HATA sınıfı bulgular düzeltilmeden teslim edilmez. UYARI sınıfı insan kararı
gerektirir; bilinçli istisna olabilir, ama gerekçesi olmalı.

**`--pptx` parametresi atlanmaz.** Yalnızca `deck.json` taranırsa üretilmiş
dosyadaki görünmez metin, font sızıntısı ve konuşmacı notu artığı yakalanmaz.
Desteler Google Slides'a aktarılarak kullanıldığı için bu katman zorunludur;
Google Slides'ta bozulan üretimlerin listesi tuzaklar 3.6g-3.6h'de.

Sonra **her slaytı önizlemede gözle kontrol et.** Script metin taşmasını ölçer ama
"grafik yanlış seriyi gösteriyor", "tablo başlığında ay etiketi mükerrer",
"kopyalanan slaytta eski başlık kalmış" sınıfı hataları görmez. Bunlar gerçek
destelerde fiilen yaşandı.

Önizleme tarayıcıda scroll sonrası boş render ediyorsa slaytı izole edip scroll-0'da
bak - bilinen bir paint sorunu:

```javascript
const s=[...document.querySelectorAll('.slide')], w=[...document.querySelectorAll('.wrap > *')];
window.__show=i=>{w.forEach(e=>e.style.display='none');s[i].style.display='';scrollTo(0,0)};
__show(5)
```

---

## FAZ 6 - Teslim

Dosyayla birlikte chat'te şunları ayrıca bildir - bunlar rapora yazılmaz:

- Doğrulanamayan veriler ve nedeni
- Destedan **çıkarılan bölümler** ve neden çıkarıldığı (ÖNEMLİ olarak işaretle)
- Örneklem, kısmi dönem, yaklaşık eşleşme gibi kapsam kısıtları
- Ölçüm kısıtları ("bu metrik iframe üzerinden ölçülemiyor" tipi)
- Sunacak kişinin sözlü açması gereken noktalar

Teslim öncesi son kontrol: konuşmacı notlarını tara. İç değerlendirme, araç kısıtı
ve ajans içi yorum notlarda kalmaz. `(Shared)`, "Blocked / In Progress" gibi iç
etiketler ve dosya adı konvansiyonları müşteri destesine sızmaz.

Çıktı klasörü yapısı ve gidişat kaydı: **`references/tuzaklar-ve-qa.md`**.

---

## Referans dosyaları

| Dosya | Ne zaman oku |
|---|---|
| `references/veri-brief-ve-export.md` | Faz 0-1. Soru setleri, kaynak bazlı export talimatları, dönem matrisi |
| `references/slayt-katalogu.md` | Faz 4. 37 slayt tipi: amaç, veri girdisi, deck.json kalıbı, insight örneği |
| `references/tablo-semalari.md` | Faz 2. T1-T14 kanonik tablo şemaları, kolon yapıları, format kuralları |
| `references/deck-spec.md` | Faz 4. deck.json tam şeması, blok tipleri, izgara sistemi |
| `references/design-system.md` | Faz 4. Token'lar, slayt izgarası, tipografi, hangi rengin nerede kullanıldığı |
| `references/gsc-erisim-kurulum.md` | Faz 1. Search Console canlı erişimi: servis hesabı ve OAuth kurulumu, salt-okunur kapsam, ekip içi paylaşım |
| `references/hacim-kaynagi-ve-fallback.md` | Faz 2. Arama hacmi kaynak sırası (SEOmonitor → Ahrefs → DataForSEO), etiketleme ve kaynak notu kuralları |
| `references/tuzaklar-ve-qa.md` | Faz 2 ve 5. Gerçek destelerde yaşanmış hatalar, teslim öncesi self-check |
| `assets/ornek/deck-ornek.json` | Çalışan 13 slaytlık örnek. Yeni deste kurarken buradan başla |
| `scripts/gsc_mcp.py` | Skill'in kendi Search Console MCP sunucusu - salt okunur, servis hesabı veya OAuth |
| `scripts/hacim_dfs.py` | Arama hacmi zincirinin DataForSEO halkası; yakın varyant birleşmesini de tespit eder |
| `reference/game-plus/` | Game+ için onaylanmış format: üretici script, veri modülleri, 34 slaytlık `deck.json` ve markaya özgü kurallar |
