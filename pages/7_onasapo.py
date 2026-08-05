"""オナサポモード：ちんぽに効く敗北誘導セッション。"""
from datetime import datetime, timedelta, timezone
import traceback

import streamlit as st

import style
from core import get_data, ensure_structure
from categories import category_labels
from storage import save_data
from utils import active_items, make_key, img_to_html

try:
    # onasapo.py ではなく sapo_engine（Cloud の名前衝突・欠落対策）
    from sapo_engine import (
        ONASAPO_STYLES,
        ONASAPO_PACES,
        dress_onasapo,
        resolve_style,
        next_phase,
        prev_phase,
        onasapo_line,
        onasapo_after,
        onasapo_self_line,
        onasapo_react_options,
        phase_label,
        render_phase_dots_html,
        render_tension_html,
        denial_self_line,
        denial_after,
    )
except Exception as _sapo_err:
    style.apply()
    st.error("オナサポの読み込みに失敗したわ")
    st.code(f"{type(_sapo_err).__name__}: {_sapo_err}\n\n{traceback.format_exc()}")
    st.stop()

try:
    from ero_flavor import MIRROR_HEAT
except ImportError:
    MIRROR_HEAT = [("soft", "甘い"), ("thick", "濃い"), ("filthy", "どろどろ")]

try:
    from self_voice import render_self_voice_html
except ImportError:
    def render_self_voice_html(line, label="あなた（声だけ）"):
        if not line:
            return ""
        return (
            f"<div style='margin:0.45em 0;padding:0.55em 0.7em;border-radius:10px;"
            f"background:rgba(0,0,0,0.28);border:1px dashed rgba(255,182,217,0.45);'>"
            f"<div style='color:#ff80ab;font-size:0.72em;'>🎙 {label}</div>"
            f"<div style='color:#ffe0f0;font-style:italic;'>「{line}」</div></div>"
        )

JST = timezone(timedelta(hours=9))

style.apply()
data = ensure_structure(get_data())
now_jst = datetime.now(JST)

st.markdown("<h2 style='text-align:center'>🎙 オナサポモード</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#ff80ab;margin-bottom:0.8em;'>"
    "ちんぽに効く❤️　手が動くたび口とキスと乳首の想像で、情けなく敗北射精まで導くわ"
    "</p>",
    unsafe_allow_html=True,
)

items = [v for v in active_items(data).values() if v.get("name")]
if not items:
    st.warning("オナペがまだないわ。管理画面で追加してから来なさい。")
    st.stop()

names = sorted({v["name"] for v in items})
name_to_item = {}
for v in items:
    name_to_item[v["name"]] = v

# --- セッション設定 ---
st.markdown("##### セッション設定")
c1, c2 = st.columns(2)
with c1:
    default_name = st.session_state.get("sapo_name") or names[0]
    try:
        n_idx = names.index(default_name)
    except ValueError:
        n_idx = 0
    sapo_name = st.selectbox("相手（オナペ）", names, index=n_idx, key="sapo_name_sel")
with c2:
    style_labs = [lab for _, lab in ONASAPO_STYLES]
    style_keys = [k for k, _ in ONASAPO_STYLES]
    cur_style = st.session_state.get("sapo_style", "mouth")
    try:
        s_idx = style_keys.index(cur_style)
    except ValueError:
        s_idx = 0
    style_lab = st.selectbox("責めタイプ", style_labs, index=s_idx, key="sapo_style_sel")
    sapo_style = style_keys[style_labs.index(style_lab)]

p1, p2, p3 = st.columns(3)
with p1:
    pace_labs = [lab for _, lab in ONASAPO_PACES]
    pace_keys = [k for k, _ in ONASAPO_PACES]
    cur_pace = st.session_state.get("sapo_pace", "normal")
    try:
        p_idx = pace_keys.index(cur_pace)
    except ValueError:
        p_idx = 1
    pace_lab = st.radio("ペース", pace_labs, index=p_idx, horizontal=True, key="sapo_pace_radio")
    sapo_pace = pace_keys[pace_labs.index(pace_lab)]
with p2:
    heat_labs = [lab for _, lab in MIRROR_HEAT]
    heat_keys = [k for k, _ in MIRROR_HEAT]
    cur_heat = st.session_state.get("sapo_heat", "filthy")
    try:
        h_idx = heat_keys.index(cur_heat)
    except ValueError:
        h_idx = 2
    heat_lab = st.radio("エロ度", heat_labs, index=h_idx, horizontal=True, key="sapo_heat_radio")
    sapo_heat = heat_keys[heat_labs.index(heat_lab)]
with p3:
    voices = [
        ("sweet", "甘い"),
        ("sticky", "ねっとり"),
        ("urgent", "急かす"),
        ("tease", "からかう"),
        ("dote", "溺愛"),
        ("command", "命令"),
    ]
    v_labs = [lab for _, lab in voices]
    v_keys = [k for k, _ in voices]
    cur_v = st.session_state.get("sapo_voice", "sticky")
    try:
        v_idx = v_keys.index(cur_v)
    except ValueError:
        v_idx = 1
    v_lab = st.radio("声色", v_labs, index=v_idx, horizontal=True, key="sapo_voice_radio")
    sapo_voice = v_keys[v_labs.index(v_lab)]

st.session_state.setdefault("sapo_self_voice", True)
sapo_self_on = st.checkbox(
    "自分の声（声だけ抵抗・ちんぽは正直）",
    key="sapo_self_voice",
    help="誘導のあいだに、抵抗する独り言を挟むよ",
)

st.session_state.sapo_name = sapo_name
st.session_state.sapo_style = sapo_style
st.session_state.sapo_pace = sapo_pace
st.session_state.sapo_heat = sapo_heat
st.session_state.sapo_voice = sapo_voice

item = name_to_item.get(sapo_name) or {}
tags = list(item.get("weak_tags") or [])
cats = category_labels(data, item.get("categories") or [])
resolved = resolve_style(sapo_style, tags)

img_html = img_to_html(
    item.get("img", ""),
    style="width:100%;max-height:280px;object-fit:cover;border-radius:14px;",
)
meta = ""
if cats:
    meta += f"<div style='color:#ff80ab;font-size:0.82em;margin-top:0.3em;'>{' · '.join(cats)}</div>"
if tags:
    meta += f"<div style='color:#ffb6d9;font-size:0.78em;margin-top:0.2em;'>弱点：{' / '.join(tags)}</div>"

st.markdown(f"""
<div class="ero-card" style="max-width:520px;margin:0.6em auto 1em;text-align:center;">
  {img_html if img_html else ''}
  <h3 style="margin:0.4em 0 0.2em;">💋 {sapo_name}</h3>
  {meta}
  <div style="color:#804060;font-size:0.78em;margin-top:0.35em;">
    モード：{dict(ONASAPO_STYLES).get(resolved, resolved)} ／ ペース：{dict(ONASAPO_PACES).get(sapo_pace)}
  </div>
  <div style="color:#ff80ab;font-size:0.78em;margin-top:0.35em;font-style:italic;">
    ちんぽ、今日は逃がさないわよ❤️
  </div>
</div>
""", unsafe_allow_html=True)

# --- セッション状態 ---
st.session_state.setdefault("sapo_phase", "ready")
st.session_state.setdefault("sapo_edge_n", 0)
st.session_state.setdefault("sapo_denial_n", 0)
st.session_state.setdefault("sapo_line", None)
st.session_state.setdefault("sapo_after", None)
st.session_state.setdefault("sapo_self", None)
st.session_state.setdefault("sapo_active", False)
st.session_state.setdefault("sapo_for", None)
st.session_state.setdefault("sapo_react", None)
st.session_state.setdefault("sapo_permit", None)

# 相手が変わったらリセット
if st.session_state.get("sapo_for") != sapo_name:
    st.session_state.sapo_for = sapo_name
    st.session_state.sapo_phase = "ready"
    st.session_state.sapo_edge_n = 0
    st.session_state.sapo_denial_n = 0
    st.session_state.sapo_line = None
    st.session_state.sapo_after = None
    st.session_state.sapo_self = None
    st.session_state.sapo_active = False
    st.session_state.sapo_react = None
    st.session_state.sapo_permit = None


def _gen_line(phase=None, edge_n=None, react=None):
    ph = phase or st.session_state.sapo_phase
    en = st.session_state.sapo_edge_n if edge_n is None else edge_n
    rx = st.session_state.sapo_react if react is None else react
    dn = int(st.session_state.get("sapo_denial_n") or 0)
    raw = onasapo_line(ph, sapo_name, resolved, sapo_pace, en, tags, react=rx)
    st.session_state.sapo_line = dress_onasapo(raw, sapo_name, sapo_voice, sapo_heat)
    if rx in ("deny", "noerect", "endure"):
        st.session_state.sapo_after = denial_after(sapo_name, dn)
        st.session_state.sapo_self = denial_self_line(sapo_name, dn) if sapo_self_on else None
    else:
        st.session_state.sapo_after = onasapo_after(ph, sapo_name, resolved, en)
        if sapo_self_on:
            st.session_state.sapo_self = onasapo_self_line(ph, sapo_name, en, react=rx)
        else:
            st.session_state.sapo_self = None


def _reset_session():
    st.session_state.sapo_active = False
    st.session_state.sapo_phase = "ready"
    st.session_state.sapo_edge_n = 0
    st.session_state.sapo_denial_n = 0
    st.session_state.sapo_line = None
    st.session_state.sapo_after = None
    st.session_state.sapo_self = None
    st.session_state.sapo_react = None
    st.session_state.sapo_permit = None


# --- 開始 / リセット ---
b_start, b_reset = st.columns(2)
with b_start:
    if st.button("🎙 ちんぽ敗北オナサポ開始", key="sapo_start", use_container_width=True):
        st.session_state.sapo_active = True
        st.session_state.sapo_phase = "ready"
        st.session_state.sapo_edge_n = 0
        st.session_state.sapo_denial_n = 0
        st.session_state.sapo_react = None
        st.session_state.sapo_permit = None
        _gen_line("ready", 0)
        st.rerun()
with b_reset:
    if st.button("↺ セッションリセット", key="sapo_reset", use_container_width=True):
        _reset_session()
        st.rerun()

if not st.session_state.sapo_active:
    st.markdown(
        "<div style='text-align:center;color:#ffb6d9;font-style:italic;margin:1em 0;'>"
        "設定を選んで開始しなさい。……ちんぽ、出す準備はいい？　口でイかせに来るわよ"
        "</div>",
        unsafe_allow_html=True,
    )
    st.stop()

phase = st.session_state.sapo_phase
edge_n = int(st.session_state.sapo_edge_n or 0)
denial_n = int(st.session_state.get("sapo_denial_n") or 0)

st.markdown(render_phase_dots_html(phase), unsafe_allow_html=True)
st.markdown(render_tension_html(phase, edge_n, denial_n), unsafe_allow_html=True)
st.caption(
    f"いま：{phase_label(phase)}"
    + (f" ／ ふち ×{edge_n}" if phase == "edge" else "")
    + (f" ／ 我慢宣言 ×{denial_n}" if denial_n else "")
    + " —— 口では負けない、ちんぽはフル勃起"
)

if not st.session_state.sapo_line:
    _gen_line()

_self_html = ""
if sapo_self_on and st.session_state.get("sapo_self"):
    _self_html = render_self_voice_html(st.session_state.sapo_self)

# メイン誘導カード
st.markdown(f"""
<div style="max-width:560px;margin:0.5em auto 0.8em;padding:1.1em 1.2em;text-align:left;
  background:linear-gradient(160deg,rgba(194,24,91,0.25),rgba(40,0,25,0.6));
  border:1px solid #ff4081;border-radius:16px;box-shadow:0 0 18px rgba(255,64,129,0.25);">
  <div style="color:#ff80ab;font-size:0.75em;letter-spacing:0.12em;text-align:center;margin-bottom:0.45em;">
    🎙 ONASAPO · {phase_label(phase)} · ちんぽ敗北誘導
  </div>
  <div class="mirror-chu" style="font-size:0.8em;text-align:center;margin-bottom:0.4em;">ちゅっ……</div>
  <div style="color:#ff80ab;font-size:0.7em;margin-bottom:0.2em;">{sapo_name}</div>
  <div style="color:#ffb6d9;font-style:italic;font-size:1.05em;line-height:1.65;margin-bottom:0.45em;">
    「{st.session_state.sapo_line}」
  </div>
  {_self_html}
  <div style="color:#ff80ab;font-size:0.7em;margin:0.35em 0 0.2em;">{sapo_name}・追い打ち</div>
  <div style="color:#ffe0f0;font-style:italic;font-size:0.9em;line-height:1.55;
    border-top:1px solid rgba(255,64,129,0.3);padding-top:0.55em;">
    「{st.session_state.sapo_after}」
  </div>
</div>
""", unsafe_allow_html=True)

# --- 我慢宣言（フル勃起特攻）---
st.markdown("##### 🛡 我慢する？（フル勃起のまま）")
st.caption("負けない宣言、大歓迎よ。……するたび張力が上がるわ❤️")
d_a, d_b = st.columns(2)
with d_a:
    if st.button("オナサポなんかに負けん！絶対我慢！", key="sapo_deny_endure", use_container_width=True):
        st.session_state.sapo_denial_n = denial_n + 1
        st.session_state.sapo_react = "deny"
        if denial_n + 1 >= 5 and phase in ("build", "edge"):
            st.session_state.sapo_permit = "ask"
        elif denial_n + 1 >= 3 and phase in ("ready", "warmup"):
            st.session_state.sapo_phase = "build"
        _gen_line(react="deny")
        st.rerun()
with d_b:
    if st.button("ボッキすらしないぞ！（フル勃起）", key="sapo_deny_noerect", use_container_width=True):
        st.session_state.sapo_denial_n = denial_n + 1
        st.session_state.sapo_react = "noerect"
        if denial_n + 1 >= 4 and phase == "build":
            st.session_state.sapo_phase = "edge"
            st.session_state.sapo_edge_n = max(1, edge_n)
        _gen_line(react="noerect")
        st.rerun()

# --- ちんぽ反応（対話）---
st.markdown("##### 💦 ちんぽの返事")
st.caption("正直に言いなさい。強がるほど誘導が寄ってくるわ")
_opts = onasapo_react_options(phase, edge_n)
_cols = st.columns(2)
for i, (okey, olabel) in enumerate(_opts):
    with _cols[i % 2]:
        if st.button(olabel, key=f"sapo_rx_{phase}_{okey}_{i}_{denial_n}", use_container_width=True):
            st.session_state.sapo_react = okey
            if okey in ("deny", "noerect", "endure"):
                st.session_state.sapo_denial_n = denial_n + 1
            if okey == "near" and phase == "build":
                st.session_state.sapo_phase = "edge"
                st.session_state.sapo_edge_n = max(1, edge_n)
            elif okey == "cum" and phase in ("edge", "build"):
                st.session_state.sapo_permit = "ask"
            elif okey == "want" and phase in ("ready", "warmup"):
                st.session_state.sapo_phase = next_phase(phase) if phase == "ready" else "build"
            _gen_line(react=okey)
            st.rerun()

# --- 操作 ---
c_prev, c_again, c_next = st.columns(3)
with c_prev:
    if st.button("← 戻る", key="sapo_prev", use_container_width=True, disabled=phase == "ready"):
        st.session_state.sapo_phase = prev_phase(phase)
        if st.session_state.sapo_phase != "edge":
            st.session_state.sapo_edge_n = 0
        st.session_state.sapo_react = None
        _gen_line()
        st.rerun()
with c_again:
    if st.button("💬 もう一声（ちんぽ向け）", key="sapo_again", use_container_width=True):
        _gen_line()
        st.rerun()
with c_next:
    next_lbl = {
        "ready": "前戯へ → 先を起こす",
        "warmup": "本番へ → しごく",
        "build": "ふちへ → 出させない",
        "edge": "仕上げへ → イかせる",
        "finish": "余韻へ →",
        "after": "最初から",
    }.get(phase, "次へ →")
    if st.button(next_lbl, key="sapo_next", use_container_width=True):
        if phase == "after":
            st.session_state.sapo_phase = "ready"
            st.session_state.sapo_edge_n = 0
            st.session_state.sapo_denial_n = 0
            st.session_state.sapo_permit = None
        elif phase == "edge" and st.session_state.get("sapo_permit") != "granted" and edge_n < 3:
            # ふちが浅いと許可を促す
            st.session_state.sapo_permit = "ask"
            st.session_state.sapo_react = "cum"
            _gen_line("edge", react="cum")
            st.rerun()
        else:
            st.session_state.sapo_phase = next_phase(phase)
            if st.session_state.sapo_phase == "edge":
                st.session_state.sapo_edge_n = max(1, edge_n)
            st.session_state.sapo_react = None
        _gen_line()
        st.rerun()

# ふち専用
if phase == "edge":
    st.markdown("##### 🔥 ふちでちんぽを泣かせる")
    st.caption(f"いまふち ×{edge_n}/5 —— 出させないまま張力を積み上げなさい")
    e1, e2, e3 = st.columns(3)
    with e1:
        if st.button("ふち+1（出さない）", key="sapo_edge_more", use_container_width=True):
            st.session_state.sapo_edge_n = min(5, edge_n + 1)
            st.session_state.sapo_react = "near"
            _gen_line("edge")
            st.rerun()
    with e2:
        if st.button("亀頭だけいじめ", key="sapo_edge_glans", use_container_width=True):
            st.session_state.sapo_edge_n = min(5, max(edge_n, 1) + 0)
            st.session_state.sapo_react = "resist"
            _gen_line("edge", react="resist")
            st.rerun()
    with e3:
        if st.button("💦 限界…仕上げて", key="sapo_edge_finish", use_container_width=True):
            st.session_state.sapo_permit = "ask"
            st.session_state.sapo_react = "cum"
            _gen_line("edge", react="cum")
            st.rerun()

# 許可制（ふち終盤〜仕上げ）
show_permit = (
    st.session_state.get("sapo_permit") in ("ask", "denied", "granted")
    or phase == "finish"
    or (phase == "edge" and edge_n >= 3)
)
if show_permit and phase in ("edge", "build", "finish") and st.session_state.get("sapo_permit") != "granted":
    if st.session_state.get("sapo_permit") not in ("ask", "denied", "granted"):
        st.session_state.sapo_permit = "ask"
    st.markdown(f"""
<div style="max-width:560px;margin:0.6em auto;padding:0.85em 1em;text-align:center;
  border:1px dashed #ff80ab;border-radius:12px;background:rgba(80,0,40,0.35);">
  <div style="color:#ff80ab;font-size:0.78em;letter-spacing:0.1em;">出していい？　ちんぽ許可制</div>
  <div style="color:#ffb6d9;font-style:italic;font-size:0.92em;margin-top:0.35em;">
    「{sapo_name}の口でイきたいなら、許可を求めなさい。……まだだめ／出していい」
  </div>
</div>
""", unsafe_allow_html=True)
    d1, d2 = st.columns(2)
    with d1:
        if st.button("まだだめ…ふちに戻せ", key="sapo_deny", use_container_width=True):
            st.session_state.sapo_permit = "denied"
            st.session_state.sapo_phase = "edge"
            st.session_state.sapo_edge_n = min(5, max(edge_n, 1) + 1)
            st.session_state.sapo_react = "resist"
            _gen_line("edge", react="resist")
            st.rerun()
    with d2:
        if st.button("出していいわ…イけ❤️", key="sapo_allow", use_container_width=True):
            st.session_state.sapo_permit = "granted"
            st.session_state.sapo_phase = "finish"
            st.session_state.sapo_react = "cum"
            _gen_line("finish", react="cum")
            st.rerun()

if st.session_state.get("sapo_permit") == "granted" and phase == "finish":
    st.markdown(f"""
<div style="max-width:560px;margin:0.5em auto;padding:0.85em;text-align:center;
  background:linear-gradient(160deg,rgba(255,64,129,0.3),rgba(40,0,25,0.55));
  border:1px solid #ff80ab;border-radius:14px;">
  <div style="color:#ff80ab;font-size:0.78em;">💋 許可済み · ちんぽ出せ</div>
  <div style="color:#ffe0f0;font-style:italic;margin-top:0.35em;line-height:1.5;">
    「{sapo_name}の口に負けて、全部出しなさい。敗北射精、記録する番よ」
  </div>
</div>
""", unsafe_allow_html=True)

# 仕上げ：敗北記録
if phase in ("finish", "after"):
    st.markdown("##### 💋 敗北を記録する")
    st.caption("イけたら証拠を残しなさい。……ちんぽが負けた記録よ")
    if st.button(f"💋 {sapo_name}にちんぽ敗北射精する", key="sapo_record", use_container_width=True):
        item_key = next((k for k, v in data["items"].items() if v.get("name") == sapo_name), None)
        count_date = now_jst.date()
        m = count_date.strftime("%Y-%m")
        if item_key:
            if not isinstance(data["items"][item_key].get("counts"), dict):
                data["items"][item_key]["counts"] = {}
            data["items"][item_key]["counts"][m] = data["items"][item_key]["counts"].get(m, 0) + 1
            tab = data["items"][item_key].get("tab", "all")
        else:
            item_key = make_key(sapo_name, "all")
            data["items"][item_key] = {
                "name": sapo_name, "tab": "all", "counts": {m: 1},
                "img": "", "points": 0, "weak_tags": [], "mirror_note": "", "categories": [],
            }
            tab = "all"
        time_str = datetime.combine(count_date, now_jst.time()).strftime("%Y-%m-%d %H:%M:%S")
        data["history"].append({"name": sapo_name, "tab": tab, "time": time_str})
        ok, err = save_data(data)
        st.session_state.sapo_phase = "after"
        st.session_state.sapo_permit = "granted"
        _gen_line("after")
        if ok:
            st.success(f"✅ {sapo_name} にちんぽ敗北射精を記録したわ……えらい子❤️")
        else:
            st.warning(f"記録に失敗かも: {err}")
        st.rerun()

st.divider()
st.markdown(
    "<p style='text-align:center;color:#804060;font-size:0.8em;'>"
    "鏡チェックとは別モードよ。ふちを積んで、許可を乞って、口でイかされなさい。"
    "</p>",
    unsafe_allow_html=True,
)
