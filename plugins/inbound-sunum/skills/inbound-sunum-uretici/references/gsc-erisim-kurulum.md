# Google Search Console erişimi - kurulum

> Faz 1'de okunur. Ekipteki bir kişi bu skill'i ilk kez kullanıyorsa ve Search
> Console'a canlı erişimi yoksa, **önce bu kurulum önerilir** - tek seferlik bir
> işlem ve sonrasında tüm destelerde veri elle export edilmeden çekilir.

## Canlı erişim mi, elle export mu

| | Canlı erişim (OAuth) | Elle export |
|---|---|---|
| Kurulum | Bir kez, ~15 dakika | Yok |
| Her deste için | Hiçbir şey | Her dönem için ayrı CSV indirme |
| Kapsam | 16 ay, tüm kırılımlar, regex filtresi | İndirilen dosyada ne varsa |
| Segment ölçümü | `includingRegex` / `excludingRegex` ile kesin | Elle sınıflandırma, anonim sorgu kaçağı |
| Hata riski | Düşük | Dönem/kapsam karışması sık yaşanıyor |

**Varsayılan öneri OAuth'tur.** Elle export yalnızca kurulum yapılamayan
durumlarda (erişim izni verilmemiş, kurumsal kısıt) kullanılır.

## Erişim yalnızca okuma iznidir

Kurulum iki katmanda da okumayla sınırlıdır; yanlışlıkla bir şey değiştirme
ihtimali yoktur:

1. **Token kapsamı:** sunucu yalnızca
   `https://www.googleapis.com/auth/webmasters.readonly` kapsamını ister. Google
   onay ekranında da "Search Console verilerinizi görüntüleme" olarak görünür.
   Bu kapsamla site ekleme/silme, sitemap gönderme/silme API tarafından
   reddedilir - token bu işlemleri yapamaz.

   **Kapsam token'ın içindedir, paylaşan kişiye göre değişmez.** Bir token
   nerede üretildiyse oradaki kapsamı taşır; başka bir araçla tam
   `webmasters` kapsamıyla üretilmiş bir token yazma yetkisi taşır. Bu yüzden
   sunucu, verilen token dosyasının kapsamını okuyup denetler ve geniş
   kapsamlı token'la **çalışmayı reddeder**.
2. **Property izni:** Search Console'da kişiye verilen izin ayrıca
   sınırlanabilir. Property sahibi **Ayarlar → Kullanıcılar ve izinler**'den
   "Kısıtlı" (Restricted) izni verirse kişi raporları görür, ayar değiştiremez.

İkisi birlikte: token yazma yetkisi taşımaz, kullanıcı da yazma izni almaz.

## Sunucu skill'in içinde - harici repo gerekmez

Search Console MCP sunucusu bu skill'le birlikte gelir:
`scripts/gsc_mcp.py`. Tek dosya, harici bir depo klonlanmaz. Sunucu yalnızca
okuma araçları tanımlar (`list_properties`, `search_analytics`,
`list_sitemaps`, `inspect_url`); site ekleme veya sitemap gönderme aracı
**hiç yoktur**.

```bash
cd /skill/yolu/scripts
python3 -m venv .venv
.venv/bin/pip install "mcp>=1.6.0" google-api-python-client google-auth google-auth-oauthlib
```

## Hangi kimlik yolu

Üç yol desteklenir. **Ajans içinde tercih edilen yol, tek kurumsal hesabın
token'ının ekiple paylaşılmasıdır** (`seo.op@inbound.com.tr`): bir kez
üretilir, herkes aynı dosyayı kullanır, kimse onay ekranı görmez ve o hesabın
eriştiği bütün property'ler tek seferde açılır.

| | Paylaşılan kurumsal token | Servis hesabı | Kişisel OAuth |
|---|---|---|---|
| Kurulum | Bir kez merkezden, ekip dosyayı alır | Bir kez merkezden | Her kişi kendi onayını verir |
| Property erişimi | Hesabın eriştiği her şey | Yalnızca hesaba açılan property'ler | Kişinin eriştiği property'ler |
| Yeni marka | Hesap zaten erişiyorsa ek iş yok | Property'ye hesap eklenir | Her kişi ayrı eklenir |
| İz | Tüm ekip tek kullanıcı olarak görünür | Tek servis kullanıcısı | Kişi bazında |

### Yol A - Paylaşılan kurumsal hesap token'ı (ajans standardı)

**Salt okunur mu? Evet - ama koşullu.** Kapsam token'ın içine gömülür, onu
paylaşan kişiye göre değişmez. Token bu skill'in sunucusuyla üretildiğinde
kapsam `webmasters.readonly` olur ve token yazma çağrısı yapamaz. Başka bir
yerde (OAuth Playground, başka bir uygulama) tam `webmasters` kapsamıyla
üretilmiş bir token yazma yetkisi taşır - bu yüzden sunucu token dosyasının
kapsamını **okuyup denetler**, geniş kapsamlı token'la çalışmayı reddeder.

Adımlar - bir kez, tek kişi yapar:

1. Google Cloud'da bir proje ve **Desktop app** OAuth client oluştur, Search
   Console API'yi aç (aşağıdaki "Google Cloud tarafı" adımları).
2. **OAuth consent screen → User type: Internal** seç. Bu adım kritik:
   uygulama **"Testing"** durumunda kalırsa Google refresh token'ı **7 günde**
   düşürür ve ekip her hafta yeniden onay vermek zorunda kalır. Workspace
   hesabıyla Internal seçilebiliyorsa sorun ortadan kalkar; seçilemiyorsa
   uygulama **"In production"** durumuna alınır.
3. Token'ı `seo.op@inbound.com.tr` hesabıyla bir kez üret:

```bash
claude mcp add gsc -s user \
  -e GSC_OAUTH_CLIENT_SECRETS=/yol/client_secrets.json \
  -e GSC_TOKEN_PATH=/yol/gsc_token.json \
  -- /skill/yolu/scripts/.venv/bin/python /skill/yolu/scripts/gsc_mcp.py
```

İlk çağrıda tarayıcı açılır, `seo.op@` hesabıyla giriş yapılır, izin verilir.
Onay ekranında istenen tek kapsam "Search Console verilerinizi görüntüleme"
olmalı - başka bir kapsam görünüyorsa devam edilmez.

4. Oluşan `gsc_token.json` ekiple paylaşılır. Dosya `client_id` ve
   `client_secret`'i de taşır, bu yüzden **tek başına yeterlidir**; ekibin
   ayrıca `client_secrets.json`'a ihtiyacı yoktur.

5. Ekipteki her kişi yalnızca şunu çalıştırır:

```bash
claude mcp add gsc -s user \
  -e GSC_TOKEN_PATH=/yol/gsc_token.json \
  -- /skill/yolu/scripts/.venv/bin/python /skill/yolu/scripts/gsc_mcp.py
```

Tarayıcı açılmaz, onay istenmez. Token süresi dolduğunda kendini yeniler.

**Paylaşılan token bir sırdır.** Parola gibi davranılır: repoya konmaz,
Slack'e/e-postaya açık atılmaz, 1Password gibi bir kasadan dağıtılır. Sızarsa
Google Cloud'dan client secret iptal edilir ve token yeniden üretilir. Tek
token paylaşıldığı için kişi bazında iptal yoktur - biri ayrıldığında token
yenilenir ve yeni dosya dağıtılır.

### Yol B - Servis hesabı

Erişimin merkezden ve property bazında yönetilmesi isteniyorsa. Servis hesabı
oluşturulur, e-posta adresi Search Console'da property'lere "Kısıtlı" izinle
eklenir, JSON anahtar `GSC_CREDENTIALS_PATH` ile verilir. Tarayıcı onayı
yoktur. Kurumsal hesap token'ından farkı: yalnızca kendisine açılan
property'leri görür, bu yüzden her yeni marka için Search Console'dan ekleme
gerekir.

### Yol C - OAuth (kişisel kullanım)

Kişi yalnızca kendi eriştiği property'lerle çalışacaksa. Adımlar aşağıda.

### 1. Google Cloud tarafı

1. [console.cloud.google.com](https://console.cloud.google.com) → yeni proje
   oluştur (ör. `gsc-mcp`).
2. **APIs & Services → Library** → "Google Search Console API" → **Enable**.
3. **APIs & Services → OAuth consent screen** → User type **External** →
   uygulama adı ve destek e-postası doldurulur. Yayınlamaya gerek yok; **Test
   users** bölümüne kendi Google hesabını ekle.
4. **Scopes** adımında elle kapsam eklemeye gerek yoktur; kapsamı uygulama
   isteyecek (`webmasters.readonly`).
5. **APIs & Services → Credentials → Create credentials → OAuth client ID** →
   Application type **Desktop app** → oluştur → **JSON'u indir**.
6. İndirilen dosyayı `client_secrets.json` adıyla sunucu klasörüne koy.

### 2. Ortam değişkeni

`client_secrets.json` indirildikten sonra bir yere konur; yolu ortam
değişkeniyle verilecek.

### 3. Claude Code'a tanıtma

```bash
claude mcp add gsc -s user \
  -e GSC_OAUTH_CLIENT_SECRETS=/yol/client_secrets.json \
  -- /skill/yolu/scripts/.venv/bin/python /skill/yolu/scripts/gsc_mcp.py
```

`-s user` önemli: sunucu tüm projelerde açık olur, her klasörde yeniden
tanıtmak gerekmez.

### 4. İlk çalıştırma - tek seferlik onay

Claude Code yeniden başlatılır ve bir GSC aracı çağrılır (ör. "Search Console
property listesini getir"). Tarayıcıda Google onay ekranı açılır, hesap seçilir
ve izin verilir. Onay sonrası `gsc_token.json` yazılır; **bir daha
sorulmaz**, token kendini yeniler.

Onay ekranında "Google bu uygulamayı doğrulamadı" uyarısı çıkarsa: kendi
oluşturduğunuz test uygulaması olduğu için normaldir - **Gelişmiş → devam et**.

### 5. Doğrulama

```bash
claude mcp list
```

`gsc: ... ✔ Connected` görünmeli. Ardından property listesi çekilerek markanın
property'sinin göründüğü teyit edilir.

## Kurulum yapılamıyorsa - elle export

Kişinin Google Cloud projesi açma yetkisi yoksa ya da property'ye erişimi
verilmediyse veri elle istenir. Hangi rapor, hangi kırılım, hangi tarih
aralığı - tam talimatlar `veri-brief-ve-export.md` içindedir. Bu durumda
segment ölçümünde regex kullanılamayacağı için brand/non-brand ayrımının
elle yapılacağı ve anonim sorgu kaçağının oluşacağı kullanıcıya söylenir
(bkz. `tuzaklar-ve-qa.md` 2.9b).

## Ekip içi paylaşımda dikkat

- Paylaşılan kurumsal token bir **sırdır**: repoya konmaz, açık kanaldan
  gönderilmez, kasadan dağıtılır. Kişisel OAuth kullanılıyorsa
  `client_secrets.json` ve token dosyası kişiye özeldir, paylaşılmaz.
- **Refresh token ömrü:** OAuth consent screen "Testing" durumundaysa Google
  refresh token'ı 7 günde düşürür ve erişim kesilir. Workspace hesabında
  **Internal** user type seçilerek ya da uygulama **In production** durumuna
  alınarak kalıcı hale gelir. Erişim haftada bir kesiliyorsa bakılacak yer
  burasıdır.
- Bir kişinin token'ı yalnızca **o kişinin Search Console'da erişebildiği**
  property'leri görür. Yeni bir markaya erişim, property sahibinin o kişiyi
  Search Console'dan kullanıcı olarak eklemesiyle açılır.
- Servis hesabı JSON anahtarı ekip içinde paylaşılabilir ama **repoya konmaz**;
  parola gibi davranılır. Kaybolduğunda Google Cloud'dan iptal edilip yenisi
  üretilir.
- Servis hesabı yalnızca **Search Console'da kendisine açılmış** property'leri
  görür. `list_properties` boş dönerse eksik olan şey 4. adımdır.
