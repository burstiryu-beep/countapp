"""鏡チェック：対話しながら敗北射精まで堕ちる（濃い甘マゾ版）。"""
from __future__ import annotations

import hashlib
import random

from name_ja import nj


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
            ("melt", "もう負けた…口に出る……"),
            ("thanks", "……イかされちゃった。余韻が……"),
        ]

    if gauge == "cum" or turn_n >= 6:
        return [
            ("beg_permit", "出していい…？　口で受けて……お願い"),
            ("melt", "もう負けた…咥えられたまま出る……"),
            ("resist_weak", "やめて…でも腰が止まらない……んっ"),
            ("nipple_finish", "乳首も口も…同時にイかせて……"),
        ]

    if gauge == "near" or turn_n >= 3:
        return [
            ("resist", "まだ出さないで…ちゅってしないで……"),
            ("beg", "イかせて…深く咥えてお願い……"),
            ("edge", "ふちが…キスだけで壊れそう……"),
            ("nipple_mouth", "上下同時は…ずるい…でも欲しい……"),
        ]

    return [
        ("resist", "やめて…ちがう…咥えないで……"),
        ("want", "…もっと、口で溶かしして……"),
        ("silent", "……言えない。でも先が疼いてる……"),
        ("nipple", "乳首も…だめ…摘まないで……"),
    ]


def _sensual_tail(name, turn_n, rng, has_nipple=False):
    """ターンが進むほど濃くなる感触の追い足し。"""
    name = nj(name)
    early = [
        f"ちゅっ……って音、もう頭に残ってるでしょ。{name}の唇、温かいでしょう。",
        f"先端がぬるぬるになってきた。……{name}の唾液、混ざってるわよ。",
        "息がかかっただけで先が跳ねるの、見てるから。隠せないわ。",
    ]
    mid = [
        f"くちゅ、ちゅっ、ふかふか……{name}の口の中、もう逃げ場ないわね。",
        "浅いのに腰が砕けるの、かわいい。……深いのを想像しただけでびくびくしてる。",
        f"亀頭だけちゅってされて、乳輪まで熱い。……{name}、上下から溶かしてるの。",
        "先走りが糸を引いてる。……舐めたらもっと甘くなるわよ、ふふ。",
    ]
    late = [
        f"んっ……奥まで咥えたまま、舌で裏側をなぞるわ。{name}の口でイく直前ね。",
        "許可なしでも腰が震えてる。……出したいって体が泣いてるの、聞こえるわ。",
        f"涎と先走りでぐちゃぐちゃ。……その情けない先に、また{name}がちゅってする。",
        "頭真っ白でしょ？　声は拒否、先は懇願。……甘マゾの完成形ね。",
    ]
    nipple = [
        f"乳首も立ってるわよ。……摘まみながら咥えると、{name}の勝ちが早いの。",
        "乳輪にちゅって。……口で先をふさいだまま、乳首を転がしてあげる。",
        "上下同時に折れる音、想像しなさい。先も乳首も、びくびく同期してるわ。",
    ]
    if turn_n >= 6:
        pool = late + (nipple if has_nipple else [])
    elif turn_n >= 3:
        pool = mid + (nipple if has_nipple else [])
    else:
        pool = early + (nipple[:1] if has_nipple else [])
    return rng.choice(pool)


def dialogue_her_lines(user_key, name, turn_n, gauge=None, tags=None, loss_n=0):
    """ユーザーの返事に対する彼女の本台詞・追い打ち・推奨ゲージ・許可ヒント。

    returns: (main, after, new_gauge, permit_hint)
    """
    name = nj(name)
    gauge = gauge or "touch"
    tags = tags or []
    turn_n = int(turn_n or 0)
    loss_n = int(loss_n or 0)
    rng = _rng(f"dlg|{user_key}|{name}|{turn_n}|{gauge}|{loss_n}")

    has_nipple = any(str(t).startswith("乳首") for t in tags)

    pools = {
        "resist": [
            (
                f"ふふ、声だけ「やめて」って。……でも先が熱くて、もう{name}の唇に吸い寄せられてるわね。"
                f"ちゅっ、ってされた瞬間に腰が前に出るの、拒めてないでしょ。",
                f"拒めば拒むほど、亀頭にちゅってしたくなるの。ぬるぬるの先端をキスで崩して、"
                f"浅いフェラで溶かして……逃げられない対話、続けてあげる❤️",
            ),
            (
                f"やめて、って。……かわいい。{name}は離さないわよ。"
                f"先端にゆっくり唇を重ねて、ちゅっ……舌で裏筋をねっとり舐めて、また咥える。",
                "抵抗する声がいちばんエロいわ。先がびくびく跳ねてるのも、見てるから。"
                "言葉は拒否、腰は懇願。……甘マゾの本音、バレバレよ。",
            ),
            (
                f"ちがう、って言いながら先走りが光ってる。……{name}の勝ちね。認めなさい。"
                f"熱い口に包まれたまま、ちゅってされるたびに頭がとろけるの、分かってるでしょ。",
                "沈黙より弱い抵抗のほうが好きよ。咥えながら乳首も摘まんで、"
                "だめって言い終わる前に、体を折ってあげる。",
            ),
        ],
        "want": [
            (
                f"もっと口が欲しいのね。……じゃあ想像しなさい。"
                f"{name}が深く咥えて、喉奥で締めながら、引き抜くたびに亀頭にちゅってする。",
                f"ぬるぬるの舌で先端を転がして、ふかふか奥まで沈めて……欲しがった罰よ。"
                f"{name}の口でとろけなさい。イく直前まで離さないわ。",
            ),
            (
                f"正直でえらい。……フェラしてほしがる声、好きよ。"
                f"浅い→深い→キス。対話のたびに一段、涎まみれにして堕とすわ。",
                f"先端が唾液で光って、くちゅって音がするたび腰が砕ける……その続きを、"
                f"{name}がちゃんと口で押し切ってあげる。情けなく欲しがりなさい。",
            ),
            (
                f"「もっと口で」って……ふふ、もう先が跳ねてるわよ。"
                f"{name}の唇が弱いところをふさいで、ちゅっ、ちゅっ……次は奥まで一気に。",
                "欲しがる対話、大好き。咥えられたまま乳首も摘まれて、"
                "どっちが先に折れるか、自分で感じなさい。",
            ),
        ],
        "silent": [
            (
                f"言えないのね。……沈黙でも、先がびくびく疼いてるだけで十分よ。"
                f"{name}がゆっくり咥えたら、黙ったまま甘い声が漏れちゃうんでしょ。楽しみね。",
                f"ちゅってするたびに肩が落ちて、それでも口から逃げられない。……ふふ、好きよ。"
                f"沈黙の敗北、いちばんかわいい。涎とキスで頭空っぽにしてあげる。",
            ),
            (
                f"黙ってるくせに腰が前に出てる。……{name}の口、いま来てるわよ。"
                f"熱い奥に沈めて、引き抜いて、亀頭だけちゅって。……答えは先が言ってる。",
                "言わなくていいわ。代わりにびくびく震えて見せなさい。"
                "フェラと亀頭キスで、出せるところまでゆっくり攻めるから。",
            ),
        ],
        "nipple": [
            (
                f"乳首もだめ、って。……隠れてないわよ。もう先端が立って、触れたら折れる顔してる。"
                f"{name}が咥えながら乳輪を摘まんで、乳首にちゅってする。……上下同時ね。",
                "口で先をふさいだまま、乳首を転がすわ。落差でビクッてするたび、"
                "下も反応してるでしょ。どっちが先にイきたがるか、見せなさい❤️",
            ),
            (
                f"乳首弱いの、バレバレ。……{name}が吸って、摘まんで、息を吹きかけて、またちゅっ。"
                f"そのあいだ先端は熱い口の中。……逃げ場、ないわよ。",
                "対話のたびに乳首も攻めるの。赤い先端と硬い先、両方びくびくさせて、"
                "声だけ拒否する甘マゾに仕上げてあげる。",
            ),
        ],
        "beg": [
            (
                f"イかせて、って。……いい子。でもまだ許可は段階よ。"
                f"{name}が深く咥えて限界まで連れてって、イく直前で止めて、また先端にちゅって。",
                f"ふちで焦らして、涎でぐちゃぐちゃにして……出したいなら、もっと情けなく乞いなさい。"
                f"口でイきたいなら、ちゃんと声に出しなさい。",
            ),
            (
                f"お願い、って震えてる。……かわいい。奥まで沈めて、喉で締めながら動くわ。"
                f"でも射精はまだ。ふちの手前で止めて、乳首だけいじめてあげる。",
                "懇願対話、好きよ。もう一段とろけてから、出していいか聞くの。"
                f"{name}の口に負けたいなら、もっと欲しがって見せなさい。",
            ),
        ],
        "edge": [
            (
                f"ふちが……もうだめ、ね。なら、キスしながら限界の手前で止めちゃう。"
                f"びくびくしてる先に、ちゅっ……咥えかけて、また離す。出させない対話よ。",
                f"{name}がふちを積み上げて、声だけ泣かせてあげる。"
                "先走りが止まらないのに許可がないの、いちばんエロいわ。……まだだめ。",
            ),
            (
                f"限界のふちで対話してるの、最高ね。……まだ出さない。口は離さないけど。"
                f"ぬるぬるの先端を舌で転がして、吸って、寸前で止める。腰、砕けそうでしょ。",
                "許可はまだよ。ふちでもう一往復、対話して。"
                "イきたがる体と、拒否する声……両方味わってあげる。",
            ),
        ],
        "nipple_mouth": [
            (
                f"上下同時はずるい、って。……知っててやるの。"
                f"咥えながら乳首ちゅって、浅いフェラのあいだに乳輪を捻る。……頭真っ白でしょ。",
                f"{name}の勝ち方、対話で確定ね。"
                "抵抗する声と、イきたがる先と乳首——どれが本音か、もう分かってるわ。",
            ),
            (
                f"ずるい、って言いながら沈んでる。……口も乳首も折れてるわよ。"
                f"奥で締めながら乳首を摘まむと、先が跳ねて甘い声が漏れる。……好きよその矛盾。",
                "同時責め対話。上下完落ちまで付き合うわ。"
                f"だめって言いながら、{name}の口と指に全部預けなさい。",
            ),
        ],
        "beg_permit": [
            (
                f"出していい……？　ふふ、やっと乞えたわね。"
                f"涎まみれの先で、{name}の口に出したいって……言えたの、えらい。",
                f"まだだめ、か口だけ、か出していい——段階で答えるわ。"
                f"対話の仕上げよ。許可が出るまで、亀頭にちゅってしながら待たせてあげる。",
            ),
            (
                f"お願い……出したいのね。声が正直でかわいい。"
                f"熱い奥で受け止めたいなら、もう少しだけふちで溶かしてから決めるわ。",
                "乞う対話まで来たなら、もう敗北の入口よ。覚悟しなさい。"
                f"{name}が咥えたまま、出していいって囁くまで、腰を離さないわ。",
            ),
        ],
        "melt": [
            (
                f"もう負けた、出る……って。……いいわ。"
                f"{name}が深く咥えて、先端を舌で押さえて、全部受け止めてあげる。",
                "対話の果てに敗北射精ね。情けない顔で、口の中にぶちまけなさい❤️"
                "出したあともキスで余韻まで搾ってあげるわ。",
            ),
            (
                f"負けを認めたのね。ふふ、えらい。……じゃあイかせてあげる。出していいわ。"
                f"奥まで沈めたまま、乳首も摘まんで……甘マゾの対話、完走よ。",
                f"{name}に屈した記録、つけなさい。"
                "射精の瞬間も、ちゅってされながら頭空っぽにしなさい。",
            ),
        ],
        "resist_weak": [
            (
                f"やめて、でも腰が止まらない……最高の矛盾ね。"
                f"だめって言いながら、{name}の口に勝手に沈んでく。……イく直前まで連れてくわ。",
                f"声は抵抗、体は敗北。先が跳ねて、乳首も立って、全部バラしてる。"
                "対話、まだ続くわよ。許可乞いまで堕とし切ってあげる。",
            ),
            (
                f"弱い抵抗……好きよ。先が跳ねてるのに、まだ拒むの？　かわいい。"
                f"くちゅって音がするたび腰が砕けて、それでも「やめて」って……ふふ。",
                "もう出るんでしょ。許可を乞う対話に切り替えなさい。"
                f"{name}の唇が離れる前に、本音だけ言いなさい。",
            ),
        ],
        "nipple_finish": [
            (
                f"乳首も口も同時に……仕上げね。"
                f"咥えて、摘まんで、ちゅってして、奥で締めながら乳首を転がす。……イかせるわ。",
                f"上下完落ちの対話。{name}の前じゃ逃げ場ないわよ。"
                "先も乳首も同期して折れる瞬間、ちゃんと見せなさい❤️",
            ),
            (
                f"同時にイかせて、って。……贅沢ね。いいわ、両方で落とす。"
                f"{name}の口が先を溶かして、指が乳首を潰す。……頭、真っ白ね。",
                "敗北射精の許可、もうすぐよ。上下でとろけたまま、乞いなさい。",
            ),
        ],
        "thanks": [
            (
                f"イかされちゃった、ね。……ふふ、余韻まで甘やかしてあげる。"
                f"出したあとの敏感な先に、そっとちゅって。……まだビクッてするでしょ。",
                f"敗北射精のあとも、{name}のキスと涎が残ってるわ。"
                "また対話しに来なさい。次も口で、情けなく受け止めてあげる。",
            ),
        ],
    }

    pair = rng.choice(pools.get(user_key) or pools["resist"])
    main, after = pair

    # 感触の追い足し（めちゃエロ）
    tail = _sensual_tail(name, turn_n, rng, has_nipple=has_nipple)
    if rng.random() < 0.85:
        after = f"{after}{tail}"

    if has_nipple and user_key in ("want", "resist", "silent", "beg", "edge") and rng.random() < 0.55:
        after = (
            f"{after}"
            f"乳首も弱いの、覚えてるわよ。……摘まみながら、{name}の口で対話してあげる。"
        )

    if loss_n >= 3 and rng.random() < 0.5:
        after = (
            f"{after}"
            f"……{loss_n}回も負けてる相手に、また涎まみれで堕ちる対話ね。学習してるくせに、かわいい。"
        )

    if turn_n >= 4 and rng.random() < 0.4:
        main = (
            f"{main}"
            f"……んっ、くちゅっ。音だけで腰が折れる甘マゾ、対話のたびに美味しくなってるわ。"
        )

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

    if turn_n >= 5 and new_gauge == "touch":
        new_gauge = "near"
    if turn_n >= 7 and new_gauge != "cum":
        new_gauge = "cum"
        permit_hint = permit_hint or "ask"

    return main, after, new_gauge, permit_hint


def render_dialogue_html(dialogue, name="", max_show=28):
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
    <div style="color:{color};font-style:italic;font-size:0.92em;line-height:1.55;">「{text}」</div>
  </div>"""
        )
    n = dialogue_turn_count(dialogue)
    return f"""
<div style="max-width:520px;margin:0.6em auto 0.4em;
  background:linear-gradient(160deg,rgba(194,24,91,0.18),rgba(40,0,25,0.55));
  border:1px solid #ff4081;border-radius:14px;padding:0.85em 1em;
  box-shadow:0 0 18px rgba(255,64,129,0.22);">
  <div style="color:#ff80ab;font-size:0.75em;letter-spacing:0.1em;margin-bottom:0.45em;text-align:center;">
    💬 敗北対話 · {n}往復 · とろける口責め
  </div>
  <div style="max-height:480px;overflow-y:auto;padding-right:0.2em;">
    {''.join(bubbles)}
  </div>
</div>
"""
