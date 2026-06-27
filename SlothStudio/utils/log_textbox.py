
import customtkinter
from datetime import datetime

class LogTextboxUtils(customtkinter.CTkTextbox):

    LOG_COLORS = {
        "INFO":   "#87CEFA",
        "WARNING":"#FFD700",
        "ERROR":  "#FF6B6B",
        "SUCCESS":"#90EE90",
        "DEBUG":  "#C0C0C0"
    }

    def __init__(self, parent, **kwargs):
        super().__init__(parent, wrap="word", **kwargs)

        for tag, color in self.LOG_COLORS.items():
            self.tag_config(tag, foreground=color)

        self.configure(state="disabled")

    def log(self, log_type, message, timestamp=True):

        yview = self.yview()
        auto_scroll = (yview[1] > 0.95)

        self.configure(state="normal")

        if timestamp:
            current_time = (datetime.now().strftime("%H:%M:%S"))
            self.insert("end", f"[{log_type}] ", log_type)
            self.insert("end", f"[{current_time}] ")
            self.insert("end", f"{message}\n")
        else:
            self.insert("end", f"{message}\n")

        if auto_scroll:
            self.see("end")

        self.configure(state="disabled")

    def append(self, message):

        self.log("INFO", message)

    def clear(self):

        self.configure(state="normal")
        self.delete("1.0","end")
        self.configure(state="disabled")

    @staticmethod
    def Broadcast(textboxes, log_type, message, timestamp=True):

        for textbox in textboxes:
            if textbox is None:
                continue

            textbox.log(log_type=log_type, message=message, timestamp=timestamp)