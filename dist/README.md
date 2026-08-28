# Dağıtım paketleri

`inbound-sunum-uretici-v<sürüm>.zip` — claude.ai (chat, cowork ve Projects) için
yüklenebilir skill paketi. Zip'in kökünde `inbound-sunum-uretici/SKILL.md` durur;
claude.ai yüklemesi bu yapıyı bekler.

Paketten çıkarılanlar: `__pycache__`, `.DS_Store` ve kullanılmayan
`fonts-eot-bozuk` klasörü.

## Güncelleme

```bash
bash scripts-guncelle/skill-paketi-guncelle.sh
```

Betik GitHub'dan son sürümü çeker, sürüm numarasını okur ve zip'i yeniden üretir.

| Yüzey | Güncelleme |
|---|---|
| Claude Code | Otomatik - plugin marketplace `presentation-maker-inbound` üzerinden |
| claude.ai chat / cowork / Projects | Betikle zip üretilir, Settings → Capabilities → Skills'ten değiştirilir |

Zip dosyaları sürüm numarasıyla adlandırıldığı için eski paketler kalabilir;
yalnızca en yüksek sürümlü olan yüklenir.
