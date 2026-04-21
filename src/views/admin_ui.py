import customtkinter as ctk
from tkinter import messagebox

# =====================
# Import Controller Logic
# =====================
try:
    from src.controllers.schedule_controller import check_schedule_conflict, save_new_schedule
except ImportError:
    print("Warning: Could not import schedule_controller.")

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # =====================
        # Window Configuration
        # =====================
        self.title("Admin Dashboard")
        self.geometry("850x650")
        self.eval('tk::PlaceWindow . center')
        
        # Main Title
        self.lbl_title = ctk.CTkLabel(self, text="ADMIN DASHBOARD", font=("Arial", 26, "bold"))
        self.lbl_title.pack(pady=20)

        # =====================
        # Tab View Setup
        # =====================
        self.tabview = ctk.CTkTabview(self, width=800, height=550)
        self.tabview.pack(padx=20, pady=10)

        self.tabview.add("Account Management (UC 11)")
        self.tabview.add("Course Management (UC 12)")
        self.tabview.add("Schedule Management (UC 13)")

        # Initialize Tabs
        self.setup_account_tab()
        self.setup_course_tab()
        self.setup_schedule_tab()

    # =====================
    # TAB 1: ACCOUNTS (UC 11)
    # =====================
    def setup_account_tab(self):
        tab = self.tabview.tab("Account Management (UC 11)")
        
        # Input Form
        form_frame = ctk.CTkFrame(tab, fg_color="transparent")
        form_frame.pack(pady=20)

        ctk.CTkLabel(form_frame, text="User ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_acc_id = ctk.CTkEntry(form_frame, width=200)
        self.entry_acc_id.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Password:").grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.entry_acc_pass = ctk.CTkEntry(form_frame, width=200)
        self.entry_acc_pass.grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Role:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.cb_acc_role = ctk.CTkComboBox(form_frame, values=["Teachers", "Students"], width=200)
        self.cb_acc_role.grid(row=1, column=1, padx=10, pady=10)

        self.btn_add_acc = ctk.CTkButton(form_frame, text="Create Account", command=self.create_account, fg_color="blue")
        self.btn_add_acc.grid(row=1, column=3, padx=10, pady=10)

        # List Area
        self.acc_list_frame = ctk.CTkScrollableFrame(tab, width=700, height=300)
        self.acc_list_frame.pack(pady=10)
        ctk.CTkLabel(self.acc_list_frame, text="Account list will be displayed here...", text_color="gray").pack(pady=20)

    # =====================
    # TAB 2: COURSES (UC 12)
    # =====================
    def setup_course_tab(self):
        tab = self.tabview.tab("Course Management (UC 12)")

        form_frame = ctk.CTkFrame(tab, fg_color="transparent")
        form_frame.pack(pady=20)

        ctk.CTkLabel(form_frame, text="Course ID:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_course_id = ctk.CTkEntry(form_frame, width=200)
        self.entry_course_id.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Course Name:").grid(row=0, column=2, padx=10, pady=10)
        self.entry_course_name = ctk.CTkEntry(form_frame, width=200)
        self.entry_course_name.grid(row=0, column=3, padx=10, pady=10)

        self.btn_add_course = ctk.CTkButton(form_frame, text="Add Course", command=self.add_course)
        self.btn_add_course.grid(row=1, column=0, columnspan=4, pady=20)

    # =====================
    # TAB 3: SCHEDULE (UC 13)
    # =====================
    def setup_schedule_tab(self):
        tab = self.tabview.tab("Schedule Management (UC 13)")

        form_frame = ctk.CTkFrame(tab)
        form_frame.pack(pady=30, padx=50, fill="both", expand=True)

        # Inputs
        ctk.CTkLabel(form_frame, text="Class ID:").grid(row=0, column=0, padx=20, pady=15, sticky="e")
        self.sch_class = ctk.CTkEntry(form_frame, width=250)
        self.sch_class.grid(row=0, column=1, padx=20, pady=15)

        ctk.CTkLabel(form_frame, text="Room (e.g., A101):").grid(row=1, column=0, padx=20, pady=15, sticky="e")
        self.sch_room = ctk.CTkEntry(form_frame, width=250)
        self.sch_room.grid(row=1, column=1, padx=20, pady=15)

        ctk.CTkLabel(form_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=20, pady=15, sticky="e")
        self.sch_date = ctk.CTkEntry(form_frame, width=250)
        self.sch_date.grid(row=2, column=1, padx=20, pady=15)

        ctk.CTkLabel(form_frame, text="Start Time (HH:MM):").grid(row=3, column=0, padx=20, pady=15, sticky="e")
        self.sch_start = ctk.CTkEntry(form_frame, width=250)
        self.sch_start.grid(row=3, column=1, padx=20, pady=15)

        ctk.CTkLabel(form_frame, text="End Time (HH:MM):").grid(row=4, column=0, padx=20, pady=15, sticky="e")
        self.sch_end = ctk.CTkEntry(form_frame, width=250)
        self.sch_end.grid(row=4, column=1, padx=20, pady=15)

        # Save Button
        self.btn_save_sch = ctk.CTkButton(form_frame, text="CHECK & SAVE SCHEDULE", font=("Arial", 14, "bold"), 
                                          fg_color="green", hover_color="darkgreen", height=40,
                                          command=self.process_schedule)
        self.btn_save_sch.grid(row=5, column=0, columnspan=2, pady=30)

    # =====================
    # Mock Functions (UC 11 & 12)
    # =====================
    def create_account(self):
        messagebox.showinfo("Success", "Mock: Account created successfully!")

    def add_course(self):
        messagebox.showinfo("Success", "Mock: Course added successfully!")

    # =====================
    # Real Integration Function (UC 13)
    # =====================
    def process_schedule(self):
        # Extract data from entries
        class_id = self.sch_class.get().strip()
        room = self.sch_room.get().strip()
        date = self.sch_date.get().strip()
        start_time = self.sch_start.get().strip()
        end_time = self.sch_end.get().strip()

        # Basic validation
        if not all([class_id, room, date, start_time, end_time]):
            messagebox.showwarning("Warning", "Please fill in all schedule fields!")
            return

        # 1. Check conflict using Developer A's logic
        try:
            is_conflict = check_schedule_conflict(room, date, start_time, end_time)
            
            if is_conflict:
                messagebox.showerror("Conflict Detected", f"Room {room} is already booked at this time!")
                return
                
            # 2. If no conflict, save it
            is_saved = save_new_schedule(class_id, date, start_time, end_time, room)
            if is_saved:
                messagebox.showinfo("Success", f"Schedule saved for Class {class_id} in Room {room}.")
            else:
                messagebox.showerror("Database Error", "Failed to save the schedule to database.")
                
        except NameError:
            print("Dev Mode: Data ready ->", class_id, room, date, start_time, end_time)
            messagebox.showwarning("Dev Mode", "UI is ready. Waiting for schedule_controller.py to be implemented.")

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
