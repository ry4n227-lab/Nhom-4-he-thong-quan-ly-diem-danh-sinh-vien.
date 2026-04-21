import customtkinter as ctk

class TeacherDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Teacher Dashboard")
        self.geometry("700x600")

        ctk.CTkLabel(self, text="TEACHER DASHBOARD", font=("Arial", 20)).pack(pady=10)

        # ===== UC7 + UC8 =====
        ctk.CTkLabel(self, text="Take Attendance").pack()

        self.students = ["SV001 - An", "SV002 - Bình", "SV003 - Cường"]
        self.status_vars = []

        for student in self.students:
            frame = ctk.CTkFrame(self)
            frame.pack(pady=5, fill="x", padx=10)

            ctk.CTkLabel(frame, text=student).pack(side="left", padx=10)

            var = ctk.StringVar(value="Present")
            self.status_vars.append(var)

            ctk.CTkOptionMenu(frame, values=["Present", "Absent", "Late"], variable=var).pack(side="right")

        ctk.CTkButton(self, text="Save Attendance", command=self.save_attendance).pack(pady=10)

        # ===== UC4 =====
        ctk.CTkLabel(self, text="Leave Requests").pack(pady=10)

        self.requests = [
            {"student": "SV001", "reason": "Sick"},
            {"student": "SV002", "reason": "Family issue"}
        ]

        for req in self.requests:
            frame = ctk.CTkFrame(self)
            frame.pack(pady=5, fill="x", padx=10)

            text = f"{req['student']} - {req['reason']}"
            ctk.CTkLabel(frame, text=text).pack(side="left", padx=10)

            ctk.CTkButton(frame, text="Approve", command=lambda r=req: self.handle_request(r, "Approved")).pack(side="right")
            ctk.CTkButton(frame, text="Reject", command=lambda r=req: self.handle_request(r, "Rejected")).pack(side="right")

    # ===== Save Attendance =====
    def save_attendance(self):
        print("=== Attendance Saved ===")
        for student, var in zip(self.students, self.status_vars):
            print(student, ":", var.get())

    # ===== UC4 =====
    def handle_request(self, request, status):
        print(f"{request['student']} request {status}")
