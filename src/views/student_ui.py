import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

try:
    from src.controllers.student_controller import get_attendance_history
except ImportError:
    print("Cảnh báo: Chưa tìm thấy file student_controller.py")

class StudentDashboard(ctk.CTk):
    def __init__(self, student_id="SV01"): 
        super().__init__()
        
        self.student_id = student_id 
        
        self.title("Student Dashboard")
        self.geometry("650x650")
        self.protocol("WM_DELETE_WINDOW", exit)
        self.eval('tk::PlaceWindow . center')
        
        self.protocol("WM_DELETE_WINDOW", self.dong_cua_so_chuan)

        self.file_path = ""

        ctk.CTkLabel(self, text=f"STUDENT DASHBOARD ({self.student_id})", font=("Arial", 22, "bold")).pack(pady=15)

        history_frame = ctk.CTkFrame(self, fg_color="transparent")
        history_frame.pack(pady=10, fill="x", padx=30)

        ctk.CTkLabel(history_frame, text="1. Lịch sử điểm danh", font=("Arial", 16, "bold")).pack(anchor="w")

        self.history_box = ctk.CTkTextbox(history_frame, height=150, font=("Arial", 14))
        self.history_box.pack(pady=10, fill="x")

        ctk.CTkButton(history_frame, text="Tải lịch sử", font=("Arial", 14, "bold"), 
                      command=self.load_history).pack(anchor="e")

        leave_frame = ctk.CTkFrame(self, fg_color="transparent")
        leave_frame.pack(pady=20, fill="x", padx=30)

        ctk.CTkLabel(leave_frame, text="2. Nộp đơn xin nghỉ học", font=("Arial", 16, "bold")).pack(anchor="w")

        self.date_entry = ctk.CTkEntry(leave_frame, placeholder_text="Ngày nghỉ (YYYY-MM-DD)", font=("Arial", 14), height=35)
        self.date_entry.pack(pady=(10, 5), fill="x")

        self.reason_entry = ctk.CTkTextbox(leave_frame, height=80, font=("Arial", 14))
        self.reason_entry.insert("1.0", "Nhập lý do nghỉ học...")
        self.reason_entry.pack(pady=5, fill="x")

        upload_frame = ctk.CTkFrame(leave_frame, fg_color="transparent")
        upload_frame.pack(fill="x", pady=5)

        ctk.CTkButton(upload_frame, text="Tải minh chứng", command=self.upload_file, 
                      fg_color="gray", hover_color="darkgray").pack(side="left")
        
        self.file_label = ctk.CTkLabel(upload_frame, text="Chưa chọn tệp", text_color="gray", font=("Arial", 12, "italic"))
        self.file_label.pack(side="left", padx=15)

        ctk.CTkButton(leave_frame, text="Gửi Đơn Xin Nghỉ", font=("Arial", 16, "bold"), 
                      fg_color="green", hover_color="darkgreen", height=40,
                      command=self.submit_request).pack(pady=20)

    def load_history(self):
        """Lấy dữ liệu từ DB và kiểm tra cảnh báo vắng mặt"""
        try:
            success, msg, data = get_attendance_history(self.student_id)
            
            if not success:
                messagebox.showerror("Lỗi", msg)
                return

            self.history_box.delete("1.0", "end")
            absent_count = 0
            
            if not data:
                self.history_box.insert("end", "Chưa có dữ liệu điểm danh.")
                return

            for record in data:
                date_val, status_val = record
                self.history_box.insert("end", f"Ngày {date_val}: {status_val}\n")
                if status_val == "Absent":
                    absent_count += 1

            if absent_count >= 3:
                messagebox.showwarning("CẢNH BÁO HỌC VỤ ⚠️", 
                    f"Bạn đã vắng mặt {absent_count} buổi!\n\nNếu vắng quá 3 buổi, bạn sẽ bị cấm thi môn này.")
            else:
                messagebox.showinfo("Thông báo", f"Bạn đã vắng {absent_count} buổi. Hãy tiếp tục đi học đầy đủ!")

        except NameError:
            self.history_box.insert("end", "Dữ liệu mẫu (Chưa kết nối DB):\n2026-04-20: Absent\n2026-04-21: Absent\n2026-04-22: Absent")
            messagebox.showwarning("Cảnh báo", "Bạn đã vắng 3 buổi! (Dữ liệu mẫu)")

    def upload_file(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg"), ("PDF files", "*.pdf")])
        if file:
            self.file_path = file
            filename = file.split("/")[-1]
            self.file_label.configure(text=f"📎 {filename}", text_color="blue")
            
    def submit_request(self):
        date = self.date_entry.get().strip()
        reason = self.reason_entry.get("1.0", "end").strip()

        if not date or not reason or reason == "Nhập lý do nghỉ học...":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin ngày nghỉ và lý do!")
            return

        try:
            from src.controllers.student_controller import submit_leave_request
            
            success, msg = submit_leave_request(self.student_id, reason, date)

            if success:
                messagebox.showinfo("Thành công", msg)
                
                self.date_entry.delete(0, 'end')
                self.reason_entry.delete("1.0", "end")
                self.file_label.configure(text="Chưa chọn tệp", text_color="gray")
                self.file_path = "" 
            else:
                messagebox.showerror("Lỗi Database", msg)
                
        except Exception as e:
            messagebox.showerror("Lỗi Hệ thống", f"Không thể gọi Controller: {e}")
            
    def dong_cua_so_chuan(self):
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = StudentDashboard()
    app.mainloop()
