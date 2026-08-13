# Game+ referans destesi - Temmuz 2026

Bu klasör, **Game+ (gameplus.com.tr) aylık değerlendirme destesinin onaylanmış
formatını** taşır. Yeni bir Game+ destesi kurulurken sıfırdan yapı tasarlanmaz;
`deck_olustur.py` dönem değerleriyle çalıştırılır ve bölüm sırası korunur.

| Dosya | Ne işe yarar |
|---|---|
| `deck_olustur.py` | Desteyi üreten script. Veri modüllerinden okur, `deck.json` yazar |
| `deck.json` | Üretilmiş deste tanımı - 34 slayt, onaylanmış sürüm |
| `veri/gsc_segment.py` | Search Console segment serisi (brand / non-brand / GFN, click-impression-pozisyon) |
| `veri/ga4.py` · `veri/ga4_analiz.py` | GA4 landing page export'unun okunması ve kanal/sayfa kırılımları |
| `veri/hacim.py` | Brand ve GFN aylık arama hacmi (Ahrefs volume history) |
| `veri/ek_veri.py` | Haftalık SSR serisi, oyun alt kategorisi Search Console verisi, AI trafik segmenti |
| `veri/ssr.py` | SSR geçişi öncesi/sonrası simetrik pencere hesabı |
| `../decks/gameplus-seo-degerlendirme-temmuz-2026.pptx` | Onaylanmış çıktı |

## Deste iskeleti (34 slayt)

```
Kapak · Akış
01 Genel Görünüm      yönetici özeti (4 KPI kartı + insight + KRİTİK TESPİT)
                      segment tanımları (panels 3'lü)
02 Google Search Console Metrikleri
                      aylık click serisi · aylık impression serisi
                      brand ve GFN aylık arama hacmi
                      Temmuz karşılaştırması (click / impression / pozisyon)
                      sorgu click hareketleri · sorgu pozisyon hareketleri
                      sayfa click hareketleri
03 SSR Geçişi Etkisi  simetrik pencere tablosu + haftalık grafik
04 GA4 Trafik         toplam ve organik aylık seri · kanal tablosu
05 İçerik Performansı /blog toplam+organik · yükselen yazılar
                      /gfn/oyunlar alt kategorileri (GA4 session + GSC click)
06 Yapay Zeka Görünürlüğü
                      mention & citation metrikleri
                      prompt-yanıt örnekleri (3 slayt, 2'şer örnek)
                      markadan nasıl bahsediliyor
                      AI kaynaklı trafiğin aylık seyri
07 Yapılan ve Planlanan İşler
                      tamamlanan işler + Game+ ekibinde bekleyen maddeler
                      planlanan işler
08 Değerlendirme      önümüzdeki dönemde öne çıkan üç başlık
Teşekkürler
```

## Game+'a özgü kurallar

**Segment tanımı.** Brand `includingRegex` ile doğrudan ölçülür
(`gameplus|game ?plus|game\+`); non-brand **toplam − brand** ile hesaplanır -
müşteri tarafındaki `gsc-dashboard` ETL'i de bu yöntemi kullanır, iki kaynağın
aynı sayıyı vermesi için yöntem takip edilir. Anonim sorgu hacmi bu nedenle
non-brand satırında yer alır ve bu, segment tanımları slaytında beyan edilir.

**GFN kesişen gruptur** (`gfn|geforce now|geforcenow`). Brand ve non-brand'in
üzerine biner; **Toplam satırına dahil edilmez** ve "üç grubun toplamı toplam
click'e eşit değildir" cümlesi slaytta durur.

**Segment sırası her tabloda aynı:** GFN → Brand → Non-Brand → Toplam. Toplam
satırı kalın ve en altta.

**Non-brand pozisyonu ayrı ölçülür** (`excludingRegex`), yalnızca pozisyon için
kullanılır; aynı çağrının click/impression değerleri anonim sorgular düştüğü
için eksiktir.

**AI Assistant kanalı** GA4 varsayılan kanal grubundan değil, yapay zeka
kaynaklı trafik segmentinden alınır; varsayılan gruptaki aynı adlı etiket daha
dar bir küme ölçer. Toplam satırı GA4'te ölçülen tüm kanalların toplamı kalır ve
bu dipnota yazılır.

**AI görünürlük metrikleri** araçtaki adlarıyla yazılır (Mention, Citation,
Brand Position, Source Visibility); pay taşıyan her metrik kesir + yüzde olarak
verilir (`966 / 1.622` · `%59.6`).

**Prompt örnekleri** marka adı geçmeyen prompt kümesinden seçilir, kart
düzeninde verilir ve olumlu örneklerin yanına en az bir eleştirel çerçeve konur.

## Yeni dönem için ne yapılır

1. `veri/` altındaki modüllerin kaynak dosya yollarını yeni export'lara çevir.
2. `deck_olustur.py` içindeki dönem sabitlerini (`202607` gibi) güncelle.
3. Elle yazılmış insight cümlelerini yeni rakamlara göre yeniden kur - sayılar
   f-string ile bağlı olanlar kendiliğinden güncellenir, yorum cümleleri değil.
4. `--check` → `qa_deck.py --pptx` → önizlemede gözle kontrol sırasını izle.
