import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AdminDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Admin Dashboard")
        self.geometry("1000x600")

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

    # ================= USERS =================
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
        if not self.user_id.get() or not self.email.get():
            messagebox.showerror("Error", "Missing required fields!")
            return

        # giả lập check trùng
        if self.user_id.get() == "1":
            messagebox.showerror("Error", "Account already exists")
            return

        messagebox.showinfo("Success", "User added successfully")

    def update_user(self):
        messagebox.showinfo("Success", "User updated")

    def delete_user(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure to delete?")
        if confirm:
            messagebox.showinfo("Deleted", "User deleted")

    # ================= COURSES =================
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
        if not self.course_id.get() or not self.course_name.get():
            messagebox.showerror("Error", "Missing information")
            return

        messagebox.showinfo("Success", "Course added")

    def edit_course(self):
        messagebox.showinfo("Success", "Course updated")

    def delete_course(self):
        messagebox.showinfo("Deleted", "Course deleted")

    # ================= SCHEDULE =================
    def show_schedule(self):
        self.clear_frame()

        ctk.CTkLabel(self.main_frame, text="Manage Schedule", font=("Arial", 18)).pack(pady=10)

        self.schedule_course = ctk.CTkEntry(self.main_frame, placeholder_text="Course ID")
        self.schedule_course.pack(pady=5)

        self.lecturer = ctk.CTkEntry(self.main_frame, placeholder_text="Lecturer ID")
        self.lecturer.pack(pady=5)

        self.date = ctk.CTkEntry(self.main_frame, placeholder_text="Date (YYYY-MM-DD)")
        self.date.pack(pady=5)

        self.time = ctk.CTkEntry(self.main_frame, placeholder_text="Time (Start-End)")
        self.time.pack(pady=5)

        self.room = ctk.CTkEntry(self.main_frame, placeholder_text="Classroom")
        self.room.pack(pady=5)

        ctk.CTkButton(self.main_frame, text="Save", command=self.save_schedule).pack(pady=10)

    def save_schedule(self):
        # giả lập conflict
        if self.room.get() == "A1":
            messagebox.showerror("Error", "Schedule conflict for classroom or lecturer")
            return

        messagebox.showinfo("Success", "Schedule created")

    # ================= HELPER =================
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
