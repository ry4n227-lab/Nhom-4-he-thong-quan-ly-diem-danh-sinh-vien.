from .login_controller import get_db_connection

# =====================
# Kiểm tra trùng lịch (UC 13)
# =====================
def check_schedule_conflict(room, date, start_time, end_time):
    """
    Kiểm tra xem phòng học có bị trùng giờ vào ngày đó không.
    """
    conn = get_db_connection()
    if not conn:
        print("Lỗi kết nối DB khi check lịch.")
        return True # Trả về True để chặn không cho lưu nếu lỗi DB

    try:
        cursor = conn.cursor()
        
        # ĐÃ SỬA: Đổi tên bảng thành sessions
        sql = """
            SELECT * FROM sessions 
            WHERE room = %s AND date = %s 
            AND (
                (start_time <= %s AND end_time > %s) OR 
                (start_time < %s AND end_time >= %s) OR
                (start_time >= %s AND end_time <= %s)
            )
        """
        cursor.execute(sql, (room, date, start_time, start_time, end_time, end_time, start_time, end_time))
        
        conflict = cursor.fetchone()
        
        if conflict:
            return True # Có dòng dữ liệu trả về -> Bị trùng
        return False    # Không có dữ liệu -> Phòng trống

    except Exception as e:
        print("Lỗi truy vấn trùng lịch:", e)
        return True
    finally:
        if conn.is_connected():
            conn.close()


# =====================
# Lưu lịch học mới (UC 13)
# =====================
def save_new_schedule(class_id, date, start_time, end_time, room):
    """
    Lưu lịch học mới xuống Database (bảng sessions).
    """
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        
        # ĐÃ SỬA: Khớp 100% với các cột trong ảnh XAMPP của bạn
        sql = """
            INSERT INTO sessions (class_id, date, start_time, end_time, room) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (class_id, date, start_time, end_time, room))
        
        conn.commit()
        return True

    except Exception as e:
        # Bẫy lỗi Foreign Key (Nếu nhập mã môn học không tồn tại)
        if "foreign key constraint fails" in str(e).lower():
            print("LỖI KHÓA NGOẠI: Mã Môn Học không tồn tại trong bảng classes!")
            return False
        
        print("Lỗi lưu lịch học xuống DB:", e)
        return False
    finally:
        if conn.is_connected():
            conn.close()
