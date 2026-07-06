import streamlit as st
import style
from core import get_data, ensure_structure
from utils import active_items, all_months, img_to_html, tier

style.apply()
data = ensure_structure(get_data())

st.markdown("<h2 style='text-align:center'>🏆 敗北ランキング</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#ff80ab;margin-bottom:1em;'>"
    "あなたが一番とろけた弱点はどこかしら？ふふ。"
    "</p>",
    unsafe_allow_html=True,
)

# 月フィルター
months = all_months(data)
month_options = ["全月"] + months
selected_month = st.selectbox("📅 月フィルター", month_options, key="rank_month")
month_filter = None if selected_month == "全月" else selected_month

# 月別 or 累計で集計
def rank_by_month(data, month=None):
    points = {}
    for v in active_items(data).values():
        name = v["name"]
        counts = v.get("counts", {})
        total = counts.get(month, 0) if month else sum(counts.values())
        points[name] = points.get(name, 0) + total

    sorted_items = sorted(points.items(), key=lambda x: -x[1])
    n = len(sorted_items)
    return [
        {"name": name, "points": pts, "tier": tier(pts, i, n)}
        for i, (name, pts) in enumerate(sorted_items)
        if pts > 0
    ]

ranked = rank_by_month(data, month_filter)

tier_info = {
    "SS": ("👑", "#ffd700", "最愛の弱点。触れるだけでとろけちゃうのね"),
    "S":  ("🔥", "#ff4081", "すごく敏感。かわいいくらい弱いわ"),
    "A":  ("💋", "#ff80ab", "かなり危険。集中されると負けちゃうのね"),
    "B":  ("🌸", "#ce93d8", "じわじわ効いてくる弱点"),
    "C":  ("💜", "#b39ddb", "まだ粘れる……でもいつか負けるわ"),
    "D":  ("🖤", "#888",    "未開拓。これから一緒に育てましょ"),
}

if not ranked:
    no_data_msg = "選択した月の記録がまだありません" if month_filter else "記録がまだありません"
    st.markdown(
        f"<p style='text-align:center;color:#804060;'>{no_data_msg}</p>",
        unsafe_allow_html=True,
    )
else:
    cols = st.columns(2)
    for rank, info in enumerate(ranked, 1):
        name = info["name"]
        pts  = info["points"]
        t    = info["tier"]
        icon, color, label = tier_info.get(t, ("", "#fff", ""))

        item = next((v for v in data["items"].values() if v["name"] == name), {})
        img_html = img_to_html(
            item.get("img", ""),
            style="width:100%;border-radius:10px;margin-bottom:0.6em;object-fit:cover;max-height:200px;"
        )

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
  <div style="color:#ff80ab;font-weight:700;font-size:1.2em;">{pts} 敗北{'（' + selected_month + '）' if month_filter else ''}</div>
</div>
""", unsafe_allow_html=True)
