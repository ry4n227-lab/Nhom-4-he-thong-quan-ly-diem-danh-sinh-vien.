import customtkinter as ctk
from tkinter import messagebox

class TeacherDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # =====================
        # Window Configuration
        # =====================
        self.title("Teacher Dashboard")
        self.geometry("800x600")
        self.eval('tk::PlaceWindow . center')
        
        # Main Title
        self.lbl_title = ctk.CTkLabel(self, text="TEACHER DASHBOARD", font=("Arial", 24, "bold"))
        self.lbl_title.pack(pady=20)

        # =====================
        # Tab View Setup
        # =====================
        self.tabview = ctk.CTkTabview(self, width=750, height=500)
        self.tabview.pack(padx=20, pady=10)

        self.tabview.add("Attendance (UC 3 & 6)")
        self.tabview.add("Leave Requests (UC 8)")

        # Initialize Tabs
        self.setup_attendance_tab()
        self.setup_leave_request_tab()

    # =====================
    # TAB 1: ATTENDANCE
    # =====================
    def setup_attendance_tab(self):
        tab = self.tabview.tab("Attendance (UC 3 & 6)")
        
        # Top Controls
        self.lbl_class = ctk.CTkLabel(tab, text="Select Class:")
        self.lbl_class.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.cb_class = ctk.CTkComboBox(tab, values=["INT1340 - Python", "INT1339 - Database"])
        self.cb_class.grid(row=0, column=1, padx=10, pady=10)

        self.btn_start = ctk.CTkButton(tab, text="Open Attendance Session", command=self.load_students)
        self.btn_start.grid(row=0, column=2, padx=20, pady=10)

        # Student List Area (Scrollable)
        self.scroll_frame = ctk.CTkScrollableFrame(tab, width=650, height=300)
        self.scroll_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Column Headers
        ctk.CTkLabel(self.scroll_frame, text="Student ID", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=30)
        ctk.CTkLabel(self.scroll_frame, text="Full Name", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=30)
        ctk.CTkLabel(self.scroll_frame, text="Status", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=30)

        # Save Button
        self.btn_save = ctk.CTkButton(tab, text="Save Attendance", command=self.save_attendance, fg_color="green", hover_color="darkgreen")
        self.btn_save.grid(row=2, column=0, columnspan=3, pady=15)

    # =====================
    # TAB 2: LEAVE REQUESTS
    # =====================
    def setup_leave_request_tab(self):
        tab = self.tabview.tab("Leave Requests (UC 8)")

        self.req_frame = ctk.CTkScrollableFrame(tab, width=700, height=350)
        self.req_frame.pack(padx=10, pady=20)

        # Mock Data for Requests
        requests = [
            ("SV01", "Nguyen Van A", "Sick Leave", "2026-04-22"),
            ("SV02", "Tran Thi B", "Family Matter", "2026-04-22")
        ]

        # Column Headers
        headers = ["ID", "Name", "Reason", "Date", "Action"]
        for col, text in enumerate(headers):
            ctk.CTkLabel(self.req_frame, text=text, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=15, pady=5)

        # Populate Data Rows
        for i, req in enumerate(requests, start=1):
            ctk.CTkLabel(self.req_frame, text=req[0]).grid(row=i, column=0, padx=15, pady=10)
            ctk.CTkLabel(self.req_frame, text=req[1]).grid(row=i, column=1, padx=15, pady=10)
            ctk.CTkLabel(self.req_frame, text=req[2]).grid(row=i, column=2, padx=15, pady=10)
            ctk.CTkLabel(self.req_frame, text=req[3]).grid(row=i, column=3, padx=15, pady=10)
            
            # Approve/Reject Buttons
            btn_frame = ctk.CTkFrame(self.req_frame, fg_color="transparent")
            btn_frame.grid(row=i, column=4, padx=15, pady=10)
            
            ctk.CTkButton(btn_frame, text="Approve", width=60, fg_color="green").pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="Reject", width=60, fg_color="red").pack(side="left", padx=5)

    # =====================
    # Mock Functions
    # =====================
    def load_students(self):
        messagebox.showinfo("System", "Attendance session opened!")
        # Mock students
        students = [("SV01", "Nguyen Van A"), ("SV02", "Tran Thi B"), ("SV03", "Le Van C")]
        
        for i, sv in enumerate(students, start=1):
            ctk.CTkLabel(self.scroll_frame, text=sv[0]).grid(row=i, column=0, padx=30, pady=5)
            ctk.CTkLabel(self.scroll_frame, text=sv[1]).grid(row=i, column=1, padx=30, pady=5)
            
            # Status Dropdown (Present, Absent, Late)
            status_cb = ctk.CTkComboBox(self.scroll_frame, values=["Present", "Absent", "Late"], width=100)
            status_cb.set("Present")
            status_cb.grid(row=i, column=2, padx=30, pady=5)

    def save_attendance(self):
        messagebox.showinfo("Success", "Attendance data saved to Database!")

if __name__ == "__main__":
    app = TeacherDashboard()
    app.mainloop()
