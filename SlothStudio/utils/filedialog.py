
from tkinter import filedialog

class FileDialogUtils:

    @staticmethod
    def BrowseFiles(title, filetypes, multiple=False):

        if multiple:
            return filedialog.askopenfilenames(title=title, filetypes=filetypes)

        return filedialog.askopenfilename(title=title, filetypes=filetypes)

    @staticmethod
    def SaveFiles(title="Save File", filetypes=(("Log Files", "*.log"), ("Text File", "*.txt"))):

        return filedialog.asksaveasfilename(title=title,
                                            defaultextension=".log",
                                            filetypes=filetypes)