#!/usr/bin/env bash
# setup_deps.sh - Bagimliliklari kontrol eder ve eksikse kurar.
#
# Iki bagimlilik var:
#   1. icerik-dili-rehberi skill'i (github.com/erdogan1ozdemir/icerik-dili-rehberi)
#      Uretilen sunumun dil ve ton standardi. Bu skill onun yerine gecmez;
#      metin yazilirken o rehber okunur.
#   2. python-pptx ve Pillow. Pillow olmadan font olcumu yaklasik kalir,
#      dolayisiyla tasma tespiti zayiflar - kurulmasi onemli.
#
# Kullanim:
#   bash setup_deps.sh --check     # sadece rapor, kurulum yapma
#   bash setup_deps.sh             # eksikleri kur
set -uo pipefail

REPO="https://github.com/erdogan1ozdemir/icerik-dili-rehberi"
TARGET="${HOME}/.claude/skills/icerik-dili-rehberi"
CHECK_ONLY=0
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=1

ok(){ printf '  OK    %s\n' "$1"; }
miss(){ printf '  EKSIK %s\n' "$1"; }
info(){ printf '  ...   %s\n' "$1"; }

echo "== Icerik dili rehberi =="

# Rehber birden fazla yoldan gelebilir: plugin marketplace, kullanici skills
# klasoru, ya da global CLAUDE.md icine gomulu hali. Yerel dosya izlerini arar.
FOUND=""
for p in \
  "$TARGET/SKILL.md" \
  "${HOME}/.claude/skills/icerik-dili-rehberi/SKILL.md" \
  "${HOME}/.claude/icerik-dili-rehberi-final.md"
do
  [[ -f "$p" ]] && { FOUND="$p"; break; }
done
if [[ -z "$FOUND" ]]; then
  while IFS= read -r p; do FOUND="$p"; break; done < <(
    find "${HOME}/.claude/plugins/cache" -maxdepth 5 -type d \
      -name "icerik-dili-rehberi" 2>/dev/null)
fi

if [[ -n "$FOUND" ]]; then
  ok "bulundu: $FOUND"
else
  miss "yerel kopya yok"
  if [[ $CHECK_ONLY -eq 1 ]]; then
    info "kurmak icin: bash setup_deps.sh"
  elif ! command -v git >/dev/null 2>&1; then
    miss "git bulunamadi - rehber elle kurulmali: $REPO"
  else
    info "klonlaniyor -> $TARGET"
    mkdir -p "$(dirname "$TARGET")"
    if git clone --depth 1 -q "$REPO" "$TARGET" 2>/dev/null; then
      ok "kuruldu: $TARGET"
      info "yeni oturumda 'icerik-dili-rehberi' skill'i olarak gorunur"
    else
      miss "klonlanamadi (ag veya erisim). Elle: git clone $REPO \"$TARGET\""
    fi
  fi
fi

echo
echo "== Python bagimliliklari =="
PY=$(command -v python3 || true)
if [[ -z "$PY" ]]; then
  miss "python3 bulunamadi - deste uretilemez"
  exit 1
fi
ok "python3: $($PY -V 2>&1)"

NEED=()
for m in pptx PIL; do
  if $PY -c "import $m" >/dev/null 2>&1; then
    ok "$m"
  else
    miss "$m"
    NEED+=("$m")
  fi
done

if ((${#NEED[@]})); then
  declare -A PKG=([pptx]=python-pptx [PIL]=Pillow)
  PIPS=""
  for m in "${NEED[@]}"; do PIPS+=" ${PKG[$m]}"; done
  if [[ $CHECK_ONLY -eq 1 ]]; then
    info "kurulum:$PIPS"
  else
    info "kuruluyor:$PIPS"
    $PY -m pip install --quiet $PIPS 2>/dev/null \
      || $PY -m pip install --quiet --user $PIPS 2>/dev/null \
      || miss "pip kurulumu basarisiz - elle: python3 -m pip install$PIPS"
  fi
fi

echo
echo "== Opsiyonel =="
$PY -c "import matplotlib" >/dev/null 2>&1 \
  && ok "matplotlib (cok serili cizgi grafik yedegi)" \
  || info "matplotlib yok - cok serili cizgi grafikte vektor cizim kullanilir"
command -v soffice >/dev/null 2>&1 \
  && ok "libreoffice (pptx -> pdf render)" \
  || info "libreoffice yok - gorsel QA build_html_preview.py uzerinden yapilir"

echo
echo "Hazir."
