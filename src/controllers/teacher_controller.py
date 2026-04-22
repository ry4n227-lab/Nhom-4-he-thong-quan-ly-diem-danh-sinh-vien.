from .login_controller import get_db_connection

# =====================
# 1. Lấy danh sách lớp của Giáo viên
# =====================
def get_teacher_classes(teacher_id):
    """Lấy các lớp học mà giáo viên này được phân công trong bảng classes"""
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database!", []

    try:
        cursor = conn.cursor()
        # Truy vấn tìm các lớp có mã giáo viên tương ứng
        sql = "SELECT class_id, class_name FROM classes WHERE teacher_id = %s"
        cursor.execute(sql, (teacher_id,))
        records = cursor.fetchall()
        
        return True, "Thành công", records
    except Exception as e:
        print("Lỗi lấy danh sách lớp:", e)
        return False, f"Lỗi DB: {str(e)}", []
    finally:
        if conn.is_connected():
            conn.close()

# =====================
# 2. Lấy danh sách Sinh viên
# =====================
def get_class_students(class_id):
    """Lấy danh sách sinh viên trong lớp"""
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database!", []

    try:
        cursor = conn.cursor()
        # LƯU Ý: Hiện tại lấy toàn bộ sinh viên trong bảng students.
        # Nếu nhóm bạn có bảng riêng (như enrollments) để chia sinh viên theo lớp thì sửa câu SQL ở đây nhé!
        sql = "SELECT student_id, full_name FROM students"
        cursor.execute(sql)
        records = cursor.fetchall()
        
        return True, "Thành công", records
    except Exception as e:
        print("Lỗi lấy danh sách sinh viên:", e)
        return False, f"Lỗi DB: {str(e)}", []
    finally:
        if conn.is_connected():
            conn.close()

# 3. Lưu / Cập nhật Điểm danh
# =====================
def save_attendance_data(class_id, date, attendance_list):
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database!"

    try:
        cursor = conn.cursor()
        
        # BƯỚC 1: Dọn dẹp dữ liệu cũ (Xóa điểm danh cũ của lớp này trong ngày hôm nay)
        # Điều này giúp giáo viên có thể bấm Save nhiều lần để cập nhật lại điểm danh
        delete_sql = "DELETE FROM attendance WHERE class_id = %s AND date = %s"
        cursor.execute(delete_sql, (class_id, date))

        # BƯỚC 2: Lưu dữ liệu mới vào
        insert_sql = """
            INSERT INTO attendance (class_id, date, student_id, status) 
            VALUES (%s, %s, %s, %s)
        """
        data_to_insert = []
        for student_id, status in attendance_list:
            data_to_insert.append((class_id, date, student_id, status))
            
        cursor.executemany(insert_sql, data_to_insert)
        
        conn.commit()
        return True, f"Đã lưu/cập nhật điểm danh cho {cursor.rowcount} sinh viên!"

    except Exception as e:
        print("Lỗi chi tiết khi lưu điểm danh:", e)
        return False, f"Lỗi Database: {str(e)}"
    finally:
        if conn.is_connected():
            conn.close()
# =====================
# 4. Lấy Đơn xin nghỉ phép (Có Tên Sinh viên)
# =====================
def get_leave_requests():
    """Lấy đơn xin nghỉ kết hợp (JOIN) với bảng students để lấy Tên"""
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database!", []

    try:
        cursor = conn.cursor()
        # Nối bảng leave_requests và bảng students thông qua cột student_id
        sql = """
            SELECT lr.request_id, lr.student_id, s.full_name, lr.reason, lr.date 
            FROM leave_requests lr
            JOIN students s ON lr.student_id = s.student_id
            WHERE lr.status = 'Pending'
        """
        cursor.execute(sql)
        return True, "Thành công", cursor.fetchall()
    except Exception as e:
        # Nếu chưa tạo bảng leave_requests thì trả về mảng rỗng để app không bị crash
        if "doesn't exist" in str(e).lower():
            return False, "Chưa tạo bảng leave_requests", []
        return False, f"Lỗi DB: {str(e)}", []
    finally:
        if conn.is_connected():
            conn.close()
