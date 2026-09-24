# ==============================================================================
# MANCHESTER UNITED 2026/27 SEASON ANALYTICS DASHBOARD (V4)
# "Why Has Manchester United Started the Season Poorly?"
# V4: Google Stitch "Tactical Intelligence & Telemetry" design, branded "Theatre of Data"
#     (Tactical Intelligence & Telemetry design system), bound to the real dataset.
# Built with Streamlit, Plotly and Pandas
# ==============================================================================

import html as _html
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# ------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & DESIGN SYSTEM
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Theatre of Data · MUFC 2026/27",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="auto",  # open on desktop, collapsed on phones
)

# Palette tokens (mirror the Stitch "Tactical Intelligence & Telemetry" DESIGN.md)
CANVAS, CARD, ELEV, OVERLAY, HIGHLIGHT = "#0B0E14", "#10141D", "#161B26", "#1B2232", "#222B3D"
RED, RED_CORE = "#FF2D3B", "#DA020E"
SEC, PASS, TACT = "#7bd0ff", "#38BDF8", "#06B6D4"
POS, WARN, DANGER = "#10B981", "#F59E0B", "#EF4444"
TEXT, MUTED, ERR = "#e1e2eb", "#e7bcb9", "#ffb4ab"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Geist:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block');
:root{
  --canvas:#0B0E14; --card:#10141D; --elev:#161B26; --overlay:#1B2232; --hl:#222B3D;
  --low:#191c22; --lowest:#0b0e14; --high:#272a31; --highest:#32353c; --bright:#363940;
  --red:#FF2D3B; --red-core:#DA020E; --sec:#7bd0ff; --pass:#38BDF8; --tact:#06B6D4;
  --pos:#10B981; --warn:#F59E0B; --danger:#EF4444; --err:#ffb4ab; --err-c:#93000a; --on-err-c:#ffdad6;
  --text:#e1e2eb; --muted:#e7bcb9; --silver:#94A3B8; --primary:#ffb3ae; --border:rgba(255,255,255,0.08);
}
/* ---------- Streamlit shell ---------- */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"]{ background:var(--canvas); color:var(--text); }
html, body, .stApp, .stMarkdown, p, div, label, input, textarea, button{ font-family:'Geist', sans-serif; }
/* Streamlit's (invisible) app header sits on top of the sticky top bar and would swallow its clicks */
[data-testid="stHeader"]{ background:transparent; height:0; pointer-events:none; }
[data-testid="stHeader"] [data-testid="stExpandSidebarButton"], [data-testid="stHeader"] button{ pointer-events:auto; }
/* Keep the toolbar (it holds the "expand sidebar" button) but hide its Deploy / menu items */
[data-testid="stDecoration"], [data-testid="stToolbarActions"], [data-testid="stMainMenu"], [data-testid="stAppDeployButton"]{ display:none; }
/* the toolbar is an invisible full-width strip over the top bar: let clicks pass through it (only » stays clickable) */
[data-testid="stToolbar"]{ pointer-events:none !important; background:transparent !important; }
[data-testid="stExpandSidebarButton"]{ position:fixed; top:0.7rem; left:0.75rem; z-index:1000; pointer-events:auto;
  background:var(--elev); border:1px solid var(--border); border-radius:0.5rem; box-shadow:0 4px 12px rgba(0,0,0,0.4); }
[data-testid="stExpandSidebarButton"]:hover{ background:var(--hl); box-shadow:0 0 0 1px var(--red), 0 4px 12px rgba(0,0,0,0.4); }
[data-testid="stExpandSidebarButton"] *{ color:var(--text) !important; }
/* leave room for the floating expand button when the sidebar is collapsed */
.stApp:has([data-testid="stSidebar"][aria-expanded="false"]) .st-key-topbar{ padding-left:3.75rem; }
[data-testid="stMainBlockContainer"], .block-container{ max-width:1440px !important; padding:0 1.5rem 3rem !important; }
.stMarkdown p{ margin-bottom:0; }
::selection{ background:var(--red-core); color:var(--text); }

/* ---------- Sidebar = Stitch left rail ---------- */
[data-testid="stSidebar"]{ background:var(--card) !important; border-right:none; box-shadow:0 1px 8px rgba(0,0,0,0.4);
  min-width:18rem !important; max-width:18rem !important; }
/* slim strip at the top of the rail holding the « collapse button (always visible, never clipped) */
[data-testid="stSidebarHeader"]{ height:2.4rem !important; min-height:2.4rem; padding:0.55rem 0.75rem 0 !important;
  display:flex !important; justify-content:flex-end; align-items:center; }
[data-testid="stSidebarCollapseButton"]{ position:static !important; display:block !important; visibility:visible !important; opacity:1 !important; }
[data-testid="stSidebarCollapseButton"] button{ background:var(--elev) !important; border:1px solid var(--border) !important;
  border-radius:0.5rem !important; color:var(--muted) !important; }
[data-testid="stSidebarCollapseButton"] button:hover{ background:var(--hl) !important; color:var(--text) !important; box-shadow:0 0 0 1px var(--red); }
[data-testid="stSidebarUserContent"]{ padding:0 0.75rem 1rem !important; }
/* stretch the rail's content to full height so the Data Feed card can sit at the very bottom */
[data-testid="stSidebarUserContent"]{ display:flex; flex-direction:column; min-height:calc(100vh - 4.4rem); }  /* 2.4rem header + 1rem gap above + 1rem bottom breathing room */
[data-testid="stSidebarUserContent"] > div{ flex:1; display:flex; flex-direction:column; }
[data-testid="stSidebarUserContent"] > div > [data-testid="stVerticalBlock"]{ flex:1; }
[data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.side-feed){ margin-top:auto; padding-top:1.5rem; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{ gap:0.25rem; }
[data-testid="stSidebar"] .stButton button{ justify-content:flex-start !important; border:none !important; border-radius:0.5rem;
  padding:0.5rem 1rem; min-height:2.4rem; font-family:'Geist'; font-size:0.8125rem; }
[data-testid="stSidebar"] .stButton button > div{ justify-content:flex-start; }
[data-testid="stSidebar"] .stButton button p{ font-size:0.8125rem; }
[data-testid="stSidebar"] button[data-testid="stBaseButton-tertiary"]{ background:transparent; color:var(--muted); }
[data-testid="stSidebar"] button[data-testid="stBaseButton-tertiary"]:hover{ background:var(--elev); color:var(--text); }
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"]{ background:var(--overlay) !important; color:var(--text) !important;
  font-weight:600; box-shadow:inset 3px 0 0 0 var(--red-core) !important; }
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] p{ font-weight:600; }

/* ---------- Sticky top bar ---------- */
[data-testid="stLayoutWrapper"]:has(> .st-key-topbar){ position:sticky; top:0; z-index:990; }
.st-key-topbar{ background:rgba(16,20,29,0.85); backdrop-filter:blur(24px);
  -webkit-backdrop-filter:blur(24px); margin:0 -1.5rem 0.5rem; padding:0.55rem 1.5rem; box-shadow:0 1px 8px rgba(0,0,0,0.35);
  width:calc(100% + 3rem) !important; }
.st-key-topbar [data-testid="stHorizontalBlock"]{ gap:1rem; }
.st-key-topbar [data-testid="stColumn"]:nth-child(2) [data-testid="stVerticalBlock"]{ align-items:center; }   /* scope control centred */
.st-key-topbar [data-testid="stColumn"]:last-child [data-testid="stVerticalBlock"]{ align-items:flex-end; }  /* filters right-aligned */
.st-key-topbar [data-testid="stPopover"] button{ min-height:2.25rem; padding:0 1rem; }
/* Streamlit pins the markdown wrappers to a fixed height; let the context label size to its content so it centres */
.st-key-topbar [data-testid="stElementContainer"]:has(.topbar-ctx), .st-key-topbar [data-testid="stMarkdown"]:has(.topbar-ctx),
.st-key-topbar [data-testid="stMarkdown"]:has(.topbar-ctx) > div,
.st-key-topbar [data-testid="stColumn"]:has(.topbar-ctx) > [data-testid="stVerticalBlock"]{ height:auto !important; min-height:2.25rem; }
/* Streamlit's markdown carries margin-bottom:-16px; inside a centred flex wrapper that pushes the label 8px down */
.st-key-topbar [data-testid="stMarkdownContainer"]:has(.topbar-ctx){ margin-bottom:0 !important; }
[data-testid="stStatusWidget"]{ display:none !important; }  /* "Running… Stop" would float over the Filters button */

/* ---------- Keyed containers rendered as Stitch cards ---------- */
[class*="st-key-card"]{ background:var(--card); border-radius:0.75rem; padding:1.25rem; box-shadow:0 1px 3px rgba(0,0,0,0.35); }
[class*="st-key-bar"]{ background:rgba(11,14,20,0.5); border-radius:0.75rem; padding:0.75rem 1rem; }
.st-key-cta{ position:relative; overflow:hidden; border-radius:0.75rem; padding:1.25rem 1.5rem;
  background:linear-gradient(90deg, var(--elev), var(--card), var(--elev)); box-shadow:0 20px 25px -5px rgba(0,0,0,0.4); }
/* clickable card overlay: a transparent full-size st.button sits on top of the card markup */
[class*="st-key-click"]{ position:relative; gap:0 !important; }
[class*="st-key-click"] [data-testid="stElementContainer"]:has(.stButton){ position:absolute; inset:0; z-index:5; margin:0; }
[class*="st-key-click"] .stButton, [class*="st-key-click"] .stButton button{ width:100%; height:100%; opacity:0; cursor:pointer; }

/* zero-footprint holder for the scroll helper component */
.st-key-scrollhook{ position:absolute !important; width:0 !important; height:0 !important; overflow:hidden !important; }
[data-testid="stElementContainer"]:has(> .st-key-scrollhook), [data-testid="stLayoutWrapper"]:has(> .st-key-scrollhook){ position:absolute; height:0; margin:0; }

/* ---------- Widgets ---------- */
.stButton button[data-testid="stBaseButton-primary"], [data-testid="stDownloadButton"] button[data-testid="stBaseButton-primary"]{
  background:var(--red-core); border:none; color:#fff; font-family:'Plus Jakarta Sans'; font-weight:700; border-radius:0.5rem;
  box-shadow:0 0 20px rgba(255,45,59,0.3); }
.stButton button[data-testid="stBaseButton-primary"]:hover{ background:var(--red); box-shadow:0 0 20px rgba(255,45,59,0.45); color:#fff; }
.stButton button[data-testid="stBaseButton-secondary"], [data-testid="stDownloadButton"] button, [data-testid="stPopover"] button{
  background:var(--elev); border:none; color:var(--muted); border-radius:0.5rem; font-size:0.8125rem; }
.stButton button[data-testid="stBaseButton-secondary"]:hover, [data-testid="stDownloadButton"] button:hover, [data-testid="stPopover"] button:hover{
  background:var(--hl); color:var(--text); border:none; }
[data-testid="stDownloadButton"] button p, [data-testid="stPopover"] button p{ font-size:0.8125rem; font-weight:500; }
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div{ background:var(--elev) !important; border-color:var(--border) !important; }
[data-baseweb="input"]:focus-within{ border-color:var(--pass) !important; }
input{ color:var(--text) !important; }
[data-baseweb="tag"], [data-testid="stMultiSelectTagsContainer"] > span > span{ background:var(--overlay) !important; color:var(--text) !important;
  box-shadow:inset 0 -2px 0 var(--red); }
[data-baseweb="popover"] [data-baseweb="menu"], [data-baseweb="popover"] ul{ background:var(--elev) !important; }
[data-testid="stPopoverBody"]{ background:var(--elev); border:1px solid var(--border); }
/* segmented control + pills = Stitch filter tabs */
[data-testid="stButtonGroup"]{ background:var(--low); padding:2px; border-radius:0.5rem; gap:2px; display:inline-flex; flex-wrap:wrap; }
[data-testid="stButtonGroup"] button{
  background:transparent !important; border:none !important; color:var(--muted) !important; border-radius:0.5rem !important; min-height:1.9rem; }
[data-testid="stButtonGroup"] button:hover{ color:var(--text) !important; }
[data-testid="stButtonGroup"] button[aria-checked="true"], [data-testid="stButtonGroup"] button[data-selected="true"],
[data-testid="stButtonGroup"] button[aria-pressed="true"]{
  background:var(--overlay) !important; border:none !important; color:var(--text) !important; border-radius:0.5rem !important;
  box-shadow:inset 0 -2px 0 var(--red); min-height:1.9rem; }
[data-testid="stButtonGroup"] button p{ font-family:'Geist'; font-size:0.6875rem !important; letter-spacing:0.12em; text-transform:uppercase; font-weight:600; }
[data-testid="stWidgetLabel"] p{ font-family:'Geist'; font-size:0.6875rem !important; letter-spacing:0.12em; text-transform:uppercase; font-weight:600; color:var(--muted); }
[data-testid="stPlotlyChart"]{ background:transparent; }
[data-testid="stAlert"]{ background:var(--elev); border:1px solid var(--border); border-radius:0.75rem; }

/* ---------- Typography (Stitch tokens) ---------- */
.msi{ font-family:'Material Symbols Outlined'; font-weight:normal; font-style:normal; line-height:1; letter-spacing:normal;
  text-transform:none; display:inline-block; white-space:nowrap; direction:ltr; -webkit-font-feature-settings:'liga';
  font-feature-settings:'liga'; -webkit-font-smoothing:antialiased; vertical-align:middle; }
.h-xl{ font-family:'Plus Jakarta Sans'; font-size:3.25rem; line-height:1.08; letter-spacing:-0.03em; font-weight:800; color:var(--text); }
.h-lg{ font-family:'Plus Jakarta Sans'; font-size:2.25rem; line-height:1.15; letter-spacing:-0.02em; font-weight:800; color:var(--text); }
.h-md{ font-family:'Plus Jakarta Sans'; font-size:1.5rem; line-height:1.3; letter-spacing:-0.01em; font-weight:600; color:var(--text); }
.h-sm{ font-family:'Plus Jakarta Sans'; font-size:1.25rem; line-height:1.35; font-weight:600; color:var(--text); }
.body-lg{ font-family:'Geist'; font-size:1.125rem; line-height:1.65; color:var(--muted); }
.body-md{ font-family:'Geist'; font-size:0.9375rem; line-height:1.55; color:var(--muted); }
.body-sm{ font-family:'Geist'; font-size:0.8125rem; line-height:1.5; letter-spacing:0.01em; color:var(--muted); }
.lbl{ font-family:'Geist'; font-size:0.6875rem; line-height:1.2; letter-spacing:0.12em; font-weight:600; text-transform:uppercase; color:var(--muted); }
.lbl-sm{ font-family:'Geist'; font-size:0.75rem; line-height:1.3; letter-spacing:0.02em; font-weight:500; color:var(--muted); }
.mono{ font-family:'Geist'; font-variant-numeric:tabular-nums; font-weight:600; letter-spacing:-0.01em; }
.stat{ font-family:'Plus Jakarta Sans'; font-weight:800; font-size:2.25rem; line-height:1.05; letter-spacing:-0.03em; color:var(--text); }
.stat-xl{ font-family:'Plus Jakarta Sans'; font-weight:800; font-size:2.75rem; line-height:1; letter-spacing:-0.03em; }
.t{ color:var(--text); } .m{ color:var(--muted); } b, strong{ color:var(--text); font-weight:600; }

/* ---------- Layout utilities ---------- */
.row{ display:flex; align-items:center; } .col{ display:flex; flex-direction:column; } .between{ justify-content:space-between; }
.start{ align-items:flex-start; } .wrap{ flex-wrap:wrap; } .grow{ flex:1; min-width:0; }
.gx{ gap:0.25rem; } .gs{ gap:0.5rem; } .gm{ gap:1rem; } .gl{ gap:1.5rem; }
.grid{ display:grid; gap:1rem; } .g2{ grid-template-columns:repeat(2,minmax(0,1fr)); } .g3{ grid-template-columns:repeat(3,minmax(0,1fr)); }
.g4{ grid-template-columns:repeat(4,minmax(0,1fr)); } .g5{ grid-template-columns:repeat(5,minmax(0,1fr)); } .g6{ grid-template-columns:repeat(6,minmax(0,1fr)); }
.gsm{ gap:0.5rem; }
@media (max-width:1200px){ .g6, .g5{ grid-template-columns:repeat(3,minmax(0,1fr)); } .g4{ grid-template-columns:repeat(2,minmax(0,1fr)); } .h-xl{ font-size:2.6rem; } }
@media (max-width:760px){ .g2, .g3, .g4{ grid-template-columns:minmax(0,1fr); } .g5, .g6{ grid-template-columns:repeat(2,minmax(0,1fr)); } .h-xl{ font-size:2.25rem; } .h-lg{ font-size:1.75rem; }
  [data-testid="stMainBlockContainer"], .block-container{ padding:0 1rem 3rem !important; }
  [data-testid="stLayoutWrapper"]:has(> .st-key-topbar){ position:static; }  /* stacked top bar would eat the screen if pinned */
  .st-key-topbar{ margin:0 0 0.5rem; padding:0.5rem 0; width:100% !important; background:transparent; box-shadow:none; backdrop-filter:none; }
  .pill{ white-space:normal; max-width:100%; } .card.lg{ padding:1rem; } }
.card{ background:var(--card); border-radius:0.75rem; padding:1rem; box-shadow:0 1px 3px rgba(0,0,0,0.35); position:relative; overflow:hidden; }
.card.lg{ padding:1.5rem; } .card.el{ background:var(--elev); }
.tile{ background:rgba(22,27,38,0.8); border-radius:0.5rem; padding:0.5rem 0.75rem; }
.hov{ transition:background .2s; } .hov:hover{ background:var(--elev); }
.pill{ display:inline-flex; align-items:center; gap:6px; padding:3px 10px; border-radius:9999px; font-family:'Geist';
  font-size:0.6875rem; line-height:1.2; letter-spacing:0.12em; font-weight:600; text-transform:uppercase; white-space:nowrap; }
.dot{ width:6px; height:6px; border-radius:9999px; display:inline-block; flex-shrink:0; }
.ping{ animation:ping 1.4s cubic-bezier(0,0,0.2,1) infinite; } @keyframes ping{ 75%,100%{ transform:scale(2.2); opacity:0; } }
.pulse{ animation:pulse 2s cubic-bezier(0.4,0,0.6,1) infinite; } @keyframes pulse{ 50%{ opacity:0.45; } }
.bar{ height:6px; background:var(--high); border-radius:9999px; overflow:hidden; display:flex; width:100%; } .bar > div{ height:100%; }
.ibox{ width:2rem; height:2rem; border-radius:0.375rem; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.glow{ position:absolute; border-radius:9999px; filter:blur(60px); pointer-events:none; }
.z{ position:relative; z-index:1; }
.sec-head{ display:flex; align-items:flex-end; justify-content:space-between; gap:1rem; margin:1.5rem 0 0.25rem; flex-wrap:wrap; }
.footer{ margin-top:2.5rem; padding-top:1rem; border-top:1px solid var(--border); display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap; }

/* ---------- Telemetry tables ---------- */
.tbl-wrap{ overflow-x:auto; border-radius:0.75rem; background:var(--card); }
.tbl{ width:100%; border-collapse:collapse; font-family:'Geist'; font-size:0.8125rem; }
.tbl th{ font-size:0.6875rem; letter-spacing:0.12em; text-transform:uppercase; font-weight:600; color:var(--muted);
  text-align:left; padding:0.8rem 0.75rem; background:var(--lowest); border:none; white-space:nowrap; }
.tbl td{ padding:0.7rem 0.75rem; border:none; border-top:1px solid rgba(255,255,255,0.04); color:var(--text); vertical-align:middle; }
.tbl tbody tr:nth-child(odd) td{ background:var(--card); } .tbl tbody tr:nth-child(even) td{ background:var(--elev); }
.tbl tbody tr:hover td{ background:var(--overlay); } .tbl tbody tr:hover td:first-child{ box-shadow:inset 2px 0 0 var(--red); }
.tbl .n{ text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; } .tbl th.n{ text-align:right; }
.tbl tr.warnrow td{ background:rgba(239,68,68,0.07) !important; }
.chip{ display:inline-flex; align-items:center; justify-content:center; min-width:2.6rem; padding:3px 8px; border-radius:0.375rem; white-space:nowrap;
  font-family:'Geist'; font-weight:700; font-variant-numeric:tabular-nums; font-size:0.8125rem; }

/* ---------- HTML chart primitives ---------- */
.chart{ position:relative; height:16rem; display:flex; align-items:flex-end; gap:0.5rem; padding:1.5rem 2.6rem 0 0.25rem; }
.chart .gridl{ position:absolute; left:0; right:0; top:1.5rem; bottom:1.35rem; display:flex; flex-direction:column; justify-content:space-between; pointer-events:none; }
.chart .gridl div{ border-bottom:1px solid rgba(255,255,255,0.06); height:0; text-align:right; font-size:10px; color:var(--muted); opacity:0.6; line-height:0; }
.chart .grp{ flex:1; display:flex; flex-direction:column; align-items:center; height:100%; z-index:1; border-radius:0.375rem 0.375rem 0 0; }
.chart .bars{ position:relative; flex:1; width:100%; display:flex; align-items:flex-end; justify-content:center; gap:3px; }
.chart .b{ width:min(1.1rem,32%); border-radius:2px 2px 0 0; transition:filter .2s; } .chart .grp:hover .b{ filter:brightness(1.25); }
.chart .x{ font-family:'Geist'; font-size:10px; color:var(--muted); height:1.35rem; display:flex; align-items:center; letter-spacing:0.06em; }
.chart .gdot{ position:absolute; width:9px; height:9px; border-radius:9999px; background:var(--warn); box-shadow:0 0 8px rgba(245,158,11,0.7); transform:translate(-50%,50%); left:50%; }
/* ---------- Hover cards for the HTML charts (styled like the Plotly hoverlabel) ---------- */
.has-tt{ position:relative; cursor:default; }
.tt{ position:absolute; z-index:60; bottom:calc(100% + 6px); left:50%; transform:translateX(-50%); min-width:11rem; max-width:17rem;
  background:var(--elev); border:1px solid rgba(255,255,255,0.14); border-radius:0.5rem; padding:0.5rem 0.65rem;
  box-shadow:0 10px 24px rgba(0,0,0,0.55); font-family:'Geist'; font-size:12px; line-height:1.45; color:#fff; text-align:left;
  white-space:normal; letter-spacing:0; text-transform:none; font-weight:400; opacity:0; visibility:hidden; pointer-events:none;
  transition:opacity .12s ease; }
.tt.l{ left:0; transform:none; } .tt.r{ left:auto; right:0; transform:none; }
.tt.top{ top:0.25rem; bottom:auto; }  /* inside tall chart columns so the card never clips */
.has-tt:hover > .tt{ opacity:1; visibility:visible; }
.has-tt:hover, .donut:hover{ z-index:40 !important; }  /* lift the hovered column above sibling bars */
.vbar .c{ position:relative; z-index:1; }
.tt-h{ font-weight:700; font-size:12px; margin-bottom:4px; color:#fff; }
.tt-r{ display:flex; align-items:center; gap:6px; } .tt-r b{ margin-left:auto; padding-left:12px; font-variant-numeric:tabular-nums; }
.tt-sw{ width:9px; height:9px; border-radius:2px; flex-shrink:0; }
.tt-n{ margin-top:5px; padding-top:5px; border-top:1px solid rgba(255,255,255,0.08); color:var(--muted); font-size:11px; }
.chart .grp:hover, .vbar .c:hover{ background:rgba(255,255,255,0.035); }
.donut circle.seg{ transition:stroke-width .12s; cursor:default; } .donut circle.seg:hover{ stroke-width:4.6; }
.donut:has(.seg-w:hover) .tt-w, .donut:has(.seg-d:hover) .tt-d, .donut:has(.seg-l:hover) .tt-l{ opacity:1; visibility:visible; }
.vbar{ height:12rem; display:flex; align-items:flex-end; gap:0.6rem; padding-top:1.5rem; border-bottom:1px solid rgba(255,255,255,0.1); }
.vbar .c{ flex:1; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:100%; gap:4px; }
.vbar .v{ font-family:'Geist'; font-weight:700; font-size:0.75rem; }
.vbar .r{ width:100%; border-radius:3px 3px 0 0; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. DATASETS (GROUNDED IN OPTA & NOTEBOOK SOURCES)
# ------------------------------------------------------------------------------

@st.cache_data
def load_match_data():
    matches = [
        {"Match_ID": 1, "Date": "2026-08-22", "Opponent": "Hull City", "Competition": "Premier League", "Venue": "Away",
         "Opponent_Category": "Mid-table / Promoted", "GF": 0, "GA": 2, "Result": "Loss", "Points": 0,
         "xG": 1.83, "xGA": 1.01, "Possession": 72, "Shots": 21, "Shots_On_Target": 5, "Opp_Shots": 8, "Opp_Shots_On_Target": 4,
         "Corners": 6, "Box_Touches": 41, "Pass_Accuracy": 88, "1st_Half_GF": 0, "1st_Half_GA": 2, "2nd_Half_GF": 0, "2nd_Half_GA": 0,
         "Yellow_Cards": 1, "Red_Cards": 0,
         "Key_Context": "Conceded 2 set-piece goals (17', 38') despite controlling 72% possession and 21 shots."},
        {"Match_ID": 2, "Date": "2026-08-30", "Opponent": "Ipswich Town", "Competition": "Premier League", "Venue": "Home",
         "Opponent_Category": "Mid-table / Promoted", "GF": 5, "GA": 2, "Result": "Win", "Points": 3,
         "xG": 4.77, "xGA": 2.06, "Possession": 60, "Shots": 33, "Shots_On_Target": 12, "Opp_Shots": 8, "Opp_Shots_On_Target": 3,
         "Corners": 5, "Box_Touches": 44, "Pass_Accuracy": 89, "1st_Half_GF": 1, "1st_Half_GA": 1, "2nd_Half_GF": 4, "2nd_Half_GA": 1,
         "Yellow_Cards": 1, "Red_Cards": 0,
         "Key_Context": "Bruno Fernandes hat-trick (40', 61'p, 68'); high xG offensive explosion but conceded late goal (91')."},
        {"Match_ID": 3, "Date": "2026-09-06", "Opponent": "Everton", "Competition": "Premier League", "Venue": "Away",
         "Opponent_Category": "Mid-table / Promoted", "GF": 2, "GA": 2, "Result": "Draw", "Points": 1,
         "xG": 0.69, "xGA": 1.01, "Possession": 55, "Shots": 14, "Shots_On_Target": 3, "Opp_Shots": 18, "Opp_Shots_On_Target": 6,
         "Corners": 3, "Box_Touches": 26, "Pass_Accuracy": 87, "1st_Half_GF": 0, "1st_Half_GA": 0, "2nd_Half_GF": 2, "2nd_Half_GA": 2,
         "Yellow_Cards": 3, "Red_Cards": 0,
         "Key_Context": "Surrendered 2-1 lead in 96th minute; outshot 14-18 by Everton; rest defense collapsed late."},
        {"Match_ID": 4, "Date": "2026-09-13", "Opponent": "Manchester City", "Competition": "Premier League", "Venue": "Home",
         "Opponent_Category": "Elite / Top-6", "GF": 0, "GA": 1, "Result": "Loss", "Points": 0,
         "xG": 1.04, "xGA": 0.80, "Possession": 51, "Shots": 12, "Shots_On_Target": 3, "Opp_Shots": 7, "Opp_Shots_On_Target": 2,
         "Corners": 5, "Box_Touches": 22, "Pass_Accuracy": 86, "1st_Half_GF": 0, "1st_Half_GA": 0, "2nd_Half_GF": 0, "2nd_Half_GA": 1,
         "Yellow_Cards": 1, "Red_Cards": 0,
         "Key_Context": "Failed to score against 10-man City (Foden red card 23'); Haaland winner 60'; Mainoo & Rashford hit posts."},
        {"Match_ID": 5, "Date": "2026-09-10", "Opponent": "Sabah FK", "Competition": "UEFA Champions League", "Venue": "Home",
         "Opponent_Category": "European Debutant", "GF": 4, "GA": 0, "Result": "Win", "Points": 3,
         "xG": 3.54, "xGA": 0.84, "Possession": 58, "Shots": 21, "Shots_On_Target": 10, "Opp_Shots": 11, "Opp_Shots_On_Target": 0,
         "Corners": 7, "Box_Touches": 42, "Pass_Accuracy": 92, "1st_Half_GF": 3, "1st_Half_GA": 0, "2nd_Half_GF": 1, "2nd_Half_GA": 0,
         "Yellow_Cards": 1, "Red_Cards": 0,
         "Key_Context": "Dominant Champions League win; dual forward setup (Cunha & Šeško both scored)."},
        {"Match_ID": 6, "Date": "2026-09-16", "Opponent": "Brighton & Hove Albion", "Competition": "EFL Cup", "Venue": "Home",
         "Opponent_Category": "Mid-table / Promoted", "GF": 2, "GA": 3, "Result": "Loss", "Points": 0,
         "xG": 1.04, "xGA": 2.15, "Possession": 50, "Shots": 12, "Shots_On_Target": 4, "Opp_Shots": 18, "Opp_Shots_On_Target": 5,
         "Corners": 4, "Box_Touches": 17, "Pass_Accuracy": 83, "1st_Half_GF": 2, "1st_Half_GA": 1, "2nd_Half_GF": 0, "2nd_Half_GA": 2,
         "Yellow_Cards": 0, "Red_Cards": 0,
         "Key_Context": "Blew 2-0 early lead (Lacey 8', Mount 10'); conceded 3 unanswered goals; eliminated from EFL Cup."}
    ]
    df = pd.DataFrame(matches).sort_values("Date").reset_index(drop=True)
    df["Seq"] = range(1, len(df) + 1)  # chronological fixture number
    return df

@st.cache_data
def load_player_data():
    players = [
        {"Player": "Bruno Fernandes", "Pos": "AM/CM", "Apps": 6, "Starts": 5, "Mins": 485, "Goals": 4, "Assists": 1, "xG_Contrib": 4.1, "Yel": 0, "Red": 0, "Primary_Role": "Primary Creator & Captain", "Tactical_Impact": "Central catalyst; hat-trick vs Ipswich; 38.5% direct goal share"},
        {"Player": "Bryan Mbeumo", "Pos": "RW/FW", "Apps": 6, "Starts": 5, "Mins": 470, "Goals": 2, "Assists": 1, "xG_Contrib": 2.2, "Yel": 1, "Red": 0, "Primary_Role": "Inverted Right Winger", "Tactical_Impact": "Goal & assist vs Ipswich; 3 pre-season goals; wide isolations"},
        {"Player": "Benjamin Šeško", "Pos": "ST", "Apps": 6, "Starts": 2, "Mins": 265, "Goals": 2, "Assists": 0, "xG_Contrib": 1.9, "Yel": 0, "Red": 0, "Primary_Role": "Target Striker / Impact Sub", "Tactical_Impact": "Goals vs Everton & Sabah; classic box presence; target option"},
        {"Player": "Matheus Cunha", "Pos": "ST/AM", "Apps": 6, "Starts": 5, "Mins": 410, "Goals": 1, "Assists": 1, "xG_Contrib": 1.8, "Yel": 0, "Red": 0, "Primary_Role": "False 9 / Linking Forward", "Tactical_Impact": "Drops deep to combine with Bruno; creates central overloads"},
        {"Player": "Lisandro Martínez", "Pos": "CB", "Apps": 5, "Starts": 4, "Mins": 380, "Goals": 1, "Assists": 0, "xG_Contrib": 0.8, "Yel": 0, "Red": 0, "Primary_Role": "Left-sided Center Back", "Tactical_Impact": "Goal vs Sabah; line-breaking progressive passes from deep"},
        {"Player": "Shea Lacey", "Pos": "RW", "Apps": 3, "Starts": 1, "Mins": 110, "Goals": 1, "Assists": 0, "xG_Contrib": 0.6, "Yel": 0, "Red": 0, "Primary_Role": "Young Wide Forward", "Tactical_Impact": "Goal on full debut vs Brighton (8'); high 1v1 dribble frequency"},
        {"Player": "Mason Mount", "Pos": "AM/CM", "Apps": 3, "Starts": 1, "Mins": 125, "Goals": 1, "Assists": 0, "xG_Contrib": 0.5, "Yel": 0, "Red": 0, "Primary_Role": "Attacking Midfielder", "Tactical_Impact": "Goal vs Brighton (10'); returning from ankle injury"},
        {"Player": "Patrick Dorgu", "Pos": "LB/LWB", "Apps": 5, "Starts": 3, "Mins": 290, "Goals": 0, "Assists": 1, "xG_Contrib": 0.7, "Yel": 2, "Red": 0, "Primary_Role": "Attacking Full-Back", "Tactical_Impact": "Assist vs Sabah; high wing overlap leaves rest defense exposed"},
        {"Player": "Youri Tielemans", "Pos": "CM/DM", "Apps": 6, "Starts": 6, "Mins": 490, "Goals": 0, "Assists": 2, "xG_Contrib": 1.1, "Yel": 0, "Red": 0, "Primary_Role": "Deep-Lying Playmaker", "Tactical_Impact": "Central pivot anchor; 2 assists; vulnerable covering lateral counters"},
        {"Player": "Kobbie Mainoo", "Pos": "CM", "Apps": 5, "Starts": 4, "Mins": 360, "Goals": 0, "Assists": 1, "xG_Contrib": 0.9, "Yel": 0, "Red": 0, "Primary_Role": "Box-to-Box Midfielder", "Tactical_Impact": "Assist vs Everton; hit post vs City; press-resistant ball carrier"},
        {"Player": "Luke Shaw", "Pos": "LB", "Apps": 3, "Starts": 3, "Mins": 250, "Goals": 0, "Assists": 1, "xG_Contrib": 0.5, "Yel": 1, "Red": 0, "Primary_Role": "Left-Back / Inverted Passing", "Tactical_Impact": "Assist vs Everton; left flank ball progression before injury"},
        {"Player": "Senne Lammens", "Pos": "GK", "Apps": 5, "Starts": 5, "Mins": 450, "Goals": 0, "Assists": 0, "xG_Contrib": 0.0, "Yel": 0, "Red": 0, "Primary_Role": "Starting Goalkeeper", "Tactical_Impact": "Clean sheet vs Sabah; faced 13 shots on target; solid debut series"},
        {"Player": "Karl Darlow", "Pos": "GK", "Apps": 1, "Starts": 1, "Mins": 90, "Goals": 0, "Assists": 0, "xG_Contrib": 0.0, "Yel": 0, "Red": 0, "Primary_Role": "Cup Goalkeeper", "Tactical_Impact": "Conceded 3 goals vs Brighton on 5 shots on target in EFL Cup"},
        {"Player": "Harry Maguire", "Pos": "CB", "Apps": 4, "Starts": 4, "Mins": 360, "Goals": 0, "Assists": 0, "xG_Contrib": 0.3, "Yel": 2, "Red": 0, "Primary_Role": "Right Center Back", "Tactical_Impact": "Forced own goal vs Ipswich; dominant aerial duels"},
        {"Player": "Diogo Dalot", "Pos": "RB/LB", "Apps": 5, "Starts": 4, "Mins": 370, "Goals": 0, "Assists": 0, "xG_Contrib": 0.4, "Yel": 1, "Red": 0, "Primary_Role": "Inverted Full-Back", "Tactical_Impact": "Flank versatility; tucks inside in build-up to form 3-man rest line"},
        {"Player": "Noussair Mazraoui", "Pos": "RB/LB", "Apps": 5, "Starts": 2, "Mins": 210, "Goals": 0, "Assists": 0, "xG_Contrib": 0.2, "Yel": 0, "Red": 0, "Primary_Role": "Full-Back Rotation", "Tactical_Impact": "Defensive rotation on right flank"},
        {"Player": "Leny Yoro", "Pos": "CB", "Apps": 4, "Starts": 2, "Mins": 220, "Goals": 0, "Assists": 0, "xG_Contrib": 0.1, "Yel": 0, "Red": 0, "Primary_Role": "Center Back", "Tactical_Impact": "Recovery speed; started vs Sabah & Brighton"},
        {"Player": "Ayden Heaven", "Pos": "CB", "Apps": 2, "Starts": 2, "Mins": 180, "Goals": 0, "Assists": 0, "xG_Contrib": 0.1, "Yel": 0, "Red": 0, "Primary_Role": "Young Center Back", "Tactical_Impact": "Started vs Hull & Brighton; steep tactical learning curve"},
        {"Player": "Andrey Santos", "Pos": "DM/CM", "Apps": 5, "Starts": 2, "Mins": 220, "Goals": 0, "Assists": 0, "xG_Contrib": 0.3, "Yel": 0, "Red": 0, "Primary_Role": "Midfield Destroyer Rotation", "Tactical_Impact": "Physical pressing option in double pivot"},
        {"Player": "Marcus Rashford", "Pos": "LW", "Apps": 5, "Starts": 3, "Mins": 310, "Goals": 0, "Assists": 0, "xG_Contrib": 1.2, "Yel": 0, "Red": 0, "Primary_Role": "Left Winger", "Tactical_Impact": "Direct speed runner; hit post vs City; energetic left-flank presence"},
        {"Player": "Joshua Zirkzee", "Pos": "ST", "Apps": 2, "Starts": 0, "Mins": 50, "Goals": 0, "Assists": 0, "xG_Contrib": 0.2, "Yel": 0, "Red": 0, "Primary_Role": "Substitute Striker", "Tactical_Impact": "Pre-season goalscorer; late sub option"},
        {"Player": "Harry Amass", "Pos": "LB", "Apps": 2, "Starts": 0, "Mins": 35, "Goals": 0, "Assists": 0, "xG_Contrib": 0.1, "Yel": 0, "Red": 0, "Primary_Role": "Substitute Left Back", "Tactical_Impact": "Late attacking sub on left wing"}
    ]
    return pd.DataFrame(players)

df_matches = load_match_data()
df_players = load_player_data()

ABBR = {"Hull City": "HUL", "Ipswich Town": "IPS", "Everton": "EVE", "Manchester City": "MCI",
        "Sabah FK": "SAB", "Brighton & Hove Albion": "BHA"}
COMP_ABBR = {"Premier League": "PL", "UEFA Champions League": "UCL", "EFL Cup": "EFL"}
MAX_MINS = 6 * 90  # minutes available across the 6 fixtures

# Every goal conceded, keyed by Match_ID (minute None = first-half goal with no recorded minute)
CONCEDED = [(1, 17), (1, 38), (2, None), (2, 91), (3, 83), (3, 96), (4, 60), (6, 45), (6, 65), (6, 70)]
TIME_BUCKETS = ["0–45'", "46–60'", "61–75'", "76–90+'"]
# Fixtures where United led and failed to win: Match_ID -> (score path, consequence)
LEADS_LOST = {3: ("Everton (A)", "2-1 → 2-2", "2 PL pts dropped"), 6: ("Brighton (H)", "2-0 → 2-3", "EFL Cup exit")}
# Set-piece-phase goals conceded (Hull 17' corner, Hull 38' free-kick, Ipswich 91' scramble, Everton 96' cross)
SET_PIECE_GA = {1: 2, 2: 1, 3: 1}

# PL-only table context (independent of the filters)
_pl = df_matches[df_matches["Competition"] == "Premier League"]
PL_W, PL_D, PL_L = int((_pl.Result == "Win").sum()), int((_pl.Result == "Draw").sum()), int((_pl.Result == "Loss").sum())
PL_PTS = int(_pl.Points.sum())

# ------------------------------------------------------------------------------
# 3. HTML / DESIGN HELPERS
# ------------------------------------------------------------------------------
def H(markup):
    """Render Stitch HTML. Lines are flattened so Markdown never re-interprets indentation or blank lines."""
    st.markdown(" ".join(l.strip() for l in markup.strip().splitlines() if l.strip()), unsafe_allow_html=True)

def esc(x):
    return _html.escape(str(x))

def rgba(hx, a):
    h = hx.lstrip("#")
    return "rgba({},{},{},{})".format(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

def ico(name, size=18, color=None, fill=False):
    style = "font-size:{}px;".format(size)
    if color:
        style += "color:{};".format(color)
    if fill:
        style += "font-variation-settings:'FILL' 1;"
    return '<span class="msi" style="{}">{}</span>'.format(style, name)

def pill(text, color, dot=False, ping=False, bg=0.15, solid=False):
    d = ""
    if dot or ping:
        d = '<span class="dot{}" style="background:{};"></span>'.format(" ping" if ping else "", color)
    if solid:
        return '<span class="pill" style="background:{};color:#fff;box-shadow:0 0 12px {};">{}{}</span>'.format(color, rgba(color, 0.5), d, text)
    return '<span class="pill" style="background:{};color:{};">{}{}</span>'.format(rgba(color, bg), color, d, text)

def sdiv(a, b):
    return a / b if b else 0.0

def signed(v, fmt="{:+.2f}"):
    return fmt.format(v).replace("-", "−")

def res_letter(r):
    return {"Win": ("W", POS), "Draw": ("D", WARN), "Loss": ("L", DANGER)}[r]

def pos_group(p):
    first = p.split("/")[0]
    if first == "GK":
        return "GK"
    if first in ("CB", "LB", "RB", "LWB", "RWB"):
        return "DEF"
    if first in ("CM", "DM", "AM"):
        return "MID"
    return "FWD"

def pos_unit(p):
    first = p.split("/")[0]
    return {"GK": "Goalkeepers", "CB": "Defence", "LB": "Defence", "RB": "Defence", "AM": "Attacking Mid",
            "CM": "Midfield Engine", "DM": "Midfield Engine"}.get(first, "Forwards")

def _football_logo_svg():
    """'Theatre of Data' mark: a classic panelled football on the red tile, over faint pitch markings.
    Geometry is computed so the pentagon panels and seams line up exactly."""
    cx, cy, R = 32.0, 33.0, 18.5          # ball centre / radius
    ink = "#10141D"
    ang = [math.radians(-90 + 72 * k) for k in range(5)]
    pt = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
    fmt = lambda pts: " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    centre = fmt(pt(6.6, a) for a in ang)                                   # central black pentagon
    seams = "".join(f'<line x1="{pt(6.6, a)[0]:.2f}" y1="{pt(6.6, a)[1]:.2f}" x2="{pt(12.4, a)[0]:.2f}" y2="{pt(12.4, a)[1]:.2f}"/>'
                    for a in ang)                                          # seams to the outer panels
    def rim_panel(a, r=4.8, d=18.0):
        """Small pentagon centred near the rim, one vertex aimed at the ball centre; clipped by the ball outline."""
        px, py = pt(d, a)
        return fmt((px + r * math.cos(a + math.pi + math.radians(72 * j)), py + r * math.sin(a + math.pi + math.radians(72 * j)))
                   for j in range(5))
    outer = "".join(f'<polygon points="{rim_panel(a)}"/>' for a in ang)  # partial pentagons at the rim
    rim_seams = "".join(f'<line x1="{pt(12.4, a)[0]:.2f}" y1="{pt(12.4, a)[1]:.2f}" x2="{pt(12.4, b)[0]:.2f}" y2="{pt(12.4, b)[1]:.2f}"/>'
                        for a, b in zip(ang, ang[1:] + ang[:1]))           # ring joining the seam ends
    return (
        '<svg width="{s}" height="{s}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">'
        '<defs><clipPath id="tod-ball"><circle cx="%.1f" cy="%.1f" r="%.1f"/></clipPath></defs>'
        '<rect width="64" height="64" rx="15" fill="#DA020E"/>'
        # faint pitch markings: halfway line + centre circle
        '<g stroke="rgba(255,255,255,0.22)" stroke-width="1.6" fill="none"><line x1="0" y1="33" x2="64" y2="33"/>'
        '<circle cx="32" cy="33" r="25"/></g>'
        '<ellipse cx="32" cy="54.5" rx="12" ry="2.2" fill="rgba(0,0,0,0.25)"/>'   # soft shadow
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffffff"/>'
        '<g clip-path="url(#tod-ball)" fill="%s"><polygon points="%s"/>%s</g>'
        '<g clip-path="url(#tod-ball)" stroke="%s" stroke-width="1.5" stroke-linecap="round" fill="none">%s%s</g>'
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="1.2" opacity="0.35"/>'
        '</svg>'
    ) % (cx, cy, R, cx, cy, R, ink, centre, outer, ink, seams, rim_seams, cx, cy, R, ink)

LOGO_SVG = _football_logo_svg()

def logo(size=32):
    return LOGO_SVG.replace("{s}", str(size))

def section_head(kicker, title, right="", kicker_color=None):
    kc = kicker_color or MUTED
    H(f'''<div class="sec-head"><div class="col gx"><span class="lbl" style="color:{kc};">{kicker}</span>
    <div class="h-sm">{title}</div></div><span class="lbl" style="color:{SEC};">{right}</span></div>''')

def page_head(tags_html, title, subtitle, right_html="", banner=False, meta=""):
    """Editorial page header. banner=True renders the Stitch hero card with ambient red/cyan glows."""
    meta_html = f'<div class="row gx m mono body-sm">{ico("update", 16, SEC)}<span>{meta}</span></div>' if meta else ""
    inner = f'''<div class="row between wrap gs z"><div class="row wrap gx">{tags_html}</div>{meta_html}</div>
    <div class="row between start wrap gl z" style="margin-top:0.5rem;">
      <div class="col gx" style="max-width:62rem;flex:1;min-width:18rem;">
        <div class="h-xl">{title}</div>
        <div class="body-lg" style="margin-top:0.35rem;max-width:56rem;">{subtitle}</div>
      </div>{right_html}</div>'''
    if banner:
        return inner  # caller wraps it with banner_open() so extra rows can sit inside the hero card
    H(f'<div style="padding:0.5rem 0 0.25rem;">{inner}</div>')
    return None

def banner_open(inner, extra=""):
    H(f'''<div class="card lg">
    <div class="glow" style="right:-6rem;top:-6rem;width:24rem;height:24rem;background:rgba(255,45,59,0.10);"></div>
    <div class="glow" style="left:33%;bottom:-5rem;width:20rem;height:10rem;background:rgba(123,208,255,0.05);"></div>
    {inner}{extra}</div>''')

def kpi(label, icon, icon_color, value, sub, sub_color=MUTED, foot_l="", foot_l_color=MUTED, foot_r="", unit="", edge=None):
    unit_html = f' <span class="h-sm" style="font-weight:400;color:{MUTED};">{unit}</span>' if unit else ""
    edge_css = f"box-shadow:inset 3px 0 0 {edge};" if edge else ""
    return f'''<div class="card hov col between" style="padding:0.75rem 1rem;{edge_css}">
    <div class="row between gx"><span class="lbl">{label}</span>{ico(icon, 16, icon_color)}</div>
    <div style="margin:0.4rem 0;"><div class="stat">{value}{unit_html}</div>
    <div class="mono body-sm" style="color:{sub_color};margin-top:2px;">{sub}</div></div>
    <div class="row between gx" style="padding-top:0.25rem;"><span class="lbl-sm" style="color:{foot_l_color};">{foot_l}</span>{foot_r}</div></div>'''

def footer():
    H(f'''<div class="footer"><div class="row gx m body-sm">{ico("verified", 16, POS)}
    <span>Theatre of Data — Manchester United 2026/27 tactical analytics portfolio · Built with Python, Streamlit &amp; Plotly</span></div>
    <span class="lbl">Dataset: MD 1–6 · Opta / FotMob · Illustrative tactical models</span></div>''')

# ------------------------------------------------------------------------------
# 4. METRICS
# ------------------------------------------------------------------------------
def team_stats(f):
    n = len(f)
    s = dict(
        n=n, W=int((f.Result == "Win").sum()), D=int((f.Result == "Draw").sum()), L=int((f.Result == "Loss").sum()),
        GF=int(f.GF.sum()), GA=int(f.GA.sum()), xG=float(f.xG.sum()), xGA=float(f.xGA.sum()),
        poss=float(f.Possession.mean()) if n else 0.0, shots=int(f.Shots.sum()), sot=int(f.Shots_On_Target.sum()),
        oshots=int(f.Opp_Shots.sum()), osot=int(f.Opp_Shots_On_Target.sum()), box=int(f.Box_Touches.sum()),
        corners=int(f.Corners.sum()), h1gf=int(f["1st_Half_GF"].sum()), h1ga=int(f["1st_Half_GA"].sum()),
        h2gf=int(f["2nd_Half_GF"].sum()), h2ga=int(f["2nd_Half_GA"].sum()), pts=int(f.Points.sum()),
    )
    s["GD"] = s["GF"] - s["GA"]
    s["win_pct"] = sdiv(s["W"], n) * 100
    ids = set(f.Match_ID)
    buckets = {b: 0 for b in TIME_BUCKETS}
    goals = {b: [] for b in TIME_BUCKETS}  # hover detail: which goals fall in each phase
    for mid, minute in CONCEDED:
        if mid not in ids:
            continue
        if minute is None or minute <= 45:
            b = "0–45'"
        elif minute <= 60:
            b = "46–60'"
        elif minute <= 75:
            b = "61–75'"
        else:
            b = "76–90+'"
        buckets[b] += 1
        goals[b].append((MATCH_TAG[mid], fmt_minute(minute)))
    s["buckets"] = buckets
    s["bucket_goals"] = goals
    s["late_ga"] = buckets["61–75'"] + buckets["76–90+'"]
    s["sp_ga"] = sum(v for k, v in SET_PIECE_GA.items() if k in ids)
    return s

MATCH_TAG = {r.Match_ID: f"{r.Opponent} ({r.Venue[0]})" for r in df_matches.itertuples()}

def fmt_minute(m):
    if m is None:
        return "1st half (minute n/a)"
    return f"90+{m - 90}'" if m > 90 else f"{m}'"

def tt(title, rows=(), note="", align="", top=False, extra_cls=""):
    """Hover card. rows: (swatch_color or None, label, value). align: '' centred, 'l' or 'r' edge-anchored."""
    body = "".join(
        f'<div class="tt-r">{f"<span class=tt-sw style=background:{c}></span>" if c else ""}<span>{lab}</span><b>{val}</b></div>'
        for c, lab, val in rows)
    cls = " ".join(x for x in ("tt", align, "top" if top else "", extra_cls) if x)
    note_html = f'<div class="tt-n">{note}</div>' if note else ""
    return f'<div class="{cls}"><div class="tt-h">{title}</div>{body}{note_html}</div>'

def plural(n, word, suffix="s"):
    return f"{n} {word}{'' if n == 1 else suffix}"

def match_conclusion(s, outcome, lost_leads):
    """Data-driven conclusion for the Match Results page. Every clause and colour is chosen from the numbers
    in view, so it reads correctly for All / Win / Draw / Loss and any top-bar scope."""
    diff = s["xG"] - s["xGA"]
    h1n, h2n = s["h1gf"] - s["h1ga"], s["h2gf"] - s["h2ga"]
    fx = "In this fixture" if s["n"] == 1 else f"Across these {s['n']} fixtures"
    gd = lambda v: "0" if v == 0 else signed(v, "{:+d}")
    # chance creation
    if abs(diff) < 0.3:
        create = f"United averaged <b>{s['poss']:.1f}% possession</b> and created <b>{s['xG']:.2f} xG</b>, roughly level with opponents ({s['xGA']:.2f})."
    else:
        create = (f"United averaged <b>{s['poss']:.1f}% possession</b> and created <b>{s['xG']:.2f} xG</b>, "
                  f"<b style='color:{POS if diff > 0 else DANGER};'>{abs(diff):.2f} {'more' if diff > 0 else 'less'}</b> than opponents.")
    # defending vs expectation
    if s["GA"] > s["xGA"] + 0.05:
        defend = f"They conceded <b style='color:{DANGER};'>{s['GA']} from {s['xGA']:.2f} xGA</b>, so opponents finished above expectation."
    elif s["GA"] < s["xGA"] - 0.05:
        defend = f"They conceded only <b style='color:{POS};'>{s['GA']} from {s['xGA']:.2f} xGA</b>, fewer than the chances allowed."
    else:
        defend = f"They conceded {s['GA']} from {s['xGA']:.2f} xGA, in line with the chances allowed."
    # halves
    trend = ("a <b style='color:%s;'>second-half drop-off</b>" % DANGER if h2n < h1n else
             "<b style='color:%s;'>stronger after the break</b>" % POS if h2n > h1n else "level across both halves")
    halves = (f"Goal difference was {gd(h1n)} in the first half and {gd(h2n)} in the second: {trend}." if s["n"] == 1 else
              f"Goal difference was {gd(h1n)} in first halves and {gd(h2n)} in second halves: {trend}.")
    # late goals
    late = (f"No goals were conceded after the 60th minute." if s["late_ga"] == 0 else
            f"{plural(s['late_ga'], 'goal')} came after the 60th minute ({sdiv(s['late_ga'], s['GA']) * 100:.0f}% of those conceded).")
    # headline + takeaway by outcome
    if outcome == "Win":
        kicker, title = "Outcome Breakdown · Wins", "What the Wins Have in Common"
        head = "Chance Dominance, Converted"
        take = (f"<b>Takeaway:</b> when United turn control into chances ({s['GF']} goals from {s['xG']:.2f} xG), results follow"
                + (f", although even these wins leaked {plural(s['late_ga'], 'late goal')}." if s["late_ga"] else "."))
    elif outcome == "Draw":
        kicker, title = "Outcome Breakdown · Draws", "Where the Points Slipped"
        head = ("Lead Surrendered Late" if s["n"] == 1 else "Leads Surrendered Late") if lost_leads else "Level Games, Few Clear Chances"
        take = ("<b>Takeaway:</b> " + ("a winning position was thrown away late — closing out games is the fix." if lost_leads
                                       else "neither side created enough to win."))
    elif outcome == "Loss":
        kicker, title = "Outcome Breakdown · Defeats", "What Went Wrong in the Defeats"
        head = ("Out-Created, Still Beaten" if diff >= 0.3 else "Beaten on Chances Too" if diff <= -0.3 else "Even on Chances, Beaten on the Scoreboard")
        take = None
    else:
        kicker, title = "Tactical Lab Executive Conclusion", "The Dual-Reality Dilemma"
        fragile = (s["GA"] > s["xGA"] or h2n < h1n) and s["W"] < s["n"]
        head = "Territorial Control Masking Game-State Fragility" if fragile else "Control Translating Into Results"
        take = None
    if take is None:  # priority for All / Loss views: the largest weakness in the numbers
        if s["GA"] and s["late_ga"] / s["GA"] >= 0.4:
            take = f"<b>Priority:</b> the post-60' concessions ({s['late_ga']} of {s['GA']} goals conceded)."
        elif s["GA"] > s["xGA"] + 0.05:
            take = "<b>Priority:</b> opponents are finishing above expectation — reduce the quality of chances allowed."
        elif s["GF"] < s["xG"] - 0.3:
            take = f"<b>Priority:</b> finishing — {s['GF']} goals from {s['xG']:.2f} xG."
        else:
            take = "<b>Priority:</b> no single weakness stands out in this view."
    body = " ".join([create, defend, halves, late])
    return kicker, title, head, body, take, fx

def venue_stats(f, venue):
    v = f[f.Venue == venue]
    n = len(v)
    return dict(n=n, W=int((v.Result == "Win").sum()), D=int((v.Result == "Draw").sum()), L=int((v.Result == "Loss").sum()),
                ppm=sdiv(v.Points.sum(), n), gd=int(v.GF.sum() - v.GA.sum()), gf=sdiv(v.GF.sum(), n), ga=sdiv(v.GA.sum(), n),
                xg=sdiv(v.xG.sum(), n), xga=sdiv(v.xGA.sum(), n), poss=sdiv(v.Possession.sum(), n), shots=sdiv(v.Shots.sum(), n))

# ------------------------------------------------------------------------------
# 5. STITCH HTML CHARTS
# ------------------------------------------------------------------------------
def donut_svg(w, d, l, size=112):
    n = max(w + d + l, 1)
    C = 2 * math.pi * 14
    parts, tips, off = [], [], 0.0
    for key, lab, v, c in (("l", "Losses", l, DANGER), ("d", "Draws", d, WARN), ("w", "Wins", w, POS)):
        seg = v / n * C
        if v:
            parts.append(f'<circle class="seg seg-{key}" cx="18" cy="18" r="14" fill="none" stroke="{c}" stroke-width="3.5" '
                         f'stroke-dasharray="{seg:.2f} {C:.2f}" stroke-dashoffset="{-off:.2f}"/>')
            # invisible, wider twin of the segment so the thin ring is easy to hover
            parts.append(f'<circle class="seg-{key}" cx="18" cy="18" r="14" fill="none" stroke="transparent" stroke-width="9" '
                         f'pointer-events="stroke" stroke-dasharray="{seg:.2f} {C:.2f}" stroke-dashoffset="{-off:.2f}"/>')
            tips.append(tt(lab, [(c, "Fixtures", v), (None, "Share", f"{v / n * 100:.1f}%"), (None, "Points", v * 3 if key == "w" else v if key == "d" else 0)],
                           extra_cls=f"tt-{key}").replace('class="tt ', 'style="left:calc(100% + 8px);top:50%;bottom:auto;transform:translateY(-50%);" class="tt '))
        off += seg
    return f'''<div class="donut" style="position:relative;width:{size}px;height:{size}px;flex-shrink:0;">
    <svg width="{size}" height="{size}" viewBox="0 0 36 36" style="transform:rotate(-90deg);">
    <circle cx="18" cy="18" r="14" fill="none" stroke="#1D2026" stroke-width="3.5"/>{''.join(parts)}</svg>
    <div class="col" style="position:absolute;inset:0;align-items:center;justify-content:center;pointer-events:none;">
    <span class="h-sm" style="font-weight:800;">{w + d + l}</span><span class="lbl" style="font-size:10px;">Games</span></div>{''.join(tips)}</div>'''

def xg_disparity_chart(f):
    rows = f.sort_values("Date")
    top = max(float(rows[["xG", "xGA"]].max().max()), float(rows[["GF"]].max().max()), 1.0)
    scale = math.ceil(top)
    worst = (rows.xGA - rows.xG).idxmax() if len(rows) else None
    grid = "".join(f'<div>{v:.0f}.0 xG&nbsp;</div>' for v in range(scale, -1, -1))
    groups = []
    for k, (i, r) in enumerate(rows.iterrows()):
        hot = i == worst and (r.xGA - r.xG) > 0
        diff = r.xG - r.xGA
        card = tt(f"{esc(r.Opponent)} ({r.Venue[0]}) · {COMP_ABBR[r.Competition]}",
                  [(RED_CORE, "MUFC xG", f"{r.xG:.2f}"), (rgba(SEC, 0.7), "Opponent xG", f"{r.xGA:.2f}"),
                   (WARN, "Score", f"{r.GF}–{r.GA} ({r.Result})"), (None, "xG difference", signed(diff))],
                  note=f"{pd.to_datetime(r.Date).strftime('%d %b')} · {esc(r.Key_Context)}",
                  align="l" if k < len(rows) / 2 else "r", top=True)
        lab_color = RED if hot else MUTED
        groups.append(f'''<div class="grp has-tt" style="{'background:rgba(255,45,59,0.06);' if hot else ''}">{card}
        <div class="bars">
          <div class="b" style="height:{r.xG / scale * 100:.1f}%;background:{RED_CORE};"></div>
          <div class="b" style="height:{r.xGA / scale * 100:.1f}%;background:{rgba(SEC, 0.5)};"></div>
          <span class="gdot" style="bottom:{r.GF / scale * 100:.1f}%;"></span>
        </div>
        <span class="x" style="color:{lab_color};{'font-weight:700;' if hot else ''}">{ABBR.get(r.Opponent, r.Opponent[:3].upper())}{'*' if hot else ''}</span></div>''')
    return f'<div class="chart"><div class="gridl">{grid}</div>{"".join(groups)}</div>'

def bucket_bars(buckets, height="12rem", goals=None):
    vals = list(buckets.values())
    mx = max(max(vals), 1)
    total = max(sum(vals), 1)
    cols = [(OVERLAY, MUTED), (rgba(WARN, 0.85), WARN), (rgba(DANGER, 0.85), DANGER), (RED_CORE, RED)]
    out = []
    for k, ((lab, v), (fill, txt)) in enumerate(zip(buckets.items(), cols)):
        rows = [(txt, "Goals conceded", v), (None, "Share of all GA", f"{v / total * 100:.0f}%")]
        rows += [(None, esc(opp), minute) for opp, minute in (goals or {}).get(lab, [])]
        card = tt(f"Minutes {lab}", rows, align="l" if k < 2 else "r", top=True)
        out.append(f'''<div class="c has-tt">{card}<span class="v" style="color:{txt};">{v}</span>
        <div class="r" style="height:{max(v / mx * 100, 3):.0f}%;background:{fill};box-shadow:inset 0 2px 0 {txt};"></div></div>''')
    labels = "".join(f'<span class="lbl" style="flex:1;text-align:center;font-size:10px;">{b}</span>' for b in buckets)
    return f'<div class="vbar" style="height:{height};">{"".join(out)}</div><div class="row" style="gap:0.6rem;margin-top:0.4rem;">{labels}</div>'

def meter(segments, marker_pct=None, ref_pct=None, ref_color=MUTED):
    """Segmented gauge; marker = solid white needle, ref = thin dashed reference line."""
    segs = "".join(f'<div style="width:{w}%;background:{c};"></div>' for w, c in segments)
    mk = ""
    if ref_pct is not None:
        mk += (f'<div style="position:absolute;left:{ref_pct:.1f}%;top:-6px;bottom:-6px;width:0;'
               f'border-left:2px dashed {ref_color};opacity:0.9;"></div>')
    if marker_pct is not None:
        mk += (f'<div style="position:absolute;left:calc({marker_pct:.1f}% - 1.5px);top:-4px;bottom:-4px;width:3px;background:#fff;'
               f'border-radius:2px;box-shadow:0 0 8px rgba(255,255,255,0.8);transition:left .3s;"></div>')
    return f'<div style="position:relative;"><div class="bar" style="height:10px;">{segs}</div>{mk}</div>'

# ------------------------------------------------------------------------------
# 6. PLOTLY THEMING (Tactical Lab)
# ------------------------------------------------------------------------------
PLOTLY_CONFIG = {"displayModeBar": False}

def style_chart(fig, height=340):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=height,
        font=dict(color=TEXT, size=12, family="Geist, sans-serif"),
        hoverlabel=dict(bgcolor=ELEV, bordercolor="rgba(255,255,255,0.14)", font=dict(color="#ffffff", size=12, family="Geist, sans-serif")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(color=MUTED, size=11), bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=30, r=10, b=30, l=10), bargap=0.35,
    )
    fig.update_xaxes(tickfont=dict(size=11, color=MUTED), gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)", zeroline=False)
    fig.update_yaxes(tickfont=dict(size=11, color=MUTED), gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    return fig

# ------------------------------------------------------------------------------
# 7. INTERACTIVE TACTICS-BOARD ENGINE (Stitch pitch stage)
# ------------------------------------------------------------------------------
PITCH_L, PITCH_W = 105, 68
PLINE = "rgba(255,255,255,0.18)"

def _pline(fig, **kw):
    fig.add_shape(line=dict(color=PLINE, width=2), layer="below", **kw)

def add_pitch(fig):
    """Broadcast pitch: striped dark turf, faint regulation lines, half-space & zone-14 guides."""
    fig.add_shape(type="rect", x0=-4, y0=-4, x1=109, y1=72, fillcolor="#0C131D", line=dict(width=0), layer="below")
    for x in range(1, 109, 10):
        fig.add_shape(type="rect", x0=x, y0=-4, x1=min(x + 5, 109), y1=72, fillcolor="#0E1622", line=dict(width=0), layer="below")
    for y in (20.4, 47.6):
        fig.add_shape(type="line", x0=0, y0=y, x1=PITCH_L, y1=y, line=dict(color="rgba(255,255,255,0.05)", width=1.5, dash="dash"), layer="below")
    for x in (35, 70):
        fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=PITCH_W, line=dict(color="rgba(255,255,255,0.05)", width=1.5, dash="dash"), layer="below")
    _pline(fig, type="rect", x0=0, y0=0, x1=PITCH_L, y1=PITCH_W)
    _pline(fig, type="line", x0=PITCH_L / 2, y0=0, x1=PITCH_L / 2, y1=PITCH_W)
    _pline(fig, type="circle", x0=PITCH_L / 2 - 9.15, y0=PITCH_W / 2 - 9.15, x1=PITCH_L / 2 + 9.15, y1=PITCH_W / 2 + 9.15)
    _pline(fig, type="rect", x0=0, y0=13.84, x1=16.5, y1=54.16)
    _pline(fig, type="rect", x0=0, y0=24.84, x1=5.5, y1=43.16)
    _pline(fig, type="rect", x0=88.5, y0=13.84, x1=105, y1=54.16)
    _pline(fig, type="rect", x0=99.5, y0=24.84, x1=105, y1=43.16)
    # penalty arcs (points outside the 18-yard box) + spots
    for cx, sgn in ((11, 1), (94, -1)):
        pts = [math.radians(a) for a in range(-53, 54, 3)]
        fig.add_trace(go.Scatter(x=[cx + sgn * 9.15 * math.cos(t) for t in pts], y=[34 + 9.15 * math.sin(t) for t in pts],
                                 mode="lines", line=dict(color=PLINE, width=2), hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=[11, 94, 52.5], y=[34, 34, 34], mode="markers", marker=dict(size=5, color="rgba(255,255,255,0.4)"),
                             hoverinfo="skip", showlegend=False))

def initials(name):
    parts = name.replace("-", " ").split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else name[:2].upper()

def add_players(fig, coords, selected=None):
    """United nodes: dark ring + red core (Stitch), initials inside, surname below. Clicking returns the full name."""
    xs = [c[0] for c in coords]; ys = [c[1] for c in coords]
    short = [c[2] for c in coords]; full = [c[3] for c in coords]
    if selected in full:
        i = full.index(selected)
        fig.add_trace(go.Scatter(x=[xs[i]], y=[ys[i]], mode="markers", hoverinfo="skip", showlegend=False,
                                 marker=dict(size=58, color="rgba(255,45,59,0.16)", line=dict(width=0))))
    ring_w = [3.5 if f == selected else 2 for f in full]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers", hoverinfo="skip", showlegend=False,
                             marker=dict(size=[36 if f == selected else 30 for f in full], color=ELEV,
                                         line=dict(width=ring_w, color=RED))))
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers+text", name="Manchester United",
        marker=dict(size=[28 if f == selected else 22 for f in full], color=[RED if f == selected else RED_CORE for f in full], line=dict(width=0)),
        text=[initials(f) for f in full], textposition="middle center",
        textfont=dict(color="#ffffff", size=9, family="Geist, sans-serif"),
        customdata=[[f] for f in full], hovertemplate="<b>%{customdata[0]}</b><br>Click to inspect<extra></extra>", showlegend=False,
    ))
    fig.add_trace(go.Scatter(x=xs, y=[y - 3.6 for y in ys], mode="text", text=short, hoverinfo="skip", showlegend=False,
                             textfont=dict(color=TEXT, size=10, family="Geist, sans-serif")))

def add_opponents(fig, coords):
    xs = [c[0] for c in coords]; ys = [c[1] for c in coords]; lbl = [c[2] for c in coords]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers", hovertext=lbl, hoverinfo="text", showlegend=False,
                             marker=dict(size=20, color="#FFFFFF", line=dict(width=2.5, color=PASS))))
    fig.add_trace(go.Scatter(x=xs, y=[y - 3.4 for y in ys], mode="text", text=[l.split(" (")[0] for l in lbl], hoverinfo="skip",
                             showlegend=False, textfont=dict(color="#C4E7FF", size=9, family="Geist, sans-serif")))

def finalize_pitch(fig, hud_left, hud_right, height=560, view=None):
    """view: optional {"x": [x0, x1], "y": [y0, y1]} camera to zoom into one area of the pitch."""
    view = view or {"x": [-4, 109], "y": [-4, 72]}
    fig.update_layout(
        # No fixedrange / select dragmode here: either one stops Streamlit's click-to-select on points.
        xaxis=dict(range=view["x"], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=view["y"], showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0A1016", margin=dict(l=0, r=0, t=0, b=0), height=height,
        clickmode="event+select", showlegend=False,
        hoverlabel=dict(bgcolor=ELEV, bordercolor="rgba(255,255,255,0.14)", font=dict(color="#ffffff", size=12, family="Geist, sans-serif")),
    )
    fig.add_annotation(xref="paper", yref="paper", x=0.012, y=0.985, xanchor="left", yanchor="top", showarrow=False,
                       text=hud_left, align="left", bgcolor="rgba(11,14,20,0.9)", borderpad=7,
                       font=dict(color=TEXT, size=12, family="Geist, sans-serif"))
    fig.add_annotation(xref="paper", yref="paper", x=0.988, y=0.015, xanchor="right", yanchor="bottom", showarrow=False,
                       text=hud_right, align="right", bgcolor="rgba(11,14,20,0.9)", borderpad=7,
                       font=dict(color=TEXT, size=11, family="Geist, sans-serif"))

# --- small drawing helpers ---
def _zone(fig, x0, y0, x1, y1, color=RED, dash="dash", alpha=0.08):
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, fillcolor=rgba(color, alpha),
                  line=dict(color=color, width=1.5, dash=dash), layer="below")

def _poly(fig, pts, color=RED, alpha=0.08, dash="dash"):
    path = "M " + " L ".join(f"{x},{y}" for x, y in pts) + " Z"
    fig.add_shape(type="path", path=path, fillcolor=rgba(color, alpha), line=dict(color=color, width=1.5, dash=dash), layer="below")

def _arrow(fig, x0, y0, x1, y1, color, width=2.5):
    fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y", text="",
                       showarrow=True, arrowhead=2, arrowsize=1.2, arrowcolor=color, arrowwidth=width)

def _label(fig, x, y, text, color, size=10):
    fig.add_annotation(x=x, y=y, text=f"<b>{text}</b>", showarrow=False,
                       font=dict(color=color, size=size, family="Plus Jakarta Sans, sans-serif"))

def _circle(fig, cx, cy, rx, ry, color=RED, alpha=0.14):
    fig.add_shape(type="circle", x0=cx - rx, y0=cy - ry, x1=cx + rx, y1=cy + ry,
                  fillcolor=rgba(color, alpha), line=dict(color=color, width=1.5, dash="dash"), layer="below")

# ==============================================================================
# ISSUE-SPECIFIC LAYER DEFINITIONS
# ==============================================================================
# ---------- ISSUE 1: REST DEFENSE ----------
I1_PLAYERS = [  # 4-2-3-1 in possession: back 4 (full-backs pushed high), double pivot, front 3 + lone striker
    (8, 34, "Lammens", "Senne Lammens"), (26, 42, "Martínez", "Lisandro Martínez"), (26, 26, "Maguire", "Harry Maguire"),
    (60, 62, "Dorgu", "Patrick Dorgu"), (60, 6, "Dalot", "Diogo Dalot"),
    (48, 40, "Tielemans", "Youri Tielemans"), (48, 26, "Mainoo", "Kobbie Mainoo"),
    (86, 58, "Rashford", "Marcus Rashford"), (80, 34, "Bruno", "Bruno Fernandes"), (86, 12, "Mbeumo", "Bryan Mbeumo"),
    (96, 34, "Cunha", "Matheus Cunha"),
]
def i1_halfspaces(f):
    _poly(f, [(32, 48), (66, 50), (66, 66), (32, 66)])
    _poly(f, [(32, 2), (66, 2), (66, 18), (32, 20)])
    _label(f, 44, 63.5, "VACATED HALF-SPACE", RED)
    _label(f, 44, 4.5, "VACATED HALF-SPACE", RED)
def i1_counters(f):
    _arrow(f, 64, 55, 36, 50, PASS, 3)
    _arrow(f, 64, 13, 36, 19, PASS, 3)
    _label(f, 50, 56.8, "OPPONENT TRANSITION HIGHWAY", PASS, 9)
def i1_isolated_pivot(f):
    _circle(f, 48, 33, 11, 13, WARN, 0.12)
    _circle(f, 40, 34, 9, 9, RED, 0.10)
    _label(f, 63.5, 34, "STRETCHED<br>DOUBLE PIVOT", WARN, 9)

# ---------- ISSUE 2: SECOND-HALF COLLAPSE ----------
I2_PLAYERS = [
    (6, 34, "Lammens", "Senne Lammens"), (22, 58, "Shaw", "Luke Shaw"), (22, 42, "Martínez", "Lisandro Martínez"),
    (22, 26, "Maguire", "Harry Maguire"), (22, 10, "Dalot", "Diogo Dalot"), (38, 42, "Mainoo", "Kobbie Mainoo"),
    (38, 26, "Tielemans", "Youri Tielemans"), (52, 56, "Rashford", "Marcus Rashford"), (52, 34, "Bruno", "Bruno Fernandes"),
    (52, 12, "Mbeumo", "Bryan Mbeumo"), (66, 34, "Šeško", "Benjamin Šeško"),
]
def i2_first_half(f):
    _zone(f, 18, 6, 56, 62, PASS, "dash", 0.06)
    _label(f, 37, 64.5, "1ST-HALF COMPACT BLOCK (GD +2)", PASS, 9)
def i2_gap(f):
    _zone(f, 27, 4, 40, 64, RED, "dot", 0.12)
    _label(f, 33.5, 1.2, "LATE FATIGUE GAP BETWEEN LINES", RED, 9)
    _arrow(f, 47, 34, 30, 34, PASS, 3)
def i2_late_goals(f):
    spots = [(3, 40, "83' Everton"), (3, 28, "90+6' Everton"), (3, 34, "90+1' Ipswich")]
    f.add_trace(go.Scatter(x=[s[0] for s in spots], y=[s[1] for s in spots], mode="markers", showlegend=False,
                           marker=dict(size=15, color=DANGER, symbol="x", line=dict(width=1, color="#fff")),
                           hovertext=[s[2] for s in spots], hoverinfo="text"))

# ---------- ISSUE 3: SET-PIECE DISORGANIZATION (defending own box, left goal) ----------
I3_PLAYERS = [
    (2.5, 34, "Lammens", "Senne Lammens"), (5.5, 40, "Maguire", "Harry Maguire"), (5.5, 28, "Martínez", "Lisandro Martínez"),
    (9, 46, "Heaven", "Ayden Heaven"), (9, 22, "Yoro", "Leny Yoro"), (12, 34, "Tielemans", "Youri Tielemans"),
    (12, 50, "Dalot", "Diogo Dalot"), (12, 18, "Dorgu", "Patrick Dorgu"), (15, 44, "Mainoo", "Kobbie Mainoo"),
    (15, 24, "Mbeumo", "Bryan Mbeumo"), (17, 34, "Bruno", "Bruno Fernandes"),
]
def i3_zonal_gaps(f):
    _circle(f, 11, 40, 4, 4, RED, 0.2)
    _circle(f, 8, 44, 3.5, 3.5, RED, 0.2)
    _label(f, 27, 53, "UNMARKED ZONAL GAPS", RED)
    _arrow(f, 24, 51.5, 12.5, 45, RED, 1.5)
def i3_opponents(f):
    add_opponents(f, [(10, 41, "Ajayi (Hull 17' corner)"), (7.5, 45, "Mendy (Hull 38' FK)"), (13, 39, "Runner (second ball)")])
def i3_conceded(f):
    goals = [(0.5, 36, "Hull 17'"), (0.5, 32, "Hull 38'"), (0.5, 34, "Everton 90+6'")]
    f.add_trace(go.Scatter(x=[g[0] for g in goals], y=[g[1] for g in goals], mode="markers", showlegend=False,
                           marker=dict(size=15, color="#ffd400", symbol="star"), hovertext=[g[2] for g in goals], hoverinfo="text"))

# ---------- ISSUE 4: BRUNO OVER-RELIANCE ----------
I4_PLAYERS = [
    (8, 34, "Lammens", "Senne Lammens"), (25, 48, "Martínez", "Lisandro Martínez"), (25, 20, "Maguire", "Harry Maguire"),
    (45, 58, "Dorgu", "Patrick Dorgu"), (50, 34, "Tielemans", "Youri Tielemans"), (45, 10, "Dalot", "Diogo Dalot"),
    (80, 60, "Rashford", "Marcus Rashford"), (72, 37, "Bruno", "Bruno Fernandes"), (75, 31, "Cunha", "Matheus Cunha"),
    (82, 10, "Mbeumo", "Bryan Mbeumo"), (92, 34, "Šeško", "Benjamin Šeško"),
]
def i4_overlap(f):
    _circle(f, 73.5, 34, 12, 14, WARN, 0.16)
    _label(f, 73.5, 50.5, "BRUNO + CUNHA SPACE OVERLAP", WARN, 9)
def i4_dependency(f):
    for (sx, sy) in [(50, 34), (25, 48), (45, 58), (45, 10), (80, 60)]:
        _arrow(f, sx, sy, 72, 37, PASS, 2)
    _label(f, 58, 21, "PASSING NETWORK FUNNELS INTO BRUNO", PASS, 9)
def i4_empty_box(f):
    _zone(f, 90, 20, 105, 48, SEC, "dot", 0.08)
    _label(f, 97.5, 50.5, "BOX LEFT TO ŠEŠKO", SEC, 9)

# ==============================================================================
# ISSUE REGISTRY (content for the Stitch investigation board)
# ==============================================================================
ISSUES = [
    {
        "key": "i1", "n": 1, "sev": "Critical High", "color": RED, "vi": 94.8, "metric": "+2.13 GA vs xGA", "metric_color": DANGER,
        "title": "The Rest Defense Void & Midfield Disconnect",
        "blurb": "Full-backs pushed into a 5-man line leave a two-man pivot covering both half-spaces on every turnover.",
        "code": "REST_DEF_V1", "stage_title": "Phase Freeze // Rest Defense Half-Space Exposure",
        "stage_sub": "United in a 2-3-5 possession shape; turnovers expose both vacated half-spaces", "direction": "Attacking L → R",
        "players": I1_PLAYERS, "focus": "Youri Tielemans",
        "layers": {"Vacated half-spaces": i1_halfspaces, "Counter vectors": i1_counters, "Isolated pivot": i1_isolated_pivot},
        "problem_title": "Structural Midfield Evacuation",
        "problem": "Inability to protect central half-spaces and prevent counter-attacks when committing numbers forward in high-possession states.",
        "fault": ("Two-Man Pivot Over-Stretched", "No destroyer: Baleba & Ugarte injured"),
        "evidence": [("Goals conceded (6 GP)", "10", DANGER), ("Opp. shots / match", "11.7", WARN), ("Opp. SoT conversion", "50%", DANGER)],
        "impact": "Opponents convert transitions at a very high rate, making ball dominance fragile — United lost 2-3 to Brighton after leading 2-0.",
        "impact_big": ("7", "Goals Conceded", "in the 4 fixtures with 55%+ possession"),
        "impact_foot": ("Brighton (H):", "2-0 → 2-3"),
        "cause_title": "Pivot Without Cover",
        "cause": "Carrick's framework pushes both full-backs high into a 5-man line, leaving a 2-man pivot (Tielemans + Mainoo) with too much lateral ground to cover — without injured destroyers Baleba & Ugarte.",
        "cause_foot": "Structural, not individual, failure",
    },
    {
        "key": "i2", "n": 2, "sev": "Severe", "color": WARN, "vi": 78.2, "metric": "5 GA after 60'", "metric_color": WARN,
        "title": "Second-Half & Stoppage-Time Collapses",
        "blurb": "A compact first-half block drifts apart after ~70' — late goals turned wins into draws and a 2-0 lead into a cup exit.",
        "code": "LATE_GAME_V2", "stage_title": "Phase Freeze // Late-Game Shape Drift",
        "stage_sub": "Lines pull apart as legs tire, opening a corridor between defence and midfield", "direction": "Defending R → L",
        "players": I2_PLAYERS, "focus": "Kobbie Mainoo",
        "layers": {"1st-half block": i2_first_half, "Late fatigue gap": i2_gap, "Late goals conceded": i2_late_goals},
        "problem_title": "Late Game-State Erosion",
        "problem": "Drastic decline in defensive organisation, press intensity and game-state management in the final 30 minutes.",
        "fault": ("Lines Separate After 70'", "Shape fine early, broken late"),
        "evidence": [("2nd-half goals (GF / GA)", "7 / 6", WARN), ("Goals conceded 76'+", "3", DANGER), ("Leads surrendered", "EVE, BHA", DANGER)],
        "impact": "Everton (A): conceded 83' &amp; 90+6' to turn a 2-1 win into a 2-2 draw. Brighton (H): conceded 45', 65', 70' to blow a 2-0 lead.",
        "impact_big": ("5", "Goals Conceded", "after the 60th minute — half of all goals against"),
        "impact_foot": ("Leads lost:", "2 PL pts + EFL exit"),
        "cause_title": "Fatigue & Disruptive Subs",
        "cause": "Physical fatigue in the double pivot plus substitutions that disrupt zonal communication in the backline under late direct play.",
        "cause_foot": "Game-state management deficit",
    },
    {
        "key": "i3", "n": 3, "sev": "High Risk", "color": DANGER, "vi": 81.0, "metric": "4 set-piece GA", "metric_color": DANGER,
        "title": "Set-Piece Disorganization & 2nd-Ball Lethargy",
        "blurb": "Hybrid zonal/man scheme leaves danger runs untracked; lower-tier sides score without open-play dominance.",
        "code": "DEAD_BALL_V3", "stage_title": "Phase Freeze // Defensive Set-Piece Map",
        "stage_sub": "Bodies in the box but nobody tracking the danger runs into the gaps", "direction": "Defending left goal",
        "players": I3_PLAYERS, "focus": "Harry Maguire", "view": {"x": [-2, 40], "y": [13, 55]},
        "layers": {"Unmarked zonal gaps": i3_zonal_gaps, "Aerial threats": i3_opponents, "Goals conceded": i3_conceded},
        "problem_title": "Dead-Ball Box Control",
        "problem": "Systematic failure to defend aerial dead-ball deliveries and clean second balls inside the 18-yard box.",
        "fault": ("Zonal / Man Hand-off Breaks", "No dominant second-ball winner"),
        "evidence": [("Hull set-piece goals", "17' & 38'", DANGER), ("Late set-piece scrambles", "IPS 91' · EVE 96'", WARN), ("Set-piece share of GA", "40%", DANGER)],
        "impact": "Lets lower-tier opponents take early leads without open-play dominance, forcing United to chase low-block games.",
        "impact_big": ("4", "Goals Conceded", "from set-piece phases across 6 fixtures"),
        "impact_foot": ("Hull (A):", "0-2 on 72% possession"),
        "cause_title": "Scheme Miscommunication",
        "cause": "Miscommunication in Carrick's hybrid zonal/man scheme between CBs (Maguire, Martínez, Heaven) and Lammens, plus no dominant second-ball winner.",
        "cause_foot": "Coaching & personnel",
    },
    {
        "key": "i4", "n": 4, "sev": "Tactical Drag", "color": PASS, "vi": 64.5, "metric": "38.5% goal share", "metric_color": MUTED,
        "title": "Bruno Over-Reliance & Frontline Friction",
        "blurb": "Every attack funnels through Bruno; when low blocks take away the #10 space, United stop scoring.",
        "code": "ATTACK_HUB_V4", "stage_title": "Phase Freeze // Attacking-Third Congestion",
        "stage_sub": "Bruno and Cunha crowd the same #10 pocket; the box is left to Šeško", "direction": "Attacking L → R",
        "players": I4_PLAYERS, "focus": "Bruno Fernandes",
        "layers": {"Bruno–Cunha overlap": i4_overlap, "Passing dependency": i4_dependency, "Vacated box": i4_empty_box},
        "problem_title": "Single-Point Creativity",
        "problem": "Offensive output leans heavily on Bruno Fernandes, causing open-play sterility when low blocks restrict central #10 space.",
        "fault": ("One Creative Hub", "Attack stalls when Bruno is marked"),
        "evidence": [("Bruno G / A", "4G · 1A", POS), ("Goals when Bruno blanked", "0 (33 shots)", DANGER), ("Cunha vs Šeško", "1G/5 st · 2G/2 st", WARN)],
        "impact": "Unable to break low blocks or beat 10-man City (51% possession, red card in 23').",
        "impact_big": ("0", "Goals Scored", "vs Hull & City — 33 shots, 11 corners"),
        "impact_foot": ("Bruno share of goals:", "38.5%"),
        "cause_title": "Forward-Line Role Tension",
        "cause": "Tension between Cunha's deep-dropping link play (crowding Bruno) and Šeško's box presence (isolating midfield when pressing).",
        "cause_foot": "Role definition issue",
    },
]

# "How to read this board" guides. Each key row names the layer exactly as its toggle does and uses the same
# symbol/colour as the pitch drawing: (symbol kind, colour, what it is, what it means).
BOARD_GUIDES = {
    "i1": {
        "setup": "United have the ball and are attacking <b>left → right</b>. Both full-backs have pushed up to join the attack.",
        "keys": [
            ("zone", RED, "Vacated half-spaces", "The space the full-backs leave behind. Nobody covers it if the ball is lost."),
            ("arrow", PASS, "Counter vectors", "Where opponents run the moment they win the ball back: straight into those empty spaces."),
            ("ring", WARN, "Isolated pivot", "Tielemans and Mainoo, the only two midfielders left to stop a counter. They can't cover both sides at once."),
        ],
        "takeaway": "When United lose the ball, two midfielders are left guarding the whole width of the pitch. Everton and Brighton punished this shape.",
    },
    "i2": {
        "setup": "United are <b>defending the goal on the left</b>. The board compares their shape early in games with the last 20 minutes.",
        "keys": [
            ("zone", PASS, "1st-half block", "How compact United are early on: defence and midfield close together."),
            ("band", RED, "Late fatigue gap", "The space that opens between defence and midfield after about 70 minutes as players tire. The arrow shows opponents running through it."),
            ("x", DANGER, "Late goals conceded", "The three late goals: 83' and 90+6' at Everton, 90+1' vs Ipswich."),
        ],
        "takeaway": "The shape holds early. It breaks late on, when midfield and defence drift apart.",
    },
    "i3": {
        "setup": "Zoomed in on <b>United's own penalty box</b> while defending a corner or free-kick. The goal is on the left.",
        "keys": [
            ("ring", RED, "Unmarked zonal gaps", "Spaces between United's zonal markers that no one is responsible for."),
            ("opp", PASS, "Aerial threats", "Opponent attackers running into those gaps, e.g. Hull's Ajayi and Mendy."),
            ("star", "#ffd400", "Goals conceded", "Set-piece goals conceded: Hull 17' and 38', Everton 90+6'."),
        ],
        "takeaway": "United have enough players in the box, but the runs into the gaps go untracked, and that's where the goals came from.",
    },
    "i4": {
        "setup": "United have the ball in the final third, attacking <b>left → right</b>.",
        "keys": [
            ("ring", WARN, "Bruno–Cunha overlap", "Bruno and Cunha both play in the same #10 space, so they get in each other's way."),
            ("arrow", PASS, "Passing dependency", "Where the passes go: almost every route leads to Bruno."),
            ("dotbox", SEC, "Vacated box", "The penalty area, often left to Šeško alone."),
        ],
        "takeaway": "When opponents mark Bruno out of that space, United run out of ideas. They failed to score against Hull and City.",
    },
}

def guide_symbol(kind, c):
    """Small legend symbol drawn in the same style as the pitch layer."""
    base = "flex-shrink:0;display:inline-block;"
    if kind == "zone":
        return f'<span style="{base}width:18px;height:12px;border:1.5px dashed {c};background:{rgba(c, 0.12)};border-radius:2px;"></span>'
    if kind == "band":
        return f'<span style="{base}width:18px;height:12px;border:1.5px dotted {c};background:{rgba(c, 0.15)};"></span>'
    if kind == "dotbox":
        return f'<span style="{base}width:18px;height:12px;border:1.5px dotted {c};background:{rgba(c, 0.08)};"></span>'
    if kind == "ring":
        return f'<span style="{base}width:14px;height:14px;border:1.5px dashed {c};background:{rgba(c, 0.15)};border-radius:9999px;"></span>'
    if kind == "arrow":
        return f'<span style="{base}color:{c};font-weight:700;font-size:15px;line-height:1;width:18px;text-align:center;">➜</span>'
    if kind == "x":
        return f'<span style="{base}color:{c};font-weight:800;font-size:15px;line-height:1;width:18px;text-align:center;">✕</span>'
    if kind == "star":
        return f'<span style="{base}color:{c};font-size:15px;line-height:1;width:18px;text-align:center;">★</span>'
    if kind == "opp":
        return f'<span style="{base}width:11px;height:11px;margin:0 3.5px;border-radius:9999px;background:#fff;box-shadow:0 0 0 2px {c};"></span>'
    return f'<span style="{base}width:11px;height:11px;margin:0 3.5px;border-radius:9999px;background:{RED_CORE};box-shadow:0 0 0 2px {ELEV},0 0 0 3.5px {RED};"></span>'

def board_guide(iss):
    g = BOARD_GUIDES[iss["key"]]
    rows = [("node", RED, "United players", "Red circles with initials. Click one to see that player on the right.")] + g["keys"]
    key_html = "".join(f'''<div class="row start gs" style="padding:0.45rem 0;border-top:1px solid rgba(255,255,255,0.05);">
      <span style="width:22px;display:flex;justify-content:center;padding-top:3px;">{guide_symbol(kind, c)}</span>
      <div class="body-sm" style="line-height:1.5;"><b style="color:{TEXT};">{name}</b> — {meaning}</div></div>''' for kind, c, name, meaning in rows)
    return f'''<div style="background:rgba(22,27,38,0.7);border-radius:0.75rem;padding:0.85rem 1rem;margin:0.75rem 0 0.5rem;">
    <div class="row gs">{ico("explore", 18, SEC)}<span class="lbl t">How to read this board</span></div>
    <div class="body-sm t" style="margin-top:0.5rem;line-height:1.6;"><span class="lbl" style="color:{SEC};">The situation</span><br>{g["setup"]}</div>
    <div class="lbl" style="color:{SEC};margin-top:0.7rem;margin-bottom:0.15rem;">Key</div>{key_html}
    <div class="row start gs" style="margin-top:0.6rem;background:{rgba(iss["color"], 0.08)};padding:0.6rem 0.75rem;border-radius:0.5rem;box-shadow:inset 3px 0 0 {iss["color"]};">
      {ico("lightbulb", 18, iss["color"])}<div class="body-sm t" style="line-height:1.55;"><b>The takeaway:</b> {g["takeaway"]}</div></div>
    <div class="lbl-sm" style="margin-top:0.5rem;opacity:0.75;font-size:11px;">Player positions show United's typical shape in this phase, not a moment from one match. Use the layer toggles below to show or hide each element.</div></div>'''

# Danger-zone centres on each board (same coordinates as the drawn layers) and the distance (m)
# beyond which a player counts as fully clear of them. Feeds the per-player exposure index.
ISSUE_ZONES = {  # (x, y, plain-English name of the danger zone)
    "i1": ([(49, 57, "the left half-space left empty when the left-back pushes on"),
            (49, 11, "the right half-space left empty when the right-back pushes on"),
            (48, 33, "the stretched two-man midfield pivot")], 30),
    "i2": ([(33.5, 34, "the gap that opens between defence and midfield late on"),
            (3, 34, "the goalmouth where the late goals went in")], 30),
    "i3": ([(11, 40, "the unmarked zone near the penalty spot"), (8, 44, "the unmarked runs at the back post")], 14),
    "i4": ([(73.5, 34, "the crowded #10 pocket where the attack gets funnelled")], 30),
}

def player_exposure(issue, name, mins):
    """Player exposure index (0–100) for one issue = zone proximity (≤60) + minutes load (≤40).
    Derived from the board model and minutes played — an analyst heuristic, not a provider metric."""
    zones, reach = ISSUE_ZONES[issue["key"]]
    x, y = next((c[0], c[1]) for c in issue["players"] if c[3] == name)
    dist, zone = min((math.hypot(x - zx, y - zy), lab) for zx, zy, lab in zones)
    prox = 60 * max(0.0, 1 - dist / reach)
    share = min(mins / MAX_MINS, 1.0)
    load = 40 * share
    score = prox + load
    tier = ("High Exposure", DANGER) if score >= 70 else (("Watch", WARN) if score >= 40 else ("Stable", POS))
    # plain-language readings of the two components
    where = ("In the danger zone" if dist <= reach / 3 else "Close to the danger zone" if dist <= 2 * reach / 3
             else "On the edge of it" if dist < reach else "Away from it")
    how = ("Ever-present" if share >= 0.8 else "Regular starter" if share >= 0.55 else "Rotation option" if share >= 0.25 else "Bit-part")
    return dict(score=score, prox=prox, load=load, dist=dist, tier=tier[0], color=tier[1],
                zone=zone, where=where, how=how, share=share)

# Hand-written role of every player on every board: (role title, what they do in this phase and how it ties to the issue).
# Grounded only in the issue write-ups, the board layouts and the player notes already in this file.
ISSUE_ROLES = {
    "i1": {  # Rest defense — United in possession, full-backs pushed high
        "Senne Lammens": ("Last line of defence",
            "With both full-backs pushed forward, only the two centre-backs stand between Lammens and a counter that breaks through a vacated half-space."),
        "Lisandro Martínez": ("Covering centre-back (left)",
            "One of only two defenders behind the ball. When the left half-space is empty, Martínez has to step across and meet the counter alone."),
        "Harry Maguire": ("Covering centre-back (right)",
            "The other half of a two-man rest defence. Maguire has to cover the right channel that opens once Dalot pushes on."),
        "Patrick Dorgu": ("Attacking left-back — leaves a gap",
            "Pushes into the front line to add width. When the ball is lost, the space Dorgu left behind is one of the two red half-spaces opponents run into."),
        "Diogo Dalot": ("Attacking right-back — leaves a gap",
            "Pushes high on the right. The half-space behind Dalot is the second red zone, and Everton and Brighton countered through this kind of space."),
        "Youri Tielemans": ("Pivot — the most stretched player",
            "One of only two midfielders screening the defence. On every turnover Tielemans is pulled between both empty half-spaces (the amber ring)."),
        "Kobbie Mainoo": ("Pivot partner — stretched",
            "Shares the screening job with Tielemans. Two midfielders cannot cover both flanks, so one channel is always open."),
        "Marcus Rashford": ("Left winger — where counters can start",
            "Stays high on the left. Not part of the defensive gap, but losing the ball here sends opponents straight into the space Dorgu left."),
        "Bruno Fernandes": ("#10 — commits forward",
            "Joins the attack to create. A lost ball in the #10 zone releases the counter before the pivot can reset."),
        "Bryan Mbeumo": ("Right winger — where counters can start",
            "Holds the width on the right. Losing the ball here exposes the channel Dalot vacated."),
        "Matheus Cunha": ("Striker — not part of the gap",
            "Furthest player forward. The problem is the space behind the midfield, not Cunha's defending."),
    },
    "i2": {  # Second-half collapse — United defending, lines drift apart after ~70'
        "Senne Lammens": ("Goalkeeper — beaten by the late goals",
            "The late goals (83' and 90+6' at Everton, 90+1' vs Ipswich) went in here. The board traces them to the gap opening in front of the defence."),
        "Luke Shaw": ("Left-back holding the line",
            "Keeps the back four's shape. Late on, the danger is the space opening in front of Shaw, not behind."),
        "Lisandro Martínez": ("Centre-back — loses protection late on",
            "Compact and well protected in the first half. After ~70' the midfield drops off and runners come through the gap straight at Martínez."),
        "Harry Maguire": ("Centre-back — loses protection late on",
            "Same exposure as Martínez: once the lines separate, the centre-backs face runners with no midfield screen."),
        "Diogo Dalot": ("Right-back holding the line",
            "Holds the right of the back four. Not in the gap itself, but defends more late-game direct balls as the block tires."),
        "Kobbie Mainoo": ("Tiring pivot — the gap opens here",
            "One half of the double pivot. As legs go after ~70', the distance to the back line grows and the red gap opens."),
        "Youri Tielemans": ("Tiring pivot — the gap opens here",
            "Partners Mainoo in the pivot. The fatigue gap between defence and midfield opens directly behind these two."),
        "Marcus Rashford": ("Left midfield in the block",
            "Part of the compact first-half block. Not in the central gap, but fewer recovery runs late on thin the midfield out."),
        "Bruno Fernandes": ("Top of the midfield block",
            "Links midfield to attack. When United chase or protect a lead, Bruno's position further up stretches the block."),
        "Bryan Mbeumo": ("Right midfield in the block",
            "Mirrors Rashford on the right: part of the first-half shape, away from the central gap."),
        "Benjamin Šeško": ("Lone striker — not involved",
            "Leads the line. Not part of the defensive shape that breaks down late."),
    },
    "i3": {  # Set pieces — defending a dead ball in United's own box
        "Senne Lammens": ("Goalkeeper — part of the hand-off",
            "Commands the six-yard box. The issue write-up points to miscommunication between Lammens and the centre-backs in the zonal/man scheme (Hull 17' and 38')."),
        "Harry Maguire": ("Zonal centre-back",
            "Holds a zone in the hybrid scheme. The unmarked red gaps sit between the zones held by Maguire and the other centre-backs."),
        "Lisandro Martínez": ("Zonal centre-back",
            "Holds a zone close to goal. Named in the write-up as part of the centre-back communication breakdown."),
        "Ayden Heaven": ("Zonal centre-back",
            "Holds a back-post zone next to one of the unmarked gaps. Also named in the write-up's miscommunication point."),
        "Leny Yoro": ("Zonal defender",
            "Guards the side of the box away from the gaps where the goals came from."),
        "Youri Tielemans": ("Screens the zonal line",
            "Stands in front of the zonal line, closest to where attackers arrive. Nobody is clearly assigned to win the second ball."),
        "Diogo Dalot": ("Wide box cover",
            "Covers the far side of the box. Close to the back-post runs that go unmarked."),
        "Patrick Dorgu": ("Wide box cover",
            "Covers the other side of the box, away from the red gaps."),
        "Kobbie Mainoo": ("Picks up a runner",
            "Man-marks inside the box. The danger comes from the runs into the gaps that nobody is tracking."),
        "Bryan Mbeumo": ("Edge of the box — second ball",
            "Waits for clearances. With no dominant second-ball winner, loose balls fall to opponents, as in the Ipswich 91' scramble."),
        "Bruno Fernandes": ("Edge of the box — second ball / counter",
            "Holds the edge ready to break. Part of the second-ball problem the write-up describes."),
    },
    "i4": {  # Bruno over-reliance — United attacking
        "Bruno Fernandes": ("Creative hub — the issue itself",
            "Almost every attack goes through Bruno (4 goals, 1 assist, 38.5% of goals). When opponents marked Bruno out of the #10 zone (Hull, City), United scored 0."),
        "Matheus Cunha": ("Drops into Bruno's space",
            "Comes off the front line into the same #10 pocket to link play, which takes a runner out of the box (1 goal in 5 starts)."),
        "Benjamin Šeško": ("Isolated in the box",
            "Often the only player in the penalty area (the dotted box). Scored 2 in 2 starts when the service arrived."),
        "Youri Tielemans": ("Feeds the Bruno funnel",
            "The deep playmaker: Tielemans' passes (2 assists) are mostly routed into Bruno rather than around the #10."),
        "Lisandro Martínez": ("Builds play from the back",
            "Plays line-breaking passes from deep, and these also funnel into Bruno."),
        "Patrick Dorgu": ("Wide supply — routed inside",
            "Gives width on the left, but the ball tends to come inside to Bruno instead of into the box."),
        "Diogo Dalot": ("Wide supply — routed inside",
            "Same pattern on the right: moves play towards Bruno rather than the penalty area."),
        "Marcus Rashford": ("Winger — under-used outlet",
            "Direct option on the left who gets less of the ball when play is forced through the middle (0 goals from 1.2 xG)."),
        "Bryan Mbeumo": ("Winger — alternative threat",
            "Right-side outlet with 2 goals. Gives the attack a way around Bruno when used."),
        "Harry Maguire": ("Not involved",
            "Stays behind the ball. Not part of this attacking issue."),
        "Senne Lammens": ("Not involved",
            "Goalkeeper. Not part of this attacking issue."),
    },
}

def exposure_card(ex, iss, name, mins, rank):
    """Player exposure gauge: score readout, needle, issue-index marker and the two score components."""
    s, vi, col = ex["score"], iss["vi"], ex["color"]
    ticks = "".join(f'<span class="mono" style="position:absolute;left:{p}%;transform:translateX({-50 if 0 < p < 100 else (0 if p == 0 else -100)}%);'
                    f'font-size:10px;color:{MUTED};">{p}</span>' for p in (0, 40, 70, 100))
    zones = "".join(f'<span class="lbl" style="position:absolute;left:{a}%;width:{b - a}%;text-align:center;font-size:9.5px;color:{c};">{t}</span>'
                    for a, b, t, c in ((0, 40, "Stable", POS), (40, 70, "Watch", WARN), (70, 100, "High", DANGER)))

    def part(label, verdict, detail, val, cap, color):
        # plain-language verdict first; the points are secondary
        return f'''<div style="background:{ELEV};padding:0.6rem 0.7rem;border-radius:0.5rem;">
        <div class="row between gs"><span class="lbl">{label}</span><span class="mono lbl-sm" style="font-size:10.5px;">+{val:.0f} of {cap} pts</span></div>
        <div class="body-sm t" style="font-weight:600;margin-top:3px;color:{color};">{verdict}</div>
        <div class="body-sm" style="font-size:12px;line-height:1.4;">{detail}</div></div>'''

    return f'''<div class="card" style="margin-top:1rem;padding:1.1rem;overflow:visible;">
    <div class="row between"><span class="lbl" style="white-space:nowrap;">Exposure Meter</span>{pill(ex["tier"], col, dot=True)}</div>
    <div class="row gs" style="align-items:baseline;margin-top:0.5rem;">
      <span class="stat" style="color:{col};">{s:.0f}</span><span class="mono body-sm m">/ 100</span>
      <span class="body-sm" style="margin-left:auto;">Rank <b>#{rank}</b> of {len(iss["players"])} on this board</span></div>
    <div style="position:relative;margin:1.4rem 0 0.2rem;">
      <div style="position:absolute;left:{s:.1f}%;top:-1.35rem;transform:translateX(-50%);" class="mono lbl-sm t"><b>{s:.0f}</b></div>
      <div class="bar" style="height:10px;"><div style="width:40%;background:{POS};"></div><div style="width:30%;background:{WARN};"></div>
      <div style="width:30%;background:{DANGER};"></div></div>
      <div style="position:absolute;left:calc({s:.1f}% - 2px);top:-4px;width:4px;height:18px;background:#fff;border-radius:2px;
        box-shadow:0 0 0 2px {CARD},0 0 10px rgba(255,255,255,0.7);"></div>
      <div style="position:absolute;left:{vi:.1f}%;top:13px;transform:translateX(-50%);width:0;height:0;
        border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:7px solid {MUTED};"></div>
    </div>
    <div style="position:relative;height:1.1rem;">{zones}</div>
    <div style="position:relative;height:0.9rem;">{ticks}</div>
    <div class="row gs lbl-sm" style="margin-top:0.35rem;font-size:11px;">
      <span class="row gx"><span style="width:4px;height:12px;background:#fff;border-radius:2px;"></span>{esc(name.split()[-1])}</span>
      <span class="row gx"><span style="width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:7px solid {MUTED};"></span>
      Issue index {vi:.1f} ({iss["sev"].lower()})</span></div>
    <div class="body-sm" style="margin-top:0.75rem;">Why this score:</div>
    <div class="col gs" style="margin-top:0.35rem;">
      {part("Position on the board", ex["where"], "Nearest danger zone: " + ex["zone"], ex["prox"], 60,
            DANGER if ex["prox"] >= 40 else WARN if ex["prox"] >= 20 else POS)}
      {part("Playing time", ex["how"], f"{ex['share'] * 100:.0f}% of available minutes ({mins} of {MAX_MINS})", ex["load"], 40,
            DANGER if ex["load"] >= 32 else WARN if ex["load"] >= 22 else POS)}</div>
    <div class="lbl-sm" style="margin-top:0.6rem;font-size:11px;opacity:0.8;">Analyst estimate: the closer a player stands to where this
    issue happens, and the more they play, the more exposed they are to it.</div></div>'''

# ------------------------------------------------------------------------------
# 8. NAVIGATION (Stitch left rail) & TOP BAR
# ------------------------------------------------------------------------------
NAV = [
    ("Executive Summary", "analytics"),
    ("Match Results & Form", "calendar_month"),
    ("Attacking Analytics", "sports_soccer"),
    ("Defensive & Transition", "shield"),
    ("Player Performance Matrix", "group"),
    ("Investigation Board", "tactic"),
    ("Data Methodology", "verified"),
]
st.session_state.setdefault("nav", "Executive Summary")
st.session_state.setdefault("issue", 0)

def goto(page):
    st.session_state["nav"] = page

def set_issue(i):
    st.session_state["issue"] = i
    st.session_state["scroll_to_board"] = True  # one-shot: jump down to the board on the next run

def scroll_to(selector):
    """Smooth-scroll the app to the first element matching `selector` (runs once, from a zero-height component).
    Streamlit has no scroll API, so a tiny same-origin component reaches into the parent page."""
    st.session_state["_scroll_seq"] = st.session_state.get("_scroll_seq", 0) + 1  # new content => script re-runs
    with st.container(key="scrollhook"):
        components.html(f"""<script>
        // run #{st.session_state['_scroll_seq']}
        const doc = window.parent.document; let tries = 0;
        const go = () => {{
          const el = doc.querySelector({selector!r});
          if (el) {{ el.scrollIntoView({{behavior: "smooth", block: "start"}}); }}
          else if (tries++ < 40) {{ setTimeout(go, 100); }}   // wait up to 4s for the board to render
        }};
        setTimeout(go, 150);
        </script>""", height=0)

with st.sidebar:
    H(f'''<div class="row gs" style="height:3rem;padding:0 0.25rem;"><span style="flex-shrink:0;display:flex;">{logo(34)}</span>
    <div class="col" style="min-width:0;"><span style="font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.08rem;letter-spacing:-0.01em;color:{TEXT};line-height:1;white-space:nowrap;">THEATRE OF DATA</span>
    <span class="lbl" style="letter-spacing:0.12em;margin-top:5px;white-space:nowrap;">MUFC Analytics · 2026/27</span></div></div>
    <div class="row between" style="background:rgba(22,27,38,0.7);padding:0.5rem;border-radius:0.5rem;margin:0.25rem 0 0.75rem;">
    <div class="row gx"><span class="dot pulse" style="width:8px;height:8px;background:{RED};"></span>
    <span class="lbl" style="color:{TEXT};">Report #4 Live</span></div><span class="mono body-sm" style="color:{SEC};">MD 1–6</span></div>''')
    for label, icon in NAV:
        st.button(label, key=f"nav_{icon}", icon=f":material/{icon}:", width="stretch",
                  type="primary" if st.session_state["nav"] == label else "tertiary", on_click=goto, args=(label,))
    H(f'''<div class="side-feed" style="background:rgba(11,14,20,0.5);padding:0.75rem;border-radius:0.5rem;">
    <div class="col gx" style="background:rgba(22,27,38,0.4);padding:0.5rem;border-radius:0.5rem;">
    <div class="row between"><span class="lbl">Data Feed Engine</span><span class="lbl" style="color:{POS};">Synchronized</span></div>
    <div class="row gx m">{ico("database", 14)}<span class="body-sm">Opta / FotMob · 6 fixtures</span></div></div></div>''')

nav = st.session_state["nav"]

SCOPES = ["All Matches", "Home", "Away", "Top-6"]
ALL_COMPS = list(df_matches["Competition"].unique())
ALL_OPPS = list(df_matches["Opponent_Category"].unique())
# The match-scope filters don't apply to these pages (season-total player data / illustrative boards)
NO_FILTER_PAGES = {"Player Performance Matrix", "Investigation Board"}
show_filters = nav not in NO_FILTER_PAGES

# Streamlit drops a widget's state on runs where it isn't rendered, so the selections are mirrored
# into plain session keys and restored as defaults when the top bar comes back.
st.session_state.setdefault("_scope", "All Matches")
st.session_state.setdefault("_comps", ALL_COMPS)
st.session_state.setdefault("_opps", ALL_OPPS)

def apply_filters(scope, comps, opps):
    out = df_matches[df_matches["Competition"].isin(comps) & df_matches["Opponent_Category"].isin(opps)]
    if scope == "Home":
        out = out[out.Venue == "Home"]
    elif scope == "Away":
        out = out[out.Venue == "Away"]
    elif scope == "Top-6":
        out = out[out.Opponent_Category == "Elite / Top-6"]
    return out

if show_filters:
    # Widget keys already hold this run's values (the _-prefixed mirrors are updated below), so the live
    # fixture count can be computed *before* the bar is drawn and the label renders at its natural height.
    cur_s = st.session_state.get("scope", st.session_state["_scope"]) or "All Matches"
    cur_c = st.session_state.get("comps", st.session_state["_comps"])
    cur_o = st.session_state.get("opps", st.session_state["_opps"])
    n_view = len(apply_filters(cur_s, cur_c, cur_o))
    n_active = (len(cur_c) < len(ALL_COMPS)) + (len(cur_o) < len(ALL_OPPS))
    with st.container(key="topbar"):
        t1, t2, t3 = st.columns([3, 3.2, 1.3], vertical_alignment="center")
        with t1:
            H(f'''<div class="row gs topbar-ctx">
            <div class="ibox" style="width:2.25rem;height:2.25rem;border-radius:0.5rem;background:{rgba(RED, 0.14)};color:{RED};">{ico("timer", 19)}</div>
            <div class="col" style="line-height:1.3;gap:1px;"><span class="lbl" style="font-size:10px;line-height:1.2;">2026/27 Season Review</span>
            <span class="body-sm t" style="font-weight:600;white-space:nowrap;line-height:1.3;">Matchday 1–6
            <span class="m" style="font-weight:400;"> · </span><span style="color:{SEC if n_view == len(df_matches) else WARN};">{n_view} of {len(df_matches)} fixtures</span></span></div></div>''')
        with t2:
            scope = st.segmented_control("Scope", SCOPES, default=st.session_state["_scope"], key="scope",
                                         label_visibility="collapsed") or "All Matches"
        with t3:
            with st.popover(f"Filters · {n_active}" if n_active else "Filters", icon=":material/tune:"):
                comp_filter = st.multiselect("Competition", options=ALL_COMPS, default=st.session_state["_comps"], key="comps")
                opp_filter = st.multiselect("Opponent strength", options=ALL_OPPS, default=st.session_state["_opps"], key="opps")
        st.session_state["_scope"], st.session_state["_comps"], st.session_state["_opps"] = scope, comp_filter, opp_filter
        filtered_df = apply_filters(scope, comp_filter, opp_filter)
    if filtered_df.empty:
        st.warning("No fixtures match the current scope and filters — widen the top-bar scope or the Filters popover.")
        st.stop()
else:
    scope, filtered_df = "All Matches", df_matches
    st.write("")  # breathing room where the top bar would sit

S = team_stats(filtered_df)
SCOPE_TXT = f"{scope} · {S['n']} fixture{'s' if S['n'] != 1 else ''}"

def cta_tactics_board():
    with st.container(key="cta"):
        c1, c2 = st.columns([4, 1.2], vertical_alignment="center")
        with c1:
            H(f'''<div class="row gm z"><div class="ibox" style="width:3rem;height:3rem;border-radius:0.75rem;background:{RED_CORE};box-shadow:0 0 20px rgba(255,45,59,0.4);">
            {ico("tactic", 28, "#fff")}</div><div class="col">
            <div class="row gx wrap"><span class="lbl" style="color:{RED};font-weight:700;">Deep Tactical Inspection</span>
            <span class="dot" style="background:{SEC};"></span><span class="lbl">Interactive 2D Pitch</span></div>
            <div class="h-sm" style="font-weight:700;">Launch Interactive Tactics Board &amp; Player Inspector</div>
            <div class="body-sm">Four issue boards with toggleable tactical layers and click-to-inspect player telemetry for MD 1–6.</div></div></div>''')
        with c2:
            st.button("Open Tactics Board", icon=":material/arrow_forward:", type="primary", width="stretch",
                      key=f"cta_{nav}", on_click=goto, args=("Investigation Board",))

# ==============================================================================
# PAGE: EXECUTIVE SUMMARY
# ==============================================================================
def page_executive(f, s):
    tags = (pill("Tactical Crisis Report // Matchdays 1–6", RED, ping=True)
            + pill(f"PL Standing: 13th ({PL_PTS} Pts / {3 * len(_pl)})", MUTED, bg=0.08)
            + pill(f"{s['W']} Wins in {s['n']}", DANGER))
    over = s["GA"] - s["xGA"]
    takeaways = [
        ((DANGER, "history_toggle_off", signed(over) + " GA", "Above xGA",
          f"{s['GA']} conceded vs {s['xGA']:.2f} expected — leaking beyond chance quality.") if over > 0.05 else
         (POS, "shield", signed(over) + " GA", "Below xGA",
          f"{s['GA']} conceded vs {s['xGA']:.2f} expected — defending held up in this view.")),
        (WARN, "crisis_alert", f"{s['late_ga']} GA", "Post-60' Collapse", f"{s['late_ga']} of {s['GA']} goals conceded came after the 60th minute."),
        (SEC, "bolt", f"{s['poss']:.1f}%", "Avg Possession", "Territorial dominance without matchday control — 13th in the PL."),
    ]
    tk = "".join(f'''<div class="tile hov row start gs" style="padding:0.6rem 0.75rem;">
      <div class="ibox" style="background:{rgba(c, 0.15)};color:{c};">{ico(i, 20)}</div>
      <div class="col grow"><div class="row gx wrap"><span class="h-sm" style="color:{c};font-weight:700;">{v}</span><span class="lbl">{l}</span></div>
      <span class="body-sm">{d}</span></div></div>''' for c, i, v, l, d in takeaways)
    inner = page_head(tags, "Anatomy of a Stalled Engine: Why United's 2026/27 Campaign is Bleeding Points",
                      "Leaky rest defense, second-half transition frailties and set-piece disorganisation have turned dominant "
                      "territorial control into self-inflicted matchday defeats.",
                      banner=True, meta=f"Sample: {s['n'] * 90:,} mins · {SCOPE_TXT} · Opta / FotMob")
    banner_open(inner, f'<div class="grid g3 gsm z" style="margin-top:1rem;">{tk}</div>')

    # --- 1. Summary first: the diagnosis ---
    conv = sdiv(s["GA"], s["osot"]) * 100
    xg_wins = int((f.xG > f.xGA).sum())
    section_head("Forensic Investigation", "Three Core Structural Failures", "Tactical Breakdown // Opta Vision")
    diags = [
        (WARN, "target", ISSUES[0], "Opp. SoT Conversion", f"{conv:.0f}% ({s['GA']} of {s['osot']})", "Issue #01"),
        (DANGER, "alt_route", ISSUES[1], "Goals Conceded After 60'", f"{s['late_ga']} of {s['GA']}", "Issue #02"),
        (SEC, "battery_alert", ISSUES[2], "Set-Piece Phase Goals", f"{s['sp_ga']} of {s['GA']}", "Issue #03"),
    ]
    H('<div class="grid g3">' + "".join(f'''<div class="card hov col between" style="padding:1rem;">
      <div class="col gx"><div class="row between">{pill(f"Diagnostic 0{k + 1}", c)}{ico(i, 22, MUTED)}</div>
      <div class="h-sm" style="margin-top:0.35rem;">{iss["title"]}</div>
      <div class="body-sm" style="line-height:1.65;">{iss["problem"]} {iss["blurb"]}</div></div>
      <div class="row between" style="margin-top:1rem;background:rgba(22,27,38,0.4);padding:0.6rem;border-radius:0.5rem;">
      <div class="col"><span class="lbl" style="font-size:10px;">{fl}</span><span class="mono body-sm" style="color:{c};font-weight:700;">{fv}</span></div>
      <span class="mono lbl-sm">{tag}</span></div></div>''' for k, (c, i, iss, fl, fv, tag) in enumerate(diags)) + '</div>')
    # insight sentence adapts to the numbers in scope
    won_txt = f", yet won only {s['W']}." if s["W"] < xg_wins else f" and won {s['W']}."
    if over > 0.05:
        opp_txt = (f" Opponents scored {s['GA']} from just {s['osot']} shots on target — the disconnect lies in transition defence and "
                   "dead-ball organisation, not chance creation.")
    else:
        opp_txt = f" Opponents scored {s['GA']} from {s['osot']} shots on target, no more than their chances warranted."
    H(f'''<div class="card" style="margin-top:1rem;"><div class="row gx" style="color:{SEC};">{ico("verified", 18, SEC)}<span class="lbl" style="color:{SEC};">Telemetry Insight Note</span></div>
    <div class="body-sm t" style="margin-top:0.5rem;line-height:1.65;">United recorded <b>greater expected goals (xG) than their opponents in {xg_wins} of {plural(s['n'], 'fixture')}</b>{won_txt}{opp_txt}</div></div>''')

    # --- 2. Then the evidence: KPI telemetry strip + interactive charts ---
    section_head("Supporting Telemetry", "The Evidence", "Hover any chart for detail", SEC)
    gf_share = sdiv(s["GF"], s["GF"] + s["GA"]) * 100
    finishing = s["GF"] - s["xG"]
    cards = [
        kpi("Record / W-D-L", "trending_down" if s["W"] <= s["L"] else "trending_up", DANGER if s["W"] <= s["L"] else POS,
            f"{s['W']}-{s['D']}-{s['L']}", f"{s['pts']} Pts · {s['n']} fixtures", MUTED,
            f"PL: 13th · {PL_PTS} pts", DANGER, f'<span class="lbl">{s["win_pct"]:.1f}% Win</span>'),
        kpi("GF / GA (Diff)", "sports_score", DANGER if s["GD"] < 0 else POS, f"{s['GF']} / {s['GA']}",
            f"{signed(s['GD'], '{:+d}')} Net Goal Diff", POS if s["GD"] >= 0 else DANGER,
            f"{sdiv(s['GF'], s['n']):.2f} GF / match", MUTED,
            f'<div class="bar" style="width:3rem;"><div style="width:{gf_share:.0f}%;background:{POS};"></div><div style="width:{100 - gf_share:.0f}%;background:{DANGER};"></div></div>'),
        kpi("Created xG", "troubleshoot", RED, f"{s['xG']:.2f}", f"{signed(finishing)} goals vs xG", POS if finishing >= 0 else WARN,
            f"{sdiv(s['xG'], s['n']):.2f} xG / match", MUTED,
            f'<span class="lbl" style="color:{POS if finishing >= 0 else WARN};">{"Clinical" if finishing >= 0 else "Low Conv."}</span>', unit="xG"),
        kpi("Conceded xGA", "security", SEC, f"{s['xGA']:.2f}", f"{signed(over)} actual over xGA", DANGER if over > 0 else POS,
            f"{s['GA']} GA from {s['osot']} SoT", MUTED,
            f'<span class="lbl" style="color:{DANGER if over > 0 else POS};">{"Leaking" if over > 0 else "Solid"}</span>', unit="xGA"),
        kpi("Possession", "pie_chart", "#4edea3", f"{s['poss']:.1f}%", f"{sdiv(s['shots'], s['n']):.1f} shots / match", SEC,
            "Territorial control", MUTED, f'<span class="lbl" style="color:{SEC};">{sdiv(s["box"], s["n"]):.0f} box touches</span>'),
        kpi("Opp. SoT Conversion", "speed", WARN, f"{conv:.0f}%", f"{s['GA']} of {s['osot']} on target", DANGER if conv >= 30 else MUTED,
            f"Opp. shots {sdiv(s['oshots'], s['n']):.1f} / match", MUTED, '<span class="lbl">Clinical Opp.</span>'),
    ]
    H(f'<div class="grid g6 gsm" style="margin-top:1rem;">{"".join(cards)}</div>')
    st.write("")

    left, right = st.columns([5, 7], gap="large")
    with left:
        home, away = venue_stats(f, "Home"), venue_stats(f, "Away")
        legend = "".join(f'''<div class="row between" style="padding:0.4rem 0.5rem;border-radius:0.5rem;background:rgba(22,27,38,0.8);">
          <div class="row gx"><span class="dot" style="width:10px;height:10px;background:{c};"></span><span class="body-sm t" style="font-weight:500;">{lab}</span></div>
          <div class="row gs mono body-sm"><b style="color:{c if lab == 'Losses' else TEXT};">{v}</b><span class="lbl-sm">{sdiv(v, s['n']) * 100:.1f}%</span></div></div>'''
                         for lab, v, c in (("Wins", s["W"], POS), ("Draws", s["D"], WARN), ("Losses", s["L"], DANGER)))
        if home["n"] and away["n"]:
            venue = (f'Home: <b class="mono" style="color:{POS};">{home["ppm"]:.1f} Pts/Match</b> vs Away: '
                     f'<b class="mono" style="color:{DANGER};">{away["ppm"]:.1f} Pts/Match</b>')
        else:
            only = home if home["n"] else away
            venue = f'{"Home" if home["n"] else "Away"} only in scope: <b class="mono">{only["ppm"]:.1f} Pts/Match</b>'
        form_rows = list(f.sort_values("Date").itertuples())
        form = "".join(f'''<div class="col has-tt hov" style="align-items:center;gap:4px;background:rgba(22,27,38,0.9);border-radius:0.5rem;padding:0.5rem 0.25rem;">
          {tt(f"{esc(r.Opponent)} ({r.Venue})",
              [(res_letter(r.Result)[1], r.Result, f"{r.GF}–{r.GA}"), (RED_CORE, "xG", f"{r.xG:.2f}"), (rgba(SEC, 0.7), "Opponent xG", f"{r.xGA:.2f}"),
               (None, "Possession", f"{r.Possession}%"), (None, "Shots (on target)", f"{r.Shots} ({r.Shots_On_Target})")],
              note=f"{r.Competition} · {pd.to_datetime(r.Date).strftime('%d %b')}<br>{esc(r.Key_Context)}",
              align="l" if k < len(form_rows) / 2 else "r")}
          <span class="chip" style="min-width:1.5rem;height:1.5rem;padding:0;background:{rgba(res_letter(r.Result)[1], 0.2)};color:{res_letter(r.Result)[1]};">{res_letter(r.Result)[0]}</span>
          <span class="lbl" style="font-size:10px;">{COMP_ABBR[r.Competition]}</span>
          <span class="mono t" style="font-size:11px;">{r.GF}-{r.GA}</span>
          <span class="lbl" style="font-size:9px;">v {ABBR.get(r.Opponent, "")}</span></div>''' for k, r in enumerate(form_rows))
        H(f'''<div class="card" style="padding:1rem;">
        <div class="row between start gs"><div class="col"><span class="lbl">Match Outcomes &amp; Split</span>
        <div class="h-sm">{s['n']} Fixture Outcome Distribution</div></div>
        <span class="mono lbl-sm" style="background:{ELEV};padding:3px 10px;border-radius:9999px;color:{SEC};">{s['win_pct']:.1f}% Win Rate</span></div>
        <div class="row gm" style="background:rgba(22,27,38,0.4);padding:1rem;border-radius:0.75rem;margin-top:0.9rem;">{donut_svg(s['W'], s['D'], s['L'])}
        <div class="col gx grow">{legend}</div></div>
        <div class="row between" style="background:{ELEV};padding:0.6rem 0.75rem;border-radius:0.5rem;margin-top:0.9rem;">
        <div class="col"><span class="lbl">Home / Away Venue Asymmetry</span><span class="body-sm t">{venue}</span></div>{ico("stadium", 20, MUTED)}</div>
        <div class="col gx" style="margin-top:0.9rem;"><span class="lbl">Form Sequence · Chronological ({s['n']} fixtures)</span>
        <div class="grid" style="grid-template-columns:repeat({s['n']},minmax(0,1fr));gap:6px;">{form}</div></div></div>''')
    with right:
        rows = f.sort_values("Date")
        worst = rows.loc[(rows.xGA - rows.xG).idxmax()]
        pos_n = int((rows.xG > rows.xGA).sum())
        H(f'''<div class="card" style="padding:1rem;">
        <div class="row between wrap gs"><div class="col"><span class="lbl">Matchday Disparity Engine</span>
        <div class="h-sm">Match-by-Match xG Generated vs. xGA Conceded</div></div>
        <div class="row gs lbl wrap"><span class="row gx"><span style="width:12px;height:12px;border-radius:2px;background:{RED_CORE};"></span>MUFC xG</span>
        <span class="row gx"><span style="width:12px;height:12px;border-radius:2px;background:{rgba(SEC, 0.5)};"></span>Opponent xG</span>
        <span class="row gx"><span class="dot" style="width:8px;height:8px;background:{WARN};"></span>Goals scored</span></div></div>
        <div style="background:rgba(22,27,38,0.4);border-radius:0.75rem;padding:1rem;margin-top:0.9rem;">{xg_disparity_chart(f)}
        <div class="row between wrap gs lbl" style="padding-top:0.5rem;"><span>xG &gt; xGA in {pos_n} of {s['n']}</span>
        <span style="color:{RED};">*{ABBR.get(worst.Opponent)}: worst xG gap ({signed(worst.xG - worst.xGA)})</span>
        <span>Net xG diff {signed(s['xG'] - s['xGA'])}</span></div></div>
        <div class="row gs" style="background:rgba(22,27,38,0.7);padding:0.6rem 0.75rem;border-radius:0.5rem;margin-top:0.9rem;">
        {ico("warning", 20, WARN)}<span class="body-sm t">Chance-quality edge, results deficit: United out-created opponents by
        <b>{s['xG'] - s['xGA']:.2f} xG</b>, but opponents finished at <b>{sdiv(s['GA'], s['xGA']) * 100:.0f}%</b> of their expected goals.</span></div></div>''')

    st.write("")
    cta_tactics_board()

# ==============================================================================
# PAGE: MATCH RESULTS & FORM
# ==============================================================================
def page_match_results(f, s):
    tags = pill("Investigation Unit #02", RED, ping=True) + '<span class="lbl" style="opacity:0.7;margin-left:0.5rem;">Telemetry Track · 2026/27</span>'
    # header alert reflects the scope in view (before the outcome filter)
    late_share = sdiv(s["late_ga"], s["GA"])
    if s["GA"] and late_share >= 0.4:
        alert_t, alert_c = "Critical · Late-Game Leak", DANGER
    elif s["GA"] > s["xGA"] + 0.05:
        alert_t, alert_c = "Elevated · Conceding Above xGA", WARN
    else:
        alert_t, alert_c = "Stable in this scope", POS
    badges = f'''<div class="row gs wrap" style="align-self:flex-end;">
      <div class="row gs" style="background:{ELEV};padding:0.5rem 1rem;border-radius:0.5rem;">{ico("warning", 20, alert_c)}
      <div class="col"><span class="lbl">Alert Level</span><span class="mono body-sm" style="color:{alert_c};">{alert_t}</span></div></div>
      <div class="row gs" style="background:{ELEV};padding:0.5rem 1rem;border-radius:0.5rem;">{ico("radar", 20, SEC)}
      <div class="col"><span class="lbl">Sample Depth</span><span class="mono body-sm" style="color:{SEC};">{s['n'] * 90:,} mins / {s['n']} fixtures</span></div></div></div>'''
    inner = page_head(tags, "Matchday Log &amp; Form Dynamics",
                      "Fixture-by-fixture autopsy tracking xG differentials, home vs. away venue splits, and second-half game-state "
                      "management vulnerabilities across the opening six fixtures.", right_html=badges, banner=True)
    banner_open(inner)

    with st.container(key="bar_outcome"):
        b1, b2 = st.columns([3, 2], vertical_alignment="center")
        with b1:
            # Stable option values (counts live only in the display label) so a scope change never resets the control
            counts = {"All": s["n"], "Win": s["W"], "Draw": s["D"], "Loss": s["L"]}
            outcome = st.segmented_control("Outcome", list(counts), default="All", key="outcome",
                                           format_func=lambda o: f"{o} ({counts[o]})", label_visibility="collapsed") or "All"
        with b2:
            H(f'''<div class="row gm wrap lbl" style="justify-content:flex-end;"><span class="row gx"><span style="width:10px;height:10px;border-radius:2px;background:{rgba(DANGER, 0.8)};"></span>
            Finishing deficit (xG &gt; Opp but lost)</span><span class="row gx"><span style="width:10px;height:10px;border-radius:2px;background:{rgba(POS, 0.8)};"></span>Win</span></div>''')

    # The outcome filter drives every section below, not just the ledger
    n_scope = len(f)
    view_txt = f"{scope} · {plural(n_scope, 'fixture')}"
    if outcome != "All":
        word = {"Win": "wins", "Draw": "draws", "Loss": "losses"}[outcome]
        f = f[f.Result == outcome]
        if f.empty:
            st.info(f"No {word} in the current scope ({SCOPE_TXT}) — pick another outcome or widen the top-bar scope.")
            return
        s = team_stats(f)
        view_txt = f"{word.capitalize()}: {s['n']} of {plural(n_scope, 'fixture')} ({scope})"
        H(f'''<div class="row gs lbl" style="margin-top:0.25rem;">{ico("filter_alt", 16, SEC)}
        <span>Showing <b style="color:{SEC};">{word} only</b> · {s['n']} of {plural(n_scope, 'fixture')} in scope ({scope})</span></div>''')

    home, away = venue_stats(f, "Home"), venue_stats(f, "Away")
    lost_ids = [k for k in LEADS_LOST if k in set(f.Match_ID)]
    h1n, h2n = s["h1gf"] - s["h1ga"], s["h2gf"] - s["h2ga"]
    h1_share = sdiv(s["h1ga"], s["GA"]) * 100

    # --- 1. Summary first: the conclusion (reflects the outcome filter above) ---
    kicker, title, head, body, take, fx = match_conclusion(s, outcome, bool(lost_ids))
    section_head(kicker, title, "", RED)
    H(f'''<div class="card lg"><div class="h-lg">{head}</div>
    <div class="body-md" style="margin-top:0.75rem;max-width:64rem;line-height:1.7;">{fx}: {body}</div>
    <div class="body-md t" style="margin-top:0.6rem;max-width:64rem;line-height:1.7;">{take}</div>
    <div class="row gs" style="margin-top:1rem;">{pill("Tactical Lab Analyst", RED)}<span class="lbl-sm">Data: Opta / FotMob · {view_txt}</span></div></div>''')

    # --- 2. Then the evidence ---
    section_head("Supporting Telemetry", "The Evidence", "Hover any chart for detail", SEC)

    def venue_card(label, v, good):
        if not v["n"]:
            return f'<div class="card lg"><span class="lbl">{label}</span><div class="stat-xl m" style="margin-top:1rem;">—</div><span class="body-sm">Not in current scope</span></div>'
        c = POS if good else DANGER
        badge = (f'<span class="row gx lbl" style="color:{POS};background:{rgba(POS, 0.1)};padding:2px 8px;border-radius:4px;">{ico("trending_up", 14)} Positive</span>'
                 if good else f'<span class="row gx lbl" style="color:#fff;background:{DANGER};padding:2px 8px;border-radius:4px;box-shadow:0 0 12px rgba(239,68,68,0.5);">{ico("error", 14)} Critical</span>')
        return f'''<div class="card lg hov"><div class="row between gs"><span class="lbl">{label}</span>{badge}</div>
        <div class="row between" style="margin-top:1rem;align-items:flex-end;"><div class="col"><span class="stat-xl" style="color:{TEXT if good else DANGER};">{v["ppm"]:.2f}</span>
        <span class="body-sm">Points per match</span></div><div class="col" style="align-items:flex-end;">
        <span class="mono t" style="font-size:1.125rem;color:{TEXT if good else DANGER};">W{v["W"]} · D{v["D"]} · L{v["L"]}</span>
        <span class="lbl" style="color:{c};">{signed(v["gd"], "{:+d}")} Goal Diff</span></div></div>
        <div class="bar" style="margin-top:1rem;"><div style="width:{v["ppm"] / 3 * 100:.0f}%;background:{c};"></div></div></div>'''

    lead_rows = "".join(f'<div class="row between"><span class="lbl-sm">{LEADS_LOST[k][0]}</span><span class="mono lbl-sm t">{LEADS_LOST[k][1]}</span></div>'
                        for k in lost_ids) or '<span class="lbl-sm">None in scope</span>'
    cards = [
        venue_card("Home Baseline", home, home["ppm"] >= 1.5),
        venue_card("Away Field Resilience", away, away["ppm"] >= 1.5),
        f'''<div class="card lg hov"><div class="row between gs"><span class="lbl">Lead Surrender Deficit</span>
        <span class="lbl" style="color:{WARN};background:{rgba(WARN, 0.1)};padding:2px 8px;border-radius:4px;">Leads lost</span></div>
        <div class="row gs" style="margin-top:1rem;align-items:baseline;"><span class="stat-xl" style="color:{WARN};">{len(lost_ids)}</span>
        <span class="body-sm">fixtures led, not won</span></div>
        <div class="col gx" style="margin-top:0.4rem;">{lead_rows}</div>
        <div class="bar" style="margin-top:1rem;"><div style="width:{sdiv(len(lost_ids), s['n']) * 100:.0f}%;background:{WARN};"></div></div></div>''',
        f'''<div class="card lg hov"><div class="row between gs"><span class="lbl">Halves Disparity Metric</span>
        <span class="lbl" style="color:{DANGER};background:{rgba(DANGER, 0.1)};padding:2px 8px;border-radius:4px;">{signed(h2n - h1n, "{:+d}")} GD swing</span></div>
        <div class="row between" style="margin-top:1rem;"><div class="col"><span class="h-md" style="font-weight:700;color:{POS if h1n >= 0 else DANGER};">{signed(h1n, "{:+d}")} GD</span>
        <span class="lbl">1st Half ({s['h1gf']}-{s['h1ga']})</span></div><div style="height:2rem;width:1px;background:var(--highest);"></div>
        <div class="col" style="align-items:flex-end;"><span class="h-md" style="font-weight:700;color:{POS if h2n >= 0 else DANGER};">{signed(h2n, "{:+d}")} GD</span>
        <span class="lbl">2nd Half ({s['h2gf']}-{s['h2ga']})</span></div></div>
        <div class="bar" style="margin-top:1rem;"><div style="width:{h1_share:.0f}%;background:{POS};"></div><div style="width:{100 - h1_share:.0f}%;background:{DANGER};"></div></div></div>''',
    ]
    H(f'<div class="grid g4" style="margin-top:0.5rem;">{"".join(cards)}</div>')
    st.write("")

    left, right = st.columns([7, 5], gap="large")
    with left:
        def half_card(title, gf, ga, net, danger):
            tot = max(gf + ga, 1)
            card = tt(title, [(POS, "Goals scored", gf), (DANGER if danger else WARN, "Goals conceded", ga),
                              (None, "Net goal difference", signed(net, "{:+d}")),
                              (None, "Share of goals conceded", f"{sdiv(ga, s['GA']) * 100:.0f}%")],
                      note="Across the fixtures in the current scope", align="r" if danger else "l")
            card = card.replace('<div class="tt', '<div style="top:calc(100% + 6px);bottom:auto;" class="tt', 1)  # open below the tile
            return f'''<div class="has-tt hov" style="background:{ELEV};padding:1rem;border-radius:0.5rem;">{card}
            {'<div style="position:absolute;right:0;top:0;width:4rem;height:4rem;background:rgba(239,68,68,0.1);border-bottom-left-radius:9999px;border-top-right-radius:0.5rem;"></div>' if danger else ''}
            <div class="row between lbl"><span>{title}</span><span style="color:{POS if net >= 0 else DANGER};font-weight:700;">{signed(net, "{:+d}")} NET</span></div>
            <div class="row gs" style="margin-top:0.75rem;align-items:baseline;"><span class="mono h-md" style="font-weight:700;color:{POS};">{gf}</span>
            <span class="body-sm">Scored</span><span class="mono m" style="font-size:1.1rem;">/</span>
            <span class="mono h-md" style="font-weight:700;color:{DANGER if danger else TEXT};">{ga}</span><span class="body-sm">Conceded</span></div>
            <div class="bar" style="height:8px;margin-top:0.75rem;"><div style="width:{gf / tot * 100:.0f}%;background:{POS};"></div>
            <div style="width:{ga / tot * 100:.0f}%;background:{DANGER if danger else WARN};"></div></div></div>'''
        H(f'''<div class="card lg"><div class="row between start gs wrap"><div class="col"><span class="lbl" style="color:{RED};">Temporal Erosion Analysis</span>
        <div class="h-md" style="margin-top:0.25rem;">1st Half vs. 2nd Half Goal Distribution</div>
        <div class="body-sm" style="margin-top:0.25rem;">Late-game erosion: the opening-half edge disappears once legs tire and substitutions reshape the backline.</div></div>
        <span class="row gx lbl" style="background:{ELEV};padding:0.35rem 0.6rem;border-radius:0.25rem;"><span class="dot" style="width:8px;height:8px;background:{DANGER};"></span>
        {sdiv(s['late_ga'], s['GA']) * 100:.0f}% of GA after 60'</span></div>
        <div class="grid g2" style="margin-top:1.25rem;">{half_card("1st Half (1–45 min)", s['h1gf'], s['h1ga'], h1n, False)}{half_card("2nd Half (46–90+ min)", s['h2gf'], s['h2ga'], h2n, True)}</div>
        <div style="margin-top:1.25rem;background:rgba(11,14,20,0.6);padding:1rem;border-radius:0.5rem;">
        <div class="row between"><span class="lbl">Goals Conceded by Match Phase</span><span class="lbl" style="color:{DANGER};">{ico("trending_up", 14)} Late surge</span></div>
        {bucket_bars(s['buckets'], "10rem", s['bucket_goals'])}</div></div>''')
    with right:
        def vrow(label, hv, av, fmt, better_high):
            if not (home["n"] and away["n"]):
                val = hv if home["n"] else av
                return f'<div class="row between" style="padding:0.5rem 0;"><span class="body-sm t">{label}</span><span class="mono t">{fmt.format(val)}</span></div>'
            mx = max(hv, av, 1e-9)
            hg = (hv >= av) == better_high
            return f'''<div style="padding:0.55rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">
            <div class="row between"><span class="body-sm t">{label}</span><span class="mono body-sm"><b style="color:{POS if hg else DANGER};">{fmt.format(hv)}</b>
            <span class="m"> vs </span><b style="color:{DANGER if hg else POS};">{fmt.format(av)}</b></span></div>
            <div class="bar" style="height:4px;margin-top:6px;background:transparent;gap:3px;"><div style="width:{hv / mx * 50:.0f}%;background:{SEC};border-radius:9999px;"></div></div>
            <div class="bar" style="height:4px;margin-top:3px;background:transparent;"><div style="width:{av / mx * 50:.0f}%;background:{rgba(MUTED, 0.5)};border-radius:9999px;"></div></div></div>'''
        body = "".join([
            vrow("Goals for / match", home["gf"], away["gf"], "{:.2f}", True),
            vrow("Goals against / match", home["ga"], away["ga"], "{:.2f}", False),
            vrow("xG / match", home["xg"], away["xg"], "{:.2f}", True),
            vrow("xGA / match", home["xga"], away["xga"], "{:.2f}", False),
            vrow("Possession %", home["poss"], away["poss"], "{:.1f}", True),
            vrow("Shots / match", home["shots"], away["shots"], "{:.1f}", True),
        ])
        venue_note = ""
        if away["n"]:
            away_rec = "are yet to win" if away["W"] == 0 else f"have won {away['W']}"
            venue_note = (f'<div class="row gs" style="margin-top:1rem;background:rgba(239,68,68,0.08);padding:0.6rem 0.75rem;border-radius:0.5rem;">'
                          f'{ico("error", 18, DANGER)}<span class="body-sm t"><b>Road record:</b> away from home United scored '
                          f'{away["gf"] * away["n"]:.0f} in {away["n"]} and {away_rec}.</span></div>')
        H(f'''<div class="card lg"><div class="row between"><span class="lbl" style="color:{SEC};">Venue Breakdown Matrix</span>
        <span class="row gs lbl"><span class="row gx"><span class="dot" style="background:{SEC};"></span>Home</span><span class="row gx"><span class="dot" style="background:{MUTED};"></span>Away</span></span></div>
        <div class="h-md" style="margin-top:0.25rem;">Home vs. Away Matrix</div>
        <div class="body-sm" style="margin-top:0.25rem;">Per-match averages at Old Trafford vs. on the road ({home['n']} home · {away['n']} away).</div>
        <div style="margin-top:0.75rem;">{body}</div>
        {venue_note}</div>''')

    # --- Forensic ledger ---
    st.write("")
    with st.container(key="card_ledger"):
        l1, l2 = st.columns([3, 1.3], vertical_alignment="center")
        with l1:
            H(f'''<div class="row gs">{ico("table_chart", 22, RED)}<div class="col"><div class="h-sm">Matchday Forensic Ledger (MD 1–6)</div>
            <span class="body-sm">Granular event metrics, tactical xG shifts and critical phase breakdowns for every fixture.</span></div></div>''')
        with l2:
            q = st.text_input("Search", "", placeholder="Search opponent…", key="ledger_q", label_visibility="collapsed")
        g = f.sort_values("Date")
        if q:
            g = g[g.Opponent.str.contains(q, case=False) | g.Competition.str.contains(q, case=False)]
        rows = []
        for r in g.itertuples():
            letter, c = res_letter(r.Result)
            deficit = r.xG > r.xGA and r.Result == "Loss"
            diff = r.xG - r.xGA
            rows.append(f'''<tr class="{'warnrow' if deficit else ''}">
            <td class="mono m">#{r.Seq:02d}</td><td class="mono m" style="white-space:nowrap;">{pd.to_datetime(r.Date).strftime('%d %b')}</td>
            <td><div class="t" style="font-weight:600;">{esc(r.Opponent)}</div><div class="lbl" style="font-size:10px;">{COMP_ABBR[r.Competition]} · {esc(r.Opponent_Category)}</div></td>
            <td class="mono">{r.Venue[0]}</td>
            <td><span class="chip" style="background:{rgba(c, 0.18)};color:{c};">{letter} {r.GF}–{r.GA}</span></td>
            <td class="n"><span class="mono" style="color:{POS if diff >= 0 else DANGER};">{r.xG:.2f} – {r.xGA:.2f}</span><div class="lbl" style="font-size:10px;">{signed(diff)} delta</div></td>
            <td class="n mono">{r.Shots} ({r.Shots_On_Target})</td><td class="n mono">{r.Opp_Shots} ({r.Opp_Shots_On_Target})</td>
            <td class="n mono">{r.Possession}%</td><td class="n mono">{r.Pass_Accuracy}%</td>
            <td class="body-sm" style="min-width:16rem;color:{DANGER if deficit else MUTED};">{esc(r.Key_Context)}</td></tr>''')
        body = "".join(rows) or '<tr><td colspan="11" class="m">No fixtures match this outcome / search.</td></tr>'
        H(f'''<div class="tbl-wrap"><table class="tbl"><thead><tr><th>MD</th><th>Date</th><th>Opponent &amp; Context</th><th>Ven</th><th>Score</th>
        <th class="n">xG – xGA</th><th class="n">Shots (SoT)</th><th class="n">Opp (SoT)</th><th class="n">Poss</th><th class="n">Pass</th><th>Tactical Diagnostic Note</th></tr></thead>
        <tbody>{body}</tbody></table></div>''')
        worst = f.loc[(f.xGA - f.xG).idxmax()]
        gap = worst.xG - worst.xGA
        if gap < 0:  # an actual chance-quality deficit exists in the filtered sample
            c, icon, head = DANGER, "crisis_alert", f"Forensic insight: {esc(worst.Opponent)} ({worst.Venue[0]}) — turning point."
            note = f"The widest chance-quality deficit in this view ({signed(gap)} xG):"
        else:       # e.g. "Win" filter: no fixture where United were out-created
            both = "this fixture" if len(f) == 1 else ("both fixtures" if len(f) == 2 else f"all {len(f)} fixtures")
            c, icon, head = POS, "verified", f"Forensic insight: United had the better chances in {both}."
            note = (f"Match note ({esc(worst.Opponent)}, {signed(gap)} xG):" if len(f) == 1 else
                    f"Narrowest xG margin was {esc(worst.Opponent)} ({worst.Venue[0]}, {signed(gap)} xG):")
        H(f'''<div class="row between wrap gs" style="background:{rgba(c, 0.08)};padding:0.75rem 1rem;border-radius:0.5rem;box-shadow:inset 3px 0 0 {c};">
        <div class="row gs">{ico(icon, 20, c)}<span class="body-sm t"><b>{head}</b> {note} {esc(worst.Key_Context)}</span></div></div>''')


# ==============================================================================
# PAGE: ATTACKING ANALYTICS
# ==============================================================================
def page_attacking(f, s):
    tags = pill("Dossier Module 02 // Attacking Teardown", RED, ping=True) + '<span class="lbl" style="margin-left:0.5rem;">Analytics Rigor: Opta / FotMob</span>'
    right = f'''<div class="row gs" style="background:{ELEV};padding:0.6rem 0.9rem;border-radius:0.5rem;align-self:flex-end;">
      {ico("filter_alt", 18, SEC)}<div class="col"><span class="lbl">Scope</span><span class="mono body-sm" style="color:{SEC};">{SCOPE_TXT}</span></div></div>'''
    page_head(tags, "Offensive Stagnation &amp; Shot Quality Bottleneck",
              f"High territorial possession ({s['poss']:.1f}%) and heavy shot volume mask a front line that goes silent whenever "
              "low blocks take away Bruno Fernandes' central pocket.", right_html=right)
    # --- 1. Summary first: how the attack fails ---
    section_head("Tactical Diagnostics", "Attacking Pattern Failure Modes", "", RED)
    modes = [
        ("01", "Dependency index: 38.5%", RED, "Bruno-Centric Creation Funnel",
         "Nearly every attack runs through Bruno. With spatial freedom (hat-trick vs Ipswich) United's xG reaches elite levels (4.77); when low blocks restrict Bruno's central space the attack stalls.",
         [("Bruno G+A", "4G · 1A"), ("Next best", "Mbeumo 2G · 1A")], "Tactical remedy: second creator in half-spaces"),
        ("02", "Blank games: 2", WARN, "Low-Block Sterility",
         "Against Hull and 10-man City United combined 33 shots and 11 corners for zero goals — possession recycled wide without penetrating the six-yard box.",
         [("Hull (A)", "21 shots · 0 G"), ("City (H)", "12 shots · 0 G")], "Tactical remedy: earlier box occupation"),
        ("03", "Role friction", PASS, "Cunha / Šeško Integration",
         "Cunha (5 starts) drops deep to link with Bruno, reducing box presence; Šeško (2 starts) offers a real target but limits press resistance. The dual-forward setup worked vs Sabah.",
         [("Cunha", "1G 1A in 5 starts"), ("Šeško", "2G in 2 starts")], "Tactical remedy: fixed box striker"),
    ]
    H('<div class="grid g3">' + "".join(f'''<div class="card col between" style="padding:1.25rem;">
      <div><div class="row between"><span class="mono lbl-sm" style="background:{ELEV};padding:2px 8px;border-radius:4px;">{n}</span>{pill(tag, c)}</div>
      <div class="h-sm" style="margin-top:0.6rem;font-weight:700;">{t}</div><div class="body-sm" style="margin-top:0.4rem;line-height:1.65;">{d}</div>
      <div class="col gx" style="margin-top:0.75rem;background:{ELEV};padding:0.6rem 0.75rem;border-radius:0.5rem;">
      {''.join(f'<div class="row between"><span class="lbl-sm">{a}</span><span class="mono body-sm" style="color:{c};">{b}</span></div>' for a, b in stats)}</div></div>
      <div class="row gx lbl" style="margin-top:0.9rem;color:{c};">{ico("tips_and_updates", 16, c)}{rem}</div></div>''' for n, tag, c, t, d, stats, rem in modes) + '</div>')

    # --- 2. Then the evidence ---
    section_head("Supporting Telemetry", "The Evidence", "Hover any chart for detail", SEC)
    xg_shot = sdiv(s["xG"], s["shots"])
    acc = sdiv(s["sot"], s["shots"]) * 100
    fin = s["GF"] - s["xG"]
    cards = [
        kpi("Total Shots", "my_location", SEC, f"{s['shots']}", f"{sdiv(s['shots'], s['n']):.1f} per match", SEC,
            f"On target: {s['sot']}", MUTED, f'<span class="lbl" style="color:{POS};">{acc:.1f}%</span>', unit=f"/ {s['n']} GP"),
        kpi("Goals Scored", "sports_score", RED, f"{s['GF']}", f"vs {s['xG']:.2f} xG ({signed(fin)})", POS if fin >= 0 else WARN,
            f"{sdiv(s['GF'], s['n']):.2f} per match", MUTED, ""),
        kpi("xG per Shot", "warning", WARN, f"{xg_shot:.3f}", "Chance quality per attempt", MUTED,
            f"{sdiv(s['shots'], max(s['GF'], 1)):.1f} shots per goal", MUTED, ""),
        kpi("Box Touches", "crop_square", SEC, f"{sdiv(s['box'], s['n']):.1f}", "per match", MUTED,
            f"Total {s['box']}", MUTED, f'<span class="lbl">{s["corners"]} corners</span>', unit="/ GP"),
        kpi("Shot Accuracy", "swap_horiz", WARN, f"{acc:.1f}%", f"{s['sot']} of {s['shots']} on target", WARN if acc < 35 else POS,
            "SoT → goal", MUTED, f'<span class="lbl" style="color:{POS};">{sdiv(s["GF"], s["sot"]) * 100:.0f}%</span>'),
    ]
    H(f'<div class="grid g5 gsm">{"".join(cards)}</div>')
    st.write("")

    left, right = st.columns([8, 4], gap="large")
    g = f.sort_values("Date")
    labels = [ABBR.get(o, o[:3].upper()) for o in g.Opponent]
    with left:
        with st.container(key="card_shotvol"):
            H(f'''<div class="row between start wrap gs"><div class="col"><span class="lbl" style="color:{SEC};">Timeline Telemetry · {s['n']} fixtures</span>
            <div class="h-md">Shot Volume vs. Shot Quality (xG) Evolution</div></div>
            <div class="row gx lbl" style="background:{ELEV};padding:0.35rem 0.6rem;border-radius:0.25rem;">Bars: shots · <span style="color:{RED};">red = 2+ xG</span></div></div>''')
            fig = go.Figure()
            fig.add_trace(go.Bar(x=labels, y=g.Shots, name="Total shots", marker_color=[RED_CORE if v >= 2 else "#32353c" for v in g.xG],
                                 customdata=g.Opponent, hovertemplate="<b>%{customdata}</b><br>Shots: %{y}<extra></extra>"))
            fig.add_trace(go.Scatter(x=labels, y=g.xG, name="Match xG", yaxis="y2", mode="lines+markers",
                                     line=dict(color=PASS, width=3), marker=dict(size=7),
                                     hovertemplate="xG: %{y:.2f}<extra></extra>"))
            fig.add_trace(go.Scatter(x=labels, y=g.GF, name="Goals", yaxis="y2", mode="lines+markers",
                                     line=dict(color=DANGER, width=2, dash="dot"), marker=dict(size=8, symbol="x"),
                                     hovertemplate="Goals: %{y}<extra></extra>"))
            style_chart(fig, 330)
            fig.update_layout(yaxis=dict(title=None, rangemode="tozero"),
                              yaxis2=dict(overlaying="y", side="right", showgrid=False, rangemode="tozero",
                                          tickfont=dict(size=11, color=PASS), zeroline=False))
            st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG, key="att_combo")
            blank = f[(f.Opponent.isin(["Hull City", "Manchester City"]))]
            if len(blank):
                H(f'''<div class="row between wrap gs" style="background:rgba(22,27,38,0.7);padding:0.6rem 0.75rem;border-radius:0.5rem;">
                <div class="row gs">{ico("troubleshoot", 20, RED)}<span class="body-sm t"><b>Forensic anomaly:</b> vs {" &amp; ".join(ABBR[o] for o in blank.Opponent)}
                United took <b>{int(blank.Shots.sum())} shots</b> ({blank.xG.sum():.2f} xG) and scored <b style="color:{DANGER};">{int(blank.GF.sum())}</b>.</span></div>
                <span class="lbl" style="color:{WARN};">Bruno held to 0 G/A</span></div>''')
    with right:
        H(f'''<div class="card" style="padding:1.25rem;"><div class="row between"><span class="row gx lbl" style="color:{RED};">{ico("gavel", 16, RED)}Technical Verdict</span>
        <span class="mono lbl-sm">SEC-02A</span></div>
        <div style="margin-top:0.75rem;height:7rem;border-radius:0.5rem;position:relative;overflow:hidden;background:radial-gradient(circle at 30% 20%, rgba(255,45,59,0.25), transparent 60%), linear-gradient(160deg,#1B2232,#0B0E14);">
        <div style="position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0 22px,rgba(255,255,255,0.03) 22px 44px);"></div>
        <div style="position:absolute;left:0.75rem;bottom:0.6rem;" class="row gs"><span class="lbl t">Old Trafford Telemetry</span><span class="lbl" style="color:{SEC};">xG Bottleneck</span></div></div>
        <div class="h-sm" style="margin-top:0.9rem;font-weight:700;">The Illusion of Dominance: {s['poss']:.0f}% Possession, {s['GF']} Goals</div>
        <div class="body-sm" style="margin-top:0.5rem;line-height:1.7;">United's possession structure establishes sustained presence in the final third
        ({sdiv(s['box'], s['n']):.0f} box touches per match), but output collapses once opponents retreat into a low block. The 5-2 and 4-0 wins
        ({f[f.GF >= 4].xG.sum():.2f} xG combined) carry the attacking totals.</div>
        <div class="col gx" style="margin-top:0.9rem;background:{ELEV};padding:0.6rem 0.75rem;border-radius:0.5rem;">
        <div class="row between"><span class="lbl-sm">Goals from 4+ goal games</span><span class="mono body-sm" style="color:{WARN};">{int(f[f.GF >= 4].GF.sum())} of {s['GF']}</span></div>
        <div class="row between"><span class="lbl-sm">Shots per goal</span><span class="mono body-sm" style="color:{WARN};">{sdiv(s['shots'], max(s['GF'], 1)):.1f}</span></div></div></div>''')
        funnel = [("Shots", s["shots"], "#32353c"), ("On target", s["sot"], PASS), ("Goals", s["GF"], RED_CORE)]
        mx = max(s["shots"], 1)
        H(f'''<div class="card" style="margin-top:1rem;padding:1.25rem;"><div class="row gs">{ico("filter_list", 20, RED)}
        <div class="col"><span class="lbl">Conversion Funnel</span><span class="h-sm" style="font-size:1.05rem;">{sdiv(s['GF'], s['shots']) * 100:.1f}% shots → goals</span></div></div>
        <div class="col gs" style="margin-top:0.75rem;">{''.join(f'<div><div class="row between lbl-sm"><span>{lab}</span><b class="mono">{v}</b></div><div class="bar" style="height:8px;margin-top:4px;"><div style="width:{v / mx * 100:.0f}%;background:{c};"></div></div></div>' for lab, v, c in funnel)}</div></div>''')

    # --- Goal contributor matrix ---
    section_head("Personnel Metric Breakdown", "Goal Contributor Matrix &amp; Finishing Efficiency", "Season totals · all competitions", SEC)
    p = df_players[(df_players.Goals + df_players.Assists > 0) | (df_players.xG_Contrib >= 1.0)].copy()
    p["GA_"] = p.Goals + p.Assists
    p = p.sort_values(["GA_", "xG_Contrib"], ascending=False)
    team_goals = int(df_matches.GF.sum())
    rows = []
    for r in p.itertuples():
        delta = r.GA_ - r.xG_Contrib
        share = sdiv(r.GA_, team_goals) * 100
        rows.append(f'''<tr><td><div class="row gs"><span class="chip" style="min-width:2rem;background:{ELEV};color:{MUTED};font-size:11px;">{r.Pos.split('/')[0]}</span>
        <div class="col"><span class="t" style="font-weight:600;">{esc(r.Player)}</span><span class="lbl" style="font-size:10px;letter-spacing:0.06em;">{esc(r.Primary_Role)}</span></div></div></td>
        <td class="n mono">{r.Goals}</td><td class="n mono">{r.Assists}</td><td class="n mono">{r.xG_Contrib:.1f}</td>
        <td class="n mono" style="color:{POS if delta >= 0 else DANGER};">{signed(delta, '{:+.1f}')}</td><td class="n mono">{r.Mins}</td>
        <td class="n mono" style="color:{SEC};">{sdiv(r.GA_ * 90, r.Mins):.2f}</td>
        <td style="min-width:10rem;"><div class="row gs"><div class="bar grow"><div style="width:{share:.0f}%;background:{RED};"></div></div><span class="mono lbl-sm">{share:.0f}%</span></div></td></tr>''')
    H(f'''<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Attacker</th><th class="n">Goals</th><th class="n">Ast</th><th class="n">xG contrib</th>
    <th class="n">Delta (G+A − xG)</th><th class="n">Mins</th><th class="n">G+A / 90</th><th>G+A share of team goals</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>''')
    H(f'''<div class="row gs" style="margin-top:0.75rem;background:rgba(239,68,68,0.08);padding:0.75rem 1rem;border-radius:0.5rem;">{ico("crisis_alert", 20, DANGER)}
    <span class="body-sm t"><b>Creator-dependency paradox:</b> Bruno Fernandes has 5 direct goal contributions (38.5% of United's {team_goals} goals); no other player has more than 3.</span></div>''')


# ==============================================================================
# PAGE: DEFENSIVE & TRANSITION
# ==============================================================================
def page_defensive(f, s):
    tags = pill("Dossier Module 03 // Defensive Telemetry", RED, ping=True) + f'<span class="lbl" style="color:{RED};margin-left:0.5rem;">Priority Critical Risk</span>'
    # Read-only scope badge (same as Attacking) — not a control
    right = f'''<div class="row gs" style="background:{ELEV};padding:0.6rem 0.9rem;border-radius:0.5rem;align-self:flex-end;">
      {ico("filter_alt", 18, SEC)}<div class="col"><span class="lbl">Scope</span><span class="mono body-sm" style="color:{SEC};">{SCOPE_TXT}</span></div></div>'''
    page_head(tags, "Defensive &amp; Transition Deficiencies",
              "Empirical dissection of transition fragility, rest-defense exposure and the late-match goal concession pattern across the "
              "opening fixtures.", right_html=right)
    over = s["GA"] - s["xGA"]
    conv = sdiv(s["GA"], s["osot"]) * 100
    # --- 1. Summary first: the root causes ---
    section_head("Diagnostic Deep-Dive", "Three Structural Root Causes", "Phase Analysis: Defensive Organisation", RED)
    factors = [
        ("Factor 01", RED, "open_in_full", "Rest Defense Defects",
         "Advancing full-backs (Shaw, Dorgu, Dalot) into a 5-man front leaves the double pivot (Tielemans + Mainoo/Santos) covering huge lateral ground. Opponents exploit vacant half-spaces on turnovers.",
         [("Opp. shots vs Everton / Brighton", "18 · 18")], ("Opp. SoT conversion", f"{conv:.0f}%")),
        ("Factor 02", WARN, "personal_injury", "Key Injury Absences",
         "Carlos Baleba & Manuel Ugarte leave no pure physical DM destroyer to break up counters; Matthijs de Ligt's back injury means young Heaven / Yoro partner Maguire / Martínez.",
         [("Destroyers unavailable", "2"), ("Young CBs started", "Heaven 2 · Yoro 2")], ("Rotation cost", "High")),
        ("Factor 03", PASS, "shield", "Set-Piece Zonal Screen Failure",
         "Zonal-marking disconnects: 2 set-piece goals at Hull, a scramble vs Ipswich and a late cross at Everton. No clear second-ball clearing assignments in box scrambles.",
         [("Hull (A)", "17' corner · 38' FK"), ("Late scrambles", "IPS 91' · EVE 96'")], ("Set-piece-phase goals", f"{s['sp_ga']} of {s['GA']}")),
    ]
    H('<div class="grid g3">' + "".join(f'''<div class="card lg col between">
      <div><div class="row between">{pill(tag, c)}{ico(i, 20, c)}</div><div class="h-sm" style="margin-top:0.6rem;font-weight:700;">{t}</div>
      <div class="body-sm" style="margin-top:0.4rem;line-height:1.65;">{d}</div>
      <div class="col gx" style="margin-top:0.9rem;background:{ELEV};padding:0.6rem 0.75rem;border-radius:0.5rem;">
      {''.join(f'<div class="row between"><span class="lbl-sm">{a}</span><span class="mono body-sm">{b}</span></div>' for a, b in rows)}</div></div>
      <div class="row between" style="margin-top:1rem;"><span class="lbl">{fl}</span><span class="mono lbl-sm" style="color:{c};font-weight:700;">{fv}</span></div></div>'''
                                     for tag, c, i, t, d, rows, (fl, fv) in factors) + '</div>')

    # --- 2. Then the evidence ---
    section_head("Supporting Telemetry", "The Evidence", "Hover any chart for detail", SEC)
    cards = [
        kpi("Goals Conceded", "sports_score", RED, f"{s['GA']}", f"{sdiv(s['GA'], s['n']):.2f} / match", DANGER,
            f"Clean sheets: {int((f.GA == 0).sum())}", MUTED, "", edge=RED),
        kpi("xGA Conceded", "monitoring", WARN, f"{s['xGA']:.2f}", f"{signed(over)} actual vs xGA", DANGER if over > 0 else POS,
            "Finishing vs United", MUTED, f'<span class="lbl" style="color:{WARN};">{"Punished" if over > 0 else "Fair"}</span>', edge=WARN),
        kpi("Opp. Shots", "speed", SEC, f"{sdiv(s['oshots'], s['n']):.1f}", "per match", SEC,
            f"Total {s['oshots']} ({s['osot']} on target)", MUTED, "", edge=SEC),
        kpi("Opp. SoT Conversion", "bolt", DANGER, f"{conv:.0f}%", f"{s['GA']} goals / {s['osot']} SoT", DANGER,
            "Clinical against United", MUTED, "", edge=DANGER),
        kpi("Goals Min 61–90+", "hourglass_bottom", RED, f"{s['late_ga']}", f"of {s['GA']} ({sdiv(s['late_ga'], s['GA']) * 100:.0f}%)", RED,
            "Collapse vector", MUTED, f'<span class="lbl" style="color:{RED};">Late surge</span>', unit=f"/{s['GA']}", edge=RED),
    ]
    H(f'<div class="grid g5 gsm">{"".join(cards)}</div>')
    st.write("")

    left, right = st.columns([7, 5], gap="large")
    with left:
        g = f.sort_values("Date")
        mx = max(int(g.Opp_Shots.max()), 1)
        g_rows = list(g.itertuples())
        bars = "".join(f'''<div class="grp has-tt">{tt(f"{esc(r.Opponent)} ({r.Venue[0]}) · {COMP_ABBR[r.Competition]}",
            [(rgba(PASS, 0.6), "Opponent shots", r.Opp_Shots), (WARN, "On target", r.Opp_Shots_On_Target), (DANGER, "Goals conceded", r.GA),
             (None, "SoT conversion", f"{sdiv(r.GA, r.Opp_Shots_On_Target) * 100:.0f}%" if r.Opp_Shots_On_Target else "—"),
             (None, "xGA", f"{r.xGA:.2f}")], note=esc(r.Key_Context), align="l" if k < len(g_rows) / 2 else "r", top=True)}
          <div class="bars"><div class="b" style="height:{r.Opp_Shots / mx * 100:.0f}%;background:{rgba(PASS, 0.45)};"></div>
          <div class="b" style="height:{r.Opp_Shots_On_Target / mx * 100:.0f}%;background:{WARN};"></div>
          <div class="b" style="height:{max(r.GA / mx * 100, 1):.0f}%;background:{DANGER};"></div></div>
          <span class="x">{ABBR.get(r.Opponent)}</span></div>''' for k, r in enumerate(g_rows))
        grid = "".join(f"<div>{v}&nbsp;</div>" for v in (mx, round(mx * 2 / 3), round(mx / 3), 0))
        ga_shot, xga_shot = sdiv(s["GA"], s["oshots"]), sdiv(s["xGA"], s["oshots"])
        H(f'''<div class="card lg"><div class="row between start wrap gs"><div class="col"><span class="lbl">Spatial Threat Matrix</span>
        <div class="h-md">Opponent Shots vs. Goals Conceded</div></div>
        <span class="mono lbl-sm" style="background:{ELEV};padding:0.35rem 0.6rem;border-radius:0.25rem;color:{SEC};">{s['oshots']} shots analysed</span></div>
        <div class="body-sm" style="margin-top:0.35rem;">Opponents need very few shots: low volume against United still turns into goals at an elite rate.</div>
        <div class="row gs lbl wrap" style="margin-top:0.75rem;"><span class="row gx"><span style="width:10px;height:10px;border-radius:2px;background:{rgba(PASS, 0.45)};"></span>Opp shots</span>
        <span class="row gx"><span style="width:10px;height:10px;border-radius:2px;background:{WARN};"></span>On target</span>
        <span class="row gx"><span style="width:10px;height:10px;border-radius:2px;background:{DANGER};"></span>Goals</span></div>
        <div style="background:rgba(11,14,20,0.6);border-radius:0.75rem;padding:0.5rem 0.75rem;margin-top:0.5rem;"><div class="chart" style="height:13rem;"><div class="gridl">{grid}</div>{bars}</div></div>
        <div class="grid g2" style="margin-top:1rem;background:rgba(22,27,38,0.5);padding:0.75rem;border-radius:0.5rem;">
        <div><span class="lbl">Goals per opp. shot</span><div class="row gs" style="align-items:baseline;"><span class="h-sm mono" style="color:{RED};font-weight:700;">{ga_shot:.3f}</span>
        <span class="lbl-sm" style="color:{RED};">{signed(sdiv(ga_shot - xga_shot, xga_shot) * 100, '{:+.0f}')}% vs xGA</span></div>
        <div class="bar" style="margin-top:6px;"><div style="width:{min(ga_shot / 0.2 * 100, 100):.0f}%;background:{RED};"></div></div></div>
        <div><span class="lbl">xGA per opp. shot</span><div class="row gs" style="align-items:baseline;"><span class="h-sm mono" style="font-weight:700;">{xga_shot:.3f}</span>
        <span class="lbl-sm">Expected</span></div><div class="bar" style="margin-top:6px;"><div style="width:{min(xga_shot / 0.2 * 100, 100):.0f}%;background:{PASS};"></div></div></div></div></div>''')
    with right:
        H(f'''<div class="card lg"><div class="row between"><span class="lbl" style="color:{RED};">Temporal Vulnerability</span>{ico("trending_up", 22, RED)}</div>
        <div class="h-md">The 60–90' Match Collapse</div>
        <div class="body-sm" style="margin-top:0.35rem;">Chronological breakdown of goals conceded by match phase.</div>
        <div style="margin-top:1rem;">{bucket_bars(s['buckets'], "13rem", s['bucket_goals'])}</div>
        <div class="row start gs" style="margin-top:1.25rem;background:rgba(22,27,38,0.7);padding:0.75rem;border-radius:0.5rem;">{ico("warning", 18, DANGER)}
        <span class="body-sm t"><b>Decisive pattern:</b> {s['late_ga']} of {s['GA']} goals arrive after the hour — including 83', 90+1' and 90+6' —
        as physical drop-off and substitutions disrupt zonal communication.</span></div></div>''')

    section_head("Player Exposure Telemetry", "Late Concession Timeline &amp; Defensive Unit Matrix", "Season totals")
    timeline = [
        (1, "Hull City (A)", "17' & 38'", "Set-Piece Breakdown", "Conceded twice early; lost 0-2", "Critical", DANGER),
        (2, "Ipswich Town (H)", "90+1'", "Late Defensive Scramble", "Conceded late; won 5-2", "Moderate", PASS),
        (3, "Everton (A)", "83' & 90+6'", "Rest Defense Collapse", "Surrendered 2-1 lead; drew 2-2", "Critical", DANGER),
        (6, "Brighton (H)", "45', 65', 70'", "Midfield Distance Separation", "Blew 2-0 lead; lost 2-3", "High", WARN),
    ]
    ids = set(f.Match_ID)
    trows = "".join(f'''<tr><td><div class="row gs"><span class="dot" style="background:{c};"></span><b>{fx}</b></div></td>
      <td class="mono" style="color:{c};">{mn}</td><td>{ty}</td><td class="m">{im}</td>
      <td><span class="chip" style="background:{rgba(c, 0.15)};color:{c};font-size:10px;letter-spacing:0.1em;text-transform:uppercase;">{rk}</span></td></tr>'''
                    for mid, fx, mn, ty, im, rk, c in timeline if mid in ids) or '<tr><td colspan="5" class="m">No late concessions in current scope.</td></tr>'
    H(f'''<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Fixture</th><th>Minute(s)</th><th>Breakdown Type</th><th>Impact</th><th>Risk</th></tr></thead>
    <tbody>{trows}</tbody></table></div>''')
    d = df_players[df_players.Pos.map(pos_group).isin(["DEF", "GK"]) | df_players.Pos.str.startswith("DM") | df_players.Pos.str.startswith("CM/DM")]
    d = d.sort_values("Mins", ascending=False)
    drows = "".join(f'''<tr><td><div class="row gs"><span class="dot" style="background:{DANGER if r.Yel >= 2 else (WARN if r.Yel else POS)};"></span><b>{esc(r.Player)}</b></div></td>
      <td class="m">{esc(r.Primary_Role)}</td><td class="n mono">{r.Apps} ({r.Starts})</td><td class="n mono">{r.Mins}</td>
      <td class="n mono" style="color:{WARN if r.Yel else MUTED};">{r.Yel}</td><td class="n mono">{r.Goals + r.Assists}</td>
      <td class="body-sm m" style="min-width:16rem;">{esc(r.Tactical_Impact)}</td></tr>''' for r in d.itertuples())
    H(f'''<div class="tbl-wrap" style="margin-top:1rem;"><table class="tbl"><thead><tr><th>Player</th><th>Role</th><th class="n">Apps (St)</th><th class="n">Mins</th>
    <th class="n">Yellows</th><th class="n">G+A</th><th>Tactical Note</th></tr></thead><tbody>{drows}</tbody></table></div>''')
    st.write("")
    cta_tactics_board()

# ==============================================================================
# PAGE: PLAYER PERFORMANCE MATRIX
# ==============================================================================
def page_players(f, s):
    tags = pill("Dossier Module 05 // Squad Telemetry", RED, ping=True)
    right = f'''<div class="row gs" style="background:{ELEV};padding:0.6rem 0.9rem;border-radius:0.5rem;align-self:flex-end;">
      <div class="col" style="align-items:flex-end;"><span class="lbl">Squad Sampling</span><span class="mono body-sm" style="color:{SEC};">6 fixtures · {MAX_MINS} max mins</span></div>{ico("monitoring", 22, SEC)}</div>'''
    page_head(tags, "Player Performance &amp; Tactical Load Matrix",
              "Individual output metrics, tactical role fulfilment and minutes-load telemetry mapped across the 22-man matchday rotation.",
              right_html=right)
    # --- 1. Summary first: three squad findings (computed from the season totals) ---
    top_load = df_players.loc[df_players.Mins.idxmax()]
    team_goals = int(df_matches.GF.sum())
    bruno = df_players[df_players.Player == "Bruno Fernandes"].iloc[0]
    engine = df_players[df_players.Pos.map(pos_unit) == "Midfield Engine"]
    findings = [
        (WARN, "monitor_heart", f"{top_load.Mins / MAX_MINS * 100:.0f}%", "Heaviest minutes load",
         f"{esc(top_load.Player)} has played {top_load.Mins} of {MAX_MINS} available minutes ({esc(top_load.Primary_Role)}), the biggest physical load in the squad."),
        (RED, "hub", f"{sdiv(bruno.Goals + bruno.Assists, team_goals) * 100:.1f}%", "Creator dependency",
         f"Bruno Fernandes has {bruno.Goals} goals and {bruno.Assists} assist{'s' if bruno.Assists != 1 else ''} of United's {team_goals} goals; no one else has more than "
         f"{int((df_players.Goals + df_players.Assists)[df_players.Player != 'Bruno Fernandes'].max())} goal contributions."),
        (SEC, "sports_soccer", f"{int(engine.Goals.sum())} goals", "Midfield engine output",
         f"The central midfielders ({', '.join(esc(n.split()[-1]) for n in engine.Player)}) have {int(engine.Goals.sum())} goals and "
         f"{int(engine.Assists.sum())} assists between them."),
    ]
    section_head("Squad Summary", "Key Findings", "Season totals · all competitions", RED)
    H('<div class="grid g3">' + "".join(f'''<div class="card row start gs" style="padding:0.9rem 1rem;">
      <div class="ibox" style="background:{rgba(c, 0.15)};color:{c};">{ico(i, 20)}</div>
      <div class="col grow"><div class="row gx wrap"><span class="h-sm" style="color:{c};font-weight:700;">{v}</span><span class="lbl">{l}</span></div>
      <span class="body-sm" style="margin-top:2px;line-height:1.55;">{d}</span></div></div>''' for c, i, v, l, d in findings) + '</div>')

    # --- 2. Then the explorable data ---
    section_head("Squad Explorer", "Filter, Rank &amp; Compare", "Search · position · sort", SEC)
    counts = df_players.Pos.map(pos_group).value_counts()
    with st.container(key="bar_players"):
        c1, c2, c3 = st.columns([2.2, 2.6, 1.4], vertical_alignment="center")
        with c1:
            q = st.text_input("Search", "", placeholder="Filter by player, position or role…", key="pl_q", label_visibility="collapsed")
        with c2:
            grp = st.segmented_control("Group", [f"All Squad ({len(df_players)})", f"GK ({counts.get('GK', 0)})", f"DEF ({counts.get('DEF', 0)})",
                                                 f"MID ({counts.get('MID', 0)})", f"FWD ({counts.get('FWD', 0)})"],
                                       default=f"All Squad ({len(df_players)})", key="pl_grp", label_visibility="collapsed")
        with c3:
            sort_by = st.selectbox("Sort", ["Minutes played", "Goals + assists", "xG contribution", "Goals", "Assists"], key="pl_sort",
                                   label_visibility="collapsed")
    p = df_players.copy()
    p["GA_"] = p.Goals + p.Assists
    p["Grp"] = p.Pos.map(pos_group)
    if q:
        p = p[p.Player.str.contains(q, case=False) | p.Pos.str.contains(q, case=False) | p.Primary_Role.str.contains(q, case=False)]
    if grp and not grp.startswith("All"):
        p = p[p.Grp == grp.split(" ")[0]]
    # metric -> (column, unit label, bar colour)
    metrics = {"Minutes played": ("Mins", "mins", PASS), "Goals + assists": ("GA_", "G+A", RED), "xG contribution": ("xG_Contrib", "xG", SEC),
               "Goals": ("Goals", "goals", POS), "Assists": ("Assists", "assists", WARN)}
    sort_col, unit_lbl, mcol = metrics[sort_by]
    p = p.sort_values([sort_col, "Mins"], ascending=False)
    grp_code = grp.split(" ")[0] if grp and not grp.startswith("All") else None
    grp_name = {"GK": "Goalkeepers", "DEF": "Defenders", "MID": "Midfielders", "FWD": "Forwards"}.get(grp_code, "Full squad")
    fmt = (lambda v: f"{v:.1f}") if sort_col == "xG_Contrib" else (lambda v: f"{int(v)}")
    H(f'''<div class="row gs lbl wrap" style="margin:0.25rem 0 0.5rem;">{ico("filter_alt", 16, SEC)}
    <span>Showing <b style="color:{SEC};">{grp_name}</b>{f' matching “{esc(q)}”' if q else ''} · {len(p)} player{'s' if len(p) != 1 else ''}
    · ranked by <b style="color:{mcol};">{sort_by.lower()}</b></span></div>''')

    left, right_c = st.columns([7, 5], gap="large")
    with left:
        # Leaderboard follows the sort metric, position group and search
        top = p.head(6)
        mx = max(float(p[sort_col].max()) if len(p) else 0.0, 1e-9)
        rows = []
        for rank, r in enumerate(top.itertuples(), 1):
            val = getattr(r, sort_col)
            load = r.Mins / MAX_MINS * 100
            if sort_col == "Mins":
                width, share = load, f"{load:.0f}% of {MAX_MINS}"
                tag = ("Critical Load", RED) if load >= 88 else (("High Load", PASS) if load >= 75 else ("Optimal", POS))
            else:
                width, share = sdiv(val, mx) * 100, f"{sdiv(getattr(r, sort_col) * 90, r.Mins):.2f} per 90"
                tag = ("Leader", RED) if rank == 1 and val > 0 else (("No output yet", MUTED) if val == 0 else (f"#{rank}", mcol))
            card = tt(esc(r.Player), [(mcol, sort_by, fmt(val)), (None, "Minutes", f"{r.Mins} ({load:.0f}%)"),
                                      (None, "Goals / assists", f"{r.Goals} / {r.Assists}"), (None, "xG contribution", f"{r.xG_Contrib:.1f}")],
                      note=esc(r.Tactical_Impact), align="l", top=False)
            rows.append(f'''<div class="has-tt hov" style="background:{ELEV};padding:0.6rem 0.75rem;border-radius:0.5rem;">{card}
            <div class="row between gs"><div class="row gs"><span class="mono lbl-sm">{r.Pos.split('/')[0]}</span><b class="t">{esc(r.Player)}</b>{pill(tag[0], tag[1])}</div>
            <span class="mono body-sm"><b style="color:{mcol};">{fmt(val)}</b> {unit_lbl} · {share}</span></div>
            <div class="bar" style="margin-top:6px;"><div style="width:{width:.0f}%;background:{mcol};"></div></div>
            <div class="row between lbl-sm" style="margin-top:4px;"><span>{r.Starts} starts / {r.Apps} apps · {r.Mins} mins</span><span>{esc(r.Primary_Role)}</span></div></div>''')
        empty = f'<div class="body-sm">No players match the current filters.</div>'
        title = "Tactical Load Index — Minutes Share" if sort_col == "Mins" else f"{sort_by} Leaderboard"
        sub = (f"Share of the {MAX_MINS} available minutes" if sort_col == "Mins" else f"Top performers by {sort_by.lower()}, bar relative to the leader")
        H(f'''<div class="card lg" style="overflow:visible;"><div class="row between start wrap gs"><div class="row gs">{ico("monitor_heart" if sort_col == "Mins" else "leaderboard", 22, RED)}<div class="col">
        <div class="h-sm">{title}</div><span class="body-sm">{sub} · {grp_name.lower()}, top {min(6, len(p))} of {len(p)}.</span></div></div>
        {pill("Critical ≥ 88%", RED) if sort_col == "Mins" else pill(sort_by, mcol)}</div><div class="col gs" style="margin-top:1rem;">{''.join(rows) or empty}</div></div>''')
    with right_c:
        u = p.copy()  # unit breakdown follows the position group + search
        u["Unit"] = u.Pos.map(pos_unit)
        order = [x for x in ["Forwards", "Attacking Mid", "Midfield Engine", "Defence", "Goalkeepers"] if x in set(u.Unit)]
        agg = u.groupby("Unit").agg(G=("Goals", "sum"), A=("Assists", "sum"), X=("xG_Contrib", "sum"), N=("Player", "count")).reindex(order).fillna(0)
        mx = max(float((agg.G + agg.A).max()) if len(agg) else 0.0, float(agg.X.max()) if len(agg) else 0.0, 1.0)
        urows = "".join(f'''<div><div class="row between"><span class="body-sm t" style="font-weight:600;">{unit} <span class="m" style="font-weight:400;">({int(r.N)})</span></span>
          <span class="mono body-sm"><b style="color:{POS};">{int(r.G + r.A)}</b> <span class="m">G+A /</span> {r.X:.1f} <span class="m">xG</span></span></div>
          <div class="bar" style="height:5px;margin-top:5px;"><div style="width:{(r.G + r.A) / mx * 100:.0f}%;background:{RED};"></div></div>
          <div class="bar" style="height:5px;margin-top:3px;"><div style="width:{r.X / mx * 100:.0f}%;background:{PASS};"></div></div></div>''' for unit, r in agg.iterrows())
        # Insight line adapts to what is being shown
        if grp_code is None and not q:
            att = sum(agg.G.get(k, 0) for k in ("Forwards", "Attacking Mid"))
            insight = (f"<b>Concentration risk:</b> forwards and attacking mids scored {sdiv(att, agg.G.sum()) * 100:.0f}% of player goals; "
                       f"the midfield engine has {int(agg.G.get('Midfield Engine', 0))} goals.")
        elif len(u):
            ga_tot, x_tot = int(u.Goals.sum() + u.Assists.sum()), float(u.xG_Contrib.sum())
            share = sdiv(u.Goals.sum(), df_players.Goals.sum()) * 100
            insight = (f"<b>{grp_name}:</b> {ga_tot} direct goal contributions from {x_tot:.1f} xG "
                       f"({signed(ga_tot - x_tot, '{:+.1f}')}) — {share:.0f}% of the squad's player goals.")
        else:
            insight = "No players match the current filters."
        H(f'''<div class="card lg"><div class="row between"><div class="row gs">{ico("hub", 22, SEC)}<div class="h-sm">Positional Unit Delta</div></div>
        <span class="lbl" style="color:{SEC};">{grp_name}</span></div>
        <div class="body-sm" style="margin-top:0.35rem;">Direct goal contributions against expected-goal contribution by tactical unit.</div>
        <div class="row gs lbl" style="margin-top:0.6rem;"><span class="row gx"><span class="dot" style="background:{RED};"></span>G+A</span><span class="row gx"><span class="dot" style="background:{PASS};"></span>xG contrib</span></div>
        <div class="col gm" style="margin-top:0.75rem;">{urows or '<span class="body-sm">No units to show.</span>'}</div>
        <div class="row start gs" style="margin-top:1rem;background:rgba(239,68,68,0.08);padding:0.6rem 0.75rem;border-radius:0.5rem;">{ico("error", 18, DANGER)}
        <span class="body-sm t">{insight}</span></div></div>''')

    st.write("")
    total_mins = int(p.Mins.sum())
    rows = []
    for i, r in enumerate(p.itertuples(), 1):
        rows.append(f'''<tr><td class="mono m">#{i:02d}</td>
        <td><div class="col"><b style="white-space:nowrap;">{esc(r.Player)}</b><span class="lbl" style="font-size:10px;">{r.Pos} · {r.Grp}</span></div></td>
        <td style="color:{SEC};font-size:0.75rem;">{esc(r.Primary_Role)}</td><td class="n mono">{r.Apps} ({r.Starts})</td>
        <td class="n mono">{r.Mins}<div class="bar" style="height:3px;margin-top:4px;"><div style="width:{r.Mins / MAX_MINS * 100:.0f}%;background:{PASS};"></div></div></td>
        <td class="n mono" style="color:{POS if r.GA_ else MUTED};">{r.Goals} + {r.Assists}</td><td class="n mono">{r.xG_Contrib:.1f}</td>
        <td class="n mono" style="color:{SEC};">{sdiv(r.GA_ * 90, r.Mins):.2f}</td>
        <td class="n mono" style="color:{WARN if r.Yel else MUTED};">{r.Yel} / {r.Red}</td>
        <td class="body-sm m" style="min-width:15rem;">{esc(r.Tactical_Impact)}</td></tr>''')
    body = "".join(rows) or '<tr><td colspan="10" class="m">No players match this filter.</td></tr>'
    sorted_hdr = {"Mins": "Mins", "GA_": "G + A", "Goals": "G + A", "Assists": "G + A", "xG_Contrib": "xG"}[sort_col]
    head_html = "".join(
        f'<th class="{c}"{f" style=color:{mcol}" if h == sorted_hdr else ""}>{h}{" ▼" if h == sorted_hdr else ""}</th>'
        for h, c in (("#", ""), ("Player", ""), ("Role", ""), ("Apps (St)", "n"), ("Mins", "n"), ("G + A", "n"),
                     ("xG", "n"), ("G+A / 90", "n"), ("Y / R", "n"), ("Tactical Impact", "")))
    H(f'''<div class="card lg" style="padding:0;overflow:hidden;"><div class="row between wrap gs" style="padding:1.25rem 1.25rem 0.75rem;">
    <div class="row gs">{ico("view_list", 22, RED)}<div class="col"><div class="h-sm">Squad Tactical Matrix &amp; Role Index</div>
    <span class="body-sm">Complete breakdown of all {len(df_players)} tracked senior members — sorted by {sort_by.lower()}.</span></div></div>
    <span class="row gs lbl"><span class="row gx"><span class="dot" style="background:{POS};"></span>{len(p)} shown</span></span></div>
    <div style="overflow-x:auto;"><table class="tbl"><thead><tr>{head_html}</tr></thead><tbody>{body}</tbody></table></div>
    <div class="row between wrap gs" style="padding:0.9rem 1.25rem;background:{ELEV};"><span class="row gx lbl-sm">{ico("shield", 16)}Tags derived from match logs (MD 1–6)</span>
    <span class="mono lbl-sm">Total minutes shown: <b>{total_mins:,}</b></span></div></div>''')

# ==============================================================================
# PAGE: INVESTIGATION BOARD (Stitch tactics board)
# ==============================================================================
def page_board(f, s):
    tags = pill("Investigation Deep Dive", RED, ping=True) + '<span class="lbl" style="margin-left:0.5rem;">Dossier Module 04 // 2026-27 MD 1–6</span>'
    page_head(tags, "Tactical Pathology &amp; Rest Defense Anatomy",
              "Four core issues, each with its own interactive tactics board — select an issue, toggle tactical layers and click any red node to open player telemetry.")
    active = st.session_state["issue"]

    # --- 1. Tactical problem switcher ---
    cols = st.columns(4, gap="small")
    for i, (col, iss) in enumerate(zip(cols, ISSUES)):
        on = i == active
        c = iss["color"]
        with col:
            with st.container(key=f"clickissue_{i}"):
                H(f'''<div class="card hov" style="padding:1rem;{f'background:{ELEV};box-shadow:0 10px 15px -3px rgba(0,0,0,0.4);' if on else ''}min-height:12.5rem;">
                {f'<div style="position:absolute;left:0;top:0;bottom:0;width:6px;background:{RED};"></div>' if on else ''}
                <div class="row between gs">{pill(iss["sev"], c, bg=0.2)}<span class="mono lbl-sm m" style="white-space:nowrap;">ISSUE #0{iss["n"]}</span></div>
                <div class="mono body-sm" style="color:{iss["metric_color"]};font-weight:600;margin-top:0.4rem;">{iss["metric"]}</div>
                <div style="font-family:'Plus Jakarta Sans';font-size:1.05rem;line-height:1.35;font-weight:{700 if on else 600};color:{TEXT};margin-top:0.5rem;">{iss["title"]}</div>
                <div class="body-sm" style="margin-top:0.25rem;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">{iss["blurb"]}</div>
                <div class="row between" style="margin-top:0.75rem;"><span class="lbl">Vulnerability Index</span>
                <span class="mono body-sm" style="color:{c};font-weight:700;">{iss["vi"]:.1f} / 100</span></div></div>''')
                st.button(f"Open issue {iss['n']}", key=f"issuebtn_{i}", on_click=set_issue, args=(i,))

    iss = ISSUES[active]
    key = iss["key"]
    chart_key, pick_key, last_key = f"board_{key}", f"pick_{key}", f"lastclick_{key}"
    board_names = [c[3] for c in iss["players"]]
    st.session_state.setdefault(pick_key, iss["focus"])

    # Apply a pitch click from the previous run (the chart's selection is stored in session state under its key)
    clicked = None
    try:
        ev = st.session_state.get(chart_key)
        pts = ev["selection"]["points"] if ev else []
        for pt in pts:
            cd = pt.get("customdata")
            if cd:
                clicked = cd[0] if isinstance(cd, (list, tuple)) else cd
    except Exception:
        clicked = None
    if clicked in board_names and st.session_state.get(last_key) != clicked:
        st.session_state[pick_key] = clicked
    st.session_state[last_key] = clicked
    st.write("")

    # --- 2. Issue summary first: problem, evidence, impact, root cause ---
    section_head(f"Issue #0{iss['n']} Summary", iss["title"], iss["sev"] + " · vulnerability index " + f"{iss['vi']:.1f}", iss["color"])
    ev_rows = "".join(f'''<div class="row between" style="padding:0.6rem;border-radius:0.5rem;background:{ELEV};">
      <span class="body-sm">{a}</span><span class="mono body-sm" style="color:{c};font-weight:700;text-align:right;">{b}</span></div>''' for a, b, c in iss["evidence"])
    big, big_t, big_s = iss["impact_big"]
    H(f'''<div class="grid g4">
    <div class="card lg col between"><div><div class="row between">{pill("Diagnostic #0" + str(iss["n"]), RED, bg=0.2)}{ico("report_problem", 20, RED)}</div>
      <div class="h-sm" style="font-weight:700;margin-top:0.6rem;">{iss["problem_title"]}</div>
      <div class="body-md" style="margin-top:0.5rem;line-height:1.65;">{iss["problem"]}</div></div>
      <div style="margin-top:1rem;background:rgba(22,27,38,0.4);padding:0.75rem;border-radius:0.75rem;"><span class="lbl">Core Fault</span>
      <div style="font-family:'Plus Jakarta Sans';font-weight:700;font-size:1.05rem;color:{TEXT};margin-top:2px;">{iss["fault"][0]}</div>
      <span class="mono lbl-sm" style="color:{DANGER};">{iss["fault"][1]}</span></div></div>
    <div class="card lg col between"><div><div class="row between">{pill("Forensic Evidence", TACT, bg=0.2)}{ico("database", 20, TACT)}</div>
      <div class="h-sm" style="font-weight:700;margin-top:0.6rem;">Empirical Telemetry</div><div class="col gs" style="margin-top:0.6rem;">{ev_rows}</div></div>
      <div class="row gs lbl" style="margin-top:1rem;">{ico("verified", 16, POS)}Verified via Opta / FotMob match logs</div></div>
    <div class="card lg col between"><div><div class="row between">{pill("Consequence", DANGER, bg=0.2)}{ico("crisis_alert", 20, DANGER)}</div>
      <div class="h-sm" style="font-weight:700;margin-top:0.6rem;">Matchday Impact</div>
      <div class="body-md" style="margin-top:0.5rem;line-height:1.65;">{iss["impact"]}</div>
      <div class="row gs" style="margin-top:0.75rem;padding:0.75rem;border-radius:0.75rem;background:rgba(147,0,10,0.25);">
      <span class="stat-xl" style="color:{ERR};">{big}</span><div class="col"><span style="font-family:'Plus Jakarta Sans';font-weight:700;font-size:0.8125rem;color:#ffdad6;">{big_t}</span>
      <span class="lbl-sm">{big_s}</span></div></div></div>
      <div class="row between mono lbl-sm" style="margin-top:1rem;"><span>{iss["impact_foot"][0]}</span><span style="color:{DANGER};font-weight:700;">{iss["impact_foot"][1]}</span></div></div>
    <div class="card lg el col between"><div class="glow" style="right:0;top:0;width:6rem;height:6rem;background:rgba(16,185,129,0.12);filter:blur(24px);"></div>
      <div class="z"><div class="row between">{pill("Root-Cause Hypothesis", POS, bg=0.2)}{ico("psychology", 20, POS)}</div>
      <div class="h-sm" style="font-weight:700;margin-top:0.6rem;">{iss["cause_title"]}</div>
      <div class="body-md" style="margin-top:0.5rem;line-height:1.65;">{iss["cause"]}</div></div>
      <div class="row gs z" style="margin-top:1rem;color:{POS};">{ico("check_circle", 18, POS)}<span class="body-sm" style="color:{POS};font-weight:600;">{iss["cause_foot"]}</span></div></div>
    </div>''')

    # --- 3. Then the interactive board ---
    H('<div class="board-anchor" style="scroll-margin-top:0.75rem;"></div>')  # scroll target for issue clicks
    section_head("Interactive Tactics Board", "Explore the Phase", "Click a red node to inspect a player", SEC)
    if st.session_state.pop("scroll_to_board", False):
        scroll_to(".board-anchor")
    stage, insp = st.columns([8, 4], gap="large")
    with stage:
        with st.container(key=f"card_stage_{key}"):
            H(f'''<div class="row gs"><span class="ibox" style="background:{ELEV};color:{RED};border-radius:0.5rem;">{ico("sports_soccer", 20)}</span>
            <div class="col"><div class="row gs wrap"><span class="h-sm" style="font-weight:700;">{iss["stage_title"]}</span>
            <span class="mono lbl-sm" style="background:{OVERLAY};color:{PASS};padding:2px 8px;border-radius:4px;">{iss["code"]}</span></div>
            <span class="body-sm">{iss["stage_sub"]}</span></div></div>''')
            H(board_guide(iss))
            h1, h2 = st.columns([1, 3.2], vertical_alignment="center")
            with h1:
                H(f'<div class="row gx lbl">{ico("layers", 16, RED)}Tactical layers</div>')
            with h2:
                layer_labels = list(iss["layers"].keys())
                on_layers = st.pills("Layers", layer_labels, selection_mode="multi", default=layer_labels,
                                     key=f"layers_{key}", label_visibility="collapsed") or []
            selected = st.session_state[pick_key]
            fig = go.Figure()
            add_pitch(fig)
            for lab in layer_labels:
                if lab in on_layers:
                    iss["layers"][lab](fig)
            add_players(fig, iss["players"], selected=selected)
            finalize_pitch(fig, f"<span style='color:{RED}'>●</span>  <b>BOARD 0{iss['n']}</b>  ·  {iss['direction']}",
                           f"<span style='color:{MUTED}'>VULNERABILITY INDEX</span><br><b style='color:{iss['color']}'>{iss['vi']:.1f} / 100</b>",
                           view=iss.get("view"))
            st.plotly_chart(fig, width="stretch", key=chart_key, on_select="rerun", selection_mode="points",
                            config={**PLOTLY_CONFIG, "scrollZoom": False, "doubleClick": "reset"})

    with insp:
        with st.container(key=f"card_insp_{key}"):
            # the pick is already in session state, so the badge can reflect the current player before the selectbox renders
            cur = st.session_state[pick_key]
            ex = player_exposure(iss, cur, int(df_players.loc[df_players.Player == cur, "Mins"].iloc[0]))
            H(f'''<div class="glow" style="right:0;top:0;width:8rem;height:8rem;background:{rgba(ex["color"], 0.14)};filter:blur(40px);"></div>
            <div class="row between" style="padding-bottom:0.6rem;border-bottom:1px solid rgba(50,53,60,0.5);">
            <div class="row gs">{ico("person_search", 18, RED)}<span class="lbl" style="letter-spacing:0.18em;">Player Forensic Telemetry</span></div>
            <span class="mono lbl-sm" style="background:{rgba(ex["color"], 0.18)};color:{ex["color"]};padding:2px 8px;border-radius:4px;font-weight:700;"
            title="Player exposure index {ex['score']:.0f}/100 for this issue">{ex["tier"].upper()} NODE · {ex["score"]:.0f}</span></div>''')
            H(f'<div class="lbl-sm" style="margin-top:0.5rem;">Pick a player or click any red node on the pitch</div>')
            name = st.selectbox("Inspect player", board_names, key=pick_key, label_visibility="collapsed")
            r = df_players[df_players.Player == name].iloc[0]
            load = r.Mins / MAX_MINS * 100
            ex_now = player_exposure(iss, name, int(r.Mins))
            role_title, role_text = ISSUE_ROLES[key][name]
            tiles = [
                ("Goals", f"{r.Goals}", "", POS if r.Goals else TEXT, f"{sdiv(r.Goals * 90, r.Mins):.2f} per 90"),
                ("Assists", f"{r.Assists}", "", POS if r.Assists else TEXT, f"{r.Goals + r.Assists} direct G+A"),
                ("Minutes", f"{r.Mins}", "'", WARN if load >= 85 else TEXT, f"{load:.0f}% of available"),
                ("xG Contribution", f"{r.xG_Contrib:.1f}", "", SEC, f"{signed(r.Goals + r.Assists - r.xG_Contrib, '{:+.1f}')} G+A vs xG"),
            ]
            tile_html = "".join(f'''<div style="background:{ELEV};padding:0.6rem;border-radius:0.75rem;">
              <span class="lbl">{lab}</span><div class="row gx" style="align-items:baseline;margin-top:4px;">
              <span class="mono h-sm" style="font-weight:700;color:{c};">{v}</span><span class="mono lbl-sm">{u}</span></div>
              <span class="lbl" style="font-size:10px;margin-top:4px;display:block;">{foot}</span></div>''' for lab, v, u, c, foot in tiles)
            H(f'''<div class="row gm" style="margin-top:0.25rem;">
            <div style="position:relative;width:4rem;height:4rem;border-radius:0.75rem;background:linear-gradient(145deg,{OVERLAY},{CANVAS});display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:inset 0 0 0 1px rgba(255,45,59,0.35);">
            <span style="font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.4rem;color:{TEXT};">{initials(name)}</span>
            <span class="mono" style="position:absolute;bottom:3px;right:3px;background:{RED_CORE};color:#fff;font-size:10px;padding:0 5px;border-radius:4px;">{r.Pos.split('/')[0]}</span></div>
            <div class="col" style="min-width:0;"><div class="h-sm" style="font-weight:700;">{esc(name)}</div>
            <div class="row gs body-sm"><span>{esc(r.Pos)}</span><span class="dot" style="width:4px;height:4px;background:var(--bright);"></span><span style="color:{PASS};">{esc(r.Primary_Role)}</span></div>
            <span class="mono lbl-sm">Apps {r.Apps} ({r.Starts} starts) · Yellows {r.Yel}</span></div></div>
            <div class="grid g2 gsm" style="margin-top:1rem;">{tile_html}</div>
            <div style="margin-top:1rem;background:rgba(27,34,50,0.8);padding:0.75rem;border-radius:0.75rem;box-shadow:inset 3px 0 0 {ex_now['color']};">
            <div class="row gx lbl" style="color:{ex_now['color']};font-weight:700;">{ico("visibility", 16, ex_now['color'])}Role in this issue</div>
            <div class="t" style="margin-top:0.4rem;font-family:'Plus Jakarta Sans';font-weight:700;font-size:0.95rem;">{esc(role_title)}</div>
            <div class="body-sm t" style="margin-top:0.2rem;line-height:1.6;">{esc(role_text)}</div>
            <div class="body-sm" style="margin-top:0.55rem;line-height:1.5;font-size:12px;"><span class="lbl" style="font-size:10px;">Season note</span><br>{esc(r.Tactical_Impact)}.</div></div>''')
        c = iss["color"]
        ex = player_exposure(iss, name, int(r.Mins))  # recomputed from the widget's final value
        rank = sorted((player_exposure(iss, p[3], int(df_players.loc[df_players.Player == p[3], "Mins"].iloc[0]))["score"]
                       for p in iss["players"]), reverse=True).index(ex["score"]) + 1
        H(exposure_card(ex, iss, name, int(r.Mins), rank))


# ==============================================================================
# PAGE: DATA METHODOLOGY
# ==============================================================================
def page_methodology(f, s):
    tags = pill("Dossier Appendix // Methodology", SEC, dot=True)
    page_head(tags, "Data Methodology &amp; Technical Standards",
              "Sources, metric definitions, benchmark assumptions and known limitations behind every figure in this dossier.")
    blocks = [
        ("database", SEC, "Data Sources", [
            ("Opta match scrapes", "Matchday feeds for all 6 competitive fixtures."),
            ("Premier League Match Centre", "Match metadata, referee records and event logs."),
            ("FotMob & TNT Sports analytics", "xG, xGA, shot maps, pass accuracy and player ratings."),
            ("Wikipedia & Fandom season logs", "Historical context, transfers and squad registrations."),
            ("Google NotebookLM", "Research and data extraction: sources above gathered and structured into the match and player datasets.")]),
        ("function", RED, "Key Metric Definitions", [
            ("Expected Goals (xG)", "Chance-quality measure, 0.0–1.0 per shot."),
            ("Rest Defense", "Positioning of non-attacking players in possession to prevent counters on turnover."),
            ("Opp. SoT Conversion", "Goals conceded ÷ opponent shots on target."),
            ("Box Touches", "Legal ball contacts inside the opponent's 18-yard box.")]),
        ("rule", POS, "Benchmark Methodology", [
            ("Competitive baseline", "6 fixtures in 2026/27 (4 PL, 1 UCL, 1 EFL Cup)."),
            ("Possession dominance", "Baseline of more than 55% ball possession."),
            ("Expected goal differential", "xG − xGA; positive = chance-creation superiority."),
            ("Vulnerability index", "Analyst composite (0–100) per issue for prioritisation.")]),
        ("report", WARN, "Limitations &amp; Uncovered Areas", [
            ("PPDA", "Estimated from tackle / interception logs where full radar feeds were unavailable."),
            ("GPS tracking", "High-intensity sprint and distance data limited to sample matches."),
            ("Goal minutes", "One first-half goal conceded (vs Ipswich) has no recorded minute and is bucketed as 0–45'."),
            ("Tactics boards", "Illustrative positional models, not literal event-level tracking snapshots.")]),
    ]
    H('<div class="grid g2">' + "".join(f'''<div class="card lg"><div class="row gs"><div class="ibox" style="background:{rgba(c, 0.15)};color:{c};">{ico(i, 20)}</div>
      <div class="h-sm" style="font-weight:700;">{t}</div></div><div class="col gs" style="margin-top:1rem;">
      {''.join(f'<div style="background:{ELEV};padding:0.6rem 0.75rem;border-radius:0.5rem;"><div class="lbl" style="color:{c};">{a}</div><div class="body-sm t" style="margin-top:3px;">{b}</div></div>' for a, b in items)}
      </div></div>''' for i, c, t, items in blocks) + '</div>')

# ------------------------------------------------------------------------------
# ROUTER
# ------------------------------------------------------------------------------
PAGES = {
    "Executive Summary": page_executive,
    "Match Results & Form": page_match_results,
    "Attacking Analytics": page_attacking,
    "Defensive & Transition": page_defensive,
    "Player Performance Matrix": page_players,
    "Investigation Board": page_board,
    "Data Methodology": page_methodology,
}
PAGES[nav](filtered_df, S)
footer()
