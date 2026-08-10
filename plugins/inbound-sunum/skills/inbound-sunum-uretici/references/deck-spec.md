# deck.json Şeması

> Faz 4'te okunur. Deste bildirimsel olarak tanımlanır; `inbound_deck.py` PPTX'e,
> `build_html_preview.py` HTML'e derler. İki çıktı aynı koordinat sistemini
> paylaşır: 1280×720 px sahne = 13.333×7.5 inch PPTX (96 DPI, 1 px = 9525 EMU).

Çalışan tam örnek: `assets/ornek/deck-ornek.json` (13 slayt). Yeni deste kurarken
sıfırdan yazmak yerine oradan kopyalayıp değiştir.

## İskelet

```json
{
  "meta": { "brand": "Marka", "mode": "M1", "period": "Haziran 2026" },
  "output": "Marka SEO Değerlendirme Haziran 2026.pptx",
  "slides": [ { "type": "cover", "...": "..." } ]
}
```

`meta.brand` marka yazım tutarlılığı denetiminde kullanılıyor: destede markanın
farklı büyük/küçük harf varyantları geçiyorsa `qa_deck.py` hata verir.

---

## Slayt tipleri

### cover

```json
{ "type": "cover",
  "title_lines": ["Marka |", "Aylık SEO Değerlendirme"],
  "title_pt": 50,
  "subtitle": "Haziran 2026 (1 - 30 Haz 2026) | MoM ve YoY karşılaştırma",
  "bg": "coral" }
```

`title_lines` satır kırmasını sen kontrol edersin. `bg`: `coral` (varsayılan) veya
`teal`. Wordmark alt-ortaya, dekoratif big-O sağ üste otomatik gelir.

### agenda

```json
{ "type": "agenda",
  "kicker": "Haziran 2026",
  "title_lines": ["SUNUM", "AKIŞI"],
  "items": [ { "no": "01", "label": "Arama Hacmi ve Rekabet" } ] }
```

Sol %45 coral panel + sağ numaralı liste. **Madde sayısı destedeki `separator`
sayısına eşit olmalı** - `qa_deck.py` bunu denetler, gerçek destelerde ajandada 3
bölüm varken destede 4 bölüm olduğu yaşandı.

### separator

```json
{ "type": "separator", "no": "01", "title": "Arama Hacmi ve Rekabet" }
```

Koyu teal zemin, soluk numeral sol marjda, başlık sayfa ortasında tek satır,
üstünde ve altında beyaz accent çizgi. Numaralar ajandayla birebir eşleşir ve
tekrarlanmaz.

### closing

```json
{ "type": "closing", "title": "Teşekkürler", "subtitle": "opsiyonel" }
```

### content

İş atı. Krom (breadcrumb, başlık, alt başlık, logo, kaynak) + blok ızgarası.

```json
{
  "type": "content",
  "breadcrumb": ["SEARCH CONSOLE", "Brand ve Non-Brand Kırılımı"],
  "title": "Impression, Click ve CTR Kırılımı",
  "subtitle": "Haziran 2026 & Haziran 2025 | YoY | web + app kapsam",
  "source": "Google Search Console · Aylık",
  "grid": [58, 42],
  "gap": 36,
  "footnotes": ["*2025 Aralık ayında domain geçişi gerçekleşmiştir."],
  "notes": "konuşmacı notu - teslim öncesi taranır",
  "blocks": [ ]
}
```

| Alan | Açıklama |
|---|---|
| `breadcrumb` | Sol üst, coral. İlk öğe bölüm (kalın), sonrası alt başlık |
| `title` | Bir satıra sığana kadar puntosu otomatik küçülür (Design System kuralı) |
| `subtitle` | **Dönem beyanı buraya.** Yoksa QA uyarı verir |
| `source` | Otomatik "Kaynak: " öneki alır. Veri bloğu varsa zorunlu |
| `grid` | Kolon yüzdeleri. `[100]` tek kolon, `[58,42]` iki kolon |
| `footnotes` | Gövde altı, yıldızlı bağlam notları |
| `bg` | `white` (varsayılan) veya `teal`/`dark` |

**Blok yerleşimi:** her blok `col` ile kolona atanır (verilmezse sırayla dağıtılır).
Aynı kolondaki bloklar dikey yığılır. `mt` / `mb` üst/alt boşluk ekler. `at: [x,y,w,h]`
mutlak konum için kaçış kapısıdır, nadiren gerekir.

**Gövde alt sınırı 636 px.** Altında logo ve kaynak şeridi var. Bu sınırı aşan blok
uyarı üretir; uyarıyı görmezden geçmek PPTX'te logonun üstüne binen tablo demektir.

---

## Blok tipleri

### table

```json
{ "type": "table", "col": 0,
  "title": "opsiyonel blok başlığı",
  "head": ["Sorgu Kümesi", "Imp Haz 25", "Imp Haz 26", "YoY"],
  "rows": [["Total", "6.42M", "7.11M", "+%10.7"]],
  "align": "lccc",
  "delta_cols": [3],
  "wash": true,
  "highlight_rows": [1],
  "bold_rows": [0, -1],
  "col_w": [40, 20, 20, 20],
  "row_h": 26, "head_h": 30, "font_pt": 9.5 }
```

- Başlık satırı: teal `#10332F` zemin, beyaz kalın (deck/HTML tablo standardı).
- `delta_cols` verilmezse **otomatik tespit**: hücrelerin yarısından fazlası
  `+%X` / `-%X` biçimindeyse o kolon delta sayılır. Pozitif yeşil, negatif kırmızı.
- `wash: true` delta hücresine yeşil/kırmızı zemin verir (deck standardı).
  Excel çıktısında dolgu kullanılmaz, ama bu bir deck üreticisi.
- `highlight_rows` coral-tint vurgu - kendi markanın satırı için.
- `bold_rows` negatif index kabul eder: `-1` son satır (Total / Grand Total).
- `col_w` verilmezse kolon genişlikleri **ölçülen içerikten** hesaplanır; ilk kolon
  esner, sayısal kolonlar içeriğini korur.
- Satır uzunlukları `head` ile eşit olmalı; QA denetler.

### insights

```json
{ "type": "insights", "col": 1,
  "title": "TREND OKUMALARI",
  "items": ["Session {g:+%10.4} artarken revenue {r:-%42} düşmüştür."],
  "gap": 12, "font_pt": 10.5, "dark": false }
```

`➔` ok otomatik. **Her veri bloğunun yanında/altında bir yorum katmanı olmalı** -
yorumsuz tablo QA hatası.

### kpi

```json
{ "type": "kpi", "cols": 4, "h": 132,
  "cards": [
    { "value": "174.7K", "label": "Organic Sessions", "delta": "+%10.4 MoM" },
    { "value": "52.4", "unit": "%", "label": "Organik Payı", "delta": "+1.8p MoM" },
    { "value": "%2.89", "label": "Organic CR", "delta": "-%0.4 MoM", "accent": "coral" }
  ] }
```

Kart zemini varsayılan teal; son kart (3+ kartta) coral olur. `accent` ile
elle seçilir. `value` karta sığmazsa puntosu otomatik küçülür.

### bar

```json
{ "type": "bar", "h": 260, "stacked": false, "value_labels": true, "bar_w": 22,
  "cats": ["Oca", "Şub", "Mar"],
  "series": [
    { "name": "2025", "data": [128000, 131000, 140000], "color": "gold" },
    { "name": "2026", "data": [141000, 149000, 156000], "color": "gray_bar" }
  ] }
```

Düzenlenebilir vektör şekil olarak çizilir, native PPTX chart kullanılmaz
(PowerPoint kategori eksenini "1,2,3" gösteriyor). `stacked: true` yığılmış bar
yapar ve etiket toplamı gösterir. Renk paleti: önceki dönem `gold`, güncel dönem
`gray_bar`, kendi kanalın/markanın `coral`.

### line

```json
{ "type": "line", "h": 260,
  "cats": ["Oca", "Şub", "Mar"],
  "series": [{ "name": "Click", "data": [214, 231, 241], "color": "coral" }] }
```

Freeform polyline + nokta işaretleri; düzenlenebilir kalır.

### panels

```json
{ "type": "panels", "cols": 3,
  "items": [{ "title": "Öncelik 1", "sub": "alt açıklama",
              "lines": ["madde bir", "madde iki"] }] }
```

Aksiyon/öneri setleri, üç panelli analiz slaytları, kazanım-kayıp blokları için.

### note

```json
{ "type": "note", "label": "YÖNTEM", "fill": "mint",
  "text": "Visibility score, marka özelinde takip edilen kelimelerin..." }
```

Metodoloji ve tanım kutuları. Metin içinde kaybolmaması gereken notlar için;
etiketli blok olarak durur.

### text

```json
{ "type": "text", "title": "opsiyonel",
  "paras": ["paragraf bir", "paragraf iki"], "font_pt": 10.5 }
```

### image

```json
{ "type": "image", "path": "gorseller/aio-ekran.png", "w": 520 }
```

Yol deck.json'a göre relatif. Ekran görüntüsü kullanılıyorsa **bulgunun özü metinde
de yazılır**, görsele delege edilmez.

---

## Zengin metin işaretleme

Tüm metin alanlarında geçerli:

| İşaret | Sonuç | Ne için |
|---|---|---|
| `{b:595.4K}` | kalın, ink | Rakamlar, metrik adları |
| `{g:+%10.4}` | kalın yeşil `#2E7D32` | Artış / pozitif |
| `{r:-%37}` | kalın kırmızı `#D32F2F` | Düşüş / negatif |
| `{c:en stabil kategori}` | kalın coral `#FF7B52` | Anahtar terim, dikkat |
| `{n:ikincil bilgi}` | soluk `#8A8A8A` | Yan bilgi |

İç içe kullanılmaz. `plain()` bu işaretleri temizler; QA denetimi işaretsiz metin
üzerinde çalışır.

---

## Komutlar

```bash
python3 scripts/inbound_deck.py deck.json -o cikti.pptx    # PPTX
python3 scripts/inbound_deck.py deck.json --check          # yazmadan doğrula
python3 scripts/build_html_preview.py deck.json -o onizleme.html
python3 scripts/qa_deck.py deck.json --pptx cikti.pptx     # tam denetim
```

Üretici uyarı verdiyse çıkış kodu 1'dir. Uyarılar bilgi değil, düzeltilecek iş.
