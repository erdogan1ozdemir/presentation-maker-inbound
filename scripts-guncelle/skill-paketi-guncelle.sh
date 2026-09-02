#!/usr/bin/env bash
# Skill'i GitHub'daki son sürüme çeker ve claude.ai'ye yüklenecek zip'i üretir.
#
#   Claude Code  : plugin marketplace zaten otomatik güncelliyor, burada sadece
#                  yerel klon tazelenir ve sürüm bildirilir.
#   claude.ai    : chat, cowork ve Projects skill'leri zip yüklemesiyle çalışır;
#                  bu betik zip'i üretir, yükleme tarayıcıdan yapılır.
#
# Kullanim: bash scripts-guncelle/skill-paketi-guncelle.sh
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL="$REPO/plugins/inbound-sunum/skills/inbound-sunum-uretici"
DIST="$REPO/dist"
cd "$REPO"

echo "→ GitHub'dan çekiliyor…"
git pull --ff-only origin main

SURUM=$(python3 -c "import json;print(json.load(open('plugins/inbound-sunum/.claude-plugin/plugin.json'))['version'])")
echo "→ Sürüm: $SURUM"

# Frontmatter denetimi: claude.ai yüklemesi description içinde açı parantez
# kabul etmiyor ("SKILL.md description cannot contain XML tags"). Yer tutucu
# <marka> yazıldığında yükleme reddediliyordu; paket üretilmeden durdurulur.
python3 - "$SKILL/SKILL.md" <<'PYCHK'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"^---\n(.*?)\n---", s, re.S)
fm = m.group(1) if m else ""
kotu = re.findall(r"<[^>]+>", fm)
if kotu:
    sys.exit(f"HATA: SKILL.md frontmatter'inda aci parantez var: {kotu}. "
             "claude.ai yuklemesi bunu XML etiketi sayip reddediyor - "
             "yer tutucuyu duz metne cevir.")
print("→ frontmatter temiz")
PYCHK

mkdir -p "$DIST"
ZIP="$DIST/inbound-sunum-uretici-v$SURUM.zip"
rm -f "$ZIP"

# Geçici bir kopya üzerinde çalışılır: zip'in kökünde skill klasörü durmalı,
# claude.ai yüklemesi SKILL.md'yi orada arıyor.
TMP=$(mktemp -d)
cp -R "$SKILL" "$TMP/inbound-sunum-uretici"
find "$TMP" \( -name "__pycache__" -o -name ".DS_Store" -o -name "fonts-eot-bozuk" \) -exec rm -rf {} + 2>/dev/null || true
( cd "$TMP" && zip -qr "$ZIP" inbound-sunum-uretici )

# Açılmış kopya da tazelenir: elle açılıp bırakıldığında eskiyip yanlış sürümün
# yüklenmesine yol açıyordu.
rm -rf "$DIST/inbound-sunum-uretici"
mv "$TMP/inbound-sunum-uretici" "$DIST/inbound-sunum-uretici"
rm -rf "$TMP"

echo "→ Paket hazır: $ZIP  ($(du -h "$ZIP" | cut -f1))"
echo
echo "Claude Code : güncelleme otomatik (plugin marketplace)."
echo "claude.ai   : Settings → Capabilities → Skills → yükle/değiştir"
echo "              (aynı zip chat, cowork ve Projects için geçerlidir)"
