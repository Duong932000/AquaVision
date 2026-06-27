
import customtkinter
from tkinterdnd2 import DND_ALL, TkinterDnD 

class DnD(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # load tkdnd package
        self.TkdndVersion = TkinterDnD._require(self)
