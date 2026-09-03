#!/usr/bin/env python3
"""
gsc_mcp.py - Search Console icin skill'in kendi MCP sunucusu (SALT OKUNUR).

Neden skill'in icinde: ekipteki herkesin harici bir repoyu klonlamasi
gerekmesin. Tek dosya, tek bagimlilik seti.

KAPSAM SABITTIR: https://www.googleapis.com/auth/webmasters.readonly
Bu kapsamla site ekleme/silme ve sitemap gonderme Google tarafindan reddedilir;
sunucu bu araclari hic tanimlamaz. Yazma yetkisi teknik olarak yoktur.

Kimlik dogrulama - uc yol, sirayla denenir:
  1. SERVIS HESABI: GSC_CREDENTIALS_PATH ile JSON anahtar verilir. Tarayici
     onayi yoktur; hesabin e-postasi Search Console'da property'lere eklenir.
  2. PAYLASILAN KURUMSAL TOKEN: GSC_TOKEN_PATH ile bir kez uretilmis token
     dosyasi verilir. Token client_id ve client_secret'i de tasidigi icin tek
     basina yeterlidir; ekip ayni dosyayi kullanir, kimse onay vermez.
  3. KISISEL OAUTH: GSC_OAUTH_CLIENT_SECRETS ile client_secrets.json verilir,
     ilk calistirmada tarayici acilir.

Kapsam denetimi: paylasilan token beklenenden genis kapsam tasiyorsa sunucu
calismayi reddeder - salt okunur garantisi token duzeyinde de dogrulanir.

Kurulum:
    python3 -m venv .venv
    .venv/bin/pip install "mcp>=1.6.0" google-api-python-client google-auth google-auth-oauthlib
    claude mcp add gsc -s user -e GSC_CREDENTIALS_PATH=/yol/servis-hesabi.json \
        -- /yol/.venv/bin/python /yol/gsc_mcp.py

Ayrintili kurulum: references/gsc-erisim-kurulum.md
"""

import json
import os
import sys

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

try:
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
except ImportError:
    sys.exit("HATA: bagimliliklar eksik. Kurulum:\n"
             "  pip install \"mcp>=1.6.0\" google-api-python-client google-auth "
             "google-auth-oauthlib")

# mcp 2.x'te FastMCP, MCPServer olarak yeniden adlandirildi. Kullandigimiz
# yuzey (tool dekoratoru, run(transport=...), list_tools) iki surumde de ayni,
# bu yuzden ikisi de destekleniyor - ekipte farkli surumler kurulu olabilir.
try:
    from mcp.server.mcpserver import MCPServer as _Sunucu      # mcp >= 2
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as _Sunucu      # mcp 1.x
    except ImportError:
        sys.exit("HATA: mcp paketi eksik. Kurulum:\n"
                 "  bash kur_gsc.sh")

mcp = _Sunucu("gsc")

_SERVIS = None


def servis():
    """Yetkilendirilmis Search Console istemcisi. Once servis hesabi, sonra OAuth."""
    global _SERVIS
    if _SERVIS is not None:
        return _SERVIS

    sa = os.environ.get("GSC_CREDENTIALS_PATH")
    if sa and os.path.exists(sa):
        creds = service_account.Credentials.from_service_account_file(sa, scopes=SCOPES)
        _SERVIS = build("searchconsole", "v1", credentials=creds)
        return _SERVIS

    gizli = os.environ.get("GSC_OAUTH_CLIENT_SECRETS")
    token = os.environ.get("GSC_TOKEN_PATH") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "gsc_token.json")

    # Paylasilan token dosyasi tek basina yeterlidir: creds.to_json() client_id
    # ve client_secret'i de tasidigi icin yenileme icin client_secrets.json
    # gerekmez. Kurumsal hesabin token'i ekibe boyle dagitilabilir.
    if os.path.exists(token) or (gizli and os.path.exists(gizli)):
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        creds = None
        if os.path.exists(token):
            # Kapsam denetimi dosyadan okunur: from_authorized_user_file
            # creds.scopes'u kendisine verilen listeyle dolduruyor, dosyadaki
            # gercek kapsami gostermiyor.
            with open(token, encoding="utf-8") as f:
                _tj = json.load(f)
            fazla = [x for x in (_tj.get("scopes") or []) if x not in SCOPES]
            creds = Credentials.from_authorized_user_file(token, SCOPES)
            if fazla:
                raise RuntimeError(
                    f"Token beklenenden geniş kapsam taşıyor: {fazla}. "
                    f"Bu sunucu yalnızca {SCOPES[0]} kabul eder; token'ı "
                    f"salt-okunur kapsamla yeniden üretin.")
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif gizli and os.path.exists(gizli):
                creds = InstalledAppFlow.from_client_secrets_file(
                    gizli, SCOPES).run_local_server(port=0)
            else:
                raise RuntimeError(
                    "Token geçersiz ve yenilenemiyor. Paylaşılan token "
                    "süresi dolmuş olabilir - OAuth ekranı 'Testing' "
                    "durumundaysa refresh token 7 günde düşer. Çözüm: "
                    "consent screen'i Internal/In production yapıp token'ı "
                    "yeniden üretmek. Ayrıntı: references/gsc-erisim-kurulum.md")
            try:
                with open(token, "w") as f:
                    f.write(creds.to_json())
            except OSError:
                pass          # salt okunur konumdaki paylasilan token: sorun degil
        _SERVIS = build("searchconsole", "v1", credentials=creds)
        return _SERVIS

    raise RuntimeError(
        "Search Console kimlik bilgisi bulunamadi. Uc yoldan biri gerekli:\n"
        "  GSC_TOKEN_PATH=/yol/gsc_token.json            (paylasilan kurumsal token)\n"
        "  GSC_OAUTH_CLIENT_SECRETS=/yol/client_secrets.json  (kisisel OAuth)\n"
        "  GSC_CREDENTIALS_PATH=/yol/servis-hesabi.json  (servis hesabi)\n"
        "Ayrintilar: references/gsc-erisim-kurulum.md")


@mcp.tool()
async def list_properties() -> str:
    """Erisilebilen Search Console property'lerini listeler."""
    try:
        r = servis().sites().list().execute()
    except Exception as e:
        return f"Hata: {e}"
    satir = r.get("siteEntry") or []
    if not satir:
        return ("Property bulunamadi. Servis hesabi kullaniyorsan hesabin "
                "e-postasinin Search Console'da property'ye kullanici olarak "
                "eklenmis olmasi gerekir.")
    return "\n".join(f"{s.get('siteUrl')} | {s.get('permissionLevel')}" for s in satir)


@mcp.tool()
async def search_analytics(site_url: str, start_date: str, end_date: str,
                           dimensions: str = "query", row_limit: int = 1000,
                           start_row: int = 0, search_type: str = "web",
                           filter_dimension: str = "", filter_operator: str = "contains",
                           filter_expression: str = "", data_state: str = "final") -> str:
    """
    Search Analytics sorgusu - boru ile ayrilmis duz metin dondurur.

    dimensions: virgulle ayrilmis (query, page, date, device, country, searchAppearance)
    filter_operator: contains, equals, notContains, notEquals, includingRegex,
                     excludingRegex
      REGEX DESTEKLENIR: cok yazimli segmentler tek cagrida olculur
      (ornek: includingRegex ile "gameplus|game ?plus|game\\+").
    data_state: final veya all (all taze/kismi gunleri de dahil eder)
    """
    dims = [d.strip() for d in dimensions.split(",") if d.strip()]
    govde = {"startDate": start_date, "endDate": end_date, "dimensions": dims,
             "rowLimit": min(row_limit, 25000), "startRow": start_row,
             "type": search_type, "dataState": data_state}
    if filter_dimension and filter_expression:
        govde["dimensionFilterGroups"] = [{"filters": [{
            "dimension": filter_dimension, "operator": filter_operator,
            "expression": filter_expression}]}]
    try:
        r = servis().searchanalytics().query(siteUrl=site_url, body=govde).execute()
    except Exception as e:
        return f"Hata: {e}"
    satirlar = r.get("rows") or []
    if not satirlar:
        return "Veri yok. Tarih araligi, property adresi ve filtreyi kontrol et."
    bas = " | ".join(dims + ["clicks", "impressions", "ctr", "position"])
    out = [bas, "-" * len(bas)]
    for s in satirlar:
        k = s.get("keys") or []
        out.append(" | ".join(list(map(str, k)) + [
            str(s.get("clicks", 0)), str(s.get("impressions", 0)),
            f"{s.get('ctr', 0) * 100:.2f}%", f"{s.get('position', 0):.1f}"]))
    out.append(f"\n{len(satirlar)} satir"
               + (" (limit dolu olabilir, start_row ile sayfalayin)"
                  if len(satirlar) >= min(row_limit, 25000) else ""))
    return "\n".join(out)


@mcp.tool()
async def list_sitemaps(site_url: str) -> str:
    """Property'ye gonderilmis sitemap'leri listeler (yalnizca okur)."""
    try:
        r = servis().sitemaps().list(siteUrl=site_url).execute()
    except Exception as e:
        return f"Hata: {e}"
    s = r.get("sitemap") or []
    if not s:
        return "Sitemap kaydi yok."
    return "\n".join(f"{x.get('path')} | son indirme: {x.get('lastDownloaded','-')} "
                     f"| hata: {x.get('errors','0')} | uyari: {x.get('warnings','0')}"
                     for x in s)


@mcp.tool()
async def inspect_url(site_url: str, page_url: str) -> str:
    """URL Inspection: indeks durumu, canonical, son tarama (yalnizca okur)."""
    try:
        r = servis().urlInspection().index().inspect(body={
            "inspectionUrl": page_url, "siteUrl": site_url}).execute()
    except Exception as e:
        return f"Hata: {e}"
    i = (r.get("inspectionResult") or {}).get("indexStatusResult") or {}
    return json.dumps({
        "indeks": i.get("verdict"), "kapsam": i.get("coverageState"),
        "robots": i.get("robotsTxtState"), "canonical_google": i.get("googleCanonical"),
        "canonical_kullanici": i.get("userCanonical"),
        "son_tarama": i.get("lastCrawlTime"),
    }, ensure_ascii=False, indent=1)


@mcp.tool()
async def batch_inspect_urls(site_url: str, page_urls: str, limit: int = 20) -> str:
    """
    Birden fazla URL'yi tek cagrida denetler (yalnizca okur).

    page_urls: satir satir ya da virgulle ayrilmis URL listesi.
    limit: en fazla kac URL denetlenecek (URL Inspection API gunluk kotasi
           2000/gun, dakikada 600 - buyuk listeler parca parca calistirilir).
    """
    urls = [u.strip() for u in page_urls.replace(",", "\n").splitlines() if u.strip()]
    if not urls:
        return "URL verilmedi."
    kesildi = len(urls) > limit
    urls = urls[:limit]
    try:
        sv = servis()
    except Exception as e:
        return f"Hata: {e}"
    out = ["URL | indeks | kapsam | robots | son tarama"]
    out.append("-" * len(out[0]))
    for u in urls:
        try:
            r = sv.urlInspection().index().inspect(body={
                "inspectionUrl": u, "siteUrl": site_url}).execute()
            i = (r.get("inspectionResult") or {}).get("indexStatusResult") or {}
            out.append(f"{u} | {i.get('verdict','-')} | {i.get('coverageState','-')} | "
                       f"{i.get('robotsTxtState','-')} | {(i.get('lastCrawlTime') or '-')[:10]}")
        except Exception as e:
            out.append(f"{u} | HATA: {str(e)[:60]}")
    if kesildi:
        out.append(f"\n{limit} URL denetlendi, liste daha uzun - kalanini ayri cagriyla calistirin.")
    return "\n".join(out)


@mcp.tool()
async def indexing_issues(site_url: str, page_urls: str, limit: int = 20) -> str:
    """
    Verilen URL'ler icinde indeks sorunu olanlari ayiklar ve ozetler.

    batch_inspect_urls'in filtreli hali: PASS olanlari atlar, yalnizca
    indekslenmemis ya da robots/canonical tarafinda ele alinacak nokta
    tasiyan adresleri dondurur.
    """
    urls = [u.strip() for u in page_urls.replace(",", "\n").splitlines() if u.strip()][:limit]
    if not urls:
        return "URL verilmedi."
    try:
        sv = servis()
    except Exception as e:
        return f"Hata: {e}"
    sorunlu, temiz = [], 0
    for u in urls:
        try:
            r = sv.urlInspection().index().inspect(body={
                "inspectionUrl": u, "siteUrl": site_url}).execute()
            i = (r.get("inspectionResult") or {}).get("indexStatusResult") or {}
            v = i.get("verdict")
            gc, uc = i.get("googleCanonical"), i.get("userCanonical")
            farkli_canonical = gc and uc and gc != uc
            if v == "PASS" and not farkli_canonical:
                temiz += 1
                continue
            sorunlu.append(f"{u}\n  indeks: {v} | kapsam: {i.get('coverageState','-')}"
                           + (f"\n  canonical farki: kullanici {uc} -> google {gc}"
                              if farkli_canonical else ""))
        except Exception as e:
            sorunlu.append(f"{u}\n  HATA: {str(e)[:80]}")
    bas = f"{len(urls)} URL denetlendi: {temiz} sorunsuz, {len(sorunlu)} ele alinacak nokta"
    return bas + ("\n\n" + "\n".join(sorunlu) if sorunlu else "")


if __name__ == "__main__":
    mcp.run(transport="stdio")
