from .login_controller import get_db_connection

# =====================
# Quản lý Tài khoản (UC 11)
# =====================
def save_new_user_to_db(user_id, fullname, email, role, password):
    """
    Lưu tài khoản mới. 
    Tự động phân luồng lưu vào bảng Teachers hoặc Students dựa theo Role.
    """
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database! (Chưa bật XAMPP hoặc sai tên DB)"

    try:
        cursor = conn.cursor()
        
        # Phân luồng bảng dựa theo Dropdown của UI
        # Lưu ý: Cấu trúc này khớp với logic Login (chia bảng) của bạn
        if role == "Teacher":
            table_name = "Teachers"
            id_col = "teacher_id"
        elif role == "Student":
            table_name = "Students"
            id_col = "student_id"
        else:
            return False, "Vai trò (Role) không hợp lệ!"

        # Câu lệnh SQL chèn dữ liệu
        # BẠN NHỚ NHẮC QUYÊN ĐẢM BẢO XAMPP CÓ CÁC CỘT NÀY NHÉ!
        sql = f"""
            INSERT INTO {table_name} ({id_col}, fullname, email, password)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (user_id, fullname, email, password))
        
        # Bắt buộc phải commit để XAMPP lưu thật
        conn.commit()
        return True, f"Thêm {role} ({user_id}) thành công vào hệ thống!"
        
    except Exception as e:
        if "Duplicate entry" in str(e):
            return False, f"Lỗi: Mã ID '{user_id}' đã tồn tại trong bảng {table_name}!"
        return False, f"Lỗi Database: {str(e)}"
    finally:
        if conn.is_connected():
            conn.close()


# =====================
# Quản lý Môn học (UC 12)
# =====================
def save_new_course_to_db(course_id, course_name):
    """
    Lưu môn học mới vào bảng Courses.
    """
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database!"

    try:
        cursor = conn.cursor()
        
        # Giả định bạn Quyên tạo bảng môn học tên là `Courses`
        sql = """
            INSERT INTO Courses (course_id, course_name)
            VALUES (%s, %s)
        """
        cursor.execute(sql, (course_id, course_name))
        
        conn.commit()
        return True, f"Thêm môn học '{course_name}' thành công!"
        
    except Exception as e:
        if "Duplicate entry" in str(e):
            return False, f"Lỗi: Mã môn '{course_id}' đã tồn tại!"
        return False, f"Lỗi Database: {str(e)}"
    finally:
        if conn.is_connected():
            conn.close()
