import customtkinter as ctk
from tkinter import filedialog

class StudentDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Student Dashboard")
        self.geometry("500x500")

        # Title
        ctk.CTkLabel(self, text="Submit Leave Request", font=("Arial", 20)).pack(pady=10)

        # Date
        self.date_entry = ctk.CTkEntry(self, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.pack(pady=5)

        # Reason
        self.reason_entry = ctk.CTkTextbox(self, height=100)
        self.reason_entry.pack(pady=5)

        # Upload file
        self.file_path = ""
        ctk.CTkButton(self, text="Upload Proof", command=self.upload_file).pack(pady=5)

        self.file_label = ctk.CTkLabel(self, text="No file selected")
        self.file_label.pack()

        # Submit button
        ctk.CTkButton(self, text="Submit Request", command=self.submit).pack(pady=10)

    def upload_file(self):
        file = filedialog.askopenfilename()
        if file:
            self.file_path = file
            self.file_label.configure(text=file)

    def submit(self):
        date = self.date_entry.get()
        reason = self.reason_entry.get("1.0", "end")

        if not date or not reason.strip():
            print("❌ Missing information")
            return

        print("✅ Submitted:", date, reason, self.file_path)


if __name__ == "__main__":
    app = StudentDashboard()
    app.mainloop()
