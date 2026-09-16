# inbound-sunum

Inbound ajans standardında SEO/GEO performans değerlendirme sunumu (PPTX) üreten
Claude Code plugin'i. Tek skill içerir: `inbound-sunum-uretici`.

Kurulum ve kullanım: reponun kökündeki [README](../../README.md).

## Bağımlılıklar

- `icerik-dili-rehberi` skill'i - dil ve ton standardı
- python-pptx, Pillow

`skills/inbound-sunum-uretici/scripts/setup_deps.sh` ikisini de denetler ve kurar.

## Güncelleme

Plugin oturum başında kendini günceller (`hooks/hooks.json` → `SessionStart`
→ `scripts/otomatik_guncelle.sh`): marketplace için Claude Code'un arka plan
güncellemesini açar (`settings.json` → `extraKnownMarketplaces.presentation-maker-inbound.autoUpdate`)
ve kurulu sürüm GitHub'dakinden geriyse `claude plugin update` ile hemen
günceller. Güncelleme olduğunda oturum notu düşer; yeni sürüm `/reload-plugins`
ile ya da bir sonraki oturumda yüklenir. Kapatmak için `INBOUND_OTO_GUNCELLE=0`.

Üretici ve denetim betikleri (`inbound_deck.py`, `qa_deck.py`) sürümü ayrıca
kontrol eder ve eski sürümle çalışmaz. claude.ai tarafında (zip) otomatik
güncelleme yoktur; `dist/` altındaki güncel zip elle yüklenir.
