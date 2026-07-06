from datetime import date, datetime, timedelta, timezone

JST = timezone(timedelta(hours=9))

import streamlit as st
import style
from core import get_data, ensure_structure, aggregate
from storage import save_data
from utils import all_months, make_key, resolve_img_path

style.apply()
data = ensure_structure(get_data())

tab_names = {t["id"]: t["name"] for t in data["tabs"]}
tab_ids = list(tab_names.keys())

# ===== サイドバー =====
current_tab = st.sidebar.selectbox(
    "📂 カテゴリ",
    tab_ids,
    format_func=lambda x: tab_names[x]
)

months = all_months(data)
month_options = ["全月"] + months
selected_month = st.sidebar.selectbox(
    "📅 月フィルター",
    month_options,
    help="特定の月の回数だけ表示できます"
)
month_filter = None if selected_month == "全月" else selected_month

_raw_date = st.sidebar.date_input(
    "🗓 カウント日付",
    value=date.today(),
    max_value=date.today(),
    help="前日分を記録するときに変更"
)
count_date = _raw_date if isinstance(_raw_date, date) else date.today()

# ===== メイン =====
is_all_tab = current_tab == "all"

month_label = f"【{selected_month}】" if month_filter else "【全月合計】"
st.markdown(
    f"<h2 style='text-align:center'>💦 弱点一覧　<span style='font-size:0.6em;color:#ff80ab;'>{month_label}</span></h2>",
    unsafe_allow_html=True,
)

if is_all_tab:
    st.markdown(
        "<div style='text-align:center;color:#ff80ab;margin-bottom:1em;'>"
        "「全体」では合計を確認できます。カウントするにはカテゴリを選択してください。"
        "</div>",
        unsafe_allow_html=True,
    )
elif count_date < date.today():
    st.markdown(
        f"<div style='text-align:center;color:#ff80ab;margin-bottom:0.5em;'>"
        f"📅 {count_date.strftime('%Y-%m-%d')} の日付でカウントします"
        f"</div>",
        unsafe_allow_html=True,
    )

items = aggregate(data, current_tab, month_filter)

cols = st.columns(3)

for i, (name, val) in enumerate(items.items()):
    with cols[i % 3]:
        if is_all_tab:
            item = next((v for v in data["items"].values() if v["name"] == name), {})
        else:
            item = data["items"].get(make_key(name, current_tab), {})

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

        # 月別内訳
        counts = item.get("counts", {})
        if counts:
            breakdown = "　".join(
                f"<span style='color:#ff4081;font-size:0.75em;'>{m}: {c}回</span>"
                for m, c in sorted(counts.items(), reverse=True)[:3]
            )
        else:
            breakdown = ""

        st.markdown(f"""
<div class="ero-card">
  {img_html}
  <h3>🌸 {name}</h3>
  <div class="ero-count">{val}</div>
  <div class="ero-label">{'回（' + selected_month + '）' if month_filter else '回（累計）'}</div>
  {f'<div style="margin-top:0.4em;">{breakdown}</div>' if breakdown and not month_filter else ''}
</div>
""", unsafe_allow_html=True)

        if not is_all_tab:
            if st.button("💋 イった", key=f"btn_{name}"):
                key = make_key(name, current_tab)
                if key not in data["items"]:
                    data["items"][key] = {
                        "name": name, "tab": current_tab,
                        "counts": {}, "img": "", "points": 0
                    }
                counts_d = data["items"][key].get("counts")
                if not isinstance(counts_d, dict):
                    data["items"][key]["counts"] = {}
                m = count_date.strftime("%Y-%m")
                data["items"][key]["counts"][m] = data["items"][key]["counts"].get(m, 0) + 1
                time_str = datetime.combine(count_date, datetime.now(JST).time()).strftime("%Y-%m-%d %H:%M:%S")
                data["history"].append({"name": name, "tab": current_tab, "time": time_str})
                save_data(data)
                st.rerun()

st.divider()
st.markdown("<h3>📜 最近の記録</h3>", unsafe_allow_html=True)
for h in reversed(data["history"][-20:]):
    st.markdown(
        f"<span style='color:#ff80ab'>{h['time']}</span>"
        f"　<span style='color:#ffe0f0'>{h['name']}</span>"
        f"　<span style='color:#804060'>({h['tab']})</span>",
        unsafe_allow_html=True,
    )
