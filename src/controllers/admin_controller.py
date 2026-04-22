from .login_controller import get_db_connectio
def save_new_user_to_db(user_id, fullname, email, role, password):
    """
    Lưu tài khoản mới. 
    Tự động phân luồng lưu vào bảng teachers hoặc students dựa theo Role.
    """
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database! (Chưa bật XAMPP hoặc sai tên DB)"

    try:
        cursor = conn.cursor()
        
        if role == "Teacher":
            table_name = "teachers" 
            id_col = "teacher_id"
        elif role == "Student":
            table_name = "students" 
            id_col = "student_id"
        else:
            return False, "Vai trò (Role) không hợp lệ!"
       
        sql = f"""
            INSERT INTO {table_name} ({id_col}, full_name, email, password)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (user_id, fullname, email, password))
        
        conn.commit()
        return True, f"Thêm {role} ({user_id}) thành công vào hệ thống!"
        
    except Exception as e:
        if "Duplicate entry" in str(e):
            return False, f"Lỗi: Mã ID '{user_id}' đã tồn tại trong bảng {table_name}!"
        return False, f"Lỗi Database: {str(e)}"
    finally:
        if conn.is_connected():
            conn.close()

def save_new_course_to_db(course_id, course_name):
    """
    Lưu môn học mới vào bảng classes.
    """
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database!"

    try:
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO classes (class_id, class_name)
            VALUES (%s, %s)
        """
        cursor.execute(sql, (course_id, course_name))
        
        conn.commit()
        return True, f"Thêm môn học/lớp '{course_name}' thành công!"
        
    except Exception as e:
        if "Duplicate entry" in str(e):
            return False, f"Lỗi: Mã '{course_id}' đã tồn tại!"
        return False, f"Lỗi Database: {str(e)}"
    finally:
        if conn.is_connected():
            conn.close()
