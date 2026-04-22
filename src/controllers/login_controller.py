import mysql.connector

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="attendance_db"
        )
    except Exception as e:
        print("DB Connection Error:", e)
        return None


def verify_login(user_id, password, role):
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        
        if role == 'Admin':
            id_col = 'username'
        elif role == 'Teachers':
            id_col = 'teacher_id'
        elif role == 'Students':
            id_col = 'student_id'
        else:
            return False

        sql = f"SELECT * FROM {role} WHERE {id_col} = %s AND password = %s"
        cursor.execute(sql, (user_id, password))
        
        if cursor.fetchone():
            return True
        return False

    except Exception as e:
        print("Login Query Error:", e)
        return False
    finally:
        if conn.is_connected():
            conn.close()
