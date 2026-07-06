import streamlit as st

CSS = """
<style>
/* ===== ベース ===== */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #120008 0%, #0d0018 50%, #120008 100%);
    color: #ffe0f0;
}
[data-testid="stHeader"] {
    background: transparent;
}

/* ===== サイドバー ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e0015 0%, #120010 100%);
    border-right: 1px solid #cc1477;
}
[data-testid="stSidebar"] * {
    color: #ffb6d9 !important;
}

/* ===== 見出し ===== */
h1, h2, h3 {
    color: #ff69b4 !important;
    text-shadow: 0 0 14px rgba(255,105,180,0.6);
    letter-spacing: 0.03em;
}
h1 { font-size: 2.2em !important; }

/* ===== ボタン ===== */
.stButton > button {
    background: linear-gradient(90deg, #c2185b, #ff4081) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 30px !important;
    font-weight: 700 !important;
    font-size: 1.05em !important;
    letter-spacing: 0.05em !important;
    padding: 0.45em 1.4em !important;
    box-shadow: 0 0 12px rgba(255,64,129,0.5) !important;
    transition: all 0.25s !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #ff4081, #ff80ab) !important;
    box-shadow: 0 0 24px rgba(255,64,129,0.8) !important;
    transform: scale(1.06) !important;
}

/* ===== メトリクス ===== */
[data-testid="metric-container"] {
    background: rgba(194,24,91,0.12) !important;
    border: 1px solid #c2185b !important;
    border-radius: 12px !important;
    padding: 0.6em 1em !important;
    box-shadow: 0 0 10px rgba(194,24,91,0.2) !important;
}
[data-testid="metric-container"] label {
    color: #ff80ab !important;
    font-weight: 600 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #fff !important;
    font-size: 2em !important;
    text-shadow: 0 0 8px rgba(255,128,171,0.7) !important;
}

/* ===== セレクトボックス / 入力 ===== */
[data-testid="stSelectbox"] > div,
[data-testid="stTextInput"] > div > div,
[data-testid="stDateInput"] > div > div {
    background: rgba(255,20,100,0.08) !important;
    border: 1px solid #c2185b !important;
    border-radius: 8px !important;
    color: #ffe0f0 !important;
}

/* ===== divider ===== */
hr {
    border-color: #c2185b !important;
    opacity: 0.4 !important;
}

/* ===== info / success ===== */
[data-testid="stAlert"] {
    background: rgba(194,24,91,0.15) !important;
    border-left: 4px solid #ff4081 !important;
    color: #ffb6d9 !important;
    border-radius: 8px !important;
}

/* ===== アイテムカード ===== */
.ero-card {
    background: linear-gradient(135deg, rgba(194,24,91,0.15), rgba(20,0,30,0.6));
    border: 1px solid #c2185b;
    border-radius: 16px;
    padding: 1em;
    margin-bottom: 0.8em;
    box-shadow: 0 0 16px rgba(194,24,91,0.2);
    text-align: center;
}
.ero-card h3 {
    margin: 0 0 0.3em 0;
    font-size: 1.2em;
}
.ero-count {
    font-size: 2.4em;
    font-weight: 900;
    color: #ff80ab;
    text-shadow: 0 0 12px rgba(255,128,171,0.8);
}
.ero-label {
    font-size: 0.85em;
    color: #ff4081;
    letter-spacing: 0.08em;
}

/* ===== ランキングバッジ ===== */
.tier-SS { color: #ffd700; text-shadow: 0 0 10px gold; font-size:1.4em; font-weight:900; }
.tier-S  { color: #ff4081; text-shadow: 0 0 8px #ff4081; font-size:1.2em; font-weight:700; }
.tier-A  { color: #ff80ab; font-weight:700; }
.tier-B  { color: #ce93d8; }
.tier-C  { color: #b39ddb; }
.tier-D  { color: #888; }

/* ===== スクロールバー ===== */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #120008; }
::-webkit-scrollbar-thumb { background: #c2185b; border-radius: 3px; }
</style>
"""

def apply():
    st.markdown(CSS, unsafe_allow_html=True)
