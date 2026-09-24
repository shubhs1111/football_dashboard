# Google Stitch — UI/UX Enhancement Brief

Paste the prompt below into Google Stitch (stitch.withgoogle.com). Optionally upload
reference screenshots of the current app (Stitch accepts image uploads). Good screens to
capture from your live app — https://footballdashboard-xbnqcqfmhej7bdikdrq3mh.streamlit.app :
1. Executive Summary (KPI header + the two charts)
2. Match Results & Form (the data table + the two split charts)
3. Player Performance Matrix (the ranked table + minutes chart)
4. Final Investigation → a tactics board (pitch + player inspector + "how to read")
Tip: collapse the sidebar (« icon) and use your browser full-screen (F11) for cleaner shots.

---

## PROMPT (copy–paste into Stitch)

Redesign and modernise the UI/UX of an existing **football (soccer) analytics dashboard** —
a "Manchester United 2026/27 Tactical Investigation" web app that analyses why the team has
started the season poorly. It's a data-dense, single-page analytics product with a left sidebar
and seven tabbed sections. Keep it a **dark, premium sports-analytics** aesthetic with a
Manchester United **red (#DA020E)** accent, but make it feel more like a modern broadcast /
Opta / The Athletic product than a default dashboard.

**Audience:** football analysts, coaches, and fans reading a tactical investigation. Desktop-first
but must also work on mobile.

**Screens / sections to redesign (tabs):**
1. **Executive Summary** — a KPI header (record, goals for/against, xG, xG conceded, possession,
   league standing) plus a results pie chart and an xG-vs-xGA bar chart.
2. **Match Results & Form** — a match-by-match data table, home/away split, and first-vs-second-half
   goals charts.
3. **Attacking Analytics** — shot-volume line chart, top goal contributors bar chart, and two
   "insight" cards.
4. **Defensive & Transition Deficiencies** — opponent-shots-vs-goals chart, a late-goals timeline
   table, and three factor cards.
5. **Player Performance Matrix** — a searchable 22-player stats table, a horizontal minutes bar
   chart, and an xG-by-position box plot.
6. **Final Investigation & Tactics Boards** — the centrepiece: four sub-tabbed "issues", each with an
   **interactive football pitch/tactics board** (player markers, shaded vulnerability zones, passing
   arrows), a player inspector panel, layer toggles, and a "how to read this board" explainer plus
   problem/evidence/impact/explanation blocks.
7. **Data Methodology** — sources, metric definitions, and limitations.

**Design goals — what to improve:**
- A stronger **visual hierarchy** and a cohesive design system (typography scale, spacing, card
  styles, consistent chart color language) instead of default Streamlit components.
- Make **KPI cards** feel premium (icons, trend indicators, clear "what is compared" microcopy) —
  currently they read as plain metrics.
- Elevate the **tactics board** into a proper football-broadcast pitch visual with a clean player
  inspector side panel and legible layer controls.
- Better **information density management**: the app is stat-heavy; introduce progressive disclosure,
  section intros, and clearer separation between "the visual" and "the analysis text".
- **Responsive / mobile** layout for the sidebar filters, tabs, tables, and pitch board.
- Improve **data tables** (readable highlighting, sticky headers, rank columns) and **tooltips**.
- Suggest a refined **navigation** pattern (the 7 tabs + 4 sub-tabs are a lot) — e.g. a left nav,
  sticky sub-nav, or a summary-first layout.

**Style direction:** dark theme, MUFC red primary accent, teal/amber/blue semantic colors for
good/warning/info, generous whitespace, rounded cards, subtle shadows, a clean geometric sans-serif.
Think "modern sports data product," not "admin dashboard."

Please propose a redesigned layout and component system for these screens, starting with the
**Executive Summary** and the **Tactics Board**.

---

## Current known UX pain points (context for the redesign)
- KPI values were truncating in narrow columns (recently split into 2 rows of 3).
- Chart hover tooltips were hard to read / truncated (recently themed).
- Tables showed a raw 0-based index and unexplained green highlights.
- The tactics board is information-dense and can feel crowded at small widths.
- Marker labels on the pitch can overlap in tight areas (e.g. defensive set-piece box).
- Everything is a Streamlit default look; it needs a distinct visual identity.

## Current tech (for context only — Stitch outputs its own design/code)
Streamlit + Plotly + Pandas, dark theme, MUFC red (#DA020E) accent, custom CSS cards.
