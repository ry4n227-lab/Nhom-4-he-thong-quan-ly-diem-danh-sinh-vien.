# File: src/controllers/student_controller.py
from .login_controller import get_db_connection

def get_attendance_history(student_id):
    """
    Lấy lịch sử điểm danh của một sinh viên từ Database.
    Trả về: (Trạng thái thành công, Lời nhắn, Danh sách dữ liệu)
    """
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database!", []

    try:
        cursor = conn.cursor()
        
        # Sửa lại tên bảng "attendance" cho khớp với XAMPP của nhóm
        sql = """
            SELECT date, status 
            FROM attendance 
            WHERE student_id = %s 
            ORDER BY date DESC
        """
        cursor.execute(sql, (student_id,))
        records = cursor.fetchall()
        
        return True, "Thành công", records

    except Exception as e:
        print("Lỗi lấy lịch sử điểm danh:", e)
        return False, f"Lỗi Database: {str(e)}", []
    finally:
        if conn.is_connected():
            conn.close()
