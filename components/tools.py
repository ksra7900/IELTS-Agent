from components import values
import mysql.connector
from openai import OpenAI
import streamlit as st

def connect_to_DB():
    return mysql.connector.connect(
        host=values.host,
        user=values.user,
        password=values.password,
        database=values.DB_name
        )

def register_user(username, password, name):
    conn = connect_to_DB()
    cursor = conn.cursor()

    try:
        user_query = """
        INSERT INTO users (username, name, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(user_query, (username, name, password))
        user_id = cursor.lastrowid

        report_query = """
        INSERT INTO reports (`User-ID`, writing_report, speaking_report)
        VALUES (%s, %s, %s)
        """

        cursor.execute(report_query, (user_id, "", ""))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        st.error(f"Registration error: {e}")
        return False

    finally:
        cursor.close()
        conn.close()


def login_user(username, password):
    conn = connect_to_DB()
    cursor = conn.cursor()

    try:
        query = """
        SELECT `User-ID`, username, name
        FROM users
        WHERE username = %s AND password = %s
        """

        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return {
                "user_id": user[0],
                "username": user[1],
                "name": user[2]
            }

        return None

    except Exception as e:
        st.error(f"Login error: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

def get_writing_report(user_id):
    conn = connect_to_DB()
    cursor = conn.cursor()

    try:
        query = """
        SELECT writing_report
        FROM reports
        WHERE `User-ID` = %s
        """

        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result and result[0]:
            return result[0]

        return ""

    except Exception as e:
        st.error(f"Error loading writing report: {e}")
        return ""

    finally:
        cursor.close()
        conn.close()
        
def update_writing_report(user_id, new_report):
    if not user_id:
        st.error("User ID is missing. Please log in again.")
        return False

    conn = connect_to_DB()
    cursor = conn.cursor()

    try:
        update_query = """
        UPDATE reports
        SET writing_report = %s
        WHERE `User-ID` = %s
        """

        cursor.execute(update_query, (new_report, user_id))

        if cursor.rowcount == 0:
            insert_query = """
            INSERT INTO reports (`User-ID`, writing_report, speaking_report)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, new_report, ""))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        st.error(f"Error updating writing report: {e}")
        return False

    finally:
        cursor.close()
        conn.close()

def load_API():
    try:
        client = OpenAI(
            base_url="https://arvancloudai.ir/gateway/models/Qwen3-30B-A3B/K3DscMU8Egy5OVcYj7NlGJG9PR6NWL6qbEzrNa9NRGnQFaI8XMzNHu9FVoojHC4FoeH3zpYe-tO_cMI6eovMQtT-xLbzkivsduP7JHJ0mATuuRIPRZW-bvdAcPCuCHANZ6YQ8o5ahjWsx_QV7Il3SYhp1eCBNbHj46IqIGMDzNcVG5sDFMk7fo2YRjeWuFnG0EAhDZX2ZOKBKHOpJE57gLQCxxNw4dP1NZQxSfVb-ibYaFWinN9wn2a3fhtTTpH6/v1", 
            api_key=st.secrets["OPENAI_API_KEY"]
        )
    except KeyError:
        st.error("OpenAI API key not found. Please add it to your Streamlit secrets.")
        client = None
        
    return client