# ==========================================
# MySQL 연결 라이브러리
# ==========================================
import mysql.connector


# ==========================================
# DB 연결
# ==========================================
def get_connection():

    return mysql.connector.connect(

        host="localhost",

        user="root",

        password="1234",

        database="mind_companion_ai"
    )


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

    connection = get_connection()

    cursor = connection.cursor()

    query = """
    INSERT INTO emotion_logs
    (
        user_message,
        happy,
        stable,
        lonely,
        anxiety,
        depressed,
        ai_response
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s
    )
    """

    values = (
        user_message,
        happy,
        stable,
        lonely,
        anxiety,
        depressed,
        ai_response
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


# ==========================================
# 감정 캘린더 조회
# ==========================================
def get_emotion_calendar():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT

        DATE(created_at) AS date,

        happy,
        stable,
        lonely,
        anxiety,
        depressed

    FROM emotion_logs

    ORDER BY created_at DESC
    """

    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


# ==========================================
# 최근 감정 데이터 조회
# ==========================================
def get_recent_emotions():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT

        DATE(created_at) AS date,

        happy,
        stable,
        lonely,
        anxiety,
        depressed

    FROM emotion_logs

    ORDER BY created_at DESC

    LIMIT 7
    """

    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result