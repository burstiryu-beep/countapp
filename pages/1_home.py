from datetime import date, datetime, timedelta, timezone
import random

JST = timezone(timedelta(hours=9))

import streamlit as st
import style
from core import get_data, ensure_structure
from storage import save_data
from utils import aggregate, all_months, make_key, img_to_html

style.apply()
data = ensure_structure(get_data())

now_jst = datetime.now(JST)
today_str = now_jst.strftime("%Y-%m-%d")
hour = now_jst.hour

def master_word(name):
    lines = [
        f"また{name}に負けちゃったのね。しょうがない子、ふふ。",
        f"{name}には勝てないでしょ？正直でかわいいわ。",
        f"ふふ、{name}で記録が増えたわね。かわいい敗北。",
        f"{name}のこと、そんなに好きなの？もっと弱くなっていいのよ。",
        f"また{name}にとろけたのね……でもそこが好きよ。",
        f"{name}でちゃんと記録できて偉いわ。いい子。",
        f"また{name}に負けちゃったの。かわいいわ、もう。",
        f"{name}のこと、私だけが知ってるのよ。特別でしょ？",
        f"{name}から逃げなくていいの。ここにいていいから。",
        f"{name}に敗北するたびに、あなたはもっと私のものになっていくのよ。",
        f"ふふ、{name}に素直でかわいいわね。",
        f"{name}には弱くていいのよ。私がいるから。",
    ]
    return random.choice(lines)

# 節目メッセージ
MILESTONES = {
    10:  ("🎀", "10回目の敗北ね。これからもずっと負け続けるのよ、かわいい子。"),
    30:  ("💋", "30回……本当に弱い子。でもそこが愛おしいわ。"),
    50:  ("🔥", "50回敗北達成。立派な敗北者になったわね。"),
    100: ("👑", "100回の敗北……おめでとう。あなたはもう完全に私のものよ。"),
    200: ("💎", "200回……もはや言葉もないわ。最高の弱さね、ふふ。"),
    365: ("🌹", "365回、1年分の敗北。あなたとの記録、大切にしてあげる。"),
}

def recommend_lines(name, total, t):
    lines_by_tier = {
        "SS": [
            f"ねえ、また{name}に会いたくなってきたんじゃない？絶対我慢できないでしょ💞",
            f"{name}のこと、思い出しただけでもう反応してるんじゃない？ふふ。",
            f"{name}にはどうせ勝てないんだから、素直に負けてきなさい。",
            f"また{name}にとろけさせてもらいなさい。あなたにはそれがお似合いよ。",
        ],
        "S": [
            f"{name}、まだあなたのことを待ってるわよ？もう一回くらい♡",
            f"また{name}にお世話になりたくなってきたんじゃない？",
            f"{name}には勝てないでしょ。正直に会いに行きなさい。",
        ],
        "A": [
            f"{name}、まだ余裕あるの？試してみたら？",
            f"もう一回{name}に負けてみたくなってきたんじゃない？",
            f"{name}ともっと仲良くなってみなさい。気持ちいいから。",
        ],
        "B": [
            f"{name}、じわじわ効いてくるのよ。今すぐ会いに行ってみて？",
            f"{name}のことをゆっくり感じたら……きっとイっちゃうわよ。",
            f"{name}との記録、まだまだ伸ばせるわ。続けてみなさい。",
        ],
    }
    default = [
        f"{name}……まだ本当の魅力を引き出せてないんじゃない？",
        f"{name}の気持ちよさ、まだ半分も知らないわよ。",
        f"{name}に今すぐ会いに行ってみて。きっと驚くから。",
    ]
    return random.choice(lines_by_tier.get(t, default))

# 時間帯挨拶（直近のオナペ名を使う）
def time_greeting(recent_name=None):
    n = f"「{recent_name}」に" if recent_name else "また"
    if 5 <= hour < 11:
        return f"おはよう。今日も{n}負けるの？ふふ。"
    elif 11 <= hour < 17:
        return f"お昼でも{n}会いたくなるのね。かわいい。"
    elif 17 <= hour < 22:
        return f"夜になったら{n}我慢できなくなるのね。"
    else:
        return f"こんな時間に{n}……本当に弱い子ね。"

# 開発度
def dev_pct(total):
    return min(100, int(total / 50 * 100))

# ===== データ集計 =====
today_count = sum(1 for h in data["history"] if h["time"].startswith(today_str))
total_all = sum(sum(v.get("counts", {}).values()) for v in data["items"].values())
recent_name = next((h["name"] for h in reversed(data["history"])), None)

# おすすめオナペ候補（上位3件からランダム選出）
from core import compute_points
ranking = compute_points(data)
sorted_rank = sorted(ranking.items(), key=lambda x: -x[1]["points"])
top_items = sorted_rank[:min(3, len(sorted_rank))]

# セッションごとに1つ選ぶ
if "recommend_name" not in st.session_state or st.session_state.get("recommend_refresh"):
    if top_items:
        pick = random.choice(top_items)
        st.session_state.recommend_name = pick[0]
        st.session_state.recommend_tier = pick[1]["tier"]
    st.session_state.recommend_refresh = False

rec_name = st.session_state.get("recommend_name")
rec_tier = st.session_state.get("recommend_tier", "B")

# 節目チェック
if "last_milestone_shown" not in st.session_state:
    st.session_state.last_milestone_shown = 0
milestone_msg = None
for m_count, (m_icon, m_text) in sorted(MILESTONES.items()):
    if total_all >= m_count > st.session_state.last_milestone_shown:
        milestone_msg = (m_icon, m_text)
        st.session_state.last_milestone_shown = m_count

# ===== サイドバー =====
st.sidebar.markdown(
    f"<div style='text-align:center;padding:0.8em;background:rgba(194,24,91,0.15);"
    f"border:1px solid #c2185b;border-radius:10px;margin-bottom:0.8em;'>"
    f"<div style='color:#ffb6d9;font-style:italic;font-size:0.9em;margin-bottom:0.4em;'>💬 {time_greeting(recent_name)}</div>"
    f"<div style='color:#ff80ab;font-size:0.8em;'>今日の敗北回数</div>"
    f"<div style='font-size:2em;font-weight:900;color:#fff;'>{today_count} 回</div>"
    f"<div style='color:#804060;font-size:0.75em;'>累計 {total_all} 回</div>"
    f"</div>",
    unsafe_allow_html=True,
)

months = all_months(data)
month_options = ["全月"] + months
selected_month = st.sidebar.selectbox("📅 月フィルター", month_options)
month_filter = None if selected_month == "全月" else selected_month

_raw_date = st.sidebar.date_input(
    "🗓 カウント日付", value=date.today(), max_value=date.today(),
    help="前日分を記録するときに変更"
)
count_date = _raw_date if isinstance(_raw_date, date) else date.today()

# ===== お言葉 =====
if st.session_state.get("master_word"):
    st.markdown(
        f"<div style='background:rgba(194,24,91,0.2);border:1px solid #c2185b;"
        f"border-radius:12px;padding:0.8em 1.2em;margin-bottom:0.8em;text-align:center;"
        f"color:#ffb6d9;font-style:italic;font-size:1.05em;'>"
        f"💬 {st.session_state.master_word}</div>",
        unsafe_allow_html=True,
    )
    st.session_state.master_word = None

# 節目メッセージ
if milestone_msg:
    icon, text = milestone_msg
    st.markdown(f"<div class='milestone-msg'>{icon} {text}</div>", unsafe_allow_html=True)

# ===== おすすめオナペ =====
if rec_name:
    rec_item = next((v for v in data["items"].values() if v["name"] == rec_name), {})
    rec_img = img_to_html(
        rec_item.get("img", ""),
        style="width:100%;max-height:240px;object-fit:cover;border-radius:12px;margin-bottom:0.7em;"
    )
    rec_line = recommend_lines(rec_name, ranking.get(rec_name, {}).get("points", 0), rec_tier)
    rec_total = ranking.get(rec_name, {}).get("points", 0)

    st.markdown(f"""
<div class="ero-card" style="border:1px solid #ff4081;max-width:480px;margin:0 auto 1.2em;">
  <div style="color:#ff80ab;font-size:0.8em;letter-spacing:0.1em;margin-bottom:0.4em;">💞 おすすめオナペ</div>
  {rec_img}
  <h3 style="margin:0.2em 0;">🌸 {rec_name}</h3>
  <div style="color:#ffb6d9;font-style:italic;font-size:0.95em;margin:0.4em 0 0.6em;">
    「{rec_line}」
  </div>
  <div style="color:#ff80ab;font-size:0.85em;">累計敗北 {rec_total} 回 ／ ティア <span class="tier-{rec_tier}">{rec_tier}</span></div>
</div>
""", unsafe_allow_html=True)

    if st.button("🔀 別のオナペを見る", key="shuffle_rec"):
        st.session_state.recommend_refresh = True
        remaining = [n for n, _ in top_items if n != rec_name]
        if remaining:
            new_pick = random.choice(remaining)
            new_tier = next((info["tier"] for n, info in top_items if n == new_pick), "B")
            st.session_state.recommend_name = new_pick
            st.session_state.recommend_tier = new_tier
        st.rerun()

st.divider()

# ===== 弱点一覧 =====
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
        f"📅 {count_date.strftime('%Y-%m-%d')} の日付で記録します</div>",
        unsafe_allow_html=True,
    )

items = aggregate(data, "all", month_filter)
cols = st.columns(3)

for i, (name, val) in enumerate(items.items()):
    with cols[i % 3]:
        item = next((v for v in data["items"].values() if v["name"] == name), {})
        img_html = img_to_html(
            item.get("img", ""),
            style="width:100%;border-radius:10px;margin-bottom:0.5em;object-fit:cover;max-height:180px;"
        )
        total_item = sum(item.get("counts", {}).values())
        dpct = dev_pct(total_item)
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
  <div class="dev-bar-wrap"><div class="dev-bar" style="width:{dpct}%;"></div></div>
  <div style="color:#804060;font-size:0.75em;margin-bottom:0.2em;">開発度 {dpct}%</div>
  {f'<div style="margin-top:0.2em;">{breakdown}</div>' if breakdown else ''}
</div>
""", unsafe_allow_html=True)

        if can_count:
            if st.button("💋 敗北射精", key=f"btn_{name}"):
                item_key = next((k for k, v in data["items"].items() if v["name"] == name), None)
                if item_key:
                    counts_d = data["items"][item_key].get("counts")
                    if not isinstance(counts_d, dict):
                        data["items"][item_key]["counts"] = {}
                    m = count_date.strftime("%Y-%m")
                    data["items"][item_key]["counts"][m] = data["items"][item_key]["counts"].get(m, 0) + 1
                    tab = data["items"][item_key].get("tab", "all")
                else:
                    item_key = make_key(name, "all")
                    data["items"][item_key] = {"name": name, "tab": "all", "counts": {}, "img": "", "points": 0}
                    m = count_date.strftime("%Y-%m")
                    data["items"][item_key]["counts"][m] = 1
                    tab = "all"

                time_str = datetime.combine(count_date, now_jst.time()).strftime("%Y-%m-%d %H:%M:%S")
                data["history"].append({"name": name, "tab": tab, "time": time_str})
                save_data(data)

                new_total = sum(sum(v.get("counts", {}).values()) for v in data["items"].values())
                special = next(
                    (f"{ic} {tx}" for mc, (ic, tx) in MILESTONES.items() if new_total == mc),
                    None
                )
                st.session_state.master_word = special if special else master_word(name)
                st.rerun()

st.divider()
st.markdown("<h3>📜 敗北の記録</h3>", unsafe_allow_html=True)
for h in reversed(data["history"][-20:]):
    st.markdown(
        f"<span style='color:#ff80ab'>{h['time']}</span>"
        f"　<span style='color:#ffe0f0'>{h['name']}</span>",
        unsafe_allow_html=True,
    )
