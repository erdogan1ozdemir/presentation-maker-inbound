# Inbound Design System

Design language, CSS tokens, typography, asset library, UI kit, and sample slides for **Inbound** - a full-service digital marketing agency in Turkey.

> **Contact:** welcome@inbound.com.tr · © Inbound

---

## What is Inbound?

Inbound is a digital performance marketing agency offering four core service lines:

- **Performance Marketing** - paid search, paid social, programmatic, campaign strategy & optimization.
- **Media** - media planning, buying, and creative production across digital + offline channels.
- **SEO** - technical SEO, on-page, off-page, outreach, content development, site audits, market & competitor analysis.
- **Marketing Intelligence** - GA4 implementation, dataLayer design, AdTech setup (Google Ads / Meta), reporting frameworks, analysis support.

Its clients include enterprise Turkish brands such as **Turkcell**, **Boyner**, **Birkenstock**, **Eczacıbaşı** and **Özdilek** (derived from the attached corporate deck and SEO reports).

The output work is predominantly **bilingual (TR primary, EN secondary)** with a professional, analytical tone - SEO audits, performance reports, strategy decks.

## Source materials (for the original author / team)

| File | Purpose |
|---|---|
| `uploads/Inbound_Sunum_Tasarim_Rehberi.md` | Canonical TR-language presentation design spec (colors, layouts, typography, pptxgenjs rules). |
| `uploads/Copy of Inbound-Corporate-Presentation-Template-280125.pptx` | 43-slide corporate template - cover, agenda, 4 section separators, content layouts, quotes, timelines, testimonial slides (Turkcell, Boyner), KPI, stats, closing. |
| `uploads/Özdilekteyim SEO Değerlendirme Q4 Internal.pptx` | Real-world SEO report (internal). Reference for data-viz + insight conventions. |
| `uploads/Eczacıbaşı SEO Değerlendirme 2025.pptx` | Real-world multi-brand SEO report. Reference for tables, heat-map coloring, footnoted metrics. |
| `uploads/inbound-yazı-logo.png` | White wordmark logo, 230×48. |
| `uploads/inbound-kucuk-logo.png` | White "O" ring mark, 79×78. |
| `uploads/inbound-buyuk-o.png` | Large decorative "O" ring mark, 605×1080. |

Fonts (Bricolage Grotesque + Outfit) were extracted from the pptx's embedded `.fntdata` and live in `fonts/` as real TTFs - licensed under OFL via Google Fonts.

---

## Index - what's in this folder

| Path | Contents |
|---|---|
| `README.md` | This document. Brand context + content + visual foundations + iconography. |
| `SKILL.md` | Agent Skill entry point - for Claude Code / agent use. |
| `colors_and_type.css` | **Start here.** CSS variables for the entire token system. |
| `fonts/` | Bricolage Grotesque (display) + Outfit (body) - real TTFs from the pptx. |
| `assets/` | Logos (white / coral / teal tints), stock photos, brand illustrations. |
| `preview/` | Static HTML cards populating the Design System review tab. |
| `slides/` | Sample deck: cover, agenda, separator, content, cards, quote, KPI, timeline, closing. |
| `ui_kits/website/` | Inbound marketing-site UI kit - hero, services, case studies, contact, nav, footer. |
| `uploads/` | Original client-supplied assets, kept verbatim. |

---

## Content Fundamentals - voice, tone, copy

**Language:** Turkish primary, English for technical terms and section labels. It is **not** code-switching; English terms stay English (*"funnel measurement"*, *"dataLayer"*, *"Heat Map by Team View"*) inside TR sentences.

**Tone:** Professional, analytical, measured. Reads like a consulting report - not a marketing brochure. Statements are qualified (*"…olabilir"*, *"…değerlendirilmelidir"*, *"…önerilmektedir"*) rather than declarative. Passive/impersonal constructions preferred (*"görülmektedir"*, *"gerçekleşmiştir"*, *"dikkat çekmektedir"*).

**Pronouns:** Rarely used. No "I", rarely "we" in copy. When "we" appears it's plural collective (*"Our Analytics & Insights relationship makes us special"*) - not personal. Audience is addressed as "siz" / "you" sparingly, usually in guidance (*"sizin anlattıklarınıza odaklanmasını sağlamalısınız"*).

**Casing:**
- Titles: **Sentence case** in TR; **Title Case** for English headings (*"Companies we've worked with"*, *"Our Analytics & Insights relationship"*).
- Section labels / breadcrumbs: **Mixed** - "SUNUM AKIŞI" and "SECTION TITLE" are uppercase; individual slide titles are sentence/title case.
- ALL-CAPS is used sparingly for breadcrumbs, badges, KPI labels (*"OFFICES"*, *"ACTIVE USERS"*, *"DISCOVER / DEFINE / DEVELOP / DELIVER"*).

**Numbers:** Always explicit with % and sign. *"%18 düşerken"*, *"-%37 düşerken"*, *"%8 artmıştır"*, *"+1.8 iyileşme ↑"*. Numbers in insight sentences are **bold** (Bricolage Bold). Negatives red, positives green, key terms coral.

**Punctuation:** Turkish curly quotes (*"…"*), `➔` arrow bullets (not `→`), ampersand `&` in titles. Use `-` (hyphen) or `&` as separators - em-dashes (`—`) should be avoided.

**Tone of guidance:** Recommendation and suggestion language is preferred (*"…önerilmektedir"*, *"…değerlendirilmelidir"*, *"…tercih edilebilir"*) over imperative/commanding forms. The voice should guide, not dictate.

**Emoji:** Not used for decoration. Rare functional icons only: ✅ for gains, ❌ or ⚠ for losses, ↑ ↓ for trend direction. Never in body copy. No faces, no hand gestures.

**Insight pattern:**
```
➔ [context clause] **[bold metric]** [explanation].
   [optional follow-up analysis / cause].
```

**Vibe:** Corporate-confident. Data-forward. Optimistic on accent (coral) but the ink is grounded dark-teal. Never playful, never cutesy, never loud. Feels closer to a Bain/BCG deck than a growth-hacker pitch.

**Example copy (from the real template):**
- *"Our Analytics & Insights relationship makes us special."*
- *"Designed and implemented dataLayer for optimal data collection, reporting, analysis and activation."*
- *"Dikkat çekici, ana noktayı karşı tarafa aktaran, üstüne yaptığımız sözlü anlatım ile pekişen derecede özet açıklamalar yer alır."*
- *"We are very happy with the design" - Head of Marketing @ Turkcell* (testimonial)

---

## Visual Foundations

### Color
Two anchor colors do all the heavy lifting:
- **Coral / Salmon `#FF7B52`** - the brand hero. Full-bleed on cover and closing slides, agenda left panel, breadcrumb copy, accent lines, text-highlight blocks behind key words in body copy (never behind slide titles), source-pill backgrounds, CTA buttons.
- **Dark Teal `#10332F`** - ink. All body copy, all headings (except on coral/teal backgrounds), section-separator fills.

**Default canvas is pure white (`#FFFFFF`).** No off-white, no cream. Content slides are white or transparent - only cover/closing (coral) and separators (teal) break the rule. The agenda is the single split-background slide (45% coral / 55% white).

Data-viz adds: red `#D32F2F` + wash `#FFCDD2` (loss), green `#2E7D32` + wash `#C8E6C9` (gain), gold `#F5A623` (previous-period bars), dark gray `#4A4A4A` (current-period bars), trend-line red `#E53935`. Heat-map tables color both the cell and the text.

### Typography
Exactly two families:
- **Bricolage Grotesque** (display) - all titles, breadcrumbs' section name, numerals, KPI values, card titles, bold insight numbers, source pills, closing "Teşekkürler". Weights 300 / 400 / 500 / 600 / 700 / 800.
- **Outfit** (body) - everything else: body paragraphs, captions, breadcrumb slide titles, table data, agenda numbers, insight text. Weights 300 / 400 / 500 / 600 / 700.

Cover title 44–52pt, section separator 36–44pt + a 160–200pt translucent numeral, slide title 28–36pt, card title 18–22pt, body 14–16pt. Insight bullets start with `➔`.

### Spacing & layout (16:9, 13.33″ × 7.5″)
Generous breathing room. Content area starts at x=0.5″, y=0.8″. Breadcrumb at x=0.3″, y=0.2″. Logo at x=0.3″, y=7.0″ (sol alt). Separator numbers peek off the left edge (x=−0.3″) to suggest a magazine layout. Grid slides use 4 equal vertical dividers at ~5% opacity as decorative structure.

### Backgrounds
Pure white content. No gradients. No repeating patterns. **Decorative faint vertical grid lines** (`#F0EDE8`, 4 columns, 5–10% opacity) appear on text-only and quote slides. The oversized "O" mark (`inbound-big-o-white.png`) can overlay coral backgrounds as a decorative half-ring peeking off-canvas. Imagery is **circular-cropped portrait photography** - warm, candid team/office shots (see `assets/photo-team-analytics.png`).

### Imagery
**Warm, candid office photography**, always **circle-cropped**. Human subjects, mid-action, natural light, muted warm palette. No stock-smile-over-laptop clichés done badly - these feel documentary. No duotones, no B&W, no heavy filtering. Grain is absent. When no photo exists, use a coral flat-color panel or the big-O mark decoratively.

### Animation & motion
The source material is a print-style pptx - no motion design documented. Default to **subtle, fast, un-bouncy** for web: 140–220ms `cubic-bezier(.2,.8,.2,1)`. Fades and slight translates (4–8px). No parallax, no spring bounces, no letter-by-letter reveals. Honor the analytical tone.

### Hover / press states
- **Primary button (coral):** hover → `#E85F36` (coral-deep). Press → same, translateY(1px).
- **Ghost / link:** hover → coral color + underline.
- **Card:** hover → shadow lifts (`--shadow-card` → `--shadow-card-hover`), no scale.
- Never opacity-only hovers.

### Borders & dividers
Hairline `#E0E0E0` (0.5–1pt) on tables. Cards are **shadow-only, no border**. A decorative 3–4pt coral accent line (`~0.5″` wide, rounded caps) is the brand's signature separator - above and below section titles, flanking quotes, between timeline milestones. Borders are never colored except coral accent lines.

### Radii
- Cards / image panels: **16–20px** (`--r-lg` / `--r-xl`) - matches pptx `rectRadius: 0.15` / `0.2`.
- Buttons / pills: **pill** (`--r-pill`).
- Source badge / small chips: 8–12px (`--r-sm` / `--r-md`).
- Tables: 0 radius on cells, 12px on outer frame.

### Shadows
One shadow system, very soft:
- **Card:** `0 2px 8px rgba(16,51,47,.08)` - matches the pptx `outer, blur 8, offset 2, angle 135, opacity .08`.
- **Card-hover:** `0 6px 20px rgba(16,51,47,.12)`.
- **Pop / modal:** `0 12px 32px rgba(16,51,47,.16)`.
No inner shadows, no glow, no neumorphism.

### Text alignment in data & stat elements
**Default: center-aligned.** KPI tiles, stat cards, carousels, table data columns, and any numeric/metric display should center their text and values. Category/label columns in tables stay left-aligned for scannability. Right-alignment is acceptable only when there's a clear reason (e.g. aligning decimal points in a dense financial table) - never as a reflex default.

### Cards (canonical recipe)
`bg: white · radius: 16px · shadow: card · padding: 20–24px`.  
If numbered: a 48–60pt Bricolage Bold numeral at ~15% opacity sits top-right.  
If iconed: a 0.45″ coral circle holds a white icon, top-left.

### Transparency & blur
**Almost never.** The only legal uses:
- Separator numeral at ~20% opacity (teal on teal).
- Decorative grid lines at 5–10%.
- Text-highlight coral block at 80–100% (not transparent - just non-100%).
No backdrop-blur. No glass. No tinted overlays.

### Fixed layout rules
- Logo: sol alt (bottom-left) on every content + agenda slide. **Never** on separators or closing. On cover, use the wordmark logo, bottom-center.
- Source badge: sol alt, just inside the logo margin, on every data slide.
- Breadcrumb: sol üst, coral. `Bölüm Adı | Slide Başlığı` format.

---

## Iconography

**The brand has no custom icon font and no extensive icon library.** What exists:

- **Ring / circle ("O") mark** (`assets/inbound-o-*.png`, `assets/inbound-big-o-*.png`) - the primary brand glyph, derivable from the "O" in the wordmark. Used as a small avatar-sized mark bottom-left on slides, and as an oversized decorative half-ring on full-bleed coral backgrounds.
- **Wordmark** (`assets/inbound-wordmark-*.png`) - three tints provided: white (original), coral, teal.
- **Functional emoji** (used sparingly, never decoratively): ✅ gain, ❌ / ⚠ loss, ↑ ↓ trend.
- **Arrow bullet** (`➔`) - the signature insight marker. Uses the Unicode heavy rightward arrow, **not** `→`. Set in body font, dark-teal color.
- **Quote mark** (`"`) - oversized Bricolage Bold, 48–60pt, dark-teal, used as a standalone glyph flanking a quotation.
- **KPI card icons** - small filled white shapes inside the 0.45″ coral circle. The source deck uses generic glyphs (briefcase, user, dollar). No specific set was shipped in the template.

**When an icon is needed that isn't in the system:** substitute from **Lucide** (https://lucide.dev) - a 1.5px-stroke open-source set. Its stroke weight and squared-off corners match Inbound's modern-geometric type personality. Usage in UI kits loads Lucide via CDN:

```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
```

**Substitution flag:** Lucide is a close-match stand-in, not the official brand icon set. When a production-grade set is agreed with the client, replace.

**For brand logos of clients** (Turkcell, Boyner, Birkenstock, Eczacıbaşı) that appear in testimonial or "companies we've worked with" slides: these are the clients' own marks and **not** part of this design system - fetch from the client's brand kit or from a source like Brandfetch at use-time.

---

## Font substitution flag

The TTFs in `fonts/` were extracted from the uploaded pptx's embedded `.fntdata` chunks - they are the **actual Bricolage Grotesque and Outfit** (OFL licensed). No substitution. If the canonical Google Fonts drops update, update these files too. Fallback stack: `'Calibri', system-ui, sans-serif`.

---

## Iterate

This system is a first pass. **Please flag:**
- Any terminology or tone examples that don't match your house voice.
- Any client logos or brand assets that should be added to `assets/`.
- Whether you want a **dark** theme (current system is white-first).
- Whether motion design guidance is needed for a video/animation context (the source is deck-first).
