#!/usr/bin/env python3
"""
build_html_preview.py - Ayni deck.json'dan tarayicida acilabilir HTML onizleme uretir.

Neden gerekli: ortamda LibreOffice olmadigi icin PPTX piksel olarak render
edilemiyor. Design System slaytlari 1280x720 px oldugu ve bu olcu 96 DPI'da
tam olarak PPTX'in 13.333x7.5 inch'ine karsilik geldigi icin, HTML onizleme
uretilen destenin birebir gorsel karsiligidir. Teslim oncesi her slayt burada
gozle kontrol edilir; qa_deck.py de bu HTML uzerinde tasma/cakisma tarar.

Kullanim:
    python3 build_html_preview.py deck.json -o onizleme.html
    python3 build_html_preview.py deck.json -o onizleme.html --open
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inbound_deck import (  # noqa: E402
    C, F_BODY, F_DISPLAY, PT, PX_PER_PT, STAGE_H, STAGE_W, M_L, M_R,
    BODY_BOTTOM, TITLE_TOP, SEP_ACC_GAP, SEP_ACC_H, SEP_ACC_W,
    _delta_kind, fit_pt, parse_runs, plain, separator_layout, text_w, wrap_lines,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
DS = os.path.join(ASSETS, "design-system")


def _b64(path, mime):
    try:
        with open(path, "rb") as f:
            return f"data:{mime};base64," + base64.b64encode(f.read()).decode()
    except Exception:
        return ""


def _fonts_css():
    """Fontlari data URI olarak gomer - onizleme tek dosya olarak tasinabilir."""
    faces, spec = [], [
        (F_DISPLAY, 300, "BricolageGrotesque-Light.ttf"),
        (F_DISPLAY, 400, "BricolageGrotesque-Regular.ttf"),
        (F_DISPLAY, 500, "BricolageGrotesque-Medium.ttf"),
        (F_DISPLAY, 600, "BricolageGrotesque-SemiBold.ttf"),
        (F_DISPLAY, 700, "BricolageGrotesque-Bold.ttf"),
        (F_BODY, 300, "Outfit-Light.ttf"),
        (F_BODY, 400, "Outfit-Regular.ttf"),
        (F_BODY, 600, "Outfit-SemiBold.ttf"),
        (F_BODY, 700, "Outfit-Bold.ttf"),
    ]
    for fam, wt, fn in spec:
        uri = _b64(os.path.join(DS, "fonts", fn), "font/ttf")
        if uri:
            faces.append(f"@font-face{{font-family:'{fam}';src:url({uri}) "
                         f"format('truetype');font-weight:{wt};font-display:block;}}")
    return "\n".join(faces)


def _logo(name):
    return _b64(os.path.join(DS, "logos", name), "image/png")


def esc(s):
    return html.escape(str(s), quote=False)


def runs_html(s, base_color="ink"):
    out = []
    for txt, st in parse_runs(s, base_color):
        col = C.get(st.get("color", base_color), st.get("color", base_color))
        if st.get("bold"):
            out.append(f'<b style="font-family:\'{F_DISPLAY}\';color:#{col}">'
                       f'{esc(txt)}</b>')
        else:
            out.append(f'<span style="color:#{col}">{esc(txt)}</span>')
    return "".join(out)


def pt(v):
    """pt -> px (onizleme px izgarada calisir)."""
    return f"{v * PX_PER_PT:.2f}px"


# ----------------------------------------------------------------------------
# Bloklar
# ----------------------------------------------------------------------------

def h_table(b):
    head, rows = b.get("head") or [], b.get("rows") or []
    ncol = max([len(head)] + [len(r) for r in rows] or [1])
    align = (b.get("align") or ("l" + "c" * (ncol - 1)))
    align = (align + "c" * ncol)[:ncol]
    A = {"l": "left", "c": "center", "r": "right"}
    wash = b.get("wash", True)
    hl = set(b.get("highlight_rows") or [])
    bold_rows = {r if r >= 0 else len(rows) + r for r in (b.get("bold_rows") or [])}
    dcols = set(b.get("delta_cols") or [])
    if not dcols:
        for ci in range(ncol):
            vals = [r[ci] for r in rows if ci < len(r)]
            if vals and sum(1 for v in vals if _delta_kind(str(v))) >= max(1, len(vals) // 2):
                dcols.add(ci)
    fp = b.get("font_pt", PT["table"])

    o = []
    if b.get("title"):
        o.append(f'<div class="blk-title">{esc(plain(b["title"]))}</div>')
    o.append('<table class="dt" style="font-size:%s">' % pt(fp))
    o.append("<thead><tr>")
    for ci in range(ncol):
        o.append(f'<th style="text-align:{A[align[ci]]}">'
                 f'{esc(plain(str(head[ci] if ci < len(head) else "")))}</th>')
    o.append("</tr></thead><tbody>")
    for ri, r in enumerate(rows):
        cls = ' class="hl-row"' if ri in hl else ""
        o.append(f"<tr{cls}>")
        for ci in range(ncol):
            v = str(r[ci]) if ci < len(r) else ""
            k = _delta_kind(plain(v)) if ci in dcols else None
            style = [f"text-align:{A[align[ci]]}"]
            if k == "pos":
                style.append(f"color:#{C['green']};font-weight:700;"
                             f"font-family:'{F_DISPLAY}'")
                if wash:
                    style.append(f"background:#{C['green_wash']}")
            elif k == "neg":
                style.append(f"color:#{C['red']};font-weight:700;"
                             f"font-family:'{F_DISPLAY}'")
                if wash:
                    style.append(f"background:#{C['red_wash']}")
            elif ri in bold_rows:
                style.append(f"font-weight:700;font-family:'{F_DISPLAY}'")
            o.append(f'<td style="{";".join(style)}">{esc(v)}</td>')
        o.append("</tr>")
    o.append("</tbody></table>")
    return "".join(o)


def h_insights(b):
    o = []
    if b.get("title"):
        o.append(f'<div class="ins-title">{esc(plain(b["title"])).upper()}</div>')
    fp = b.get("font_pt", PT["sm"])
    o.append(f'<ul class="ins" style="font-size:{pt(fp)}">')
    for it in b.get("items") or []:
        o.append(f"<li>{runs_html(it, 'white' if b.get('dark') else 'ink')}</li>")
    o.append("</ul>")
    return "".join(o)


def h_kpi(b):
    cards = b.get("cards") or []
    cols = b.get("cols") or min(4, max(1, len(cards)))
    o = [f'<div class="kpi" style="grid-template-columns:repeat({cols},1fr);'
         f'gap:{b.get("gap",18)}px">']
    for i, c in enumerate(cards):
        accent = c.get("accent") or ("coral" if (i == len(cards) - 1
                                                and len(cards) > 2) else "teal")
        vpt = c.get("pt") or 40
        o.append(f'<div class="kpi-card" style="background:#{C[accent]};'
                 f'min-height:{b.get("h",132)}px">')
        o.append(f'<div class="kpi-v" style="font-size:{pt(vpt)}">'
                 f'{esc(c.get("value",""))}'
                 + (f'<span style="font-size:{pt(vpt*0.5)}">'
                    f'{esc(c.get("unit",""))}</span>' if c.get("unit") else "")
                 + "</div>")
        o.append(f'<div class="kpi-l">{esc(plain(str(c.get("label","")))).upper()}</div>')
        if c.get("delta"):
            o.append(f'<div class="kpi-d">{esc(plain(c["delta"]))}</div>')
        o.append("</div>")
    o.append("</div>")
    return "".join(o)


def _fmt(v):
    a = abs(v)
    if a >= 1_000_000:
        return f"{v/1_000_000:.1f}M".replace(".0M", "M")
    if a >= 1_000:
        return f"{v/1_000:.1f}K".replace(".0K", "K")
    if a and a < 10:
        return f"{v:.1f}"
    return f"{v:.0f}"


def h_bar(b):
    cats, series = b.get("cats") or [], b.get("series") or []
    if not cats or not series:
        return ""
    stacked = b.get("stacked", False)
    h = b.get("h", 260)
    plot_h = h - 56 - (22 if b.get("title") else 0)
    if stacked:
        vmax = max(sum(float(s["data"][i] or 0) for s in series)
                   for i in range(len(cats)))
    else:
        vmax = max(max(float(v or 0) for v in s["data"]) for s in series)
    vmax = (vmax * 1.12) or 1

    o = []
    if b.get("title"):
        o.append(f'<div class="blk-title">{esc(plain(b["title"]))}</div>')
    o.append('<div class="lg">')
    for s in series:
        o.append(f'<span><i style="background:#{C.get(s.get("color","gray_bar"), s.get("color"))}">'
                 f'</i>{esc(s.get("name",""))}</span>')
    o.append("</div>")
    o.append(f'<div class="chart" style="height:{plot_h}px">')
    for k in range(1, 4):
        o.append(f'<div class="grid-l" style="bottom:{plot_h*k/4:.0f}px"></div>')
    o.append(f'<div class="axis"></div><div class="bars">')
    for i, cat in enumerate(cats):
        o.append('<div class="slot">')
        o.append('<div class="grp%s">' % (" stk" if stacked else ""))
        for s in series:
            v = float(s["data"][i] or 0)
            bh = plot_h * v / vmax
            col = C.get(s.get("color", "gray_bar"), s.get("color"))
            lbl = (f'<span class="vl">{_fmt(v)}</span>'
                   if b.get("value_labels", True) and not stacked else "")
            o.append(f'<div class="bar" style="height:{bh:.1f}px;background:#{col};'
                     f'width:{b.get("bar_w", 46 if stacked else 22)}px">{lbl}</div>')
        o.append("</div>")
        o.append(f'<div class="cat">{esc(cat)}</div>')
        o.append("</div>")
    o.append("</div></div>")
    return "".join(o)


def h_line(b):
    cats, series = b.get("cats") or [], b.get("series") or []
    if not cats or not series:
        return ""
    h = b.get("h", 260)
    plot_h = h - 56 - (22 if b.get("title") else 0)
    W = b.get("_w", STAGE_W - M_L - M_R)
    vals = [float(v or 0) for s in series for v in s["data"]]
    vmin, vmax = (min(vals), max(vals)) if vals else (0, 1)
    if vmax == vmin:
        vmax = vmin + 1
    span = (vmax - vmin) * 1.15
    base = vmin - (vmax - vmin) * 0.075
    n = len(cats)
    step = W / max(1, n - 1) if n > 1 else W

    o = []
    if b.get("title"):
        o.append(f'<div class="blk-title">{esc(plain(b["title"]))}</div>')
    o.append('<div class="lg">')
    for s in series:
        o.append(f'<span><i style="background:#{C.get(s.get("color","coral"), s.get("color"))};'
                 f'height:3px;border-radius:2px"></i>{esc(s.get("name",""))}</span>')
    o.append("</div>")
    o.append(f'<svg class="chart" style="height:{plot_h}px;width:100%" '
             f'viewBox="0 0 {W:.0f} {plot_h:.0f}" preserveAspectRatio="none">')
    for k in range(1, 4):
        gy = plot_h - plot_h * k / 4
        o.append(f'<line x1="0" y1="{gy:.0f}" x2="{W:.0f}" y2="{gy:.0f}" '
                 f'stroke="#{C["line_soft"]}" stroke-width="1"/>')
    o.append(f'<line x1="0" y1="{plot_h:.0f}" x2="{W:.0f}" y2="{plot_h:.0f}" '
             f'stroke="#{C["line"]}" stroke-width="1"/>')
    for s in series:
        col = C.get(s.get("color", "coral"), s.get("color"))
        pts = []
        for i, v in enumerate(s["data"][:n]):
            vx = step * i if n > 1 else W / 2
            vy = plot_h - plot_h * ((float(v or 0) - base) / span)
            pts.append(f"{vx:.1f},{vy:.1f}")
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#{col}" '
                 f'stroke-width="2.25"/>')
        for p_ in pts:
            xx, yy = p_.split(",")
            o.append(f'<circle cx="{xx}" cy="{yy}" r="3.5" fill="#{col}"/>')
    o.append("</svg>")
    o.append('<div class="cats">' + "".join(
        f'<span style="width:{100/max(1,n):.4f}%">{esc(c)}</span>' for c in cats)
        + "</div>")
    return "".join(o)


def h_panels(b):
    items = b.get("items") or []
    cols = b.get("cols") or min(3, max(1, len(items)))
    o = [f'<div class="panels" style="grid-template-columns:repeat({cols},1fr);'
         f'gap:{b.get("gap",18)}px">']
    for it in items:
        o.append('<div class="panel">')
        o.append(f'<div class="p-title">{esc(plain(it.get("title","")))}</div>')
        if it.get("sub"):
            o.append(f'<div class="p-sub">{esc(plain(it["sub"]))}</div>')
        if it.get("lines"):
            o.append("<ul>" + "".join(f"<li>{runs_html(l)}</li>"
                                      for l in it["lines"]) + "</ul>")
        o.append("</div>")
    o.append("</div>")
    return "".join(o)


def h_note(b):
    return (f'<div class="note" style="background:#{C.get(b.get("fill","mint"))}">'
            f'<div class="n-label">{esc(plain(b.get("label","NOT"))).upper()}</div>'
            f'<div class="n-text">{runs_html(b.get("text",""))}</div></div>')


def h_text(b):
    paras = b.get("paras") or ([b["text"]] if b.get("text") else [])
    o = []
    if b.get("title"):
        o.append(f'<div class="blk-title">{esc(plain(b["title"]))}</div>')
    fp = b.get("font_pt", PT["sm"])
    for p_ in paras:
        o.append(f'<p class="tx" style="font-size:{pt(fp)}">'
                 f'{runs_html(p_, b.get("color","ink"))}</p>')
    return "".join(o)


def h_image(b, base):
    p = b.get("path") or ""
    p = p if os.path.isabs(p) else os.path.join(base, p)
    uri = _b64(p, "image/png")
    if not uri:
        return '<div class="missing">[gorsel bulunamadi]</div>'
    return f'<img class="blk-img" src="{uri}" style="width:100%">'


HB = {"table": h_table, "insights": h_insights, "kpi": h_kpi, "bar": h_bar,
      "line": h_line, "panels": h_panels, "note": h_note, "text": h_text}


# ----------------------------------------------------------------------------
# Slaytlar
# ----------------------------------------------------------------------------

def sl_cover(s):
    lines = s.get("title_lines") or [plain(s.get("title", ""))]
    tpt = s.get("title_pt", 54)
    body = "<br>".join(esc(l) for l in lines)
    sub = (f'<p class="cv-sub">{esc(plain(s["subtitle"]))}</p>'
           if s.get("subtitle") else "")
    bigo = _logo("inbound-big-o-white.png")
    wm = _logo("inbound-wordmark-white.png")
    return (f'<div class="slide coral cover">'
            f'<img class="bigo" src="{bigo}">'
            f'<div class="cv"><h1 style="font-size:{pt(tpt)}">{body}</h1>{sub}</div>'
            f'<img class="wm" src="{wm}"></div>')


def sl_agenda(s):
    lines = s.get("title_lines") or [plain(s.get("title", "SUNUM AKIŞI"))]
    items = s.get("items") or []
    li = []
    for i, it in enumerate(items):
        no = (it.get("no") if isinstance(it, dict) else None) or f"{i+1:02d}"
        lb = it.get("label") if isinstance(it, dict) else str(it)
        li.append(f'<div class="ag-item"><div class="ag-no">{esc(no)}</div>'
                  f'<div class="ag-lb">{esc(plain(lb))}</div></div>')
    return (f'<div class="slide agenda">'
            f'<div class="ag-l"><div class="ag-k">'
            f'{esc(plain(s.get("kicker","")).upper())}</div>'
            f'<div class="ag-t">{"<br>".join(esc(l) for l in lines)}</div>'
            f'<img class="ag-logo" src="{_logo("inbound-o-white.png")}"></div>'
            f'<div class="ag-r">{"".join(li)}</div></div>')


def sl_separator(s):
    # Yerlesim inbound_deck.separator_layout ile hesaplanir: satir kirilmasi ve
    # punto tek yerde belirlenir, boylece HTML ve PPTX birebir ayni gorunur.
    # Tarayicinin kendi sarma davranisina birakilsa iki cikti ayrisirdi.
    L = separator_layout(s)
    body = "<br>".join(esc(ln) for ln in L["lines"])
    return (f'<div class="slide dark sepslide">'
            f'<div class="sep-no" style="font-size:{pt(L["npt"])}">'
            f'{esc(L["num"])}</div>'
            f'<div class="sep-c"><span class="acc"></span>'
            f'<h1 style="font-size:{pt(L["tpt"])}">{body}</h1>'
            f'<span class="acc"></span></div><div></div></div>')


def sl_closing(s):
    title = plain(s.get("title", "Teşekkürler"))
    sub = (f'<p class="cv-sub">{esc(plain(s["subtitle"]))}</p>'
           if s.get("subtitle") else "")
    return (f'<div class="slide dark cover">'
            f'<img class="bigo left" src="{_logo("inbound-big-o-white.png")}">'
            f'<div class="cv"><h1 style="font-size:{pt(s.get("title_pt",56))}">'
            f'{esc(title)}</h1>{sub}</div>'
            f'<img class="wm" src="{_logo("inbound-wordmark-white.png")}"></div>')


def sl_content(s, base):
    dark = s.get("bg") in ("teal", "dark")
    cls = "slide" + (" dark" if dark else "")
    o = [f'<div class="{cls}">']

    if s.get("breadcrumb"):
        bc = s["breadcrumb"]
        parts = bc if isinstance(bc, list) else [bc]
        sp = '<span class="sep">|</span>'.join(
            f'<span class="{"section" if i==0 else "title"}">{esc(plain(str(p)))}</span>'
            for i, p in enumerate(parts))
        o.append(f'<div class="breadcrumb-top">{sp}</div>')

    o.append('<div class="body">')
    if s.get("title"):
        t = plain(s["title"])
        p_ = fit_pt(t, STAGE_W - M_L - M_R, PT["h1"])
        o.append(f'<h1 style="font-size:{pt(p_)}">{esc(t)}</h1>')
    if s.get("subtitle"):
        o.append(f'<p class="sub">{runs_html(s["subtitle"], "ink2")}</p>')

    grid = s.get("grid") or [100]
    gap = s.get("gap", 36)
    avail = STAGE_W - M_L - M_R
    tot = float(sum(grid))
    colw = [(avail - gap * (len(grid) - 1)) * g / tot for g in grid]
    cols = [[] for _ in grid]
    auto = 0
    for b in s.get("blocks") or []:
        c = b.get("col")
        if c is None:
            c = auto % len(grid)
            auto += 1
        c = max(0, min(c, len(grid) - 1))
        bb = dict(b)
        bb["_w"] = colw[c]
        if b.get("type") == "image":
            cols[c].append(h_image(bb, base))
        else:
            fn = HB.get(b.get("type"))
            cols[c].append(fn(bb) if fn else
                           f'<div class="missing">[bilinmeyen blok: '
                           f'{esc(b.get("type"))}]</div>')
    o.append(f'<div class="cols" style="grid-template-columns:'
             f'{" ".join(f"{w:.2f}px" for w in colw)};gap:{gap}px">')
    for c in cols:
        o.append('<div class="col">' + "".join(c) + "</div>")
    o.append("</div></div>")

    if s.get("footnotes"):
        fns = s["footnotes"]
        fns = fns if isinstance(fns, list) else [fns]
        o.append('<div class="fns">' + "".join(
            f"<div>{runs_html(f, 'ink3')}</div>" for f in fns) + "</div>")

    o.append(f'<img class="logo-bl" src="'
             f'{_logo("inbound-o-white.png" if dark else "inbound-o-teal.png")}">')
    if s.get("source"):
        src = s["source"]
        if not src.strip().lower().startswith("kaynak"):
            src = "Kaynak: " + src.strip()
        o.append(f'<div class="source-pill">{esc(src)}</div>')
    o.append("</div>")
    return "".join(o)


CSS = """
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#0b1f1c;font-family:'%(body)s'}
.wrap{padding:28px 0 60px}
.slide{position:relative;width:1280px;height:720px;background:#fff;color:#%(teal)s;
  overflow:hidden;margin:0 auto 26px;box-shadow:0 8px 30px rgba(0,0,0,.45)}
.slide.dark{background:#%(teal)s;color:#fff}
.slide.coral{background:#%(coral)s;color:#fff}
.sn{width:1280px;margin:0 auto;color:#7d9b95;font:600 12px/1 '%(disp)s';
  letter-spacing:.1em;padding:0 0 6px 2px}
h1{font-family:'%(disp)s';font-weight:700;letter-spacing:-.02em;line-height:1.05;margin:0}
.body{position:absolute;left:%(ml)spx;right:%(mr)spx;top:%(tt)spx;bottom:84px}
.sub{font-size:14px;color:#%(ink2)s;margin:10px 0 0;line-height:1.45}
.slide.dark .sub{color:#cfe0dc}
.cols{display:grid;margin-top:20px;align-items:start}
.col>*{margin-bottom:20px}
.col>*:last-child{margin-bottom:0}
.breadcrumb-top{position:absolute;top:28px;left:48px;right:48px;font-size:12px;
  white-space:nowrap;overflow:hidden}
.breadcrumb-top .section{font-family:'%(disp)s';font-weight:700;color:#%(coral)s}
.breadcrumb-top .sep{color:#%(coral)s;margin:0 6px;opacity:.6}
.breadcrumb-top .title{color:#%(coral)s;opacity:.9}
.logo-bl{position:absolute;left:44px;bottom:32px;width:36px;height:36px}
.source-pill{position:absolute;left:100px;bottom:36px;background:#%(coral)s;color:#fff;
  font-family:'%(disp)s';font-weight:700;font-size:11px;padding:6px 12px;border-radius:8px}
.fns{position:absolute;left:%(ml)spx;right:%(mr)spx;bottom:88px;font-size:10px;
  color:#%(ink3)s;line-height:1.4}
.fns div{margin-bottom:2px}
/* cover / closing */
.cover{display:flex;align-items:center;justify-content:center}
.cv{text-align:center;position:relative;z-index:2;padding:0 80px}
.cv h1{color:#fff}
.cv-sub{margin-top:18px;font-size:18px;color:#fff;opacity:.92}
.bigo{position:absolute;right:-120px;top:-200px;height:1400px;opacity:.14}
.bigo.left{right:auto;left:-300px;top:200px;height:1000px;opacity:.10}
.wm{position:absolute;bottom:60px;left:50%%;transform:translateX(-50%%);height:34px;z-index:2}
/* agenda */
.agenda{display:grid;grid-template-columns:45%% 55%%}
.ag-l{background:#%(coral)s;color:#fff;padding:60px 50px;display:flex;
  flex-direction:column;justify-content:center;position:relative}
.ag-k{font-family:'%(disp)s';font-weight:300;font-size:13px;letter-spacing:.1em;opacity:.85}
.ag-t{font-family:'%(disp)s';font-weight:300;font-size:58px;letter-spacing:-.02em;
  line-height:1.05;margin-top:12px}
.ag-logo{position:absolute;left:44px;bottom:40px;width:36px;height:36px}
.ag-r{padding:64px 60px;display:flex;flex-direction:column;justify-content:space-between}
.ag-no{font-size:18px;color:#%(ink3)s}
.ag-lb{font-family:'%(disp)s';font-weight:700;font-size:24px;color:#%(teal)s;margin-top:2px}
/* separator */
.sepslide{display:grid;grid-template-columns:1fr auto 1fr;align-items:center}
.sepslide .sep-no{justify-self:center;font-family:'%(disp)s';font-weight:700;font-size:210px;
  color:#%(tealsoft)s;line-height:.9}
.sepslide .sep-c{text-align:center}
.sepslide .sep-c h1{color:#fff;line-height:1.1}
.acc{display:block;width:%(accw)spx;height:%(acch)spx;background:#fff;border-radius:999px;margin:0 auto %(accgap)spx}
.sepslide .sep-c .acc:last-child{margin:%(accgap)spx auto 0}
/* table */
.dt{width:100%%;border-collapse:collapse;font-family:'%(body)s';
  box-shadow:0 2px 8px rgba(16,51,47,.06)}
.dt th{background:#%(teal)s;color:#fff;font-family:'%(disp)s';font-weight:700;
  font-size:12px;letter-spacing:.04em;padding:9px 12px}
.dt td{padding:8px 12px;border-top:1px solid #%(line)s}
.dt tbody tr:last-child td{border-bottom:1px solid #%(line)s}
.dt tr.hl-row td{background:#%(coraltint)s}
.blk-title{font-family:'%(disp)s';font-weight:700;font-size:18px;margin-bottom:8px}
/* insights */
.ins{list-style:none;padding:0;margin:0}
.ins li{position:relative;padding-left:22px;margin-bottom:12px;line-height:1.5}
.ins li:before{content:"➔";position:absolute;left:0;top:0;color:#%(teal)s}
.slide.dark .ins li:before{color:#%(coral)s}
.ins-title{font-family:'%(disp)s';font-weight:700;font-size:10px;letter-spacing:.06em;
  color:#%(coral)s;margin-bottom:8px}
/* kpi */
.kpi{display:grid}
.kpi-card{color:#fff;border-radius:16px;padding:22px 18px;text-align:center;
  display:flex;flex-direction:column;justify-content:center}
.kpi-v{font-family:'%(disp)s';font-weight:700;line-height:1;letter-spacing:-.02em}
.kpi-l{font-size:11px;opacity:.9;letter-spacing:.04em;margin-top:10px}
.kpi-d{font-family:'%(disp)s';font-weight:700;font-size:12px;margin-top:6px}
/* chart */
.lg{display:flex;gap:24px;font-size:10px;color:#%(ink2)s;margin-bottom:6px}
.lg span{display:inline-flex;align-items:center;gap:6px}
.lg i{width:10px;height:10px;border-radius:3px;display:inline-block}
.chart{position:relative;width:100%%}
.grid-l{position:absolute;left:0;right:0;height:1px;background:#%(linesoft)s}
.axis{position:absolute;left:0;right:0;bottom:0;height:1px;background:#%(line)s}
.bars{position:absolute;inset:0;display:flex;align-items:flex-end}
.slot{flex:1;display:flex;flex-direction:column;align-items:center;height:100%%;
  justify-content:flex-end}
.grp{display:flex;align-items:flex-end;gap:4px;height:100%%}
.grp.stk{flex-direction:column-reverse;gap:0}
.bar{position:relative;border-radius:2px 2px 0 0}
.vl{position:absolute;top:-15px;left:50%%;transform:translateX(-50%%);
  font-family:'%(disp)s';font-weight:700;font-size:10px;color:#%(teal)s;white-space:nowrap}
.cat{font-size:10px;color:#%(ink2)s;margin-top:5px;white-space:nowrap}
.cats{display:flex;margin-top:4px}
.cats span{font-size:10px;color:#%(ink2)s;text-align:center}
/* panels */
.panels{display:grid}
.panel{border:1px solid #%(line)s;border-radius:16px;padding:18px}
.p-title{font-family:'%(disp)s';font-weight:700;font-size:18px}
.p-sub{font-size:10px;color:#%(ink3)s;margin-top:6px;line-height:1.4}
.panel ul{list-style:none;padding:0;margin:8px 0 0}
.panel li{position:relative;padding-left:14px;margin-bottom:6px;font-size:14px;line-height:1.45}
.panel li:before{content:"\\2022";position:absolute;left:0;color:#%(coral)s}
/* note */
.note{border-radius:12px;padding:14px}
.n-label{font-family:'%(disp)s';font-weight:700;font-size:10px;letter-spacing:.06em;
  color:#%(coraldeep)s;margin-bottom:6px}
.n-text{font-size:12px;line-height:1.5}
.tx{font-size:14px;line-height:1.55;margin:0 0 8px}
.blk-img{border-radius:12px;display:block}
.missing{background:#%(redwash)s;color:#%(red)s;padding:10px;border-radius:8px;font-size:12px}
/* self-check isaretleyicileri: HTML esnek kutu oldugu icin tasmayi sessizce
   sikistirir; PPTX mutlak konumlandirma kullandigindan ayni icerik orada tasar.
   Asagidaki isaretler iki ciktinin ayni sinirda okunmasini sagliyor. */
.ovf{outline:2px dashed #%(red)s !important;outline-offset:2px}
.ovf-badge{position:absolute;right:14px;top:14px;z-index:9;background:#%(red)s;color:#fff;
  font:700 11px/1 '%(disp)s';padding:6px 10px;border-radius:6px}
"""

SELFCHECK_JS = """
<script>
/* Govde alt siniri 636px: altinda logo + kaynak pill seridi var.
   Bu siniri asan blok PPTX'te logo/kaynak uzerine biner. */
(function(){
  var LIMIT = 636;
  document.querySelectorAll('.slide').forEach(function(sl){
    var sb = sl.getBoundingClientRect(), hits = 0;
    sl.querySelectorAll('.body .col > *').forEach(function(el){
      var r = el.getBoundingClientRect();
      if (r.height && (r.bottom - sb.top) > LIMIT + 1){ el.classList.add('ovf'); hits++; }
    });
    if (hits){
      var b = document.createElement('div');
      b.className = 'ovf-badge';
      b.textContent = hits + ' blok govde alt sinirini asiyor';
      sl.appendChild(b);
    }
  });
})();
</script>
"""


def render(spec, base):
    parts = []
    for i, s in enumerate(spec.get("slides") or [], 1):
        t = s.get("type", "content")
        fn = {"cover": sl_cover, "agenda": sl_agenda, "separator": sl_separator,
              "closing": sl_closing}.get(t)
        body = fn(s) if fn else sl_content(s, base)
        label = plain(s.get("title") or t)
        parts.append(f'<div class="sn">S{i:02d} · {esc(t)} · {esc(label)}</div>'
                     + body)

    meta = spec.get("meta") or {}
    head_title = f"{meta.get('brand','Deste')} · {meta.get('period','')} · önizleme"
    css = CSS % dict(body=F_BODY, disp=F_DISPLAY, teal=C["teal"], coral=C["coral"],
                     ink2=C["ink2"], ink3=C["ink3"], line=C["line"],
                     linesoft=C["line_soft"], coraltint=C["coral_tint"],
                     coraldeep=C["coral_deep"], tealsoft=C["teal_soft"],
                     redwash=C["red_wash"], red=C["red"], ml=M_L, mr=M_R,
                     tt=TITLE_TOP, accw=SEP_ACC_W, acch=SEP_ACC_H,
                     accgap=SEP_ACC_GAP)
    return (f'<!doctype html><meta charset="utf-8"><title>{esc(head_title)}</title>'
            f"<style>{_fonts_css()}\n{css}</style>"
            f'<div class="wrap">{"".join(parts)}</div>'
            f"{SELFCHECK_JS}")


def main():
    ap = argparse.ArgumentParser(description="deck.json -> HTML onizleme")
    ap.add_argument("spec")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--open", action="store_true")
    a = ap.parse_args()

    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)
    base = os.path.dirname(os.path.abspath(a.spec))
    out = a.out or os.path.splitext(a.spec)[0] + "-onizleme.html"
    if not os.path.isabs(out):
        out = os.path.join(base, out)
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(spec, base))
    print(f"Onizleme -> {out}")
    if a.open:
        os.system(f'open "{out}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
