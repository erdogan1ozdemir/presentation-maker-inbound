# Arama hacmi: kaynak sırası ve etiketleme

> Faz 2'de okunur. Sorgu ve sayfa tablolarında click/pozisyon değişimi verilirken
> **o değişimin ne kadar hacme tekabül ettiği** de gösterilir. Hacim olmadan
> "pozisyon 3 basamak iyileşti" cümlesi büyüklük taşımaz: 200 hacimli bir
> kelimede de 40.000 hacimli bir kelimede de aynı görünür.

## Kaynak sırası

Sırayla denenir, ilk veri dönen kullanılır. Her sorgu için hangi kaynaktan
geldiği kaydedilir - sütun adına ve kaynak notuna yazılacak.

### 1. SEOmonitor (birinci tercih)

Marka için zaten takip edilen kelimelerin hacmi buradadır; ayrıca müşteriye
gösterilen panelle aynı sayıyı verdiği için tutarlılık sağlar.

```
mcp__*__seomonitor_get_keyword_data
  campaign_id, start_date, end_date, order_by="search_volume"
  → satırlarda search_volume
mcp__*__seomonitor_find_keywords   # belirli sorguları aramak için
```

**Kapsam sınırı:** yalnızca **takip edilen** kelimeler. Search Console'dan gelen
hareket listesinde takip edilmeyen sorgular çıkar; onlar bir sonraki kaynağa
düşer. Kaç sorgunun SEOmonitor'de bulunduğu dipnotta yazılır.

`include_monthly_searches` yalnızca 13 aylık seri gerektiğinde açılır; tek
dönem hacmi için gereksiz yük.

### 2. Ahrefs (SEOmonitor'de bulunmayanlar)

```
mcp__*__keywords-explorer-overview
  select="keyword,volume", keywords="<satır satır sorgular>", country="tr"
```

Takip listesi dışındaki sorguları da kapsar. Değerler SEOmonitor'den farklı
seviyede olabilir - bu yüzden **aynı tabloda iki kaynağın sayısı karıştırılmaz**;
hangi satırın nereden geldiği sütun adında ayrışır (aşağıya bak).

### 3. DataForSEO (ikisi de yoksa)

```
POST /v3/keywords_data/google_ads/search_volume/live
  keywords[], location_code, language_code, search_partners=false
```

Yerel betik: `scripts/hacim_dfs.py` - MCP bağlı olmasa da REST üzerinden çalışır.

**İki tuzağı var, ikisi de tabloya yansır:**
- **Bant etkisi:** Google Ads hacmi basamaklı döndürür (2.900 / 3.600 / 4.400 …).
  Ay bazında değişim yazılmaz, ısı haritası kullanılmaz.
- **Yakın varyant birleşmesi:** Google Ads yazım varyantlarını tek keyword
  sayar; "gameplus" ile "game plus" aynı seriyi döndürebilir. Toplama girecek
  terimler önce karşılaştırılır, aynıysa biri elenir (bkz. tuzaklar 2.9c).

## Etiketleme - zorunlu

Hacim hangi kaynaktan geldiyse **görünür olmalı**. Üç kural:

1. **Tek kaynak kullanıldıysa** sütun adı sade kalır, kaynak notuna eklenir:

   | Sorgu | Click Tem'26 | Δ Click | Pozisyon | **Arama hacmi** |

   `Kaynak: Google Search Console & SEOmonitor`

2. **Birden fazla kaynak karıştıysa** sütun adı kaynağı taşır ve satır bazında
   ayrışır:

   | Sorgu | Δ Click | **Hacim (SEOmonitor)** | **Hacim (DfS)** |

   Ya da tek sütun + kaynak kolonu:

   | Sorgu | Δ Click | Hacim | **Hacim kaynağı** |

   İkinci biçim uzun listelerde daha okunur; kısa tabloda birinci tercih edilir.

3. **Kaynak notu her zaman hangi hacmin nereden geldiğini söyler:**

   > Kaynak: Google Search Console (click, pozisyon) & SEOmonitor (takip edilen
   > 41 sorgunun hacmi) & arama motoru veri kaynağı (kalan 12 sorgu)

DataForSEO müşteri çıktısında araç adıyla anılmaz; "arama motoru veri kaynağı"
ya da verinin geldiği yer olan "Google Ads Keyword Planner" yazılır
(bkz. icerik-dili-rehberi Bölüm 12).

## Hacim bulunamayan satır

`-` yazılır, sıfır yazılmaz. Dipnotta kaç satırda hacim bulunamadığı belirtilir.
Tahmini bir değer üretilmez.

## Insight'a nasıl bağlanır

Hacim, değişimin büyüklüğünü çerçevelemek için kullanılır - kendi başına bir
bulgu değildir:

> ➔ Pozisyonu en çok iyileşen sorgular {b:8.2K toplam aylık hacim} taşıyan
>   kümededir; iyileşmenin click karşılığı bu nedenle {g:+1.4K} seviyesindedir.

> ➔ Click kaybının yoğunlaştığı sorgular {b:1.1K hacim} bandındadır; kaybın
>   mutlak etkisi sınırlı kalmaktadır.

Yasak kullanım: hacimden click tahmini üretmek ("hacmin %30'u alınabilir").
Hedef verilecekse bant olarak ve ayrı bir fırsat slaytında verilir.
