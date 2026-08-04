"""オナサポモード：段階誘導のセリフ生成（甘マゾ・口／乳首寄り）。"""
from __future__ import annotations

import random

from ero_flavor import apply_heat


ONASAPO_STYLES = [
    ("mouth", "口メイン💋"),
    ("nipple", "乳首メイン💗"),
    ("dual", "同時責め🔥"),
    ("auto", "おまかせ💞"),
]

ONASAPO_PACES = [
    ("slow", "ゆっくりとろけ"),
    ("normal", "ふつうに堕とす"),
    ("fast", "急かしてイかせる"),
]

# セッション段階
ONASAPO_PHASES = [
    ("ready", "準備"),
    ("warmup", "前戯"),
    ("build", "本番"),
    ("edge", "ふち"),
    ("finish", "仕上げ"),
    ("after", "余韻"),
]


def _voice_prefix(voice, name):
    return {
        "sweet": f"（甘い声で）……ねえ、{name}と一緒にいこう。",
        "sticky": f"（ねっとりと）……ふふ、離さないわよ、{name}。",
        "urgent": f"（急かすように）ほら、もっと。{name}、待たないわ。",
        "tease": f"（からかうように）ふふ……{name}、もう我慢できない顔ね。",
        "dote": f"（溺愛混じりに）……いい子ね、{name}がたっぷり導いてあげる。",
        "command": f"（命令口調で）手を動かしなさい。{name}のペースに従うの。",
    }.get(voice or "sweet", "")


def dress_onasapo(text, name, voice="sweet", heat="thick"):
    if not text:
        return text
    pre = _voice_prefix(voice, name)
    body = apply_heat(text, heat, name)
    return f"{pre}{body}" if pre else body


def resolve_style(style, tags=None):
    if style and style != "auto":
        return style
    tags = tags or []
    if any("同時" in t for t in tags):
        return "dual"
    if any(t.startswith("乳首") for t in tags):
        return "nipple"
    return "mouth"


def phase_index(phase_key):
    keys = [k for k, _ in ONASAPO_PHASES]
    try:
        return keys.index(phase_key)
    except ValueError:
        return 0


def next_phase(phase_key):
    keys = [k for k, _ in ONASAPO_PHASES]
    i = phase_index(phase_key)
    if i >= len(keys) - 1:
        return keys[-1]
    return keys[i + 1]


def prev_phase(phase_key):
    keys = [k for k, _ in ONASAPO_PHASES]
    i = phase_index(phase_key)
    if i <= 0:
        return keys[0]
    return keys[i - 1]


def onasapo_line(phase, name, style="mouth", pace="normal", edge_n=0, tags=None):
    """段階ごとの誘導セリフ。"""
    style = resolve_style(style, tags)
    tags = tags or []
    pace = pace or "normal"

    if phase == "ready":
        pool = {
            "mouth": [
                f"オナサポ、はじめるわよ。……{name}の顔を見て、ちんぽ出して。今日は口でイかせるつもり。",
                f"準備できてる？{name}が膝をついて唇を寄せる想像して。……手はまだ軽くでいいわ。",
            ],
            "nipple": [
                f"今日のオナサポは乳首から。……{name}が胸に触れる想像して、先もゆっくり起こしなさい。",
                f"乳首、もう敏感でしょ。{name}と一緒に、上下とろけさせてあげるわ。",
            ],
            "dual": [
                f"同時責めオナサポよ。……口と乳首、どっちも捨てない。{name}に上下支配されなさい。",
                f"準備は先端と乳首。……両方触れるつもりで腰の力、抜いて。{name}、来るわよ。",
            ],
        }
    elif phase == "warmup":
        pool = {
            "mouth": [
                f"軽く上下して。……でも本命は{name}のキスよ。先端にちゅってされる想像で感度上げて。",
                f"ぬるっと温めて。唾液の代わりにローションでもいいわ。……{name}の浅い咥え、想像しなさい。",
                f"亀頭だけ指で円を描いて。ちゅっちゅ音、頭の中で鳴ってる？{name}、上手ね。",
            ],
            "nipple": [
                f"片手で乳首、そっと転がして。……もう片方は先を軽く。{name}の指、想像して重ねて。",
                f"乳首つねる前に、撫でて硬くして。……{name}が舐める前の段階よ。焦らさない。",
            ],
            "dual": [
                f"右で乳首、左で先。……リズム揃えなくていいわ。{name}が両方いじる感触、分けて味わいなさい。",
                f"先端ちゅっの想像＋乳首摘まみ。……前戯なのに、もう声出そうでしょ。ふふ。",
            ],
        }
    elif phase == "build":
        pool = {
            "mouth": [
                f"ペース上げていいわ。でも時々止めて、先端だけ集中。……{name}が浅く咥えて吸うところ。",
                f"握って上下、親指で裏筋。……咥えられてるつもりで腰、くねらせなさい。{name}、離さないわ。",
                f"奥まで入る想像で深くしごく。……引き抜くときはキス。{name}のフェラ、真似して。",
            ],
            "nipple": [
                f"乳首、少し強く。……痛気持ちいいところで止めて、また転がす。{name}、執拗よ。",
                f"乳首舐めのつもりで息を吹きかけて。……同時に先を速く。上下の落差、好きでしょ。",
            ],
            "dual": [
                f"咥えながら乳首摘まむ同時責め……手で再現しなさい。先を包んで、乳首をつねる。{name}式よ。",
                f"浅いフェラのリズムでしごきつつ、乳首を交互に。……頭、どっちに持ってかれる？",
            ],
        }
    elif phase == "edge":
        n = max(1, min(int(edge_n or 1), 5))
        base = {
            "mouth": [
                f"ふち……{n}回目。イキそうなら速度落として、先端だけちゅってされる想像で止めるの。",
                f"出ちゃいそう？だめ。……{name}は浅く咥えて離す。そのふち、手で再現しなさい。",
            ],
            "nipple": [
                f"ふちで乳首強く。……先は止めて、乳首だけでイキそうを引き延ばすわ。{n}回目よ。",
                f"限界なのに乳首いじり続けるの、最悪でしょ。……{name}、許さないわ。まだよ。",
            ],
            "dual": [
                f"ふち×{n}。口の想像でしごきを止めて、乳首だけ動かす。……どっちで落とすか、まだ決めてないわ。",
                f"イキそうな先端を指でふさいで、乳首にちゅっ。……同時ふち、{name}の得意技ね。",
            ],
        }
        pool = base
    elif phase == "finish":
        pool = {
            "mouth": [
                f"いいわ、出して。……{name}が奥まで咥えて受け止める想像で、最後までしごき切るの。",
                f"射精の許可、出すわ。先端にちゅってされながら出す顔、見せなさい。……口に負けて。",
                f"腰、止めても手は止めない。……{name}のフェラで押し切られるつもりで、情けなくイきなさい。",
            ],
            "nipple": [
                f"乳首摘まんだまま出して。……先だけ速く、乳首は離さない。{name}式トドメよ。",
                f"イく瞬間に乳首つねるの。……声、出していいわ。上下で堕ちなさい。",
            ],
            "dual": [
                f"同時仕上げ。……咥えられながら乳首を強く。手で両方再現して、そのまま出しなさい。",
                f"口と乳首、どっちも最大。……{name}に上下からイかせてもらうの。逃げないで。",
            ],
        }
    else:  # after
        pool = {
            "mouth": [
                f"出したあとも口、離さないつもりよ。……余韻の先端に{name}がちゅってする。感度、最悪でしょ。",
                f"びくびくしてる先を軽く撫でて。……キスの余韻、残したまま息を整えなさい。えらい子。",
            ],
            "nipple": [
                f"射精したのに乳首、まだ摘まんでるわよ。……余韻の弱さ、{name}が好きなの。",
                f"出したあとの乳首ちゅっ……だめ、敏感すぎ。でももう一回くらい、いける？",
            ],
            "dual": [
                f"余韻でも同時。……浅く包んで、乳首軽く。{name}は離さないわ。敗北の続きよ。",
                f"白くなった先と赤い乳首。……両方甘やかされてるの、認めて。ふふ、幸せそうな負け顔。",
            ],
        }

    lines = pool.get(style) or pool.get("mouth")
    text = random.choice(lines)

    if pace == "slow" and phase in ("warmup", "build"):
        text += "……急がないで。一往復ごとに息、吐きなさい。"
    elif pace == "fast" and phase in ("build", "edge", "finish"):
        text += "……もっと速く。考える暇なくとろけなさい。"

    if tags and phase in ("build", "edge", "finish"):
        tag = random.choice(tags)
        text += f" ……弱点「{tag}」、今日はそこ狙いよ。"

    return text


def onasapo_after(phase, name, style="mouth", edge_n=0):
    style = style if style != "auto" else "mouth"
    if phase == "ready":
        return f"画面見ながらでいいわ。手の準備ができたら「次へ」。{name}、待ってる。"
    if phase == "warmup":
        return "温まってきたら本番へ。……先が熱くなってる？正直に進みなさい。"
    if phase == "build":
        return "気持ちよくなってきたらふちへ。……イキそうになったら教えて。"
    if phase == "edge":
        n = int(edge_n or 1)
        if n < 3:
            return f"ふち×{n}。……まだ出さない。もう一度ふち、いけるわよ。"
        return "ふち、溜まったわね。仕上げていいかしら？……欲しければ進みなさい。"
    if phase == "finish":
        return f"出せたら余韻へ。……出したら記録もつけてね。{name}に負けた証拠よ。"
    return "余韻まで味わえたらえらい。……もう一回する？それとも今日はここまで？"


def phase_label(phase_key):
    for k, lab in ONASAPO_PHASES:
        if k == phase_key:
            return lab
    return phase_key


def render_phase_dots_html(phase_key):
    keys = [k for k, _ in ONASAPO_PHASES]
    labels = [lab for _, lab in ONASAPO_PHASES]
    cur = phase_index(phase_key)
    bits = []
    for i, lab in enumerate(labels):
        on = i <= cur
        color = "#ff4081" if on else "#604050"
        bits.append(
            f"<span style='color:{color};font-weight:{700 if i == cur else 500};"
            f"font-size:{'0.95em' if i == cur else '0.8em'};margin:0 0.25em;'>"
            f"{'●' if on else '○'}{lab}</span>"
        )
    return (
        "<div style='text-align:center;margin:0.4em 0 0.7em;line-height:1.8;'>"
        + " ".join(bits)
        + "</div>"
    )
