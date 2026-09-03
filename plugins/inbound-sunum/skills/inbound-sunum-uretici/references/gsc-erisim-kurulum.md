# Google Search Console erişimi - kurulum

> Faz 1'de okunur. Ekipteki bir kişi bu skill'i ilk kez kullanıyorsa ve Search
> Console'a canlı erişimi yoksa, **önce bu kurulum önerilir** - tek seferlik bir
> işlem ve sonrasında tüm destelerde veri elle export edilmeden çekilir.

## İki yol, tek tercih

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
2. **Property izni:** Search Console'da kişiye verilen izin ayrıca
   sınırlanabilir. Property sahibi **Ayarlar → Kullanıcılar ve izinler**'den
   "Kısıtlı" (Restricted) izni verirse kişi raporları görür, ayar değiştiremez.

İkisi birlikte: token yazma yetkisi taşımaz, kullanıcı da yazma izni almaz.

## Kurulum

Aşağıdaki adımlar kişinin kendi makinesinde bir kez yapılır.

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

### 2. Sunucu kurulumu

```bash
git clone https://github.com/AminForou/mcp-gsc.git
cd mcp-gsc
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

`client_secrets.json` bu klasörün içinde durmalı.

### 3. Claude Code'a tanıtma

```bash
claude mcp add gsc -s user -- /TAM/YOL/mcp-gsc/.venv/bin/python /TAM/YOL/mcp-gsc/gsc_server.py
```

`-s user` önemli: sunucu tüm projelerde açık olur, her klasörde yeniden
tanıtmak gerekmez.

### 4. İlk çalıştırma - tek seferlik onay

Claude Code yeniden başlatılır ve bir GSC aracı çağrılır (ör. "Search Console
property listesini getir"). Tarayıcıda Google onay ekranı açılır, hesap seçilir
ve izin verilir. Onay sonrası klasöre `token.json` yazılır; **bir daha
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

- `client_secrets.json` ve `token.json` **kişiye özeldir**, repoya konmaz,
  paylaşılmaz. Her kullanıcı kendi onayını verir.
- Bir kişinin token'ı yalnızca **o kişinin Search Console'da erişebildiği**
  property'leri görür. Yeni bir markaya erişim, property sahibinin o kişiyi
  Search Console'dan kullanıcı olarak eklemesiyle açılır.
- Servis hesabı (service account) alternatifi de desteklenir: tek bir hesap
  oluşturulup e-posta adresi property'lere "Kısıtlı" izinle eklenir, JSON anahtar
  `GSC_CREDENTIALS_PATH` ile verilir. Ekipte tek merkezden yönetmek isteniyorsa
  bu yol tercih edilir; kapsam yine `webmasters.readonly` kalır.
