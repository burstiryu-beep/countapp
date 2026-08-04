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
today_jst = now_jst.date()          # UTC対策：常にJST日付を使う
today_str = today_jst.strftime("%Y-%m-%d")
hour = now_jst.hour

def master_word(name):
    lines = [
        f"また{name}に情けなく負けちゃったのね……ふふ、かわいいわ。",
        f"{name}の前じゃ、すぐとろけて射精しちゃうの？しょうがない子。",
        f"抵抗できずに出しちゃったのね。{name}に弱いの、バレバレよ。",
        f"ふふ、{name}で情けない顔してイったのね。見てたかったわ。",
        f"また白旗……{name}には勝てないまま、気持ちよく負けたね。",
        f"{name}に甘えて、ちんぽまで正直になっちゃったの。かわいい敗北。",
        f"我慢できなくて記録つけに来たの？{name}にメロメロで情けないわ。",
        f"とろけたあとの顔、想像できるわ。{name}に負けたあとって、いつもそう。",
        f"ふふ、また{name}にイかされてきたのね。弱いのに、ちゃんと報告できてえらい。",
        f"{name}のこと考えただけで負けたんでしょ？情けない……でも好きよ。",
        f"射精してからアプリ開くの、いちばんかわいいわ。{name}に屈した余韻、残ってるでしょ。",
        f"また{name}に甘やかされて敗北射精……幸せそうな負け方ね、ふふ。",
    ]
    return random.choice(lines)

# 節目メッセージ
MILESTONES = {
    10:  ("🎀", "10回目の情けない敗北ね。これからも、とろけて負けていいのよ。"),
    30:  ("💋", "30回……本当に弱い子。でもその情けなさ、愛おしいわ。"),
    50:  ("🔥", "50回敗北達成。立派な甘マゾになったわね、ふふ。"),
    100: ("👑", "100回の敗北……おめでとう。もう負け癖、かわいく決まってるわ。"),
    200: ("💎", "200回。言葉より先にちんぽが負けるタイプね……最高よ。"),
    365: ("🌹", "365回、1年分の甘い敗北。あなたの情けない記録、大切にしてあげる。"),
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
    delta = (today_jst - datetime.strptime(last, "%Y-%m-%d").date()).days
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
            "border:1px solid rgba(180,100,140,0.5);box-shadow:0 0 6px rgba(180,100,140,0.15);",
            "💋", "気になってるでしょ？ふふ", "#ce93d8",
        )
    elif count <= 15:
        return (
            "border:1px solid rgba(245,124,0,0.85);box-shadow:0 0 12px rgba(245,124,0,0.3);",
            "💞", "もう弱いのね", "#ffb74d",
        )
    else:
        return (
            "border:2px solid #ff4081;box-shadow:0 0 20px rgba(255,64,129,0.5);animation:pulse-glow 2s infinite;",
            "💞💋", "もう抵抗もできないね💞", "#ff4081",
        )

# 月間カレンダーヒートマップ（画像付き）
def render_calendar(history, year, month, items_data):
    days_in_month = cal_mod.monthrange(year, month)[1]
    first_weekday = cal_mod.monthrange(year, month)[0]
    month_str = f"{year}-{month:02d}"

    # name → base64 src をキャッシュ（ホバー拡大クラス付き）
    _img_cache = {}
    def _thumb(name):
        if name in _img_cache:
            return _img_cache[name]
        item = next((v for v in items_data.values() if v["name"] == name), {})
        tag = img_to_html(
            item.get("img", ""),
            style="width:26px;height:26px;object-fit:cover;border-radius:50%;",
            face_detect=False,
        )
        # class="cal-t" を付与してホバー拡大を有効化
        tag = tag.replace("<img ", '<img class="cal-t" ')
        _img_cache[name] = tag
        return tag

    # day → list of names（重複あり）
    day_entries: dict = {}
    for h in history:
        if h["time"].startswith(month_str):
            try:
                d = int(h["time"][8:10])
                day_entries.setdefault(d, []).append(h["name"])
            except Exception:
                pass

    def cell_style(c):
        if c == 0:
            return "rgba(35,35,35,0.5)", "border:1px solid transparent;"
        elif c == 1:
            return "rgba(56,142,60,0.28)", "border:1px solid rgba(56,142,60,0.5);"
        elif c == 2:
            return "rgba(245,124,0,0.32)", "border:1px solid rgba(245,124,0,0.6);"
        else:
            return "rgba(194,24,91,0.55)", "border:1px solid rgba(255,64,129,0.8);"

    headers = ["月", "火", "水", "木", "金", "土", "日"]
    header_row = "".join(
        f"<div style='text-align:center;color:#ff80ab;font-size:0.72em;"
        f"padding:3px 0;font-weight:700;'>{h}</div>"
        for h in headers
    )
    cells = ""
    for _ in range(first_weekday):
        cells += "<div></div>"
    for d in range(1, days_in_month + 1):
        entries = day_entries.get(d, [])
        c = len(entries)
        bg, bdr = cell_style(c)
        is_today = (date(year, month, d) == today_jst)
        if is_today:
            bdr = "border:1.5px solid #ff4081;"
        # 画像：最大3枚まで（重複含む）
        shown = entries[:3]
        extra = c - 3 if c > 3 else 0
        imgs_html = "".join(_thumb(n) for n in shown)
        if extra:
            imgs_html += f"<span style='color:#ff80ab;font-size:0.65em;'>+{extra}</span>"
        count_label = f"<div style='color:#ddd;font-size:0.7em;font-weight:700;'>{c}回</div>" if c > 0 else ""
        cells += (
            f"<div style='background:{bg};border-radius:6px;{bdr}"
            f"text-align:center;padding:4px 2px;min-height:56px;overflow:visible;'>"
            f"<div style='color:#666;font-size:0.65em;'>{d}</div>"
            f"<div style='display:flex;flex-wrap:wrap;justify-content:center;gap:1px;margin:2px 0;'>{imgs_html}</div>"
            f"{count_label}"
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
        f"<div style='display:grid;grid-template-columns:repeat(7,1fr);gap:4px;overflow:visible;'>"
        f"{header_row}{cells}</div>"
        f"<div style='display:flex;gap:1em;justify-content:center;margin-top:0.7em;"
        f"font-size:0.7em;color:#666;flex-wrap:wrap;'>"
        f"<span>⬛ 0回</span>"
        f"<span style='color:#81c784;'>🟩 1回</span>"
        f"<span style='color:#ffb74d;'>🟧 2回</span>"
        f"<span style='color:#ff80ab;'>🟥 3回+</span>"
        f"</div></div>"
    )

# 欲求蓄積度ゲージ（禁欲日数ベース）
def desire_gauge(days):
    if days is None:
        return 0, "#555", "まだ記録がないわ"
    if days == 0:
        return 10, "#f48fb1", "今日は既に一回負けてるわ♡"
    elif days == 1:
        return 36, "#f06292", "少し溜まってきたわよ？"
    elif days == 2:
        return 60, "#ffb74d", "だいぶ溜まってきてるわね"
    elif days == 3:
        return 80, "#ff7043", "もうかなり限界に近いわ♡"
    elif days <= 5:
        return 93, "#f44336", "もう抑えられないでしょ💞"
    else:
        return 99, "#c2185b", f"{days}日分……もう爆発寸前よ💋"

# 週間危険予報
def weekly_danger_html(history, today):
    wd_counts = {i: 0 for i in range(7)}
    for h in history:
        try:
            dt = datetime.strptime(h["time"], "%Y-%m-%d %H:%M:%S")
            wd_counts[dt.weekday()] += 1
        except Exception:
            pass
    max_c = max(wd_counts.values()) or 1
    monday = today - timedelta(days=today.weekday())
    day_labels = ["月", "火", "水", "木", "金", "土", "日"]
    cells = ""
    for i in range(7):
        d = monday + timedelta(days=i)
        c = wd_counts[i]
        pct = int(c / max_c * 100)
        if pct >= 75:
            bg, bdr, icon, lbl, col = "rgba(194,24,91,0.45)", "2px solid #ff4081", "🔥", "危険", "#ff4081"
        elif pct >= 40:
            bg, bdr, icon, lbl, col = "rgba(245,124,0,0.28)", "1px solid rgba(245,124,0,0.6)", "⚠️", "注意", "#ffb74d"
        else:
            bg, bdr, icon, lbl, col = "rgba(40,40,40,0.35)", "1px solid rgba(100,100,100,0.25)", "💤", "安全", "#555"
        is_today = (d == today)
        if is_today:
            bdr = "2px solid #ff80ab"
        cells += (
            f"<div style='flex:1;background:{bg};border:{bdr};border-radius:8px;"
            f"text-align:center;padding:0.45em 0.2em;'>"
            f"<div style='color:#ff80ab;font-size:0.72em;font-weight:700;'>{day_labels[i]}</div>"
            f"<div style='color:#666;font-size:0.62em;'>{d.month}/{d.day}</div>"
            f"<div style='font-size:1em;margin:2px 0;'>{icon}</div>"
            f"<div style='color:{col};font-size:0.65em;font-weight:700;'>{lbl}</div>"
            f"</div>"
        )
    peak = max(range(7), key=lambda i: wd_counts[i])
    comment = f"「{day_labels[peak]}曜日が最も危険な日ね。気をつけて……できれば、だけど♡」"
    return (
        f"<div style='background:rgba(15,0,10,0.6);border:1px solid rgba(194,24,91,0.3);"
        f"border-radius:12px;padding:0.8em;margin-bottom:1em;'>"
        f"<div style='color:#ff80ab;font-size:0.85em;font-weight:700;text-align:center;"
        f"margin-bottom:0.55em;'>📅 今週の危険予報</div>"
        f"<div style='display:flex;gap:4px;'>{cells}</div>"
        f"<div style='color:#ffb6d9;font-style:italic;font-size:0.82em;text-align:center;"
        f"margin-top:0.55em;'>{comment}</div>"
        f"</div>"
    )

# 敗北日記1行生成（シード固定）
def diary_line(h, month_count):
    name = h["name"]
    ts = h["time"]
    seed = int(hashlib.md5(ts.encode()).hexdigest(), 16)
    rng = random.Random(seed)
    try:
        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        date_lbl = f"{dt.month}月{dt.day}日（{'月火水木金土日'[dt.weekday()]}）"
        time_lbl = dt.strftime("%H:%M")
        hr = dt.hour
        tod = "深夜" if hr < 5 else ("朝" if hr < 11 else ("昼間" if hr < 17 else "夜"))
    except Exception:
        date_lbl, time_lbl, tod = ts[:10], ts[11:16], ""
    lines = [
        f"{tod}、また{name}に負けたのね。今月{month_count}回目よ。",
        f"{name}に{tod}から呼ばれたの？かわいいわ。",
        f"また{name}ね。{tod}でも我慢できなかったの。しょうがない子。",
        f"{tod}に{name}との闘いに完敗。素直でかわいい。",
        f"ふふ、{tod}に{name}ね。どうせ最初から負けるつもりだったでしょ。",
    ]
    return date_lbl, time_lbl, rng.choice(lines)

# ===== 試し: 開くだけで勃つモード（トグルOFFで完全に非表示）=====
def tease_wall_lines(name, ab_days, night=False, clean_day=False):
    lines = [
        f"ただ見に来ただけ？……いいのよ、{name}を見てなさい。",
        f"カウントしないつもり？ふふ、でも{name}の顔は見てるわね。",
        f"{name}……触らなくても、もう反応してるでしょ。",
        f"記録はしなくていいわ。まずは{name}をじっくり見て。",
        f"また開いちゃったの。{name}に会いたくなっただけ？かわいい。",
    ]
    if ab_days and ab_days >= 2:
        lines.append(f"{ab_days}日我慢してるのに、また{name}を見に来たのね……正直でかわいいわ。")
    if clean_day:
        lines.extend([
            f"今日はまだ負けてないのね。じゃあせめて{name}を見ていきなさい。",
            f"我慢の日？ふふ……{name}の顔だけでもいいのよ。",
            f"記録ゼロのくせに、{name}を見に来るなんて……かわいい矛盾ね。",
        ])
    if night:
        lines.extend([
            f"こんな時間に{name}……もう我慢のつもり、ないでしょ。",
            f"夜のあなた、{name}に弱いのバレバレよ。",
            f"{name}の顔、夜だと余計に効くでしょ？素直になりなさい。",
        ])
    return random.choice(lines)


def tease_memory_line(name, when_lbl):
    lines = [
        f"{when_lbl}、{name}のこの顔で負けたよね。覚えてる？",
        f"この日の{name}……思い出しただけで、また疼いてきたでしょ。",
        f"{when_lbl}の敗北。{name}にまた負けたくなってきたんじゃない？",
        f"記録を見に来たの？それとも{name}に会いたくて？ふふ。",
    ]
    return random.choice(lines)


def tease_gallery_whisper(name, night=False):
    lines = [
        f"{name}……眺めてるだけでもう十分？",
        f"触らなくていいのよ。でも目は離さないで。",
        f"{name}の顔、好きすぎて見るだけで負けそうね。",
    ]
    if night:
        lines.extend([
            f"夜に{name}を眺めてるの……かわいいわ。",
            f"{name}、もう頭の中いっぱいでしょ？",
        ])
    return random.choice(lines)


def tease_desire_extra(ab_days, d_pct):
    if ab_days is None:
        return "まだ記録がないわ……でも、見に来た時点で負けよ。"
    if ab_days == 0:
        return "今日もう一回？見てるだけでもう疼いてるでしょ。"
    if ab_days == 1:
        return "見るだけで溜まるのね。手は動かさなくていいわ……今は。"
    if ab_days <= 3:
        return f"{ab_days}日分……画面を開いただけで限界が近づいてるわよ。"
    if ab_days <= 7:
        return f"蓄積度 {d_pct}%。触らなくても、もう正直な顔してるわ。"
    return f"{ab_days}日我慢して開くなんて……見るだけでイキそうなんでしょ？"


def tease_predict_next(history, items_list, hour_now):
    """曜日・時間帯の傾向から『次に負ける相手』を断言。"""
    if not items_list:
        return None
    wd = today_jst.weekday()
    bucket = "深夜" if hour_now < 5 else ("朝" if hour_now < 11 else ("昼" if hour_now < 17 else "夜"))
    scores = {}
    for h in history:
        try:
            dt = datetime.strptime(h["time"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            continue
        name = h.get("name")
        if not name:
            continue
        score = 1
        if dt.weekday() == wd:
            score += 3
        hb = "深夜" if dt.hour < 5 else ("朝" if dt.hour < 11 else ("昼" if dt.hour < 17 else "夜"))
        if hb == bucket:
            score += 2
        scores[name] = scores.get(name, 0) + score
    if not scores:
        pick = random.choice(items_list)
        return pick.get("name"), pick, "まだデータが薄いけど……たぶんこの子ね。"
    best = max(scores.items(), key=lambda x: x[1])[0]
    item = next((v for v in items_list if v.get("name") == best), None)
    if item is None:
        item = {"name": best, "img": ""}
    lines = [
        f"今夜はたぶん「{best}」ね。逃げられないわよ。",
        f"{bucket}のあなたは「{best}」に弱いの、もう分かってるでしょ。",
        f"次に負ける相手は「{best}」。ふふ、予言してあげる。",
        f"「{best}」……また会いたくなってきたでしょ？素直に認めなさい。",
    ]
    return best, item, random.choice(lines)


def mirror_reply(choice, name):
    """鏡チェック。フェラ＋亀頭キスでイかせに来る甘マゾ煽り（長め・描写寄り）。"""
    if choice == "hard":
        lines = [
            (
                f"ふふ……もうこんなに硬いのね。{name}がゆっくり唇を寄せて、"
                f"先にちゅってしてから咥えたら……すぐ腰が引けちゃうでしょ。"
                f"逃げなくていいわ。口で温めて、キスして、情けなくイかせてあげる。"
            ),
            (
                f"硬くなって歓迎してるの？かわいい。……じゃあ想像しなさい。"
                f"{name}の熱い口に包まれて、亀頭だけちゅっちゅされる感触。"
                f"唾液でぬるぬるになった先を、キスとフェラで交互にいじめられて……そのままイくまで離さないわよ。"
            ),
            (
                f"反応いいわね。勃ってるなら、もうフェラの準備完了ってこと。"
                f"{name}が先端にキスして、ふかふか咥えて、またキス。"
                f"そのたびに頭がとろけていくの、分かってるでしょ。……行かせに来てるわよ。"
            ),
            (
                f"硬いのに逃げないの？ふふ、好きよその顔。"
                f"いまから{name}の唇が亀頭に触れて、ちゅっ……次は奥まで咥えられる。"
                f"口の中で溶かされながら、情けない声出してイきなさい。"
            ),
            (
                f"ちんぽ、もう正直すぎるわ。{name}のフェラ想像しただけで硬くなってるんでしょ。"
                f"先端キスのたびにビクッてして、咥えられたらもう終わり。"
                f"いいのよ、口に負けて出ちゃうところまで付き合うから。"
            ),
        ]
    elif choice == "want":
        lines = [
            (
                f"口でしてほしいのね。……手じゃなくて、{name}に咥えてほしくて疼いてるの。"
                f"亀頭だけちゅってされて、次に熱い舌でなぞられて……欲しがってる顔、好きよ。"
                f"そのままイかせに来てあげるわ。我慢しなくていいの。"
            ),
            (
                f"触ってほしいより、咥えてほしいんでしょ。ふふ、ばれてるわ。"
                f"{name}の唇が先をふさいで、ちゅっ……ぬるっと奥まで入れて、ゆっくり動く。"
                f"先端キスつきのフェラで、頭真っ白になるまでイかせてあげる。"
            ),
            (
                f"欲しがるなら、ちゃんと想像しなさい。"
                f"{name}が膝をついて、あなたの弱い先にちゅっちゅしてから、"
                f"ねっとりフェラで吸い上げるところ。……腰が引けても離さないわ。出るまでよ。"
            ),
            (
                f"手がほしい？ちがうでしょ。{name}の口と亀頭キスがほしいのよ。"
                f"認めなさい。咥えられて、キスされて、とろけてイくのが本音なんでしょ。"
                f"ふふ……じゃあ、その弱さのままイかせに来るわ。"
            ),
            (
                f"「してほしい」って顔、かわいいわ。"
                f"{name}の唾液で先が光って、ちゅってされるたび腰が震える……その続きを、"
                f"ちゃんとフェラで最後までやってあげる。情けなく出していいのよ。"
            ),
        ]
    elif choice == "silent":
        lines = [
            (
                f"黙ってるのに、口とキスのこと考えてるでしょ。ふふ……目が正直ね。"
                f"言わなくてもいいわ。{name}が咥えて、先端にちゅってするたびに、"
                f"黙ったまま弱い声が漏れちゃうところまで連れてってあげる。"
            ),
            (
                f"言えないの？じゃあ体で答えなさい。"
                f"フェラと亀頭キスで、出せるところまでゆっくり攻めるわ。"
                f"沈黙のままイかされるの、いちばんかわいい負け方よ。……覚悟して。"
            ),
            (
                f"沈黙のまま咥えられるのね。先端にちゅってされるたびに肩が落ちて、"
                f"それでも口から逃げられない。……ふふ、好きよその弱さ。"
                f"{name}のフェラで、黙ったまま頭空っぽにしてあげる。"
            ),
            (
                f"答えなくていいわ。代わりに想像しなさい。"
                f"{name}の唇が亀頭に触れて、ちゅっ、ちゅっ……次に深く咥えられる感触。"
                f"言えないまま腰が砕けて、情けなく出ちゃうところまで、イかせに来てるわよ。"
            ),
            (
                f"言えない弱さもかわいい。……でも口は正直でしょ。"
                f"{name}にフェラされてる想像で、もう先が熱くなってるわ。"
                f"黙ったままキスと咥えで溶かして、イくまで離さないわよ。"
            ),
        ]
    elif choice == "kiss":
        lines = [
            (
                f"いいわ、決め技ね。……{name}が亀頭にキスしながらフェラするわ。"
                f"ちゅっ、咥える、ちゅっ、また咥える。弱い先をキスで崩して、口で奥まで仕上げる。"
                f"逃げられないわよ。ぬるぬるの唇と熱い口の中で、出るまでイかせてあげる。"
            ),
            (
                f"先端だけちゅっちゅしてから、ゆっくり深く咥える。"
                f"キスのたびに腰が引けても、{name}は笑って追いかけてくるわ。"
                f"フェラの途中でまた亀頭にキスして……ふふ、それでも最後はちゃんとイかせるの。離さない。"
            ),
            (
                f"唇で先を甘くふさいで、ちゅっ。舌でなぞって、またちゅっ。"
                f"次は奥まで咥えて、ゆっくり動かしながら弱いところを吸い上げる。"
                f"イきたくなったら我慢しなくていいわ。{name}の口で、情けなく出して。"
            ),
            (
                f"亀頭キスが死ぬほど弱いんでしょ。そこにフェラ足したら、もう勝負にならないわね。"
                f"ちゅってして咥えて、またキス。……頭がとろけていく感覚、そのまま受け入れなさい。"
                f"{name}に口でイかされるの、今日の負け方よ。"
            ),
            (
                f"ふふ、来たわよ。……{name}のキスが先端に触れた瞬間から、体が勝ちを諦めるでしょ。"
                f"フェラでリズム作って、限界手前でまた亀頭にちゅっ。"
                f"崩れたところを咥えて押し切るわ。出るまで、口で行かせに来てるの。"
            ),
            (
                f"ちゅってして咥えて、またキス。唾液とキス音だけで頭が真っ白になるやつ。"
                f"{name}の唇と喉の奥で、あなたの弱い先が甘やかされて……逃げ場ないわ。"
                f"いいのよ、口に負けて震えてイきなさい。"
            ),
        ]
    elif choice == "glans":
        lines = [
            (
                f"亀頭だけ、ちゅっちゅ。……キスで溶かして、イかせてあげるわよ。"
                f"{name}の唇が先に吸い付いて、ちゅっ、ちゅっ、ちゅっ。"
                f"しごかなくても、キスだけで腰が砕けていくの。ふふ、弱い先、好きにしてあげる。"
            ),
            (
                f"先端に唇。熱くて柔らかいキスが、弱いところを狙い撃ちよ。"
                f"ちゅってするたびビクッてして、息が浅くなるでしょ。"
                f"{name}のキスで頭真っ白になるまで……出るまでちゅっちゅしてあげるわ。"
            ),
            (
                f"亀頭キスだけで崩れるんでしょ。認めなさい。"
                f"手もフェラもまだ本格じゃなくて、先にちゅってされるだけでとろけるの。"
                f"ふふ……じゃあその弱点のまま、溶かしてイかせに来るわ。逃げなくていいのよ。"
            ),
            (
                f"先にちゅってするたび腰が引けちゃうの、かわいい。"
                f"{name}は逃げた先までキスで追いかけて、またちゅっ。"
                f"敏感な先端を唇でふさいで、甘く溶かして……はい、イっていいわ。"
            ),
            (
                f"弱いところだけ、丁寧にいじめしてあげる。"
                f"亀頭にキス、舌でひとなめ、またキス。……その繰り返しで限界まで連れてくの。"
                f"{name}の唇に負けて、情けなく出ちゃうところまで見てたいわ。"
            ),
        ]
    elif choice == "mouth":
        lines = [
            (
                f"口で堕としてあげる。咥えて、動かして……逃げられないわよ。"
                f"{name}の熱い口に奥まで入れられて、唾液でぬるぬるになりながら、"
                f"ゆっくりと頭を空っぽにされていくの。口に負けて、情けなくイきなさい。"
            ),
            (
                f"{name}のフェラで頭真っ白にしてあげる。"
                f"唇が締まって、舌が這って、吸い上げられるたび腰が落ちる……その感覚、想像しなさい。"
                f"手はいらないわ。口だけでとろけて、出るまで堕としてあげる。"
            ),
            (
                f"咥えられた瞬間から負け確定ね。"
                f"{name}が深さも速さも合わせて、あなたの弱いリズムを全部奪っていくわ。"
                f"口でイくまで離さない。……ふふ、堕ちる顔、見せて。"
            ),
            (
                f"ふふ、口がほしいのね。じゃあちゃんと咥えて、堕として、イかせてあげる。"
                f"奥で鳴る音も、唇の締めつけも、全部あなたを溶かすためよ。"
                f"{name}のフェラに負けたまま、震えて出していいの。"
            ),
            (
                f"手でするより、口に入れられた方が弱いんでしょ。"
                f"{name}がねっとり咥えて、引き抜いて、また咥える。"
                f"そのたびに膝が笑って……最後は口の中で情けなくイきなさい。"
            ),
        ]
    elif choice == "start":
        lines = [
            (
                f"触りはじめたのね。でも本命は口でしょ。"
                f"手が動いてるあいだに、{name}のフェラと亀頭キスに切り替わる想像しなさい。"
                f"先端にちゅってされて咥えられたら、その触れはじめ、すぐ終わっちゃうわよ。……イかせに来るわ。"
            ),
            (
                f"手で温めてるの？かわいい。……次は{name}の口とキスよ。"
                f"指の感触が、熱い唇と舌に変わっていくところまで想像して。"
                f"ちゅってして咥えて、とろけ始めなさい。イくまで付き合うわ。"
            ),
            (
                f"始めちゃったなら、途中から咥えられる覚悟もしておきなさい。"
                f"ゆっくり触ってるうちに{name}が先にキスして、ぬるっと咥えてくる。"
                f"先端キスで崩れるやつ……ふふ、そのつもりで続けて。"
            ),
            (
                f"触ってるあいだに、フェラされたいって顔になってるわよ。"
                f"手が動くたび、頭の中では{name}の口が前後してるでしょ。"
                f"いいわ、その欲のまま。口とキスで最後までイかせてあげる。"
            ),
            (
                f"手は練習。本番は口と亀頭キスよ。"
                f"いま温めてる先に、あとで{name}の唇がちゅってして、奥まで咥える。"
                f"そのつもりでとろけ始めなさい。……逃げ道、ないから。"
            ),
        ]
    elif choice == "stroke":
        lines = [
            (
                f"しごいてる途中でも、頭の中はフェラでしょ。"
                f"手の上下より、{name}に先端キスされて咥えられる想像の方が強いわ。"
                f"リズム乗ってるところに口が入ったら一気にイきそうね。……ふふ、仕上げてあげる。"
            ),
            (
                f"手より口がほしいのに、自分で動いてるの。かわいい。"
                f"でもいいわ。しごきながら{name}のフェラを想像して、腰を震わせていなさい。"
                f"その限界の手前で咥えて、亀頭にちゅってして……口でイかせるわよ。"
            ),
            (
                f"リズム出てるなら、そのまま口に入れていいわよ。"
                f"{name}が手の代わりに咥えて、先にちゅってして、吸いながら動く。"
                f"しごきで近づけた熱を、キスとフェラで押し切るの。出るまでね。"
            ),
            (
                f"しごきながらフェラ想像してるの、ばれてるわ。"
                f"キスのたびに腰が震えるんでしょ。咥えられたら声も出ちゃうやつ。"
                f"{name}の口でその想像を本物にしてあげる。……負けていいのよ。"
            ),
            (
                f"手で限界近くまで来たのね。あとは{name}のフェラと亀頭キスで仕上げよ。"
                f"指を離した瞬間に唇が来て、ちゅっ、ふかふか。……逃げられないわ。"
                f"せっかく近づけた熱、口でぜんぶ出させてあげる。"
            ),
        ]
    else:  # edge
        lines = [
            (
                f"イキそう？いいわ。……じゃあ行かせに来てあげる。"
                f"{name}がフェラして、亀頭にちゅってして、限界の先端を口で受け止める。"
                f"我慢しなくていいわ。震えたまま、情けなくイきなさい。"
            ),
            (
                f"限界手前ね。口で咥えて、先にキス。……そのふたつで終わりよ。"
                f"出ちゃいそうな熱を{name}の唇がふさいで、ちゅっ、奥まで。"
                f"ふふ、行かせに来たわよ。逃げる暇ないわ。"
            ),
            (
                f"出ちゃいそうなところを咥えて、ちゅっ。"
                f"ビクビクしてる先をキスで甘やかして、フェラで押し切る。"
                f"{name}の口の中で頭が真っ白になるまで……はい、出して。"
            ),
            (
                f"震えてる先端にキスして、深く咥える。"
                f"もう少しでイケる熱を、{name}が全部飲み込んで導いてくれるわ。"
                f"弱い声出していいの。口に負けて、そのままイかせてあげる。"
            ),
            (
                f"限界のサイン、出てるわよ。かわいい。"
                f"{name}のフェラと亀頭キスで仕上げるから、腰の力抜いて。"
                f"ちゅってされて咥えられて……情けない顔のまま、イっていいわ。"
            ),
        ]
    return random.choice(lines)


def mirror_after(choice, name, ab_days=None):
    """回答後：フェラ＋亀頭キスでイかせる追い打ち（長め）。"""
    if choice == "hard":
        extras = [
            (
                f"硬いなら口の準備、完了ね。"
                f"{name}が咥えて、先にちゅって、また咥える……そのたびに腰が落ちていくわ。"
                f"イくまで離さないから、勃ったままとろけて待ちなさい。"
            ),
            (
                f"反応だけでこんなに弱いの。フェラ始めたらすぐイきそう。……かわいい。"
                f"先端キスひとつで肩がすくむんでしょ。"
                f"{name}の口とキスで、頭真っ白になるまで行かせに来るわよ。"
            ),
            (
                f"勃ったまま待ってなさい。手で触らなくていいわ。"
                f"{name}が唇を寄せて、ちゅっ……熱い口で包むところまで、想像して疼いていなさい。"
                f"その硬さのまま、情けなくイかせてあげる。"
            ),
        ]
    elif choice == "want":
        extras = [
            (
                f"欲しがるなら、咥えられてイく覚悟しなさい。亀頭キスつきよ。"
                f"{name}の唇が先を甘くふさいで、ちゅってしてから奥まで入れる。"
                f"欲しがった罰……いや、ご褒美ね。口で最後まで甘やかすわ。"
            ),
            (
                f"口がほしいんでしょ。じゃあちゃんと想像しなさい。"
                f"ちゅってして、咥えて、吸い上げて、またキス。"
                f"{name}に出るまでやられて、頭がとろけるところまで付き合うわよ。"
            ),
            (
                f"欲しがった気持ち、受け取ったわ。"
                f"フェラと先端キスで、拒めないところまで連れてく。"
                f"ふふ……{name}の口に負けて、情けなくイく顔、見せて。"
            ),
        ]
    elif choice == "silent":
        extras = [
            (
                f"黙ってても口ではイけるわよ。フェラと亀頭キス、拒否できないでしょ。"
                f"言えないまま{name}に咥えられて、キスのたびに肩が落ちていく。"
                f"沈黙の敗北、いちばんかわいいわ。……そのまま出して。"
            ),
            (
                f"言えないまま出させられるの、覚悟して。"
                f"{name}は言葉なんて要らないわ。唇と舌と喉で、全部答えさせるから。"
                f"黙ったままイかされる感触、最後まで味わいなさい。"
            ),
            (
                f"沈黙のまま咥えられて……キスのたびに負けていくのね。ふふ。"
                f"声は出さなくていいわ。腰と先が正直なら、それで十分。"
                f"{name}の口で、静かに頭空っぽにしてあげる。"
            ),
        ]
    elif choice == "kiss":
        extras = [
            (
                f"亀頭キスしながら咥えるわ。ちゅっ、ふかふか、ちゅっ……出るまで止めない。"
                f"弱い先をキスで崩して、口で押し切る。"
                f"{name}に口でイかされるの、認めなさい。行かせに来てるわよ。"
            ),
            (
                f"先端にキスしてから深く。弱いところ狙い撃ちよ。"
                f"キスで甘くして、フェラで溶かして、またキスでトドメ。"
                f"ふふ……あなたの負け方、いちばん好きなやつ。イきなさい。"
            ),
            (
                f"ちゅってされてイくの、逃げないで。"
                f"{name}の唇とフェラが交互に来て、思考が追いつかなくなるまで続けるわ。"
                f"口で崩れて、情けなく出るところまで見てたいの。"
            ),
            (
                f"決め技どおりよ。キスで崩して、フェラで仕上げ。"
                f"先端の感度も、腰の力も、全部{name}の口に預けるの。"
                f"いいわ、その弱さのまま……行かせてあげる。"
            ),
        ]
    elif choice == "glans":
        extras = [
            (
                f"亀頭にちゅってするだけでもう終わりね。溶かして、イかせるわ。"
                f"{name}の唇が先に吸い付いて離さない。"
                f"しごきなしでも崩れる弱点、今日は徹底的に甘やかしてあげる。"
            ),
            (
                f"先端キスで崩れるの、認めなさい。……出るまでちゅっちゅよ。"
                f"ちゅっ、息、ちゅっ、腰が引ける。……かわいい。"
                f"{name}のキスだけで頭真っ白になるまで、付き合うわ。"
            ),
            (
                f"弱い先だけ狙ってあげる。キスで溶かして、行かせに来たわよ。"
                f"熱い唇が亀頭をふさいで、甘く、丁寧に、何度も。"
                f"逃げても追いかけてくるから……イっていいわ。"
            ),
        ]
    elif choice == "mouth":
        extras = [
            (
                f"口に堕ちたら最後よ。咥えられて、情けなくイきなさい。"
                f"{name}の喉の奥と唇の締めつけで、考えられなくなるまで動くわ。"
                f"手は離して。口だけで堕としてあげる。"
            ),
            (
                f"フェラで頭真っ白。……{name}の口に負けた記録、あとでつけなさい。"
                f"咥えられてイく瞬間の顔、隠さなくていいわ。"
                f"ふふ、堕ちるところまでちゃんと見ててあげる。"
            ),
            (
                f"咥えられてイくの、いちばんかわいいわ。覚悟して。"
                f"{name}がリズムも深さも全部決めるから、あなたはとろけるだけでいいの。"
                f"口に負けて、震えて、出して。"
            ),
        ]
    elif choice == "start":
        extras = [
            (
                f"触りはじめたなら、途中で口に切り替わる想像しなさい。"
                f"指の感触が{name}の唇と舌に変わって、キスつきでイくまでよ。"
                f"手は前戯。本番のフェラ、もうすぐ来るわ。"
            ),
            (
                f"手は前戯。本番はフェラと亀頭キス。……とろけて待ちなさい。"
                f"いま温めてる先に、あとでちゅってして咥えられる。"
                f"{name}に口で仕上げられる前提で、続けていいわよ。"
            ),
            (
                f"始めた以上、最後は口で出させるわ。覚悟、できてる？"
                f"触れはじめの甘い時間のあとに、{name}の本気のフェラが来るの。"
                f"ふふ……逃げ道、最初から塞いであるわよ。"
            ),
        ]
    elif choice == "stroke":
        extras = [
            (
                f"しごいてる手、止めてもいいわ。代わりに咥えて、先にちゅってしてあげる。"
                f"リズム乗ってる熱を、{name}の口がそのまま引き継ぐの。"
                f"キスでトドメして、出るまで離さないわよ。"
            ),
            (
                f"リズム乗ってるところにフェラ入ったら終わりね。キスでトドメよ。"
                f"手で近づけた限界を、口が一気に押し切る。"
                f"{name}にイかされる想像で、もっと腰とろけさせなさい。"
            ),
            (
                f"手で近づけた限界を、口で押し切るわ。出していいのよ、そのとき。"
                f"{name}が咥えて、亀頭にちゅって、吸いながら動く。"
                f"しごきの続きがフェラになる瞬間……ふふ、好きよ。"
            ),
        ]
    else:
        extras = [
            (
                f"限界なら、口で受け止めてあげる。亀頭キスして……はい、イっていいわ。"
                f"{name}が震えてる先端を唇でふさいで、そのまま咥えて導く。"
                f"我慢はいらないの。情けなく出して。"
            ),
            (
                f"イキそうなまま咥えられるの、さいきょうに弱いでしょう。行かせるわよ。"
                f"出ちゃいそうな熱を{name}の口が全部もらって、キスで甘やかす。"
                f"ふふ……崩れていいわ。口でイかせに来てるの。"
            ),
            (
                f"我慢しなくていい。{name}のフェラとキスで、情けなく出して。"
                f"限界のビクビクを唇が追いかけて、奥まで入れて押し切る。"
                f"弱い声、そのままでいいから。イきなさい。"
            ),
            (
                f"震えてるなら合図ね。ちゅってして咥えて……そのままイかせる。"
                f"{name}は逃さないわ。先端キスで崩して、フェラで仕上げるだけ。"
                f"今日の負け方、口で決めてあげる。"
            ),
        ]
    if ab_days and ab_days >= 2:
        extras.append(
            (
                f"{ab_days}日分、口と亀頭キスで全部出させてあげる。"
                f"溜めた熱を{name}の唇が先にちゅってして、奥まで咥えて受け止めるわ。"
                f"溜めたまま負けなさい。……ふふ、行かせてあげる。"
            )
        )
        if choice in ("kiss", "glans", "mouth", "edge"):
            extras.append(
                (
                    f"{ab_days}日溜めた先端にキスして咥えるの……即イきね。"
                    f"敏感な先を{name}がちゅっちゅして、熱い口で押し切る。"
                    f"我慢できた日数ぶん、情けなくイかせてあげるわよ。"
                )
            )
    return random.choice(extras)


def tease_mirror_reply(choice, name):
    mapped = {"touch": "want"}.get(choice, choice)
    return mirror_reply(mapped, name)


# ===== 鏡チェック拡張：手順 / ゲージ / 弱点 / 履歴 / 許可 =====
MIRROR_WEAK_OPTIONS = [
    "亀頭キス弱い",
    "奥フェラが好き",
    "浅い咥えで溶ける",
    "ちゅっ音に弱い",
    "先端なめが効く",
    "ゆっくりされると落ちる",
]

MIRROR_STEPS = [
    ("キスだけ", "kiss_only"),
    ("先を舐める", "lick"),
    ("浅く咥える", "shallow"),
    ("深く咥える", "deep"),
    ("イかせる", "finish"),
]

MIRROR_GAUGE = [
    ("touch", "触ってる…", 34),
    ("near", "限界近い…", 68),
    ("cum", "もう出る…", 100),
]

MIRROR_VOICES = [
    ("sweet", "甘い"),
    ("sticky", "ねっとり"),
    ("urgent", "急かす"),
    ("tease", "からかう"),
    ("dote", "溺愛"),
    ("command", "命令"),
]

MIRROR_WEAK_COMBOS = {
    frozenset({"亀頭キス弱い", "浅い咥えで溶ける"}): (
        "……亀頭キスから浅く咥えて溶かすコンボよ。{name}、その順番がいちばん効くの、分かってるわね。"
    ),
    frozenset({"亀頭キス弱い", "奥フェラが好き"}): (
        "……先にちゅってしてから奥まで。{name}のフェラ、いちばん堕ちやすい順番でいくわ。"
    ),
    frozenset({"ちゅっ音に弱い", "亀頭キス弱い"}): (
        "……ちゅっ、ちゅっ、ってキス音だけで腰が砕けるんでしょ。{name}、音つきで先端をいじめてあげる。"
    ),
    frozenset({"先端なめが効く", "浅い咥えで溶ける"}): (
        "……先を舐めてから浅く咥える。ねっとり→ぬるっ、のコンボで頭空っぽにするわよ。"
    ),
    frozenset({"ゆっくりされると落ちる", "奥フェラが好き"}): (
        "……ゆっくり深く咥えられるの、ダブルで効くわね。{name}、急がず奥まで堕としてあげる。"
    ),
    frozenset({"ちゅっ音に弱い", "浅い咥えで溶ける"}): (
        "……浅く咥えながらちゅっちゅ。音と浅さのコンボ、{name}得意の負け方でしょ。"
    ),
}


def mirror_loss_streak_days(name, history):
    """同一オナペへの連続敗北日数（直近から遡る）。"""
    loss_days = sorted(
        {h["time"][:10] for h in history if h.get("name") == name},
        reverse=True,
    )
    if not loss_days:
        return 0
    streak = 1
    prev = datetime.strptime(loss_days[0], "%Y-%m-%d").date()
    for day_str in loss_days[1:]:
        d = datetime.strptime(day_str, "%Y-%m-%d").date()
        if prev - d == timedelta(days=1):
            streak += 1
            prev = d
        else:
            break
    return streak


def mirror_calendar_whisper(name, history, ref_date=None):
    """カレンダー連動：同じ日付の過去敗北を囁く。"""
    ref = ref_date or today_jst
    ref_str = ref.strftime("%Y-%m-%d")
    same_day = [h for h in history if h.get("name") == name and h.get("time", "")[:10] == ref_str]
    if len(same_day) >= 2:
        return (
            f"今日、もう{name}の口で{len(same_day)}回負けてるわね。"
            f"同じ日に何度も堕ちるの、いちばん情けないパターンよ。"
        )
    if len(same_day) == 1:
        return f"今日もう一度{name}の口に来たの？……同じ日の二回目、覚悟して。"
    md = ref_str[5:]  # MM-DD
    anniv = [h for h in history if h.get("name") == name and h.get("time", "")[5:10] == md]
    if anniv:
        y = anniv[-1]["time"][:4]
        return (
            f"{ref.month}月{ref.day}日……{y}年もこの日、{name}の口で負けたわね。"
            f"記念日みたいに、また咥えられに来たの？"
        )
    return ""


def mirror_self_note_flavor(name, note):
    if not note or not str(note).strip():
        return ""
    note = str(note).strip()[:120]
    return f"……あなたの申告「{note}」、{name}が全部口で叶えてあげるわよ。"


def mirror_weak_combo_flavor(name, tags, loss_count=0):
    if len(tags or []) < 2:
        return ""
    tagset = frozenset(tags)
    for combo, tmpl in MIRROR_WEAK_COMBOS.items():
        if combo.issubset(tagset):
            line = tmpl.format(name=name)
            if loss_count >= 5:
                line += f"……{loss_count}回負けてるから、このコンボはもう体に刻まれてるわね。"
            return line
    pair = random.sample(list(tags), 2)
    return (
        f"……{pair[0]}と{pair[1]}、セットで効くの分かってるでしょ。"
        f"{name}が交互に攻めて、頭真っ白にしてあげる。"
    )


def mirror_voice_prefix(voice, name):
    return {
        "sweet": f"（甘い声で）……ねえ、{name}が優しくしてあげる。",
        "sticky": f"（ねっとりと）……ふふ、離さないわよ、{name}。",
        "urgent": f"（急かすように）ほら、早くとろけなさい。{name}、待たないわ。",
        "tease": f"（からかうように）ふふ……{name}、また情けない顔しに来たの？",
        "dote": f"（溺愛混じりに）……いい子ね、{name}がたっぷり可愛がってあげる。",
        "command": f"（命令口調で）{name}の口に従いなさい。抵抗は無駄よ。",
    }.get(voice or "sweet", "")


def mirror_loss_count(name, history):
    return sum(1 for h in history if h.get("name") == name)


def mirror_weak_level(loss_count):
    if loss_count >= 10:
        return 2
    if loss_count >= 3:
        return 1
    return 0


def mirror_with_voice(text, voice, name):
    if not text:
        return text
    pre = mirror_voice_prefix(voice, name)
    return f"{pre}{text}" if pre else text


def mirror_history_whisper(name, history):
    """前回の負けを囁く。"""
    hits = [h for h in history if h.get("name") == name]
    if not hits:
        return (
            f"まだ{name}の口では記録してないのね。"
            f"……今夜が最初の情けない敗北になるかもよ、ふふ。"
        )
    last = hits[-1].get("time", "")[:10]
    n = len(hits)
    days = None
    try:
        days = (today_jst - datetime.strptime(last, "%Y-%m-%d").date()).days
    except Exception:
        pass
    growth = ""
    lv = mirror_weak_level(n)
    if lv == 1:
        growth = f"……{n}回も負けてるから、もう体が{name}の口を覚えてるわよ。"
    elif lv == 2:
        growth = f"……{n}回敗北ね。弱点、完全に育ってる。また同じ口で落ちる気満々でしょ。"
    if days == 0:
        base = (
            f"今日ももう{name}に負けてるわね。……回数は累計{n}回。"
            f"また口と亀頭キスで、情けなく重ねてきなさい。"
        )
    elif days == 1:
        base = (
            f"昨日も{name}にイかされたでしょ。累計{n}回目の口負け……。"
            f"また咥えられて、ちゅってされて、崩れる番よ。"
        )
    elif days is not None and days >= 2:
        base = (
            f"{days}日ぶりに{name}の口を思い出してるのね。累計{n}回も負けてる相手よ。"
            f"溜めた先にキスして咥えられたら……すぐイきそうでかわいいわ。"
        )
    else:
        base = (
            f"{name}にはもう{n}回負けてるわ。"
            f"またフェラと亀頭キスで、同じ負け方してしまいなさい。"
        )
    return f"{base}{growth}"


def mirror_weak_flavor(name, tags, loss_count=0, self_note=""):
    """弱点メモをセリフに混ぜる一文。負け回数で育つ。2タグ以上はコンボ優先。"""
    note = mirror_self_note_flavor(name, self_note)
    if tags and len(tags) >= 2:
        combo = mirror_weak_combo_flavor(name, tags, loss_count)
        if combo:
            return f"{combo}{note}" if note else combo
    if not tags:
        if loss_count >= 3:
            base = (
                f"……メモなくても分かるわ。{name}に{loss_count}回も負けてる時点で、"
                f"口と亀頭キスが弱点でしょ。"
            )
            return f"{base}{note}" if note else base
        return note
    tag = random.choice(tags)
    lv = mirror_weak_level(loss_count)
    soft = {
        "亀頭キス弱い": f"……そういえば{name}、あなたの亀頭キス弱さ、もう把握してるわ。そこ狙いよ。",
        "奥フェラが好き": f"……{name}の奥、好きなんでしょ。深く咥えられた想像、もうしてるわね。",
        "浅い咥えで溶ける": f"……浅く咥えられるだけで溶けるタイプ、{name}が一番分かってるわよ。",
        "ちゅっ音に弱い": f"……ちゅっ、って音だけでもう腰が引けるんでしょ。{name}、知ってるわ。",
        "先端なめが効く": f"……先端をねっとり舐められるの、{name}相手だと特に弱いものね。",
        "ゆっくりされると落ちる": f"……ゆっくりされるほど落ちるんでしょ。{name}、丁寧にイかせてあげる。",
    }
    mid = {
        "亀頭キス弱い": f"……{loss_count}回分の記憶ね。{name}の亀頭キスで落ちた回数、体が覚えてるわ。またそこよ。",
        "奥フェラが好き": f"……また奥が欲しくなったの？{name}に深く咥えられて負けたの、もう{loss_count}回よ。",
        "浅い咥えで溶ける": f"……浅いだけで溶ける弱点、{loss_count}回の敗北で育ってるわね。{name}、知ってて浅くするわよ。",
        "ちゅっ音に弱い": f"……ちゅっ、の音で落ちるの、何回目？累計{loss_count}回の口負け、音にも弱いんでしょ。",
        "先端なめが効く": f"……先端なめに弱いの、{name}相手だと特に。{loss_count}回分、舌で思い出しなさい。",
        "ゆっくりされると落ちる": f"……ゆっくりで落ちる体質、{loss_count}回かけて証明済みね。{name}、丁寧に崩すわ。",
    }
    hard = {
        "亀頭キス弱い": (
            f"……{loss_count}回も{name}の亀頭キスで負けてる時点で、そこは完成した弱点よ。"
            f"ちゅってされたら即とろけるの、もう逃げられないわ。"
        ),
        "奥フェラが好き": (
            f"……{loss_count}回の奥負けね。{name}に深く咥えられるたびに、同じ顔で堕ちてるわ。"
            f"また奥で頭真っ白にしてあげる。"
        ),
        "浅い咥えで溶ける": (
            f"……浅く咥えられただけで{loss_count}回分とろけてきた子ね。"
            f"{name}はそれを知ってて、浅さでいじめられるわよ。"
        ),
        "ちゅっ音に弱い": (
            f"……ちゅっ、って聞いただけで腰が覚えるでしょ。{loss_count}回の口敗北側。"
            f"{name}のキス音、もう条件反射よ。"
        ),
        "先端なめが効く": (
            f"……先端を舐められる弱点、{loss_count}回で固定されたわね。"
            f"{name}の舌が入った瞬間から、負け確定よ。"
        ),
        "ゆっくりされると落ちる": (
            f"……ゆっくりされるほど落ちる。{loss_count}回の実験結果、完璧よ。"
            f"{name}が急がないほど、あなたは情けなくイくの。"
        ),
    }
    table = soft if lv == 0 else mid if lv == 1 else hard
    base = table.get(tag, f"……{name}の「{tag}」、{loss_count}回分の弱さごと攻めるわよ。")
    return f"{base}{note}" if note else base


def mirror_permit_lines(name, stage="deny"):
    """許可段階：deny / mouth / grant"""
    if stage == "grant":
        return random.choice([
            (
                f"……いいわ。出して。"
                f"{name}が咥えたまま、亀頭にちゅってして、そのまま受け止めるわ。"
                f"情けない声出してイきなさい。口に負けた記録、あとでつけなさい。"
            ),
            (
                f"射精の許可、出すわ。逃げなくていいの。"
                f"{name}のフェラと先端キスで、頭真っ白になるまでイかせてあげる。"
            ),
        ])
    if stage == "mouth":
        return random.choice([
            (
                f"口だけ、許可するわ。咥えて、キスして……でもまだ出さない。"
                f"{name}が浅く前後して、先端にちゅっちゅ。射精は、そのあとね。"
            ),
            (
                f"いいわ、口は使っていいの。フェラと亀頭キスでとろけなさい。"
                f"ただし出すのはまだ。口の中で我慢のふち、味わって。"
            ),
        ])
    return random.choice([
        (
            f"まだだめ。……イキそうなのに出させないわ。"
            f"{name}は先端にちゅってして、浅く咥えて、また離す。"
            f"限界のふちで溶かされてるの、気持ちいいでしょ。"
        ),
        (
            f"ふふ、却下。出したい顔なのにかわいいわ。"
            f"{name}の口で焦らして、キスで崩して……射精はまだよ。"
        ),
    ])


def mirror_edge_loop_lines(name, loop_n, tags=None, loss_count=0, self_note=""):
    """イく直前ループ。許可なしでふちを積み上げる。"""
    n = max(1, min(int(loop_n or 1), 5))
    weak = mirror_weak_flavor(name, tags or [], loss_count, self_note)
    pool = {
        1: (
            f"ふち、1回目。……{name}が先にちゅってして、浅く咥えて、また離す。"
            f"イキそうなのに出させないわ。腰、震えてるでしょ。かわいい。"
        ),
        2: (
            f"2回目のふちよ。さっきより敏感になってる。"
            f"{name}は亀頭キスを長めにして、咥えて、寸前で止める。"
            f"許可、まだないわ。とろけたまま耐えなさい。"
        ),
        3: (
            f"3回目……頭、だいぶ白いでしょう。"
            f"{name}の口がリズムを作っては崩して、キスでトドメ寸前まで来る。"
            f"でも出さない。ふちのまま、もう一度溶かしてあげる。"
        ),
        4: (
            f"4回目の粘着よ。もう限界の顔ね。"
            f"{name}が深く咥えて、引き抜いて、先端だけちゅっちゅ。"
            f"出したい？まだまだ。許可が出るまで、イキそうのままいなさい。"
        ),
        5: (
            f"5回目……ふちの最大ね。ここまで来たら体が正直よ。"
            f"{name}のフェラと亀頭キスで、射精の一歩手前だけを何度も撫でるわ。"
            f"ふふ、もう許可求めていいわよ。でも、まだだめって言うかも。"
        ),
    }
    line = pool[n]
    if weak:
        line = f"{line}{weak}"
    after = (
        f"ふち×{n}。……イキたい気持ち、ちゃんと貯めて。"
        f"許可はまだよ。{name}の口、離さないわ。"
        if n < 5
        else f"ふち×5、限界超え寸前ね。今度こそ「出していい？」って聞きなさい。"
    )
    return line, after


def mirror_afterglow_lines(name, tags=None, loss_count=0):
    """射精後の余韻。口を離さない追い打ち。"""
    weak = mirror_weak_flavor(name, tags or [], loss_count)
    lines = [
        (
            f"出したあとも、{name}は口を離さないわ。……ちゅっ。"
            f"余韻の先端にキスして、まだ軽く咥えてるの。感度、最悪でしょ。"
            f"ふふ、敗北のあとも甘やかしてあげる。"
        ),
        (
            f"射精したのに逃げないで。……{name}が白くなった先を、そっと舐めてるわ。"
            f"記録したあとのちんぽ、いちばん弱い時間よ。キス、もう一回。"
        ),
        (
            f"とろけたあともフェラの口、残ってるわよ。"
            f"{name}は離さない。浅く含んで、ちゅってして、余韻を伸ばすの。"
            f"情けない敗北の続き、味わいなさい。"
        ),
        (
            f"出したね。……えらい。でも終わりじゃないわ。"
            f"{name}の唇がまだ先端にいる。余韻キスで、頭をもう一度真っ白にできるわよ。"
        ),
    ]
    line = random.choice(lines)
    if weak:
        line = f"{line}{weak}"
    return line


def mirror_step_lines(step_key, name, tags=None, loss_count=0, self_note=""):
    """口プレイ手順ごとのセリフ。"""
    weak = mirror_weak_flavor(name, tags or [], loss_count, self_note)
    pool = {
        "kiss_only": [
            (
                f"まずはキスだけ。……{name}の唇が亀頭に、ちゅっ。"
                f"咥えない。動かす手もない。キスの感触だけで先が熱くなるの。"
                f"ふふ、まだ本編じゃないわよ。でももう腰、引けてるでしょ。"
            ),
            (
                f"ちゅっ……離す。ちゅっ……また触れる。"
                f"{name}は先端だけを甘くふさいで、フェラには進まない。"
                f"焦らされてるのに気持ちいいの、認める？ ……次で舐めてあげる。"
            ),
        ],
        "lick": [
            (
                f"次は舌よ。……{name}が亀頭をねっとり舐めるわ。"
                f"キスのあとのぬるぬるした先を、上下にゆっくり。"
                f"咥えてほしくて疼くでしょ。まだ浅いフェラにも入れないわ。とろけなさい。"
            ),
            (
                f"先端を舌で一周……ふふ、ビクッてしたわね。"
                f"{name}は弱いところだけ丁寧に舐めて、唇でちゅって追撃。"
                f"しごかれてるより効くでしょ。次、浅く咥えてあげる。"
            ),
        ],
        "shallow": [
            (
                f"浅く咥えるわ。……{name}の唇が先だけを包んで、ちゅっ、と吸い上げる。"
                f"奥まではまだ。浅いフェラと先端キスで、頭を溶かす段階よ。"
                f"腰が追従してくるの、かわいいわ。深くは、もうちょっとあとにして。"
            ),
            (
                f"ぬるっと、先だけ口に入る。……浅いのに、もう負け顔ね。"
                f"{name}が浅く前後して、たまに亀頭にちゅってする。"
                f"深く欲しがるなら、次で奥までよ。いまは浅さに堕ちていなさい。"
            ),
        ],
        "deep": [
            (
                f"深く咥えるわよ。……{name}の口が奥まで受け入れて、喉の方まで熱い。"
                f"引き抜いてはまた深く。途中で亀頭にキスして、また奥。"
                f"逃げられないわ。口の中で形を覚えられながら、イキそうまで連れてくの。"
            ),
            (
                f"ふかふか……奥まで。{name}のフェラ、本気出してきたわね。"
                f"深いリズムのあいだに先端キスを挟んで、感度を上げていく。"
                f"もう少しで仕上げよ。限界の顔、隠さなくていいわ。"
            ),
        ],
        "finish": [
            (
                f"仕上げよ。……{name}がフェラと亀頭キスで、出るところまで来るわ。"
                f"深く咥えて、先にちゅってして、また吸う。逃げ場ないわよ。"
                f"イキそうなら言いなさい。許可、出してあげるから。"
            ),
            (
                f"イかせに来たわ。口で包んで、キスで崩して、奥で押し切る。"
                f"{name}の唇も舌も、あなたの弱い先を最後まで甘やかすわ。"
                f"ふふ……出していいタイミング、聞いてあげる。我慢のふちで待ってて。"
            ),
        ],
    }
    line = random.choice(pool.get(step_key, pool["kiss_only"]))
    if weak:
        line = f"{line}{weak}"
    return line


def mirror_step_after(step_key, name):
    extras = {
        "kiss_only": f"キスだけなのに先が正直ね。……{name}、次は舌よ。覚悟して。",
        "lick": f"舐められてるのに咥えられないの、いちばん弱い時間よ。次、浅く入れるわ。",
        "shallow": f"浅いのに溶けてる。……奥が欲しければ、次で深くしてあげる。",
        "deep": f"深いフェラで頭真っ白。……仕上げの前に、限界を教えなさい。",
        "finish": f"口でここまで来たのね。イキたいなら「出していい？」って聞きなさい。ふふ。",
    }
    return extras.get(step_key, f"{name}の口、続きがあるわよ。")


def mirror_gauge_lines(gauge_key, name, tags=None, loss_count=0, self_note=""):
    weak = mirror_weak_flavor(name, tags or [], loss_count, self_note)
    pool = {
        "touch": [
            (
                f"触ってる段階ね。……でも本命は{name}の口でしょ。"
                f"手で温めながら、亀頭キスとフェラの想像で感度を上げていなさい。"
                f"まだ出さなくていいわ。とろける準備よ。"
            ),
        ],
        "near": [
            (
                f"限界近いのね。いいわ、そのふち。"
                f"{name}が浅く咥えて、先にちゅってして、また離す……その繰り返しで崩せるわ。"
                f"イキそうでも、まだ許可は出さないかもよ。ふふ、弱い顔見せて。"
            ),
        ],
        "cum": [
            (
                f"もう出る……？ふふ、正直ね。"
                f"じゃあ{name}の口で受け止める準備をするわ。フェラして、亀頭にキスして、"
                f"出ちゃいそうな熱を唇でふさいであげる。でも出すのは、許可が先よ。"
            ),
        ],
    }
    line = random.choice(pool.get(gauge_key, pool["touch"]))
    if weak and gauge_key != "touch":
        line = f"{line}{weak}"
    return line


def mirror_enrich(
    choice, name, ab_days=None, tags=None, gauge=None,
    loss_count=0, voice="sweet", self_note="",
):
    """既存セリフに弱点・ゲージ・声色・自己申告を足して返す。"""
    main = mirror_reply(choice, name)
    after = mirror_after(choice, name, ab_days)
    weak = mirror_weak_flavor(name, tags or [], loss_count, self_note)
    if weak:
        main = f"{main}{weak}"
    if gauge == "cum" and choice not in ("kiss", "glans", "mouth", "edge"):
        after = (
            f"{after}"
            f"……もう出そうなら、許可を段階で求めなさい。口だけ→出していい、の順番よ。"
        )
    elif gauge == "near":
        after = f"{after}限界のふちね。口とキスで、もう一段とろけさせられるわよ。"
    main = mirror_with_voice(main, voice, name)
    return main, after

# ===== データ集計 =====
today_count = sum(1 for h in data["history"] if h["time"].startswith(today_str))
total_all = sum(sum(v.get("counts", {}).values()) for v in data["items"].values())
recent_name = next((h["name"] for h in reversed(data["history"])), None)

# 禁欲連続日数（最後のカウントから今日まで）
def abstinence_days(history):
    last = next((h["time"][:10] for h in reversed(history)), None)
    if not last:
        return None
    return (today_jst - datetime.strptime(last, "%Y-%m-%d").date()).days

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

# 欲求蓄積度ゲージ
d_pct, d_color, d_msg = desire_gauge(ab_days)
st.sidebar.markdown(
    f"<div style='padding:0.5em;background:rgba(80,0,40,0.2);"
    f"border:1px solid rgba(194,24,91,0.35);border-radius:8px;margin-bottom:0.8em;'>"
    f"<div style='display:flex;justify-content:space-between;margin-bottom:0.3em;'>"
    f"<span style='color:#ff80ab;font-size:0.75em;'>🌡 欲求蓄積度</span>"
    f"<span style='color:{d_color};font-size:0.8em;font-weight:900;'>{d_pct}%</span>"
    f"</div>"
    f"<div style='background:rgba(30,0,20,0.6);border-radius:4px;height:8px;'>"
    f"<div style='width:{d_pct}%;height:100%;border-radius:4px;"
    f"background:linear-gradient(90deg,{d_color}88,{d_color});transition:width 0.5s;'></div>"
    f"</div>"
    f"<div style='color:#ffb6d9;font-style:italic;font-size:0.75em;margin-top:0.3em;'>{d_msg}</div>"
    f"</div>",
    unsafe_allow_html=True,
)

# === TRIAL TEASE: サイドバートグル（OFFで元に戻る）===
trial_tease = st.sidebar.toggle(
    "🧪 試し：開くだけで勃つモード",
    value=st.session_state.get("trial_tease", False),
    help="壁ドン・鏡チェック・観賞・予言など。OFFで消えます",
)
st.session_state.trial_tease = trial_tease
is_night = hour >= 22 or hour < 5
clean_day = today_count == 0
if trial_tease:
    st.sidebar.caption("ON中：カウントしなくても刺激が出ます")
    if is_night:
        st.sidebar.markdown(
            "<div style='color:#ff4081;font-size:0.78em;font-style:italic;"
            "margin-bottom:0.5em;'>🌙 夜モード発動中……容赦しないわよ</div>",
            unsafe_allow_html=True,
        )
    extra = tease_desire_extra(ab_days, d_pct)
    st.sidebar.markdown(
        f"<div style='padding:0.45em;background:rgba(194,24,91,0.12);"
        f"border:1px solid rgba(255,64,129,0.35);border-radius:8px;margin-bottom:0.8em;'>"
        f"<div style='color:#ff80ab;font-size:0.72em;'>💋 見るだけ煽り</div>"
        f"<div style='color:#ffb6d9;font-style:italic;font-size:0.78em;'>{extra}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
else:
    st.session_state.tease_wall_dismissed = False
    st.session_state.pop("tease_mirror_reply", None)

months = all_months(data)
current_month = now_jst.strftime("%Y-%m")
if current_month not in months:
    months = [current_month] + months
month_options = ["全月"] + months
selected_month = st.sidebar.selectbox("📅 月フィルター", month_options, index=1)
month_filter = None if selected_month == "全月" else selected_month

sort_key = st.sidebar.selectbox(
    "🔀 並び替え",
    ["累計多い順", "今月多い順", "最近負けた順", "禁欲が長い順"],
)

_raw_date = st.sidebar.date_input(
    "🗓 カウント日付", value=today_jst, max_value=today_jst,
    help="前日分を記録するときに変更"
)
count_date = _raw_date if isinstance(_raw_date, date) else today_jst

# ===== お言葉（敗北射精直後：強雌様に屈した感）=====
if st.session_state.get("master_word"):
    flash_name = st.session_state.get("defeat_flash_name", "")
    flash_img = ""
    if flash_name:
        flash_item = next((v for v in data["items"].values() if v["name"] == flash_name), {})
        flash_img = img_to_html(
            flash_item.get("img", ""),
            style="width:100%;max-height:260px;object-fit:cover;border-radius:12px;margin:0.5em 0;",
        )
    st.markdown(f"""
<div class="tease-wall" style="border-color:#ff4081;">
  <div class="tease-badge">💞 情けない敗北射精</div>
  {flash_img}
  <div style="color:#ff80ab;font-size:0.85em;margin-top:0.2em;">💋 またとろけて負けちゃった</div>
  <div class="tease-line" style="font-size:1.08em;">「{st.session_state.master_word}」</div>
  <div style="color:#804060;font-size:0.78em;margin-top:0.4em;">いいのよ、情けなくて。記録できたわね。……余韻、まだ続くわよ</div>
</div>
""", unsafe_allow_html=True)
    st.session_state.master_word = None
    st.session_state.defeat_flash_name = None

# ===== 射精後余韻 =====
if st.session_state.get("mirror_afterglow"):
    ag_name = st.session_state.get("mirror_afterglow_name") or ""
    ag_line = st.session_state.get("mirror_afterglow_line") or ""
    ag_n = int(st.session_state.get("mirror_afterglow_count", 1) or 1)
    st.markdown(f"""
<div class="tease-wall" style="border-color:#ff80ab;max-width:520px;margin:0 auto 0.8em;">
  <div class="tease-badge">💋 射精後の余韻 ×{ag_n}</div>
  <div class="mirror-chu" style="margin-top:0.4em;">ちゅっ……まだ離さない</div>
  <div class="tease-line mirror-line-main" style="margin-top:0.4em;line-height:1.55;text-align:left;">
    「{ag_line}」
  </div>
</div>
""", unsafe_allow_html=True)
    ag1, ag2, ag3 = st.columns(3)
    with ag1:
        if st.button("余韻をもう一度…口離さない", key="mirror_afterglow_more", use_container_width=True):
            ag_item = next((v for v in data["items"].values() if v.get("name") == ag_name), {})
            ag_tags = list(ag_item.get("weak_tags") or [])
            ag_loss = mirror_loss_count(ag_name, data.get("history", []))
            voice = st.session_state.get("mirror_voice", "sweet")
            st.session_state.mirror_afterglow_count = ag_n + 1
            st.session_state.mirror_afterglow_line = mirror_with_voice(
                mirror_afterglow_lines(ag_name, ag_tags, ag_loss), voice, ag_name
            )
            st.rerun()
    with ag2:
        if st.button("もう一回口でイかせに来て", key="mirror_afterglow_restart", use_container_width=True):
            st.session_state.mirror_afterglow = False
            st.session_state.mirror_afterglow_line = None
            st.session_state.mirror_afterglow_name = None
            st.session_state.mirror_afterglow_count = 0
            st.session_state.mirror_name = ag_name
            st.session_state.mirror_onape_sel = ag_name
            st.session_state.pop("mirror_open_base", None)
            st.session_state.pop("mirror_hist_whisper", None)
            _mirror_reset_play()
            st.rerun()
    with ag3:
        if st.button("今日はここまで", key="mirror_afterglow_close", use_container_width=True):
            st.session_state.mirror_afterglow = False
            st.session_state.mirror_afterglow_line = None
            st.session_state.mirror_afterglow_name = None
            st.session_state.mirror_afterglow_count = 0
            st.rerun()

# 節目メッセージ
if milestone_msg:
    icon, text = milestone_msg
    st.markdown(f"<div class='milestone-msg'>{icon} {text}</div>", unsafe_allow_html=True)

# ===== 鏡チェック（本番常設）=====
def _mirror_pick_item(pool, prefer_name=None, rec_boost=None):
    if not prefer_name and rec_boost and random.random() < 0.78:
        prefer_name = rec_boost
    if prefer_name:
        hit = next((v for v in pool if v.get("name") == prefer_name and v.get("img")), None)
        if hit:
            return hit
        hit = next((v for v in pool if v.get("name") == prefer_name), None)
        if hit:
            return hit
    with_img = [v for v in pool if v.get("img")]
    return random.choice(with_img or pool)


_MIRROR_FINISHERS = [
    ("kiss", "フェラ＋亀頭キスでイかせて"),
    ("glans", "亀頭キスで溶かして"),
    ("mouth", "口で堕として"),
]
_MIRROR_FINISHER_LABELS = [label for _, label in _MIRROR_FINISHERS]
_MIRROR_FINISHER_KEY = {label: key for key, label in _MIRROR_FINISHERS}
_MIRROR_FINISH_KEYS = {"kiss", "glans", "mouth", "edge", "finish"}


def _mirror_set_gauge(key):
    """論理ゲージを更新。radio キーは描画前に同期する（描画後の書込は Streamlit が拒否する）。"""
    st.session_state.mirror_gauge = key
    st.session_state._mirror_gauge_sync = True


def _mirror_reset_play():
    st.session_state.mirror_reply_text = None
    st.session_state.mirror_after_text = None
    st.session_state.mirror_choice = None
    st.session_state.mirror_step = 0
    _mirror_set_gauge("touch")
    st.session_state.mirror_permit = None
    st.session_state.mirror_permit_line = None
    st.session_state.mirror_edge_loop = 0
    st.session_state.pop("mirror_open_line", None)
    st.session_state.pop("mirror_open_base", None)
    st.session_state.pop("mirror_hist_whisper", None)


def _mirror_start_afterglow(name):
    item = next((v for v in data["items"].values() if v.get("name") == name), {})
    tags = list(item.get("weak_tags") or [])
    loss_n = mirror_loss_count(name, data.get("history", []))
    voice = st.session_state.get("mirror_voice", "sweet")
    st.session_state.mirror_afterglow = True
    st.session_state.mirror_afterglow_name = name
    st.session_state.mirror_afterglow_count = 1
    st.session_state.mirror_afterglow_line = mirror_with_voice(
        mirror_afterglow_lines(name, tags, loss_n), voice, name
    )


def _mirror_switch_to(name, pool, sync_select=True):
    hit = next((v for v in pool if v.get("name") == name), None)
    if not hit:
        return False
    st.session_state.mirror_name = hit.get("name", "")
    st.session_state.mirror_img = hit.get("img", "")
    _mirror_reset_play()
    if sync_select:
        st.session_state.mirror_onape_sel = hit.get("name", "")
    return True


def _mirror_record_defeat(name):
    """鏡チェックの許可後に敗北射精を記録。"""
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
        data["items"][item_key] = {
            "name": name, "tab": "all", "counts": {}, "img": "", "points": 0, "weak_tags": [],
        }
        m = count_date.strftime("%Y-%m")
        data["items"][item_key]["counts"][m] = 1
        tab = "all"
    time_str = datetime.combine(count_date, now_jst.time()).strftime("%Y-%m-%d %H:%M:%S")
    data["history"].append({"name": name, "tab": tab, "time": time_str})
    save_data(data)
    new_total = sum(sum(v.get("counts", {}).values()) for v in data["items"].values())
    special = next((f"{ic} {tx}" for mc, (ic, tx) in MILESTONES.items() if new_total == mc), None)
    st.session_state.master_word = special if special else master_word(name)
    st.session_state.defeat_flash_name = name
    _mirror_reset_play()
    _mirror_start_afterglow(name)


_mirror_pool = [v for v in data["items"].values() if v.get("name")]
_mirror_with_img = [v for v in _mirror_pool if v.get("img")]
_mirror_names = [v.get("name") for v in (_mirror_with_img or _mirror_pool)]
if _mirror_with_img or _mirror_pool:
    _pool_for_pick = _mirror_with_img or _mirror_pool
    if "mirror_name" not in st.session_state or st.session_state.mirror_name not in _mirror_names:
        picked = _mirror_pick_item(_pool_for_pick, recent_name or rec_name, rec_boost=rec_name)
        st.session_state.mirror_name = picked.get("name", "")
        st.session_state.mirror_img = picked.get("img", "")
        st.session_state.mirror_onape_sel = st.session_state.mirror_name
        _mirror_reset_play()

    if rec_name and st.session_state.mirror_name == rec_name:
        st.caption(f"💞 おすすめの {rec_name} が、いま口で来てるわよ")
    elif rec_name and rec_name in _mirror_names:
        if st.button(f"💞 おすすめの {rec_name} で鏡チェック", key="mirror_pick_rec", use_container_width=True):
            _mirror_switch_to(rec_name, _mirror_with_img or _mirror_pool)
            st.rerun()

    if st.session_state.get("mirror_onape_sel") not in _mirror_names:
        st.session_state.mirror_onape_sel = st.session_state.mirror_name
    st.session_state.setdefault("mirror_step", 0)
    st.session_state.setdefault("mirror_gauge", "touch")
    st.session_state.setdefault("mirror_permit", None)

    st.markdown("<h3 style='text-align:center'>🪞 鏡チェック</h3>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align:center;color:#ffb6d9;font-style:italic;font-size:0.9em;"
        "margin-bottom:0.6em;'>フェラと亀頭キスで、イかせに来てるわよ</div>",
        unsafe_allow_html=True,
    )

    selected_onape = st.selectbox(
        "どのオナペにイかせてもらう？",
        _mirror_names,
        key="mirror_onape_sel",
    )
    if selected_onape != st.session_state.get("mirror_name"):
        if _mirror_switch_to(selected_onape, _mirror_with_img or _mirror_pool, sync_select=False):
            st.rerun()

    mirror_name = st.session_state.mirror_name
    mirror_item_key = next(
        (k for k, v in data["items"].items() if v.get("name") == mirror_name),
        None,
    )
    mirror_item = (
        data["items"][mirror_item_key]
        if mirror_item_key
        else next(
            (v for v in (_mirror_with_img or _mirror_pool) if v.get("name") == mirror_name),
            (_mirror_with_img or _mirror_pool)[0],
        )
    )
    st.session_state.mirror_img = mirror_item.get("img", "") or st.session_state.get("mirror_img", "")
    mirror_name = mirror_item.get("name", mirror_name)
    mirror_tags = list(mirror_item.get("weak_tags") or [])
    mirror_note = str(mirror_item.get("mirror_note") or "")
    mirror_loss_n = mirror_loss_count(mirror_name, data.get("history", []))
    mirror_streak = mirror_loss_streak_days(mirror_name, data.get("history", []))
    mirror_cal = mirror_calendar_whisper(mirror_name, data.get("history", []), count_date)
    mirror_weak_lv = mirror_weak_level(mirror_loss_n)
    st.session_state.setdefault("mirror_voice", "sweet")
    st.session_state.setdefault("mirror_edge_loop", 0)

    voice_labs = [lab for _, lab in MIRROR_VOICES]
    voice_keys = [k for k, _ in MIRROR_VOICES]
    cur_voice = st.session_state.get("mirror_voice", "sweet")
    try:
        v_idx = voice_keys.index(cur_voice)
    except ValueError:
        v_idx = 0
    voice_lab = st.radio(
        "声のトーン",
        voice_labs,
        index=v_idx,
        horizontal=True,
        key="mirror_voice_radio",
    )
    mirror_voice = voice_keys[voice_labs.index(voice_lab)]
    st.session_state.mirror_voice = mirror_voice
    if mirror_weak_lv >= 1:
        lv_lbl = "育ってきた弱点" if mirror_weak_lv == 1 else "完成した弱点"
        st.caption(f"弱点成長：{mirror_name}に累計 {mirror_loss_n} 回負け → {lv_lbl}")

    mirror_img_html = img_to_html(
        st.session_state.mirror_img,
        style="width:100%;max-height:360px;object-fit:cover;border-radius:14px;",
    )

    # 前回の負け囁き
    if (
        "mirror_hist_whisper" not in st.session_state
        or st.session_state.get("mirror_hist_for") != mirror_name
    ):
        st.session_state.mirror_hist_whisper = mirror_history_whisper(
            mirror_name, data.get("history", [])
        )
        st.session_state.mirror_hist_for = mirror_name

    # 開いた瞬間のささやき（回答前）
    if (
        "mirror_open_base" not in st.session_state
        or st.session_state.get("mirror_open_for") != mirror_name
    ):
        open_lines = [
            (
                f"{mirror_name}、フェラと亀頭キスでイかせに来たわよ。"
                f"先端にちゅってして、熱い口で包んで……出るまで離さないつもり。"
                f"いま、どのくらい弱い？正直に言いなさい。"
            ),
            (
                f"ふふ、今日は焦らして終わらせないわ。"
                f"口でして、先端にちゅっちゅして、そのままイかせる。"
                f"{mirror_name}の唇と喉、想像しながら状態を報告しなさい。"
            ),
            (
                f"咥えて、キスして、イかせる。その前提で来てるの。"
                f"{mirror_name}が弱い先にキスしてから奥まで咥えるところ……もう浮かんでるでしょ。"
                f"いまの体、どこまでとろけてる？"
            ),
            (
                f"{mirror_name}のフェラ想像してるでしょ。亀頭キスつきよ。"
                f"ちゅってされるたび腰が引けて、咥えられたら頭真っ白……その続きまで付き合うわ。"
                f"だから正直に。硬い？触ってる？もうイキそう？"
            ),
            (
                f"手じゃなく口で行かせてあげる。先端ちゅっちゅしながらね。"
                f"{mirror_name}の唇が先をふさいで、ぬるっと咥えて、またキス。"
                f"そのつもりで、いまの弱さを見せなさい。"
            ),
            (
                f"見てるだけで疼くなら、もう負けはじまってるわ。"
                f"{mirror_name}が口で来て、亀頭にキスして、フェラで仕上げる……逃げ道ないわよ。"
                f"ふふ、イかせに来たの。状態、言いなさい。"
            ),
        ]
        if ab_days and ab_days >= 2:
            open_lines.append(
                (
                    f"{ab_days}日分、口と亀頭キスで全部出させてあげる。"
                    f"溜めた先端に{mirror_name}がちゅってして、奥まで咥えて受け止めるわ。"
                    f"……溜めたまま来なさい。今日はちゃんとイかせるから。"
                )
            )
        if mirror_streak >= 3:
            open_lines.append(
                (
                    f"{mirror_streak}日連続で{mirror_name}の口に負けてるわね。"
                    f"……今日も同じ負け方、続ける？咥えられて、ちゅってされて、情けなくイく番よ。"
                )
            )
        weak_open = mirror_weak_flavor(mirror_name, mirror_tags, mirror_loss_n, mirror_note)
        chosen = random.choice(open_lines)
        if weak_open:
            chosen = f"{chosen}{weak_open}"
        st.session_state.mirror_open_base = chosen
        st.session_state.mirror_open_for = mirror_name

    st.session_state.mirror_open_line = mirror_with_voice(
        st.session_state.mirror_open_base, mirror_voice, mirror_name
    )

    st.markdown(f"""
<div class="tease-wall" style="max-width:520px;margin:0 auto 0.8em;">
  <div class="tease-badge">💋 {mirror_name} が口で来るわよ</div>
  {mirror_img_html if mirror_img_html else ''}
  <div class="mirror-chu" style="margin-top:0.55em;font-size:0.85em;">ちゅっ……</div>
  <div class="tease-line mirror-line-main" style="margin-top:0.35em;line-height:1.55;text-align:left;">
    「{st.session_state.mirror_open_line}」
  </div>
  <div class="mirror-after-delay" style="color:#ffb6d9;font-style:italic;font-size:0.88em;
    margin-top:0.65em;line-height:1.45;text-align:left;border-top:1px solid rgba(255,64,129,0.25);padding-top:0.55em;">
    「{st.session_state.mirror_hist_whisper}」
  </div>
  {f'<div class="mirror-after-delay" style="color:#ff80ab;font-style:italic;font-size:0.82em;margin-top:0.5em;line-height:1.4;text-align:left;">「{mirror_cal}」</div>' if mirror_cal else ''}
</div>
""", unsafe_allow_html=True)
    if not mirror_img_html:
        raw = st.session_state.mirror_img or ""
        if raw.startswith("data:") and "," in raw:
            try:
                import base64
                from io import BytesIO
                st.image(BytesIO(base64.b64decode(raw.split(",", 1)[1])), use_container_width=True)
            except Exception:
                st.caption("画像を読み込めなかったわ……別の子を見てみて")
        else:
            st.caption("この子はまだ画像がないわ。でも口では来れるわよ")

    # --- 弱点メモ ---
    with st.expander("弱点メモ（セリフに混ざるよ）", expanded=False):
        picked_tags = st.multiselect(
            f"{mirror_name}の口プレイ弱点",
            MIRROR_WEAK_OPTIONS,
            default=[t for t in mirror_tags if t in MIRROR_WEAK_OPTIONS],
            key=f"mirror_weak_sel_{mirror_name}",
        )
        note_input = st.text_area(
            "いまの状態（自己申告・次のセリフに混ざる）",
            value=mirror_note,
            key=f"mirror_note_input_{mirror_name}",
            placeholder="例：先端ちゅう中、咥えられてる想像、もう出そう…",
            max_chars=120,
        )
        if st.button("弱点メモを保存", key="mirror_weak_save", use_container_width=True):
            if mirror_item_key:
                data["items"][mirror_item_key]["weak_tags"] = list(picked_tags)
                data["items"][mirror_item_key]["mirror_note"] = note_input.strip()
                save_data(data)
                st.session_state.pop("mirror_open_base", None)
                st.success("保存したわ。次のセリフから混ざるわよ")
                st.rerun()
        if mirror_tags:
            st.caption("弱点タグ: " + " / ".join(mirror_tags))
        if len(mirror_tags) >= 2:
            st.caption("弱点コンボ有効（2つ以上で専用セリフ）")

    # --- イキそうゲージ ---
    st.markdown("##### イキそうゲージ")
    g_labels = [f"{lab}" for _, lab, _ in MIRROR_GAUGE]
    g_keys = [k for k, _, _ in MIRROR_GAUGE]
    g_pcts = {k: p for k, _, p in MIRROR_GAUGE}
    cur_g = st.session_state.get("mirror_gauge", "touch")
    try:
        g_idx = g_keys.index(cur_g)
    except ValueError:
        g_idx = 0
        cur_g = g_keys[0]
    # 初回 or プログラム更新時のみ、radio を描画前に合わせる（描画後の書込は不可）
    if st.session_state.pop("_mirror_gauge_sync", False) or "mirror_gauge_radio" not in st.session_state:
        st.session_state.mirror_gauge_radio = g_labels[g_idx]
    g_choice = st.radio(
        "いまどのくらい？",
        g_labels,
        horizontal=True,
        key="mirror_gauge_radio",
        label_visibility="collapsed",
    )
    new_g = g_keys[g_labels.index(g_choice)]
    gauge_pct = g_pcts[new_g]
    hot_cls = "mirror-gauge-hot" if new_g in ("near", "cum") else ""
    st.markdown(f"""
<div class="{hot_cls}" style="max-width:520px;margin:0.2em auto 0.6em;">
  <div class="dev-bar-wrap" style="height:12px;"><div class="dev-bar" style="width:{gauge_pct}%;"></div></div>
  <div style="text-align:center;color:#ff80ab;font-size:0.78em;">{g_choice}</div>
</div>
""", unsafe_allow_html=True)
    if new_g != st.session_state.get("mirror_gauge"):
        st.session_state.mirror_gauge = new_g
        st.session_state.mirror_choice = f"gauge_{new_g}"
        st.session_state.mirror_reply_text = mirror_with_voice(
            mirror_gauge_lines(new_g, mirror_name, mirror_tags, mirror_loss_n, mirror_note),
            mirror_voice,
            mirror_name,
        )
        st.session_state.mirror_after_text = (
            f"ゲージは正直ね。……{mirror_name}の口プレイ、この熱に合わせてくるわよ。"
        )
        if new_g != "cum":
            st.session_state.mirror_permit = None
        st.rerun()

    def _mirror_pick(choice):
        main, after = mirror_enrich(
            choice,
            mirror_name,
            ab_days,
            mirror_tags,
            st.session_state.get("mirror_gauge"),
            mirror_loss_n,
            mirror_voice,
            mirror_note,
        )
        st.session_state.mirror_choice = choice
        st.session_state.mirror_reply_text = main
        st.session_state.mirror_after_text = after
        if choice in _MIRROR_FINISH_KEYS or st.session_state.get("mirror_gauge") == "cum":
            st.session_state.mirror_permit = "ask"
            st.session_state.mirror_permit_line = None
        st.rerun()

    st.markdown(
        "<div style='text-align:center;color:#ff80ab;font-size:0.78em;margin:0.4em 0 0.6em;'>"
        "口とキスでイかせる前提よ。いまの弱さを言いなさい</div>",
        unsafe_allow_html=True,
    )

    st.caption("反応")
    r1, r2, r3 = st.columns(3)
    with r1:
        if st.button("もう硬い…咥えられそう", key="mirror_hard", use_container_width=True):
            _mirror_pick("hard")
    with r2:
        if st.button("フェラしてほしい", key="mirror_want", use_container_width=True):
            _mirror_pick("want")
    with r3:
        if st.button("言えない…でも口が欲しい", key="mirror_silent", use_container_width=True):
            _mirror_pick("silent")

    st.caption("進捗")
    p1, p2, p3 = st.columns(3)
    with p1:
        if st.button("触りながら口想像してる", key="mirror_start", use_container_width=True):
            _mirror_pick("start")
    with p2:
        if st.button("しごいてる…フェラが欲しい", key="mirror_stroke", use_container_width=True):
            _mirror_pick("stroke")
    with p3:
        if st.button("イキそう…口でイカせて", key="mirror_edge", use_container_width=True):
            _mirror_set_gauge("cum")
            _mirror_pick("edge")

    # --- 口プレイ手順モード ---
    st.markdown("##### 口プレイ手順")
    step_i = int(st.session_state.get("mirror_step", 0) or 0)
    step_i = max(0, min(step_i, len(MIRROR_STEPS) - 1))
    dots = "".join(
        f'<span class="mirror-step-dot {"on" if i <= step_i else ""}"></span>'
        for i in range(len(MIRROR_STEPS))
    )
    step_label, step_key = MIRROR_STEPS[step_i]
    st.markdown(
        f"<div style='text-align:center;margin:0.2em 0 0.45em;'>{dots}"
        f"<div style='color:#ffb6d9;font-size:0.85em;margin-top:0.35em;'>"
        f"いま：{step_label}</div></div>",
        unsafe_allow_html=True,
    )
    s_prev, s_now, s_next = st.columns(3)
    with s_prev:
        if st.button("← 戻す", key="mirror_step_back", use_container_width=True, disabled=step_i <= 0):
            st.session_state.mirror_step = step_i - 1
            sk = MIRROR_STEPS[st.session_state.mirror_step][1]
            st.session_state.mirror_choice = sk
            st.session_state.mirror_reply_text = mirror_with_voice(
                mirror_step_lines(sk, mirror_name, mirror_tags, mirror_loss_n, mirror_note),
                mirror_voice,
                mirror_name,
            )
            st.session_state.mirror_after_text = mirror_step_after(sk, mirror_name)
            st.session_state.mirror_permit = None
            st.rerun()
    with s_now:
        if st.button("この手順で囁く", key="mirror_step_say", use_container_width=True):
            st.session_state.mirror_choice = step_key
            st.session_state.mirror_reply_text = mirror_with_voice(
                mirror_step_lines(step_key, mirror_name, mirror_tags, mirror_loss_n, mirror_note),
                mirror_voice,
                mirror_name,
            )
            st.session_state.mirror_after_text = mirror_step_after(step_key, mirror_name)
            if step_key == "finish" or st.session_state.get("mirror_gauge") == "cum":
                st.session_state.mirror_permit = "ask"
            st.rerun()
    with s_next:
        if st.button(
            "次へ →" if step_i < len(MIRROR_STEPS) - 1 else "仕上げへ",
            key="mirror_step_next",
            use_container_width=True,
        ):
            if step_i < len(MIRROR_STEPS) - 1:
                st.session_state.mirror_step = step_i + 1
            sk = MIRROR_STEPS[st.session_state.mirror_step][1]
            st.session_state.mirror_choice = sk
            st.session_state.mirror_reply_text = mirror_with_voice(
                mirror_step_lines(sk, mirror_name, mirror_tags, mirror_loss_n, mirror_note),
                mirror_voice,
                mirror_name,
            )
            st.session_state.mirror_after_text = mirror_step_after(sk, mirror_name)
            if sk == "finish":
                _mirror_set_gauge("cum")
                st.session_state.mirror_permit = "ask"
            elif st.session_state.mirror_step >= 2 and st.session_state.get("mirror_gauge") == "touch":
                _mirror_set_gauge("near")
            st.rerun()

    st.markdown("##### 決め技")
    st.caption("どれでイかせてほしいか、選んでね")
    finisher_label = st.radio(
        "決め技を選ぶ",
        _MIRROR_FINISHER_LABELS,
        key="mirror_finisher_radio",
        label_visibility="collapsed",
    )
    if st.button("💋 この決め技でイかせて", key="mirror_finisher_go", use_container_width=True):
        st.session_state.mirror_step = len(MIRROR_STEPS) - 1
        _mirror_pick(_MIRROR_FINISHER_KEY.get(finisher_label, "kiss"))

    c_shuf, c_more = st.columns(2)
    with c_shuf:
        if st.button("🔀 ランダムで別の子", key="mirror_shuffle", use_container_width=True):
            others = [v for v in (_mirror_with_img or _mirror_pool) if v.get("name") != mirror_name]
            if others:
                nxt = random.choice(others)
                _mirror_switch_to(nxt.get("name", ""), _mirror_with_img or _mirror_pool)
                st.rerun()
    with c_more:
        if st.button("💋 もっと口でイかせに来る", key="mirror_more", use_container_width=True):
            finishers = ("kiss", "glans", "mouth")
            choice = st.session_state.get("mirror_choice") or "kiss"
            choice = {"touch": "want"}.get(choice, choice)
            if choice not in finishers and random.random() < 0.6:
                choice = random.choice(finishers)
            elif choice not in finishers + ("edge",) and random.random() < 0.35:
                choice = "edge"
            elif choice in finishers and random.random() < 0.4:
                choice = random.choice(finishers)
            _mirror_pick(choice)

    if st.session_state.get("mirror_reply_text"):
        after = st.session_state.get("mirror_after_text") or ""
        _badge = {
            "kiss": "フェラ＋亀頭キスで行かせる",
            "glans": "亀頭キスで溶かす",
            "mouth": "口で堕としてイかせる",
            "kiss_only": "まずは亀頭キスだけ",
            "lick": "先端をねっとり舐める",
            "shallow": "浅く咥えて溶かす",
            "deep": "深く咥えて堕とす",
            "finish": "口で仕上げてイかせる",
            "gauge_touch": "触りながらの口想像",
            "gauge_near": "限界ふちで口責め",
            "gauge_cum": "もう出る…許可待ち",
            "denied": "まだだめ…ふちで焦らし",
            "mouth_ok": "口だけ許可・まだ出さない",
            "granted": "許可済み・イけ",
        }.get(st.session_state.get("mirror_choice"), "フェラ＋亀頭キスで行かせる")
        _choice = st.session_state.get("mirror_choice") or ""
        if str(_choice).startswith("edge_loop_"):
            _badge = f"イく直前ループ ×{_choice.split('_')[-1]}"
        st.markdown(f"""
<div style="max-width:520px;margin:0.6em auto 0.4em;
  background:linear-gradient(160deg,rgba(194,24,91,0.22),rgba(40,0,25,0.55));
  border:1px solid #ff4081;border-radius:14px;padding:1em;text-align:center;
  box-shadow:0 0 18px rgba(255,64,129,0.25);">
  <div style="color:#ff80ab;font-size:0.75em;letter-spacing:0.1em;margin-bottom:0.35em;">💋 {_badge}</div>
  <div class="mirror-chu" style="font-size:0.8em;margin-bottom:0.35em;">ちゅっ……</div>
  <div class="mirror-line-main" style="color:#ffb6d9;font-style:italic;font-size:1.02em;
    margin-bottom:0.55em;line-height:1.55;text-align:left;">
    「{st.session_state.mirror_reply_text}」
  </div>
  <div class="mirror-after-delay" style="color:#ffe0f0;font-style:italic;font-size:0.92em;
    opacity:0.95;line-height:1.5;text-align:left;">
    「{after}」
  </div>
</div>
""", unsafe_allow_html=True)

    # --- イく直前ループ ---
    st.markdown("##### イく直前ループ")
    edge_n = int(st.session_state.get("mirror_edge_loop", 0) or 0)
    st.caption(f"許可なしでふちを積み上げるよ（いま {edge_n}/5）")
    if st.button(
        "🔥 ふちでもう一度…まだ出させない",
        key="mirror_edge_loop_btn",
        use_container_width=True,
    ):
        edge_n = min(5, edge_n + 1)
        st.session_state.mirror_edge_loop = edge_n
        _mirror_set_gauge("near" if edge_n < 5 else "cum")
        main, after = mirror_edge_loop_lines(mirror_name, edge_n, mirror_tags, mirror_loss_n, mirror_note)
        st.session_state.mirror_choice = f"edge_loop_{edge_n}"
        st.session_state.mirror_reply_text = mirror_with_voice(main, mirror_voice, mirror_name)
        st.session_state.mirror_after_text = after
        st.session_state.mirror_permit = "ask" if edge_n >= 3 else "denied"
        st.rerun()

    # --- 出していい？許可制（3段階）---
    show_permit = (
        st.session_state.get("mirror_permit") in ("ask", "denied", "mouth_ok", "granted")
        or st.session_state.get("mirror_gauge") == "cum"
        or st.session_state.get("mirror_choice") in _MIRROR_FINISH_KEYS
        or str(st.session_state.get("mirror_choice") or "").startswith("edge_loop_")
        or int(st.session_state.get("mirror_step", 0) or 0) >= len(MIRROR_STEPS) - 1
    )
    permit_stage = st.session_state.get("mirror_permit") or "ask"
    if show_permit and permit_stage != "granted":
        if permit_stage not in ("ask", "denied", "mouth_ok", "granted"):
            st.session_state.mirror_permit = "ask"
            permit_stage = "ask"
        title = "出していい？" if permit_stage != "mouth_ok" else "口だけ許可中"
        hint = (
            f"「{mirror_name}の口でイきたいなら、許可を段階で求めなさい。まだだめ / 口だけ / 出していい」"
            if permit_stage != "mouth_ok"
            else f"「口は使っていいわ。でも射精はまだ。……出していい許可、求める？」"
        )
        st.markdown(f"""
<div class="mirror-permit-delay" style="max-width:520px;margin:0.5em auto;padding:0.85em 1em;
  border:1px dashed #ff80ab;border-radius:12px;text-align:center;
  background:rgba(80,0,40,0.35);">
  <div style="color:#ff80ab;font-size:0.78em;letter-spacing:0.12em;">{title}</div>
  <div style="color:#ffb6d9;font-style:italic;font-size:0.95em;margin-top:0.35em;">{hint}</div>
</div>
""", unsafe_allow_html=True)
        if permit_stage == "mouth_ok":
            m1, m2 = st.columns(2)
            with m1:
                if st.button("まだだめ…口も止めて", key="mirror_deny", use_container_width=True):
                    st.session_state.mirror_permit = "denied"
                    st.session_state.mirror_permit_line = mirror_with_voice(
                        mirror_permit_lines(mirror_name, "deny"), mirror_voice, mirror_name
                    )
                    _mirror_set_gauge("near")
                    st.session_state.mirror_reply_text = st.session_state.mirror_permit_line
                    st.session_state.mirror_after_text = (
                        f"口も一旦止めるわ。{mirror_name}のキスだけで、またふちまで戻しなさい。"
                    )
                    st.session_state.mirror_choice = "denied"
                    st.rerun()
            with m2:
                if st.button("出していいわ…イけ", key="mirror_allow", use_container_width=True):
                    st.session_state.mirror_permit = "granted"
                    st.session_state.mirror_permit_line = mirror_with_voice(
                        mirror_permit_lines(mirror_name, "grant"), mirror_voice, mirror_name
                    )
                    _mirror_set_gauge("cum")
                    st.session_state.mirror_reply_text = st.session_state.mirror_permit_line
                    st.session_state.mirror_after_text = (
                        f"射精の許可、出したわ。口に負けて出したら記録しなさい。余韻も続くわよ。"
                    )
                    st.session_state.mirror_choice = "granted"
                    st.rerun()
        else:
            d1, d2, d3 = st.columns(3)
            with d1:
                if st.button("まだだめ", key="mirror_deny", use_container_width=True):
                    st.session_state.mirror_permit = "denied"
                    st.session_state.mirror_permit_line = mirror_with_voice(
                        mirror_permit_lines(mirror_name, "deny"), mirror_voice, mirror_name
                    )
                    _mirror_set_gauge("near")
                    st.session_state.mirror_reply_text = st.session_state.mirror_permit_line
                    st.session_state.mirror_after_text = (
                        f"許可、まだないわ。{mirror_name}のキスと浅いフェラで、ふちのまま溶かされなさい。"
                    )
                    st.session_state.mirror_choice = "denied"
                    st.rerun()
            with d2:
                if st.button("口だけ…いいわ", key="mirror_mouth_ok", use_container_width=True):
                    st.session_state.mirror_permit = "mouth_ok"
                    st.session_state.mirror_permit_line = mirror_with_voice(
                        mirror_permit_lines(mirror_name, "mouth"), mirror_voice, mirror_name
                    )
                    _mirror_set_gauge("near")
                    st.session_state.mirror_reply_text = st.session_state.mirror_permit_line
                    st.session_state.mirror_after_text = (
                        f"口だけ許可。咥えて、キスして……でもまだ出さない。"
                        f"射精の許可は、そのあとね。"
                    )
                    st.session_state.mirror_choice = "mouth_ok"
                    st.rerun()
            with d3:
                if st.button("出していい…イけ", key="mirror_allow", use_container_width=True):
                    st.session_state.mirror_permit = "granted"
                    st.session_state.mirror_permit_line = mirror_with_voice(
                        mirror_permit_lines(mirror_name, "grant"), mirror_voice, mirror_name
                    )
                    _mirror_set_gauge("cum")
                    st.session_state.mirror_reply_text = st.session_state.mirror_permit_line
                    st.session_state.mirror_after_text = (
                        f"許可出たわ。口に負けて出したら、下のボタンで情けなく記録しなさい。"
                    )
                    st.session_state.mirror_choice = "granted"
                    st.rerun()

    if st.session_state.get("mirror_permit") == "granted":
        st.markdown(f"""
<div style="max-width:520px;margin:0.55em auto;padding:0.9em;text-align:center;
  background:linear-gradient(160deg,rgba(255,64,129,0.28),rgba(40,0,25,0.6));
  border:1px solid #ff80ab;border-radius:14px;">
  <div style="color:#ff80ab;font-size:0.78em;">💋 許可済み・口でイけ</div>
  <div style="color:#ffe0f0;font-style:italic;font-size:0.95em;margin-top:0.4em;line-height:1.5;">
    「{st.session_state.get("mirror_permit_line") or mirror_permit_lines(mirror_name, "grant")}」
  </div>
</div>
""", unsafe_allow_html=True)
        if month_filter is not None:
            if st.button(
                f"💋 {mirror_name}に敗北射精する",
                key="mirror_defeat_btn",
                use_container_width=True,
            ):
                _mirror_record_defeat(mirror_name)
                st.rerun()
        else:
            st.caption("月を選ぶと、許可後にここから敗北射精を記録できるわ")

else:
    st.markdown("<h3 style='text-align:center'>🪞 鏡チェック</h3>", unsafe_allow_html=True)
    st.caption("弱点（オナペ）を登録すると、ここで選べるわよ。")

# === TRIAL TEASE START ===
if trial_tease:
    tease_items = [v for v in data["items"].values() if v.get("img")]
    if not tease_items:
        tease_items = list(data["items"].values())

    # 0) 今日まだ負けてない日のバナー
    if clean_day:
        st.markdown(
            "<div style='text-align:center;background:rgba(194,24,91,0.18);"
            "border:1px solid #ff4081;border-radius:12px;padding:0.7em;margin-bottom:0.9em;'>"
            "<div style='color:#ff80ab;font-size:0.78em;letter-spacing:0.08em;'>🕊 今日はまだ負けてない</div>"
            "<div style='color:#ffb6d9;font-style:italic;font-size:0.95em;'>"
            "「我慢の日？……じゃあ、せめて見ていきなさい。記録は後でいいわ」"
            "</div></div>",
            unsafe_allow_html=True,
        )
    elif is_night:
        st.markdown(
            "<div style='text-align:center;background:rgba(80,0,40,0.35);"
            "border:1px solid #c2185b;border-radius:12px;padding:0.55em;margin-bottom:0.9em;"
            "color:#ffb6d9;font-style:italic;'>"
            "🌙 夜の甘マゾ時間……見るだけで十分疼くわよ"
            "</div>",
            unsafe_allow_html=True,
        )

    # 1) 壁ドン起動
    if tease_items and not st.session_state.get("tease_wall_dismissed"):
        if "tease_wall_name" not in st.session_state:
            pick = random.choice(tease_items)
            st.session_state.tease_wall_name = pick.get("name", "")
            st.session_state.tease_wall_img = pick.get("img", "")
        wall_name = st.session_state.tease_wall_name
        wall_img = img_to_html(
            st.session_state.tease_wall_img,
            style="width:100%;max-height:320px;object-fit:cover;border-radius:12px;",
        )
        wall_line = tease_wall_lines(wall_name, ab_days, night=is_night, clean_day=clean_day)
        night_tag = "🌙 夜の壁ドン" if is_night else "💋 ただ見に来ただけ？"
        st.markdown(f"""
<div class="tease-wall">
  <div class="tease-badge">{night_tag}</div>
  {wall_img}
  <h2 style="color:#ffe0f0;margin:0.2em 0;">🌸 {wall_name}</h2>
  <div class="tease-line">「{wall_line}」</div>
  <div style="color:#804060;font-size:0.78em;margin-top:0.4em;">カウントしなくていいわ。まず見てなさい。</div>
</div>
""", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("👀 もっと見る", key="tease_keep", use_container_width=True):
                st.session_state.tease_wall_dismissed = True
                st.session_state.tease_focus = "gallery"
                st.rerun()
        with c2:
            if st.button("閉じる（記録へ）", key="tease_close", use_container_width=True):
                st.session_state.tease_wall_dismissed = True
                st.rerun()

    # 3) 次に負ける相手 断言
    pred = tease_predict_next(data.get("history", []), tease_items or list(data["items"].values()), hour)
    if pred:
        p_name, p_item, p_line = pred
        p_img = img_to_html(
            p_item.get("img", ""),
            style="width:100%;max-height:240px;object-fit:cover;border-radius:12px;",
        )
        st.markdown(f"""
<div class="ero-card" style="border:1px solid #ff4081;max-width:480px;margin:0 auto 1.2em;">
  <div style="color:#ff80ab;font-size:0.8em;letter-spacing:0.1em;">🔮 次に負ける相手</div>
  {p_img}
  <h3 style="margin:0.3em 0;">🌸 {p_name}</h3>
  <div class="tease-line">「{p_line}」</div>
</div>
""", unsafe_allow_html=True)

    # 4) 観賞スライドショー（大きく1枚＋次へ）
    if tease_items:
        st.markdown("<h3 style='text-align:center'>🎞 観賞スライド</h3>", unsafe_allow_html=True)
        st.caption("手を動かさなくていいわ。顔だけ、ゆっくり見てなさい。")
        if "tease_slide_idx" not in st.session_state:
            st.session_state.tease_slide_idx = random.randrange(len(tease_items))
        s_idx = st.session_state.tease_slide_idx % len(tease_items)
        s_item = tease_items[s_idx]
        s_name = s_item.get("name", "")
        s_img = img_to_html(
            s_item.get("img", ""),
            style="width:100%;max-height:360px;object-fit:cover;border-radius:14px;",
        )
        s_line = tease_gallery_whisper(s_name, night=is_night)
        st.markdown(f"""
<div class="tease-wall" style="max-width:520px;">
  <div class="tease-badge">👀 {s_idx + 1} / {len(tease_items)}</div>
  {s_img}
  <h2 style="color:#ffe0f0;margin:0.3em 0;">🌸 {s_name}</h2>
  <div class="tease-line">「{s_line}」</div>
</div>
""", unsafe_allow_html=True)
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("⏭ 次の顔", key="tease_slide_next", use_container_width=True):
                st.session_state.tease_slide_idx = (s_idx + 1) % len(tease_items)
                st.rerun()
        with sc2:
            if st.button("🔀 ランダム", key="tease_slide_rand", use_container_width=True):
                st.session_state.tease_slide_idx = random.randrange(len(tease_items))
                st.rerun()

    # 5) 観賞グリッド
    if tease_items:
        st.markdown("<h3 style='text-align:center'>👀 観賞ギャラリー</h3>", unsafe_allow_html=True)
        if st.button("🔀 別の顔を並べる", key="tease_gallery_shuffle"):
            st.session_state.tease_gallery_seed = random.randint(0, 10**9)
            st.rerun()
        g_seed = st.session_state.get("tease_gallery_seed", int(hashlib.md5(today_str.encode()).hexdigest(), 16))
        g_rng = random.Random(g_seed)
        gallery = tease_items[:]
        g_rng.shuffle(gallery)
        gallery = gallery[:6]
        cards = ""
        for it in gallery:
            n = it.get("name", "")
            thumb = img_to_html(
                it.get("img", ""),
                style="width:100%;height:120px;object-fit:cover;display:block;",
                face_detect=True,
            )
            whisper = tease_gallery_whisper(n, night=is_night)
            cards += (
                f"<div class='tease-gallery-item'>"
                f"{thumb}"
                f"<div class='name'>🌸 {n}</div>"
                f"<div style='color:#ffb6d9;font-style:italic;font-size:0.7em;padding:0 0.4em 0.5em;'>"
                f"「{whisper}」</div></div>"
            )
        st.markdown(f"<div class='tease-gallery-grid'>{cards}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # 6) 思い出再生
    hist_with_img = []
    for h in reversed(data.get("history", [])):
        item = next((v for v in data["items"].values() if v["name"] == h["name"]), None)
        if item and item.get("img"):
            hist_with_img.append((h, item))
            if len(hist_with_img) >= 30:
                break
    if hist_with_img:
        if st.button("📖 思い出を再生", key="tease_memory_btn", use_container_width=True):
            st.session_state.tease_memory = random.choice(hist_with_img)
        mem = st.session_state.get("tease_memory")
        if mem:
            h, item = mem
            try:
                dt = datetime.strptime(h["time"], "%Y-%m-%d %H:%M:%S")
                when_lbl = f"{dt.month}月{dt.day}日"
            except Exception:
                when_lbl = h["time"][:10]
            mem_img = img_to_html(
                item.get("img", ""),
                style="width:100%;max-height:260px;object-fit:cover;border-radius:12px;",
            )
            mem_line = tease_memory_line(h["name"], when_lbl)
            st.markdown(f"""
<div class="ero-card" style="border:1px solid #ff4081;max-width:480px;margin:0 auto 1.2em;">
  <div style="color:#ff80ab;font-size:0.8em;letter-spacing:0.1em;">📖 思い出再生</div>
  {mem_img}
  <h3 style="margin:0.3em 0;">🌸 {h['name']}</h3>
  <div style="color:#804060;font-size:0.8em;">{when_lbl}　{h['time'][11:16]}</div>
  <div class="tease-line">「{mem_line}」</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
# === TRIAL TEASE END ===

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
    if rec_name:
        st.caption(f"鏡チェックは {rec_name} を優先して選びやすいわ（上の🪞へ）")

st.divider()

# ===== 週間危険予報 =====
st.markdown(weekly_danger_html(data["history"], today_jst), unsafe_allow_html=True)

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
elif count_date < today_jst:
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
                st.session_state.defeat_flash_name = name
                _mirror_start_afterglow(name)
                st.rerun()

st.divider()

# ===== 月間カレンダー =====
if month_filter:
    cal_year, cal_month = int(month_filter[:4]), int(month_filter[5:7])
else:
    cal_year, cal_month = now_jst.year, now_jst.month
st.markdown(render_calendar(data["history"], cal_year, cal_month, data["items"]), unsafe_allow_html=True)

st.markdown("<h3>📖 敗北日記</h3>", unsafe_allow_html=True)

# 月ごとのカウントを計算（日記コメント用）
month_running = {}
history_ordered = list(data["history"])
for h in history_ordered:
    m = h["time"][:7]
    month_running[m] = month_running.get(m, 0) + 1

# 月ごとの累計を逆算するため、各エントリに「その月で何回目か」を付ける
month_idx = {}
history_with_idx = []
for h in history_ordered:
    m = h["time"][:7]
    month_idx[m] = month_idx.get(m, 0) + 1
    history_with_idx.append((h, month_idx[m]))

diary_html = ""
for h, m_count in reversed(history_with_idx[-20:]):
    date_lbl, time_lbl, comment = diary_line(h, m_count)
    diary_html += (
        f"<div style='border-left:2px solid rgba(194,24,91,0.4);padding:0.4em 0.8em;"
        f"margin-bottom:0.5em;'>"
        f"<div style='display:flex;gap:0.8em;align-items:baseline;'>"
        f"<span style='color:#ff80ab;font-size:0.8em;font-weight:700;'>{date_lbl}</span>"
        f"<span style='color:#804060;font-size:0.72em;'>{time_lbl}</span>"
        f"</div>"
        f"<div style='color:#ffb6d9;font-style:italic;font-size:0.85em;margin-top:0.15em;'>"
        f"「{comment}」</div>"
        f"</div>"
    )
if diary_html:
    st.markdown(
        f"<div style='background:rgba(15,0,10,0.5);border:1px solid rgba(194,24,91,0.25);"
        f"border-radius:12px;padding:0.8em;max-height:360px;overflow-y:auto;'>"
        f"{diary_html}</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown("<div style='color:#555;font-style:italic;'>まだ記録がないわ。</div>", unsafe_allow_html=True)
