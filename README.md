# presentation-maker-inbound

Inbound ajans standardında **SEO/GEO performans değerlendirme sunumu** üreten Claude
Code skill'i. Inbound Design System görselini, `icerik-dili-rehberi` dil standardını ve
GSC/GA4/Keyword Planner/SEOmonitor/Ahrefs veri şemalarını uygulayarak düzenlenebilir
PPTX üretir.

Dört modda çalışır: **aylık (M1)**, **çeyreklik (M2)**, **yarıyıl (M3)**,
**etki/migrasyon analizi (M4)**.

---

## Kurulum

### Yol 1 - Plugin marketplace (önerilen)

Claude Code içinde:

```
/plugin marketplace add erdogan1ozdemir/presentation-maker-inbound
```

```
/plugin install inbound-sunum@presentation-maker-inbound
```

Güncelleme `/plugin update` ile gelir.

### Yol 2 - Doğrudan klonlama

```bash
git clone https://github.com/erdogan1ozdemir/presentation-maker-inbound.git /tmp/pmi \
  && cp -r /tmp/pmi/plugins/inbound-sunum/skills/inbound-sunum-uretici ~/.claude/skills/ \
  && rm -rf /tmp/pmi
```

### Bağımlılıklar

Kurulumdan sonra bir kez:

```bash
bash ~/.claude/skills/inbound-sunum-uretici/scripts/setup_deps.sh
```

Script iki şeyi denetler ve eksikse kurar:

- **`icerik-dili-rehberi`** skill'i ([repo](https://github.com/erdogan1ozdemir/icerik-dili-rehberi)) -
  üretilen sunumun dil ve ton standardı. Bu skill onun yerine geçmez; metin yazılırken
  o rehber okunur.
- **python-pptx** ve **Pillow**. Pillow önemli: font ölçümü onun üzerinden yapılıyor,
  olmadan taşma tespiti tahmine düşer.

---

## Kullanım

Skill kendiliğinden tetiklenir. Örnek istekler:

```
VitrA için Haziran 2026 aylık SEO sunumu hazırla
2026 Q1 çeyreklik değerlendirme sunumu yapalım
Gameplus SSR geçişinin etkisini sunumlaştır
şu GSC ve GA4 export'larından deste çıkar
```

Skill üretime girmeden önce brief alır: mod ve dönem, property'ler, iş modeli, hangi
veri kaynakları dahil olacak, hangi export'lar sende hangileri istenmesi gerekiyor,
"Neler Yaptık" ve "Sonraki Dönem Planı" bölümleri eklenecek mi. Elde olmayan her
kaynak için hangi raporu hangi tarih aralığıyla ve compare açık mı kapalı mı indirmek
gerektiğini tek tek söyler.

Veri tamamlanmadan slayt üretimine geçmez. Sağlanamayan veri için ilgili bölüm
destedan çıkarılır ve bu chat'te ayrıca bildirilir - rapora placeholder metrik veya
"sonraki aşamada eklenecek" vaadi bırakılmaz.

---

## Nasıl çalışıyor

Deste `deck.json` üzerinden bildirimsel olarak tanımlanır ve iki çıktıya derlenir:

```bash
python3 scripts/inbound_deck.py deck.json -o "Marka SEO Değerlendirme.pptx"
python3 scripts/build_html_preview.py deck.json -o onizleme.html
python3 scripts/qa_deck.py deck.json --pptx cikti.pptx
```

**Neden iki çıktı:** Design System slaytı 1280×720 px; bu ölçü 96 DPI'da tam olarak
PPTX'in 13.333×7.5 inch'i (1 px = 9525 EMU). Aynı koordinat sistemi olduğu için HTML
önizleme üretilen destenin birebir görsel karşılığıdır. LibreOffice kurulu olmayan
ortamlarda PPTX piksel olarak render edilemez; görsel kontrolün tek yolu bu önizlemedir.
Önizleme tek dosyadır (fontlar data URI olarak gömülü), doğrudan paylaşılabilir.

**Font ölçümü gerçek TTF üzerinden yapılır.** Bunun üç sonucu var: uzun başlık tek
satıra sığana kadar puntosu küçülür (Design System kuralı - slayt başlığı sarmaz),
tablo kolon genişlikleri içeriğe göre hesaplanır, ve gövde alt sınırını aşan blok
uyarı üretir. Metin taşması geçmiş destelerin en sık teslim hatasıydı; artık ölçülüyor.

**Grafikler düzenlenebilir vektör şekil olarak çizilir**, native PPTX chart
kullanılmaz: PowerPoint native bar chart'ta kategori eksenini "1, 2, 3" olarak
gösteriyor ve tasarım sistemi görünümü tam kontrol edilemiyor.

---

## Repo yapısı

```
.claude-plugin/marketplace.json          marketplace tanımı
plugins/inbound-sunum/
├── .claude-plugin/plugin.json
└── skills/inbound-sunum-uretici/
    ├── SKILL.md                         altı fazlı akış: brief -> veri kapısı ->
    │                                    işleme -> yorum -> deste -> denetim -> teslim
    ├── references/
    │   ├── veri-brief-ve-export.md      soru setleri, kaynak bazlı export talimatları
    │   ├── slayt-katalogu.md            37 slayt tipi + mod bazlı deste iskeletleri
    │   ├── tablo-semalari.md            T1-T14 kanonik tablo şemaları
    │   ├── deck-spec.md                 deck.json tam şeması
    │   ├── design-system.md             token'lar, slayt ızgarası, grafik kuralları
    │   └── tuzaklar-ve-qa.md            yaşanmış hatalar + teslim self-check
    ├── scripts/
    │   ├── inbound_deck.py              deck.json -> PPTX (çekirdek üretici)
    │   ├── build_html_preview.py        deck.json -> HTML önizleme
    │   ├── qa_deck.py                   yerleşim + dil + rakam denetimi
    │   ├── veri_tara.py                 export dosyalarını tanı, eksik listesi çıkar
    │   └── setup_deps.sh                bağımlılık kurulumu
    └── assets/
        ├── design-system/               token CSS, 12 TTF font, logolar
        └── ornek/deck-ornek.json        çalışan 13 slaytlık örnek deste

reference/
├── decks/                               referans SEO değerlendirme desteleri
└── notlar/                              destelerden çıkarılmış süreç ve veri notları
```

---

## Referanslar

`reference/notlar/` altındaki dört doküman, skill'in çıkarıldığı kaynak analizlerdir:

| Dosya | İçerik |
|---|---|
| `01-turkcell-surec-ve-veri-notlari.md` | Veri kaynakları, kapsam tuzakları, üretim pipeline'ı, QA |
| `02-gameplus-veri-tablo-slayt-katalogu.md` | 37 slayt tipi, T1-T14 tablo şemaları, mod matrisi, bilinen tuzaklar |
| `03-ozdilek-uretim-ve-qa-notlari.md` | AI görünürlük bölümü, metrik sözlüğü, teknik üretim, denetim yöntemi |
| `04-loft-slayt-mapping.md` | Slayt bazlı veri kaynağı eşlemesi ve insight soru setleri |

`reference/decks/` altındaki desteler yapı, dil ve veri gösterim biçimi için
referanstır.

---

## Kapsam

Bu skill **SEO/GEO performans değerlendirme sunumları** içindir. Kapsam dışı: tüketiciye
dönük blog içeriği, teknik PageSpeed denetim sunumu, tek sayfa SEO analizi, Excel audit
çıktısı. Bunların kendi skill'leri var.
