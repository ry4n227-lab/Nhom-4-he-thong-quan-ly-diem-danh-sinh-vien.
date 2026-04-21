
import customtkinter as ctk
from tkinter import messagebox
import datetime

# 1. KẾT NỐI BACKEND
try:
    from src.controllers.attendance_controller import save_attendance_data
except ImportError:
    print("Lỗi: Không tìm thấy attendance_controller.py")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class TeacherDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Teacher Dashboard")
        self.geometry("750x750")
        self.eval('tk::PlaceWindow . center')

        ctk.CTkLabel(self, text="TEACHER DASHBOARD", font=("Arial", 22, "bold")).pack(pady=10)

        # ==========================================
        # PHẦN 1: TẠO BUỔI ĐIỂM DANH (CREATE SESSION)
        # ==========================================
        session_frame = ctk.CTkFrame(self, fg_color="transparent")
        session_frame.pack(pady=5, fill="x", padx=20)

        ctk.CTkLabel(session_frame, text="1. Create Attendance Session", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        
        # Chọn lớp học
        ctk.CTkLabel(session_frame, text="Select Class:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.cb_class = ctk.CTkComboBox(session_frame, values=["1 - INT1340 (Python)", "2 - INT1339 (Database)"], width=200)
        self.cb_class.grid(row=1, column=1, padx=10, pady=5)

        # Nhập ngày giờ (Tự động lấy giờ hiện tại làm gợi ý)
        ctk.CTkLabel(session_frame, text="Start Time (YYYY-MM-DD HH:MM):", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.entry_datetime = ctk.CTkEntry(session_frame, width=200)
        self.entry_datetime.insert(0, now_str)
        self.entry_datetime.grid(row=2, column=1, padx=10, pady=5)

        # THÊM MỚI: Nhập thời lượng điểm danh
        ctk.CTkLabel(session_frame, text="Duration (Minutes):", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_duration = ctk.CTkEntry(session_frame, width=200)
        self.entry_duration.insert(0, "10") # Mặc định 10 phút
        self.entry_duration.grid(row=3, column=1, padx=10, pady=5)

        # Nút Tạo ca điểm danh
        self.btn_create = ctk.CTkButton(session_frame, text="Tạo buổi điểm danh", font=("Arial", 14, "bold"), command=self.create_session)
        self.btn_create.grid(row=2, column=2, rowspan=2, padx=20, pady=5)

        # ==========================================
        # PHẦN 2: DANH SÁCH ĐIỂM DANH
        # ==========================================
        ctk.CTkLabel(self, text="2. Student List", font=("Arial", 16, "bold")).pack(pady=(10, 0), anchor="w", padx=20)
        
        # THÊM MỚI: Label hiển thị đếm ngược/thời gian đóng
        self.lbl_deadline = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 12, "italic"))
        self.lbl_deadline.pack()

        self.student_frame = ctk.CTkScrollableFrame(self, width=650, height=200)
        self.student_frame.pack(pady=5, padx=20, fill="x")

        self.student_ids = []
        self.status_vars = []

        self.btn_save = ctk.CTkButton(self, text="Save Attendance", command=self.save_attendance, font=("Arial", 14, "bold"), state="disabled")
        self.btn_save.pack(pady=10)

        # ==========================================
        # PHẦN 3: DUYỆT ĐƠN NGHỈ
        # ==========================================
        ctk.CTkLabel(self, text="Leave Requests", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        self.req_frame = ctk.CTkScrollableFrame(self, width=650, height=100)
        self.req_frame.pack(pady=5, padx=20, fill="x")
        self.requests = [
            {"student": "SV001", "reason": "Sick Leave"},
            {"student": "SV002", "reason": "Family Issue"}
        ]
        for req in self.requests:
            frame = ctk.CTkFrame(self.req_frame)
            frame.pack(pady=5, fill="x", padx=5)
            text = f"ID: {req['student']} | Lý do: {req['reason']}"
            ctk.CTkLabel(frame, text=text, font=("Arial", 14)).pack(side="left", padx=10, pady=10)
            ctk.CTkButton(frame, text="Reject", width=80, fg_color="#d9534f", hover_color="#c9302c", 
                          command=lambda r=req: self.handle_request(r, "Rejected")).pack(side="right", padx=5)
            ctk.CTkButton(frame, text="Approve", width=80,
                          command=lambda r=req: self.handle_request(r, "Approved")).pack(side="right", padx=5)

    # ================= LOGIC TẠO CA =================
    def create_session(self):
        for widget in self.student_frame.winfo_children():
            widget.destroy()
        self.student_ids.clear()
        self.status_vars.clear()

        class_selected = self.cb_class.get()
        dt_input = self.entry_datetime.get()
        duration_input = self.entry_duration.get()

        if not class_selected or not dt_input or not duration_input:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            # Lưu lại dt_obj để dùng cho lúc Save
            self.start_dt = datetime.datetime.strptime(dt_input, "%Y-%m-%d %H:%M")
            duration = int(duration_input)
            self.end_dt = self.start_dt + datetime.timedelta(minutes=duration)
            
            # Hiển thị giờ đóng form lên màn hình
            self.lbl_deadline.configure(text=f"Phiên điểm danh sẽ tự động khóa sau: {self.end_dt.strftime('%Y-%m-%d %H:%M')}")
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng thời gian hoặc thời lượng không hợp lệ!")
            return

        mock_students = [
            ("SV01", "Nguyễn Văn An"), 
            ("SV02", "Trần Thị Bình"), 
            ("SV03", "Lê Văn Cường")
        ]
        for sv_id, sv_name in mock_students:
            frame = ctk.CTkFrame(self.student_frame)
            frame.pack(pady=2, fill="x")
            ctk.CTkLabel(frame, text=f"{sv_id} - {sv_name}", font=("Arial", 14)).pack(side="left", padx=10, pady=5)
            var = ctk.StringVar(value="Present")
            self.student_ids.append(sv_id)
            self.status_vars.append(var)
            ctk.CTkOptionMenu(frame, values=["Present", "Absent", "Late"], variable=var).pack(side="right", padx=10)

        self.btn_save.configure(state="normal")
        messagebox.showinfo("Thành công", f"Đã mở ca điểm danh. Bạn có {duration} phút để hoàn thành.")

    # ================= LOGIC LƯU ĐIỂM DANH =================
    def save_attendance(self):
        if not self.student_ids:
            return
            
        # THÊM MỚI: Kiểm tra xem đã quá giờ quy định chưa?
        now = datetime.datetime.now()
        if now > self.end_dt:
            messagebox.showerror("Đã khóa", "Đã hết thời gian điểm danh! Hệ thống không cho phép lưu thay đổi.")
            self.btn_save.configure(state="disabled")
            return

        raw_class = self.cb_class.get()
        class_id = raw_class.split(' - ')[0].strip()
        
        start_time_str = self.start_dt.strftime("%Y-%m-%d %H:%M")
        end_time_str = self.end_dt.strftime("%Y-%m-%d %H:%M")

        attendance_list = [(self.student_ids[i], self.status_vars[i].get()) for i in range(len(self.student_ids))]
        try:
            # Truyền start_time và end_time sang Controller
            success, msg = save_attendance_data(class_id, start_time_str, end_time_str, attendance_list)
            if success:
                messagebox.showinfo("Thành công", msg)
                self.btn_save.configure(state="disabled") # Lưu thành công thì khóa nút
            else:
                messagebox.showerror("Lỗi Database", msg)
        except NameError:
            messagebox.showerror("Lỗi hệ thống", "Chưa kết nối được file Controller!")

    # ================= LOGIC DUYỆT ĐƠN =================
    def handle_request(self, request, status):
        messagebox.showinfo("Thông báo", f"Đã {status} đơn của {request['student']}")

if __name__ == "__main__":
    app = TeacherDashboard()
    app.mainloop()
