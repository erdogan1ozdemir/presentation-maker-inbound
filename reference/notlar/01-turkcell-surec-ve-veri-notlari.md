# SEO Değerlendirme Sunumu Üretici — Süreç & Veri Modülü (jenerik)

> **Bu dosya ne?** Birden çok chatten toplanacak `skill` notlarının **bir modülü**. Kapsamı: **üretim süreci + veri kaynaklarının nasıl kullanıldığı + sunum tipleri (aylık / çeyreklik / half) + aylık metrik tabloları**.
> **Bu dosyada OLMAYAN, ayrı modüllerden gelecek:** (a) İçerik dili/ton kuralları → `icerik-dili-rehberi`, (b) Görsel tasarım/token/tipografi → `Inbound Design System`, (c) marka-özel veri değerleri. Bu iki modüle referans verilir, tekrar edilmez.
> **Jeneriklik:** Her yer marka-bağımsız yazıldı. `{MARKA}`, `{PROPERTY}`, `{DOMAIN}`, `{DÖNEM}` gibi placeholder'lar kullanılır. "Örnek (Turkcell)" notları yalnızca somutlaştırma içindir; skillde silinebilir.

---

## 0. Skill'in amacı ve tetikleyici

Bir markanın **SEO/GEO performansını** değerlendiren, **Inbound Design System** ile tasarlanmış, **PPTX** çıktısı veren sunum üretmek. Girdi: brief/outline + veri export'ları. Çıktı: düzenlenebilir PPTX (opsiyonel HTML önizleme).

Tetikleyici ifadeler: "aylık SEO sunumu", "çeyreklik değerlendirme", "H1/H2 sunumu", "{marka} performans sunumu hazırla", "GSC/GA4 verilerini sunumlaştır".

**Üç kadans, tek iskelet:** Aynı bölüm iskeleti ve bileşenler; sadece **karşılaştırma dönemi** ve **derinlik** değişir (bkz. Bölüm 4).

---

## 1. Girdiler (her marka için toplanacaklar)

| Girdi | Ne işe yarar | Format |
|---|---|---|
| Brief / outline | Sunum akışı, öncelikler, hangi bölümler | docx / metin |
| Veri klasörü | Ham GA4, GSC, SEOmonitor, Ahrefs, kanal export'ları | csv / md / xlsx |
| Marka künyesi | Property adları, domain, GSC property, rakip seti, dönem | metin |
| Tasarım sistemi | Renk/font/token (ayrı modül) | Inbound Design System |
| İçerik dili | Ton/üslup (ayrı modül) | icerik-dili-rehberi |

**Marka başına parametreler (skill'de sorulacak/alınacak):**
- Marka/property adları (ör. ana domain + subproperty'ler)
- GSC property URL'leri (URL-prefix veya `sc-domain:`)
- Rakip seti (SoV karşılaştırması için)
- Karşılaştırma dönemi ve kadans (aylık / çeyreklik / half)
- Öne çıkacak KPI'lar (revenue var mı, non-brand odağı vb.)

---

## 2. Veri Kaynakları — hangisinden ne alınır, nasıl kullanılır

> **Altın kural:** Hiçbir sayı uydurulmaz. Veri yoksa → chat'ten bildir, manuel iste, gelmezse ilgili alanı **çıkar** (bkz. Bölüm 11). Her sayı bir kaynağa bağlanır ve ham veri dosyaya kaydedilir (izlenebilirlik).

### 2.1. GA4 / GA360 (oturum, kullanıcı, gelir, kanal, platform)
- **Metrikler:** Sessions, Total/Active Users, Engagement Rate, Avg. Engagement Time, Key Events / Conversions, **Total Revenue**.
- **Kırılımlar:** Organic Search kanalı; Default Channel Group (Direct, Organic, Paid, Cross-network, Unassigned, AI Assistant…); Platform (Android/iOS/Web); Landing Pages.
- **Kullanım:** Yönetici özeti KPI'ları, organik performans tablosu, kanal dinamikleri, platform (web→app kayması), top sayfalar.
- **KRİTİK UYARILAR (bu projede yaşanan tuzaklar):**
  - **web+app vs web-only:** Property/subproperty toplamı genelde **web + app birlikte**. "Web-only organik" ayrı bir GA export'u (Web platform filtresi) gerektirir; toplam × platform-payı ile **türetilemez** (organik platform kırılımı ayrı gelmeli). Aynı metriği farklı slaytlarda farklı kapsamda vermek **tutarsızlık** yaratır — deck baştan sona **tek kapsam** olmalı, kapsam her tabloda etiketlenmeli.
  - **Revenue bazı subproperty'lerde ₺0:** Bazı property'lerde gelir GA'da track edilmez (tüm kanallar 0). O zaman revenue analizini **çıkar**, session odaklı git, dipnotla belirt. (Örnek: telco/ISP subproperty'lerinde revenue 0; e-ticaret subproperty'sinde gerçek revenue var.)
  - **Canlı GA erişimi genelde YOK:** GA4/GA360 MCP bağlı değilse veri **kullanıcının export'undan** gelir; bunu net söyle ("canlı çekim değil").
  - **"(not set)" landing page:** Organik landing raporunda büyük "(not set)" bucket'ı = app oturumları; app-ağırlıklı organiği gösterir.

### 2.2. Google Search Console (görünürlük, tıklama, sıra)
- **Metrikler:** Impressions, Clicks, CTR, Avg. Position.
- **Kırılımlar:** Brand vs Non-brand, query (kelime), page, device, country, tarih.
- **Kullanım:** GSC performans tablosu, non-brand büyüme hikâyesi, **kelime bazlı pozisyon iyileşmeleri** (before→after), odak kelime tabloları.
- **CANLI ÇEKİM MÜMKÜN** (GSC MCP bağlıysa): `get_advanced_search_analytics` (filtre/sıralama/sayfalama), `compare_search_periods`, `get_search_analytics`.
  - **16 ay retention:** Bugünden ~16 ay öncesine kadar. Tam "H1 geçen yıl" karşılaştırması pencere dışına taşabilir → **H1 2026 vs H2 2025** gibi geçerli, eşit uzunlukta bir "önceki dönem" seç.
  - Kelime bazlı çekim: property başına top query'leri (impressions/clicks sıralı, row_limit ~100) iki dönem için çek, hedef kelimeleri filtrele, pozisyon delta'sını hesapla.
  - "before → after" pozisyon: SEOmonitor/GSC "3 +63" gösterimi = güncel sıra 3, +63 iyileşme → **önce 66 → sonra 3**.

### 2.3. SEOmonitor (visibility, SoV, AI görünürlük)
- **Metrikler:** Visibility Top 3 / Top 10 kelime sayısı; Share of Voice; **Google / AI Overview / AI Search** için **Mention** (anılma payı) ve **Citation** (atıf/kaynak payı); before→after pozisyon.
- **Kullanım:** Visibility büyüme (bar), rakip görünürlük tabloları (SoV), odak kelime before→after tabloları.
- **Mention ≠ Citation** ayrımı net verilir (legend + not). Değişimler **puan (pp)** dilinde. Rakipler isimle + nötr, kazanım **fırsat** olarak çerçevelenir (içerik dili modülü).
- SEOmonitor MCP genelde bağlı değil → veri ekran görüntüsü/export ile gelir; **tabloya çevrilir** (screenshot slayda yapıştırılmaz).

### 2.4. Ahrefs / SEO Tool (visibility, backlink, DR)
- Visibility (Top 3/10), organic keywords, backlink profili, DR. Rakip benchmark için.

### 2.5. Kanal export'ları (Traffic Acquisition CSV)
- **Session primary channel group** export'u: kanal bazlı Sessions, Engaged Sessions, Engagement Rate, Key Events, **Total Revenue**.
- Her property için ayrı dosya olur (Master + subproperty'ler). **Dosya başlığındaki `# Property:` ve `# Start/End date` satırlarını mutlaka oku** — hangi property ve hangi dönem olduğunu belirler (yanlış dosyayı yanlış slayta bağlamamak için).
- Kullanım: Kanal YoY tablosu, organik payı, kanal dağılımı (stacked bar), attribution kayması (Unassigned↔Direct).

---

## 3. Bir sayıyı slayta koymadan önce checklist
1. Hangi **property/subproperty**? (Master mı, alt mı)
2. Hangi **kanal**? (genelde Organic Search)
3. Hangi **metrik**? (Sessions ≠ Users ≠ Clicks)
4. **web+app mı, web-only mı?** (deck genelinde tutarlı mı)
5. Hangi **dönem** ve karşılaştırma? (aylık/çeyreklik/half; YoY/MoM/QoQ)
6. **Kaynak dosya** hangisi, ham değer kaydedildi mi?
7. Revenue gerçekten track ediliyor mu (yoksa ₺0 mı)?

---

## 4. Sunum tipleri (aylık / çeyreklik / half) — tek iskelet, değişen karşılaştırma

| Tip | Karşılaştırma | Vurgu | Tablo kadansı |
|---|---|---|---|
| **Aylık** | MoM (ay / önceki ay) + opsiyonel YoY (ay / geçen yıl aynı ay) | Kısa, trend + o ayın hikâyesi | **Aylık** GSC & GA4 tabloları (bkz. Bölüm 5) |
| **Çeyreklik** | QoQ (çeyrek / önceki çeyrek) + YoY | Çeyrek momentumu, Q içi aylık trend | Aylık tablolar + çeyrek özet |
| **Half (H1/H2)** | YoY (H1 / geçen H1) | Kapsamlı; tüm bölümler, derinlik, öneri seti | Yarıyıl özet + aylık trend grafiği |

**Ortak akış:** Kapak → Sunum Akışı (ajanda) → bölümler → kapanış (Teşekkürler). Bölümler kadansa göre kısalır/uzar; **aylıkta** genelde 1-2 veri bölümü + kısa öneri; **halfte** tam set.

**Dönem etiketi standardı:** "H1 2026 (1 Oca - 30 Haz 2026) vs H1 2025 | YoY". Çeyrek: "2026 Q1". Ay: "Mart 2026" (metin), "Mar'26" (dar hücre). (Detay: içerik dili modülü, Rakam/Tarih standardı.)

---

## 5. AYLIK METRİK TABLOLARI (her marka için — bu skillin çekirdeği)

> Bu tablolar **diğer markalarda da tekrarlanacak** standart bloktur. Her property için bir GA4 + bir GSC aylık tablosu. Aylıkta ana içerik; çeyreklik/halfte trend/özet olarak kullanılır.

### 5.1. GA4 — Aylık Organic Search (property başına)

| Ay | Sessions | Users | Engagement Rate | Key Events / Conv. | Revenue* | MoM (Sessions) |
|----|----------|-------|-----------------|--------------------|----------|----------------|
| Oca | … | … | …% | … | ₺… | — |
| Şub | … | … | …% | … | ₺… | +/-% |
| … | | | | | | |

\* Revenue track edilmiyorsa (₺0) kolon **çıkarılır**, dipnot düşülür.
Kaynak: GA4 - {PROPERTY} · Organic Search · Aylık.

### 5.2. GSC — Aylık (property başına)

| Ay | Impressions | Clicks | CTR | Avg. Position | MoM (Clicks) |
|----|-------------|--------|-----|---------------|--------------|
| Oca | … | … | …% | … | — |
| Şub | … | … | …% | … | +/-% |
| … | | | | | |

Kaynak: Google Search Console - {PROPERTY} · Aylık. Opsiyonel: Brand / Non-brand kırılımı ayrı iki satır/tablo.

### 5.3. Çok markalı özet (aylık kıyas)
- Markalar/property'ler yan yana: `Marka | Sessions (bu ay) | MoM | Clicks | MoM | Avg. Pos`.
- Kapsam etiketi zorunlu (web-only / web+app).

**Renk kodu (tüm tablolar):** artış yeşil `#2E7D32`, düşüş kırmızı `#D32F2F`, kendi marka/öne çıkan satır coralTint highlight, rakamlar bold. (Tasarım modülüyle uyumlu.)

---

## 6. Deck bölüm iskeleti (half örneği — aylıkta sadeleştir)

1. **Genel Özet** — KPI kartları + Kritik Tespit kutusu + ✓/▲ öne çıkanlar; property performans özeti (GA + GSC tablo); en çok büyüyen/düşen alanlar.
2. **Marka & Kelime Karşılaştırması** — GA organic sessions kıyas; GSC clicks & brand/non-brand; non-brand kelime pozisyon iyileşmeleri; visibility (Top 3/10 bar); **Odak Kelimeler** (GSC + opsiyonel SEOmonitor versiyonu).
3. **Marka Bazında İnceleme** — her property için: chip'ler (KPI) + top organik sayfalar + insight'lar; **her markanın arkasına rakip görünürlük (SoV) tablosu** (Google + AI Overview mention/citation + AI Search).
4. **Kanal & Platform Dinamikleri** — platform dağılımı (web/app); web→app kayması & attribution; **property başına kanal kırılımı** (session ± revenue tablosu) + organik payı/dağılımı (stacked bar) + organik kalite stat chip'leri.
5. **Önceliklendirme & H2/Sonraki Dönem Focus** — Neler Yaptık/Başardık (retrospektif + audit'te çözülenler); Neleri Korumalıyız; Hızlı Aksiyonlar (audit teknik); Yatırım / Low-Hanging Fruit (audit içerik/GEO); Growth Backlog; Learnings.
6. **Dijital & AI Trendler** — GEO / AI aramada görünürlük; agentic commerce; markaya çıkarımlar (audit ile bağla).
+ Kapak, Ajanda, Bölüm ayraçları (01-06 numaralı, faded büyük numara), Teşekkürler.

> **Aylık** için: 1 (özet) + 2/4'ten seçili tablolar + kısa 5 (aksiyon) yeterli. **Çeyreklik** için orta. **Half** için tam set.

---

## 7. Slayt tipi kataloğu (yeniden kullanılabilir bileşenler)

| Bileşen | Ne için | Not |
|---|---|---|
| KPI kartı | Yönetici özeti büyük metrik | 4'lü grid, teal/coral zemin |
| Veri tablosu | Metrik × dönem × YoY | Teal başlık, YoY renk kodu, highlight satır |
| Stat chip | Tekil büyük metrik + alt etiket | before→after gösterebilir |
| Insight listesi (➔) | Bulgu + yorum | Her madde `➔` ile; 1 sayısal + 1 yorum cümlesi |
| Stacked bar | Kanal/pay dağılımı (dönem kıyas) | Kendi kanal coral highlight; custom shape (native chart DEĞİL) |
| Rakip SoV tablosu | Google + AI Overview/AI Search mention/citation | Kendi marka highlight; mention≠citation legend |
| Kelime before→after | Odak/mover kelimeler | "66 → 3" formatı, iyileşme yeşil |
| Audit tablosu | Teknik/içerik bulguları | Bulgu \| Aksiyon \| Marka/Etki |
| Retrospektif | Yapılanlar / Kazanımlar | iki kolon ✓ liste |
| Trend kartları | GEO / agentic | 3 kart + çıkarım notu |

---

## 8. Üretim pipeline (iki yol)

### Yol A — Sıfırdan üretim: Node + pptxgenjs (`build_deck.js`)
- Kendi Scene/components katmanı; **Inbound Design System token'ları** ile HTML + PPTX aynı kaynaktan.
- Canvas **13.333 × 7.5 in** (1280×720). Avantaj: tam kontrol, HTML önizleme, token tutarlılığı.
- **Native pptx bar chart KULLANMA:** PowerPoint kategori eksenini "1,2,3" gösteriyor. Bar'ları **custom shape** (rect + text label) çiz (HTML render'ı birebir yansıt).
- Başlık **auto-shrink**: tek satıra sığmıyorsa font otomatik küçülür (`wrap:false`).

### Yol B — Mevcut deck'i düzenleme: python-pptx
- Kullanıcı deck'i **Google Slides'ta** düzenlemişse dosya **10 × 5.625 in** ölçeğine geçer ("GoogleShape" görselleri). Build pipeline'dan diverge eder → **kullanıcının dosyasını doğrudan python-pptx ile düzenle** (el emeğini korur).
- **Stil eşleme:** yeni tabloları mevcut bir tablonun (ör. deckteki bir Odak tablosu) hücre formatına birebir eşle — fill `#10332F` teal başlık, Bricolage 8pt, ince `#E0E0E0` border, `strip_style` ile banding kapat, border XML'i tcPr'de **fill'den ÖNCE** ekle.
- **Slayt ekleme + konumlama:** `add_slide(layout)` sona ekler → `slides._sldIdLst` üzerinde reorder ile doğru yere taşı; inherited placeholder'ları sil; `p:bg` ile beyaz zemin ver.
- **Görsel (logo/badge):** `add_picture` + rounded-rect kaynak badge.
- **Yorumları koru:** Google Slides'tan gelen `ppt/comments/*` (ör. ekip yorumları) silinmez; "duplicate authorid" uyarısı Google kaynaklı, zararsız.

> **Kural:** Kullanıcı Slides'ta çalışıyorsa **her turda onun son export'unu baz al**; build_deck.js divergent kalır. Tek kaynak üzerinden ilerlemek için baştan anlaş.

---

## 9. Tasarım sistemi (özet — detay ayrı modül: Inbound Design System)
- Renk: teal `#10332F`, coral `#FF7B52`/`#E85F36`, yeşil `#2E7D32`, kırmızı `#D32F2F`, gold `#F5A623`, gri tonları, highlight coralTint `#FFE3D8`.
- Font: **Bricolage Grotesque** (başlık/display), **Outfit** (gövde). Excel'de Calibri.
- Teslimde **font klasörü** de ver (sunum makinesine kurulunca doğru görünür).

---

## 10. İçerik dili (özet — detay ayrı modül: icerik-dili-rehberi)
- Advisory ton (emir kipi yok, kesin vaat yok), pasif/3. tekil, İngilizce sektör terimleri korunur.
- `➔` insight; artış yeşil / düşüş kırmızı / anahtar terim coral / rakam bold.
- **Em dash (—) yasak**, GA360 değil **GA4**, mention≠citation, puan (pp) dili, rakip nötr + fırsat çerçevesi.
- Kaynak notu her veri tablosunda: "Kaynak: {sistem} - {property} · {dönem}".

---

## 11. Veri bütünlüğü & eksik veri politikası
1. **Uydurma yok.** Gerçek veri yoksa varsayım rakamı yazılmaz.
2. **Eksik veri → chat'ten bildir + manuel iste + gelmezse alanı çıkar** (rapora "sonra eklenecek" placeholder bırakılmaz). Örnek: subproperty revenue ₺0 → revenue kolonu çıkar, dipnot.
3. **İzlenebilirlik:** her sayı kaynağa bağlanır; ham export dosyaya kaydedilir (ör. `veri/…-veri.md`), böylece "bu rakam neye göre?" sorusu birebir yanıtlanır.
4. **Kapsam tutarlılığı:** aynı metrik (ör. organik session) tüm deckte tek kapsam (web-only VEYA web+app). Karışıksa **her tabloda kapsam etiketi**. (Bu projede slayt 8 web-only iken slayt 5 web+app kalıp tutarsızlık yaratmıştı — önlem: baştan kapsam kararı.)
5. **İç kısıtlar rapora yazılmaz** (ör. "canlı çekilemedi") → sunacak kişiye chat'ten iletilir.

---

## 12. QA (teslim öncesi — her çıktıda)
- **Overlap/overflow detektörü** (tarayıcı JS): tüm slaytlarda metin taşması / üst üste binme taraması. (Bileşen kutuları değil, gerçek text span/td rect'leri karşılaştırılır; ayraç numarası gibi bilinçli öğeler hariç tutulur.)
- **Görsel doğrulama (LibreOffice yoksa):** slaytın **HTML birebir kopyasını** (aynı ölçek/renk/font) yapıp tarayıcıda screenshot al — pptx'i piksel render edemesen de tasarımı teyit edersin. (Tarayıcı pane scroll sonrası paint glitch veriyorsa: slaytı `display:none` ile izole edip scroll-0'da çek.)
- **validate.py** (pptx skill) — dosya bütünlüğü.
- **Dil taraması:** `grep "—"` = 0; GA360 = 0; register kayması (-iyor) kontrolü; çift boşluk; typo.
- **Rakam tutarlılığı:** yüzde formatı tek (`+%X`, nokta ondalık), imkansız rakam yok, kapsam etiketi var.

### Overlap detektörü (referans snippet)
```js
// her section.slide için text span/td rect'lerini karşılaştır; overflow (>1280x720) + overlap raporla
[...document.querySelectorAll('section.slide')].forEach((sl,si)=>{ /* rects topla, pairwise kesişim, alan>threshold raporla */ });
```

---

## 13. Marka değiştirince neyi parametrele (jeneriklik checklist)
- [ ] Property/subproperty adları + domain + GSC property URL'leri
- [ ] Rakip seti (SoV)
- [ ] Kadans (aylık/çeyreklik/half) + karşılaştırma dönemi
- [ ] Revenue var mı (yoksa revenue bloklarını çıkar)
- [ ] web-only mi web+app mi (deck geneli tek kapsam)
- [ ] KPI seçimi (revenue / non-brand / visibility / position…)
- [ ] Kaynak notları ({sistem} - {property} · {dönem})
- [ ] Aylık GSC + GA4 tabloları her property için dolduruldu mu (Bölüm 5)

---

## 14. Uçtan uca akış (özet)
1. Brief + veri klasörü + kadans al → parametreleri netle.
2. Veri kaynaklarını oku, **başlık/dönem/property/kapsam** doğrula; ham veriyi kaydet.
3. Eksikleri chat'ten bildir; kapsam kararı ver (web-only/web+app).
4. Bölüm iskeletini kadansa göre seç (Bölüm 6); aylık metrik tablolarını doldur (Bölüm 5).
5. Üret: Yol A (sıfırdan pptxgenjs) veya Yol B (mevcut deck'i python-pptx ile düzenle).
6. QA: overlap + HTML mock + validate + dil taraması.
7. Teslim: PPTX (+ font klasörü); her tabloda kaynak; tutarlılık teyidi.
8. Gidişat kaydını güncelle (proje md'si).
