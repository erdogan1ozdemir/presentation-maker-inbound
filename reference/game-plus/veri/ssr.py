# -*- coding: utf-8 -*-
"""Game+ SSR geçişi (8-14 Şubat 2026) öncesi/sonrası - GSC.

Pencereler simetrik ve geçiş haftası hariç (kullanıcı onayı):
  Sonrası: 15 Şub 2026 - 13 Ağu 2026 (180 gün)
  Öncesi : 12 Ağu 2025 -  7 Şub 2026 (180 gün)
Property: sc-domain:gameplus.com.tr · dimensions=device, pozisyon impression ağırlıklı.
"""
# (clicks, impressions, position) - DESKTOP, MOBILE, TABLET
SONRA = [(81395, 2227107, 8.0), (60190, 1929064, 7.2), (2507, 104430, 6.4)]
ONCE = [(56431, 1520281, 13.1), (56178, 1030922, 10.8), (1584, 35185, 6.3)]


def agg(rows):
    c = sum(r[0] for r in rows)
    i = sum(r[1] for r in rows)
    return c, i, c / i * 100, sum(r[1] * r[2] for r in rows) / i


if __name__ == "__main__":
    o, s = agg(ONCE), agg(SONRA)
    print(f"{'':10}{'Click':>10}{'Impression':>13}{'CTR':>9}{'Pozisyon':>10}")
    print(f"{'Öncesi':10}{o[0]:>10,}{o[1]:>13,}{o[2]:>8.2f}%{o[3]:>10.2f}")
    print(f"{'Sonrası':10}{s[0]:>10,}{s[1]:>13,}{s[2]:>8.2f}%{s[3]:>10.2f}")
    print(f"{'Değişim':10}{(s[0]/o[0]-1)*100:>+9.1f}%{(s[1]/o[1]-1)*100:>+12.1f}%"
          f"{s[2]-o[2]:>+8.2f}p{o[3]-s[3]:>+10.2f}")
