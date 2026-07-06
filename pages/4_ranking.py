import streamlit as st
import style
from core import get_data, ensure_structure, compute_points

style.apply()
data = ensure_structure(get_data())

st.markdown("<h2 style='text-align:center'>🏆 感度ランキング</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#ff80ab;margin-bottom:1.5em;'>"
    "あなたが最もイかされた弱点はどこ？"
    "</p>",
    unsafe_allow_html=True,
)

ranking = compute_points(data)
sorted_rank = sorted(ranking.items(), key=lambda x: -x[1]["points"])

tier_info = {
    "SS": ("👑", "#ffd700", "伝説級の弱点"),
    "S":  ("🔥", "#ff4081", "超敏感ゾーン"),
    "A":  ("💋", "#ff80ab", "かなり敏感"),
    "B":  ("🌸", "#ce93d8", "そこそこ敏感"),
    "C":  ("💜", "#b39ddb", "まあまあ"),
    "D":  ("🖤", "#888",    "まだ未開拓"),
}

for rank, (name, info) in enumerate(sorted_rank, 1):
    t = info["tier"]
    icon, color, label = tier_info.get(t, ("", "#fff", ""))
    pts = info["points"]

    st.markdown(f"""
<div class="ero-card" style="text-align:left; padding:1em 1.4em;">
  <div style="display:flex; align-items:center; gap:0.8em;">
    <span style="font-size:1.8em; min-width:1.8em; text-align:center;">{icon}</span>
    <div style="flex:1;">
      <div style="font-size:1.2em; font-weight:700; color:#ffe0f0;">
        #{rank}　{name}
      </div>
      <div style="font-size:0.85em; color:{color}; margin-top:0.1em;">{label}</div>
    </div>
    <div style="text-align:right;">
      <div class="tier-{t}" style="font-size:1.6em;">{t}</div>
      <div style="color:#ff80ab; font-weight:700; font-size:1.1em;">{pts} 回</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
