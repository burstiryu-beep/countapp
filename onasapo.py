"""オナサポモード：ちんぽに効く甘マゾ敗北誘導。"""
from __future__ import annotations

import hashlib
import random

from ero_flavor import apply_heat
from onasapo_denial import denial_roast_lines, denial_self_line, denial_after


ONASAPO_STYLES = [
    ("mouth", "口でちんぽ💋"),
    ("nipple", "乳首×ちんぽ💗"),
    ("dual", "上下同時で落とす🔥"),
    ("auto", "おまかせ敗北💞"),
]

ONASAPO_PACES = [
    ("slow", "ゆっくりとろけ"),
    ("normal", "ふつうに堕とす"),
    ("fast", "急かしてイかせる"),
]

ONASAPO_PHASES = [
    ("ready", "準備"),
    ("warmup", "前戯"),
    ("build", "本番"),
    ("edge", "ふち"),
    ("finish", "仕上げ"),
    ("after", "余韻"),
]


def _rng(seed_key: str) -> random.Random:
    return random.Random(int(hashlib.md5(seed_key.encode("utf-8")).hexdigest(), 16))


def _voice_prefix(voice, name):
    return {
        "sweet": f"（甘い声で）……ねえ、{name}の口でちんぽ、溶かそうね。",
        "sticky": f"（ねっとりと）……ふふ、先から離さないわよ、{name}。",
        "urgent": f"（急かすように）ほら、しごいて。{name}、待たないわ。イかせる番よ。",
        "tease": f"（からかうように）ふふ……ちんぽ、もう正直すぎる顔してるわね。",
        "dote": f"（溺愛混じりに）……いい子ね、{name}がちんぽごと可愛がってあげる。",
        "command": f"（命令口調で）手を動かしなさい。ちんぽは{name}のペースに従うの。",
    }.get(voice or "sweet", "")


def dress_onasapo(text, name, voice="sweet", heat="filthy"):
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


def onasapo_line(phase, name, style="mouth", pace="normal", edge_n=0, tags=None, react=None):
    """段階ごとのちんぽ誘導セリフ。react で反応に寄せる。"""
    style = resolve_style(style, tags)
    tags = tags or []
    pace = pace or "normal"
    react = react or ""

    if phase == "ready":
        pool = {
            "mouth": [
                f"オナサポ、はじめるわよ。……パンツ下ろして、ちんぽ出して。"
                f"{name}の顔を見ながら、今日は口でイかせるつもり。先端、もう熱い？",
                f"準備できてる？　ちんぽを軽く握って。……{name}が膝をついて唇を寄せる想像して。"
                f"亀頭にちゅってされる前の緊張、味わいなさい。",
                f"ちんぽ、見せなさい。……{name}が涎たらしながら咥える相手よ。"
                f"手はまだ軽くでいい。でも先は、もう負け顔してるわね。",
            ],
            "nipple": [
                f"今日のオナサポは乳首からちんぽへ。……{name}が胸に触れる想像して、"
                f"先もゆっくり起こしなさい。上下、両方起こすの。",
                f"乳首、もう敏感でしょ。摘まみながらちんぽも軽く。……{name}と一緒に、"
                f"上下とろけさせてあげるわ。どっちが先に硬くなるか、見せなさい。",
            ],
            "dual": [
                f"同時責めオナサポよ。……口と乳首、どっちも捨てない。"
                f"ちんぽ出して、乳首も出せる体勢に。……{name}に上下支配されなさい。",
                f"準備は先端と乳首。……両方触れるつもりで腰の力、抜いて。"
                f"{name}、来るわよ。ちんぽ、今日は逃がさない。",
            ],
        }
    elif phase == "warmup":
        pool = {
            "mouth": [
                f"ちんぽ、軽く上下して。……でも本命は{name}のキスよ。"
                f"亀頭だけ指で円を描いて、ちゅっちゅ音、頭の中で鳴らしなさい。感度、上げて。",
                f"ぬるっと温めて。ローションでも唾液想像でもいいわ。……{name}の浅い咥えを手で再現。"
                f"先端だけ包んで、ゆっくり。奥はまだ。焦らして、ちんぽを正直にさせなさい。",
                f"裏筋を親指で。……そこ、弱いでしょう。{name}が舌でねっとり舐めるところ。"
                f"先走りが出てきたら、キスされてるつもりで塗り広げなさい。エロいわよ、その先。",
                f"亀頭の傘の下、ゆっくりこすって。……ちゅってされる直前の疼き、手で作るの。"
                f"{name}、上手に起こしてるわね。ちんぽ、もう挨拶してきた？",
            ],
            "nipple": [
                f"片手で乳首、そっと転がして。……もう片方はちんぽを軽く。"
                f"{name}の指、想像して重ねて。乳首が立つと先も跳ねるでしょ。同期してるわ。",
                f"乳首つねる前に、撫でて硬くして。……同時にちんぽの先だけ撫でる。"
                f"{name}が舐める前の段階よ。上下、両方起こしなさい。",
            ],
            "dual": [
                f"右で乳首、左でちんぽ。……リズム揃えなくていいわ。"
                f"{name}が両方いじる感触、分けて味わいなさい。先が先に反応したら負けよ。",
                f"先端ちゅっの想像＋乳首摘まみ。……前戯なのに、ちんぽもうびくびくしてるでしょ。"
                f"ふふ、正直。このまま本番で落とすわ。",
            ],
        }
    elif phase == "build":
        pool = {
            "mouth": [
                f"ペース上げていいわ。握って上下、親指で裏筋。……咥えられてるつもりで腰、くねらせなさい。"
                f"{name}、離さないわ。くちゅって音、頭で鳴らしながらしごきなさい。",
                f"奥まで入る想像で深くしごく。……引き抜くときは亀頭キス。"
                f"{name}のフェラ、手で真似して。ちんぽが欲しがるリズム、見つけて。",
                f"時々止めて、先端だけ集中。……{name}が浅く咥えて吸うところ。"
                f"吸い上げられる感触で腰が浮いたら、また深く。ちんぽ、もうメロメロね。",
                f"先走りでぬるぬるになったら最高。……それを潤滑にして、"
                f"{name}の涎まみれフェラだと思って速くしごきなさい。情けない音、出していいわ。",
                f"亀頭を掌でくるくる、次に全体をふかふか。……浅い→深い→キスのループよ。"
                f"ちんぽが跳ねたら、そこが弱点。{name}、そこを執拗に責めるわ。",
            ],
            "nipple": [
                f"乳首、少し強く。……痛気持ちいいところで止めて、また転がす。"
                f"同時にちんぽを速く。上下の落差で頭持ってかれるでしょ。{name}、執拗よ。",
                f"乳首舐めのつもりで息を吹きかけて。……ちんぽは止めない。"
                f"乳首が折れるたびに先が跳ねるの、見てるわ。同期敗北ね。",
            ],
            "dual": [
                f"咥えながら乳首摘まむ同時責め……手で再現しなさい。"
                f"ちんぽを包んで、乳首をつねる。{name}式よ。どっちで先に折れるか競争。",
                f"浅いフェラのリズムでしごきつつ、乳首を交互に。……"
                f"ちんぽも乳首もびくびくしてたら、もう本番クリア近いわよ。",
                f"上下同時に速くして、急に止めて先端だけ。……"
                f"{name}がくちゅって吸って乳首ちゅってする想像で、ちんぽを壊しなさい。",
            ],
        }
    elif phase == "edge":
        n = max(1, min(int(edge_n or 1), 5))
        pool = {
            "mouth": [
                f"ふち……{n}回目。イキそうなら速度落として、亀頭だけちゅってされる想像で止めるの。"
                f"ちんぽ、出すな。出たそうな先端を指でふさいで、キスの余韻だけ味わいなさい。",
                f"出ちゃいそう？　だめ。……{name}は浅く咥えて離す。そのふち、手で再現しなさい。"
                f"びくびくしてるちんぽ、かわいい。まだよ。先走りだけ垂れさせて。",
                f"限界の手前で止めて、亀頭をねっとり円。……{n}回目のふちよ。"
                f"{name}の口なら、ここでイかせずに焦らすわ。手も同じ。ちんぽ、泣いてる？",
                f"腰、止めて。手は先端だけ。……ちゅっ、ちゅっ、って頭で鳴らしながら、"
                f"射精を飲み込ませる寸前まで連れてって、また離す。ふち×{n}、積み上げなさい。",
            ],
            "nipple": [
                f"ふちで乳首強く。……ちんぽは止めて、乳首だけでイキそうを引き延ばすわ。{n}回目よ。"
                f"先が跳ねてもしごかない。乳首で落とす寸前まで。……{name}、許さないわ。",
                f"限界なのに乳首いじり続けるの、最悪でしょ。……ちんぽは熱いまま放置。"
                f"上下の矛盾で頭真っ白。……まだ出さない。{n}回目。",
            ],
            "dual": [
                f"ふち×{n}。口の想像でしごきを止めて、乳首だけ動かす。……"
                f"ちんぽどっちで落とすか、まだ決めてないわ。先走りは垂れさせていいのよ。",
                f"イキそうな先端を指でふさいで、乳首にちゅっ。……同時ふち、{name}の得意技ね。"
                f"ちんぽも乳首も限界。……でも射精はまだ。対話みたいに積み上げなさい。",
            ],
        }
    elif phase == "finish":
        pool = {
            "mouth": [
                f"いいわ、出して。……{name}が奥まで咥えて受け止める想像で、最後までしごき切るの。"
                f"ちんぽ、口の中にぶちまけなさい。敗北射精よ。",
                f"射精の許可、出すわ。先端にちゅってされながら出す顔、見せなさい。"
                f"……口に負けて。腰止めても手は止めない。情けなくイきなさい。",
                f"速く、深く、止めない。……{name}のフェラで押し切られるつもりで、"
                f"ちんぽから全部出しなさい。余韻まで吸われる想像で、最後の一滴まで。",
                f"亀頭を掌で締めながら上下。……キスされながら出す感触よ。"
                f"出る瞬間「{name}」って言いなさい。ちんぽの敗北宣言ね❤️",
            ],
            "nipple": [
                f"乳首摘まんだまま出して。……ちんぽだけ速く、乳首は離さない。{name}式トドメよ。"
                f"イく瞬間に乳首つねるの。……声、出していいわ。上下で堕ちなさい。",
            ],
            "dual": [
                f"同時仕上げ。……咥えられながら乳首を強く。手で両方再現して、そのまま出しなさい。"
                f"ちんぽも乳首も最大。……{name}に上下からイかせてもらうの。逃げないで。",
                f"奥フェラ＋乳首捻り、手で同時に。……頭真っ白で出して。"
                f"敗北射精、上下完落ちよ。ちんぽ、全部吐き出しなさい。",
            ],
        }
    else:  # after
        pool = {
            "mouth": [
                f"出したあとも口、離さないつもりよ。……余韻のちんぽに{name}がちゅってする。"
                f"感度、最悪でしょ。びくびくしてる先、軽く撫でて。えらい子。",
                f"白くなった先端を、キスで綺麗にする想像。……まだ出そう？　ふふ、欲張りね。"
                f"でも今日の敗北は記録しなさい。{name}の口勝ちよ。",
            ],
            "nipple": [
                f"射精したのに乳首、まだ摘まんでるわよ。……余韻の弱さ、{name}が好きなの。"
                f"ちんぽはもう空っぽなのに、乳首でまた起こされそう。……だめ、敏感すぎ。",
            ],
            "dual": [
                f"余韻でも同時。……浅く包んで、乳首軽く。{name}は離さないわ。敗北の続きよ。"
                f"白くなった先と赤い乳首。……両方甘やかされてるの、認めて。幸せそうな負け顔ね。",
            ],
        }

    lines = pool.get(style) or pool.get("mouth")
    # react 寄せ
    if react == "hard":
        lines = lines + [
            f"硬いのね。……じゃあその正直なちんぽを、{name}の口だと思って丁寧にいじめなさい。"
            f"先端から丁寧に。跳ねるたびにキス想像よ。",
        ]
    elif react == "near":
        lines = lines + [
            f"イキそう？　いいわ、その震え。……でもまだ出さないなら速度落として、"
            f"亀頭だけちゅってされる想像でふちを作れ。ちんぽ、泣かせなさい。",
        ]
    elif react == "resist":
        lines = lines + [
            f"やめて、って。……かわいい。でも手は止めないで。"
            f"声だけ抵抗して、ちんぽは{name}に預けてるの。その矛盾がエロいわ。",
        ]
    elif react == "cum":
        lines = lines + [
            f"出したいのね。……じゃあ仕上げのつもりで速くしごきなさい。"
            f"{name}が奥で受け止める。ちんぽ、許可待ちでも体はもう敗北よ。",
        ]
    elif react in ("deny", "noerect", "endure"):
        # 我慢宣言は追い打ちプール優先
        lines = denial_roast_lines(name, phase, style)

    text = random.choice(lines)

    if pace == "slow" and phase in ("warmup", "build"):
        text += "……急がないで。一往復ごとに息、吐きなさい。ちんぽの熱、味わうの。"
    elif pace == "fast" and phase in ("build", "edge", "finish"):
        text += "……もっと速く。考える暇なくちんぽをとろけなさい。頭、空けて。"

    if tags and phase in ("build", "edge", "finish"):
        tag = random.choice(tags)
        text += f" ……弱点「{tag}」、今日はそこ狙いよ。ちんぽ、覚えなさい。"

    return text


def onasapo_after(phase, name, style="mouth", edge_n=0):
    style = style if style != "auto" else "mouth"
    if phase == "ready":
        return (
            f"ちんぽ出したら「次へ」。{name}が唇を寄せるまで、先を軽く起こして待ってなさい。"
        )
    if phase == "warmup":
        return "温まってきたら本番へ。……先が熱くて先走り出てきた？　正直に進みなさい。"
    if phase == "build":
        return (
            f"気持ちよくなってきたらふちへ。……イキそうになったら教えて。"
            f"ちんぽが跳ねたら、{name}の勝ち近いわよ。"
        )
    if phase == "edge":
        n = int(edge_n or 1)
        if n < 3:
            return f"ふち×{n}。……まだ出さない。ちんぽ、もう一度ふちいけるわよ。泣いてもだめ。"
        if n < 5:
            return (
                f"ふち×{n}、溜まってるわね。……先走りだらしない。"
                f"仕上げていいかしら？　欲しければ進みなさい。{name}、待ってる。"
            )
        return (
            f"ふち×{n}……もう限界でしょ。ちんぽ、真っ赤でびくびくしてる。"
            f"仕上げへ行きなさい。口でイかせてあげる。"
        )
    if phase == "finish":
        return (
            f"出せたら余韻へ。……出したら記録もつけてね。"
            f"{name}にちんぽ負けした証拠よ❤️"
        )
    return (
        "余韻まで味わえたらえらい。……もう一回ちんぽ溶かされる？"
        "それとも今日は敗北記録で終わり？"
    )


def onasapo_self_line(phase, name, edge_n=0, react=None):
    """声だけ抵抗・ちんぽは正直。"""
    edge_n = int(edge_n or 0)
    react = react or ""
    if react in ("deny", "noerect", "endure"):
        return denial_self_line(name, edge_n or 1)
    rng = _rng(f"sapo_self|{phase}|{name}|{edge_n}|{react}")
    pools = {
        "ready": [
            f"……やめて、見ないで。……でもちんぽ、もう{name}の口を想像して硬くなってる……",
            "出さない、って決めたのに……先が熱い……恥ずかしい……",
        ],
        "warmup": [
            "軽く触るだけ、って……でも裏筋なぞっただけで腰が……んっ……",
            f"ちゅってされる想像だけで先走りが……{name}、ひどい……でも止められない……",
        ],
        "build": [
            f"だめ、速くしないで……って言いながら、しごいてる。……ちんぽが{name}に負けてる……",
            "奥まで入る想像……いや……でも腰がくねって、くちゅって音が頭から離れない……",
            "乳首も……関係ない、って。……でも摘まれたら先が跳ねる……上下……ずるい……",
        ],
        "edge": [
            f"出る……出ちゃう……やめて。……でもふち×{edge_n}でちんぽが泣いてる……出したい……",
            "まだだめ、って……声だけ。……先はびくびくで、キスされたら終わりなのに……",
            f"イかせないで……お願い……でも手、先端から離れない……{name}のせい……",
        ],
        "finish": [
            f"出していい……？　いや、出す……もう負けた……{name}の口に……出る……",
            "やめて……でも止まらない……ちんぽ、全部出ちゃう……敗北射精……んっ……",
        ],
        "after": [
            f"出したあと……まだちゅって……敏感……でも離してほしくない……{name}……",
            "びくびくしてる……恥ずかしい……でも余韻まで甘やかされて、また硬くなりそう……",
        ],
    }
    if react == "resist":
        return rng.choice([
            "やめて……ちがう……でもちんぽが正直で……腰が前に……",
            f"だめだって……声が出るのに、先は{name}を欲しがってる……情けない……",
        ])
    if react == "cum":
        return rng.choice([
            "出る……もう出る……許可とか……間に合わない……口に……",
            f"イく……{name}……ちんぽ、負けた……出して……受けて……",
        ])
    return rng.choice(pools.get(phase) or pools["build"])


def onasapo_react_options(phase, edge_n=0):
    """段階ごとの反応ボタン。"""
    edge_n = int(edge_n or 0)
    deny = ("deny", "我慢する！負けない！")
    noerect = ("noerect", "勃たないぞ！（フル勃起）")
    if phase in ("ready", "warmup"):
        return [
            deny,
            noerect,
            ("hard", "ちんぽ…もう硬い"),
            ("want", "口で溶かして…"),
        ]
    if phase == "build":
        return [
            deny,
            noerect,
            ("near", "イキそう…ふちが…"),
            ("want", "もっと奥…咥えて…"),
        ]
    if phase == "edge":
        if edge_n >= 3:
            return [
                deny,
                ("near", "ふち限界…もうだめ…"),
                ("cum", "もうだめ…イかせて…"),
                noerect,
            ]
        return [
            deny,
            noerect,
            ("near", "限界…出ちゃう…"),
            ("cum", "出したい…口で受けて…"),
        ]
    if phase == "finish":
        return [
            deny,
            ("cum", "出る…敗北する…"),
            ("resist", "やめて…でも出る…"),
        ]
    return [
        deny,
        ("hard", "また硬くなりそう…"),
        ("want", "もう一回…口で…"),
    ]


def tension_pct(phase, edge_n=0, denial_n=0):
    """ちんぽ張力ゲージ（表示用）。我慢宣言するほど逆に上がる。"""
    edge_n = int(edge_n or 0)
    denial_n = int(denial_n or 0)
    base = {
        "ready": 12,
        "warmup": 28,
        "build": 55,
        "edge": 70 + min(edge_n, 5) * 5,
        "finish": 96,
        "after": 40,
    }.get(phase, 20)
    # 我慢するたびにフル勃起補正
    base += min(denial_n, 8) * 4
    return max(5, min(99, base))


def render_tension_html(phase, edge_n=0, denial_n=0):
    pct = tension_pct(phase, edge_n, denial_n)
    if denial_n >= 3:
        label = f"我慢宣言×{denial_n}なのにフル勃起❤️"
    elif pct < 40:
        label = "とろけ始め"
    elif pct < 80:
        label = "ちんぽ限界付近"
    else:
        label = "敗北射精寸前❤️"
    return f"""
<div style="max-width:560px;margin:0.2em auto 0.7em;">
  <div style="display:flex;justify-content:space-between;color:#ff80ab;font-size:0.75em;margin-bottom:0.25em;">
    <span>💦 ちんぽ張力</span><span>{label} · {pct}%</span>
  </div>
  <div style="height:12px;background:rgba(40,0,25,0.6);border-radius:999px;overflow:hidden;
    border:1px solid rgba(255,64,129,0.35);">
    <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#c2185b,#ff4081,#ff80ab);"></div>
  </div>
</div>
"""


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
