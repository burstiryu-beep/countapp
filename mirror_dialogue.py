"""鏡チェック：対話しながら敗北射精まで堕ちる。"""
from __future__ import annotations

import hashlib
import random


def _rng(seed_key: str) -> random.Random:
    return random.Random(int(hashlib.md5(seed_key.encode("utf-8")).hexdigest(), 16))


def dialogue_turn_count(dialogue) -> int:
    """彼女の発話回数をターン数とする。"""
    if not dialogue:
        return 0
    return sum(1 for t in dialogue if t.get("role") == "her")


def dialogue_options(turn_n, gauge=None, permit=None):
    """いま選べる返事ボタン [(key, label), ...]。"""
    gauge = gauge or "touch"
    permit = permit or None
    turn_n = int(turn_n or 0)

    if permit == "granted":
        return [
            ("melt", "もう負けた…出る……"),
            ("thanks", "……イかされちゃった"),
        ]

    if gauge == "cum" or turn_n >= 6:
        return [
            ("beg_permit", "出していい…？　お願い……"),
            ("melt", "もう負けた…出る……"),
            ("resist_weak", "やめて…でも腰が止まらない……"),
            ("nipple_finish", "乳首も…口も…同時に……"),
        ]

    if gauge == "near" or turn_n >= 3:
        return [
            ("resist", "まだ出さないで…やめて……"),
            ("beg", "イかせて…お願い……"),
            ("edge", "ふちが…もうだめ……"),
            ("nipple_mouth", "上下同時は…ずるい……"),
        ]

    # early
    return [
        ("resist", "やめて…ちがう……"),
        ("want", "…もっと、口で……"),
        ("silent", "……言えない。でも……"),
        ("nipple", "乳首も…だめ……"),
    ]


def dialogue_her_lines(user_key, name, turn_n, gauge=None, tags=None, loss_n=0):
    """ユーザーの返事に対する彼女の本台詞・追い打ち・推奨ゲージ・許可ヒント。

    returns: (main, after, new_gauge, permit_hint)
    permit_hint: None | "ask" | "denied" | "mouth_ok"
    """
    gauge = gauge or "touch"
    tags = tags or []
    turn_n = int(turn_n or 0)
    loss_n = int(loss_n or 0)
    rng = _rng(f"dlg|{user_key}|{name}|{turn_n}|{gauge}|{loss_n}")

    has_nipple = any(str(t).startswith("乳首") for t in tags)

    pools = {
        "resist": [
            (
                f"ふふ、声だけ抵抗してる。……でも体はもう{name}の口に預けてるわね。",
                f"拒めば拒むほど、ちゅってしたくなるの。腰、逃げられないでしょ？",
            ),
            (
                f"やめて、って。……かわいい。{name}は離さないわよ。もっと溶かしてあげる。",
                "抵抗する声、いちばんエロいわ。先が正直なのも、見てるから。",
            ),
            (
                f"ちがう、って言いながら先が跳ねてる。……{name}の勝ちね。認めなさい。",
                "言葉は拒否、腰は懇願。甘マゾの対話、続けてあげる❤️",
            ),
        ],
        "want": [
            (
                f"もっと口が欲しいのね。……じゃあ深く咥えて、亀頭にちゅってしてあげる。",
                f"{name}の舌でとろけなさい。欲しがった罰よ。",
            ),
            (
                f"正直でえらい。……フェラしてほしがる声、好きよ。奥まで沈めてあげる。",
                "浅い→深い→キス。対話のたびに一段、堕とすわ。",
            ),
        ],
        "silent": [
            (
                f"言えないのね。……沈黙でも、先がびくびくしてるだけで十分よ。",
                f"{name}が咥えたら、声、漏れちゃうんでしょ。楽しみね。",
            ),
            (
                f"黙ってるくせに腰が前に出てる。……ふふ、{name}の口、来てるわよ。",
                "沈黙の敗北、いちばんかわいい。そのまま感じなさい。",
            ),
        ],
        "nipple": [
            (
                f"乳首もだめ、って。……摘まむわよ。口で咥えながら、乳輪ちゅって。",
                "上下同時に落とす対話ね。どっちが先に折れるか、見せなさい。",
            ),
            (
                f"乳首弱いの、隠れてないわよ。{name}が摘まんで、舐めて……声、出して。",
                "口だけじゃないの。対話のたびに乳首も攻めるわ❤️",
            ),
        ],
        "beg": [
            (
                f"イかせて、って。……いい子。でもまだ許可は段階よ。ふちで焦らしてあげる。",
                f"{name}の口で限界まで連れてく。出したいなら、ちゃんと乞いなさい。",
            ),
            (
                f"お願い、って震えてる。……かわいい。深く咥えて、イく直前で止めるわ。",
                "懇願対話、好きよ。もう一段とろけてから、出していいか聞くの。",
            ),
        ],
        "edge": [
            (
                f"ふちが……もうだめ、ね。なら、キスしながら限界の手前で止めちゃう。",
                f"出させない対話。{name}がふちを積み上げて、声だけ泣かせてあげる。",
            ),
            (
                f"限界のふちで対話してるの、エロいわ。……まだ出さない。口は離さないけど。",
                "びくびくしてる先に、ちゅって。……許可はまだよ。",
            ),
        ],
        "nipple_mouth": [
            (
                f"上下同時はずるい、って。……知っててやるの。咥えながら乳首ちゅって。",
                f"{name}の勝ち方、対話で確定ね。頭真っ白になるまで付き合うわ。",
            ),
            (
                f"ずるい、って言いながら沈んでる。……口も乳首も折れてるわよ。",
                "同時責め対話。抵抗する声と、イきたがる体、どっちが本音？",
            ),
        ],
        "beg_permit": [
            (
                f"出していい……？　ふふ、やっと乞えたわね。段階で答えるわよ。",
                f"まだだめ、か口だけ、か出していい——{name}が決める番。対話の仕上げよ。",
            ),
            (
                f"お願い……出したいのね。声が正直でかわいい。許可、考えてあげる。",
                "乞う対話まで来たなら、もう敗北の入口よ。覚悟しなさい。",
            ),
        ],
        "melt": [
            (
                f"もう負けた、出る……って。……いいわ。{name}の口で受け止めてあげる。",
                "対話の果てに敗北射精ね。情けない顔で、全部出しなさい❤️",
            ),
            (
                f"負けを認めたのね。ふふ、えらい。……じゃあイかせてあげる。出していいわ。",
                f"甘マゾの対話、完走。{name}に屈した記録、つけなさい。",
            ),
        ],
        "resist_weak": [
            (
                f"やめて、でも腰が止まらない……最高の矛盾ね。そのままイく直前まで連れてく。",
                f"{name}が離さないわ。声は抵抗、体は敗北。対話、まだ続くわよ。",
            ),
            (
                f"弱い抵抗……好きよ。先が跳ねてるのに、まだ拒むの？　かわいい。",
                "もう出るんでしょ。許可を乞う対話に切り替えなさい。",
            ),
        ],
        "nipple_finish": [
            (
                f"乳首も口も同時に……仕上げね。咥えて、摘まんで、ちゅってして、イかせる。",
                f"上下完落ちの対話。{name}の前じゃ、逃げ場ないわよ。",
            ),
        ],
        "thanks": [
            (
                f"イかされちゃった、ね。……ふふ、余韻まで甘やかしてあげる。",
                f"敗北射精のあとも、{name}のキスが残ってるでしょ。また対話しに来なさい。",
            ),
        ],
    }

    pair = rng.choice(pools.get(user_key) or pools["resist"])
    main, after = pair

    if has_nipple and user_key in ("want", "resist", "silent") and rng.random() < 0.45:
        after = f"{after}乳首も弱いの、覚えてるわよ。……摘まみながら対話してあげる。"

    if loss_n >= 3 and rng.random() < 0.4:
        after = f"{after}……{loss_n}回も負けてる相手に、また堕ちる対話ね。"

    # gauge / permit progression
    new_gauge = gauge
    permit_hint = None
    if user_key in ("melt",):
        new_gauge = "cum"
        permit_hint = "ask"
    elif user_key in ("beg_permit", "nipple_finish"):
        new_gauge = "cum"
        permit_hint = "ask"
    elif user_key in ("beg", "edge", "nipple_mouth", "resist_weak"):
        new_gauge = "near" if gauge != "cum" else "cum"
        if turn_n >= 4:
            permit_hint = "ask"
    elif user_key in ("want", "nipple"):
        if turn_n >= 2 and gauge == "touch":
            new_gauge = "near"
    elif user_key == "resist":
        if turn_n >= 4:
            new_gauge = "near" if gauge == "touch" else gauge
    elif user_key == "thanks":
        new_gauge = gauge
        permit_hint = "granted"

    # turn pressure
    if turn_n >= 5 and new_gauge == "touch":
        new_gauge = "near"
    if turn_n >= 7 and new_gauge != "cum":
        new_gauge = "cum"
        permit_hint = permit_hint or "ask"

    return main, after, new_gauge, permit_hint


def render_dialogue_html(dialogue, name="", max_show=24):
    """対話ログのHTML。最新が下。"""
    if not dialogue:
        return ""
    turns = dialogue[-max_show:]
    bubbles = []
    for t in turns:
        role = t.get("role") or "her"
        text = t.get("text") or ""
        if not text:
            continue
        if role == "you":
            label = "あなた（声だけ）"
            bg = "rgba(0,0,0,0.28)"
            border = "1px dashed rgba(255,182,217,0.45)"
            color = "#ffe0f0"
            align = "left"
        elif role == "her_after":
            label = f"{name}・追い打ち" if name else "彼女・追い打ち"
            bg = "transparent"
            border = "none"
            color = "#ffe0f0"
            align = "left"
        else:
            label = name or "彼女"
            bg = "rgba(194,24,91,0.12)"
            border = "1px solid rgba(255,64,129,0.25)"
            color = "#ffb6d9"
            align = "left"
        bubbles.append(
            f"""
  <div style="margin:0.4em 0;padding:0.5em 0.7em;border-radius:10px;
    background:{bg};border:{border};text-align:{align};">
    <div style="color:#ff80ab;font-size:0.68em;letter-spacing:0.08em;margin-bottom:0.2em;">{label}</div>
    <div style="color:{color};font-style:italic;font-size:0.92em;line-height:1.5;">「{text}」</div>
  </div>"""
        )
    n = dialogue_turn_count(dialogue)
    return f"""
<div style="max-width:520px;margin:0.6em auto 0.4em;
  background:linear-gradient(160deg,rgba(194,24,91,0.18),rgba(40,0,25,0.55));
  border:1px solid #ff4081;border-radius:14px;padding:0.85em 1em;
  box-shadow:0 0 18px rgba(255,64,129,0.22);">
  <div style="color:#ff80ab;font-size:0.75em;letter-spacing:0.1em;margin-bottom:0.45em;text-align:center;">
    💬 敗北対話 · {n}往復
  </div>
  <div style="max-height:420px;overflow-y:auto;padding-right:0.2em;">
    {''.join(bubbles)}
  </div>
</div>
"""
