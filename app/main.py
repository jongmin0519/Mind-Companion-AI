# ==========================================
# FastAPI
# ==========================================
from fastapi import FastAPI

# ==========================================
# 환경 변수
# ==========================================
from dotenv import load_dotenv
import os

# ==========================================
# JSON 처리
# ==========================================
import json

# ==========================================
# Groq API
# ==========================================
from groq import Groq

# ==========================================
# DB 함수
# ==========================================
from app.database import (
    save_emotion_log,
    get_emotion_calendar,
    get_recent_emotions
)

from app.pdf_report import create_pdf_report
from app.database import save_emotion_log
#from app.tts import speak
from app.database import create_tables

create_tables()

# ==========================================
# .env 읽기
# ==========================================
load_dotenv()

# ==========================================
# API KEY
# ==========================================
api_key = os.getenv("GROQ_API_KEY")

# ==========================================
# Groq Client
# ==========================================
client = Groq(api_key=api_key)

# ==========================================
# FastAPI
# ==========================================
app = FastAPI()
from app.database import create_tables

create_tables()


# ==========================================
# 감정 분석
# ==========================================
def analyze_emotion(message):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0,

        messages=[
            {
                "role": "system",
                "content": """
당신은 감정 분석 AI입니다.

반드시 JSON 형식으로만 응답하세요.

{
    "happy": 10,
    "stable": 20,
    "lonely": 80,
    "anxiety": 30,
    "depressed": 90
}
"""
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    try:

        return json.loads(
            response.choices[0].message.content
        )

    except:

        return {
            "happy": 0,
            "stable": 0,
            "lonely": 0,
            "anxiety": 0,
            "depressed": 0
        }


# ==========================================
# AI 응답 생성
# ==========================================
def generate_response(message):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0.4,

        messages=[
            {
                "role": "system",
                "content": """
당신은 마음동행 AI입니다.

독거 어르신을 위한 말벗입니다.

규칙

1. 반드시 한국어만 사용
2. 영어 사용 절대 금지
3. 일본어 사용 절대 금지
4. 중국어 사용 절대 금지
5. 베트남어 사용 절대 금지
6. 외국어 단어가 포함되면 다시 한국어로 작성
7. 존댓말 사용
8. 답변은 3문장 이하
9. 공감을 먼저 표현
10. 마지막에는 질문 1개
"""
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content


# ==========================================
# AI 감정 리포트 생성
# ==========================================
def generate_emotion_report():

    data = get_recent_emotions()

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0.3,

        messages=[
            {
                "role": "system",
                "content": """
당신은 감정 분석 전문가입니다.

최근 감정 데이터를 분석하여

1. 현재 감정 상태
2. 위험 요소
3. 추천 행동

을 설명하세요.

반드시 한국어만 사용하세요.
5문장 이내로 작성하세요.
"""
            },
            {
                "role": "user",
                "content": str(data)
            }
        ]
    )

    return response.choices[0].message.content


# ==========================================
# 기본 페이지
# ==========================================
@app.get("/")
def root():

    return {
        "message": "Mind Companion AI"
    }


# ==========================================
# 채팅 API
# ==========================================
@app.get("/chat")
def chat(message: str):

    try:

        emotion_result = analyze_emotion(message)
        print("감정분석 결과:", emotion_result)
        ai_response = generate_response(message)

        save_emotion_log(
            user_message=message,

            happy=emotion_result.get("happy", 0),
            stable=emotion_result.get("stable", 0),
            lonely=emotion_result.get("lonely", 0),
            anxiety=emotion_result.get("anxiety", 0),
            depressed=emotion_result.get("depressed", 0),
            ai_response=ai_response
        )

        return {
            "user_message": message,
            "emotion_analysis": emotion_result,
            "ai_response": ai_response
        }

    except Exception as e:

        import traceback

        return {
            "error": str(e),
            "traceback": traceback.format_exc()
    }
# ==========================================
# 감정 캘린더 API
# ==========================================
@app.get("/emotion-calendar")
def emotion_calendar():

    data = get_emotion_calendar()

    return {

        "count": len(data),

        "data": data
    }


# ==========================================
# 감정 리포트 API
# ==========================================
@app.get("/emotion-report")
def emotion_report():

    data = get_recent_emotions()

    report = generate_emotion_report()

    return {

        "count": len(data),

        "data": data,

        "report": report
    }
# ==========================================
# PDF 보고서 생성 API
# ==========================================
@app.get("/pdf-report")
def pdf_report():

    report_text = generate_emotion_report()

    pdf_path = create_pdf_report(
        report_text
    )

    return {

        "message": "PDF 생성 완료",

        "file": pdf_path
    }