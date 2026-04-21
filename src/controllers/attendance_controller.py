from .login_controller import get_db_connection

# =====================
# Xử lý Điểm danh (UC 3 & 6)
# =====================
def save_attendance_data(class_id, date, attendance_list):
    """
    Nhận dữ liệu từ UI và lưu vào Database.
    
    Tham số:
    - class_id (str): Mã lớp học (VD: "INT1340")
    - date (str): Ngày điểm danh (VD: "2026-04-22")
    - attendance_list (list): Danh sách tuple chứa ID sinh viên và trạng thái
      VD: [("SV01", "Present"), ("SV02", "Absent"), ("SV03", "Late")]
      
    Trả về: (bool, str) -> (Trạng thái thành công, Lời nhắn)
    """
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi hệ thống: Không thể kết nối Database!"

    try:
        cursor = conn.cursor()
        
        # Câu lệnh SQL để chèn dữ liệu
        # (Giả định nhóm thiết kế DB có bảng Attendance với 4 cột này)
        sql = """
        INSERT INTO Attendance (class_id, date, student_id, status) 
        VALUES (%s, %s, %s, %s)
        """
        
        # Gom dữ liệu lại để chạy 1 lần cho tối ưu (tránh gọi INSERT nhiều lần)
        data_to_insert = []
        for student_id, status in attendance_list:
            data_to_insert.append((class_id, date, student_id, status))
            
        # Dùng executemany để nạp toàn bộ danh sách vào DB
        cursor.executemany(sql, data_to_insert)
        conn.commit()
        
        # cursor.rowcount sẽ đếm xem có bao nhiêu dòng đã được lưu thành công
        return True, f"Đã lưu thành công điểm danh cho {cursor.rowcount} sinh viên!"

    except Exception as e:
        print("Lỗi lưu điểm danh DB:", e)
        # Trường hợp sinh viên đã được điểm danh trong ngày hôm đó rồi (Lỗi trùng khóa chính)
        if "Duplicate entry" in str(e):
            return False, "Lỗi: Lớp này đã được điểm danh trong ngày hôm nay rồi!"
        return False, f"Lỗi Database: {str(e)}"
    finally:
        if conn.is_connected():
            conn.close()
