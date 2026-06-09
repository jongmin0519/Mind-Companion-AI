# ==========================================
# SQLite
# ==========================================
import sqlite3


# ==========================================
# DB 연결
# ==========================================
def get_connection():

    conn = sqlite3.connect(
        "mind_companion_ai.db",
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# 테이블 생성
# ==========================================
def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emotion_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_message TEXT,

            happy INTEGER,

            stable INTEGER,

            lonely INTEGER,

            anxiety INTEGER,

            depressed INTEGER,

            ai_response TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    conn.close()


# ==========================================
# 감정 저장
# ==========================================
def save_emotion_log(

    user_message,

    happy,

    stable,

    lonely,

    anxiety,

    depressed,

    ai_response

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO emotion_logs (

            user_message,

            happy,

            stable,

            lonely,

            anxiety,

            depressed,

            ai_response

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        user_message,

        happy,

        stable,

        lonely,

        anxiety,

        depressed,

        ai_response

    ))

    conn.commit()

    conn.close()


# ==========================================
# 감정 캘린더
# ==========================================
def get_emotion_calendar():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            DATE(created_at) as date,

            happy,

            stable,

            lonely,

            anxiety,

            depressed

        FROM emotion_logs

        ORDER BY created_at ASC

    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================
# 최근 감정 조회
# ==========================================
def get_recent_emotions():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            DATE(created_at) as date,

            happy,

            stable,

            lonely,

            anxiety,

            depressed

        FROM emotion_logs

        ORDER BY created_at DESC

        LIMIT 10

    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]