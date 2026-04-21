import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ==========================================
# IMPORT TOÀN BỘ CONTROLLER BACKEND
# ==========================================
try:
    from src.controllers.admin_controller import save_new_user_to_db, save_new_course_to_db
    from src.controllers.schedule_controller import check_schedule_conflict, save_new_schedule
except ImportError:
    print("Cảnh báo: Chưa tìm thấy file controller! Đảm bảo cấu trúc thư mục đúng.")

class AdminDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Admin Dashboard")
        self.geometry("1000x600")
        self.eval('tk::PlaceWindow . center')

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(self.sidebar, text="ADMIN", font=("Arial", 20, "bold")).pack(pady=20)

        ctk.CTkButton(self.sidebar, text="Manage Users", command=self.show_users).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Manage Courses", command=self.show_courses).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Manage Schedule", command=self.show_schedule).pack(pady=10)

        # Main Content
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.show_users()

    # ================= USERS (UC 11) =================
    def show_users(self):
        self.clear_frame()

        ctk.CTkLabel(self.main_frame, text="Manage Users", font=("Arial", 18)).pack(pady=10)

        self.user_id = ctk.CTkEntry(self.main_frame, placeholder_text="User ID")
        self.user_id.pack(pady=5)

        self.fullname = ctk.CTkEntry(self.main_frame, placeholder_text="Full Name")
        self.fullname.pack(pady=5)

        self.email = ctk.CTkEntry(self.main_frame, placeholder_text="Email")
        self.email.pack(pady=5)

        self.role = ctk.CTkOptionMenu(self.main_frame, values=["Student", "Teacher"])
        self.role.pack(pady=5)

        self.password = ctk.CTkEntry(self.main_frame, placeholder_text="Password", show="*")
        self.password.pack(pady=5)

        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Add", command=self.add_user).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Update", command=self.update_user).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Delete", command=self.delete_user).grid(row=0, column=2, padx=5)

    def add_user(self):
        # 1. Lấy dữ liệu từ giao diện
        uid = self.user_id.get().strip()
        fname = self.fullname.get().strip()
        email_val = self.email.get().strip()
        role_val = self.role.get()
        pwd = self.password.get().strip()

        if not uid or not email_val or not pwd:
            messagebox.showerror("Error", "Vui lòng điền đủ các trường bắt buộc (ID, Email, Pass)!")
            return

        # 2. Gọi logic lưu vào Database
        try:
            is_saved, msg = save_new_user_to_db(uid, fname, email_val, role_val, pwd)
            if is_saved:
                messagebox.showinfo("Success", msg)
                # Xóa trắng form sau khi thêm thành công
                self.user_id.delete(0, 'end')
                self.fullname.delete(0, 'end')
                self.email.delete(0, 'end')
                self.password.delete(0, 'end')
            else:
                messagebox.showerror("Database Error", msg)
        except NameError:
            messagebox.showwarning("Lỗi Import", "Chưa kết nối được với file admin_controller.py")

    def update_user(self):
        messagebox.showinfo("Thông báo", "Chức năng Update đang được phát triển")

    def delete_user(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure to delete?")
        if confirm:
            messagebox.showinfo("Deleted", "Mock: User deleted")

    # ================= COURSES (UC 12) =================
    def show_courses(self):
        self.clear_frame()

        ctk.CTkLabel(self.main_frame, text="Manage Courses", font=("Arial", 18)).pack(pady=10)

        self.course_id = ctk.CTkEntry(self.main_frame, placeholder_text="Course ID")
        self.course_id.pack(pady=5)

        self.course_name = ctk.CTkEntry(self.main_frame, placeholder_text="Course Name")
        self.course_name.pack(pady=5)

        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Add", command=self.add_course).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Edit", command=self.edit_course).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Delete", command=self.delete_course).grid(row=0, column=2, padx=5)

    def add_course(self):
        cid = self.course_id.get().strip()
        cname = self.course_name.get().strip()

        if not cid or not cname:
            messagebox.showerror("Error", "Vui lòng nhập đủ mã môn và tên môn!")
            return

        try:
            is_saved, msg = save_new_course_to_db(cid, cname)
            if is_saved:
                messagebox.showinfo("Success", msg)
                self.course_id.delete(0, 'end')
                self.course_name.delete(0, 'end')
            else:
                messagebox.showerror("Database Error", msg)
        except NameError:
            messagebox.showwarning("Lỗi Import", "Chưa kết nối được với file admin_controller.py")

    def edit_course(self):
        messagebox.showinfo("Success", "Chức năng Edit đang được phát triển")

    def delete_course(self):
        messagebox.showinfo("Deleted", "Mock: Course deleted")

    # ================= SCHEDULE (UC 13) =================
    def show_schedule(self):
        self.clear_frame()

        ctk.CTkLabel(self.main_frame, text="Manage Schedule", font=("Arial", 18)).pack(pady=10)

        self.schedule_course = ctk.CTkEntry(self.main_frame, placeholder_text="Course ID")
        self.schedule_course.pack(pady=5)

        self.lecturer = ctk.CTkEntry(self.main_frame, placeholder_text="Lecturer ID")
        self.lecturer.pack(pady=5)

        self.date = ctk.CTkEntry(self.main_frame, placeholder_text="Date (YYYY-MM-DD)")
        self.date.pack(pady=5)

        self.time = ctk.CTkEntry(self.main_frame, placeholder_text="Time (Ví dụ: 07:00-09:00)")
        self.time.pack(pady=5)

        self.room = ctk.CTkEntry(self.main_frame, placeholder_text="Classroom (VD: A1)")
        self.room.pack(pady=5)

        ctk.CTkButton(self.main_frame, text="Save", command=self.save_schedule).pack(pady=10)

    def save_schedule(self):
        cid = self.schedule_course.get().strip()
        date_val = self.date.get().strip()
        time_val = self.time.get().strip()
        room_val = self.room.get().strip()

        if not cid or not date_val or not time_val or not room_val:
            messagebox.showerror("Error", "Vui lòng điền đủ thông tin xếp lịch!")
            return

        # Cắt chuỗi thời gian (VD: "07:00-09:00" -> start="07:00", end="09:00")
        try:
            start_time, end_time = time_val.split('-')
            start_time = start_time.strip()
            end_time = end_time.strip()
        except ValueError:
            messagebox.showerror("Error", "Sai định dạng thời gian! Vui lòng nhập kiểu 07:00-09:00")
            return

        # Gọi logic kiểm tra trùng và lưu DB
        try:
            # 1. Check trùng lịch
            is_conflict = check_schedule_conflict(room_val, date_val, start_time, end_time)
            if is_conflict:
                messagebox.showerror("Conflict Error", f"Lỗi: Phòng {room_val} đã bị kẹt lịch vào khoảng thời gian này!")
                return

            # 2. Lưu nếu không trùng
            is_saved = save_new_schedule(cid, date_val, start_time, end_time, room_val)
            if is_saved:
                messagebox.showinfo("Success", "Đã lưu lịch học thành công vào XAMPP!")
                # Xóa Form
                self.schedule_course.delete(0, 'end')
                self.date.delete(0, 'end')
                self.time.delete(0, 'end')
                self.room.delete(0, 'end')
            else:
                messagebox.showerror("Database Error", "Lỗi trong quá trình lưu xuống DB!")
        except NameError:
            messagebox.showwarning("Lỗi Import", "Chưa kết nối được với file schedule_controller.py")

    # ================= HELPER =================
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
