
from tkinter import filedialog

class FileDialogUtils:

    @staticmethod
    def BrowseFiles(title, filetypes, multiple=False):

        if multiple:
            return filedialog.askopenfilenames(title=title, filetypes=filetypes)

        return filedialog.askopenfilename(title=title, filetypes=filetypes)
