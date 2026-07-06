import streamlit as st
import style
from core import get_data, ensure_structure, compute_points
from utils import img_to_html

style.apply()
data = ensure_structure(get_data())

st.markdown("<h2 style='text-align:center'>🏆 敗北ランキング</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#ff80ab;margin-bottom:1.5em;'>"
    "あなたが一番とろけた弱点はどこかしら？ふふ。"
    "</p>",
    unsafe_allow_html=True,
)

ranking = compute_points(data)
sorted_rank = sorted(ranking.items(), key=lambda x: -x[1]["points"])

tier_info = {
    "SS": ("👑", "#ffd700", "最愛の弱点。触れるだけでとろけちゃうのね"),
    "S":  ("🔥", "#ff4081", "すごく敏感。かわいいくらい弱いわ"),
    "A":  ("💋", "#ff80ab", "かなり危険。集中されると負けちゃうのね"),
    "B":  ("🌸", "#ce93d8", "じわじわ効いてくる弱点"),
    "C":  ("💜", "#b39ddb", "まだ粘れる……でもいつか負けるわ"),
    "D":  ("🖤", "#888",    "未開拓。これから一緒に育てましょ"),
}

cols = st.columns(2)

for rank, (name, info) in enumerate(sorted_rank, 1):
    t = info["tier"]
    icon, color, label = tier_info.get(t, ("", "#fff", ""))
    pts = info["points"]

    item = next((v for v in data["items"].values() if v["name"] == name), {})
    img_html = img_to_html(item.get("img", ""), style="width:100%;border-radius:10px;margin-bottom:0.6em;object-fit:cover;object-position:top;max-height:200px;")

    with cols[(rank - 1) % 2]:
        st.markdown(f"""
<div class="ero-card" style="text-align:center;">
  {img_html}
  <div style="font-size:0.85em;color:#804060;margin-bottom:0.2em;">#{rank}</div>
  <h3 style="margin:0.1em 0;">🌸 {name}</h3>
  <div style="margin:0.3em 0;">
    <span class="tier-{t}" style="font-size:2em;">{t}</span>
    <span style="font-size:1.2em;">　{icon}</span>
  </div>
  <div style="color:{color};font-size:0.85em;font-style:italic;margin-bottom:0.4em;">{label}</div>
  <div style="color:#ff80ab;font-weight:700;font-size:1.2em;">{pts} 敗北</div>
</div>
""", unsafe_allow_html=True)
