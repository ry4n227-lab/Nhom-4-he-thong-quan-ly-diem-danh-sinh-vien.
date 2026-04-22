import customtkinter as ctk
from tkinter import messagebox
import datetime

try:
    from src.controllers.teacher_controller import (
        update_leave_request_status,
        get_teacher_classes, get_class_students, 
        save_attendance_data, get_leave_requests
    )
except ImportError:
    print("Cảnh báo: Chưa tìm thấy file teacher_controller.py")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class TeacherDashboard(ctk.CTk):
    def __init__(self, teacher_id="T01"):
        super().__init__()
        self.teacher_id = teacher_id
        self.title("Teacher Dashboard")
        self.geometry("750x650")
        self.eval('tk::PlaceWindow . center')

        # ĐÃ XÓA NÚT ĐĂNG XUẤT Ở ĐÂY

        ctk.CTkLabel(self, text="TEACHER DASHBOARD", font=("Arial", 22, "bold")).pack(pady=10)

        # ==========================================
        # 1. TẠO BUỔI ĐIỂM DANH (CREATE SESSION)
        # ==========================================
        session_frame = ctk.CTkFrame(self, fg_color="transparent")
        session_frame.pack(pady=5, fill="x", padx=20)

        ctk.CTkLabel(session_frame, text="1. Create Attendance Session", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        ctk.CTkLabel(session_frame, text="Select Class:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        
        self.cb_class = ctk.CTkComboBox(session_frame, values=["Đang tải..."], width=200)
        self.cb_class.grid(row=1, column=1, padx=10, pady=5)

        self.btn_create = ctk.CTkButton(session_frame, text="Tạo buổi điểm danh", font=("Arial", 14, "bold"), command=self.create_session)
        self.btn_create.grid(row=1, column=2, padx=20, pady=5)

        # ==========================================
        # 2. DANH SÁCH ĐIỂM DANH (TAKE ATTENDANCE)
        # ==========================================
        ctk.CTkLabel(self, text="2. Student List", font=("Arial", 16, "bold")).pack(pady=(15, 5), anchor="w", padx=20)

        self.student_frame = ctk.CTkScrollableFrame(self, width=650, height=200)
        self.student_frame.pack(pady=5, padx=20, fill="x")

        self.student_ids = []
        self.status_vars = []

        self.btn_save = ctk.CTkButton(self, text="Save Attendance", command=self.save_attendance, font=("Arial", 14, "bold"), state="disabled")
        self.btn_save.pack(pady=10)

        # ==========================================
        # 3. DUYỆT ĐƠN (LEAVE REQUESTS)
        # ==========================================
        ctk.CTkLabel(self, text="Leave Requests", font=("Arial", 16, "bold")).pack(pady=(10, 5))

        self.req_frame = ctk.CTkScrollableFrame(self, width=650, height=130)
        self.req_frame.pack(pady=5, padx=20, fill="x")

        # Gọi hàm load dữ liệu ban đầu
        self.load_classes_from_db()
        self.load_leave_requests()

    # ================= CÁC HÀM XỬ LÝ DỮ LIỆU =================

    def load_classes_from_db(self):
        success, msg, classes = get_teacher_classes(self.teacher_id)
        if success and classes:
            class_values = [f"{c[0]} - {c[1]}" for c in classes]
            self.cb_class.configure(values=class_values)
            self.cb_class.set(class_values[0])
        else:
            self.cb_class.configure(values=["Chưa có lớp được phân công"])
            self.cb_class.set("Chưa có lớp được phân công")

    def load_leave_requests(self):
        success, msg, requests = get_leave_requests()
        
        if not success:
            ctk.CTkLabel(self.req_frame, text=f"Lỗi: {msg}", text_color="red").pack()
            return
            
        if not requests:
            ctk.CTkLabel(self.req_frame, text="Không có đơn xin nghỉ nào cần duyệt.", text_color="gray").pack()
            return

        for req in requests:
            req_id, sv_id, sv_name, reason, date = req
            frame = ctk.CTkFrame(self.req_frame)
            frame.pack(pady=5, fill="x", padx=5)

            text = f"[{date}] {sv_id} - {sv_name} | Lý do: {reason}"
            ctk.CTkLabel(frame, text=text, font=("Arial", 13)).pack(side="left", padx=10, pady=10)

            ctk.CTkButton(frame, text="Reject", width=60, fg_color="#d9534f", hover_color="#c9302c", 
                          command=lambda r=req_id: self.handle_request(r, "Rejected")).pack(side="right", padx=5)
            ctk.CTkButton(frame, text="Approve", width=60,
                          command=lambda r=req_id: self.handle_request(r, "Approved")).pack(side="right", padx=5)

    def create_session(self):
        class_selected = self.cb_class.get()
        if "Chưa có lớp" in class_selected:
            messagebox.showwarning("Cảnh báo", "Bạn chưa có lớp học nào để điểm danh!")
            return

        class_id = class_selected.split(' - ')[0].strip()
        success, msg, students = get_class_students(class_id)

        if not success:
            messagebox.showerror("Lỗi", msg)
            return

        for widget in self.student_frame.winfo_children():
            widget.destroy()
        self.student_ids.clear()
        self.status_vars.clear()

        for sv_id, sv_name in students:
            frame = ctk.CTkFrame(self.student_frame)
            frame.pack(pady=2, fill="x")

            ctk.CTkLabel(frame, text=f"{sv_id} - {sv_name}", font=("Arial", 14)).pack(side="left", padx=10, pady=5)

            var = ctk.StringVar(value="Present")
            self.student_ids.append(sv_id)
            self.status_vars.append(var)

            ctk.CTkOptionMenu(frame, values=["Present", "Absent", "Late"], variable=var).pack(side="right", padx=10)

        self.btn_save.configure(state="normal")
        messagebox.showinfo("Thành công", f"Đã mở ca điểm danh cho {len(students)} sinh viên!")

    def save_attendance(self):
        if not self.student_ids:
            return

        raw_class = self.cb_class.get()
        class_id = raw_class.split(' - ')[0].strip() 
        today = datetime.date.today().strftime('%Y-%m-%d')
        
        attendance_list = []
        for i in range(len(self.student_ids)):
            sv_id = self.student_ids[i]
            status = self.status_vars[i].get()
            attendance_list.append((sv_id, status))

        success, msg = save_attendance_data(class_id, today, attendance_list)
        if success:
            messagebox.showinfo("Thành công", msg)
        else:
            messagebox.showerror("Lỗi Database", msg)

  def handle_request(self, req_id, status):
        # 1. Gọi xuống Database để cập nhật thật
        success, msg = update_leave_request_status(req_id, status)
        
        if success:
            messagebox.showinfo("Thành công", f"Đã {status} đơn số {req_id}")
            
            # 2. Xóa sạch các đơn cũ đang hiển thị trên màn hình
            for widget in self.req_frame.winfo_children():
                widget.destroy()
                
            # 3. Tải lại danh sách đơn (những đơn Pending còn lại)
            self.load_leave_requests()
        else:
            messagebox.showerror("Lỗi Database", msg)

if __name__ == "__main__":
    app = TeacherDashboard()
    app.mainloop()
