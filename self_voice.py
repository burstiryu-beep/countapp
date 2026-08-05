"""自分の声（声だけ抵抗・体は正直）— 鏡チェック用。"""
from __future__ import annotations

import hashlib
import random


def _rng(seed_key: str) -> random.Random:
    return random.Random(int(hashlib.md5(seed_key.encode("utf-8")).hexdigest(), 16))


def self_resist_line(choice, name, gauge=None, heat="thick", edge_n=0):
    """声だけ抵抗するも体は正直 — ユーザー側の情けない独り言。

    彼女のセリフのあいだに差し込むと、抵抗する声と正直な体のズレで抜ける。
    choice / gauge / heat でシード固定し、同じ操作では同じ独り言になる。
    """
    choice = str(choice or "")
    gauge = gauge or ""
    heat = heat or "thick"
    edge_n = int(edge_n or 0)

    resists = [
        "……やめて。ちがう。そんなの……",
        "だめ……声だけは、負けたくない……",
        "ちがう……イきたくない、って言ってるのに……",
        "……お願い、少しだけ待って。心の準備が……",
        "やめ……そこは……だめだって……",
        "ちがう、そんな声出してない……出てない……",
        "……本気で抵抗してるのに。言葉だけでも……",
        "いや……そんなこと言わせないで……",
    ]
    bodies = [
        f"でも腰が勝手に前に出て、{name}の口に届いちゃう……",
        "でも先がびくびくして、もう我慢できてない……",
        "でも乳首が立ってて、触られた瞬間に折れる……",
        "でも息が荒くて、声が情けなく漏れてる……",
        f"でも体はもう{name}に預けてる。……正直すぎる……",
        "でも先走りが止まらなくて、感じてるのバレてる……",
        "でも腰が引けない。……近づいちゃう……",
        "でも頭が真っ白で、だめって言いながら腰が動いてる……",
    ]

    by_choice = {
        "kiss": [
            f"……キスだけなら……って思ったのに。亀頭にちゅってされた瞬間、声が裏返る。でも体はもっと欲しがってる……{name}、ひどい……",
            "ちゅって……やめて。……でも唇が離れるたびに、先がついていっちゃう……",
        ],
        "glans": [
            "亀頭だけ……だめ。……でもキスされるたび腰が浮いて、正直すぎる……",
            "そこ……弱いって言わない。……言わないのに、びくびくしてる……",
        ],
        "mouth": [
            f"咥えないで……って言ってるのに。口の中が熱くて、だめって言いながら奥まで沈んでる。……{name}の勝ちだ……",
            "口で……だめ。……でも舌の感触に負けて、声が甘い……体が先に折れてる……",
        ],
        "want": [
            "フェラしてほしい、なんて……言いたくない。……でも喉が鳴って、欲しがってる……",
            "お願い、なんて……恥ずかしい。……でも腰がもう答えを出してる……",
        ],
        "hard": [
            "硬いなんて……言いたくない。……でも先が立ってて、もう隠せない……",
            "……触らないで、って言いたい。でも指が近づいただけで跳ねてる……",
        ],
        "silent": [
            "……何も言えない。声は出せない。……でも先が正直で、びくびくしてる……",
            "黙ってるのに……体が全部バラしてる。恥ずかしい……",
        ],
        "edge": [
            "イかせないで……ふちで……だめ。……でも限界の手前で腰が震えて、もっと欲しがってる……",
            f"まだ出さないで……って頼む声と、出したい体が喧嘩してる。……{name}、いじわる……",
        ],
        "denied": [
            "許可が欲しい……って言いたくない。……でも出したいって体が泣いてる……",
            "だめって言われてるのに……先が疼いて、声だけ抵抗してる……情けない……",
        ],
        "mouth_ok": [
            "口だけ……まだ出さない、って。……でも奥で締められて、出しそうで怖い……",
            "出すのはだめ……声ではそう言う。……腰はもうイく準備してる……",
        ],
        "granted": [
            "イっていい、なんて……恥ずかしい。……でも許可された瞬間、体が崩れる……",
            f"出していい……？　声が震えてる。……もう{name}の口に全部預けてる……",
        ],
        "nipple": [
            "乳首は……関係ない、って。……でも摘まれただけで声が漏れて、口より先に折れる……",
            "そこ触らないで……だめ。……でも乳輪が熱くて、指を欲しがってる……",
        ],
        "nipple_lick": [
            "舐めないで……ちゅって……だめ。……でも乳首が吸われて、腰が抜けてる……",
            "声出さない……って決めたのに。乳首にちゅってされて、甘い声だけ漏れる……体は正直……",
        ],
        "nipple_mouth": [
            f"上下同時は……ずるい。……やめて、って言いながら、口にも乳首にも沈んでる。……{name}、ずるい……",
            "どっちもだめ……って。……でも先も乳首も同時に折れて、抵抗する声だけが残ってる……",
        ],
        "finish": [
            "仕上げないで……まだ……だめ。……でも喉奥で締められて、出るの止められない……",
            f"イきたくない、って嘘。……もう{name}の口で出すしかない。……声だけが抵抗してる……",
        ],
        "deep": [
            "深く……だめ。……喉が……って言いながら、奥まで沈めてる。……体が正直すぎる……",
            "苦しい……やめて。……でも腰が離せずに、咥えられたまま震えてる……",
        ],
        "shallow": [
            "浅く……だけなら……って思ったのに。浅いのに溶けて、もっと欲しがってる……",
            "入口だけ……だめ。……でも舌に負けて、浅いくせに腰が前に出てる……",
        ],
        "lick": [
            "舐めないで……先端……だめ。……でもねっとりした舌に、先がついていっちゃう……",
            "そこ……弱いって言わない。……言わないのに、舐められて声が甘い……",
        ],
        "kiss_only": [
            "キスだけ……なら大丈夫、って。……でもちゅってされるたび、先が疼いてる……",
            "キスだけって……嘘だ。……体はもう咥えてほしがってる……",
        ],
        "open": [
            f"……来ないで、って言いたい。でも{name}の顔を見ただけで、先が熱くなって声が弱い……",
            "鏡なんて……見たくない。……でも体が正直で、口と乳首の想像だけで腰が疼いてる……",
            f"やめて……そんな目で見ないで。……でももう{name}に負けてるの、バレてる……",
        ],
    }

    key = choice
    if choice.startswith("edge_loop"):
        key = "edge"
    elif choice.startswith("dual_mouth"):
        key = "mouth"
    elif choice.startswith("dual_nipple"):
        key = "nipple"
    elif choice.startswith("dual_both") or choice.startswith("dual_"):
        key = "nipple_mouth"
    elif choice.startswith("gauge_"):
        key = choice
    elif choice in ("start", "touch"):
        key = "hard"
    elif choice in ("near",):
        key = "edge"

    gauge_lines = {
        "touch": [
            "触りながら……口を想像するだけ、って。……でも想像しただけで先が硬くなってる……",
            f"まだ触ってないのに……{name}の口が頭にあって、体が先に反応してる……",
        ],
        "near": [
            "限界……まだ大丈夫、って嘘。……ふちで声だけ抵抗して、腰はもうイきたがってる……",
            f"まだ出さない……って言いながら、{name}の口を想像しただけで震えが止まない……",
        ],
        "cum": [
            "もう出る……って言いたくない。……でも先が跳ねて、許可なしでも崩れそう……",
            f"イく……いや、まだ……声が矛盾してる。体はもう{name}に負けてる……",
        ],
    }

    heat_extra = {
        "soft": [
            "……優しくしないで。優しいと、だめって言えない……体がとろける……",
        ],
        "thick": [
            "ぬるぬるして……いや。……でもその感触に負けて、声が甘くなってる……",
        ],
        "filthy": [
            "そんな卑猥な音……聞きたくない。……でもくちゅってされるたび、腰が折れる……どろどろに……",
        ],
    }

    rng = _rng(f"self|{key}|{gauge}|{heat}|{name}|{edge_n}|{choice}")

    special = []
    if key.startswith("gauge_"):
        g = key.replace("gauge_", "") or gauge
        special = gauge_lines.get(g, [])
    elif key in by_choice:
        special = by_choice[key]
    elif gauge in gauge_lines:
        special = gauge_lines[gauge]

    if edge_n >= 3 and (
        key in ("edge", "denied", "mouth_ok") or str(choice).startswith("edge_loop")
    ):
        special = list(special) + [
            f"ふちを{edge_n}回も……やめて。……でも出させてもらえなくて、声だけ泣きそうで、体はもっと疼いてる……",
            "まだ出させない……って。……抵抗する声が弱くなって、体だけが正直にイきたがってる……",
        ]

    if special and rng.random() < 0.72:
        line = rng.choice(special)
    else:
        line = f"{rng.choice(resists)}{rng.choice(bodies)}"

    if heat in heat_extra and rng.random() < 0.35:
        line = f"{line}{rng.choice(heat_extra[heat])}"

    return line


def render_self_voice_html(line, label="あなた（声だけ）"):
    """鏡カード用：自分の声バブル。"""
    if not line:
        return ""
    return f"""
  <div style="margin:0.45em 0 0.35em;padding:0.55em 0.7em;border-radius:10px;
    background:rgba(0,0,0,0.28);border:1px dashed rgba(255,182,217,0.45);text-align:left;">
    <div style="color:#ff80ab;font-size:0.72em;letter-spacing:0.08em;margin-bottom:0.25em;">🎙 {label}</div>
    <div style="color:#ffe0f0;font-style:italic;font-size:0.95em;line-height:1.5;">
      「{line}」
    </div>
  </div>
"""
