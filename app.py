import streamlit as st
import style

st.set_page_config(
    page_title="射精カウンター",
    page_icon="💦",
    layout="wide",
)
style.apply()

st.markdown("""
<div style="text-align:center; padding: 2em 0 1em;">
  <div style="font-size:3.5em;">💦</div>
  <h1 style="font-size:2.6em; margin:0.2em 0;">射精カウンター</h1>
  <p style="color:#ff80ab; font-size:1.15em; letter-spacing:0.06em;">
    あなたの健康習慣を、こっそり記録。
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
<div class="ero-card">
  <div style="font-size:2em;">🏠</div>
  <h3>ホーム</h3>
  <p style="color:#ffb6d9; font-size:0.9em;">弱点ごとにカウント</p>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div class="ero-card">
  <div style="font-size:2em;">📊</div>
  <h3>ダッシュボード</h3>
  <p style="color:#ffb6d9; font-size:0.9em;">月別・合計の記録を確認</p>
</div>
""", unsafe_allow_html=True)
with col3:
    st.markdown("""
<div class="ero-card">
  <div style="font-size:2em;">🏆</div>
  <h3>ランキング</h3>
  <p style="color:#ffb6d9; font-size:0.9em;">最も感じた弱点はどこ？</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center; color:#804060; font-size:0.8em; margin-top:2em;">
  ← 左のメニューからページを選んでください
</p>
""", unsafe_allow_html=True)
