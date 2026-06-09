# ==========================================
# Streamlit
# ==========================================
import streamlit as st

# ==========================================
# API 호출
# ==========================================
import requests

# ==========================================
# 데이터 처리
# ==========================================
import pandas as pd

# ==========================================
# 그래프
# ==========================================
import plotly.express as px
import os
from streamlit_mic_recorder import mic_recorder
import tempfile
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==========================================
# 페이지 설정
# ==========================================
st.set_page_config(
    page_title="마음동행 AI",
    page_icon="🧠",
    layout="wide"
)

# ==========================================
# 제목
# ==========================================
st.title("🧠 마음동행 AI")

st.subheader("감정 캘린더 & 감정 분석")
# ==========================================
# 채팅 UI
# ==========================================

st.write("---")

st.write("## 💬 AI 말벗")
# ==========================================
# 음성 녹음
# ==========================================

audio = mic_recorder(
    

    start_prompt="🎤 녹음 시작",

    stop_prompt="⏹ 녹음 종료",

    key="recorder"
)
if audio:

    st.success("음성 녹음 완료")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as tmp_audio:

        tmp_audio.write(
            audio["bytes"]
        )

        audio_path = tmp_audio.name

    with open(audio_path, "rb") as file:

        transcription = client.audio.transcriptions.create(

            file=file,

            model="whisper-large-v3"
        )

    st.write("### 📝 음성 인식 결과")

    st.success(
        transcription.text
    )

    response = requests.get(

        "http://127.0.0.1:8000/chat",

        params={
            "message": transcription.text
        }
    )

    chat_data = response.json()

    st.write("### 🤖 AI 응답")

    st.success(
        chat_data["ai_response"]
    )
# ==========================================
# 채팅 기록 저장
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# ==========================================
# 채팅 기록 출력
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

user_input = st.text_input(
    "오늘 어떤 하루를 보내셨나요?"
)

if st.button("전송"):

    if user_input:

        response = requests.get(

            "http://127.0.0.1:8000/chat",

            params={
                "message": user_input
            }
        )

        chat_data = response.json()

        st.write("### 🤖 AI 응답")

        st.success(
            chat_data["ai_response"]
        )

        st.write("### 😊 감정 분석")

        st.json(
            chat_data["emotion_analysis"]
        )


# ==========================================
# API 데이터 조회
# ==========================================
response = requests.get(
    "http://127.0.0.1:8000/emotion-calendar"
)

data = response.json()

# ==========================================
# 데이터 없음
# ==========================================
if data["count"] == 0:

    st.warning("저장된 감정 데이터가 없습니다.")

else:

    # DataFrame 변환
    df = pd.DataFrame(data["data"])

    # 날짜 정렬
    df = df.sort_values("date")

    # --------------------------------------
    # 감정 기록
    # --------------------------------------
    st.write("## 📋 감정 기록")

    st.dataframe(
        df,
        use_container_width=True
    )

    # --------------------------------------
    # 최근 감정 상태
    # --------------------------------------
    latest = df.iloc[-1]
    
    # ==========================================
# AI 감정 리포트
# ==========================================

st.write("---")

st.write("## 🚨 AI 감정 리포트")

if latest["depressed"] >= 70:

    st.error(
        "최근 우울 점수가 높게 나타나고 있습니다."
    )

    st.write(
        "💡 추천 : 가벼운 산책, 가족과 통화, 취미 활동"
    )

elif latest["lonely"] >= 70:

    st.warning(
        "최근 외로움 감정이 높게 나타나고 있습니다."
    )

    st.write(
        "💡 추천 : 지인과 대화, 복지관 프로그램 참여"
    )

elif latest["anxiety"] >= 70:

    st.warning(
        "최근 불안 감정이 높게 나타나고 있습니다."
    )

    st.write(
        "💡 추천 : 명상, 심호흡, 가벼운 운동"
    )

else:

    st.success(
        "전반적으로 안정적인 감정 상태입니다."
    )

    st.write(
        "💡 추천 : 현재 생활 패턴 유지"
    )

    st.write("---")

    st.write("## 😊 최근 감정 상태")

    st.write(f"📅 날짜 : {latest['date']}")
    st.write(f"😊 행복 : {latest['happy']}")
    st.write(f"😌 안정 : {latest['stable']}")
    st.write(f"😔 외로움 : {latest['lonely']}")
    st.write(f"😟 불안 : {latest['anxiety']}")
    st.write(f"😢 우울 : {latest['depressed']}")

    # 감정 상태 표시
    if latest["depressed"] >= 70:
        st.error("🔴 우울 감정이 높습니다.")

    elif latest["lonely"] >= 70:
        st.warning("🟠 외로움 감정이 높습니다.")

    else:
        st.success("🟢 전반적으로 안정적인 상태입니다.")

    st.write("---")

    # --------------------------------------
    # 감정 그래프
    # --------------------------------------
    
    df = pd.DataFrame(data["data"])

    st.write("## 📊 감정 통계")

    avg_happy = round(df["happy"].mean(), 1)
    avg_stable = round(df["stable"].mean(), 1)
    avg_lonely = round(df["lonely"].mean(), 1)
    avg_anxiety = round(df["anxiety"].mean(), 1)
    avg_depressed = round(df["depressed"].mean(), 1)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("😊 행복", avg_happy)

    with col2:
        st.metric("😌 안정", avg_stable)

    with col3:
        st.metric("😔 외로움", avg_lonely)

    with col4:
        st.metric("😟 불안", avg_anxiety)

    with col5:
        st.metric("😢 우울", avg_depressed)

    emotion_avg = {
        "행복": avg_happy,
        "안정": avg_stable,
        "외로움": avg_lonely,
        "불안": avg_anxiety,
        "우울": avg_depressed
    }

    top_emotion = max(
        emotion_avg,
        key=emotion_avg.get
    )

    st.info(
        f"🏆 최근 가장 강하게 나타난 감정 : {top_emotion}"
    )
    st.write("## 📈 감정 변화 그래프")

    graph_df = pd.melt(

        df,

        id_vars=["date"],

        value_vars=[
            "happy",
            "stable",
            "lonely",
            "anxiety",
            "depressed"
        ],

        var_name="emotion",

        value_name="score"
    )

    fig = px.line(

        graph_df,

        x="date",

        y="score",

        color="emotion",

        markers=True,

        title="감정 변화 추이"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================================
# 감정 캘린더
# ==========================================

st.write("---")

st.write("## 🗓 감정 캘린더")

calendar_data = []

for _, row in df.iterrows():

    # 가장 높은 감정 찾기
    emotions = {

        "happy": row["happy"],
        "stable": row["stable"],
        "lonely": row["lonely"],
        "anxiety": row["anxiety"],
        "depressed": row["depressed"]
    }

    dominant_emotion = max(
        emotions,
        key=emotions.get
    )

    emoji_map = {
        "happy": "😊",
        "stable": "🟢",
        "lonely": "🟠",
        "anxiety": "🟡",
        "depressed": "🔴"
    }

    calendar_data.append({

        "날짜": row["date"],

        "대표 감정": dominant_emotion,

        "상태": emoji_map[dominant_emotion]
    })

calendar_df = pd.DataFrame(calendar_data)

st.dataframe(
    calendar_df,
    use_container_width=True
)

# ==========================================
# 위험 감지 시스템
# ==========================================

st.write("---")

st.write("## 🚨 감정 위험 감지")

recent_data = df.tail(3)

depressed_risk = all(
    score >= 70
    for score in recent_data["depressed"]
)

lonely_risk = all(
    score >= 70
    for score in recent_data["lonely"]
)

if depressed_risk:

    st.error(
        "최근 3회 연속 우울 점수가 높게 나타났습니다."
    )

if lonely_risk:

    st.warning(
        "최근 3회 연속 외로움 점수가 높게 나타났습니다."
    )

if not depressed_risk and not lonely_risk:

    st.success(
        "현재 특별한 위험 신호는 감지되지 않았습니다."
    )

# ==========================================
# PDF 보고서 생성
# ==========================================

st.write("---")

st.write("## 📄 감정 보고서")

pdf_path = "reports/emotion_report.pdf"

if st.button("PDF 생성"):

    requests.get(
        "http://127.0.0.1:8000/pdf-report"
    )

    st.success("PDF 생성 완료!")

if os.path.exists(pdf_path):

    with open(pdf_path, "rb") as file:

        st.download_button(

            label="📥 PDF 다운로드",

            data=file,

            file_name="emotion_report.pdf",

            mime="application/pdf"
        )

report_response = requests.get(
    "http://127.0.0.1:8000/emotion-report"
)

report_data = report_response.json()

st.info(
    report_data["report"]
)