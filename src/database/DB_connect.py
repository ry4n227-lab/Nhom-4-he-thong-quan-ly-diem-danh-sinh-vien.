import mysql.connector

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",  
            database="attendance_db"
        )
    except Exception as e:
        print("❌ Lỗi kết nối DB:", e)
        return None

def get_students():
    conn = connect_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students")

        rows = cursor.fetchall()
        print("\n📋 Danh sách sinh viên:")

        for row in rows:
            print(f"ID: {row[0]} | Tên: {row[1]} | Email: {row[2]} | Lớp: {row[3]}")

    except Exception as e:
        print("❌ Lỗi:", e)

    finally:
        if conn.is_connected():
            conn.close()

def add_student(student_id, full_name, email, class_id):
    conn = connect_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM Students WHERE student_id = %s", (student_id,))
        if cursor.fetchone():
            return

        sql = """
        INSERT INTO Students (student_id, full_name, email, class_id)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (student_id, full_name, email, class_id))
        conn.commit()

        print("✅ Thêm sinh viên thành công")

    except Exception as e:
        print("❌ Lỗi:", e)

    finally:
        if conn.is_connected():
            conn.close()

def delete_student(student_id):
    conn = connect_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        sql = "DELETE FROM Students WHERE student_id = %s"
        cursor.execute(sql, (student_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print("🗑️ Xóa thành công")

    except Exception as e:
        print("❌ Lỗi:", e)

    finally:
        if conn.is_connected():
            conn.close()

def update_student(student_id, new_name, new_email, new_class):
    conn = connect_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        sql = """
        UPDATE Students
        SET full_name = %s, email = %s, class_id = %s
        WHERE student_id = %s
        """

        cursor.execute(sql, (new_name, new_email, new_class, student_id))
        conn.commit()

        if cursor.rowcount > 0:
            print("✏️ Cập nhật thành công")

    except Exception as e:
        print("❌ Lỗi:", e)

    finally:
        if conn.is_connected():
            conn.close()

# =====================
# CHECK LOGIN
# =====================
def check_login(user_id, password, role):
    conn = connect_db()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        if role == 'Admin':
            id_column = 'username'
        elif role == 'Teachers':
            id_column = 'teacher_id'
        elif role == 'Students':
            id_column = 'student_id'
        else:
            return False

        sql = f"SELECT * FROM {role} WHERE {id_column} = %s AND password = %s"
        cursor.execute(sql, (user_id, password))

        if cursor.fetchone():
            return True
        return False

    except Exception as e:
        print("❌ Lỗi:", e)
        return False

    finally:
        if conn.is_connected():
            conn.close()

# =====================
# CHECK SCHEDULE
# =====================
def check_schedule_conflict(room, date, start_time, end_time):
    conn = connect_db()
    if conn is None:
        return True

    try:
        cursor = conn.cursor()

        sql = """
        SELECT 1 FROM Sessions 
        WHERE room = %s AND date = %s 
        AND NOT (end_time <= %s OR start_time >= %s)
        """
        cursor.execute(sql, (room, date, end_time, start_time))

        if cursor.fetchone():
            return True
        return False

    except Exception as e:
        print("❌ Lỗi:", e)
        return True

    finally:
        if conn.is_connected():
            conn.close()

# Test chức năng
if __name__ == "__main__":
#Thêm
    add_student("SV05", "Tran T", "ttran@gmail.com", 1)
    
#Update
    update_student("SV05", "Tran T", "ttran@gmail.com", 1)
    
#Xoá
    delete_student("SV05")
    
#Xem ds
    get_students()
    
#Check login
    print("Login Admin:", check_login("admin", "123456", "Admin"))

#Check schedule
    print("Conflict:", check_schedule_conflict("A101", "2026-04-22", "09:00:00", "11:00:00"))
