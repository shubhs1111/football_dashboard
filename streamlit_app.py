# ==============================================================================
# MANCHESTER UNITED 2026/27 SEASON ANALYTICS DASHBOARD (V3)
# "Why Has Manchester United Started the Season Poorly?"
# V3: Per-Issue Interactive Tactics Boards + Click-to-Inspect Player Maps
# Built with Streamlit, Plotly, and Pandas
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="MUFC 2026/27 Tactical & Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Design system ported from the "United Intel / Tactical Lab" Google Stitch concept ---
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    :root{
        --canvas:#0B0E14; --card:#10141D; --elevated:#161B26; --overlay:#1B2232; --highlight:#222B3D;
        --red:#FF2D3B; --red-core:#DA020E; --cyan:#38BDF8; --cyan-deep:#06B6D4; --emerald:#10B981;
        --amber:#F59E0B; --danger:#EF4444; --text:#E1E2EB; --muted:#94A3B8;
        --border:rgba(255,255,255,0.08);
    }
    /* Base canvas + typography */
    .stApp, [data-testid="stAppViewContainer"]{ background:var(--canvas); color:var(--text); }
    [data-testid="stHeader"]{ background:transparent; }
    html, body, [class*="css"], .stMarkdown, p, span, div, label{ font-family:'Geist', sans-serif; }
    h1,h2,h3,h4,h5{ font-family:'Plus Jakarta Sans', sans-serif !important; font-weight:800; letter-spacing:-0.02em; color:#ffffff; }
    h1{ font-size:2.6rem; line-height:1.08; }
    h2{ font-size:1.9rem; } h3{ font-size:1.35rem; font-weight:700; } h4{ font-size:1.05rem; font-weight:700; }
    a{ color:var(--cyan); }

    /* Sidebar */
    [data-testid="stSidebar"]{ background:#0B0E14; border-right:1px solid var(--border); }
    [data-testid="stSidebar"] *{ color:var(--text); }

    /* Editorial kicker label */
    .kicker{ font-family:'Geist'; font-size:0.72rem; letter-spacing:0.16em; text-transform:uppercase;
             color:var(--red); font-weight:700; margin-bottom:2px; }

    /* Tabs -> segmented pills */
    .stTabs [data-baseweb="tab-list"]{ gap:6px; border-bottom:1px solid var(--border); padding-bottom:4px; flex-wrap:wrap; }
    .stTabs [data-baseweb="tab"]{ background:var(--card); border:1px solid var(--border); border-radius:9999px;
        color:var(--muted); padding:6px 16px; font-family:'Geist'; font-size:0.82rem; font-weight:600; }
    .stTabs [aria-selected="true"]{ background:var(--overlay) !important; color:#ffffff !important;
        border-color:var(--red) !important; box-shadow:inset 0 0 0 1px var(--red); }

    /* KPI metric cards */
    [data-testid="stMetric"]{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:16px 18px; }
    [data-testid="stMetricLabel"] p{ font-family:'Geist' !important; font-size:0.68rem !important; letter-spacing:0.12em;
        text-transform:uppercase; color:var(--muted) !important; font-weight:600; }
    [data-testid="stMetricValue"]{ font-family:'Plus Jakarta Sans' !important; font-weight:800 !important;
        font-size:2.1rem !important; color:#ffffff; letter-spacing:-0.02em; }
    [data-testid="stMetricDelta"]{ font-family:'Geist' !important; font-weight:600; font-size:0.8rem; }

    /* Content cards */
    .metric-card{ background:var(--card); border:1px solid var(--border); border-left:3px solid var(--red);
        border-radius:12px; padding:18px; }
    .metric-value{ font-family:'Plus Jakarta Sans'; font-size:24px; font-weight:800; color:#ffffff; }
    .metric-label{ font-size:0.68rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.12em; font-weight:600; }
    .problem-box{ background:var(--card); border:1px solid var(--border); border-left:4px solid var(--danger); padding:16px; border-radius:10px; margin-bottom:14px; }
    .evidence-box{ background:var(--card); border:1px solid var(--border); border-left:4px solid var(--emerald); padding:16px; border-radius:10px; margin-bottom:14px; }
    .impact-box{ background:var(--card); border:1px solid var(--border); border-left:4px solid var(--amber); padding:16px; border-radius:10px; margin-bottom:14px; }
    .explanation-box{ background:var(--card); border:1px solid var(--border); border-left:4px solid var(--cyan); padding:16px; border-radius:10px; margin-bottom:14px; }
    .tactics-card{ background:var(--elevated); border:1px solid var(--border); border-radius:12px; padding:18px; margin-top:10px; }
    .player-card{ background:var(--overlay); border:1px solid var(--red); border-radius:12px; padding:14px; margin-top:8px;
        box-shadow:0 0 16px rgba(255,45,59,0.20); }

    /* Buttons */
    .stButton>button{ background:var(--red); color:#ffffff; border:none; border-radius:8px;
        font-family:'Plus Jakarta Sans'; font-weight:700; }
    .stButton>button:hover{ box-shadow:0 0 20px rgba(255,45,59,0.4); color:#ffffff; }

    /* Inputs, tables, alerts */
    [data-testid="stDataFrame"]{ border:1px solid var(--border); border-radius:10px; }
    [data-testid="stAlert"]{ background:var(--elevated); border:1px solid var(--border); border-radius:10px; }
    .stMultiSelect [data-baseweb="tag"]{ background:var(--overlay) !important; }
    hr{ border-color:var(--border); }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. DATASETS GENERATION (GROUNDED IN OPTA & NOTEBOOK SOURCES)
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
    return pd.DataFrame(matches)

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

# Palette tokens (mirror the CSS design system) for use in Plotly traces
C_RED = "#FF2D3B"; C_CYAN = "#38BDF8"; C_EMERALD = "#10B981"; C_AMBER = "#F59E0B"; C_DANGER = "#EF4444"

# ------------------------------------------------------------------------------
# CHART THEMING — consistent fonts + readable hover tooltips across all charts
# ------------------------------------------------------------------------------
def style_chart(fig):
    """Apply the Tactical-Lab design system (fonts, palette, legible hover) to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E1E2EB", size=13, family="Geist, sans-serif"),
        title_font=dict(color="#ffffff", size=16, family="Plus Jakarta Sans, sans-serif"),
        colorway=["#FF2D3B", "#38BDF8", "#10B981", "#F59E0B", "#A78BFA", "#F472B6", "#22D3EE"],
        hoverlabel=dict(bgcolor="#161B26", bordercolor="rgba(255,255,255,0.14)",
                        font=dict(color="#ffffff", size=13, family="Geist, sans-serif"), align="left"),
        legend=dict(font=dict(color="#E1E2EB", size=12)),
        margin=dict(t=60, r=20, b=50, l=20),
    )
    fig.update_xaxes(title_font=dict(size=13, color="#94A3B8"), tickfont=dict(size=12, color="#94A3B8"),
                     gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(title_font=dict(size=13, color="#94A3B8"), tickfont=dict(size=12, color="#94A3B8"),
                     gridcolor="rgba(255,255,255,0.06)")
    return fig

# ------------------------------------------------------------------------------
# 3. INTERACTIVE TACTICS-BOARD ENGINE (PITCH + LAYERS + PLAYER MAPS)
# ------------------------------------------------------------------------------
PITCH_L, PITCH_W = 105, 68

def add_pitch(fig):
    """Draw the base football pitch (lines, boxes, center circle, half-space guides)."""
    fig.add_shape(type="rect", x0=0, y0=0, x1=PITCH_L, y1=PITCH_W,
                  fillcolor="#0E131C", line=dict(color="rgba(255,255,255,0.55)", width=2), layer="below")
    fig.add_shape(type="line", x0=PITCH_L/2, y0=0, x1=PITCH_L/2, y1=PITCH_W, line=dict(color="#ffffff", width=2))
    fig.add_shape(type="circle", x0=PITCH_L/2 - 9.15, y0=PITCH_W/2 - 9.15, x1=PITCH_L/2 + 9.15, y1=PITCH_W/2 + 9.15,
                  line=dict(color="#ffffff", width=2))
    fig.add_trace(go.Scatter(x=[PITCH_L/2], y=[PITCH_W/2], mode="markers",
                             marker=dict(size=4, color="#ffffff"), hoverinfo="skip", showlegend=False))
    # Penalty & goal areas (both ends)
    fig.add_shape(type="rect", x0=0, y0=13.84, x1=16.5, y1=54.16, line=dict(color="#ffffff", width=2))
    fig.add_shape(type="rect", x0=0, y0=24.84, x1=5.5, y1=43.16, line=dict(color="#ffffff", width=1.5))
    fig.add_shape(type="rect", x0=88.5, y0=13.84, x1=105, y1=54.16, line=dict(color="#ffffff", width=2))
    fig.add_shape(type="rect", x0=99.5, y0=24.84, x1=105, y1=43.16, line=dict(color="#ffffff", width=1.5))
    # Half-space guides
    fig.add_shape(type="line", x0=0, y0=20.4, x1=PITCH_L, y1=20.4, line=dict(color="rgba(255,255,255,0.2)", width=1, dash="dot"))
    fig.add_shape(type="line", x0=0, y0=47.6, x1=PITCH_L, y1=47.6, line=dict(color="rgba(255,255,255,0.2)", width=1, dash="dot"))

def finalize_pitch(fig, title, height=580):
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color="#ffffff", family="Plus Jakarta Sans, sans-serif"), x=0, xanchor="left", y=0.97, yanchor="top"),
        xaxis=dict(range=[-2, 107], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-2, 70], showgrid=False, zeroline=False, visible=False),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=55, b=55), height=height,
        clickmode="event+select",
        hoverlabel=dict(bgcolor="#161B26", bordercolor="rgba(255,255,255,0.14)",
                        font=dict(color="#ffffff", size=13, family="Geist, sans-serif"), align="left"),
        legend=dict(orientation="h", yanchor="top", y=-0.04, x=0.5, xanchor="center",
                    font=dict(color="#ffffff", size=10), bgcolor="rgba(0,0,0,0.25)")
    )

def add_players(fig, coords, color="#FF2D3B", name="Manchester United"):
    """coords: list of (x, y, short_label, full_name). Clicking a marker returns full_name via customdata."""
    xs = [c[0] for c in coords]; ys = [c[1] for c in coords]
    short = [c[2] for c in coords]; full = [c[3] for c in coords]
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers+text",
        marker=dict(size=24, color=color, line=dict(width=2, color="#ffffff")),
        text=short, textposition="top center", textfont=dict(color="#ffffff", size=10, family="sans-serif"),
        customdata=[[f] for f in full], hovertext=full, hoverinfo="text", name=name
    ))

def add_opponents(fig, coords, color="#38BDF8", name="Opponent Threat"):
    xs = [c[0] for c in coords]; ys = [c[1] for c in coords]; lbl = [c[2] for c in coords]
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers",
        marker=dict(size=18, color=color, symbol="diamond", line=dict(width=1.5, color="#ffffff")),
        hovertext=lbl, hoverinfo="text", name=name
    ))

# --- small drawing helpers ---
def _zone(fig, x0, y0, x1, y1, rgba, edge, dash="dash"):
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, fillcolor=rgba,
                  line=dict(color=edge, width=1.5, dash=dash), layer="below")

def _arrow(fig, x0, y0, x1, y1, color, width=3):
    fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.3, arrowcolor=color, arrowwidth=width)

def _label(fig, x, y, text, color, size=11):
    fig.add_annotation(x=x, y=y, text=text, showarrow=False, font=dict(color=color, size=size, family="sans-serif"))

def _circle(fig, cx, cy, rx, ry, rgba, edge):
    fig.add_shape(type="circle", x0=cx - rx, y0=cy - ry, x1=cx + rx, y1=cy + ry,
                  fillcolor=rgba, line=dict(color=edge, width=2), layer="below")

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
    _zone(f, 32, 48, 66, 66, "rgba(255,75,75,0.20)", "#EF4444")
    _zone(f, 32, 2, 66, 20, "rgba(255,75,75,0.20)", "#EF4444")
    _label(f, 49, 57, "Vacated half-space", "#ff8a8a", 10)
    _label(f, 49, 11, "Vacated half-space", "#ff8a8a", 10)
def i1_counters(f):
    _arrow(f, 62, 55, 36, 50, "#EF4444")
    _arrow(f, 62, 13, 36, 20, "#EF4444")
    _label(f, 64, 52, "Counter", "#EF4444", 10)
    _label(f, 64, 16, "Counter", "#EF4444", 10)
def i1_isolated_pivot(f):
    _circle(f, 48, 33, 11, 13, "rgba(255,167,38,0.14)", "#F59E0B")
    _label(f, 63, 44, "Stretched<br>double pivot", "#F59E0B", 10)

# ---------- ISSUE 2: SECOND-HALF COLLAPSE ----------
I2_PLAYERS = [
    (6, 34, "Lammens", "Senne Lammens"), (22, 58, "Shaw", "Luke Shaw"), (22, 42, "Martínez", "Lisandro Martínez"),
    (22, 26, "Maguire", "Harry Maguire"), (22, 10, "Dalot", "Diogo Dalot"), (38, 42, "Mainoo", "Kobbie Mainoo"),
    (38, 26, "Tielemans", "Youri Tielemans"), (52, 56, "Rashford", "Marcus Rashford"), (52, 34, "Bruno", "Bruno Fernandes"),
    (52, 12, "Mbeumo", "Bryan Mbeumo"), (66, 34, "Šeško", "Benjamin Šeško"),
]
def i2_first_half(f):
    _zone(f, 18, 8, 56, 60, "rgba(66,165,245,0.10)", "#38BDF8")
    _label(f, 37, 63, "1st-half compact block (GD +2)", "#8fc4f5", 10)
def i2_gap(f):
    _zone(f, 27, 6, 40, 62, "rgba(255,75,75,0.18)", "#EF4444", dash="dot")
    _label(f, 33, 65, "Late fatigue gap between lines", "#ff8a8a", 10)
    _arrow(f, 46, 34, 30, 34, "#EF4444")
def i2_late_goals(f):
    spots = [(3, 40, "83' George (Everton)"), (3, 28, "90+6' Maitland-Niles"), (3, 34, "90+1' Akpom (Ipswich)")]
    fig_x = [s[0] for s in spots]; fig_y = [s[1] for s in spots]; lbl = [s[2] for s in spots]
    f.add_trace(go.Scatter(x=fig_x, y=fig_y, mode="markers", marker=dict(size=16, color="#EF4444", symbol="x"),
                           hovertext=lbl, hoverinfo="text", name="Late goals conceded"))

# ---------- ISSUE 3: SET-PIECE DISORGANIZATION (defending own box, left goal) ----------
I3_PLAYERS = [
    (2.5, 34, "Lammens", "Senne Lammens"), (5.5, 40, "Maguire", "Harry Maguire"), (5.5, 28, "Martínez", "Lisandro Martínez"),
    (9, 46, "Heaven", "Ayden Heaven"), (9, 22, "Yoro", "Leny Yoro"), (12, 34, "Tielemans", "Youri Tielemans"),
    (12, 50, "Dalot", "Diogo Dalot"), (12, 18, "Dorgu", "Patrick Dorgu"), (15, 44, "Mainoo", "Kobbie Mainoo"),
    (15, 24, "Mbeumo", "Bryan Mbeumo"), (17, 34, "Bruno", "Bruno Fernandes"),
]
def i3_zonal_gaps(f):
    _circle(f, 11, 40, 4, 4, "rgba(255,75,75,0.22)", "#EF4444")
    _circle(f, 8, 44, 3.5, 3.5, "rgba(255,75,75,0.22)", "#EF4444")
    _label(f, 11, 47, "Unmarked zonal gaps", "#ff8a8a", 10)
def i3_opponents(f):
    opp = [(10, 41, "Ajayi (Hull 17' corner)"), (7.5, 45, "Mendy (Hull 38' FK)"), (13, 39, "Second-ball runner")]
    add_opponents(f, opp)
def i3_conceded(f):
    goals = [(0.5, 36, "Hull 17'"), (0.5, 32, "Hull 38'"), (0.5, 34, "Everton 96'")]
    gx = [g[0] for g in goals]; gy = [g[1] for g in goals]; lbl = [g[2] for g in goals]
    f.add_trace(go.Scatter(x=gx, y=gy, mode="markers", marker=dict(size=15, color="#ffd400", symbol="star"),
                           hovertext=lbl, hoverinfo="text", name="Set-piece goals conceded"))

# ---------- ISSUE 4: BRUNO OVER-RELIANCE ----------
I4_PLAYERS = [
    (8, 34, "Lammens", "Senne Lammens"), (25, 48, "Martínez", "Lisandro Martínez"), (25, 20, "Maguire", "Harry Maguire"),
    (45, 58, "Dorgu", "Patrick Dorgu"), (50, 34, "Tielemans", "Youri Tielemans"), (45, 10, "Dalot", "Diogo Dalot"),
    (80, 60, "Rashford", "Marcus Rashford"), (72, 37, "Bruno", "Bruno Fernandes"), (75, 31, "Cunha", "Matheus Cunha"),
    (82, 10, "Mbeumo", "Bryan Mbeumo"), (92, 34, "Šeško", "Benjamin Šeško"),
]
def i4_overlap(f):
    _circle(f, 73.5, 34, 12, 14, "rgba(255,167,38,0.25)", "#F59E0B")
    _label(f, 73.5, 34, "Bruno + Cunha<br>space overlap", "#ffd08a", 10)
def i4_dependency(f):
    for (sx, sy) in [(50, 34), (25, 48), (45, 58), (45, 10), (80, 60)]:
        _arrow(f, sx, sy, 72, 37, "#10B981", 2)
    _label(f, 60, 20, "Passing network funnels into Bruno", "#10B981", 10)
def i4_empty_box(f):
    _zone(f, 90, 20, 105, 48, "rgba(66,165,245,0.12)", "#38BDF8", dash="dot")
    _label(f, 97.5, 50, "Box left to Šeško alone", "#8fc4f5", 10)

# ==============================================================================
# ISSUE REGISTRY
# ==============================================================================
ISSUES = [
    {
        "key": "i1", "tab_label": "1 · Rest Defense",
        "title": "Issue 1: Rest Defense Vulnerability & Defensive Transition Exposure",
        "pitch_title": "Rest Defense Defect — Half-Space Counter Exploitation (attacking L→R)",
        "players": I1_PLAYERS,
        "layers": {"Vacated half-spaces": i1_halfspaces, "Opponent counter runs": i1_counters, "Isolated double pivot": i1_isolated_pivot},
        "board_summary": (
            "United attack **left → right** in a 2-3-5 shape. Both full-backs (**Dorgu**, **Dalot**) have pushed high, "
            "so the moment possession is lost the two **red half-space zones** are wide open. The **red arrows** are the "
            "counter-attacks opponents drive into that space, while the two-man pivot (**Tielemans + Mainoo**, orange circle) "
            "is stretched trying to cover both channels. This is the exact shape Everton and Brighton punished on the transition."
        ),
        "prose": """
        <div class="problem-box"><b>PROBLEM:</b> Inability to protect central half-spaces and prevent opposition counter-attacks when committing numbers forward in high-possession states.</div>
        <div class="evidence-box"><b>EVIDENCE:</b><ul>
            <li>Conceded 10 actual goals across 6 games despite averaging 57.7% possession.</li>
            <li>Opponents averaged 11.8 shots per game (18 by Everton, 18 by Brighton).</li>
            <li>In 55%+ possession games, conceded 7 goals in 4 matches; lost 2-3 to Brighton after leading 2-0.</li>
        </ul></div>
        <div class="impact-box"><b>IMPACT:</b> Opponents convert transitions at a very high rate (50% of shots on target scored), making ball dominance fragile.</div>
        <div class="explanation-box"><b>POSSIBLE EXPLANATION:</b> Carrick's framework pushes both full-backs high into a 5-man line, leaving a 2-man pivot (Tielemans + Mainoo) with too much lateral ground to cover — without injured destroyers Baleba & Ugarte.</div>
        """
    },
    {
        "key": "i2", "tab_label": "2 · 2nd-Half Collapse",
        "title": "Issue 2: Severe Second-Half & Stoppage-Time Concentration Collapses",
        "pitch_title": "Late-Game Shape Drift — Gaps Open Between the Lines (defending R→L)",
        "players": I2_PLAYERS,
        "layers": {"1st-half compact block": i2_first_half, "Late fatigue gap": i2_gap, "Late goals conceded": i2_late_goals},
        "board_summary": (
            "United defend **right → left**. The **blue box** is their compact, well-organised first-half block. The "
            "**dotted red band** shows how the lines pull apart as legs tire after ~70', opening a gap straight through the "
            "middle (**red arrow**). The **red ✕ marks** are the actual late goals conceded — 83' & 90+6' at Everton and "
            "90+1' vs Ipswich. The shape is fine early; it falls apart late."
        ),
        "prose": """
        <div class="problem-box"><b>PROBLEM:</b> Drastic decline in defensive organization, press intensity, and game-state management in the final 30 minutes.</div>
        <div class="evidence-box"><b>EVIDENCE:</b><ul>
            <li>Outscored 6-7 in second halves overall.</li>
            <li>Everton (A): conceded 83' & 90+6' to turn a 2-1 win into a 2-2 draw.</li>
            <li>Ipswich (H): conceded 90+1'. Brighton (H): conceded 45', 65', 70' to blow a 2-0 lead.</li>
        </ul></div>
        <div class="impact-box"><b>IMPACT:</b> Dropped 4 PL points from winning positions and an early EFL Cup exit.</div>
        <div class="explanation-box"><b>POSSIBLE EXPLANATION:</b> Physical fatigue in the double pivot plus substitutions that disrupt zonal communication in the backline under late direct play.</div>
        """
    },
    {
        "key": "i3", "tab_label": "3 · Set-Pieces",
        "title": "Issue 3: Acute Set-Piece & Dead-Ball Disorganization",
        "pitch_title": "Defensive Set-Piece Map — Zonal Gaps in United's Own Box (defending left goal)",
        "players": I3_PLAYERS,
        "layers": {"Unmarked zonal gaps": i3_zonal_gaps, "Opponent aerial threats": i3_opponents, "Goals conceded (spots)": i3_conceded},
        "board_summary": (
            "United defend a set-piece at the **left goal**. **Blue diamonds** are the opponent's aerial threats attacking the "
            "near and far post; the **red circles** are the zones United leave unmarked; the **gold stars** on the goal-line are "
            "goals actually conceded from dead balls (Hull 17' & 38', Everton 96'). The board shows plenty of bodies in the box "
            "but nobody tracking the danger runs into the red gaps."
        ),
        "prose": """
        <div class="problem-box"><b>PROBLEM:</b> Systematic failure to defend aerial dead-ball deliveries and clean second balls inside the 18-yard box.</div>
        <div class="evidence-box"><b>EVIDENCE:</b><ul>
            <li>Conceded 2 set-piece goals vs Hull (17' corner to Ajayi, 38' free-kick to Mendy).</li>
            <li>Set-piece scramble vs Ipswich (91') and deep set-piece cross vs Everton (96').</li>
            <li>High opponent xG per set-piece attempt despite limiting corner counts.</li>
        </ul></div>
        <div class="impact-box"><b>IMPACT:</b> Lets lower-tier opponents take early leads without open-play dominance, forcing United to chase low-block games.</div>
        <div class="explanation-box"><b>POSSIBLE EXPLANATION:</b> Miscommunication in Carrick's hybrid zonal/man scheme between CBs (Maguire, Martínez, Heaven) and Lammens, plus no dominant second-ball winner.</div>
        """
    },
    {
        "key": "i4", "tab_label": "4 · Bruno Reliance",
        "title": "Issue 4: Bruno Fernandes Over-Reliance & Frontline Integration Friction",
        "pitch_title": "Attacking-Third Map — Bruno & Cunha Crowding the #10 Space (attacking L→R)",
        "players": I4_PLAYERS,
        "layers": {"Bruno–Cunha overlap zone": i4_overlap, "Passing dependency network": i4_dependency, "Vacated box presence": i4_empty_box},
        "board_summary": (
            "United attack **left → right**. The **orange circle** is the congested #10 zone where **Bruno and Cunha occupy the "
            "same space**; the **teal arrows** show how nearly every attack is funnelled through Bruno; the **dotted blue box** is "
            "the penalty area left with only Šeško in it. When opponents mark Bruno out of this zone (Hull, City), the attack "
            "produces almost nothing."
        ),
        "prose": """
        <div class="problem-box"><b>PROBLEM:</b> Offensive output leans heavily on Bruno Fernandes, causing open-play sterility when low blocks restrict central #10 space.</div>
        <div class="evidence-box"><b>EVIDENCE:</b><ul>
            <li>Bruno created/scored 38.5% of goals (4G, 1A).</li>
            <li>When Bruno was held to 0 G/A (Hull 0-2, City 0-1), United scored 0 despite 33 shots & 12 corners combined.</li>
            <li>Cunha: 1 goal in 5 starts; Šeško: 2 goals in 2 starts.</li>
        </ul></div>
        <div class="impact-box"><b>IMPACT:</b> Unable to break low blocks or beat 10-man City (51% possession, red card in 23').</div>
        <div class="explanation-box"><b>POSSIBLE EXPLANATION:</b> Tension between Cunha's deep-dropping link play (crowding Bruno) and Šeško's box presence (isolating midfield when pressing).</div>
        """
    },
]

def render_issue_board(issue):
    """Render one issue: layer toggles, interactive pitch (click-to-inspect), player panel, and prose."""
    st.markdown(f"### {issue['title']}")

    layer_labels = list(issue["layers"].keys())
    active = st.multiselect(
        "🎛️ Tactical layers to display:",
        options=layer_labels, default=layer_labels, key=f"layers_{issue['key']}"
    )

    # Build the figure
    fig = go.Figure()
    add_pitch(fig)
    for lab in layer_labels:
        if lab in active:
            issue["layers"][lab](fig)
    add_players(fig, issue["players"])
    finalize_pitch(fig, issue["pitch_title"])

    col_pitch, col_info = st.columns([3, 1.5])
    with col_pitch:
        event = st.plotly_chart(
            fig, use_container_width=True, key=f"board_{issue['key']}",
            on_select="rerun", selection_mode="points"
        )
    with col_info:
        st.markdown("#### 🔍 Player Inspector")

        # Primary control: player picker (always works). Bonus: clicking a marker also selects.
        board_players = [c[3] for c in issue["players"]]
        picked = st.selectbox(
            "Pick a player (or click a marker):",
            options=["— select —"] + board_players, index=0, key=f"pick_{issue['key']}"
        )

        sel_name = None
        # 1) Prefer a live marker click, if the click registered a point
        try:
            pts = event["selection"]["points"] if event and "selection" in event else []
            if pts:
                cd = pts[-1].get("customdata")
                if cd:
                    sel_name = cd[0]
        except Exception:
            sel_name = None
        # 2) Otherwise use the dropdown selection
        if not sel_name and picked in board_players:
            sel_name = picked

        if sel_name:
            prow = df_players[df_players["Player"] == sel_name]
            if not prow.empty:
                r = prow.iloc[0]
                st.markdown(f"<div class='player-card'><b style='font-size:16px;color:#fff'>{r['Player']}</b> "
                            f"<span style='color:#8b92a5'>· {r['Pos']}</span></div>", unsafe_allow_html=True)
                m1, m2 = st.columns(2)
                m1.metric("Goals", int(r["Goals"]))
                m2.metric("Assists", int(r["Assists"]))
                m3, m4 = st.columns(2)
                m3.metric("Minutes", int(r["Mins"]))
                m4.metric("xG Contrib", f"{r['xG_Contrib']:.1f}")
                st.caption(f"**Role:** {r['Primary_Role']}")
                st.info(r["Tactical_Impact"])
        else:
            st.caption("👆 Pick a player above (or click a **red marker** on the pitch) to see their season stats and tactical role.")
        st.markdown("---")
        st.markdown("**Legend**")
        st.caption("🔴 United XI  ·  🔷 Opponent threat  ·  Shaded zones = structural flaws  ·  Arrows = runs/passes")

    # "How to read this board" — ties the map back to the issue before the analysis boxes
    st.markdown("#### 🧭 How to read this board")
    st.info(issue["board_summary"])
    st.caption("Positions are an illustrative model of United's typical shape in this phase — not a literal tracking snapshot of one moment.")

    st.markdown("#### The analysis")
    st.markdown(issue["prose"], unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4. SIDEBAR FILTERS
# ------------------------------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg", width=80)
st.sidebar.title("MUFC Analytics Control")
st.sidebar.markdown("**Season 2026/27 Investigation**")
st.sidebar.markdown("---")

comp_filter = st.sidebar.multiselect("Filter Competition", options=df_matches["Competition"].unique(), default=df_matches["Competition"].unique())
venue_filter = st.sidebar.multiselect("Filter Venue", options=df_matches["Venue"].unique(), default=df_matches["Venue"].unique())
opp_filter = st.sidebar.multiselect("Filter Opponent Strength", options=df_matches["Opponent_Category"].unique(), default=df_matches["Opponent_Category"].unique())

filtered_df = df_matches[
    (df_matches["Competition"].isin(comp_filter)) &
    (df_matches["Venue"].isin(venue_filter)) &
    (df_matches["Opponent_Category"].isin(opp_filter))
]

st.sidebar.markdown("---")
st.sidebar.info("""
**Executive Briefing**:
Manchester United has managed only **2 wins in 6 competitive matches** (1W-1D-2L in Premier League, 13th place).

Despite strong underlying possession (57.7% avg) and xG (12.91 generated), severe structural vulnerabilities in **rest defense**, **set-piece organization**, and **second-half collapses** have severely undermined Michael Carrick's side.
""")

# ------------------------------------------------------------------------------
# 5. DASHBOARD HEADER & TITLE
# ------------------------------------------------------------------------------
st.markdown('<div class="kicker">● UNITED INTEL · TACTICAL LAB // 2026/27 · MATCHDAYS 1–6</div>', unsafe_allow_html=True)
st.title("Manchester United 2026/27 Tactical Investigation")
st.markdown('<p style="color:#94A3B8; font-size:1.05rem; max-width:70ch;">Analysing the root causes of a poor start — where dominant territorial control has turned into self-inflicted matchday defeats.</p>', unsafe_allow_html=True)
st.markdown("---")

if filtered_df.empty:
    st.warning("No match data matches your selected filters. Please adjust the sidebar filters.")
    st.stop()

# ------------------------------------------------------------------------------
# 6. DASHBOARD TABS
# ------------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Executive Summary",
    "🗓️ Match Results & Form",
    "⚔️ Attacking Analytics",
    "🛡️ Defensive & Transition Deficiencies",
    "🏃 Player Performance Matrix",
    "🔎 Final Investigation & Tactics Boards",
    "📑 Data Methodology"
])

# ==============================================================================
# TAB 1: EXECUTIVE SUMMARY
# ==============================================================================
with tab1:
    st.subheader("Executive KPI Overview")
    total_matches = len(filtered_df)
    wins = (filtered_df["Result"] == "Win").sum()
    draws = (filtered_df["Result"] == "Draw").sum()
    losses = (filtered_df["Result"] == "Loss").sum()
    gf = filtered_df["GF"].sum(); ga = filtered_df["GA"].sum(); gd = gf - ga
    total_xg = filtered_df["xG"].sum(); total_xga = filtered_df["xGA"].sum()
    avg_poss = filtered_df["Possession"].mean()
    win_pct = (wins / total_matches * 100) if total_matches > 0 else 0

    r1c1, r1c2, r1c3 = st.columns(3)
    r1c1.metric("Record (W-D-L)", f"{wins}-{draws}-{losses}", f"{win_pct:.0f}% win rate",
                help="Wins–Draws–Losses across the matches currently shown by the sidebar filters.")
    r1c2.metric("Goals: For – Against", f"{gf} – {ga}", f"Goal difference {gd:+d}",
                help="Total goals United scored vs conceded in the filtered matches.")
    r1c3.metric("Premier League Standing", "13th", "4 pts · 1W-1D-2L",
                help="League position (Premier League fixtures only, not affected by the filters).")

    r2c1, r2c2, r2c3 = st.columns(3)
    r2c1.metric("xG created", f"{total_xg:.2f}", f"{gf - total_xg:+.2f} goals vs xG",
                help="Expected Goals — the quality-weighted total of chances United CREATED. "
                     "The sub-figure is actual goals minus xG: positive = finishing ABOVE the chances created.")
    r2c2.metric("xG conceded (xGA)", f"{total_xga:.2f}", f"{ga - total_xga:+.2f} goals vs xGA",
                delta_color="inverse",
                help="Expected Goals Against — the quality of chances United GAVE UP. "
                     "The sub-figure is actual goals conceded minus xGA: positive (red) = conceding MORE than the chances warranted.")
    r2c3.metric("Avg possession", f"{avg_poss:.1f}%", "Territorial control",
                help="Average share of the ball across the filtered matches.")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Match Results Breakdown")
        res_counts = filtered_df["Result"].value_counts().reset_index()
        res_counts.columns = ["Result", "Count"]
        color_map = {"Win": "#10B981", "Draw": "#F59E0B", "Loss": "#EF4444"}
        fig_res = px.pie(res_counts, values="Count", names="Result", color="Result",
                         color_discrete_map=color_map, hole=0.4, title="Distribution of Results")
        fig_res.update_traces(hovertemplate="<b>%{label}</b><br>%{value} match(es) · %{percent}<extra></extra>")
        style_chart(fig_res)
        st.plotly_chart(fig_res, use_container_width=True)
    with c2:
        st.markdown("#### xG vs xGA Comparison per Match")
        fig_xg = go.Figure()
        fig_xg.add_trace(go.Bar(x=filtered_df["Opponent"], y=filtered_df["xG"], name="xG created", marker_color="#10B981",
                                hovertemplate="<b>%{x}</b><br>xG created: %{y:.2f}<extra></extra>"))
        fig_xg.add_trace(go.Bar(x=filtered_df["Opponent"], y=filtered_df["xGA"], name="xG conceded", marker_color="#EF4444",
                                hovertemplate="<b>%{x}</b><br>xG conceded: %{y:.2f}<extra></extra>"))
        fig_xg.update_layout(barmode="group", title="xG Created vs xG Conceded (per match)", xaxis_title="Opponent", yaxis_title="Expected Goals")
        style_chart(fig_xg)
        st.plotly_chart(fig_xg, use_container_width=True)

    st.markdown("---")
    st.markdown("""
    ### Key Executive Findings
    1. **Dominant Underlying xG Creation**: Manchester United generated **12.91 total xG** across 6 matches (**2.15 xG/game**), heavily skewed by the 5-2 win vs Ipswich (4.77 xG) and 4-0 vs Sabah FK (3.54 xG).
    2. **Catastrophic Defensive Efficiency**: Surrendered **10 actual goals from just 7.87 xGA** (opponents scored 10 on 20 shots on target — 50% conversion).
    3. **Possession Paradox**: Averaged **57.7% possession**, yet failed to win any game where they conceded first.
    """)

# ==============================================================================
# TAB 2: MATCH RESULTS & FORM TRACKER
# ==============================================================================
with tab2:
    st.subheader("Match-by-Match Performance Breakdown")
    display_cols = ["Date", "Opponent", "Competition", "Venue", "Result", "GF", "GA", "xG", "xGA", "Possession", "Shots", "Shots_On_Target", "Corners"]
    best_high = ["GF", "xG", "Possession", "Shots", "Shots_On_Target", "Corners"]  # higher = better
    best_low = ["GA", "xGA"]                                                        # lower = better
    styled_matches = (
        filtered_df[display_cols].style
        .highlight_max(subset=best_high, color="#1e5631")
        .highlight_min(subset=best_low, color="#1e5631")
    )
    st.dataframe(styled_matches, use_container_width=True, hide_index=True)
    st.caption("🟢 **Green = United's best match** in that column across the fixtures shown — the most GF, xG, possession, shots, "
               "shots on target and corners, and the fewest goals (GA) and xG conceded (xGA).")
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Home vs Away Performance Split")
        home_away = df_matches.groupby("Venue")[["GF", "GA", "xG", "xGA", "Possession"]].mean().reset_index()
        fig_ha = go.Figure()
        fig_ha.add_trace(go.Bar(x=home_away["Venue"], y=home_away["GF"], name="Avg goals for", marker_color="#10B981",
                                hovertemplate="<b>%{x}</b><br>Avg goals FOR: %{y:.2f}<extra></extra>"))
        fig_ha.add_trace(go.Bar(x=home_away["Venue"], y=home_away["GA"], name="Avg goals against", marker_color="#EF4444",
                                hovertemplate="<b>%{x}</b><br>Avg goals AGAINST: %{y:.2f}<extra></extra>"))
        fig_ha.update_layout(barmode="group", title="Average Goals per Match: Home vs Away",
                             xaxis_title="Venue", yaxis_title="Avg goals per match")
        style_chart(fig_ha)
        st.plotly_chart(fig_ha, use_container_width=True)
    with col_b:
        st.markdown("#### First Half vs Second Half Performance Split")
        half_data = pd.DataFrame({
            "Half": ["1st Half", "2nd Half"],
            "Goals_Scored": [filtered_df["1st_Half_GF"].sum(), filtered_df["2nd_Half_GF"].sum()],
            "Goals_Conceded": [filtered_df["1st_Half_GA"].sum(), filtered_df["2nd_Half_GA"].sum()]
        })
        fig_half = go.Figure()
        fig_half.add_trace(go.Bar(x=half_data["Half"], y=half_data["Goals_Scored"], name="Goals scored", marker_color="#10B981",
                                  hovertemplate="<b>%{x}</b><br>Goals scored: %{y}<extra></extra>"))
        fig_half.add_trace(go.Bar(x=half_data["Half"], y=half_data["Goals_Conceded"], name="Goals conceded", marker_color="#EF4444",
                                  hovertemplate="<b>%{x}</b><br>Goals conceded: %{y}<extra></extra>"))
        fig_half.update_layout(barmode="group", title="Goal Distribution by Half (Critical Second-Half Collapse)",
                               xaxis_title="Match half", yaxis_title="Total goals")
        style_chart(fig_half)
        st.plotly_chart(fig_half, use_container_width=True)

    st.markdown("""
    > **Crucial Form Pattern**: First-half goal differential is **+2 (6 GF, 4 GA)**; second-half collapses to **+1 (7 GF, 6 GA)**, driven by late concessions (83' & 96' vs Everton, 91' vs Ipswich, 65' & 70' vs Brighton).
    """)

# ==============================================================================
# TAB 3: ATTACKING ANALYTICS
# ==============================================================================
with tab3:
    st.subheader("Attacking Dynamics & Offensive Output")
    col_att1, col_att2 = st.columns(2)
    with col_att1:
        st.markdown("#### Shot Volume & Touches in Opposition Box")
        fig_shots = go.Figure()
        fig_shots.add_trace(go.Scatter(x=filtered_df["Opponent"], y=filtered_df["Shots"], name="Total shots",
                                       mode="lines+markers", line=dict(color="#10B981", width=3),
                                       hovertemplate="<b>%{x}</b><br>Total shots: %{y}<extra></extra>"))
        fig_shots.add_trace(go.Scatter(x=filtered_df["Opponent"], y=filtered_df["Box_Touches"], name="Opposition box touches",
                                       mode="lines+markers", line=dict(color="#38BDF8", width=3, dash="dash"),
                                       hovertemplate="<b>%{x}</b><br>Opp. box touches: %{y}<extra></extra>"))
        fig_shots.update_layout(title="Shot Generation vs Opposition Box Penetration",
                                xaxis_title="Opponent", yaxis_title="Count")
        style_chart(fig_shots)
        st.plotly_chart(fig_shots, use_container_width=True)
    with col_att2:
        st.markdown("#### Top Goal Contributors")
        top_contrib = df_players.sort_values(by="Goals", ascending=False).head(7)
        fig_top = px.bar(top_contrib, x="Player", y=["Goals", "Assists"], title="Direct Goal Contributions (Goals & Assists)",
                         color_discrete_sequence=["#FF2D3B", "#F59E0B"], labels={"value": "Count", "variable": "Metric"})
        fig_top.update_traces(hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>")
        fig_top.update_layout(xaxis_title="Player", yaxis_title="Count", legend_title_text="")
        style_chart(fig_top)
        st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("---")
    st.markdown("### Tactical Focus: Bruno Fernandes Centricity vs Central Forward Dilemma")
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Bruno Fernandes Dependency</div>
            <div class="metric-value">38.5% Direct Goal Share</div>
            <p style="color:#d0d0d0; font-size:13px; margin-top:8px;">
            Bruno Fernandes has scored <b>4 goals and 1 assist</b> in 6 appearances. With spatial freedom (hat-trick vs Ipswich), United's xG reaches elite levels (>3.5 xG). When low blocks restrict his central space (Hull, City), United scored <b>0 goals from open play</b>.
            </p>
        </div>""", unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Matheus Cunha vs Benjamin Šeško Profile</div>
            <div class="metric-value">Cunha (1G 1A) vs Šeško (2G)</div>
            <p style="color:#d0d0d0; font-size:13px; margin-top:8px;">
            <b>Cunha (5 starts)</b> drops deep to link with Bruno, reducing central box presence. <b>Šeško (2 starts)</b> offers an authentic box target but limits central press resistance. The dual-forward setup succeeded vs Sabah but exposed midfield cover domestically.
            </p>
        </div>""", unsafe_allow_html=True)

# ==============================================================================
# TAB 4: DEFENSIVE & TRANSITION DEFICIENCIES
# ==============================================================================
with tab4:
    st.subheader("Defensive Vulnerabilities & Transition Analysis")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("#### Shot Conversion Conceded (Opposition Clinicality)")
        fig_opp = go.Figure()
        fig_opp.add_trace(go.Bar(x=filtered_df["Opponent"], y=filtered_df["Opp_Shots"], name="Opponent total shots", marker_color="#38BDF8",
                                 hovertemplate="<b>%{x}</b><br>Opponent shots: %{y}<extra></extra>"))
        fig_opp.add_trace(go.Bar(x=filtered_df["Opponent"], y=filtered_df["GA"], name="Actual goals conceded", marker_color="#EF4444",
                                 hovertemplate="<b>%{x}</b><br>Goals conceded: %{y}<extra></extra>"))
        fig_opp.update_layout(barmode="group", title="Opponent Shots vs Actual Goals Conceded",
                              xaxis_title="Opponent", yaxis_title="Count")
        style_chart(fig_opp)
        st.plotly_chart(fig_opp, use_container_width=True)
    with d2:
        st.markdown("#### Late Goal Concessions Timeline")
        timeline_data = pd.DataFrame([
            {"Fixture": "Hull City (A)", "Min": "17' & 38'", "Type": "Set-Piece Breakdown", "Impact": "Conceded twice early; lost 0-2"},
            {"Fixture": "Ipswich Town (H)", "Min": "90+1'", "Type": "Late Defensive Scramble", "Impact": "Conceded late; won 5-2"},
            {"Fixture": "Everton (A)", "Min": "83' & 90+6'", "Type": "Rest Defense Collapse", "Impact": "Surrendered 2-1 lead; drew 2-2"},
            {"Fixture": "Brighton (H)", "Min": "45', 65', 70'", "Type": "Midfield Distance Separation", "Impact": "Blew 2-0 lead; lost 2-3"}
        ])
        st.table(timeline_data)

    st.markdown("---")
    st.markdown("### Core Defensive Factors")
    df_c1, df_c2, df_c3 = st.columns(3)
    with df_c1:
        st.markdown("""
        **1. Rest Defense Defects**
        * Advancing full-backs (Shaw, Dorgu, Dalot) high into a 5-man front leaves the double pivot (**Tielemans + Mainoo/Santos**) covering huge lateral ground.
        * Opponents exploit vacant half-spaces on turnovers.
        """)
    with df_c2:
        st.markdown("""
        **2. Key Injury Absences**
        * **Carlos Baleba & Manuel Ugarte**: no pure physical DM destroyers to break up counters.
        * **Matthijs de Ligt**: back injury leaves young Heaven/Yoro alongside Maguire/Martínez.
        """)
    with df_c3:
        st.markdown("""
        **3. Set-Piece Inefficiencies**
        * Zonal marking disconnects (2 set-piece goals vs Hull; 1 vs Ipswich; late cross vs Everton).
        * No clear second-ball clearing assignments in box scrambles.
        """)

# ==============================================================================
# TAB 5: PLAYER PERFORMANCE MATRIX
# ==============================================================================
with tab5:
    st.subheader("22-Player Squad Performance & Positional Matrix")
    p_search = st.text_input("Search Player Name or Position", "")
    if p_search:
        filtered_players = df_players[
            df_players["Player"].str.contains(p_search, case=False) |
            df_players["Pos"].str.contains(p_search, case=False)
        ]
    else:
        filtered_players = df_players

    # Rank by minutes so the leftmost column is a meaningful 1..N rank, not a raw 0-based index
    table_players = filtered_players.sort_values(by="Mins", ascending=False).reset_index(drop=True).copy()
    table_players.insert(0, "Rank", range(1, len(table_players) + 1))
    st.dataframe(
        table_players.style.format({"xG_Contrib": "{:.1f}"}).highlight_max(subset=["Goals", "Assists", "Mins"], color="#1e5631"),
        use_container_width=True, hide_index=True
    )
    st.caption("Rows ranked by minutes played. 🟢 **Green = squad-leading value** for Goals, Assists and Minutes.")
    st.markdown("---")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown("#### Squad Minutes Distribution")
        fig_mins = px.bar(df_players.sort_values(by="Mins", ascending=True), y="Player", x="Mins", color="Pos",
                          orientation="h", title="Player Total Minutes Played", height=600)
        fig_mins.update_traces(hovertemplate="<b>%{y}</b><br>Minutes: %{x}<br>Position: %{fullData.name}<extra></extra>")
        fig_mins.update_layout(xaxis_title="Minutes played", yaxis_title="", legend_title_text="Position")
        style_chart(fig_mins)
        st.plotly_chart(fig_mins, use_container_width=True)
    with p_col2:
        st.markdown("#### Position-by-Position xG Contribution")
        fig_pos = px.box(df_players, x="Pos", y="xG_Contrib", points="all", hover_data=["Player"],
                         title="xG Contribution Variance by Position Group")
        fig_pos.update_traces(hovertemplate="<b>%{customdata[0]}</b><br>Position: %{x}<br>xG contribution: %{y:.1f}<extra></extra>")
        fig_pos.update_layout(xaxis_title="Position group", yaxis_title="xG contribution")
        style_chart(fig_pos)
        st.plotly_chart(fig_pos, use_container_width=True)

# ==============================================================================
# TAB 6: FINAL INVESTIGATION — PER-ISSUE INTERACTIVE TACTICS BOARDS
# ==============================================================================
with tab6:
    st.subheader("Central Investigation: Why Has Manchester United Started Poorly?")
    st.markdown("#### *Each of the 4 core issues has its own interactive tactics board — toggle layers and click players to inspect them.*")
    st.info("💡 **How to use:** pick an issue tab below → toggle the **tactical layers** on/off → **pick a player** (or click a red marker) to open their season stats in the Player Inspector.")
    st.markdown("---")

    issue_tabs = st.tabs([iss["tab_label"] for iss in ISSUES])
    for it, issue in zip(issue_tabs, ISSUES):
        with it:
            render_issue_board(issue)

# ==============================================================================
# TAB 7: DATA METHODOLOGY & LIMITATIONS
# ==============================================================================
with tab7:
    st.subheader("Data Methodology & Technical Standards")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("### Data Sources")
        st.markdown("""
        * **Opta Match Scrapes**: Matchday feeds for all 6 competitive matches.
        * **Premier League Official Match Center**: Match metadata, referee records, event logs.
        * **FotMob & TNT Sports Match Analytics**: xG, xGA, shot maps, pass accuracy, player ratings.
        * **Wikipedia & Fandom Season Logs**: Historical context, transfers, squad registrations.
        """)
        st.markdown("### Key Metric Definitions")
        st.markdown("""
        * **Expected Goals (xG)**: Chance-quality measure (0.0–1.0 per shot).
        * **Rest Defense**: Positioning of non-attacking players in possession to prevent counters on turnover.
        * **Touches in Opposition Box**: Legal ball contacts inside the opponent's 18-yard box.
        """)
    with col_m2:
        st.markdown("### Benchmark Methodology & Assumptions")
        st.markdown("""
        * **Competitive Baseline**: 6 fixtures in 2026/27 (4 PL, 1 UCL, 1 EFL Cup).
        * **Possession Dominance Baseline**: >55% ball possession.
        * **Expected Goal Differential**: `xG - xGA`; positive = chance-creation superiority.
        """)
        st.markdown("### Data Limitations & Uncovered Areas")
        st.markdown("""
        * **PPDA**: Estimated from tackle/interception logs where full radar feeds were unavailable.
        * **GPS Tracking**: High-intensity sprint/distance data limited to sample matches.
        * **Field Tilt %**: Derived from box touches and final-third passes, not raw optical tracking.
        * **Tactics boards** are illustrative positional models, not literal event-level tracking snapshots.
        """)

st.markdown("---")
st.caption("Manchester United 2026/27 Football Analytics Portfolio Project | V3 Interactive Tactics Boards | Built with Python, Streamlit & Plotly")
