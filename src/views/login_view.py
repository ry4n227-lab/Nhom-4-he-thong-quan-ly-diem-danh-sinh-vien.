import customtkinter as ctk
from tkinter import messagebox

# Thiết lập giao diện chung
ctk.set_appearance_mode("light")  # Chế độ nền sáng
ctk.set_default_color_theme("blue") # Tông màu chủ đạo là xanh dương

# Import logic xử lý từ controller
try:
    from src.controllers.login_controller import verify_login
except ImportError:
    print("Cảnh báo: Chưa tìm thấy file login_controller.py")

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Thiết lập cửa sổ ---
        self.title("Hệ thống Quản lý Điểm danh")
        self.geometry("450x550")
        self.resizable(False, False) # Không cho phóng to thu nhỏ để tránh vỡ giao diện
        
        # Căn giữa màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (450 / 2)
        y = (screen_height / 2) - (550 / 2)
        self.geometry(f"450x550+{int(x)}+{int(y)}")

        # --- Container chính (Dùng Frame để tạo khoảng trắng bao quanh) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.main_frame.pack(pady=40, padx=40, fill="both", expand=True)

        # Tiêu đề
        self.label_title = ctk.CTkLabel(self.main_frame, text="WELCOME BACK", 
                                        font=("Arial", 28, "bold"), text_color="#1f538d")
        self.label_title.pack(pady=(40, 5))
        
        self.label_subtitle = ctk.CTkLabel(self.main_frame, text="Please login to your account", 
                                           font=("Arial", 13), text_color="gray")
        self.label_subtitle.pack(pady=(0, 30))

        # Nhập ID
        self.entry_id = ctk.CTkEntry(self.main_frame, placeholder_text="Username / ID", 
                                     width=300, height=45, corner_radius=10, border_width=1)
        self.entry_id.pack(pady=10)

        # Nhập Password
        self.entry_pass = ctk.CTkEntry(self.main_frame, placeholder_text="Password", 
                                       show="*", width=300, height=45, corner_radius=10, border_width=1)
        self.entry_pass.pack(pady=10)

        # Chọn Vai trò (Sắp xếp lại cho chuyên nghiệp)
        self.role_var = ctk.StringVar(value="Students")
        self.combobox_role = ctk.CTkComboBox(self.main_frame, values=["Admin", "Teachers", "Students"], 
                                             variable=self.role_var, width=300, height=45, 
                                             corner_radius=10, justify="center")
        self.combobox_role.pack(pady=10)

        # Nút Login (Màu xanh đậm, bo góc đẹp)
        self.btn_login = ctk.CTkButton(self.main_frame, text="LOGIN", command=self.process_login, 
                                       width=300, height=50, font=("Arial", 16, "bold"), 
                                       corner_radius=10)
        self.btn_login.pack(pady=(30, 20))

    # --- Xử lý sự kiện ---
    def process_login(self):
        username = self.entry_id.get().strip()
        password = self.entry_pass.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

       # Gọi hàm kiểm tra từ login_controller.py
        try:
            is_valid = verify_login(username, password, role)
            if is_valid:
                messagebox.showinfo("Thành công", f"Chào mừng {role} đã quay trở lại!")
                
                # SỬA DÒNG NÀY: Dùng destroy() thay vì withdraw()
                self.destroy() 
                
                self.open_main_dashboard(role)
            else:
                messagebox.showerror("Lỗi", "Tài khoản hoặc mật khẩu không chính xác!")

    def open_main_dashboard(self, role):
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
        except Exception as e:
            print(f"Lỗi khởi động Dashboard: {e}")
            self.deiconify() # Hiện lại màn hình login nếu lỗi

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()
