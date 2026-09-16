#!/usr/bin/env bash
# inbound-sunum otomatik güncelleme - oturum başında (SessionStart hook) çalışır.
#
# 1) Marketplace için Claude Code'un kendi arka plan güncellemesini açar
#    (settings.json -> extraKnownMarketplaces.presentation-maker-inbound.autoUpdate)
# 2) Kurulu sürümü GitHub'daki sürümle karşılaştırır; geriyse
#    `claude plugin update` ile hemen günceller ve oturuma not düşer.
# Kapatmak için: INBOUND_OTO_GUNCELLE=0
set -u
[ "${INBOUND_OTO_GUNCELLE:-1}" = "0" ] && exit 0

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_JSON="$HERE/../../../.claude-plugin/plugin.json"
MARKET="presentation-maker-inbound"
PLUGIN="inbound-sunum@$MARKET"
UZAK="https://raw.githubusercontent.com/erdogan1ozdemir/presentation-maker-inbound/main/plugins/inbound-sunum/.claude-plugin/plugin.json"

surum() { python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" "$1" 2>/dev/null; }
YEREL="$(surum "$PLUGIN_JSON")"
UZAK_S="$(curl -s -m 6 "$UZAK" | python3 -c "import json,sys;print(json.load(sys.stdin)['version'])" 2>/dev/null)"

# --- 1) marketplace arka plan güncellemesini aç (bir kez)
python3 - <<'PY' 2>/dev/null
import json, os
p = os.path.expanduser("~/.claude/settings.json")
try:
    d = json.load(open(p, encoding="utf-8"))
except Exception:
    d = {}
m = d.setdefault("extraKnownMarketplaces", {}).setdefault("presentation-maker-inbound", {})
m.setdefault("source", {"source": "github", "repo": "erdogan1ozdemir/presentation-maker-inbound"})
if m.get("autoUpdate") is not True:
    m["autoUpdate"] = True
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY

# --- 2) sürüm geriyse hemen güncelle
[ -z "$YEREL" ] || [ -z "$UZAK_S" ] && exit 0
eski() { [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | head -1)" = "$1" ] && [ "$1" != "$2" ]; }
if eski "$YEREL" "$UZAK_S"; then
  if command -v claude >/dev/null 2>&1; then
    claude plugin marketplace update "$MARKET" >/dev/null 2>&1
    if claude plugin update "$PLUGIN" >/dev/null 2>&1; then
      echo "[inbound-sunum] Skill $YEREL sürümünden $UZAK_S sürümüne güncellendi. Yeni sürüm bu oturumda henüz yüklü değil: kullanıcıya /reload-plugins çalıştırmasını söyle, ardından skill'i yeniden çağır. Güncellemeden önce deste üretme."
    else
      echo "[inbound-sunum] Skill $YEREL, güncel sürüm $UZAK_S. Otomatik güncelleme yapılamadı; kullanıcıya 'claude plugin update $PLUGIN' komutunu ve ardından /reload-plugins çalıştırmasını söyle. Güncellemeden önce deste üretme."
    fi
  else
    echo "[inbound-sunum] Skill $YEREL, güncel sürüm $UZAK_S. claude CLI bulunamadı; kullanıcıya /plugin menüsünden güncellemesini söyle."
  fi
fi
exit 0
