from datetime import date, datetime, timedelta, timezone
import random

JST = timezone(timedelta(hours=9))

import streamlit as st
import style
from core import get_data, ensure_structure
from storage import save_data
from utils import aggregate, all_months, make_key, resolve_img_path

style.apply()
data = ensure_structure(get_data())

# ===== お言葉リスト（甘マゾ） =====
MASTER_WORDS = [
    "またイっちゃったの？しょうがない子ね、ふふ。",
    "その弱点、ほんとうにかわいいわ。正直に言えたこと、褒めてあげる。",
    "ふふ、また記録が増えたわね。かわいい敗北。",
    "もっと弱くなっていいのよ？私が全部管理してあげるから。",
    "弱い子ね……でもそこが好きよ、ふふ。",
    "ちゃんと記録できて偉いわ。いい子。",
    "また負けちゃったのね。かわいいわ、もう。",
    "その弱点、私だけが知ってるのよ。特別でしょ？",
    "逃げなくていいの。ここにいていいから。",
    "敗北するたびに、あなたはもっと私のものになっていくのよ。",
    "ふふ、素直でかわいいわね。",
    "いいの、いいの。弱くていいのよ。私がいるから。",
]

# ===== 今日の敗北回数 =====
today_str = datetime.now(JST).strftime("%Y-%m-%d")
today_count = sum(1 for h in data["history"] if h["time"].startswith(today_str))

# ===== サイドバー =====
st.sidebar.markdown(
    f"<div style='text-align:center;padding:0.8em;background:rgba(194,24,91,0.15);"
    f"border:1px solid #c2185b;border-radius:10px;margin-bottom:1em;'>"
    f"<div style='color:#ff80ab;font-size:0.8em;'>今日の敗北回数</div>"
    f"<div style='font-size:2em;font-weight:900;color:#fff;'>{today_count} 回</div>"
    f"</div>",
    unsafe_allow_html=True,
)

months = all_months(data)
month_options = ["全月"] + months
selected_month = st.sidebar.selectbox(
    "📅 月フィルター",
    month_options,
    help="特定の月の敗北回数を表示"
)
month_filter = None if selected_month == "全月" else selected_month

_raw_date = st.sidebar.date_input(
    "🗓 カウント日付",
    value=date.today(),
    max_value=date.today(),
    help="前日分を記録するときに変更"
)
count_date = _raw_date if isinstance(_raw_date, date) else date.today()

# ===== お言葉表示 =====
if st.session_state.get("master_word"):
    st.markdown(
        f"<div style='background:rgba(194,24,91,0.2);border:1px solid #c2185b;"
        f"border-radius:12px;padding:0.8em 1.2em;margin-bottom:1em;text-align:center;"
        f"color:#ffb6d9;font-style:italic;font-size:1.05em;'>"
        f"💬 {st.session_state.master_word}"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.session_state.master_word = None

# ===== メイン =====
month_label = f"【{selected_month}】" if month_filter else "【全月合計】"
st.markdown(
    f"<h2 style='text-align:center'>🌸 弱点一覧　<span style='font-size:0.6em;color:#ff80ab;'>{month_label}</span></h2>",
    unsafe_allow_html=True,
)

can_count = month_filter is not None

if not can_count:
    st.markdown(
        "<div style='text-align:center;background:rgba(194,24,91,0.1);border:1px solid #c2185b;"
        "border-radius:10px;padding:0.6em;margin-bottom:0.8em;color:#ff80ab;'>"
        "📅 月を選択するとカウントできます"
        "</div>",
        unsafe_allow_html=True,
    )
elif count_date < date.today():
    st.markdown(
        f"<div style='text-align:center;color:#ff80ab;margin-bottom:0.5em;'>"
        f"📅 {count_date.strftime('%Y-%m-%d')} の日付で記録します"
        f"</div>",
        unsafe_allow_html=True,
    )

items = aggregate(data, "all", month_filter)

cols = st.columns(3)

for i, (name, val) in enumerate(items.items()):
    with cols[i % 3]:
        item = next((v for v in data["items"].values() if v["name"] == name), {})

        img_path = resolve_img_path(item.get("img", ""))
        img_html = ""
        if img_path:
            import base64
            try:
                with open(str(img_path), "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                ext = str(img_path).rsplit(".", 1)[-1].lower()
                mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
                img_html = f'<img src="data:{mime};base64,{b64}" style="width:100%;border-radius:10px;margin-bottom:0.5em;"/>'
            except Exception:
                pass

        counts = item.get("counts", {})
        breakdown = "　".join(
            f"<span style='color:#ff4081;font-size:0.75em;'>{m}: {c}回</span>"
            for m, c in sorted(counts.items(), reverse=True)[:3]
        ) if counts and not month_filter else ""

        st.markdown(f"""
<div class="ero-card">
  {img_html}
  <h3>🌸 {name}</h3>
  <div class="ero-count">{val}</div>
  <div class="ero-label">{'敗北（' + selected_month + '）' if month_filter else '累計敗北回数'}</div>
  {f'<div style="margin-top:0.4em;">{breakdown}</div>' if breakdown else ''}
</div>
""", unsafe_allow_html=True)

        item_key = item.get("_key") or next(
            (k for k, v in data["items"].items() if v["name"] == name), None
        )

        if can_count and st.button("💋 敗北射精", key=f"btn_{name}"):
            if item_key and item_key in data["items"]:
                counts_d = data["items"][item_key].get("counts")
                if not isinstance(counts_d, dict):
                    data["items"][item_key]["counts"] = {}
                m = count_date.strftime("%Y-%m")
                data["items"][item_key]["counts"][m] = data["items"][item_key]["counts"].get(m, 0) + 1
                tab = data["items"][item_key].get("tab", "all")
            else:
                # 新規（念のため）
                item_key = make_key(name, "all")
                data["items"][item_key] = {"name": name, "tab": "all", "counts": {}, "img": "", "points": 0}
                m = count_date.strftime("%Y-%m")
                data["items"][item_key]["counts"][m] = 1
                tab = "all"

            time_str = datetime.combine(count_date, datetime.now(JST).time()).strftime("%Y-%m-%d %H:%M:%S")
            data["history"].append({"name": name, "tab": tab, "time": time_str})
            save_data(data)
            st.session_state.master_word = random.choice(MASTER_WORDS)
            st.rerun()

st.divider()
st.markdown("<h3>📜 敗北の記録</h3>", unsafe_allow_html=True)
for h in reversed(data["history"][-20:]):
    st.markdown(
        f"<span style='color:#ff80ab'>{h['time']}</span>"
        f"　<span style='color:#ffe0f0'>{h['name']}</span>",
        unsafe_allow_html=True,
    )
