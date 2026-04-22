from .login_controller import get_db_connection

def check_schedule_conflict(room, date, start_time, end_time):
    """
    Kiểm tra xem phòng học có bị trùng giờ vào ngày đó không.
    """
    conn = get_db_connection()
    if not conn:
        print("Lỗi kết nối DB khi check lịch.")
        return True 

    try:
        cursor = conn.cursor()

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
            return True 
        return False    
    except Exception as e:
        print("Lỗi truy vấn trùng lịch:", e)
        return True
    finally:
        if conn.is_connected():
            conn.close()


def save_new_schedule(class_id, date, start_time, end_time, room):
    """
    Lưu lịch học mới xuống Database (bảng sessions).
    """
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        
      
        sql = """
            INSERT INTO sessions (class_id, date, start_time, end_time, room) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (class_id, date, start_time, end_time, room))
        
        conn.commit()
        return True

    except Exception as e:
       
        if "foreign key constraint fails" in str(e).lower():
            print("LỖI KHÓA NGOẠI: Mã Môn Học không tồn tại trong bảng classes!")
            return False
        
        print("Lỗi lưu lịch học xuống DB:", e)
        return False
    finally:
        if conn.is_connected():
            conn.close()
