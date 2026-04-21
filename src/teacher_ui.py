import customtkinter as ctk

class TeacherDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Teacher Dashboard")
        self.geometry("600x500")

        ctk.CTkLabel(self, text="Take Attendance", font=("Arial", 20)).pack(pady=10)

        # Fake student list
        self.students = ["SV001 - An", "SV002 - Bình", "SV003 - Cường"]

        self.status_vars = []

        for student in self.students:
            frame = ctk.CTkFrame(self)
            frame.pack(pady=5, fill="x", padx=10)

            ctk.CTkLabel(frame, text=student).pack(side="left", padx=10)

            var = ctk.StringVar(value="Present")
            self.status_vars.append(var)

            ctk.CTkOptionMenu(frame, values=["Present", "Absent", "Late"], variable=var).pack(side="right")

        ctk.CTkButton(self, text="Save Attendance", command=self.save).pack(pady=20)

    def save(self):
        for student, var in zip(self.students, self.status_vars):
            print(student, ":", var.get())


if __name__ == "__main__":
    app = TeacherDashboard()
    app.mainloop()
