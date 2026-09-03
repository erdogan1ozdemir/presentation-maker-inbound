# Arama hacmi: tek kaynak, tek talep, tarih etiketi

> Faz 2'de okunur. Sorgu tablolarında click/pozisyon değişimi verilirken **o
> değişimin ne kadar hacme tekabül ettiği** de gösterilir. Hacim olmadan
> "pozisyon 3 basamak iyileşti" cümlesi büyüklük taşımaz: 200 hacimli kelimede
> de 40.000 hacimli kelimede de aynı görünür.

## Üç kural

### 1. Bir destede tek kaynak

Hacim **tek bir kaynaktan** alınır. Satır satır farklı kaynak karıştırılmaz:
iki aracın hacim modeli farklıdır, aynı kolonda yan yana durunca tablo
kıyaslanamaz hale gelir ve okuyucu hangi sayının neyle karşılaştırılabilir
olduğunu bilemez.

Kaynak deste başında **bir kez** seçilir, sırayla denenir:

| Sıra | Kaynak | Ne zaman seçilir |
|---|---|---|
| 1 | SEOmonitor | Marka için kampanya var ve gereken kelimelerin **tamamı** takip ediliyorsa. Müşteriye gösterilen panelle aynı sayıyı verir |
| 2 | Ahrefs | SEOmonitor kapsamı yetmiyorsa (takip dışı kelimeler var) |
| 3 | DataForSEO | İkisi de erişilemiyorsa |

**Kapsam kontrolü seçimden önce yapılır:** gereken kelime listesi çıkarılır,
SEOmonitor'de kaçının bulunduğuna bakılır. Bir kısmı eksikse SEOmonitor
**tamamen** bırakılır ve bir sonraki kaynağa geçilir - yarısı bir yerden
yarısı başka yerden alınmaz.

Bir destede iki farklı hacim kaynağı yalnızca **iki ayrı bölüm** birbirinden
tamamen bağımsızsa kullanılabilir (ör. marka hacmi slaytı ile rakip hacmi
slaytı); o durumda her bölümün kaynak notu kendi kaynağını yazar ve iki bölüm
arasında karşılaştırma yapılmaz.

### 2. Tek seferde tek talep

Hacim gereken kelimeler **toplanır, tek çağrıda istenir.** Sorgu başına ayrı
çağrı yapılmaz.

Toplama sırası:
1. Hangi slaytlarda hacim kolonu olacak, belirlenir (C30, C47, C33, C04-C08).
2. Bütün bu slaytların kelimeleri **tek listeye** yazılır, tekilleştirilir.
3. Liste tek çağrıyla gönderilir; sonuç bir sözlüğe alınır ve tüm slaytlar
   aynı sözlükten okur.

```bash
# DataForSEO seçildiyse: tek dosya, tek çağrı
python3 scripts/hacim_dfs.py --kelime-dosyasi kelimeler.txt --json hacim.json
```

SEOmonitor'de `get_keyword_data` tek çağrıda 1.000 satıra kadar döner; Ahrefs
`keywords-explorer-overview` çok satırlı `keywords` parametresi alır;
DataForSEO tek istekte 700-1.000 kelime kabul eder. Üçünde de tek çağrı
yeterlidir.

Aynı kelime iki slaytta geçiyorsa **bir kez** istenir ve iki slaytta aynı
değer görünür - aynı kelimenin iki slaytta farklı hacimle görünmesi geçmişte
yaşanmış bir teslim hatasıdır.

### 3. Hacmin dönemi yazılır

Arama hacmi bir dönem değeridir; hangi döneme ait olduğu yazılmazsa okuyucu
onu cari ayın değeri sanar. **Kolon adı dönemi taşır:**

| Biçim | Ne zaman | Örnek kolon adı |
|---|---|---|
| Tek ay | Belirli bir ayın hacmi alındıysa | `Arama hacmi (2026 Temmuz)` |
| Yıl ortalaması | Yılın aylık ortalaması alındıysa | `Arama hacmi (2026 ort. aylık)` |
| Dönem ortalaması | Rapor dönemi ortalaması | `Arama hacmi (2026 Q2 ort. aylık)` |
| 12 ay ortalaması | Araç varsayılanı 12 aylık ortalama döndürüyorsa | `Arama hacmi (son 12 ay ort.)` |

Kaynak notu hem kaynağı hem dönemi tekrarlar:

> Kaynak: Google Search Console (click, pozisyon) & SEOmonitor (arama hacmi,
> 2026 Temmuz)

**Hangi aracın ne döndürdüğü:**
- **SEOmonitor** `search_volume`: son 12 ayın aylık ortalaması.
  `include_monthly_searches` ile aylık seri de alınabilir - tek ay gerekiyorsa
  bu açılır ve kolon adına o ay yazılır.
- **Ahrefs** `volume`: son ayın değeri; `volume-history` ile aylık seri.
- **DataForSEO** `search_volume`: son 12 ayın ortalaması;
  `monthly_searches` dizisi aylık seriyi taşır. `date_from`/`date_to` verilerek
  dönem daraltılabilir.

Varsayılanı bilmeden "arama hacmi" yazmak, farklı dönemleri aynı kolonda
göstermek demektir. Araç varsayılanı kullanılacaksa kolon adına ortalama
olduğu yazılır.

## Kaynak bazlı çağrı kalıpları

### SEOmonitor
```
mcp__*__seomonitor_get_keyword_data
  campaign_id, start_date, end_date, limit=1000, order_by="search_volume"
  include_monthly_searches=true   # yalnizca tek ay veya seri gerekiyorsa
```
Kapsam: yalnızca takip edilen kelimeler.

### Ahrefs
```
mcp__*__keywords-explorer-overview
  select="keyword,volume", keywords="<satır satır>", country="tr"
```

### DataForSEO
```
scripts/hacim_dfs.py --kelime-dosyasi <dosya> [--ilk-tarih 2026-07-01 --son-tarih 2026-07-31]
```
İki tuzağı tabloya yansır:
- **Bant etkisi:** değerler basamaklı döner (2.900 / 3.600 / 4.400 …). Ay
  bazında değişim yazılmaz, ısı haritası kullanılmaz.
- **Yakın varyant birleşmesi:** yazım varyantları tek keyword sayılabilir;
  betik bunu tespit edip uyarır (bkz. tuzaklar 2.9c).

## Hacim bulunamayan satır

`-` yazılır, sıfır yazılmaz, tahmin üretilmez. Dipnotta kaç satırda hacim
bulunamadığı belirtilir. Kelime listesinin önemli bir bölümü boş dönüyorsa
kaynak seçimi gözden geçirilir.

## Nerede kullanılır, nerede kullanılmaz

**Kullanılır:** sorgu bazlı tablolar (C30, C47, C33), marka ve kategori hacmi
slaytları (C04-C08).

**Kullanılmaz:** sayfa bazlı tablolar. Bir sayfa tek bir kelimeye karşılık
gelmez; sayfa için hacim toplamak yanıltıcı olur.

## Insight'a nasıl bağlanır

Hacim, değişimin büyüklüğünü çerçeveler - kendi başına bulgu değildir:

> ➔ Pozisyonu en çok iyileşen sorgular {b:8.2K aylık hacim} taşıyan kümededir;
>   iyileşmenin click karşılığı bu nedenle {g:+1.4K} seviyesindedir.

> ➔ Click kaybının yoğunlaştığı sorgular {b:1.1K hacim} bandındadır; kaybın
>   mutlak etkisi sınırlı kalmaktadır.

Yasak kullanım: hacimden click tahmini üretmek ("hacmin %30'u alınabilir").
Hedef verilecekse bant olarak ve ayrı bir fırsat slaytında verilir.
