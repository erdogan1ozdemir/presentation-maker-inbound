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

Punto ölçeği px × 0.75 ile pt'ye çevrilir: 36 px başlık = 27 pt, 14 px gövde =
10.5 pt, 13 px tablo = 9.75 pt, 12 px tablo başlığı = 9 pt.

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

**Başlık tek satırda kalır.** Uzun başlık sarmaz, puntosu küçülür. Üretici bunu
gerçek font metriğiyle ölçüp otomatik yapar ve 27 pt altına düştüğünde uyarır -
o uyarı "başlığı kısaltmayı düşün" demektir.

**Büyük harfli etiketlerde İngilizce terim tuzağı:** CSS `text-transform:uppercase`
Türkçe locale'de İngilizce terimlerin "i" harfini "İ"ye çeviriyor (VİSİBİLİTY,
MENTİON, GEMİNİ). Bu yüzden büyük harfli etiketler kaynakta doğru harflemeyle
yazılır: İngilizce terim düz I (VISIBILITY, MENTION, POSITION), Türkçe İ (İLK,
METNİ). Üretici `.upper()` uyguladığı yerlerde bu risk var; etiketleri baştan
büyük harfle yazmak en temizi.

---

## Slayt gramerleri

| Slayt | Zemin | Ayırt edici |
|---|---|---|
| Kapak | coral (veya teal) | Ortalanmış display başlık, alt-orta wordmark, sağ üstte %14 opak big-O |
| Ajanda | sol %45 coral panel + beyaz sağ | Sol panelde Light ağırlıklı büyük başlık, sağda numaralı liste |
| Bölüm ayracı | teal | Sol marjda `teal_soft` 210 px numeral, ortada tek satır başlık, üst-alt beyaz accent çizgi |
| İçerik | beyaz | Breadcrumb + başlık + dönem alt başlığı + blok ızgarası + dipnot + logo + kaynak |
| Kapanış | teal | Ortalanmış başlık, wordmark |

**Logo kuralı:** her içerik slaytının sol altında `inbound-o-teal.png` (koyu
zeminde `inbound-o-white.png`). Bölüm ayraçlarında logo **yok**. Kapak ve kapanışta
alt-ortada wordmark.

**Accent çizgi:** 60 × 3.5 px coral pill. Bölüm başlıklarını ve alıntıları çevreler.
Koyu zeminde beyaz olur.

**Coral highlight bar (`.hl`) slayt başlıklarında kullanılmaz.** Başlıklar düz koyu
teal. Coral bar yalnızca gövde metni, insight cümlesi ve alıntı içinde vurgu için.

**Insight işareti `➔`** (heavy rightward). `→`, `•` veya emoji ok değil. Tek sembol
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
