# Fontlar

`BricolageGrotesque-var.ttf` ve `Outfit-var.ttf` - Google Fonts'tan alınmış
**variable** TrueType dosyaları (OFL 1.1, lisanslar bu klasörde).

Variable font tercih edildi çünkü tek dosya tüm ağırlıkları taşıyor: PIL ölçüm
yaparken `wght` eksenini istenen ağırlığa çekiyor, HTML önizleme aynı dosyayı
`font-weight: 200 800` aralığıyla kullanıyor. Bricolage'da ayrıca `opsz` (optik
boyut) ekseni var; ölçüm sırasında punto değerine göre 12-96 arasına kırpılıyor.

## Neden değiştirildi

Önceki klasördeki `BricolageGrotesque-*.ttf` / `Outfit-*.ttf` dosyaları `.ttf`
uzantılı olmasına rağmen içerikleri **EOT** (Embedded OpenType) idi; bir pptx'in
gömülü font kaynağından çıkarılmışlardı. Sonucu:

- PIL bu dosyaları açamıyordu, dolayısıyla font ölçümü sessizce karakter
  genişliği yaklaşımına düşüyordu (gerçek metrik değil).
- HTML önizlemedeki `@font-face ... format('truetype')` tanımı da geçersizdi;
  önizleme yalnızca fontlar işletim sisteminde kurulu olduğu için doğru
  görünüyordu, başka makinede fallback'e düşerdi.

Bozuk dosyalar `../fonts-eot-bozuk/` altında referans olarak duruyor; üretimde
kullanılmıyor.

## Teslim

Sunum başka makinede açılacaksa fontların kurulu olması gerekir. Bu klasör deste
ile birlikte iletilir; variable TTF'ler doğrudan kurulabilir.
