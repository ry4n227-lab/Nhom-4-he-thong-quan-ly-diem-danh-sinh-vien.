from .login_controller import get_db_connection

# =====================
# Xử lý Điểm danh (UC 3 & 6)
# =====================
def save_attendance_data(class_id, date, attendance_list):
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database! (Chưa bật XAMPP hoặc sai tên DB)"

    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO attendance (class_id, date, student_id, status) 
        VALUES (%s, %s, %s, %s)
        """
        
        # Gom dữ liệu lại để chạy 1 lần cho tối ưu
        data_to_insert = []
        for student_id, status in attendance_list:
            data_to_insert.append((class_id, date, student_id, status))
            
        # Dùng executemany để nạp toàn bộ danh sách (cả chục sinh viên) vào DB cùng lúc
        cursor.executemany(sql, data_to_insert)
        
        # LỆNH CỐT LÕI: Phải commit thì XAMPP mới nhận dữ liệu
        conn.commit()
        
        # cursor.rowcount đếm số dòng vừa được lưu
        return True, f"Đã lưu thành công điểm danh cho {cursor.rowcount} sinh viên!"

    except Exception as e:
        print("Lỗi lưu điểm danh DB:", e)
        # Bắt lỗi trùng lặp (nếu sinh viên đó đã được điểm danh trong ngày)
        if "Duplicate entry" in str(e):
            return False, "Lỗi: Lớp này đã được điểm danh trong ngày hôm nay rồi!"
        # Bắt lỗi sai kiểu dữ liệu (VD: nhét chữ vào cột số)
        if "Incorrect integer value" in str(e):
            return False, "Lỗi: Sai kiểu dữ liệu Mã lớp hoặc Mã SV! Vui lòng check lại UI."
            
        return False, f"Lỗi Database: {str(e)}"
    finally:
        if conn.is_connected():
            conn.close()
