# Önceki Uygulamalar

`loft-generate_presentation.py` - Loft aylık destesinin üretiminde kullanılan ilk
implementasyon. python-pptx ile mevcut şablonu düzenler, grafikleri matplotlib ile
PNG olarak üretir.

Burada referans olarak duruyor çünkü skill'in bugünkü mimarisi bu yaklaşımın
sınırlarından çıktı:

- **Şablon düzenleme yerine bildirimsel üretim.** Şablon slaytlarını klonlayıp içini
  temizlemek, her yeni deste tipinde elle koordinat ayarı gerektiriyordu. Bugün deste
  `deck.json` ile tanımlanıyor, yerleşim ölçümle hesaplanıyor.
- **PNG grafik yerine düzenlenebilir vektör şekil.** matplotlib PNG'si sunum içinden
  düzenlenemiyor ve her değişiklik yeniden export gerektiriyor.
- **Renk paleti.** Bu script kendi mavi paletini kullanıyor; bugün Inbound Design
  System token'ları esas.
- **Görsel doğrulama yok.** Bugün aynı tanımdan HTML önizleme üretiliyor ve taşma
  gerçek font metriğiyle ölçülüyor.

Veri okuma yaklaşımı (GA4 CSV'sinin çok dönemli başlık bloklarını ayrıştırma,
`# Start date` satırlarını okuma) hâlâ geçerli ve `veri_tara.py` içinde yaşıyor.
