# Inbound Design System - Sunum Katmanı

> Faz 4'te okunur. Token'ların tam listesi `assets/design-system/colors_and_type.css`
> içinde; buradaki kurallar o token'ların **sunumda nerede kullanıldığını** anlatır.
> Tam tasarım sistemi brief'i: `assets/design-system/DESIGN-SYSTEM-README.md`.

Üretici bu kuralları koda gömülü uygular; elle slayt kurarken veya yeni blok tipi
eklerken buraya bakılır.

---

## Sahne ve ızgara

| Ölçü | Değer | Not |
|---|---|---|
| Sahne | 1280 × 720 px | 96 DPI'da 13.333 × 7.5 inch = standart PPTX 16:9 |
| EMU dönüşümü | 1 px = 9525 EMU | HTML ve PPTX aynı koordinatta |
| İçerik yan boşluk | 60 px | Sol ve sağ |
| Breadcrumb | x 48, y 28 | 12 px, coral |
| Başlık üst | y 88 | 36 px (27 pt) Bricolage Bold |
| Gövde alt sınırı | y 636 | Altında logo + kaynak şeridi |
| Logo | x 44, y 652, 36 × 36 | Her içerik slaytında |
| Kaynak pill | x 100, y 658 | Coral zemin, beyaz kalın 11 px |

### Punto ölçeği ve 12 pt tavanı

| Rol | Punto | Nerede |
|---|---|---|
| Slayt başlığı (h1) | 27 | İçerik slaytı başlığı |
| Blok başlığı (h4) | 13.5 | Tablo/grafik blok başlığı |
| Gövde (body) | **12** | Insight, metin bloğu, not kutusu gövdesi |
| İkincil (sm) | 11 | Panel maddeleri |
| Tablo gövdesi | 10.5 | |
| Tablo başlığı (xs) | 10 | KPI delta, insight blok başlığı |
| Dipnot (micro) | 9 | Grafik etiketi, KPI etiketi |
| Kaynak pill | 8.5 | |

**12 pt gövde metni için tavandır** (`BODY_PT_MAX`); üstü slaytta fazla büyük duruyor.
Buna karşılık boş alan kalacaksa yazıyı büyütmek tercih edilir - küçük punto ile
boşluk bırakmak okunabilirliği düşürüyor. Blok başlıkları ve slayt başlıkları bu
tavanın dışındadır; onlar başlıktır, gövde değil.

---

## Renk

### Marka çıpaları

| Token | Hex | Kullanım |
|---|---|---|
| `coral` | `#FF7B52` | Vurgu, CTA, kapak zemini, kaynak pill, accent çizgi, breadcrumb |
| `coral_tint` | `#FFE3D8` | Tablo vurgu satırı (kendi marka), yumuşak zemin |
| `coral_deep` | `#E85F36` | Not kutusu etiketi |
| `teal` | `#10332F` | Gövde metni, başlık, tablo başlık zemini, bölüm ayracı zemini |
| `teal_soft` | `#1A4238` | Bölüm ayracındaki soluk numeral |
| `mint` | `#E8F5E9` | Not / yöntem kutusu zemini |

Yeni hue icat edilmez. İhtiyaç varsa data-viz token'ları üzerinden genişletilir.

### Veri renkleri

| Token | Hex | Kullanım |
|---|---|---|
| `green` / `green_wash` | `#2E7D32` / `#C8E6C9` | Artış, pozitif delta metni / hücre zemini |
| `red` / `red_wash` | `#D32F2F` / `#FFCDD2` | Düşüş, negatif delta metni / hücre zemini |
| `gold` | `#F5A623` | Grafikte **önceki** dönem barı |
| `gray_bar` | `#4A4A4A` | Grafikte **güncel** dönem barı |
| `line` / `line_soft` | `#E0E0E0` / `#F0EDE8` | Tablo çizgileri / grafik ızgarası |
| `ink2` / `ink3` | `#4A4A4A` / `#8A8A8A` | İkincil metin / dipnot ve üçüncül |

Insight vurgu renkleri (artış yeşil, düşüş kırmızı, anahtar terim coral) marka
paletiyle birebir örtüşür - ayrı bir vurgu paleti yoktur.

### Tablo renk standardı

Bu bir **deck** üreticisi; deck ve HTML rapor tabloları pazarlama yüzeyidir ve
marka teal başlığını taşır:

- Başlık satırı: `teal` zemin + beyaz kalın Bricolage
- Kenarlık: `line` `#E0E0E0`, satır başına üst kenarlık
- Delta hücresi: yeşil/kırmızı metin **+ wash zemin**
- Vurgu satırı: `coral_tint`
- Toplam satırı: renklendirilmez, **kalın** yapılır

Excel çıktılarında bu standart farklıdır (charcoal `#434343` başlık, dolgusuz
delta, Calibri gövde) - Excel bir çalışma aracıdır ve bilinçle daha sadedir.
İkisi karıştırılmaz. Bu skill Excel üretmez; Excel gerekiyorsa
`icerik-dili-rehberi`'nin kanal kuralları uygulanır.

---

## Tipografi

| Aile | Dosya | Kullanım |
|---|---|---|
| **Bricolage Grotesque** | `assets/design-system/fonts/BricolageGrotesque-*.ttf` | Başlık, display, rakam, tablo başlığı, kalın vurgu |
| **Outfit** | `assets/design-system/fonts/Outfit-*.ttf` | Gövde metni, tablo gövdesi, dipnot |

Inter, system-ui veya başka bir yüz birincil olarak kullanılmaz. Fallback yalnızca
`'Calibri', system-ui`.

**Teslimde font klasörü de verilir.** Sunum başka makinede açılacaksa fontlar
kurulu olmadan Bricolage/Outfit yerine fallback görünür. `assets/design-system/fonts/`
klasörünü deste ile birlikte ilet.

**İçerik slaytı başlığı tek satırda kalır.** Uzun başlık sarmaz, puntosu küçülür.
Üretici bunu gerçek font metriğiyle ölçüp otomatik yapar ve 27 pt altına düştüğünde
uyarır - o uyarı "başlığı kısaltmayı düşün" demektir.

**Bölüm ayracında kural terstir: punto sabit, başlık sarar.** Numeral her ayraçta
157 pt (210 px), başlık her ayraçta 45 pt (60 px) - hiçbiri küçültülmez. Başlık
sığmıyorsa alt satıra kayar; accent çizgiler ve numeral çok satırlı bloğa göre
konumlanır ve blok dikeyde ortalanır (merkez her durumda 360 px).

Bu, vendor'daki `DESIGN-SYSTEM-README.md`'nin "ayraç başlığı tek satır, sarmaz"
ifadesinden **bilinçli bir ayrılmadır.** Gerekçe: numeralin puntosunu başlığa kalan
boşluğa göre ölçeklendirmek, numeral boyutunu başlık uzunluğunun fonksiyonu yapıyor
ve aynı destede farklı boyutta numeraller üretiyordu (örnekte 157 pt ve 141 pt bir
arada). Tutarlı numeral boyutu, tek satır zorunluluğundan daha önemli.

Başlık genişliği sınırı numeral bölgesinden türetilir: iki yanda numeral (218 px) +
24 px açıklık ayrıldıktan sonra kalan **748 px**. Bunun üstündeki başlık sarar. Üç
satıra taşan başlıkta uyarı verilir - iki satır tasarımın rahat sınırı.

**Büyük harfli etiketlerde İngilizce terim tuzağı:** CSS `text-transform:uppercase`
Türkçe locale'de İngilizce terimlerin "i" harfini "İ"ye çeviriyor (VİSİBİLİTY,
MENTİON, GEMİNİ). Bu yüzden büyük harfli etiketler kaynakta doğru harflemeyle
yazılır: İngilizce terim düz I (VISIBILITY, MENTION, POSITION), Türkçe İ (İLK,
METNİ). Üretici `.upper()` uyguladığı yerlerde bu risk var; etiketleri baştan
büyük harfle yazmak en temizi.

---

## Slayt gramerleri

Kapak, ajanda ve bölüm ayracının ölçüleri **VitrA Şubat 2026 destesinden birebir
ölçülmüştür** (kaynak deste 2560×1440; değerler 1280×720 sahneye çevrildi). Görseller
`assets/design-system/vitra-slides/` altında.

| Slayt | Zemin | Ayırt edici |
|---|---|---|
| Kapak | coral `#FF7B52` | Sol kenara yaslanmış soluk big-O (`cover-art-front.png`, 403×720). Ortalanmış başlık **47.5 pt SemiBold** `paper` (y=275), 22 px boşluk, altında dönem satırı **43 pt SemiBold**. Alt-ortada wordmark (563, 635, 153×32) |
| Ajanda | `paper_bg` `#FEFFFA` | Sol 640 px coral panel (`agenda-panel.png`, sağ köşeleri yuvarlak) + üzerinde big-O. Panelde ortalanmış **48 pt Regular** başlık (y=313). Sol altta beyaz logo (31, 632, 52×51). Sağda x=665 w=573 numaralı liste: numara **20 pt Regular** `ink3`, 8 px boşluk, etiket **20 pt Bold** `ink`; maddeler arası 26 px; blok dikeyde ortalanır |
| Bölüm ayracı | teal `#10332F` | Sabit konumlu **200 pt ExtraBold** numeral, renk `sep_num` `#254E49`, yatay merkezi x=146 (filigran gibi davranır, başlığa göre yer değiştirmez). Başlık sayfa ortasında **37 pt ExtraBold** `paper`. Üst-alt **coral** accent 43×11 px |
| İçerik | beyaz | Breadcrumb + başlık + dönem alt başlığı + blok ızgarası + dipnot + logo + kaynak |
| Kapanış | teal | Ortalanmış başlık, wordmark |

**Kapak metni kısa tutulur:** `<Marka> SEO Değerlendirme` + alt satırda yalnızca dönem
("Temmuz 2026"). Tarih aralığı, YoY/MoM ibaresi ve kapsam notu kapakta yer almaz;
bunlar içerik slaytlarının alt başlığında zaten veriliyor.

**Ayraçta punto sabittir, başlık sarar.** Numeral ve başlık puntosu deste genelinde
değişmez; 1080 px'i aşan başlık alt satıra kayar, accent çizgiler blok yüksekliğine
göre simetrik açılır ve blok dikeyde ortalanır (merkez her durumda 360 px). Numerali
başlığa göre ölçeklendirmek aynı destede farklı boyutta numeraller üretiyordu.

**Logo kuralı:** her içerik slaytının sol altında `inbound-o-teal.png` (koyu
zeminde `inbound-o-white.png`). Bölüm ayraçlarında logo **yok**. Kapak ve kapanışta
alt-ortada wordmark.

**Accent çizgi:** 60 × 3.5 px coral pill. Bölüm başlıklarını ve alıntıları çevreler.
Koyu zeminde beyaz olur.

**Coral highlight bar (`.hl`) slayt başlıklarında kullanılmaz.** Başlıklar düz koyu
teal. Coral bar yalnızca gövde metni, insight cümlesi ve alıntı içinde vurgu için.

**KPI delta satırı:** etiket önce, değer sonra - `MoM  +%8.3    YoY  -%18.9`.
Etiket gövde fontunda normal ağırlıkta ve hafif soluk, değer display fontunda
kalın. Okuma sırası "hangi karşılaştırma" → "ne kadar" olur.

**Ters eksenli grafik:** ortalama pozisyon gibi küçük değerin iyi olduğu
metriklerde bar yükseklikleri ters çevrilir (`invert: true`), iyileşme yukarı
okunur. Dipnotta ters eksenli olduğu yazılır.

**Insight işareti `➔`** (heavy rightward) ve **her zaman coral**; zemin açık ya da
koyu olsun ok rengi değişmez. `→`, `•` veya emoji ok değil. Tek sembol
setine sadık kalınır: `➔` insight başlatıcı, `→` önce-sonra dönüşümü, `↑ ↓` yön,
`✓ ▲` özet blok maddesi. `⇒ ➜ ⚠` ve emoji oklar kullanılmaz.

**Fotoğraf** kullanılıyorsa daire kırpımlı, sıcak ve dokümanter tonda. İkon seti
markada yok; gerekirse Lucide kullanılır ve bu kullanıcıya bildirilir.

---

## Grafik kuralları

**Native PPTX chart kullanılmaz.** İki gerekçe: PowerPoint native bar chart'ta
kategori eksenini "1, 2, 3" olarak gösteriyor (gerçek projede yaşandı) ve tasarım
sistemi görünümü tam kontrol edilemiyor. Bunun yerine düzenlenebilir vektör şekil
çizilir - sunum içinden renk ve metin düzenlenebilir, HTML önizlemeyle birebir olur.

- Eksen yerine **veri etiketi**: bar üstüne değer yazılır, y ekseni çizilmez.
- Yatay ızgara `line_soft`, taban çizgisi `line`.
- Legend üstte, 10 px, `ink2`.
- İki dönem karşılaştırmasında önceki `gold`, güncel `gray_bar`. Kendi kanalın veya
  markanın öne çıkması gerekiyorsa `coral`.
- Çok serili çizgi grafikte polyline + nokta işareti; seri sayısı dörtten fazlaysa
  okunurluk için grafiği bölmek daha iyi.

---

## Görsel doğrulama

Ortamda LibreOffice yoksa PPTX piksel olarak render edilemez. Bu yüzden
`build_html_preview.py` üretilen destenin birebir HTML karşılığını basar; görsel
kontrol orada yapılır. Önizleme tek dosyadır (fontlar data URI olarak gömülü),
taşınabilir ve kullanıcıya doğrudan gönderilebilir.

Önizlemeye gömülü self-check, gövde alt sınırını aşan blokları kırmızı kesikli
çerçeveyle işaretler ve slayta sayaç rozeti koyar. HTML esnek kutu kullandığı için
taşmayı sessizce sıkıştırır; PPTX mutlak konumlandırma kullandığından aynı içerik
orada logonun üstüne biner. İşaretleyici iki çıktının aynı sınırda okunmasını sağlar.
