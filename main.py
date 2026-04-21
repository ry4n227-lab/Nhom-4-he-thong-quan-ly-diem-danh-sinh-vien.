import customtkinter as ctk
from tkinter import messagebox

# Import logic xử lý từ controller
from src.controllers.login_controller import verify_login

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Thiết lập cửa sổ ---
        self.title("Hệ thống Quản lý Điểm danh")
        self.geometry("400x500")
        self.eval('tk::PlaceWindow . center')
        
        # --- Bố cục giao diện (Sườn) ---
        self.label_title = ctk.CTkLabel(self, text="LOGIN", font=("Arial", 26, "bold"))
        self.label_title.pack(pady=(50, 30))

        # Nhập ID
        self.entry_id = ctk.CTkEntry(self, placeholder_text="Username / ID", width=280, height=40)
        self.entry_id.pack(pady=10)

        # Nhập Password
        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=280, height=40)
        self.entry_pass.pack(pady=10)

        # Chọn Vai trò
        self.role_var = ctk.StringVar(value="Students")
        self.combobox_role = ctk.CTkComboBox(self, values=["Admin", "Teachers", "Students"], 
                                             variable=self.role_var, width=280, height=40)
        self.combobox_role.pack(pady=10)

        # Nút Login
        self.btn_login = ctk.CTkButton(self, text="LOG IN", command=self.process_login, 
                                       width=280, height=45, font=("Arial", 14, "bold"))
        self.btn_login.pack(pady=30)

    # --- Xử lý sự kiện (Logic điều hướng) ---
    def process_login(self):
        username = self.entry_id.get().strip()
        password = self.entry_pass.get().strip()
        role = self.role_var.get()

        # 1. Gọi hàm kiểm tra từ login_controller.py
        # Trả về True/False (dựa trên code xử lý của bạn)
        is_valid = verify_login(username, password, role)

        if is_valid:
            # Nếu đúng -> Chuyển màn hình
            messagebox.showinfo("Thành công", f"Đăng nhập thành công với quyền {role}")
            self.destroy() # Đóng màn hình đăng nhập
            self.open_main_dashboard(role) # Mở màn hình tương ứng
        else:
            # Nếu sai -> Hiện thông báo lỗi (UC 2)
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

    def open_main_dashboard(self, role):
        """
        Dẫn luồng sang các giao diện Admin / Giảng viên / Sinh viên
        """
        try:
            if role == "Admin":
                from src.views.admin_ui import AdminDashboard
                app = AdminDashboard()
                app.mainloop()
            elif role == "Teachers":
                from src.views.teacher_ui import TeacherDashboard
                app = TeacherDashboard()
                app.mainloop()
            elif role == "Students":
                from src.views.student_ui import StudentDashboard
                app = StudentDashboard()
                app.mainloop()
        except ImportError as e:
            # Trường hợp các file UI kia chưa được tạo trên GitHub
            print(f"Lỗi: Không tìm thấy file UI của {role}. Chi tiết: {e}")
            messagebox.showwarning("Cảnh báo", f"Giao diện của {role} đang được phát triển!")

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()
