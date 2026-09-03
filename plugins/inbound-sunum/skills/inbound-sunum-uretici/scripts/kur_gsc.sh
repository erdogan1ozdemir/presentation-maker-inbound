#!/usr/bin/env bash
# Search Console MCP sunucusunu kurar - tek komut, harici depo yok.
#
# Kullanim:
#   bash kur_gsc.sh                          # sadece kurulum, komutu yazdirir
#   bash kur_gsc.sh /yol/gsc_token.json      # kurulum + paylasilan token ile kaydet
#   bash kur_gsc.sh --oauth /yol/client_secrets.json   # kisisel OAuth ile kaydet
set -euo pipefail

BURA="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$BURA/.venv"
PY="$VENV/bin/python"

# Surumlu eklenti onbellegi uyarisi: ~/.claude/plugins/cache/.../1.6.0/... yolu
# her surum yukseltmesinde degisir; oraya kaydedilen MCP sunucusu ilk
# guncellemede kirilir. Kalici olan iki yol var, asagida yazili.
case "$BURA" in
  */.claude/plugins/cache/*)
    KALICI="$HOME/.claude/plugins/marketplaces/presentation-maker-inbound/plugins/inbound-sunum/skills/inbound-sunum-uretici/scripts"
    echo "UYARI: bu betik sürümlü eklenti önbelleğinden çalışıyor:"
    echo "  $BURA"
    echo "Buraya kaydedilen MCP sunucusu, eklenti güncellenince kırılır."
    echo "Kalıcı yollardan biriyle çalıştırın:"
    echo "  1) marketplace klonu (yerinde güncellenir):"
    echo "     bash $KALICI/kur_gsc.sh"
    echo "  2) kendi klonunuz:"
    echo "     git clone https://github.com/erdogan1ozdemir/presentation-maker-inbound.git ~/inbound-sunum"
    echo "     bash ~/inbound-sunum/plugins/inbound-sunum/skills/inbound-sunum-uretici/scripts/kur_gsc.sh"
    echo
    read -r -p "Yine de devam edilsin mi? [e/H] " yanit
    case "$yanit" in [eE]*) ;; *) echo "İptal edildi."; exit 1 ;; esac
    ;;
esac

echo "→ Sanal ortam: $VENV"
if [ ! -x "$PY" ]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r "$BURA/requirements-gsc.txt"
echo "→ Bağımlılıklar kuruldu"

# Sunucu ayaga kalkiyor mu - araclari sayarak dogrula
"$PY" - "$BURA/gsc_mcp.py" <<'PYCHK'
import asyncio, importlib.util, sys
spec = importlib.util.spec_from_file_location("gsc_mcp", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
araclar = [t.name for t in asyncio.run(m.mcp.list_tools())]
print(f"→ Sunucu hazır, {len(araclar)} araç: {', '.join(araclar)}")
print(f"→ Kapsam: {m.SCOPES[0]}  (salt okunur)")
PYCHK

KOMUT_TABAN="claude mcp add gsc -s user"
SON=" -- $PY $BURA/gsc_mcp.py"

if [ "${1:-}" = "--oauth" ]; then
  [ -n "${2:-}" ] || { echo "HATA: --oauth sonrasi client_secrets.json yolu gerekli"; exit 1; }
  [ -f "$2" ] || { echo "HATA: dosya bulunamadi: $2"; exit 1; }
  eval "$KOMUT_TABAN -e GSC_OAUTH_CLIENT_SECRETS=$2$SON"
  echo
  echo "→ Kaydedildi. İlk çağrıda tarayıcı açılıp onay isteyecek."
elif [ -n "${1:-}" ]; then
  [ -f "$1" ] || { echo "HATA: token dosyasi bulunamadi: $1"; exit 1; }
  eval "$KOMUT_TABAN -e GSC_TOKEN_PATH=$1$SON"
  echo
  echo "→ Kaydedildi. Tarayıcı onayı istenmeyecek."
else
  echo
  echo "Kurulum tamam. Kaydetmek için biri:"
  echo
  echo "  # paylaşılan kurumsal token ile (ajans standardı)"
  echo "  $KOMUT_TABAN -e GSC_TOKEN_PATH=/yol/gsc_token.json$SON"
  echo
  echo "  # kişisel OAuth ile"
  echo "  $KOMUT_TABAN -e GSC_OAUTH_CLIENT_SECRETS=/yol/client_secrets.json$SON"
  echo
  echo "Ardından doğrula:  claude mcp list"
fi
