"""自分の声（声だけ抵抗・体は正直）— 鏡チェック用・濃い版。"""
from __future__ import annotations

import hashlib
import random


def _rng(seed_key: str) -> random.Random:
    return random.Random(int(hashlib.md5(seed_key.encode("utf-8")).hexdigest(), 16))


def self_resist_line(choice, name, gauge=None, heat="thick", edge_n=0):
    """声だけ抵抗するも体は正直 — ユーザー側の情けない独り言。"""
    choice = str(choice or "")
    gauge = gauge or ""
    heat = heat or "thick"
    edge_n = int(edge_n or 0)

    resists = [
        "……やめて。ちがう。咥えないで……んっ……",
        "だめ……声だけは、負けたくない……ちゅってしないで……",
        "ちがう……イきたくない、って言ってるのに……腰が……",
        "……お願い、少しだけ待って。心の準備が……先が熱くて……",
        "やめ……そこは……亀頭はだめだって……あ……",
        "ちがう、そんな甘い声出してない……出てない……嘘……",
        "……本気で抵抗してるのに。言葉だけでも……体が裏切る……",
        "いや……そんなこと言わせないで……奥まで……だめ……",
    ]
    bodies = [
        f"でも腰が勝手に前に出て、{name}のぬるぬるの口に届いちゃう……",
        "でも先がびくびく跳ねて、先走りが糸を引いてる……もう隠せない……",
        "でも乳首が立ってて、摘まれた瞬間に腰が折れる……上下同時に……",
        "でも息が荒くて、くちゅって音がするたび情けない声が漏れる……",
        f"でも体はもう{name}の唇に預けてる。……涎混じりで正直すぎる……",
        "でも先走りが止まらなくて、キスされるたび感じてるのバレてる……",
        "でも腰が引けない。……熱い奥に、また沈んじゃう……",
        "でも頭が真っ白で、だめって言いながら腰が浅く動いてる……恥ずかしい……",
    ]

    by_choice = {
        "kiss": [
            f"……キスだけなら……って思ったのに。亀頭にちゅってされた瞬間、声が裏返る。"
            f"ぬるぬるの唇が離れるたびに、先がついていっちゃう……{name}、ひどい……でももっと……",
            "ちゅって……やめて。……でも裏筋を舌でなぞられて、腰が浮いて、欲しがってる……体が先に折れてる……",
        ],
        "glans": [
            "亀頭だけ……だめ。……でもキスされるたびビクッてして、先走りが光ってる……正直すぎる……",
            "そこ……弱いって言わない。……言わないのに、ちゅってされるたび甘い声が漏れて、びくびくしてる……",
        ],
        "mouth": [
            f"咥えないで……って言ってるのに。口の中が熱くてぬるぬるで、だめって言いながら奥まで沈んでる。"
            f"……{name}の勝ちだ……喉で締められたら終わり……",
            "口で……だめ。……でもくちゅって音に負けて、声が甘くて……体が先にイきたがってる……",
        ],
        "want": [
            "フェラしてほしい、なんて……言いたくない。……でも喉が鳴って、奥まで欲しがってる……恥ずかしい……",
            f"お願い、なんて……情けない。……でも腰がもう{name}の口に答えを出してる……溶かして、って……",
        ],
        "hard": [
            "硬いなんて……言いたくない。……でも先が立って唾液を想像しただけで跳ねてる……もう隠せない……",
            "……触らないで、って言いたい。でも指が近づいただけでビクッてして、咥えられそうで怖い……でも欲しい……",
        ],
        "silent": [
            "……何も言えない。声は出せない。……でも先が疼いて、びくびくして、全部バラしてる……恥ずかしい……",
            f"黙ってるのに……{name}の口を想像しただけで腰が前に出てる。沈黙の敗北……",
        ],
        "edge": [
            "イかせないで……ふちで……だめ。……でも限界の手前で腰が震えて、ちゅってされるたびもっと欲しがってる……",
            f"まだ出さないで……って頼む声と、出したい体が喧嘩してる。……{name}、いじわる……でも離さないで……",
        ],
        "denied": [
            "許可が欲しい……って言いたくない。……でも出したいって先が泣いてて、口を欲しがってる……情けない……",
            "だめって言われてるのに……先が疼いて、声だけ抵抗して、腰はイく準備してる……甘マゾ……",
        ],
        "mouth_ok": [
            "口だけ……まだ出さない、って。……でも奥で締められて、出す寸前で止められて怖い……でも気持ちいい……",
            "出すのはだめ……声ではそう言う。……腰はもう{name}の口に全部預けてイく準備してる……",
        ],
        "granted": [
            "イっていい、なんて……恥ずかしい。……でも許可された瞬間、奥まで沈んで体が崩れる……出る……",
            f"出していい……？　声が震えてる。……もう{name}の口に全部出す。……敗北射精……",
        ],
        "nipple": [
            "乳首は……関係ない、って。……でも摘まれただけで声が漏れて、口より先に折れる……上下……だめ……",
            "そこ触らないで……だめ。……でも乳輪が熱くて、ちゅって欲しがってる……先も同時に疼いてる……",
        ],
        "nipple_lick": [
            "舐めないで……乳首ちゅって……だめ。……でも吸われて腰が抜けて、先までびくびく同期してる……",
            "声出さない……って決めたのに。乳首にちゅってされて、甘い声だけ漏れる……体は正直……口も欲しい……",
        ],
        "nipple_mouth": [
            f"上下同時は……ずるい。……やめて、って言いながら、口にも乳首にも沈んでる。……{name}、ずるい……でも最高……",
            "どっちもだめ……って。……でも先も乳首も同時に折れて、抵抗する声だけが残ってる……頭真っ白……",
        ],
        "finish": [
            "仕上げないで……まだ……だめ。……でも喉奥で締められて、ちゅってされて、出るの止められない……出る……",
            f"イきたくない、って嘘。……もう{name}の口で出すしかない。……声だけが抵抗してる……敗北……",
        ],
        "deep": [
            "深く……だめ。……喉が……って言いながら、奥まで沈めてる。……ぬるぬるで体が正直すぎる……",
            "苦しい……やめて。……でも腰が離せずに、咥えられたまま震えて、イきたがってる……",
        ],
        "shallow": [
            "浅く……だけなら……って思ったのに。浅いのに溶けて、もっと奥が欲しがってる……腰が前に……",
            "入口だけ……だめ。……でも舌に負けて、浅いくせに先走りが出て、咥えてほしがってる……",
        ],
        "lick": [
            "舐めないで……先端……だめ。……でもねっとりした舌に、先がついていっちゃう……ちゅって……あ……",
            "そこ……弱いって言わない。……言わないのに、舐められて声が甘くて、腰が砕けてる……",
        ],
        "kiss_only": [
            "キスだけ……なら大丈夫、って。……でもちゅってされるたび先が疼いて、咥えてほしがってる……嘘だ……",
            f"キスだけって……嘘だ。……体はもう{name}の奥まで欲しがってる……フェラして、って……",
        ],
        "open": [
            f"……来ないで、って言いたい。でも{name}の顔を見ただけで、先が熱くなって声が弱い……口が欲しい……",
            "鏡なんて……見たくない。……でも体が正直で、口と乳首の想像だけで腰が疼いて先走りが出そう……",
            f"やめて……そんな目で見ないで。……でももう{name}に負けてるの、先がバレてる……咥えて……",
        ],
    }

    # dlg_* keys from dialogue
    key = choice
    if "_t" in choice:
        key = choice.split("_t")[0]
    if key.startswith("dlg_"):
        key = key[4:]
    if key.startswith("edge_loop"):
        key = "edge"
    elif key.startswith("dual_mouth"):
        key = "mouth"
    elif key.startswith("dual_nipple"):
        key = "nipple"
    elif key.startswith("dual_both") or key.startswith("dual_"):
        key = "nipple_mouth"
    elif key.startswith("gauge_"):
        key = choice if choice.startswith("gauge_") else key
    elif key in ("start", "touch"):
        key = "hard"
    elif key in ("near",):
        key = "edge"
    elif key in ("resist", "resist_weak"):
        key = "edge" if "weak" in key else "denied"
    elif key == "beg":
        key = "want"
    elif key == "beg_permit":
        key = "granted"
    elif key == "melt":
        key = "finish"
    elif key == "nipple_finish":
        key = "nipple_mouth"
    elif key == "thanks":
        key = "granted"

    gauge_lines = {
        "touch": [
            "触りながら……口を想像するだけ、って。……でも想像しただけで先が硬くて熱くて……ちゅってされそう……",
            f"まだ触ってないのに……{name}のぬるぬるの口が頭にあって、体が先に反応してる……",
        ],
        "near": [
            "限界……まだ大丈夫、って嘘。……ふちで声だけ抵抗して、腰はもう口の中でイきたがってる……",
            f"まだ出さない……って言いながら、{name}のキスを想像しただけで震えが止まない……先走りが……",
        ],
        "cum": [
            "もう出る……って言いたくない。……でも先が跳ねて、許可なしでも口に崩しそう……出る……",
            f"イく……いや、まだ……声が矛盾してる。体はもう{name}の奥に負けてる……敗北射精……",
        ],
    }

    heat_extra = {
        "soft": [
            "……優しくしないで。優しいキスだと、だめって言えない……体がとろける……んっ……",
        ],
        "thick": [
            "ぬるぬるして……いや。……でもその感触に負けて、くちゅって音で声が甘くなってる……もっと……",
            f"涎と先走りが混ざって……汚い。……でも{name}の口、熱くて離したくない……体が正直……",
        ],
        "filthy": [
            "そんな卑猥な音……聞きたくない。……でもくちゅ、ちゅっ、んっ、ってされるたび腰が折れる……どろどろに……出る……",
            "ぐちゃぐちゃの先端……見せたくない。……でも吸われて、乳首も赤くて……情けない顔でイきそう……",
        ],
    }

    rng = _rng(f"self|{key}|{gauge}|{heat}|{name}|{edge_n}|{choice}")

    special = []
    if str(key).startswith("gauge_"):
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
            f"ふちを{edge_n}回も……やめて。……でも出させてもらえなくて、声だけ泣きそうで、"
            f"先は{name}の唇にすりすりして欲しがってる……情けない……",
            "まだ出させない……って。……抵抗する声が弱くなって、体だけが正直に口の中でイきたがってる……出したい……",
        ]

    if special and rng.random() < 0.78:
        line = rng.choice(special)
    else:
        line = f"{rng.choice(resists)}{rng.choice(bodies)}"

    if heat in heat_extra and rng.random() < 0.55:
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
    <div style="color:#ffe0f0;font-style:italic;font-size:0.95em;line-height:1.55;">
      「{line}」
    </div>
  </div>
"""
