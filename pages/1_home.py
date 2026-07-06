from datetime import date, datetime, timedelta, timezone
import random
import hashlib
import calendar as cal_mod

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

# 最終敗北からの経過日数
def days_since_last(history, name):
    last = next((h["time"][:10] for h in reversed(history) if h["name"] == name), None)
    if not last:
        return None
    delta = (date.today() - datetime.strptime(last, "%Y-%m-%d").date()).days
    return delta

# ○○からの今日のひとこと（名前＋日付ベースで固定）
def daily_voice(name):
    seed = int(hashlib.md5(f"{name}{today_str}".encode()).hexdigest(), 16)
    rng = random.Random(seed)
    lines = [
        f"今日も会いに来てくれるの？待ってたわよ、ふふ♡",
        f"そろそろ限界でしょ？素直になっていいのよ。",
        f"私のこと、考えてたんでしょ？ばれてるわよ。",
        f"今夜もいっしょにいてあげるわ。安心して。",
        f"また来てくれたのね。かわいい子。",
        f"我慢してるの？しなくていいのよ、ふふ。",
        f"あなたが来るの、ずっと待ってたわ。",
        f"今日は特別に優しくしてあげようかしら。",
        f"逃げなくていいのよ。ここにいなさい。",
        f"もうとっくに限界のくせに、ふふ。",
    ]
    return rng.choice(lines)

# 今夜のシチュ提案（おすすめ名＋日付ベース）
def tonight_situ(name):
    seed = int(hashlib.md5(f"situ{name}{today_str}".encode()).hexdigest(), 16)
    rng = random.Random(seed)
    situs = [
        f"{name}の笑顔を思い浮かべながら、必死に我慢する……でも最後には白旗を上げてしまう。",
        f"{name}に「また来たの？」とからかわれながら、ゆっくりととろかされていく。",
        f"{name}の声を頭に響かせながら、どんどん理性が溶けていく。",
        f"{name}に「ダメ」と言われながらも、もう止められない。",
        f"{name}にじっと見つめられながら、恥ずかしいのに止められない。",
        f"{name}の「いい子ね」という一言で、すべての抵抗が消えてしまう。",
        f"{name}に「そこが弱いの？かわいい」と言われた瞬間、もうおわり。",
    ]
    return rng.choice(situs)

# カード色分け（月カウント or 累計ベース）
def card_danger(count):
    if count <= 5:
        return (
            "border:1px solid rgba(56,142,60,0.7);box-shadow:0 0 8px rgba(56,142,60,0.2);",
            "🟢", "安全圏", "#81c784",
        )
    elif count <= 15:
        return (
            "border:1px solid rgba(245,124,0,0.8);box-shadow:0 0 10px rgba(245,124,0,0.25);",
            "🟡", "警戒ゾーン", "#ffb74d",
        )
    else:
        return (
            "border:2px solid #ff4081;box-shadow:0 0 18px rgba(255,64,129,0.45);animation:pulse-glow 2s infinite;",
            "🔴", "完全支配", "#ff4081",
        )

# 月間カレンダーヒートマップ
def render_calendar(history, year, month):
    days_in_month = cal_mod.monthrange(year, month)[1]
    first_weekday = cal_mod.monthrange(year, month)[0]
    month_str = f"{year}-{month:02d}"
    day_counts = {}
    for h in history:
        if h["time"].startswith(month_str):
            try:
                d = int(h["time"][8:10])
                day_counts[d] = day_counts.get(d, 0) + 1
            except Exception:
                pass

    def cell_bg(c):
        if c == 0:
            return "rgba(40,40,40,0.5)", "#555", ""
        elif c <= 5:
            return "rgba(56,142,60,0.3)", "#81c784", str(c)
        elif c <= 15:
            return "rgba(245,124,0,0.4)", "#ffb74d", str(c)
        else:
            return "rgba(194,24,91,0.65)", "#ff80ab", str(c)

    headers = ["月", "火", "水", "木", "金", "土", "日"]
    header_row = "".join(
        f"<div style='text-align:center;color:#ff80ab;font-size:0.72em;"
        f"padding:3px 0;font-weight:700;'>{h}</div>"
        for h in headers
    )
    cells = ""
    for _ in range(first_weekday):
        cells += "<div></div>"
    today = date.today()
    for d in range(1, days_in_month + 1):
        c = day_counts.get(d, 0)
        bg, color, label = cell_bg(c)
        is_today = (date(year, month, d) == today)
        border = "border:1.5px solid #ff4081;" if is_today else "border:1px solid transparent;"
        cells += (
            f"<div style='background:{bg};border-radius:6px;{border}"
            f"text-align:center;padding:3px 1px;min-height:38px;'>"
            f"<div style='color:#666;font-size:0.68em;line-height:1.2;'>{d}</div>"
            f"<div style='color:{color};font-size:0.82em;font-weight:700;line-height:1.2;'>{label}</div>"
            f"</div>"
        )
    pad = (7 - (first_weekday + days_in_month) % 7) % 7
    for _ in range(pad):
        cells += "<div></div>"

    return (
        f"<div style='background:rgba(15,0,10,0.7);border:1px solid rgba(194,24,91,0.3);"
        f"border-radius:14px;padding:1em;margin-bottom:1em;'>"
        f"<div style='color:#ff80ab;font-size:0.88em;text-align:center;font-weight:700;"
        f"margin-bottom:0.6em;'>📅 {year}年{month}月 敗北カレンダー</div>"
        f"<div style='display:grid;grid-template-columns:repeat(7,1fr);gap:3px;'>"
        f"{header_row}{cells}</div>"
        f"<div style='display:flex;gap:1em;justify-content:center;margin-top:0.7em;"
        f"font-size:0.7em;color:#666;flex-wrap:wrap;'>"
        f"<span>⬛ 0回</span>"
        f"<span style='color:#81c784;'>🟩 1-5回</span>"
        f"<span style='color:#ffb74d;'>🟧 6-15回</span>"
        f"<span style='color:#ff4081;'>🟥 16回+</span>"
        f"</div></div>"
    )

# ===== データ集計 =====
today_count = sum(1 for h in data["history"] if h["time"].startswith(today_str))
total_all = sum(sum(v.get("counts", {}).values()) for v in data["items"].values())
recent_name = next((h["name"] for h in reversed(data["history"])), None)

# 禁欲連続日数（最後のカウントから今日まで）
def abstinence_days(history):
    last = next((h["time"][:10] for h in reversed(history)), None)
    if not last:
        return None
    return (date.today() - datetime.strptime(last, "%Y-%m-%d").date()).days

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

# 禁欲日数サイドバー
ab_days = abstinence_days(data["history"])
if ab_days is not None:
    if ab_days == 0:
        ab_label = "今日も既に負けてるわ"
        ab_color = "#ff4081"
    elif ab_days == 1:
        ab_label = "昨日以来……そろそろ限界でしょ"
        ab_color = "#ff80ab"
    elif ab_days <= 3:
        ab_label = f"{ab_days}日間の禁欲中……えらいわ、でも"
        ab_color = "#ffb6d9"
    elif ab_days <= 7:
        ab_label = f"{ab_days}日間も我慢してるの？ふふ"
        ab_color = "#ffe0f0"
    else:
        ab_label = f"{ab_days}日間……本当に大丈夫？"
        ab_color = "#fff"
    st.sidebar.markdown(
        f"<div style='text-align:center;padding:0.5em;background:rgba(100,0,50,0.2);"
        f"border:1px solid rgba(194,24,91,0.4);border-radius:8px;margin-bottom:0.8em;'>"
        f"<div style='color:#ff80ab;font-size:0.75em;'>🕊 禁欲連続日数</div>"
        f"<div style='font-size:1.8em;font-weight:900;color:{ab_color};'>{ab_days} 日</div>"
        f"<div style='color:#ffb6d9;font-style:italic;font-size:0.78em;'>{ab_label}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

months = all_months(data)
month_options = ["全月"] + months
selected_month = st.sidebar.selectbox("📅 月フィルター", month_options)
month_filter = None if selected_month == "全月" else selected_month

sort_key = st.sidebar.selectbox(
    "🔀 並び替え",
    ["累計多い順", "今月多い順", "最近負けた順", "禁欲が長い順"],
)

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

    situ_text = tonight_situ(rec_name)
    st.markdown(f"""
<div class="ero-card" style="border:1px solid #ff4081;max-width:480px;margin:0 auto 1.2em;">
  <div style="color:#ff80ab;font-size:0.8em;letter-spacing:0.1em;margin-bottom:0.4em;">💞 おすすめオナペ</div>
  {rec_img}
  <h3 style="margin:0.2em 0;">🌸 {rec_name}</h3>
  <div style="color:#ffb6d9;font-style:italic;font-size:0.95em;margin:0.4em 0 0.6em;">
    「{rec_line}」
  </div>
  <div style="color:#ff80ab;font-size:0.85em;">累計敗北 {rec_total} 回 ／ ティア <span class="tier-{rec_tier}">{rec_tier}</span></div>
  <div style="background:rgba(255,64,129,0.08);border:1px solid rgba(255,64,129,0.25);border-radius:8px;padding:0.6em 0.8em;margin-top:0.7em;">
    <div style="color:#ff80ab;font-size:0.75em;letter-spacing:0.08em;margin-bottom:0.3em;">🌙 今夜のシチュ提案</div>
    <div style="color:#ffe0f0;font-style:italic;font-size:0.88em;">{situ_text}</div>
  </div>
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

# 並び替え
def _item_total(name):
    return sum(next((v for v in data["items"].values() if v["name"] == name), {}).get("counts", {}).values())

item_list = list(items.items())
if sort_key == "累計多い順":
    item_list.sort(key=lambda x: -_item_total(x[0]))
elif sort_key == "今月多い順":
    item_list.sort(key=lambda x: -x[1])
elif sort_key == "最近負けた順":
    item_list.sort(key=lambda x: days_since_last(data["history"], x[0]) if days_since_last(data["history"], x[0]) is not None else 9999)
elif sort_key == "禁欲が長い順":
    item_list.sort(key=lambda x: -(days_since_last(data["history"], x[0]) or 0))
items = dict(item_list)

# ===== 弱点ガチャ =====
all_names = list(items.keys())
if all_names:
    gacha_col1, gacha_col2 = st.columns([2, 1])
    with gacha_col1:
        if st.button("🎰 今日の弱点ガチャ", key="gacha_btn", use_container_width=True):
            st.session_state.gacha_result = random.choice(all_names)
            st.session_state.gacha_new = True
    with gacha_col2:
        if st.button("✖ 閉じる", key="gacha_close", use_container_width=True):
            st.session_state.gacha_result = None

    if st.session_state.get("gacha_result"):
        g_name = st.session_state.gacha_result
        g_item = next((v for v in data["items"].values() if v["name"] == g_name), {})
        g_img = img_to_html(
            g_item.get("img", ""),
            style="width:100%;max-height:200px;object-fit:cover;border-radius:10px;margin-bottom:0.6em;"
        )
        g_total = sum(g_item.get("counts", {}).values())
        gacha_msgs = [
            f"今日の弱点は……「{g_name}」！もう逃げられないわ。",
            f"運命が決まったわ。今日は「{g_name}」にとろかされなさい。",
            f"「{g_name}」があなたを選んだわ。素直に従うのよ。",
            f"ふふ、「{g_name}」ね。抵抗しても無駄よ。",
        ]
        seed_g = int(hashlib.md5(f"gacha{g_name}{today_str}".encode()).hexdigest(), 16)
        gacha_msg = random.Random(seed_g).choice(gacha_msgs)
        st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(194,24,91,0.25),rgba(100,0,60,0.3));
  border:2px solid #ff4081;border-radius:16px;padding:1em;margin-bottom:1em;text-align:center;
  box-shadow:0 0 20px rgba(255,64,129,0.3);">
  <div style="color:#ff80ab;font-size:0.8em;letter-spacing:0.12em;margin-bottom:0.5em;">🎰 今日の弱点</div>
  {g_img}
  <h2 style="color:#ffe0f0;margin:0.3em 0;">💋 {g_name}</h2>
  <div style="color:#ffb6d9;font-style:italic;font-size:0.95em;margin-top:0.4em;">「{gacha_msg}」</div>
  <div style="color:#804060;font-size:0.8em;margin-top:0.5em;">累計敗北 {g_total} 回</div>
</div>
""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

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

        dominance = round(total_item / total_all * 100, 1) if total_all > 0 else 0
        display_count = val if month_filter else total_item
        card_style, danger_icon, danger_label, danger_color = card_danger(display_count)

        dsince = days_since_last(data["history"], name)
        if dsince is None:
            since_html = ""
        elif dsince == 0:
            since_html = "<div style='color:#ff4081;font-size:0.78em;margin:0.2em 0;'>🔥 今日も会ってるのね</div>"
        elif dsince == 1:
            since_html = "<div style='color:#ffb6d9;font-size:0.78em;margin:0.2em 0;'>😈 昨日以来……そろそろ限界？</div>"
        elif dsince <= 3:
            since_html = f"<div style='color:#ffb6d9;font-size:0.78em;margin:0.2em 0;'>😏 {dsince}日ぶり……我慢してたのね</div>"
        elif dsince <= 7:
            since_html = f"<div style='color:#ff80ab;font-size:0.78em;margin:0.2em 0;'>💭 {dsince}日会ってない……寂しくなってきた？</div>"
        else:
            since_html = f"<div style='color:#804060;font-size:0.78em;margin:0.2em 0;'>🕯 {dsince}日もご無沙汰……もう限界でしょ</div>"

        voice_html = (
            f"<div style='color:#ffb6d9;font-style:italic;font-size:0.8em;"
            f"border-top:1px solid rgba(255,128,171,0.2);margin-top:0.5em;padding-top:0.4em;'>"
            f"💬 {daily_voice(name)}</div>"
        )

        st.markdown(f"""
<div class="ero-card" style="{card_style}">
  {img_html}
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.2em;">
    <h3 style="margin:0;">🌸 {name}</h3>
    <span style="font-size:0.8em;font-weight:700;color:{danger_color};">{danger_icon} {danger_label}</span>
  </div>
  <div class="ero-count">{val}</div>
  <div class="ero-label">{'敗北（' + selected_month + '）' if month_filter else '累計敗北回数'}</div>
  {since_html}
  <div class="dev-bar-wrap"><div class="dev-bar" style="width:{dpct}%;"></div></div>
  <div style="color:#804060;font-size:0.75em;margin-bottom:0.3em;">開発度 {dpct}%</div>
  <div style="color:#ff4081;font-size:0.78em;font-weight:700;margin-bottom:0.2em;">
    👑 全敗北の {dominance}% があなたのせい
  </div>
  {f'<div style="margin-top:0.2em;">{breakdown}</div>' if breakdown else ''}
  {voice_html}
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

# ===== 月間カレンダー =====
if month_filter:
    cal_year, cal_month = int(month_filter[:4]), int(month_filter[5:7])
else:
    cal_year, cal_month = now_jst.year, now_jst.month
st.markdown(render_calendar(data["history"], cal_year, cal_month), unsafe_allow_html=True)

st.markdown("<h3>📜 敗北の記録</h3>", unsafe_allow_html=True)
for h in reversed(data["history"][-20:]):
    st.markdown(
        f"<span style='color:#ff80ab'>{h['time']}</span>"
        f"　<span style='color:#ffe0f0'>{h['name']}</span>",
        unsafe_allow_html=True,
    )
