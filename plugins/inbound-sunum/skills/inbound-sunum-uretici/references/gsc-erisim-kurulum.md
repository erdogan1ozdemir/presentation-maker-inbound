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
bash /skill/yolu/scripts/kur_gsc.sh
```

Betik sanal ortamı kurar, bağımlılıkları yükler, sunucunun ayağa kalktığını
araçları sayarak doğrular ve `claude mcp add` komutunu tam yollarla yazdırır.
Token dosyası elinizdeyse tek adımda kaydı da yapar:

```bash
bash /skill/yolu/scripts/kur_gsc.sh /yol/gsc_token.json
```

Sunucunun altı aracı var, hepsi okuma: `list_properties`, `search_analytics`
(regex filtreli), `list_sitemaps`, `inspect_url`, `batch_inspect_urls`,
`indexing_issues`.

### Hangi yol kaydedilmeli - dikkat

Eklenti marketplace'ten kurulduğunda dosyalar **sürüm numaralı** bir önbelleğe
açılır:

```
~/.claude/plugins/cache/presentation-maker-inbound/inbound-sunum/1.6.0/...
                                                              ^^^^^ her sürümde değişir
```

Buraya kaydedilen MCP sunucusu **ilk eklenti güncellemesinde kırılır**. İki
kalıcı yol var:

| Yol | Nasıl güncellenir |
|---|---|
| `~/.claude/plugins/marketplaces/presentation-maker-inbound/plugins/inbound-sunum/skills/inbound-sunum-uretici/scripts` | `claude plugin marketplace update` ile yerinde (git clone) |
| Kendi klonunuz, ör. `~/inbound-sunum/plugins/.../scripts` | `git pull` |

`kur_gsc.sh` sürümlü önbellekten çalıştırıldığını fark ederse uyarır ve
kalıcı yolları yazdırır.

### MCP sunucusu skill'den bağımsız çalışır

`claude mcp add` ile bir kez kaydedildikten sonra sunucu **her oturumda**
açıktır; sunum skill'ini çağırmak gerekmez. Ekipteki biri "son üç ayın en çok
click alan sorgularını getir" dediğinde veri doğrudan gelir. Skill yalnızca
sunum üretimi için gerekli; Search Console verisine erişim ondan bağımsızdır.

## Hangi kimlik yolu

**Ajans standardı: ekibin ortak Drive'ındaki `token.json` kullanılır.** Bu dosya
`seo.op@inbound.com.tr` hesabının Search Console erişimidir; `client_id`,
`client_secret` ve `refresh_token`'ı kendi içinde taşıdığı için tek başına
yeterlidir. Google Cloud'a girilmez, tarayıcıdan onay verilmez.

| | Drive'daki token (standart) | client_secrets + kendi onayı | Servis hesabı |
|---|---|---|---|
| Kişinin adımı | Dosyayı kopyala, tek komut | Tarayıcıdan bir kez onay | Dosyayı yerine koy |
| Tüm domainlere erişim | Var | Var (seo.op@ ile girilirse) | Yalnızca hesaba açılanlar |
| Kişi bazında iptal | Yok | Var | Yok |
| Ne zaman | Varsayılan | Drive'a erişim yoksa | Merkezi, property bazlı yönetim gerekirse |

### Yol A - Drive'daki token (standart)

**Adım 1 - Dosyayı bul.** Ekibin ortak Drive'ında `token.json`.

**Adım 2 - Kendi bilgisayarına kopyala.** Ana klasöre `gsc_token.json` adıyla:

```bash
cp "/Drive/klasörünün/yolu/token.json" ~/gsc_token.json
```

**Drive'daki dosyayı doğrudan gösterme.** Sunucu token'ı yaklaşık saatte bir
yeniliyor ve dosyanın üzerine yazıyor. Drive yolu gösterilirse bu yazma işlemi
herkese senkronlanmaya çalışır, "çakışan kopya" dosyaları oluşur ve hangisinin
geçerli olduğu karışır. Yerel kopyada böyle bir sorun yok - aynı token'ın
farklı bilgisayarlardan kullanılması Google tarafında sorun değil.

**Adım 3 - Kur.**

```bash
bash ~/.claude/plugins/marketplaces/presentation-maker-inbound/plugins/inbound-sunum/skills/inbound-sunum-uretici/scripts/kur_gsc.sh ~/gsc_token.json
```

Claude Code yeniden başlatılır, `claude mcp list` ile `gsc: ✔ Connected`
görülür.

**Güvenlik ağı:** yanlışlıkla Drive, iCloud, Dropbox ya da OneDrive yolu
verilirse `kur_gsc.sh` bunu fark eder, dosyayı `~/gsc_token.json`'a kopyalar ve
kaydı yerel kopyaya yapar. Drive'daki dosyaya dokunulmaz.

**Drive klasörünün erişimi:** token 100'ü aşkın müşteri property'sinin Search
Console verisini okuyabiliyor. Klasör yalnızca iç ekiple paylaşılır; "bağlantıya
sahip olan herkes" ayarında ya da bir müşteriyle paylaşılan klasörde durmaz.

### Yol B - client_secrets + kendi onayı

Drive'a erişimi olmayan biri için. `client_secrets.json` Google Cloud'dan
indirilir ya da mevcut bir token'dan üretilir:

```bash
python3 <skill-klasoru>/scripts/client_secrets_cikar.py /yol/token.json -o client_secrets.json
```

Ardından:

```bash
bash <skill-klasoru>/scripts/kur_gsc.sh --oauth /yol/client_secrets.json
```

İlk çağrıda tarayıcı açılır, `seo.op@inbound.com.tr` ile giriş yapılır, izin
verilir. Kişinin kendi token'ı yerel olarak oluşur.

### Yol C - Servis hesabı

Erişimin property bazında ve merkezden yönetilmesi isteniyorsa. Servis hesabı
oluşturulur, e-postası Search Console'da property'lere "Kısıtlı" izinle
eklenir, JSON anahtar `GSC_CREDENTIALS_PATH` ile verilir. Tarayıcı onayı
yoktur; ancak yalnızca kendisine açılan property'leri görür, her yeni marka
için ekleme gerekir.

#### Consent screen durumu - adım adım

`seo.op@inbound.com.tr` hesabıyla giriş yapılmış olmalı.

1. [console.cloud.google.com](https://console.cloud.google.com) açılır.
2. Sol üstte **proje seçici**den ilgili proje seçilir (yeni açtıysanız o proje).
3. Sol menü **☰ → APIs & Services → OAuth consent screen** (yeni arayüzde
   **APIs & Services → Google Auth Platform → Audience**).
4. Sayfada **User type** ya da **Audience** başlığı görünür. İki durum var:

   **a) "Internal" seçilebiliyorsa** - Workspace hesabında normal olan budur.
   Seçin ve kaydedin. Bu durumda:
   - Refresh token 7 günde düşmez, kalıcıdır.
   - Yalnızca `@inbound.com.tr` hesapları giriş yapabilir - dışarıya kapalıdır.
   - Doğrulama (verification) süreci gerekmez.

   **b) "Internal" gri/seçilemez durumdaysa** - proje bir Workspace
   organizasyonuna bağlı değil demektir. O zaman **External** kalır ve
   **Publishing status** başlığına bakılır:
   - **Testing** yazıyorsa **PUBLISH APP** düğmesine basılır, çıkan uyarı
     onaylanır. Durum **In production** olur ve refresh token kalıcı hale gelir.
   - Yalnızca `webmasters.readonly` kapsamı istendiği için Google'ın
     "sensitive/restricted scope" doğrulaması **gerekmez**; uygulama doğrulama
     beklemeden çalışır. Giriş ekranında "doğrulanmamış uygulama" uyarısı
     çıkabilir, **Gelişmiş → devam et** ile geçilir.

5. Kontrol: sayfada durum **Internal** ya da **In production** görünüyorsa
   tamamdır. **Testing** görünüyorsa 4. adım tamamlanmamıştır.

**Belirti:** erişim yaklaşık haftada bir kesiliyor ve sunucu "Token geçersiz
ve yenilenemiyor" diyorsa bakılacak yer tam olarak burasıdır.

### Kişisel OAuth - kendi hesabıyla

Bir kişi `seo.op@` yerine kendi `@inbound.com.tr` hesabıyla çalışacaksa aynı
adımlar izlenir; o durumda yalnızca kendi eriştiği property'ler görünür.

## Google Cloud tarafı - bir kez, tek kişi

1. [console.cloud.google.com](https://console.cloud.google.com) → yeni proje
   oluştur (ör. `gsc-mcp`).
2. **APIs & Services → Library** → "Google Search Console API" → **Enable**.
3. **APIs & Services → OAuth consent screen** → User type **Internal**.
   Uygulama adı ve destek e-postası doldurulur. Internal seçilemiyorsa
   yukarıdaki "Consent screen durumu" bölümüne bakılır - orada External
   durumunda ne yapılacağı yazılı.
4. **Scopes** adımında elle kapsam eklemeye gerek yoktur; kapsamı uygulama
   isteyecek (`webmasters.readonly`).
5. **APIs & Services → Credentials → Create credentials → OAuth client ID** →
   Application type **Desktop app** → oluştur → **JSON'u indir**.
6. Dosya `client_secrets.json` adıyla saklanır ve ekiple paylaşılır.

### Kurulum ve kayıt

Her kişi kendi makinesinde tek komut çalıştırır:

```bash
bash /skill/yolu/scripts/kur_gsc.sh --oauth /yol/client_secrets.json
```

İlk çağrıda tarayıcı açılır, `seo.op@inbound.com.tr` hesabıyla giriş yapılır,
izin verilir. Onay sonrası token yerel olarak yazılır ve bir daha sorulmaz.

Onay ekranında "Google bu uygulamayı doğrulamadı" uyarısı çıkarsa: kendi
oluşturduğunuz uygulama olduğu için normaldir - **Gelişmiş → devam et**.

### Doğrulama

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

- `client_secrets.json` ekip içinde paylaşılır ama **repoya konmaz**. Bir
  kişiyi değil uygulamayı tanımladığı için hesap şifresinden daha dar bir
  bilgidir; yine de dışarıya çıkmaması gerekir - sızarsa Google Cloud'dan
  client secret iptal edilip yenisi üretilir ve ekip yeniden onay verir.
- Üretilen token dosyaları **kişiye özeldir**, paylaşılmaz. Yol B seçildiyse
  paylaşılan token bir sırdır ve kasadan dağıtılır.
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
