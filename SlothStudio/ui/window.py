
import sys
import cv2
import time
import customtkinter
from PIL import Image
from CTkMessagebox import CTkMessagebox


# custom appearance of UI
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

from SlothStudio.config import 

class MainWindow(customtkinter.CTk):

    width_dashboard = 1300
    height_dashboard = 800

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # init UI
        self.GUI_InitialSetupResources_Displayer()

        # setup widgets for UI
        self.GUI_WidgetsPanelSetup_Displayer()
        
        self.GUI_CoreFunctionality_Displayer()

    # ---------------- INIT SETUP RESOURCE ---------------- #
    # ------------------------------------------------------#
    def GUI_InitialSetupResources_Displayer(self):

        # config for common resources of UI
        self.commonSetupResources()

        # config for images as an icon
        self.imageSetupResources()

    def commonSetupResources(self):

        # Window title
        self.title("Sloth Studio")
        self.geometry(f"{self.width_dashboard}x{self.height_dashboard}")
        self.resizable(True, True)

        # root grid configuration
        self.grid_columnconfigure(0, weight=0)      # menu panel
        self.grid_columnconfigure(1, weight=1)      # display panel
        self.grid_rowconfigure(0, weight=1)

        # menu panel
        self.menu_panel = customtkinter.CTkFrame(self, width=220, corner_radius=20)
        self.menu_panel.grid(row=0, column=0, padx=20, pady=20, sticky="ns")
        self.menu_panel.grid_rowconfigure(0, weight=1)

        # display panel
        self.display_panel = customtkinter.CTkFrame(self, corner_radius=20)
        self.display_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.display_panel.grid_rowconfigure(0, weight=1)
        self.display_panel.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def imageSetupResources(self):

        # i



    def on_closing(self):

        msg_ExitSystem \
            = CTkMessagebox(master=self,
                            title="Exit",
                            message="Do you want to exit the FaceID Enrollment System",
                            icon="question",
                            option_1="Cancel",
                            option_2="Exit")
        if msg_ExitSystem.get() == "Exit":
            if hasattr(self, "face_processor"):
                self.face_processor.stop()

            if hasattr(self, "camera_stream"):
                self.camera_stream.stop()

            self.destroy()
            sys.exit()