import customtkinter as ctk
from tkinter import filedialog

class StudentDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Student Dashboard")
        self.geometry("600x600")

        self.file_path = ""

        ctk.CTkLabel(self, text="STUDENT DASHBOARD", font=("Arial", 20)).pack(pady=10)

        # ===== View Attendance History =====
        ctk.CTkLabel(self, text="Attendance History").pack()

        self.history_box = ctk.CTkTextbox(self, height=100)
        self.history_box.pack(pady=5)

        ctk.CTkButton(self, text="Load History", command=self.load_history).pack(pady=5)

        # ===== Submit Leave Request =====
        ctk.CTkLabel(self, text="Submit Leave Request").pack(pady=10)

        self.date_entry = ctk.CTkEntry(self, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.pack(pady=5)

        self.reason_entry = ctk.CTkTextbox(self, height=100)
        self.reason_entry.pack(pady=5)

        ctk.CTkButton(self, text="Upload Proof", command=self.upload_file).pack(pady=5)

        self.file_label = ctk.CTkLabel(self, text="No file selected")
        self.file_label.pack()

        ctk.CTkButton(self, text="Submit Request", command=self.submit).pack(pady=10)

    # ===== UC5 =====
    def load_history(self):
        fake_data = [
            "2026-04-01: Present",
            "2026-04-02: Absent",
            "2026-04-03: Late"
        ]
        self.history_box.delete("1.0", "end")
        for item in fake_data:
            self.history_box.insert("end", item + "\n")

    # ===== UC6 =====
    def upload_file(self):
        file = filedialog.askopenfilename()
        if file:
            if not file.endswith((".png", ".jpg", ".pdf")):
                self.file_label.configure(text="❌ Invalid file format")
                return
            self.file_path = file
            self.file_label.configure(text=file)

    # ===== UC3 =====
    def submit(self):
        date = self.date_entry.get()
        reason = self.reason_entry.get("1.0", "end").strip()

        if not date or not reason:
            self.file_label.configure(text="❌ Missing information")
            return

        print("✅ Leave Request Submitted")
        print("Date:", date)
        print("Reason:", reason)
        print("File:", self.file_path)

        self.file_label.configure(text="✅ Submitted successfully")
