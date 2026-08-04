"""オナサポモード：カウントと別枠の段階誘導セッション。"""
from datetime import datetime, timedelta, timezone

import streamlit as st

import style
from core import get_data, ensure_structure
from categories import category_labels
from storage import save_data
from utils import active_items, make_key, img_to_html
from onasapo import (
    ONASAPO_STYLES,
    ONASAPO_PACES,
    dress_onasapo,
    resolve_style,
    next_phase,
    prev_phase,
    onasapo_line,
    onasapo_after,
    phase_label,
    render_phase_dots_html,
)
from ero_flavor import MIRROR_HEAT

JST = timezone(timedelta(hours=9))

style.apply()
data = ensure_structure(get_data())
now_jst = datetime.now(JST)

st.markdown("<h2 style='text-align:center'>🎙 オナサポモード</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#ff80ab;margin-bottom:0.8em;'>"
    "カウントと別枠よ。……お姉さんが手の動きまで導いて、情けなくイかせてあげる❤️"
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
    cur_style = st.session_state.get("sapo_style", "dual")
    try:
        s_idx = style_keys.index(cur_style)
    except ValueError:
        s_idx = 2
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
    cur_heat = st.session_state.get("sapo_heat", "thick")
    try:
        h_idx = heat_keys.index(cur_heat)
    except ValueError:
        h_idx = 1
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
    cur_v = st.session_state.get("sapo_voice", "sweet")
    try:
        v_idx = v_keys.index(cur_v)
    except ValueError:
        v_idx = 0
    v_lab = st.radio("声色", v_labs, index=v_idx, horizontal=True, key="sapo_voice_radio")
    sapo_voice = v_keys[v_labs.index(v_lab)]

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
</div>
""", unsafe_allow_html=True)

# --- セッション状態 ---
st.session_state.setdefault("sapo_phase", "ready")
st.session_state.setdefault("sapo_edge_n", 0)
st.session_state.setdefault("sapo_line", None)
st.session_state.setdefault("sapo_after", None)
st.session_state.setdefault("sapo_active", False)
st.session_state.setdefault("sapo_for", None)

# 相手が変わったらリセット
if st.session_state.get("sapo_for") != sapo_name:
    st.session_state.sapo_for = sapo_name
    st.session_state.sapo_phase = "ready"
    st.session_state.sapo_edge_n = 0
    st.session_state.sapo_line = None
    st.session_state.sapo_after = None
    st.session_state.sapo_active = False


def _gen_line(phase=None, edge_n=None):
    ph = phase or st.session_state.sapo_phase
    en = st.session_state.sapo_edge_n if edge_n is None else edge_n
    raw = onasapo_line(ph, sapo_name, resolved, sapo_pace, en, tags)
    st.session_state.sapo_line = dress_onasapo(raw, sapo_name, sapo_voice, sapo_heat)
    st.session_state.sapo_after = onasapo_after(ph, sapo_name, resolved, en)


# --- 開始 / リセット ---
b_start, b_reset = st.columns(2)
with b_start:
    if st.button("🎙 オナサポ開始", key="sapo_start", use_container_width=True):
        st.session_state.sapo_active = True
        st.session_state.sapo_phase = "ready"
        st.session_state.sapo_edge_n = 0
        _gen_line("ready", 0)
        st.rerun()
with b_reset:
    if st.button("↺ セッションリセット", key="sapo_reset", use_container_width=True):
        st.session_state.sapo_active = False
        st.session_state.sapo_phase = "ready"
        st.session_state.sapo_edge_n = 0
        st.session_state.sapo_line = None
        st.session_state.sapo_after = None
        st.rerun()

if not st.session_state.sapo_active:
    st.markdown(
        "<div style='text-align:center;color:#ffb6d9;font-style:italic;margin:1em 0;'>"
        "設定を選んで「オナサポ開始」を押しなさい。……手、準備はいい？"
        "</div>",
        unsafe_allow_html=True,
    )
    st.stop()

phase = st.session_state.sapo_phase
edge_n = int(st.session_state.sapo_edge_n or 0)

st.markdown(render_phase_dots_html(phase), unsafe_allow_html=True)
st.caption(f"いま：{phase_label(phase)}" + (f" ／ ふち ×{edge_n}" if phase == "edge" else ""))

if not st.session_state.sapo_line:
    _gen_line()

# メイン誘導カード
st.markdown(f"""
<div style="max-width:560px;margin:0.5em auto 0.8em;padding:1.1em 1.2em;text-align:left;
  background:linear-gradient(160deg,rgba(194,24,91,0.25),rgba(40,0,25,0.6));
  border:1px solid #ff4081;border-radius:16px;box-shadow:0 0 18px rgba(255,64,129,0.25);">
  <div style="color:#ff80ab;font-size:0.75em;letter-spacing:0.12em;text-align:center;margin-bottom:0.45em;">
    🎙 ONASAPO · {phase_label(phase).upper()}
  </div>
  <div class="mirror-chu" style="font-size:0.8em;text-align:center;margin-bottom:0.4em;">ちゅっ……</div>
  <div style="color:#ffb6d9;font-style:italic;font-size:1.05em;line-height:1.6;margin-bottom:0.65em;">
    「{st.session_state.sapo_line}」
  </div>
  <div style="color:#ffe0f0;font-style:italic;font-size:0.9em;line-height:1.5;
    border-top:1px solid rgba(255,64,129,0.3);padding-top:0.55em;">
    「{st.session_state.sapo_after}」
  </div>
</div>
""", unsafe_allow_html=True)

# --- 操作 ---
c_prev, c_again, c_next = st.columns(3)
with c_prev:
    if st.button("← 戻る", key="sapo_prev", use_container_width=True, disabled=phase == "ready"):
        st.session_state.sapo_phase = prev_phase(phase)
        if st.session_state.sapo_phase != "edge":
            st.session_state.sapo_edge_n = 0
        _gen_line()
        st.rerun()
with c_again:
    if st.button("💬 もう一声", key="sapo_again", use_container_width=True):
        _gen_line()
        st.rerun()
with c_next:
    next_lbl = {
        "ready": "前戯へ →",
        "warmup": "本番へ →",
        "build": "ふちへ →",
        "edge": "仕上げへ →",
        "finish": "余韻へ →",
        "after": "最初から",
    }.get(phase, "次へ →")
    if st.button(next_lbl, key="sapo_next", use_container_width=True):
        if phase == "after":
            st.session_state.sapo_phase = "ready"
            st.session_state.sapo_edge_n = 0
        else:
            st.session_state.sapo_phase = next_phase(phase)
            if st.session_state.sapo_phase == "edge":
                st.session_state.sapo_edge_n = max(1, edge_n)
            if phase == "edge" and st.session_state.sapo_phase == "finish":
                pass
        _gen_line()
        st.rerun()

# ふち専用
if phase == "edge":
    e1, e2 = st.columns(2)
    with e1:
        if st.button("🔥 ふちでもう一度（出さない）", key="sapo_edge_more", use_container_width=True):
            st.session_state.sapo_edge_n = min(5, edge_n + 1)
            _gen_line("edge")
            st.rerun()
    with e2:
        if st.button("💦 もう限界…仕上げて", key="sapo_edge_finish", use_container_width=True):
            st.session_state.sapo_phase = "finish"
            _gen_line("finish")
            st.rerun()

# 仕上げ：敗北記録
if phase in ("finish", "after"):
    st.markdown("##### 敗北を記録する？")
    st.caption("イけたら証拠を残しなさい。……オナサポの成果よ")
    if st.button(f"💋 {sapo_name}に敗北射精する", key="sapo_record", use_container_width=True):
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
        _gen_line("after")
        if ok:
            st.success(f"✅ {sapo_name} に敗北射精を記録したわ……えらい子❤️")
        else:
            st.warning(f"記録に失敗かも: {err}")
        st.rerun()

st.divider()
st.markdown(
    "<p style='text-align:center;color:#804060;font-size:0.8em;'>"
    "鏡チェックやカウントとは別モードよ。焦らしていいし、一気にイかせてもいいわ。"
    "</p>",
    unsafe_allow_html=True,
)
