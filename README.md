# 🧠 마음동행 AI (Mind Companion AI)

> AI와의 대화를 통해 감정을 기록하고 분석하여 독거 어르신의 정서 건강을 지원하는 감정 케어 플랫폼

---

## 📖 프로젝트 소개

마음동행 AI는 독거 어르신을 위한 AI 기반 감정 케어 서비스입니다.

사용자와의 대화를 통해 감정 상태를 분석하고, 장기간 데이터를 축적하여 감정 변화 추이와 정서 상태를 시각적으로 제공합니다.

단순한 챗봇이 아닌 **감정 추적 및 정서 관리 플랫폼**을 목표로 개발합니다.

---

## 🎯 프로젝트 목표

* 독거 어르신의 정서적 고립 완화
* AI 기반 자연스러운 말벗 서비스 제공
* 감정 데이터 장기 추적
* 감정 변화 시각화
* 우울감 및 외로움 위험 신호 탐지

---

## ✨ 주요 기능

### 💬 AI 말벗

* Groq API 기반 AI 대화
* 자연스러운 일상 대화 지원
* 사용자 맞춤형 대화 제공

### 😊 감정 분석

대화 내용을 분석하여

* 행복(Happy)
* 안정(Stable)
* 외로움(Lonely)
* 불안(Anxiety)
* 우울(Depressed)

점수를 산출합니다.

---

### 🌡 마음온도

감정 점수를 기반으로 현재 정서 상태를 온도로 표현합니다.

예시

* 80℃ 이상 : 매우 안정적
* 60~79℃ : 양호
* 40~59℃ : 관심 필요
* 39℃ 이하 : 정서 지원 권장

---

### 📅 감정 캘린더

날짜별 감정 상태를 기록하고 시각화합니다.

예시

🟢 행복

🟡 보통

🟠 외로움

🔴 우울

---

### 📈 감정 그래프

* 최근 7일
* 최근 30일
* 최근 90일

감정 변화 추이를 그래프로 제공합니다.

---

### 📋 감정 리포트

AI가 감정 패턴을 분석하여 요약 리포트를 생성합니다.

예시

* 행복도 증가
* 외로움 감소
* 정서 상태 양호

---

### 🚨 위험 신호 탐지

다음과 같은 상황 발생 시 알림 생성

* 우울 점수 지속 증가
* 외로움 점수 급상승
* 부정 감정 장기 지속

---

## 🏗 시스템 아키텍처

User

↓

Frontend

↓

FastAPI

↓

Groq API

↓

Emotion Analysis

↓

MySQL

↓

Calendar / Graph / Report

---

## 🛠 기술 스택

### Backend

* Python
* FastAPI

### AI

* Groq API
* Llama Model

### Database

* MySQL

### Visualization

* Plotly

### Frontend

* Streamlit

### Deployment

* Docker
* AWS EC2

---

## 🗄 데이터베이스 구조

### users

| Column     | Type     |
| ---------- | -------- |
| user_id    | BIGINT   |
| name       | VARCHAR  |
| birth      | DATE     |
| gender     | VARCHAR  |
| created_at | DATETIME |

### conversations

| Column          | Type     |
| --------------- | -------- |
| conversation_id | BIGINT   |
| user_id         | BIGINT   |
| user_message    | TEXT     |
| ai_response     | TEXT     |
| created_at      | DATETIME |

### emotion_logs

| Column       | Type     |
| ------------ | -------- |
| emotion_id   | BIGINT   |
| user_id      | BIGINT   |
| happy        | INT      |
| stable       | INT      |
| lonely       | INT      |
| anxiety      | INT      |
| depressed    | INT      |
| emotion_temp | FLOAT    |
| created_at   | DATETIME |

---

## 🚀 개발 로드맵

### Phase 1

* [ ] 프로젝트 환경 구축
* [ ] FastAPI 세팅
* [ ] MySQL 연동

### Phase 2

* [ ] Groq API 연동
* [ ] AI 채팅 기능 구현
* [ ] 대화 저장 기능

### Phase 3

* [ ] 감정 분석 기능 구현
* [ ] 마음온도 계산 기능

### Phase 4

* [ ] 감정 캘린더 구현
* [ ] 감정 그래프 구현

### Phase 5

* [ ] 감정 리포트 생성
* [ ] 위험 신호 탐지

### Phase 6

* [ ] Docker 컨테이너화
* [ ] AWS 배포

---

## 📌 향후 계획

* 음성 인식(STT)
* 음성 출력(TTS)
* 회상 치료 모드
* 보호자 대시보드
* AI 기반 감정 예측 기능

---

## 👨‍💻 Developer

강종민

동양미래대학교 컴퓨터소프트웨어공학과 졸업

관심 분야

* AI
* Cloud
* Information Security
* Welfare Technology
