import streamlit as st
import requests

st.set_page_config(page_title="💓 감정 분석 기반 향기 추천", layout="centered")

st.markdown("""
<style>
.input-label {
    font-size:1.6em !important; font-weight:bold; color:#2a2a2a;
    margin-bottom:0.3em;
}
.neat-box {
    background:#eeeeee; border-radius:15px; padding:36px 0 36px 0;
    margin:10px 0 18px 0; box-shadow:0 2px 12px rgba(0,0,0,0.06);
}
.stButton button {
    background:linear-gradient(90deg,#FFB172 0%,#ffec87 100%);
    color:#000; border-radius:2em; font-weight:700; font-size:1.1em; padding:0.7em 2.2em;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border:none;
}
.stButton button:hover {
    background:linear-gradient(90deg,#ffec87 0%,#FFB172 100%);
    color:#333;
}
</style>
""", unsafe_allow_html=True)

st.title("💓 감정 분석 기반 향기 추천")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="input-label">심박수 (BPM)</div>', unsafe_allow_html=True)
    bpm = st.number_input("", min_value=40, max_value=180, value=75, key="bpm", label_visibility="collapsed")
    st.markdown('<div class="neat-box"></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-label">체온 (℃)</div>', unsafe_allow_html=True)
    temp = st.number_input("", min_value=34.0, max_value=42.0, value=36.5, step=0.1, key="temp", label_visibility="collapsed")
    st.markdown('<div class="neat-box"></div>', unsafe_allow_html=True)

# 상태 판별
if bpm >= 105 or temp >= 37.5:
    emotion = "STRESSED"
    label = '<span style="font-size:2em; font-weight:bold;">🔥 긴장 상태</span>'
    scent = "Stress Relief (White/Orange/Blue)"
elif bpm <= 65 or temp <= 35.0:
    emotion = "SLEEPY"
    label = '<span style="font-size:2em; font-weight:bold;">😴 졸림 상태</span>'
    scent = "Arousal (Red/Purple)"
else:
    emotion = "RELAXED"
    label = '<span style="font-size:2em; font-weight:bold;">😊 안정 상태</span>'
    scent = "Relaxation (Green/Blue)"

st.markdown(label, unsafe_allow_html=True)
st.markdown(f"<div style='font-size:1.15em; margin-bottom:18px;'>추천 컬러/향기: <b>{scent}</b></div>", unsafe_allow_html=True)

if st.button("🌸 실행하기"):
    try:
        res = requests.post(
            "https://cpd-flask2.onrender.com/trigger",
            json={"emotion": emotion},
            timeout=10   # 서버 깨우는 데 오래 걸릴 때 대비, 타임아웃 10초 권장
        )
        if res.status_code == 200:
            st.success("✅ 서버에 감정 상태가 전달되었습니다.")
            st.info("💡 GIGA 보드가 감정 상태를 요청해서 직접 실행합니다.")
        else:
            st.error(f"❌ 실행 실패: 서버 오류 (상태코드: {res.status_code})")
            st.error(res.text)
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
