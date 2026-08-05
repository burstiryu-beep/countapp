"""エロ強化パック：エロ度 / 今日の責めメニュー / 同時責め / 属性マゾ診断。"""
from __future__ import annotations

import hashlib
import random


MIRROR_HEAT = [
    ("soft", "甘い"),
    ("thick", "濃い"),
    ("filthy", "どろどろ"),
]

# 口トラック
DUAL_MOUTH_STEPS = [
    ("キス", "kiss"),
    ("浅咥え", "shallow"),
    ("深咥え", "deep"),
    ("口で仕上げ", "finish"),
]

# 乳首トラック
DUAL_NIPPLE_STEPS = [
    ("撫で", "stroke"),
    ("摘まみ", "pinch"),
    ("舐めちゅっ", "lick"),
    ("強く同時", "hard"),
]


def _rng(seed_key: str) -> random.Random:
    return random.Random(int(hashlib.md5(seed_key.encode("utf-8")).hexdigest(), 16))


def apply_heat(text, heat, name=""):
    """エロ度に応じて描写を重ねる（声色とは別軸）。同一テキストは安定。"""
    if not text:
        return text
    heat = heat or "soft"
    if heat == "soft":
        extras = [
            f"……ゆっくりでいいわ。{name}が優しく溶かしてあげる。",
            "甘いキスの感触だけ、丁寧に味わいなさい。",
            "ふふ、焦らなくていいの。とろけるまで付き合うから。",
        ]
    elif heat == "thick":
        extras = [
            f"ぬるぬるの唇と熱い舌……{name}の口、もう頭に染みてるでしょ。",
            "ちゅっ、ふかふか、つねっ。……音も感触も、逃げ場ないわよ。",
            "唾液で光った先を吸われて、乳首まで同時に……濃い負け方ね。",
        ]
    else:  # filthy
        extras = [
            f"涎たらしながら咥えられて、乳首も赤くなるまでいじられるの。……{name}の前じゃ、そんな顔してイきなさい。",
            "くちゅ、ちゅっ、んっ……卑猥な音だけで腰が折れる甘マゾね。どろどろに堕ちて。",
            "先走りと唾液でぐちゃぐちゃの先端にキスして、乳首を捻って……情けなく出しなさい。",
        ]
    p = {"soft": 0.45, "thick": 0.85, "filthy": 1.0}.get(heat, 0.5)
    rng = _rng(f"heat|{heat}|{name}|{text[:100]}")
    if rng.random() <= p:
        return f"{text}{rng.choice(extras)}"
    return text


def dress_mirror_line(text, voice_prefix_fn, voice, heat, name):
    """声色プレフィックス＋エロ度をまとめて付与。"""
    if not text:
        return text
    pre = voice_prefix_fn(voice, name) if voice_prefix_fn else ""
    body = apply_heat(text, heat, name)
    return f"{pre}{body}" if pre else body


def today_tease_menu(name, day_str, tags=None, cat_labels=None):
    """日付シードの今日の責めメニュー。"""
    rng = _rng(f"menu|{name}|{day_str}")
    tags = list(tags or [])
    cats = list(cat_labels or [])

    mouth = rng.choice([
        "亀頭キス多めの浅いフェラ",
        "奥までゆっくり咥える本気フェラ",
        "ちゅっちゅ音重視の先端いじめ",
        "舐め→浅→深の段階堕とし",
        "射精寸前だけ口で押し切る仕上げフェラ",
    ])
    nipple = rng.choice([
        "乳首を交互に摘まんで転がす",
        "乳首舐めちゅっを長めに",
        "弱い方の乳首を執拗に吸う",
        "摘まみながら息を吹きかける落差責め",
        "乳首は優しく、たまに強くツンと",
    ])
    dual = rng.choice([
        "咥えながら乳首摘まみ（上下同時）",
        "先端キスと乳首キスを交互に",
        "浅いフェラ中に乳首を強く",
        "奥フェラの合間に乳首舐め",
        "ふちで止めて、乳首だけで追い込む",
    ])
    finish = rng.choice([
        "口の中に出して受け止める",
        "亀頭にちゅってされながら出す",
        "乳首摘ままれたまま口でイく",
        "許可が出た瞬間に深く咥えられて出す",
        "余韻キスまでセットで敗北確定",
    ])

    # タグがあれば寄せる
    if any("奥フェラ" in t for t in tags):
        mouth = "奥までゆっくり咥える本気フェラ"
    if any("亀頭キス" in t or "ちゅっ" in t for t in tags):
        mouth = "亀頭キス多めの浅いフェラ"
    if any("乳首舐め" in t for t in tags):
        nipple = "乳首舐めちゅっを長めに"
    if any("摘まみ" in t for t in tags):
        nipple = "乳首を交互に摘まんで転がす"
    if any("同時" in t for t in tags):
        dual = "咥えながら乳首摘まみ（上下同時）"

    cat_bit = f"{'・'.join(cats[:2])}属性の" if cats else ""
    title = f"今日の責めメニュー — {cat_bit}{name}"
    whisper = rng.choice([
        f"今日はこれでイかせるわ。逃げ道、最初から塞いであるの。",
        f"メニュー通りに堕ちなさい。……予定調和の敗北、最高よ。",
        f"見てるだけで先が熱くなるメニューね。素直に従いなさい。",
        f"今日の負け方、もう決まってるわ。{name}の口と指に預けなさい。",
    ])
    return {
        "title": title,
        "mouth": mouth,
        "nipple": nipple,
        "dual": dual,
        "finish": finish,
        "whisper": whisper,
        "seed": day_str,
    }


def render_today_menu_html(menu):
    if not menu:
        return ""
    return f"""
<div style="max-width:520px;margin:0.4em auto 0.9em;padding:0.85em 1em;
  background:linear-gradient(160deg,rgba(194,24,91,0.2),rgba(40,0,25,0.55));
  border:1px solid #ff4081;border-radius:14px;">
  <div style="color:#ff80ab;font-size:0.78em;letter-spacing:0.08em;text-align:center;margin-bottom:0.45em;">
    📋 {menu['title']}
  </div>
  <div style="color:#ffe0f0;font-size:0.88em;line-height:1.55;">
    <div>💋 口：{menu['mouth']}</div>
    <div>💗 乳首：{menu['nipple']}</div>
    <div>🔥 同時：{menu['dual']}</div>
    <div>💦 仕上げ：{menu['finish']}</div>
  </div>
  <div style="color:#ffb6d9;font-style:italic;font-size:0.85em;margin-top:0.55em;text-align:left;">
    「{menu['whisper']}」
  </div>
</div>
"""


def dual_mouth_line(step_key, name):
    pool = {
        "kiss": [
            f"{name}が先端にちゅっ。……口トラック開始よ。キスだけで先を熱くしてあげる。",
            f"亀頭キス、丁寧に。……{name}の唇が先をふさいで、まだ咥えないわ。焦らしなさい。",
        ],
        "shallow": [
            f"浅く咥えるわ。……{name}の口が先だけ包んで、ちゅっ、と吸う。奥はまだよ。",
            f"ぬるっと浅く。……腰が追従しても深くしない。{name}、浅さで溶かしてあげる。",
        ],
        "deep": [
            f"深く。……{name}が奥まで咥えて、喉の熱で頭を白くするわ。逃げられない。",
            f"ふかふか奥まで。引き抜いてはまた深く。{name}の本気フェラ、来たわよ。",
        ],
        "finish": [
            f"口トラック仕上げ。……{name}が咥えたままキスで塞いで、出るところまで来るわ。",
            f"イかせる番よ。奥と先端キスで押し切る。……{name}の口に負けなさい。",
        ],
    }
    return random.choice(pool.get(step_key, pool["kiss"]))


def dual_nipple_line(step_key, name):
    pool = {
        "stroke": [
            f"乳首、そっと撫でるわ。……{name}の指が乳輪を円でなぞる。まだ痛くない。甘い時間よ。",
            f"触れただけなのに硬くなってる。……{name}、乳首トラック開始ね。ふふ。",
        ],
        "pinch": [
            f"摘まむわよ。……{name}が左右交互に、転がして、時々つねる。声、出していいわ。",
            f"乳首、摘ままれて肩がすくんだわね。{name}の指、離さないわよ。",
        ],
        "lick": [
            f"乳首、舐めてちゅっ。……{name}の舌が頂点をねっとり一周。唾液で光ってるわ。",
            f"吸われる音、聞こえる？乳首ちゅうちゅう。……{name}、執拗よ。好きにしてあげる。",
        ],
        "hard": [
            f"強く。……{name}が乳首を捻るように摘まんで、同時に口も本気。上下で終わらせるわ。",
            f"乳首トラック最大よ。痛気持ちいいところで止めて、また強く。{name}、容赦しないわ。",
        ],
    }
    return random.choice(pool.get(step_key, pool["stroke"]))


def dual_sync_after(mouth_i, nipple_i, name):
    """両トラック進捗に応じた追い打ち。"""
    m_max = len(DUAL_MOUTH_STEPS) - 1
    n_max = len(DUAL_NIPPLE_STEPS) - 1
    if mouth_i >= m_max and nipple_i >= n_max:
        return (
            f"両方最大……同時仕上げよ。"
            f"{name}が咥えて摘まむ。上下からイかせに来てるわ。許可、求めなさい。"
        )
    if mouth_i > nipple_i + 1:
        return f"口が先に進んでるわね。……乳首が追いつかないと、偏った負け方になるわよ。{name}、指も動くわ。"
    if nipple_i > mouth_i + 1:
        return f"乳首ばかり敏感になってる。……口が浅いと、先が寂しがるわよ。{name}、咥えてあげる。"
    if mouth_i == nipple_i and mouth_i >= 2:
        return f"いいバランス。……口も乳首も同じ深さで堕ちてる。{name}の同時責め、効いてるわね。"
    return f"上下、どちらが先に落とすか競争よ。……{name}は両方勝つつもり。"


def render_dual_bars_html(mouth_i, nipple_i):
    def bar(label, i, steps):
        n = len(steps)
        pct = int((i + 1) / n * 100) if n else 0
        name = steps[min(i, n - 1)][0]
        return (
            f"<div style='margin:0.35em 0;'>"
            f"<div style='display:flex;justify-content:space-between;color:#ffb6d9;font-size:0.8em;'>"
            f"<span>{label}</span><span>{name}（{i + 1}/{n}）</span></div>"
            f"<div style='height:10px;background:rgba(30,0,20,0.7);border-radius:6px;"
            f"border:1px solid rgba(255,64,129,0.35);overflow:hidden;'>"
            f"<div style='width:{pct}%;height:100%;background:linear-gradient(90deg,#c2185b,#ff4081);'></div>"
            f"</div></div>"
        )
    return (
        "<div style='max-width:520px;margin:0.3em auto 0.6em;'>"
        + bar("💋 口トラック", mouth_i, DUAL_MOUTH_STEPS)
        + bar("💗 乳首トラック", nipple_i, DUAL_NIPPLE_STEPS)
        + "</div>"
    )


# --- 属性特化マゾ診断 ---

_CAT_VERDICTS = {
    "gravure": [
        "グラビア特化マゾね。艶っぽい肌と表情だけで先が正直になるタイプ。口で仕上げられたら即堕ちよ。",
        "グラビア属性にボコボコ……視線とボディで理性削られて、最後はフェラでトドメ、典型よ。",
    ],
    "cosplay": [
        "コスプレ特化マゾ。衣装の記号性に弱いのね。役柄のまま咥えられる想像で、もう負けてるわ。",
        "コスに敗北射精してる時点で、属性に支配されてるわよ。ふふ、かわいい。",
    ],
    "swimsuit": [
        "水着特化。……肌の露出と水気の連想で、涎と一緒にとろけるタイプね。",
        "水着グラビアに負けるの、夏だけじゃないでしょ。通年マゾよ。",
    ],
    "uniform": [
        "制服特化マゾ。記号に屈して、口で堕とされる流れが決まってるわね。",
        "制服属性の敗北が多い……ギャップで崩れるタイプ。乳首も一緒にやられたら終わりよ。",
    ],
    "idol": [
        "アイドル特化。推しに敗北射精するの、いちばん甘マゾよ。口で甘やかされても拒否できないわね。",
        "アイドル属性に偏ってる。……応援の延長でイかされてるの、ばれてるわ。",
    ],
    "oneesan": [
        "お姉さん・OL特化。余裕ある責めで溶かされるのが好きなんでしょ。命令＋フェラ、最悪ね。",
        "お姉さん属性にボコボコ……頭の中で叱られながら咥えられてるわよ。",
    ],
    "jk": [
        "学生系特化。……いけない属性に弱いの、自覚ありそうね。ふふ、責めやすい。",
        "学生系に偏った敗北記録、ちゃんと残ってるわ。口と乳首、両方狙うわよ。",
    ],
    "married": [
        "人妻・熟女特化。ねっとりとした大人の口に堕ちるタイプね。濃い負け方がお似合いよ。",
        "熟れた属性に敗北が多い……涎と体温で溶かされてるの、目に浮かぶわ。",
    ],
    "other": [
        "その他枠に逃げるな。……分類できない弱さこそ、一番エロいわよ。",
        "その他に固まってるなら、もっと細かく属性つけなさい。偏りを直視するの。",
    ],
}


def category_mazo_diagnosis(stats, top_n=3):
    """カテゴリ敗北統計から属性特化マゾ診断テキストを返す。"""
    rows = [r for r in (stats.get("rows") or []) if r.get("count", 0) > 0]
    if not rows:
        return {
            "headline": "まだ属性マゾ診断できないわ",
            "body": "カテゴリを付けて敗北を重ねなさい。……偏りが出たときが、本当の快感よ。",
            "cards": [],
        }
    cards = []
    for i, r in enumerate(rows[:top_n]):
        cid = r.get("id", "")
        if cid in _CAT_VERDICTS:
            verdicts = _CAT_VERDICTS[cid]
        else:
            verdicts = [
                f"「{r.get('name')}」特化で{r.get('count')}回。……この属性の口と身体に、ちゃんと飼われてるわね。"
            ]
        rng = _rng(f"diag|{cid}|{r.get('count')}")
        cards.append({
            "rank": i + 1,
            "icon": r.get("icon", "🏷"),
            "name": r.get("name", cid),
            "count": r.get("count", 0),
            "pct": r.get("pct", 0),
            "verdict": rng.choice(verdicts),
        })
    peak = cards[0]
    headline = f"あなたは【{peak['icon']} {peak['name']}】特化マゾよ"
    body = (
        f"属性敗北の{peak['pct']}%が「{peak['name']}」。"
        f"{peak['count']}回もボコボコにされて、ちんぽが属性記憶してるわね❤️ "
        f"他の属性も見なさい。……負け癖の地図よ。"
    )
    return {"headline": headline, "body": body, "cards": cards}


def render_category_mazo_html(diag):
    if not diag:
        return ""
    cards_html = ""
    for c in diag.get("cards") or []:
        crown = " 👑" if c["rank"] == 1 else ""
        cards_html += f"""
<div style="background:rgba(30,0,20,0.45);border:1px solid rgba(255,64,129,0.3);
  border-radius:12px;padding:0.75em 0.9em;margin:0.45em 0;">
  <div style="display:flex;justify-content:space-between;align-items:baseline;">
    <span style="color:#ffe0f0;font-weight:800;">#{c['rank']} {c['icon']} {c['name']}{crown}</span>
    <span style="color:#ff80ab;font-weight:700;">{c['count']} 敗北 · {c['pct']}%</span>
  </div>
  <div style="color:#ffb6d9;font-style:italic;font-size:0.88em;margin-top:0.4em;line-height:1.5;">
    「{c['verdict']}」
  </div>
</div>
"""
    return f"""
<div style="background:rgba(15,0,10,0.65);border:1px solid rgba(194,24,91,0.4);
  border-radius:14px;padding:1em 1.1em;margin:0.5em 0 1em;max-width:640px;margin-left:auto;margin-right:auto;">
  <div style="color:#ff80ab;font-size:0.8em;letter-spacing:0.1em;text-align:center;">🏷 属性特化マゾ診断</div>
  <div style="color:#ffe0f0;font-size:1.15em;font-weight:900;text-align:center;margin:0.35em 0;">
    {diag.get('headline', '')}
  </div>
  <div style="color:#ffb6d9;font-style:italic;font-size:0.9em;text-align:center;line-height:1.5;margin-bottom:0.6em;">
    {diag.get('body', '')}
  </div>
  {cards_html}
</div>
"""


def self_resist_line(choice, name, gauge=None, heat="thick", edge_n=0):
    """声だけ抵抗するも体は正直 — ユーザー側の情けない独り言。

    彼女のセリフのあいだに差し込むと、抵抗する声と正直な体のズレで抜ける。
    choice / gauge / heat でシード固定し、同じ操作では同じ独り言になる。
    """
    choice = str(choice or "")
    gauge = gauge or ""
    heat = heat or "thick"
    edge_n = int(edge_n or 0)

    # 声だけの抵抗
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
    # 体は正直
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

    # キー正規化（dual / edge_loop / gauge）
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
        key = choice  # 下でゲージ別処理
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
