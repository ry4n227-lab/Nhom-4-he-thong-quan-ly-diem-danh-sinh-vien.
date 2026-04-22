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

from .login_controller import get_db_connection # Tận dụng lại hàm kết nối DB

# =====================
# Hàm gửi đơn xin nghỉ cho Sinh viên
# =====================
def submit_leave_request(student_id, reason, date):
    conn = get_db_connection()
    if not conn:
        return False, "Lỗi kết nối Database!"

    try:
        cursor = conn.cursor()
        
        # Lệnh SQL Insert dữ liệu (Mặc định status là 'Pending')
        sql = """
            INSERT INTO leave_requests (student_id, reason, date, status) 
            VALUES (%s, %s, %s, 'Pending')
        """
        
        # Thực thi lệnh
        cursor.execute(sql, (student_id, reason, date))
        
        # BƯỚC QUAN TRỌNG NHẤT: CHỐT SỔ (LƯU VĨNH VIỄN) VÀO DATABASE
        conn.commit() 
        
        return True, "Đã gửi đơn xin nghỉ thành công! Vui lòng chờ Giảng viên duyệt."
        
    except Exception as e:
        # Nếu có lỗi (ví dụ sai tên bảng, sai cột) thì In ra để biết đường sửa
        print("Lỗi khi nộp đơn:", e)
        return False, f"Lỗi Database: {str(e)}"
    finally:
        # Nhớ đóng cửa khi ra về
        if conn.is_connected():
            conn.close()
