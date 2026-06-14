
import sys
import cv2
from config.assets import asset_resources
import customtkinter
from PIL import Image
from CTkMessagebox import CTkMessagebox
from tkinterdnd2 import DND_FILES, TkinterDnD


# custom appearance of UI
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


class InferenceProgressTextbox(customtkinter.CTkFrame):
    def _init_(self, master, textbox_width=300, textbox_height=150, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.textbox \
            = customtkinter.CTkTextbox(self,
                                       width=textbox_width,
                                       height=textbox_height,
                                       wrap="word",
                                       corner_radius=5,
                                       font=customtkinter.CTkFont(size=13))
        self.textbox.pack(fill="both", expand=True)
        self.textbox.configure(state="disabled")

    def append(self, message):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"{message}")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def clear(self):

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")

class MainWindow(TkinterDnD.DnDWrapper, customtkinter.CTk):

    width_dashboard = 1300
    height_dashboard = 800

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # init UI
        self.GUI_InitSetupResources_Displayer()

        # setup widgets for UI
        self.GUI_PanelSetupResources_Displayer()

        # self.GUI_CoreFunctionality_Displayer()

    # ------------------- INIT SETUP RESOURCE ------------------- #
    # ------------------------------------------------------------#
    def GUI_InitSetupResources_Displayer(self):

        # config for common resources of UI
        self.CommonSetupResources()

        # config for images as an icon
        self.ImageSetupResources()

    def CommonSetupResources(self):

        # Window title
        self.title("Sloth Studio - Inference and Train Computer Vision model locally")
        self.geometry(f"{self.width_dashboard}x{self.height_dashboard}")
        self.resizable(True, True)

        # root grid configuration
        self.grid_columnconfigure(0, weight=0)      # menu panel
        self.grid_columnconfigure(1, weight=1)      # display panel
        self.grid_rowconfigure(0, weight=1)

        # menu panel
        self.menu_panel = customtkinter.CTkFrame(self, width=220, corner_radius=20)
        self.menu_panel.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

        # display panel
        self.display_panel = customtkinter.CTkFrame(self, corner_radius=20)
        self.display_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.display_panel.grid_rowconfigure(0, weight=1)
        self.display_panel.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.OnClosingApp_Event)

    def ImageSetupResources(self):

        self.logo_img = customtkinter.CTkImage(
            Image.open(asset_resources("logo.png")), size=(55, 55))

        self.inference_img = customtkinter.CTkImage(
            Image.open(asset_resources("inference.png")), size=(25, 25))

        self.train_img = customtkinter.CTkImage(
            Image.open(asset_resources("train.png")), size=(30, 30))

        self.dataset_img = customtkinter.CTkImage(
            Image.open(asset_resources("dataset.png")), size=(25, 25))

        self.dragdrop_img = customtkinter.CTkImage(
            Image.open(asset_resources("dragdrop.png")), size=(50, 50))


    # ------------------- PANEL SETUP RESOURCE ------------------- #
    # -------------------------------------------------------------#
    def GUI_PanelSetupResources_Displayer(self):

        # Menu Panel
        self.MenuPanel_Adapter()

        # Display Panel configure
        self.DisplayPanel_Adapter()

        # Inference Panel
        self.InferencePanel_Adapter()

        # Train Panel
        self.TrainPanel_Adapter()

        # Dataset Panel
        self.DatasetPanel_Adapter()

        # frame selection
        self.FrameSelection("Inference")
    
    def MenuPanel_Adapter(self):

        # logo
        self.logo_label \
            = customtkinter.CTkButton(self.menu_panel,
                                      text="Sloth-Studio",
                                      corner_radius=5,
                                      height=60,
                                      anchor="w",
                                      state="disabled",
                                      fg_color="transparent",
                                      text_color=("gray10", "gray90"),
                                      hover_color=("gray70", "gray30"),
                                      font=customtkinter.CTkFont(size=23, weight="bold"),
                                      image=self.logo_img)
        self.logo_label.grid(row=0, column=0, padx=15, pady=(20, 40), sticky="ew")

        # Inference menu tab
        self.inference_menu_tab \
            = customtkinter.CTkButton(self.menu_panel,
                                      text="Inference Models",
                                      command=self.InferenceFrame_Event,
                                      image=self.inference_img,
                                      anchor="w",
                                      height=50,
                                      corner_radius=10,
                                      font=customtkinter.CTkFont(size=16, slant="italic"))
        self.inference_menu_tab.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

        # Train menu tab
        self.train_menu_tab \
            = customtkinter.CTkButton(self.menu_panel,
                                      text="Train Models",
                                      command=self.TrainFrame_Event,
                                      image=self.train_img,
                                      anchor="w",
                                      height=50,
                                      corner_radius=10,
                                      font=customtkinter.CTkFont(size=16, slant="italic"))
        self.train_menu_tab.grid(row=2, column=0, padx=15, pady=5, sticky="ew")

        # Dataset menu tab
        self.dataset_menu_tab \
            = customtkinter.CTkButton(self.menu_panel,
                                      text="Dataset Handling",
                                      command=self.DatasetFrame_Event,
                                      image=self.dataset_img,
                                      anchor="w",
                                      height=50,
                                      corner_radius=10,
                                      font=customtkinter.CTkFont(size=16, slant="italic"))
        self.dataset_menu_tab.grid(row=3, column=0, padx=15, pady=5, sticky="ew")

        # Spacer
        self.menu_panel.grid_rowconfigure(4, weight=1)

    def DisplayPanel_Adapter(self):

        # inference frame
        self.inference_frame \
            = customtkinter.CTkFrame(self.display_panel, corner_radius=10, fg_color="transparent")

        # train frame
        self.train_frame \
            = customtkinter.CTkFrame(self.display_panel, corner_radius=10, fg_color="transparent")

        # dataset frame
        self.dataset_frame \
            = customtkinter.CTkFrame(self.display_panel, corner_radius=10, fg_color="transparent")

        for frame in (self.inference_frame, self.train_frame, self.dataset_frame):
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

    def InferencePanel_Adapter(self):

        # setup rate of inference_frame: 6-2-2
        self.inference_frame.grid_columnconfigure(0, weight=9)
        self.inference_frame.grid_columnconfigure(1, weight=1)
        self.inference_frame.grid_columnconfigure(2, weight=1)
        self.inference_frame.grid_rowconfigure(0, weight=1)

        # Create Subframes
        # video frame
        self.inference_video_frame \
            = customtkinter.CTkFrame(self.inference_frame, corner_radius=10)
        self.inference_video_frame.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="snew")
        self.inference_video_frame.grid_rowconfigure(0, weight=1)
        self.inference_video_frame.grid_columnconfigure(0, weight=1)

        # inference log frame
        self.inference_log_frame \
            = customtkinter.CTkFrame(self.inference_frame, corner_radius=10)
        self.inference_log_frame.grid(row=0, column=1, padx=5, pady=5, sticky="snew")
        self.inference_log_frame.grid_rowconfigure(0, weight=1)
        self.inference_log_frame.grid_columnconfigure(0, weight=1)

        # inference control frame
        self.inference_control_frame \
            = customtkinter.CTkFrame(self.inference_frame, corner_radius=10)
        self.inference_control_frame.grid(row=0, column=2, padx=5, pady=0, sticky="snew")
        self.inference_control_frame.grid_rowconfigure(0, weight=1)
        self.inference_control_frame.grid_columnconfigure(0, weight=1)

        # Calling widget functions
        self.InferenceVideo_WidgetConfigure()
        self.InferenceLog_WidgetConfigure()
        self.InferenceControl_WidgetConfigure()

    def InferenceVideo_WidgetConfigure(self):
        
        # Video panel label
        self.video_panel_label \
            = customtkinter.CTkLabel(self.inference_video_frame,
                                     text="✓ Video Panel",
                                     font=customtkinter.CTkFont(size=18, weight="bold"))
        self.video_panel_label.pack(anchor="w", padx=5, pady=(10, 5))

        # drop frame
        self.inference_drop_frame \
            = customtkinter.CTkFrame(self.inference_video_frame, corner_radius=15)
        self.inference_drop_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # drop icon
        self.drop_icon \
            = customtkinter.CTkButton(self.inference_drop_frame,
                                      text="",
                                      image=self.dragdrop_img,
                                      corner_radius=5,
                                      height=120,
                                      anchor="w",
                                      state="disabled",
                                      fg_color="transparent",
                                      text_color=("gray10", "gray90"),
                                      hover_color=("gray70", "gray30"),)
        self.drop_icon.pack(anchor="center", padx=100)

        # drop label
        self.drop_label \
            = customtkinter.CTkLabel(self.inference_drop_frame,
                                     text="Drag & Drop Image / Video Here",
                                     font=customtkinter.CTkFont(size=24, weight="bold"))
        self.drop_label.pack()

        self.youtube_entry \
            = customtkinter.CTkEntry(self.inference_drop_frame,
                                    width=500,
                                    height=40,
                                    placeholder_text=
                                    "https://www.youtube.com/watch?v=...")
        self.youtube_entry.pack(pady=(30, 10))

        self.load_source_button \
            = customtkinter.CTkButton(self.inference_drop_frame,
                                      text="Browse Files",
                                      command=self.BrowseFiles_Event)
        self.load_source_button.pack(pady=10)

    def InferenceLog_WidgetConfigure(self):
        
        # Inference log label
        self.inference_log_label \
            = customtkinter.CTkLabel(self.inference_log_frame,
                                     text="✓ Inference log",
                                     font=customtkinter.CTkFont(size=18, weight="bold"))
        self.inference_log_label.pack(anchor="w", padx=5, pady=(10, 5))

        # Clear Log button
        self.clear_log_button \
            = customtkinter.CTkButton(self.inference_log_frame,
                                      text="Clear log",
                                      command=self.ClearInferenceLog_Event,
                                      font=customtkinter.CTkFont(size=14, slant="italic"))
        self.clear_log_button.pack(anchor="w", padx=5, pady=(5, 10))

        # Inference Progress textbox
        self.inference_log_textbox \
            = InferenceProgressTextbox(self.inference_log_frame)
        self.inference_log_textbox.pack(fill="both", expand=True, padx=10, pady=(10, 0))

    def InferenceControl_WidgetConfigure(self):

        # tabview configure
        self.inference_control_tabview = customtkinter.CTkTabview(self.inference_control_frame)
        self.inference_control_tabview.grid(row=0, column=0, padx=15, pady=15, sticky="snew")
        self.inference_control_tabview.add("Inference Control")

        # show inference control tab
        self.inference_control_tab = self.inference_control_tabview.tab("Inference Control")
        
        #-------------------------------------------------------------------------------#
        #                                   FRAME CONFIGURE                             #
        #-------------------------------------------------------------------------------#
        # frame configure
        self.control_scroll_frame \
            = customtkinter.CTkScrollableFrame(self.inference_control_tab, corner_radius=10)
        self.control_scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)


        #-------------------------------------------------------------------------------#
        #                                  SOURCE CONFIGURE                             #
        #-------------------------------------------------------------------------------#
        # Source label
        self.source_label \
            = customtkinter.CTkLabel(self.control_scroll_frame,
                                     text="✓ Source:",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.source_label.pack(anchor="w", padx=10, pady=(15, 5))

        # Source entry
        self.source_entry \
            = customtkinter.CTkEntry(self.control_scroll_frame,
                                     height=35,
                                     placeholder_text="Enter source path here (e.g: video.mp4 / image.jpg / youtube url)")
        self.source_entry.pack(fill="x", padx=10, pady=10)


        #-------------------------------------------------------------------------------#
        #                                  MODEL CONFIGURE                              #
        #-------------------------------------------------------------------------------#
        # Model label
        self.model_label \
            = customtkinter.CTkLabel(self.control_scroll_frame,
                                     text="✓ Model:",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.model_label.pack(anchor="w", padx=10, pady=(15, 5))

        # Model entry
        self.model_entry \
            = customtkinter.CTkEntry(self.control_scroll_frame,
                                     height=35,
                                     placeholder_text=
                                     "e.g: runs/detect/train/weights/best.pt")
        self.model_entry.pack(fill="x", padx=10, pady=10)

        #-------------------------------------------------------------------------------#
        #                                TRACKER CONFIGURE                              #
        #-------------------------------------------------------------------------------#
        # Tracking label
        self.tracking_label \
            = customtkinter.CTkLabel(self.control_scroll_frame,
                                     text="✓ Tracking:",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.tracking_label.pack(anchor="w", padx=10, pady=(15, 5))

        # Tracking checkbox
        self.enable_tracking_checkbox \
            = customtkinter.CTkCheckBox(self.control_scroll_frame, text="Enable Tracking")
        self.enable_tracking_checkbox.select()
        self.enable_tracking_checkbox.pack(anchor="w", padx=10, pady=5)

        # Tracker combobox
        self.tracker_combobox \
            = customtkinter.CTkComboBox(self.control_scroll_frame,
                                        values=[
                                            "ByteTrack",
                                            "BoT-SORT",
                                            "DeepSORT"
                                        ])
        self.tracker_combobox.set("ByteTrack")
        self.tracker_combobox.pack(fill="x", padx=10, pady=10)

        #-------------------------------------------------------------------------------#
        #                       DETECTION PARAMETERS CONFIGURE                          #
        #-------------------------------------------------------------------------------#
        # detection parameters label
        self.parameter_label \
            = customtkinter.CTkLabel(self.control_scroll_frame,
                                    text="✓ Detection Parameters",
                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.parameter_label.pack(anchor="w", padx=10, pady=(15, 5))

        self.confidence_frame \
            = customtkinter.CTkFrame(self.control_scroll_frame, fg_color="transparent")
        self.confidence_frame.pack(fill="x", padx=10, pady=(0, 5))

        # Confidence threshold label
        self.confidence_label \
            = customtkinter.CTkLabel(self.confidence_frame,
                                     text="Confidence Threshold")
        self.confidence_label.pack(side="left")

        self.confidence_value_label \
            = customtkinter.CTkLabel(self.confidence_frame,
                                     text="0.25", width=50)
        self.confidence_value_label.pack(side="right")

        # Confidence slider
        self.confidence_slider \
            = customtkinter.CTkSlider(self.control_scroll_frame,
                                      command=self.ConfidenceSlider_Event,
                                      from_=0.05, to=1.0)
        self.confidence_slider.set(0.25)
        self.confidence_slider.pack(fill="x", padx=10, pady=5)

        self.iou_frame = customtkinter.CTkFrame(self.control_scroll_frame, fg_color="transparent")
        self.iou_frame.pack(fill="x", padx=10, pady=(0, 5))

        # IoU label
        self.iou_label \
            = customtkinter.CTkLabel(self.iou_frame,
                                     text="NMS IOU Threshold")
        self.iou_label.pack(side="left")

        self.iou_value_label \
            = customtkinter.CTkLabel(self.iou_frame, text="0.45", width=50)
        self.iou_value_label.pack(side="right")

        # IoU slider
        self.iou_slider \
            = customtkinter.CTkSlider(self.control_scroll_frame,
                                      command=self.IoUSlider_Event,
                                      from_=0.1, to=1.0)
        self.iou_slider.set(0.45)
        self.iou_slider.pack(fill="x", padx=10, pady=10)

        # Output Options label
        self.output_options_label \
            = customtkinter.CTkLabel(self.control_scroll_frame,
                                     text="✓ Output Options",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.output_options_label.pack(anchor="w", padx=10, pady=(15, 5))
    
        # Save video checkbox
        self.save_video_checkbox = \
            customtkinter.CTkCheckBox(self.control_scroll_frame,
                                     text="Save Output Video/Image")
        self.save_video_checkbox.pack(anchor="w", padx=10, pady=5)

        # Save Frame checkbox
        self.save_frames_checkbox = \
            customtkinter.CTkCheckBox(self.control_scroll_frame,
                                      text="Save Detection Frames")
        self.save_frames_checkbox.pack(anchor="w", padx=10, pady=5)

        # Runtime label
        self.runtime_label \
            = customtkinter.CTkLabel(self.control_scroll_frame,
                                     text="✓ Runtime",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.runtime_label.pack(anchor="w", padx=10, pady=(15, 5))
        
        # device combobox
        self.device_combobox = \
            customtkinter.CTkComboBox(self.control_scroll_frame,
                                      values=[
                                          "Auto",
                                          "CPU",
                                          "CUDA"
                                      ])
        self.device_combobox.set("Auto")
        self.device_combobox.pack(fill="x", padx=10, pady=5)

        # Start inference button
        self.start_button \
            = customtkinter.CTkButton(self.control_scroll_frame,
                                      text="Start Inference",
                                      height=40,
                                      font=customtkinter.CTkFont(size=14))
        self.start_button.pack(fill="x", padx=10, pady=(25, 10))

        # Stop inference button
        self.stop_button \
            = customtkinter.CTkButton(self.control_scroll_frame,
                                      text="Stop Inference",
                                      height=40,
                                      fg_color="darkred",
                                      font=customtkinter.CTkFont(size=14))
        self.stop_button.pack(fill="x", padx=10, pady=(5, 20))

    def TrainPanel_Adapter(self):

        pass

    def DatasetPanel_Adapter(self):

        pass

    def FrameSelection(self, frame_name):

        self.inference_menu_tab.configure(fg_color="transparent")

        self.train_menu_tab.configure(fg_color="transparent")

        self.dataset_menu_tab.configure(fg_color="transparent")

        self.inference_frame.grid_forget()
        self.train_frame.grid_forget()
        self.dataset_frame.grid_forget()

        if frame_name == "Inference":
            self.inference_menu_tab.configure(fg_color=("gray75", "gray25"))
            self.inference_frame.grid(row=0, column=0, sticky="nsew")
        elif frame_name == "Train":
            self.train_menu_tab.configure(fg_color=("gray75", "gray25"))
            self.train_frame.grid(row=0, column=0, sticky="nsew")
        elif frame_name == "Dataset":
            self.dataset_menu_tab.configure(fg_color=("gray75", "gray25"))
            self.dataset_frame.grid(row=0, column=0, sticky="nsew")

    def InferenceFrame_Event(self):

        self.FrameSelection("Inference")

    def TrainFrame_Event(self):

        self.FrameSelection("Train")

    def DatasetFrame_Event(self):

        self.FrameSelection("Dataset")

    def BrowseFiles_Event(self):

        pass

    def ConfidenceSlider_Event(self, value):

        self.confidence_value_label.configure(text=f"{value:.2f}")

    def IoUSlider_Event(self, value):

        self.iou_value_label.configure(text=f"{value:.2f}")

    def OnClosingApp_Event(self):

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

    def ClearInferenceLog_Event(self):

        pass

