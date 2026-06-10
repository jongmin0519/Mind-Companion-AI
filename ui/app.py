# ==========================================
# Streamlit
# ==========================================
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
import tempfile
import streamlit.components.v1 as components

from dotenv import load_dotenv
from groq import Groq
from streamlit_mic_recorder import mic_recorder
API_URL = "https://mind-companion-ai.onrender.com"

# ==========================================
# 환경 변수
# ==========================================
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
    layout="centered"
)

# ==========================================
# 제목
# ==========================================
st.title("🧠 마음동행 AI")

st.caption(
    "어르신 정서 케어 AI 말벗 서비스"
)

# ==========================================
# 탭 생성
# ==========================================
tab1, tab2, tab3 = st.tabs(
    [
        "💬 AI 말벗",
        "📊 감정 분석",
        "📄 보고서"
    ]
)

# ==========================================
# 감정 데이터 조회
# ==========================================
try:

    response = requests.get(
        f"{API_URL}/emotion-calendar"
    )

    data = response.json()

except:

    data = {
        "count": 0,
        "data": []
    }

# ==========================================
# DataFrame
# ==========================================
if data["count"] > 0:

    df = pd.DataFrame(
        data["data"]
    )

    df = df.sort_values(
        "date"
    )

    latest = df.iloc[-1]

else:

    df = pd.DataFrame()

    latest = None

# ==========================================
# TAB 1
# ==========================================
with tab1:

    st.subheader("💬 AI 말벗")

    audio = mic_recorder(

        start_prompt="🎤 녹음 시작",

        stop_prompt="⏹ 녹음 종료",

        key="voice"
    )

    if audio:

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

               f"{API_URL}/chat",

            params={
                "message": transcription.text
            }
        )
       

        chat_data = response.json()

        st.write("### 🤖 AI 응답")

        st.success(
            chat_data["ai_response"]
        )
    
                
    user_input = st.text_input(
        "오늘 어떤 하루를 보내셨나요?"
    )

    if st.button(
        "전송",
        key="chat_send"
    ):  

        if user_input:

            response = requests.get(

                   f"{API_URL}/chat",

                params={
                    "message": user_input
                }
            )

            chat_data = response.json()

            

            st.write("### 🤖 AI 응답")

            st.success(
                chat_data["ai_response"]
            )

            tts_text = chat_data["ai_response"]

            components.html(
                f"""
                <script>
                var msg = new SpeechSynthesisUtterance("{tts_text}");
                msg.lang = "ko-KR";
                msg.rate = 1.0;
                msg.pitch = 1.0;
                window.speechSynthesis.speak(msg);
                </script>
                """,
                height=0
            )
            st.write("### 😊 감정 분석")

            st.json(
                chat_data["emotion_analysis"]
            )
# ==========================================
# TAB 2
# ==========================================
with tab2:

    st.subheader("📊 감정 분석")

    if df.empty:

        st.warning(
            "감정 데이터가 없습니다."
        )

    else:

        # ------------------------------
        # 감정 통계
        # ------------------------------
        st.write("## 📈 감정 통계")

        avg_happy = round(
            df["happy"].mean(), 1
        )

        avg_stable = round(
            df["stable"].mean(), 1
        )

        avg_lonely = round(
            df["lonely"].mean(), 1
        )

        avg_anxiety = round(
            df["anxiety"].mean(), 1
        )

        avg_depressed = round(
            df["depressed"].mean(), 1
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "😊 행복",
                avg_happy
            )

        with col2:
            st.metric(
                "😌 안정",
                avg_stable
            )

        with col3:
            st.metric(
                "😔 외로움",
                avg_lonely
            )

        with col4:
            st.metric(
                "😟 불안",
                avg_anxiety
            )

        with col5:
            st.metric(
                "😢 우울",
                avg_depressed
            )

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
            f"🏆 가장 강하게 나타난 감정 : {top_emotion}"
        )

        # ------------------------------
        # 감정 그래프
        # ------------------------------
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

        # ------------------------------
        # 감정 캘린더
        # ------------------------------
        st.write("## 🗓 감정 캘린더")

        calendar_data = []

        for _, row in df.iterrows():

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

                "상태": emoji_map[
                    dominant_emotion
                ]
            })

        calendar_df = pd.DataFrame(
            calendar_data
        )

        st.dataframe(
            calendar_df,
            use_container_width=True
        )

        # ------------------------------
        # 위험 감지
        # ------------------------------
        st.write("## 🚨 감정 위험 감지")

        recent_data = df.tail(3)

        depressed_risk = all(

            score >= 70

            for score in recent_data[
                "depressed"
            ]
        )

        lonely_risk = all(

            score >= 70

            for score in recent_data[
                "lonely"
            ]
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
# TAB 3
# ==========================================
with tab3:

    st.subheader("📄 감정 보고서")

    try:

        report_response = requests.get(
               f"{API_URL}/emotion-report"
        )

        report_data = report_response.json()

    except:

        report_data = {
            "report": "감정 리포트를 불러올 수 없습니다."
        }

    st.write("## 🤖 AI 감정 리포트")

    st.info(
        report_data["report"]
    )

    st.write("---")

    st.write("## 📄 PDF 보고서")

    pdf_path = "reports/emotion_report.pdf"

    if st.button(
        "PDF 생성",
        key="pdf_create"
    ):

        try:

            requests.get(
                f"{API_URL}/emotion-pdf-report"
            )

            st.success(
                "PDF 생성 완료!"
            )

        except:

            st.error(
                "PDF 생성 실패"
            )

    if os.path.exists(pdf_path):

        with open(
            pdf_path,
            "rb"
        ) as file:

            st.download_button(

                label="📥 PDF 다운로드",

                data=file,

                file_name="emotion_report.pdf",

                mime="application/pdf"
            )

    else:

        st.warning(
            "생성된 PDF가 없습니다."
        )

    st.write("---")

    st.write("## 😊 최근 감정 상태")

    if latest is not None:

        st.write(
            f"📅 날짜 : {latest['date']}"
        )

        st.write(
            f"😊 행복 : {latest['happy']}"
        )

        st.write(
            f"😌 안정 : {latest['stable']}"
        )

        st.write(
            f"😔 외로움 : {latest['lonely']}"
        )

        st.write(
            f"😟 불안 : {latest['anxiety']}"
        )

        st.write(
            f"😢 우울 : {latest['depressed']}"
        )

        if latest["depressed"] >= 70:

            st.error(
                "🔴 우울 감정이 높습니다."
            )

        elif latest["lonely"] >= 70:

            st.warning(
                "🟠 외로움 감정이 높습니다."
            )

        else:

            st.success(
                "🟢 전반적으로 안정적인 상태입니다."
            )

    else:

        st.warning(
            "감정 데이터가 없습니다."
        )