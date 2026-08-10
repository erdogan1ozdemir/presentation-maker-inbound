#!/usr/bin/env python3
"""
inbound_deck.py - Inbound Design System PPTX uretici.

deck.json (bildirimsel sahne tanimi) -> duzenlenebilir PPTX.

Koordinat sistemi: 1280x720 px sahne. 96 DPI'da tam olarak 13.333x7.5 inch,
yani standart PPTX 16:9. 1 px = 9525 EMU. Bu sayede Design System'in HTML
slaytlari ile PPTX birebir ayni izgarayi paylasir; build_html_preview.py ayni
deck.json'dan onizleme uretir ve iki cikti piksel piksel ortusur.

Font olcumu gercek TTF uzerinden PIL ile yapilir (assets/design-system/fonts).
Bu yuzden baslik auto-shrink, tablo kolon genisligi ve tasma tespiti tahmine
degil olcume dayanir - gecmis destelerdeki en sik teslim hatasi metin tasmasiydi.

Kullanim:
    python3 inbound_deck.py deck.json -o cikti.pptx
    python3 inbound_deck.py deck.json --check      # sadece dogrula, dosya yazma
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

# ----------------------------------------------------------------------------
# Geometri
# ----------------------------------------------------------------------------

PX = 9525                 # 1 px @96dpi = 9525 EMU
STAGE_W, STAGE_H = 1280, 720
PT_PER_PX = 0.75          # px -> pt
PX_PER_PT = 4.0 / 3.0     # pt -> px


def px(v) -> Emu:
    return Emu(int(round(v * PX)))


# ----------------------------------------------------------------------------
# Design System token'lari (colors_and_type.css ile birebir)
# ----------------------------------------------------------------------------

C = {
    "coral":      "FF7B52",
    "coral_tint": "FFE3D8",
    "coral_deep": "E85F36",
    "teal":       "10332F",
    "teal_soft":  "1A4238",
    "mint":       "E8F5E9",
    "white":      "FFFFFF",
    "ink":        "10332F",
    "ink2":       "4A4A4A",
    "ink3":       "8A8A8A",
    "line":       "E0E0E0",
    "line_soft":  "F0EDE8",
    "red":        "D32F2F",
    "red_wash":   "FFCDD2",
    "green":      "2E7D32",
    "green_wash": "C8E6C9",
    "gold":       "F5A623",
    "gray_bar":   "4A4A4A",
}

F_DISPLAY = "Bricolage Grotesque"
F_BODY = "Outfit"

# Slayt izgarasi (Design System slides/*.html padding degerleri)
M_L, M_R = 60, 60                 # icerik slaytlari yan bosluk
BREADCRUMB_XY = (48, 28)
TITLE_TOP = 88
BODY_BOTTOM = 636                 # altinda logo/kaynak seridi
LOGO_XY = (44, 652)
LOGO_WH = 36
SOURCE_XY = (100, 658)

# Punto olcegi (px * 0.75)
PT = {
    "cover":      66,
    "section":    45,
    "section_num": 157,
    "h1":         27,
    "h2":         21,
    "h3":         18,
    "h4":         13.5,
    "lead":       13.5,
    "body":       12,
    "sm":         10.5,
    "table":      9.5,
    "xs":         9,
    "pill":       8,
    "micro":      7.5,
}

# ----------------------------------------------------------------------------
# Font olcumu (gercek TTF, PIL)
# ----------------------------------------------------------------------------

_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "assets", "design-system", "fonts")
_TTF = {
    (F_DISPLAY, 300): "BricolageGrotesque-Light.ttf",
    (F_DISPLAY, 400): "BricolageGrotesque-Regular.ttf",
    (F_DISPLAY, 500): "BricolageGrotesque-Medium.ttf",
    (F_DISPLAY, 600): "BricolageGrotesque-SemiBold.ttf",
    (F_DISPLAY, 700): "BricolageGrotesque-Bold.ttf",
    (F_DISPLAY, 800): "BricolageGrotesque-ExtraBold.ttf",
    (F_BODY, 300): "Outfit-Light.ttf",
    (F_BODY, 400): "Outfit-Regular.ttf",
    (F_BODY, 500): "Outfit-Medium.ttf",
    (F_BODY, 600): "Outfit-SemiBold.ttf",
    (F_BODY, 700): "Outfit-Bold.ttf",
    (F_BODY, 800): "Outfit-ExtraBold.ttf",
}
_cache: dict = {}
_HAVE_PIL = True
try:
    from PIL import ImageFont
except Exception:          # pragma: no cover
    _HAVE_PIL = False


def _font(family: str, weight: int, size_px: float):
    key = (family, weight, round(size_px, 1))
    if key in _cache:
        return _cache[key]
    if not _HAVE_PIL:
        return None
    name = _TTF.get((family, weight)) or _TTF.get((family, 400))
    path = os.path.normpath(os.path.join(_FONT_DIR, name))
    try:
        f = ImageFont.truetype(path, int(round(size_px)))
    except Exception:
        f = None
    _cache[key] = f
    return f


def text_w(s: str, pt: float, family: str = F_BODY, bold: bool = False) -> float:
    """Metin genisligi (px). PIL yoksa karakter genisligi yaklasimina duser."""
    if not s:
        return 0.0
    size_px = pt * PX_PER_PT
    f = _font(family, 700 if bold else 400, size_px)
    if f is None:
        return len(s) * size_px * 0.52
    try:
        bbox = f.getbbox(s)
        return float(bbox[2] - bbox[0])
    except Exception:
        return len(s) * size_px * 0.52


def wrap_lines(s: str, max_w: float, pt: float, family: str = F_BODY,
               bold: bool = False) -> list:
    """Kelime bazli sarma; olculmus genisliklere gore satirlara boler."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and text_w(trial, pt, family, bold) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines or [""]


def fit_pt(s: str, max_w: float, start_pt: float, min_pt: float = 15,
           family: str = F_DISPLAY, bold: bool = True) -> float:
    """Tek satira sigana kadar puntoyu kucultur (Design System: baslik sarmaz)."""
    p = start_pt
    while p > min_pt and text_w(s, p, family, bold) > max_w:
        p -= 0.5
    return p


# ----------------------------------------------------------------------------
# Zengin metin: {b:..} bold, {g:..} yesil, {r:..} kirmizi, {c:..} coral, {n:..} soluk
# ----------------------------------------------------------------------------

_TAG = re.compile(r"\{([bgrcn]):([^{}]*)\}")
_STYLE = {
    "b": dict(bold=True, color="ink",  family=F_DISPLAY),
    "g": dict(bold=True, color="green", family=F_DISPLAY),
    "r": dict(bold=True, color="red",   family=F_DISPLAY),
    "c": dict(bold=True, color="coral", family=F_DISPLAY),
    "n": dict(bold=False, color="ink3", family=F_BODY),
}


def parse_runs(s: str, base_color: str = "ink", base_family: str = F_BODY) -> list:
    """'Organik {g:+%8 artmistir}.' -> [(metin, stil), ...]"""
    out, pos = [], 0
    for m in _TAG.finditer(s or ""):
        if m.start() > pos:
            out.append((s[pos:m.start()],
                        dict(bold=False, color=base_color, family=base_family)))
        st = dict(_STYLE[m.group(1)])
        if st["color"] == "ink" and base_color != "ink":
            st["color"] = base_color
        out.append((m.group(2), st))
        pos = m.end()
    if pos < len(s or ""):
        out.append((s[pos:], dict(bold=False, color=base_color, family=base_family)))
    return out or [("", dict(bold=False, color=base_color, family=base_family))]


def plain(s: str) -> str:
    return _TAG.sub(r"\2", s or "")


# ----------------------------------------------------------------------------
# Alcak seviye cizim yardimcilari
# ----------------------------------------------------------------------------

def _no_line(shape):
    shape.line.fill.background()


def rect(slide, x, y, w, h, fill=None, radius=None, line=None, line_w=1):
    shp_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(shp_type, px(x), px(y), px(w), px(h))
    if radius:
        # adj = yaricap / kisa kenar
        try:
            s.adjustments[0] = min(0.5, radius / max(1.0, min(w, h)))
        except Exception:
            pass
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = RGBColor.from_string(C.get(fill, fill))
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = RGBColor.from_string(C.get(line, line))
        s.line.width = Pt(line_w)
    else:
        _no_line(s)
    s.shadow.inherit = False
    if s.has_text_frame:
        s.text_frame.text = ""
    return s


def hline(slide, x, y, w, color="line", weight=1):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(x), px(y), px(w),
                               Pt(weight))
    s.fill.solid()
    s.fill.fore_color.rgb = RGBColor.from_string(C.get(color, color))
    _no_line(s)
    s.shadow.inherit = False
    return s


def textbox(slide, x, y, w, h, runs, pt=PT["body"], family=F_BODY,
            color="ink", bold=False, align="l", anchor="t", line_pct=1.5,
            space_after=0, wrap=True):
    """runs: str | [(metin, stil)] | [ [(metin,stil)], ... ] (paragraf listesi)"""
    tb = slide.shapes.add_textbox(px(x), px(y), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE,
                          "b": MSO_ANCHOR.BOTTOM}[anchor]

    if isinstance(runs, str):
        paras = [parse_runs(runs, color, family)]
    elif runs and isinstance(runs[0], tuple):
        paras = [runs]
    else:
        paras = runs

    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER,
                       "r": PP_ALIGN.RIGHT, "j": PP_ALIGN.JUSTIFY}[align]
        p.line_spacing = line_pct
        if space_after:
            p.space_after = Pt(space_after)
        for txt, st in (para or [("", {})]):
            r = p.add_run()
            r.text = txt
            fnt = r.font
            fnt.size = Pt(pt)
            fnt.name = st.get("family", family)
            fnt.bold = bool(st.get("bold", bold))
            fnt.color.rgb = RGBColor.from_string(
                C.get(st.get("color", color), st.get("color", color)))
    return tb


def picture(slide, path, x, y, w=None, h=None):
    if not os.path.exists(path):
        return None
    kw = {}
    if w:
        kw["width"] = px(w)
    if h:
        kw["height"] = px(h)
    return slide.shapes.add_picture(path, px(x), px(y), **kw)


def set_bg(slide, color):
    """Slayt zeminini doldurur (p:bg)."""
    xml = (
        '<p:bg xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<p:bgPr><a:solidFill><a:srgbClr val="%s"/></a:solidFill>'
        '<a:effectLst/></p:bgPr></p:bg>' % C.get(color, color)
    )
    from lxml import etree
    bg = etree.fromstring(xml)
    spTree = slide.shapes._spTree
    spTree.getparent().insert(0, bg)


# ----------------------------------------------------------------------------
# Slayt kromu: breadcrumb, baslik, alt baslik, logo, kaynak, dipnot
# ----------------------------------------------------------------------------

class Ctx:
    """Uretim baglami: varlik yollari, uyarilar, olcum kayitlari."""

    def __init__(self, assets_dir, base_dir):
        self.assets = assets_dir
        self.base = base_dir
        self.warnings = []
        self.boxes = []          # (slayt_no, etiket, x, y, w, h) - QA icin
        self.overflowed = set()  # (slayt_no, blok_tipi) - mukerrer uyari onleme

    def logo(self, name):
        return os.path.join(self.assets, "design-system", "logos", name)

    def resolve(self, p):
        if not p:
            return p
        return p if os.path.isabs(p) else os.path.join(self.base, p)

    def warn(self, msg):
        self.warnings.append(msg)


def chrome(slide, spec, ctx, idx, dark=False):
    """Breadcrumb + baslik + alt baslik + logo + kaynak pill. Govde ust y dondurur."""
    inv = dark
    avail = STAGE_W - M_L - M_R

    if spec.get("breadcrumb"):
        bc = spec["breadcrumb"]
        parts = bc if isinstance(bc, list) else [bc]
        runs = []
        for i, part in enumerate(parts):
            if i:
                runs.append(("  |  ", dict(bold=False, color="coral", family=F_BODY)))
            runs.append((str(part), dict(bold=(i == 0), color="coral",
                                         family=F_DISPLAY if i == 0 else F_BODY)))
        textbox(slide, BREADCRUMB_XY[0], BREADCRUMB_XY[1], STAGE_W - 96, 18,
                runs, pt=PT["xs"], line_pct=1.0)

    y = TITLE_TOP
    if spec.get("title"):
        t = plain(spec["title"])
        p = fit_pt(t, avail, PT["h1"])
        if p < PT["h1"]:
            ctx.warn(f"S{idx}: baslik tek satira sigmasi icin {PT['h1']}pt -> {p}pt kucultuldu")
        textbox(slide, M_L, y, avail, p * PX_PER_PT * 1.15, t, pt=p,
                family=F_DISPLAY, bold=True,
                color="white" if inv else "ink", line_pct=1.05, wrap=False)
        y += p * PX_PER_PT * 1.15 + 10

    if spec.get("subtitle"):
        sub = spec["subtitle"]
        lines = wrap_lines(plain(sub), avail, PT["sm"])
        h = len(lines) * PT["sm"] * PX_PER_PT * 1.45
        textbox(slide, M_L, y, avail, h, sub, pt=PT["sm"],
                color="white" if inv else "ink2", line_pct=1.45)
        y += h + 16

    logo_name = "inbound-o-white.png" if inv else "inbound-o-teal.png"
    picture(slide, ctx.logo(logo_name), LOGO_XY[0], LOGO_XY[1], w=LOGO_WH, h=LOGO_WH)

    if spec.get("source"):
        src = spec["source"]
        if not src.strip().lower().startswith("kaynak"):
            src = "Kaynak: " + src.strip()
        w = text_w(src, PT["pill"], F_DISPLAY, True) + 24
        s = rect(slide, SOURCE_XY[0], SOURCE_XY[1], w, 22, fill="coral", radius=8)
        tf = s.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = src
        r.font.size = Pt(PT["pill"])
        r.font.name = F_DISPLAY
        r.font.bold = True
        r.font.color.rgb = RGBColor.from_string(C["white"])

    return y


def footnotes(slide, notes, ctx, idx):
    """Yildizli dipnotlar: govde altinda, kaynak seridinin ustunde."""
    if not notes:
        return BODY_BOTTOM
    notes = notes if isinstance(notes, list) else [notes]
    avail = STAGE_W - M_L - M_R
    paras, total = [], 0
    for n in notes:
        ls = wrap_lines(plain(n), avail, PT["micro"])
        total += len(ls) * PT["micro"] * PX_PER_PT * 1.4
        paras.append(parse_runs(n, "ink3"))
    y = BODY_BOTTOM - total
    textbox(slide, M_L, y, avail, total, paras, pt=PT["micro"],
            color="ink3", line_pct=1.4, space_after=2)
    return y - 12


# ----------------------------------------------------------------------------
# Blok: tablo
# ----------------------------------------------------------------------------

_NUMISH = re.compile(r"^[\s+\-]*[\d.,]+\s*(%|p|x|K|M|₺|pt)?[\s]*$|^%[\s]*[+\-]?[\d.,]+")


def _delta_kind(v: str):
    """'+%8.1' -> 'pos', '-%37' -> 'neg', digerleri None."""
    s = (v or "").strip()
    if not s or s in {"-", "—", "n/a"}:
        return None
    if s.startswith("+"):
        return "pos"
    if s.startswith("-") and re.search(r"\d", s):
        return "neg"
    return None


def block_table(slide, b, x, y, w, ctx, idx):
    """
    b = {
      type: "table",
      head: ["Kategori","Impression","Click","Degisim"],
      rows: [["Armaturler","1.2M","48.2K","+%8.1"], ...],
      align: "lccc",              # kolon hizalama (l/c/r), varsayilan ilk sol digerleri orta
      delta_cols: [3],            # delta renk kodu uygulanacak kolonlar (auto tespit de var)
      wash: true,                 # delta hucrelerine yesil/kirmizi zemin (deck/HTML standardi)
      highlight_rows: [2],        # coral-tint vurgu satiri (kendi marka)
      bold_rows: [-1],            # kalin satir (Total / Grand Total)
      col_w: [40,20,20,20],       # yuzde; verilmezse olcumden turetilir
      row_h: 26
    }
    """
    head = b.get("head") or []
    rows = b.get("rows") or []
    ncol = max([len(head)] + [len(r) for r in rows] or [1])
    head = list(head) + [""] * (ncol - len(head))

    align = b.get("align") or ("l" + "c" * (ncol - 1))
    align = (align + "c" * ncol)[:ncol]
    wash = b.get("wash", True)
    hl_rows = set(b.get("highlight_rows") or [])
    bold_rows = {r if r >= 0 else len(rows) + r for r in (b.get("bold_rows") or [])}

    delta_cols = set(b.get("delta_cols") or [])
    if not delta_cols:
        for ci in range(ncol):
            vals = [r[ci] for r in rows if ci < len(r)]
            if vals and sum(1 for v in vals if _delta_kind(str(v))) >= max(1, len(vals) // 2):
                delta_cols.add(ci)

    pad = 12
    th_pt, td_pt = PT["xs"], b.get("font_pt", PT["table"])

    if b.get("col_w"):
        tot = float(sum(b["col_w"]))
        widths = [w * c / tot for c in b["col_w"]]
    else:
        need = []
        for ci in range(ncol):
            mx = text_w(plain(str(head[ci])), th_pt, F_DISPLAY, True)
            for r in rows:
                if ci < len(r):
                    mx = max(mx, text_w(plain(str(r[ci])), td_pt, F_BODY, True))
            need.append(mx + pad * 2)
        # ilk kolon esnek, sayisal kolonlar olculen genisligi korur
        fixed = sum(need[1:])
        first = max(need[0], w - fixed)
        widths = [first] + need[1:]
        scale = w / sum(widths)
        if scale < 1:
            widths = [wd * scale for wd in widths]

    row_h = b.get("row_h", 26)
    head_h = b.get("head_h", 30)

    # ilk kolonda sarma gerekiyorsa satir yuksekligini buyut
    row_hs = []
    for r in rows:
        n = len(wrap_lines(plain(str(r[0] if r else "")), widths[0] - pad * 2,
                           td_pt)) if ncol else 1
        row_hs.append(max(row_h, n * td_pt * PX_PER_PT * 1.35 + 10))

    total_h = head_h + sum(row_hs)
    if b.get("title"):
        total_h += PT["h4"] * PX_PER_PT * 1.3 + 8

    y0 = y
    if b.get("title"):
        textbox(slide, x, y, w, PT["h4"] * PX_PER_PT * 1.3, b["title"],
                pt=PT["h4"], family=F_DISPLAY, bold=True, color="ink", line_pct=1.2)
        y += PT["h4"] * PX_PER_PT * 1.3 + 8

    # baslik satiri (teal zemin + beyaz kalin) - Bolum 15.3 deck standardi
    rect(slide, x, y, w, head_h, fill="teal")
    cx = x
    for ci in range(ncol):
        textbox(slide, cx + pad, y, widths[ci] - pad * 2, head_h,
                plain(str(head[ci])), pt=th_pt, family=F_DISPLAY, bold=True,
                color="white", align=align[ci], anchor="m", line_pct=1.0)
        cx += widths[ci]
    y += head_h

    for ri, r in enumerate(rows):
        rh = row_hs[ri]
        if ri in hl_rows:
            rect(slide, x, y, w, rh, fill="coral_tint")
        cx = x
        for ci in range(ncol):
            val = str(r[ci]) if ci < len(r) else ""
            kind = _delta_kind(plain(val)) if ci in delta_cols else None
            col, bold = "ink", (ri in bold_rows)
            if kind == "pos":
                col, bold = "green", True
                if wash:
                    rect(slide, cx, y, widths[ci], rh, fill="green_wash")
            elif kind == "neg":
                col, bold = "red", True
                if wash:
                    rect(slide, cx, y, widths[ci], rh, fill="red_wash")
            textbox(slide, cx + pad, y, widths[ci] - pad * 2, rh, val,
                    pt=td_pt, family=F_DISPLAY if bold else F_BODY, bold=bold,
                    color=col, align=align[ci], anchor="m", line_pct=1.3)
            cx += widths[ci]
        hline(slide, x, y, w, "line", 0.75)
        y += rh

    hline(slide, x, y, w, "line", 0.75)
    ctx.boxes.append((idx, "table", x, y0, w, y - y0))
    return y - y0


# ----------------------------------------------------------------------------
# Blok: insight listesi
# ----------------------------------------------------------------------------

def block_insights(slide, b, x, y, w, ctx, idx):
    """b = {type:"insights", title?:"TREND OKUMALARI", items:[".."], dark?:false}"""
    items = b.get("items") or []
    dark = b.get("dark", False)
    base = "white" if dark else "ink"
    y0, ind, gap = y, 22, b.get("gap", 12)

    if b.get("title"):
        textbox(slide, x, y, w, 18, plain(b["title"]).upper(), pt=PT["micro"],
                family=F_DISPLAY, bold=True, color="coral", line_pct=1.0)
        y += 22

    pt_ = b.get("font_pt", PT["sm"])
    for it in items:
        lines = wrap_lines(plain(it), w - ind, pt_)
        h = len(lines) * pt_ * PX_PER_PT * 1.5
        textbox(slide, x, y, 16, pt_ * PX_PER_PT * 1.5, "➔", pt=pt_,
                family=F_BODY, color="coral" if dark else "teal", line_pct=1.5)
        textbox(slide, x + ind, y, w - ind, h, it, pt=pt_, color=base, line_pct=1.5)
        y += h + gap

    ctx.boxes.append((idx, "insights", x, y0, w, y - y0))
    return y - y0


# ----------------------------------------------------------------------------
# Blok: KPI kartlari
# ----------------------------------------------------------------------------

def block_kpi(slide, b, x, y, w, ctx, idx):
    """
    b = {type:"kpi", cards:[{value:"595.4K", unit?:"+", label:"CLICK",
                             delta?:"+%12.4 YoY", accent?:"teal|coral"}],
         cols?:4, h?:132}
    """
    cards = b.get("cards") or []
    cols = b.get("cols") or min(4, max(1, len(cards)))
    gap = b.get("gap", 18)
    cw = (w - gap * (cols - 1)) / cols
    ch = b.get("h", 132)
    rows = (len(cards) + cols - 1) // cols

    for i, c in enumerate(cards):
        cx = x + (i % cols) * (cw + gap)
        cy = y + (i // cols) * (ch + gap)
        accent = c.get("accent") or ("coral" if (i == len(cards) - 1
                                                and len(cards) > 2) else "teal")
        rect(slide, cx, cy, cw, ch, fill=accent, radius=16)

        val, unit = str(c.get("value", "")), str(c.get("unit", "") or "")
        vpt = c.get("pt") or 40
        while vpt > 20 and text_w(val + unit, vpt, F_DISPLAY, True) > cw - 32:
            vpt -= 1
        runs = [(val, dict(bold=True, color="white", family=F_DISPLAY))]
        vy = cy + 22
        textbox(slide, cx, vy, cw, vpt * PX_PER_PT * 1.05, runs, pt=vpt,
                family=F_DISPLAY, bold=True, color="white", align="c",
                line_pct=1.0, wrap=False)
        if unit:
            textbox(slide, cx, vy + vpt * PX_PER_PT * 0.12, cw,
                    vpt * PX_PER_PT * 0.6, unit, pt=vpt * 0.5, family=F_DISPLAY,
                    bold=True, color="white", align="c", line_pct=1.0, wrap=False)

        ly = vy + vpt * PX_PER_PT * 1.05 + 8
        textbox(slide, cx + 12, ly, cw - 24, 16, plain(str(c.get("label", ""))).upper(),
                pt=PT["micro"], color="white", align="c", line_pct=1.1)
        if c.get("delta"):
            textbox(slide, cx + 12, ly + 18, cw - 24, 16, c["delta"], pt=PT["xs"],
                    family=F_DISPLAY, bold=True, color="white", align="c",
                    line_pct=1.1)

    h = rows * ch + (rows - 1) * gap
    ctx.boxes.append((idx, "kpi", x, y, w, h))
    return h


# ----------------------------------------------------------------------------
# Blok: bar / stacked bar (duzenlenebilir vektor sekiller)
# ----------------------------------------------------------------------------

def _fmt_axis(v):
    a = abs(v)
    if a >= 1_000_000:
        return f"{v/1_000_000:.1f}M".replace(".0M", "M")
    if a >= 1_000:
        return f"{v/1_000:.1f}K".replace(".0K", "K")
    if a and a < 10:
        return f"{v:.1f}"
    return f"{v:.0f}"


def block_bar(slide, b, x, y, w, ctx, idx):
    """
    b = {type:"bar", cats:["Oca","Sub",...],
         series:[{name:"2025", data:[...], color:"gold"},
                 {name:"2026", data:[...], color:"gray_bar"}],
         h?:280, value_labels?:true, stacked?:false, fmt?:"K"}
    Native pptx chart yerine sekil cizilir: PowerPoint kategori eksenini
    "1,2,3" gosterdigi icin (gecmis projelerde yasandi) ve tasarim sistemi
    gorunumu sekillerle birebir tutuluyor. Sekiller sunum icinden duzenlenebilir.
    """
    cats = b.get("cats") or []
    series = b.get("series") or []
    if not cats or not series:
        return 0
    stacked = b.get("stacked", False)
    h = b.get("h", 260)
    y0 = h_used = y

    if b.get("title"):
        textbox(slide, x, y, w, PT["h4"] * PX_PER_PT * 1.3, b["title"],
                pt=PT["h4"], family=F_DISPLAY, bold=True, line_pct=1.2)
        y += PT["h4"] * PX_PER_PT * 1.3 + 6

    # legend
    if len(series) > 1 or b.get("legend", True):
        lx = x
        for s in series:
            rect(slide, lx, y + 3, 10, 10, fill=s.get("color", "gray_bar"), radius=3)
            nm = str(s.get("name", ""))
            textbox(slide, lx + 15, y, 200, 14, nm, pt=PT["micro"], color="ink2",
                    line_pct=1.0, wrap=False)
            lx += 15 + text_w(nm, PT["micro"]) + 26
        y += 20

    lab_h = 20
    val_h = 16 if b.get("value_labels", True) else 0
    plot_top = y + val_h
    plot_bot = y0 + h - lab_h
    plot_h = max(40, plot_bot - plot_top)

    if stacked:
        tops = [sum(float(s["data"][i] or 0) for s in series) for i in range(len(cats))]
        vmax = max(tops) if tops else 1
    else:
        vmax = max((max(float(v or 0) for v in s["data"]) for s in series), default=1)
    vmax = vmax * 1.12 or 1

    # yatay izgara
    for k in range(1, 4):
        gy = plot_bot - plot_h * k / 4
        hline(slide, x, gy, w, "line_soft", 0.75)
    hline(slide, x, plot_bot, w, "line", 0.75)

    n = len(cats)
    slot = w / n
    if stacked:
        bw = min(b.get("bar_w", 46), slot * 0.62)
    else:
        bw = min(b.get("bar_w", 22), (slot * 0.72) / len(series))
    grp_w = bw if stacked else bw * len(series) + 4 * (len(series) - 1)

    for i, cat in enumerate(cats):
        cx = x + slot * i + (slot - grp_w) / 2
        if stacked:
            acc = 0.0
            for s in series:
                v = float(s["data"][i] or 0)
                bh = plot_h * v / vmax
                if bh >= 1:
                    rect(slide, cx, plot_bot - acc - bh, bw, bh,
                         fill=s.get("color", "gray_bar"))
                acc += bh
            if b.get("value_labels", True):
                tot = sum(float(s["data"][i] or 0) for s in series)
                textbox(slide, cx - 12, plot_bot - acc - 15, bw + 24, 14,
                        _fmt_axis(tot), pt=PT["micro"], family=F_DISPLAY,
                        bold=True, color="ink", align="c", line_pct=1.0, wrap=False)
        else:
            for si, s in enumerate(series):
                v = float(s["data"][i] or 0)
                bh = plot_h * v / vmax
                bx = cx + si * (bw + 4)
                if bh >= 1:
                    rect(slide, bx, plot_bot - bh, bw, bh,
                         fill=s.get("color", "gray_bar"))
                if b.get("value_labels", True):
                    textbox(slide, bx - 14, plot_bot - bh - 15, bw + 28, 14,
                            _fmt_axis(v), pt=PT["micro"], family=F_DISPLAY,
                            bold=True, color="ink", align="c", line_pct=1.0,
                            wrap=False)
        textbox(slide, x + slot * i, plot_bot + 5, slot, 16, str(cat),
                pt=PT["micro"], color="ink2", align="c", line_pct=1.0, wrap=False)

    ctx.boxes.append((idx, "bar", x, y0, w, h))
    return h


def block_line(slide, b, x, y, w, ctx, idx):
    """
    b = {type:"line", cats:[...], series:[{name, data, color}], h?:260}
    Freeform polyline + nokta isaretleri; duzenlenebilir kalir.
    """
    cats = b.get("cats") or []
    series = b.get("series") or []
    if not cats or not series:
        return 0
    h = b.get("h", 260)
    y0 = y

    if b.get("title"):
        textbox(slide, x, y, w, PT["h4"] * PX_PER_PT * 1.3, b["title"],
                pt=PT["h4"], family=F_DISPLAY, bold=True, line_pct=1.2)
        y += PT["h4"] * PX_PER_PT * 1.3 + 6

    lx = x
    for s in series:
        rect(slide, lx, y + 4, 14, 3, fill=s.get("color", "coral"), radius=2)
        nm = str(s.get("name", ""))
        textbox(slide, lx + 19, y, 200, 14, nm, pt=PT["micro"], color="ink2",
                line_pct=1.0, wrap=False)
        lx += 19 + text_w(nm, PT["micro"]) + 26
    y += 20

    plot_top, plot_bot = y + 14, y0 + h - 20
    plot_h = max(40, plot_bot - plot_top)
    vals = [float(v or 0) for s in series for v in s["data"]]
    vmin, vmax = (min(vals), max(vals)) if vals else (0, 1)
    if vmax == vmin:
        vmax = vmin + 1
    span = (vmax - vmin) * 1.15
    base = vmin - (vmax - vmin) * 0.075

    for k in range(1, 4):
        hline(slide, x, plot_bot - plot_h * k / 4, w, "line_soft", 0.75)
    hline(slide, x, plot_bot, w, "line", 0.75)

    n = len(cats)
    step = w / max(1, n - 1) if n > 1 else w

    for s in series:
        col = C.get(s.get("color", "coral"), s.get("color", "coral"))
        pts = []
        for i, v in enumerate(s["data"][:n]):
            vx = x + step * i if n > 1 else x + w / 2
            vy = plot_bot - plot_h * ((float(v or 0) - base) / span)
            pts.append((vx, vy))
        if len(pts) > 1:
            ff = slide.shapes.build_freeform(px(pts[0][0]), px(pts[0][1]))
            ff.add_line_segments([(px(a), px(bb)) for a, bb in pts[1:]], close=False)
            shp = ff.convert_to_shape()
            shp.fill.background()
            shp.line.color.rgb = RGBColor.from_string(col)
            shp.line.width = Pt(2.25)
            shp.shadow.inherit = False
        for (vx, vy) in pts:
            d = slide.shapes.add_shape(MSO_SHAPE.OVAL, px(vx - 3.5), px(vy - 3.5),
                                       px(7), px(7))
            d.fill.solid()
            d.fill.fore_color.rgb = RGBColor.from_string(col)
            _no_line(d)
            d.shadow.inherit = False

    for i, cat in enumerate(cats):
        vx = x + step * i if n > 1 else x + w / 2
        textbox(slide, vx - step / 2, plot_bot + 5, max(step, 40), 16, str(cat),
                pt=PT["micro"], color="ink2", align="c", line_pct=1.0, wrap=False)

    ctx.boxes.append((idx, "line", x, y0, w, h))
    return h


# ----------------------------------------------------------------------------
# Blok: panel kartlari / not kutusu / duz metin / gorsel
# ----------------------------------------------------------------------------

def block_panels(slide, b, x, y, w, ctx, idx):
    """b = {type:"panels", cols?:3, items:[{title, sub?, lines:[..]}], h?:auto}"""
    items = b.get("items") or []
    cols = b.get("cols") or min(3, max(1, len(items)))
    gap = b.get("gap", 18)
    cw = (w - gap * (cols - 1)) / cols
    pad = 18
    pt_ = b.get("font_pt", PT["sm"])

    heights = []
    for it in items:
        hh = pad
        hh += PT["h4"] * PX_PER_PT * 1.25 + 6
        if it.get("sub"):
            hh += len(wrap_lines(plain(it["sub"]), cw - pad * 2, PT["micro"])) \
                  * PT["micro"] * PX_PER_PT * 1.4 + 8
        for ln in it.get("lines") or []:
            hh += len(wrap_lines(plain(ln), cw - pad * 2 - 14, pt_)) \
                  * pt_ * PX_PER_PT * 1.45 + 6
        heights.append(hh + pad)
    ch = b.get("h") or (max(heights) if heights else 100)

    for i, it in enumerate(items):
        cx = x + (i % cols) * (cw + gap)
        cy = y + (i // cols) * (ch + gap)
        rect(slide, cx, cy, cw, ch, fill=b.get("fill", "white"), radius=16,
             line="line", line_w=0.75)
        ty = cy + pad
        textbox(slide, cx + pad, ty, cw - pad * 2, PT["h4"] * PX_PER_PT * 1.25,
                plain(it.get("title", "")), pt=PT["h4"], family=F_DISPLAY,
                bold=True, color=it.get("color", "ink"), line_pct=1.25)
        ty += PT["h4"] * PX_PER_PT * 1.25 + 6
        if it.get("sub"):
            hh = len(wrap_lines(plain(it["sub"]), cw - pad * 2, PT["micro"])) \
                 * PT["micro"] * PX_PER_PT * 1.4
            textbox(slide, cx + pad, ty, cw - pad * 2, hh, it["sub"],
                    pt=PT["micro"], color="ink3", line_pct=1.4)
            ty += hh + 8
        for ln in it.get("lines") or []:
            hh = len(wrap_lines(plain(ln), cw - pad * 2 - 14, pt_)) \
                 * pt_ * PX_PER_PT * 1.45
            textbox(slide, cx + pad, ty, 12, hh, "•", pt=pt_, color="coral",
                    line_pct=1.45)
            textbox(slide, cx + pad + 14, ty, cw - pad * 2 - 14, hh, ln, pt=pt_,
                    color="ink", line_pct=1.45)
            ty += hh + 6

    rows = (len(items) + cols - 1) // cols
    h = rows * ch + (rows - 1) * gap
    ctx.boxes.append((idx, "panels", x, y, w, h))
    return h


def block_note(slide, b, x, y, w, ctx, idx):
    """b = {type:"note", label:"YONTEM", text:"..", fill?:"mint"}"""
    label = plain(b.get("label", "NOT")).upper()
    pad = 14
    pt_ = b.get("font_pt", PT["xs"])
    lines = wrap_lines(plain(b.get("text", "")), w - pad * 2, pt_)
    th = len(lines) * pt_ * PX_PER_PT * 1.5
    h = pad + PT["micro"] * PX_PER_PT * 1.2 + 6 + th + pad
    rect(slide, x, y, w, h, fill=b.get("fill", "mint"), radius=12)
    textbox(slide, x + pad, y + pad, w - pad * 2, PT["micro"] * PX_PER_PT * 1.2,
            label, pt=PT["micro"], family=F_DISPLAY, bold=True, color="coral_deep",
            line_pct=1.2)
    textbox(slide, x + pad, y + pad + PT["micro"] * PX_PER_PT * 1.2 + 6,
            w - pad * 2, th, b.get("text", ""), pt=pt_, color="ink", line_pct=1.5)
    ctx.boxes.append((idx, "note", x, y, w, h))
    return h


def block_text(slide, b, x, y, w, ctx, idx):
    pt_ = b.get("font_pt", PT["sm"])
    paras = b.get("paras") or ([b["text"]] if b.get("text") else [])
    total = 0
    rendered = []
    for p in paras:
        ls = wrap_lines(plain(p), w, pt_)
        total += len(ls) * pt_ * PX_PER_PT * 1.55 + 8
        rendered.append(parse_runs(p, b.get("color", "ink")))
    if b.get("title"):
        textbox(slide, x, y, w, PT["h4"] * PX_PER_PT * 1.3, b["title"],
                pt=PT["h4"], family=F_DISPLAY, bold=True, line_pct=1.2)
        y += PT["h4"] * PX_PER_PT * 1.3 + 8
        total += PT["h4"] * PX_PER_PT * 1.3 + 8
    textbox(slide, x, y, w, total, rendered, pt=pt_, color=b.get("color", "ink"),
            line_pct=1.55, space_after=6)
    ctx.boxes.append((idx, "text", x, y, w, total))
    return total


def block_image(slide, b, x, y, w, ctx, idx):
    p = ctx.resolve(b.get("path"))
    if not p or not os.path.exists(p):
        ctx.warn(f"S{idx}: gorsel bulunamadi -> {b.get('path')}")
        return 0
    ph = b.get("h")
    pic = picture(slide, p, x, y, w=b.get("w", w), h=ph)
    h = (pic.height / PX) if pic else 0
    ctx.boxes.append((idx, "image", x, y, w, h))
    return h


BLOCKS = {
    "table": block_table, "insights": block_insights, "kpi": block_kpi,
    "bar": block_bar, "line": block_line, "panels": block_panels,
    "note": block_note, "text": block_text, "image": block_image,
}


# ----------------------------------------------------------------------------
# Slayt tipleri
# ----------------------------------------------------------------------------

def s_cover(slide, spec, ctx, idx):
    bg = spec.get("bg", "coral")
    set_bg(slide, bg)
    big = ctx.logo("inbound-big-o-white.png")
    if os.path.exists(big):
        pic = picture(slide, big, 800, -300, h=1400)
        if pic:
            _fade(pic, 14000)

    title = plain(spec.get("title", ""))
    lines = spec.get("title_lines") or [title]
    tpt = spec.get("title_pt", 54)
    for ln in lines:
        while tpt > 26 and text_w(ln, tpt, F_DISPLAY, True) > STAGE_W - 200:
            tpt -= 1
    lh = tpt * PX_PER_PT * 1.08
    block_h = len(lines) * lh + (34 if spec.get("subtitle") else 0)
    y = (STAGE_H - block_h) / 2 - 30
    for ln in lines:
        textbox(slide, 80, y, STAGE_W - 160, lh, ln, pt=tpt, family=F_DISPLAY,
                bold=True, color="white", align="c", line_pct=1.08, wrap=False)
        y += lh
    if spec.get("subtitle"):
        textbox(slide, 120, y + 14, STAGE_W - 240, 30, plain(spec["subtitle"]),
                pt=PT["h4"], color="white", align="c", line_pct=1.3)

    wm = ctx.logo("inbound-wordmark-white.png")
    if os.path.exists(wm):
        pic = picture(slide, wm, 0, STAGE_H - 94, h=34)
        if pic:
            pic.left = px((STAGE_W - pic.width / PX) / 2)


def s_agenda(slide, spec, ctx, idx):
    lw = STAGE_W * 0.45
    rect(slide, 0, 0, lw, STAGE_H, fill="coral")
    kicker = plain(spec.get("kicker", ""))
    if kicker:
        textbox(slide, 50, 250, lw - 100, 18, kicker.upper(), pt=PT["micro"],
                family=F_DISPLAY, color="white", line_pct=1.0)
    title_lines = spec.get("title_lines") or plain(
        spec.get("title", "SUNUM AKIŞI")).split(" ")
    tpt = 46
    for ln in title_lines:
        while tpt > 24 and text_w(ln, tpt, F_DISPLAY, False) > lw - 100:
            tpt -= 1
    y = 276
    for ln in title_lines:
        textbox(slide, 50, y, lw - 100, tpt * PX_PER_PT * 1.05, ln, pt=tpt,
                family=F_DISPLAY, bold=False, color="white", line_pct=1.05,
                wrap=False)
        y += tpt * PX_PER_PT * 1.05
    lg = ctx.logo("inbound-o-white.png")
    picture(slide, lg, 44, STAGE_H - 76, w=36, h=36)

    items = spec.get("items") or []
    rx, rw = lw + 60, STAGE_W - lw - 120
    top, bot = 64, STAGE_H - 64
    n = max(1, len(items))
    slot = (bot - top) / n
    for i, it in enumerate(items):
        iy = top + slot * i
        num = it.get("no") if isinstance(it, dict) else None
        label = it.get("label") if isinstance(it, dict) else str(it)
        num = num or f"{i+1:02d}"
        textbox(slide, rx, iy, rw, 20, str(num), pt=PT["h4"], color="ink3",
                line_pct=1.0)
        lpt = PT["h3"]
        while lpt > 12 and text_w(plain(label), lpt, F_DISPLAY, True) > rw:
            lpt -= 0.5
        textbox(slide, rx, iy + 22, rw, lpt * PX_PER_PT * 1.25, plain(label),
                pt=lpt, family=F_DISPLAY, bold=True, color="ink", line_pct=1.25)


def s_separator(slide, spec, ctx, idx):
    set_bg(slide, "teal")
    title = plain(spec.get("title", ""))
    tpt = spec.get("title_pt", PT["section"])
    while tpt > 22 and text_w(title, tpt, F_DISPLAY, True) > STAGE_W * 0.62:
        tpt -= 1
    tw = text_w(title, tpt, F_DISPLAY, True)
    tx = (STAGE_W - tw) / 2
    cy = STAGE_H / 2

    num = str(spec.get("no", "") or "")
    if num:
        npt = PT["section_num"]
        nw = text_w(num, npt, F_DISPLAY, True)
        while nw > tx * 0.8 and npt > 60:
            npt -= 4
            nw = text_w(num, npt, F_DISPLAY, True)
        nh = npt * PX_PER_PT
        textbox(slide, (tx - nw) / 2, cy - nh * 0.52, nw + 20, nh, num, pt=npt,
                family=F_DISPLAY, bold=True, color="teal_soft", align="c",
                line_pct=0.9, wrap=False)

    th = tpt * PX_PER_PT * 1.1
    rect(slide, (STAGE_W - 60) / 2, cy - th / 2 - 30, 60, 3.5, fill="white",
         radius=2)
    textbox(slide, tx - 20, cy - th / 2, tw + 40, th, title, pt=tpt,
            family=F_DISPLAY, bold=True, color="white", align="c", line_pct=1.1,
            wrap=False)
    rect(slide, (STAGE_W - 60) / 2, cy + th / 2 + 26, 60, 3.5, fill="white",
         radius=2)


def s_closing(slide, spec, ctx, idx):
    set_bg(slide, spec.get("bg", "teal"))
    big = ctx.logo("inbound-big-o-white.png")
    if os.path.exists(big):
        pic = picture(slide, big, -300, 200, h=1000)
        if pic:
            _fade(pic, 10000)
    title = plain(spec.get("title", "Teşekkürler"))
    tpt = spec.get("title_pt", 56)
    while tpt > 28 and text_w(title, tpt, F_DISPLAY, True) > STAGE_W - 200:
        tpt -= 1
    textbox(slide, 80, STAGE_H / 2 - 60, STAGE_W - 160, tpt * PX_PER_PT * 1.1,
            title, pt=tpt, family=F_DISPLAY, bold=True, color="white",
            align="c", line_pct=1.1, wrap=False)
    if spec.get("subtitle"):
        textbox(slide, 160, STAGE_H / 2 + 10, STAGE_W - 320, 60, spec["subtitle"],
                pt=PT["h4"], color="white", align="c", line_pct=1.4)
    wm = ctx.logo("inbound-wordmark-white.png")
    if os.path.exists(wm):
        pic = picture(slide, wm, 0, STAGE_H - 94, h=30)
        if pic:
            pic.left = px((STAGE_W - pic.width / PX) / 2)


def s_content(slide, spec, ctx, idx):
    dark = spec.get("bg") in ("teal", "dark")
    if spec.get("bg") and spec["bg"] not in ("white", None):
        set_bg(slide, "teal" if spec["bg"] == "dark" else spec["bg"])
    top = chrome(slide, spec, ctx, idx, dark=dark)
    bottom = footnotes(slide, spec.get("footnotes"), ctx, idx)

    grid = spec.get("grid") or [100]
    gap = spec.get("gap", 36)
    avail = STAGE_W - M_L - M_R
    tot = float(sum(grid))
    xs, ws, cx = [], [], M_L
    for g in grid:
        cw = (avail - gap * (len(grid) - 1)) * g / tot
        xs.append(cx)
        ws.append(cw)
        cx += cw + gap

    cursor = [top] * len(grid)
    auto = 0
    for b in spec.get("blocks") or []:
        fn = BLOCKS.get(b.get("type"))
        if not fn:
            ctx.warn(f"S{idx}: bilinmeyen blok tipi '{b.get('type')}'")
            continue
        if b.get("at"):
            x, y, w, _h = b["at"]
            fn(slide, b, x, y, w, ctx, idx)
            continue
        col = b.get("col")
        if col is None:
            col = auto % len(grid)
            auto += 1
        col = max(0, min(col, len(grid) - 1))
        y = cursor[col] + (b.get("mt") or 0)
        used = fn(slide, b, xs[col], y, ws[col], ctx, idx)
        cursor[col] = y + used + b.get("mb", 20)
        if y + used > bottom + 2:
            ctx.warn(f"TASMA S{idx}: '{b.get('type')}' blogu (kolon {col}) "
                     f"y={y+used:.0f}px, alt sinir {bottom:.0f}px - "
                     f"{y+used-bottom:.0f}px asiyor")
            ctx.overflowed.add((idx, b.get("type")))


SLIDES = {"cover": s_cover, "agenda": s_agenda, "separator": s_separator,
          "content": s_content, "closing": s_closing}


def _fade(pic, alpha_off):
    """Gorsele saydamlik uygular (big-O dekoratif marka)."""
    try:
        blip = pic._element.blipFill.find(qn("a:blip"))
        from lxml import etree
        el = etree.SubElement(blip, qn("a:alphaModFix"))
        el.set("amt", str(100000 - alpha_off))
    except Exception:
        pass


# ----------------------------------------------------------------------------
# Deste kurulumu
# ----------------------------------------------------------------------------

def _blank_layout(prs):
    """En bos layout'u sec ve mirasli placeholder'lari temizle."""
    best, best_n = prs.slide_layouts[0], 99
    for lay in prs.slide_layouts:
        n = len(lay.placeholders)
        if n < best_n:
            best, best_n = lay, n
    return best


def build(spec, out_path, assets_dir, base_dir, check_only=False):
    prs = Presentation()
    prs.slide_width = px(STAGE_W)
    prs.slide_height = px(STAGE_H)
    layout = _blank_layout(prs)
    ctx = Ctx(assets_dir, base_dir)

    slides_spec = spec.get("slides") or []
    for i, s in enumerate(slides_spec, 1):
        kind = s.get("type", "content")
        fn = SLIDES.get(kind)
        if not fn:
            ctx.warn(f"S{i}: bilinmeyen slayt tipi '{kind}' - atlandi")
            continue
        slide = prs.slides.add_slide(layout)
        for shp in list(slide.shapes):
            if shp.is_placeholder:
                shp._element.getparent().remove(shp._element)
        if kind == "content" and not s.get("bg"):
            set_bg(slide, "white")
        fn(slide, s, ctx, i)
        if s.get("notes"):
            slide.notes_slide.notes_text_frame.text = plain(s["notes"])

    # sag kenar taramasi (alt sinir taramasi s_content icinde, kolon bilgisiyle)
    for (si, label, x, y, w, h) in ctx.boxes:
        if x + w > STAGE_W - M_R + 2:
            ctx.warn(f"TASMA S{si}: {label} blogu sag kenari asiyor "
                     f"(x+w={x+w:.0f}px, sinir {STAGE_W-M_R}px)")

    if not check_only:
        prs.save(out_path)
    return ctx, len(slides_spec)


def main():
    ap = argparse.ArgumentParser(description="deck.json -> Inbound PPTX")
    ap.add_argument("spec")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--assets", default=None,
                    help="varsayilan: <script>/../assets")
    ap.add_argument("--check", action="store_true", help="dosya yazmadan dogrula")
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    assets = a.assets or os.path.normpath(os.path.join(here, "..", "assets"))
    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)
    base = os.path.dirname(os.path.abspath(a.spec))
    out = a.out or spec.get("output") or os.path.splitext(a.spec)[0] + ".pptx"
    if not os.path.isabs(out):
        out = os.path.join(base, out)

    ctx, n = build(spec, out, assets, base, check_only=a.check)

    if not _HAVE_PIL:
        print("UYARI: PIL yok - font olcumu yaklasik, tasma tespiti zayif.")
    print(f"{n} slayt {'dogrulandi' if a.check else 'uretildi'}"
          f"{'' if a.check else ' -> ' + out}")
    if ctx.warnings:
        print(f"\n{len(ctx.warnings)} uyari:")
        for w in ctx.warnings:
            print("  -", w)
        return 1
    print("Uyari yok.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
