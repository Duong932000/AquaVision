
import customtkinter
from datetime import datetime

class LogTextbox(customtkinter.CTkFrame):
    def __init__(self, master, textbox_width=310, textbox_height=220, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.textbox \
            = customtkinter.CTkTextbox(self,
                                       width=textbox_width,
                                       height=textbox_height,
                                       wrap="word",
                                       corner_radius=5,
                                       font=customtkinter.CTkFont(size=13))
        self.textbox.pack(fill="both", expand=True)
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(10, 10))
        self.textbox.tag_config("INFO", foreground="#87CEFA")       # light blue
        self.textbox.tag_config("WARNING", foreground="#FFD700")    # light yellow
        self.textbox.tag_config("ERROR", foreground="#FF6B6B")      # light red
        self.textbox.configure(state="disabled")

    def append_log(self, log_type, message):

        # check user is near bottom
        yview = self.textbox.yview()
        auto_scroll = yview[1] > 0.95

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.textbox.configure(state="normal")

        self.textbox.insert("end", f"[{log_type}] ", log_type)
        self.textbox.insert("end", f"[{timestamp}] ")
        self.textbox.insert("end", f"{message}\n")

        if auto_scroll:
            self.textbox.see("end")

        self.textbox.configure(state="disabled")

    def append(self, message):

        yview = self.textbox.yview()
        auto_scroll = yview[1] > 0.95

        self.textbox.configure(state="normal")

        self.textbox.insert("end", f"{message}\n")

        if auto_scroll:
            self.textbox.see("end")

        self.textbox.configure(state="disabled")

    def clear(self):

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")
