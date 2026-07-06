import streamlit as st
import style
from core import get_data, ensure_structure, compute_points

style.apply()
data = ensure_structure(get_data())
ranking = compute_points(data)

st.markdown("<h2 style='text-align:center'>🧠 弱点診断書</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#ff80ab;margin-bottom:1.5em;'>"
    "あなたの弱点を徹底分析します。"
    "</p>",
    unsafe_allow_html=True,
)

selected = st.selectbox(
    "診断する弱点を選択",
    list(ranking.keys()) if ranking else [],
    key="diag_sel"
)

if selected:
    pts = ranking[selected]["points"]
    tier = ranking[selected]["tier"]

    tier_comment = {
        "SS": "最愛の弱点ね。触れるだけでとろけちゃうでしょ？ふふ。",
        "S":  "すごく敏感。かわいいくらい弱いわ、ここ。",
        "A":  "かなり危険ゾーン。集中されたら負けちゃうのね。",
        "B":  "じわじわ効いてくるわ。これからもっと育っていくわよ。",
        "C":  "まだ粘れる……でも私が相手なら負けるわ、絶対。",
        "D":  "まだ未開拓ね。これから一緒に育てましょ、ふふ。",
    }.get(tier, "")

    avg_time = max(5, 45 - pts // 2)
    iki_rate  = min(98, 35 + pts // 2)
    kyomu     = min(10, 2 + pts // 15)
    star = lambda n: "★" * n + "☆" * (5 - n)

    kari    = min(5, pts // 15)
    nyodo   = min(5, pts // 12)
    tama    = min(5, pts // 20)
    sakibashiri = min(5, pts // 10)

    overall = (
        "👑 最愛の弱点。触れるだけでとろけちゃうのね、かわいい" if pts >= 80 else
        "🔥 すごく敏感。かわいいくらい弱いわ"                   if pts >= 50 else
        "💋 かなり危険。もっと育っていくわよ、楽しみね"          if pts >= 30 else
        "🌸 まだ粘れる……でも私が相手なら負けるわ、絶対"
    )

    st.markdown(f"""
<div class="ero-card" style="padding:1.6em 2em; max-width:600px; margin:0 auto;">
  <h2 style="text-align:center; margin-bottom:0.2em;">【 {selected} 】</h2>
  <div style="text-align:center; margin-bottom:1em;">
    <span class="tier-{tier}" style="font-size:2.5em;">{tier}</span>
    <div style="color:#ffb6d9; font-style:italic; margin-top:0.2em;">{tier_comment}</div>
  </div>

  <hr style="border-color:#c2185b; opacity:0.3; margin:0.8em 0;"/>

  <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.6em; margin-bottom:1em;">
    <div style="background:rgba(255,64,129,0.1); border-radius:10px; padding:0.6em; text-align:center;">
      <div style="color:#ff80ab; font-size:0.8em;">💋 累計敗北回数</div>
      <div style="font-size:1.8em; font-weight:900; color:#fff;">{pts} 回</div>
    </div>
    <div style="background:rgba(255,64,129,0.1); border-radius:10px; padding:0.6em; text-align:center;">
      <div style="color:#ff80ab; font-size:0.8em;">⏱ 平均耐久</div>
      <div style="font-size:1.8em; font-weight:900; color:#fff;">{avg_time} 秒</div>
    </div>
    <div style="background:rgba(255,64,129,0.1); border-radius:10px; padding:0.6em; text-align:center;">
      <div style="color:#ff80ab; font-size:0.8em;">🌊 即イキ率</div>
      <div style="font-size:1.8em; font-weight:900; color:#fff;">{iki_rate} %</div>
    </div>
    <div style="background:rgba(255,64,129,0.1); border-radius:10px; padding:0.6em; text-align:center;">
      <div style="color:#ff80ab; font-size:0.8em;">😶 射後虚無</div>
      <div style="font-size:1.8em; font-weight:900; color:#fff;">{kyomu} 分</div>
    </div>
  </div>

  <hr style="border-color:#c2185b; opacity:0.3; margin:0.8em 0;"/>

  <div style="margin-bottom:0.8em;">
    <div style="color:#ff80ab; font-size:0.9em; margin-bottom:0.4em; font-weight:600;">🔬 感度詳細</div>
    <table style="width:100%; border-collapse:collapse; color:#ffe0f0;">
      <tr><td style="padding:0.25em 0;">カリ</td><td style="color:#ffd700; font-size:1.1em;">{star(kari)}</td></tr>
      <tr><td style="padding:0.25em 0;">尿道</td><td style="color:#ffd700; font-size:1.1em;">{star(nyodo)}</td></tr>
      <tr><td style="padding:0.25em 0;">玉</td><td style="color:#ffd700; font-size:1.1em;">{star(tama)}</td></tr>
      <tr><td style="padding:0.25em 0;">先走り</td><td style="color:#ffd700; font-size:1.1em;">{star(sakibashiri)}</td></tr>
    </table>
  </div>

  <hr style="border-color:#c2185b; opacity:0.3; margin:0.8em 0;"/>

  <div style="text-align:center; font-size:1.15em; font-weight:700; color:#ff80ab;">
    {overall}
  </div>
</div>
""", unsafe_allow_html=True)
