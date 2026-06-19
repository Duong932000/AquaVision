import json
import sys
import customtkinter
from PIL import Image
from datetime import datetime
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
from tkinterdnd2 import TkinterDnD, DND_ALL
from PIL import Image
from PIL import ImageTk

import cv2

# internal modules
from config.assets import asset_resources
from processor.inference_processor import InferenceProcessor

# custom appearance of UI
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


class InferenceLogTextbox(customtkinter.CTkFrame):
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

        timestamp = datetime.now().strftime("%H:%M:%S")
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"[{log_type}] ", log_type)
        self.textbox.insert("end", f"[{timestamp}] ")
        self.textbox.insert("end", f"{message}\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def append(self, message):

        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"{message}\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def clear(self):

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")

class DragnDropSources(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # load tkdnd package
        self.TkdndVersion = TkinterDnD._require(self)

class MainWindow(DragnDropSources):

    width_dashboard = 1300
    height_dashboard = 800

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # inference display variable
        self.inference_config = {}
        self.selected_local_sources = []
        self.selected_youtube_url = []
        self.local_file_checkboxes = []
        self.source_type_var = customtkinter.StringVar(value="Youtube URL")

        # inference control variable
        self.model_selection_var = customtkinter.StringVar(value="Trained")
        self.trained_model_var = customtkinter.StringVar(value="")
        self.pretrained_version_var = customtkinter.StringVar(value="YOLO26")
        self.pretrained_size_var = customtkinter.StringVar(value="n")

        # init UI
        self.GUI_InitSetupResources_Controller()

        # setup widgets for UI
        self.GUI_PanelSetupResources_Controller()

        # start core functionality
        self.GUI_CoreFunctionality_Controller()

    # ------------------- INIT SETUP RESOURCE ------------------- #
    # ------------------------------------------------------------#
    def GUI_InitSetupResources_Controller(self):

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

    # ------------------- PANEL SETUP RESOURCE ------------------- #
    # -------------------------------------------------------------#
    def GUI_PanelSetupResources_Controller(self):

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
        self.FrameSelection_Adapter("Inference")
    
    # MENU PANEL SETUP --------------------------------------------#
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
                                      text=" Inference Models",
                                      command=self.InferenceFrame_Event,
                                      image=self.inference_img,
                                      anchor="w",
                                      height=50,
                                      corner_radius=10,
                                      text_color=("gray10", "gray90"),
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
                                      text_color=("gray10", "gray90"),
                                      font=customtkinter.CTkFont(size=16, slant="italic"))
        self.train_menu_tab.grid(row=2, column=0, padx=15, pady=5, sticky="ew")

        # Dataset menu tab
        self.dataset_menu_tab \
            = customtkinter.CTkButton(self.menu_panel,
                                      text=" Dataset Handling",
                                      command=self.DatasetFrame_Event,
                                      image=self.dataset_img,
                                      anchor="w",
                                      height=50,
                                      corner_radius=10,
                                      text_color=("gray10", "gray90"),
                                      font=customtkinter.CTkFont(size=16, slant="italic"))
        self.dataset_menu_tab.grid(row=3, column=0, padx=15, pady=5, sticky="ew")

        # Spacer
        self.menu_panel.grid_rowconfigure(4, weight=1)

    # DISPLAY PANEL SETUP -----------------------------------------#
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

    # INFERENCE PANEL SETUP ---------------------------------------#
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
        self.InferenceDisplay_WidgetConfigure()
        self.InferenceLog_WidgetConfigure()
        self.InferenceControl_WidgetConfigure()

    def InferenceDisplay_WidgetConfigure(self):

        # ----------------------------------------------------------------------------#
        # Common frame for display inference
        # ----------------------------------------------------------------------------#
        # Display panel label
        self.display_panel_label \
            = customtkinter.CTkLabel(self.inference_video_frame,
                                     text="✓ Display Panel",
                                     font=customtkinter.CTkFont(size=18, weight="bold"))
        self.display_panel_label.pack(anchor="w", padx=5, pady=(10, 5))

        # source type options
        self.source_type_optionmenu \
            = customtkinter.CTkOptionMenu(self.inference_video_frame,
                                          width=150,
                                          height=30,
                                          variable=self.source_type_var,
                                          values=["Youtube URL", "Local Files"],
                                          command=self.SourceTypeChanged_Event)
        self.source_type_optionmenu.pack(anchor="w", padx=5, pady=(10, 5))

        # ----------------------------------------------------------------------------#
        # Local widget configuration
        # ----------------------------------------------------------------------------#
        self.upload_files_label \
            = customtkinter.CTkLabel(self.inference_video_frame,
                                     text="▼ Upload Source Files ▼",
                                     text_color="#90EE90",
                                     font=customtkinter.CTkFont(size=22))

        # drop frame
        self.drop_zone_entry \
            = customtkinter.CTkEntry(self.inference_video_frame,
                                     width=690,
                                     height=200,
                                     placeholder_text="Drag and Drop source files here ...",
                                     justify="center",
                                     corner_radius=15,
                                     border_width=2,
                                     font=customtkinter.CTkFont(size=24))
        self.drop_zone_entry.drop_target_register(DND_ALL)
        self.drop_zone_entry.dnd_bind("<<Drop>>", self.SourcesDrop_Event)
        self.drop_zone_entry.dnd_bind("<<DropEnter>>", self.DropEnter_Event)
        self.drop_zone_entry.dnd_bind("<<DropLeave>>", self.DropLeave_Event)
    
        # or label
        self.or_label \
            = customtkinter.CTkLabel(self.inference_video_frame,
                                     text="Or",
                                     text_color="#90EE90",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))

        # Browse file button
        self.browse_files_button \
            = customtkinter.CTkButton(self.inference_video_frame,
                                      width=50,
                                      height=25,
                                      text="Browse Files",
                                      command=self.BrowseLocalSourceFiles_Event,
                                      font=customtkinter.CTkFont(size=28))

        self.source_files_list_label \
            = customtkinter.CTkLabel(self.inference_video_frame,
                                     text="▼ Source Files List ▼",
                                     text_color="#87CEFA",
                                     font=customtkinter.CTkFont(size=22))

        # source list frame
        self.source_list_checkbox \
            = customtkinter.CTkScrollableFrame(self.inference_video_frame,
                                               width=760, height=390,
                                               border_color="#90EE90")

        # ----------------------------------------------------------------------------#
        # Youtube widget configuration
        # ----------------------------------------------------------------------------#
        # or label
        self.youtube_label \
            = customtkinter.CTkLabel(self.inference_video_frame,
                                     text="▼ Youtube URL: Paste a link to the content you want to inference ▼",
                                     text_color="#90EE90",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))

        # youtube entry
        self.youtube_entry \
            = customtkinter.CTkEntry(self.inference_video_frame,
                                    width=690,
                                    height=50,
                                    placeholder_text="https://www.youtube.com/watch?v=...")

        self.submit_youtube_url_button \
            = customtkinter.CTkButton(self.inference_video_frame,
                                      width=50,
                                      height=25,
                                      text="Submit URL",
                                      command=self.SubmitYoutubeSources_Event,
                                      font=customtkinter.CTkFont(size=28))

        self.SourceTypeChanged_Event(self.source_type_var.get())

    def SourceTypeChanged_Event(self, source_type):

        # Hide all widgets first
        self.upload_files_label.pack_forget()
        self.drop_zone_entry.pack_forget()
        self.or_label.pack_forget()
        self.browse_files_button.pack_forget()
        self.youtube_label.pack_forget()
        self.youtube_entry.pack_forget()
        self.submit_youtube_url_button.pack_forget()
        self.source_files_list_label.pack_forget()
        self.source_list_checkbox.pack_forget()

        if source_type == "Youtube URL":
            self.youtube_label.pack(anchor="center", padx=5, pady=(50, 10))
            self.youtube_entry.pack(anchor="center", pady=(10, 10))
            self.submit_youtube_url_button.pack(anchor="center", pady=(50, 10))
        elif source_type == "Local Files":
            self.upload_files_label.pack(anchor="center", padx=5, pady=(50, 10))
            self.drop_zone_entry.pack(anchor="center", pady=(10, 5))
            self.or_label.pack(anchor="center", pady=(5, 5))
            self.browse_files_button.pack(anchor="center", pady=(5, 10))
            self.source_files_list_label.pack(anchor="center", pady=(50, 10))
            self.source_list_checkbox.pack(anchor="center", padx=5, pady=10)

    def SourcesDrop_Event(self, event):

        filepath = event.data.strip()

        if filepath.startswith("{"):
            filepath = filepath[1:-1]

        if filepath not in self.selected_local_sources:
            self.selected_local_sources.append(filepath)
            self.AppendInferenceLog_Event("INFO", f"Source added: {filepath}")

        self.ShowLocalSourceFiles_Event()

    def DropEnter_Event(self, event):

        self.drop_zone_entry.configure(border_width=2, border_color="#00AA55")

        return event.action

    def DropLeave_Event(self, event):

        self.drop_zone_entry.configure(border_width=1, border_color=("gray50", "gray50"))

        return event.action

    def BrowseLocalSourceFiles_Event(self):

        filepaths = filedialog.askopenfilenames(
            title="Select Source Files",
            filetypes=[
                (
                    "Media Files",
                    "*.jpg *.jpeg *.png *.bmp *.mp4 *.avi *.mov *.mkv"
                )
            ]
        )

        if not filepaths:
            return

        for filepath in filepaths:
            if filepath not in self.selected_local_sources:
                self.selected_local_sources.append(filepath)

        self.ShowLocalSourceFiles_Event()
        self.AppendInferenceLog_Event("INFO", f"Added {len(filepaths)} source files")

    def ShowLocalSourceFiles_Event(self):

        for widget in self.source_list_checkbox.winfo_children():
            widget.destroy()

        self.local_file_checkboxes.clear()

        # select all show
        self.select_all_var = customtkinter.BooleanVar(value=True)
        select_all_checkbox \
            = customtkinter.CTkCheckBox(self.source_list_checkbox,
                                        text="Select All",
                                        variable=self.select_all_var,
                                        command=self.SelectAllSources_Event)
        select_all_checkbox.pack(anchor="w", padx=10, pady=(10, 20))

        # individual file checkboxes
        for filepath in self.selected_local_sources:
            var = customtkinter.BooleanVar(value=True)
            checkbox \
                = customtkinter.CTkCheckBox(self.source_list_checkbox, text=filepath, variable=var)
            checkbox.pack(anchor="w", padx=25, pady=5)
            self.local_file_checkboxes.append((filepath, var))

        submit_button \
            = customtkinter.CTkButton(self.source_list_checkbox,
                                      text="Submit Sources",
                                      command=self.SubmitLocalSources_Event)
        submit_button.pack(anchor="center", pady=25)

    def SelectAllSources_Event(self):

        state = self.select_all_var.get()

        for _, var in self.local_file_checkboxes:
            var.set(state)

    def SubmitLocalSources_Event(self):

        selected_files = []

        for filepath, var in self.local_file_checkboxes:
            if var.get():
                selected_files.append(filepath)

        if not selected_files:
            self.AppendInferenceLog_Event("ERROR", "No source files selected!")
            return
        
        self.selected_local_sources = selected_files

        config = self.BuildInferenceConfig_Event()

        self.AppendInferenceLog_Event("INFO", f"Local source: {len(selected_files)} files submitted")

        print(json.dumps(config, indent=4))

    def SubmitYoutubeSources_Event(self):

        url = self.youtube_entry.get().strip()
        if not url:
            self.AppendInferenceLog_Event("ERROR", "Please enter a youtube URL")
            return

        if not url:
            self.AppendInferenceLog_Event("ERROR", "Please enter a Youtube URL")
            return
        
        self.selected_youtube_url = url

        config = self.BuildInferenceConfig_Event()

        self.AppendInferenceLog_Event("INFO", f"Youtube URL selected: {url}")

        print(json.dumps(config, indent=4))

    def InferenceLog_WidgetConfigure(self):
        
        # Inference log label
        self.inference_log_label \
            = customtkinter.CTkLabel(self.inference_log_frame,
                                     text="✓ Inference log",
                                     font=customtkinter.CTkFont(size=18, weight="bold"))
        self.inference_log_label.pack(anchor="w", padx=15, pady=(10, 5))

        # Clear Log button
        self.clear_log_button \
            = customtkinter.CTkButton(self.inference_log_frame,
                                      text="Clear log",
                                      command=self.ClearInferenceLog_Event,
                                      font=customtkinter.CTkFont(size=14, slant="italic"))
        self.clear_log_button.pack(anchor="w", padx=15, pady=(5, 10))

        # Inference Progress textbox
        self.inference_log_textbox \
            = InferenceLogTextbox(self.inference_log_frame)
        self.inference_log_textbox.pack(fill="both", expand=True, padx=10, pady=(10, 10))

    def AppendInferenceLog_Event(self, log_type, message):

        self.inference_log_textbox.append_log(log_type, message)

    def ClearInferenceLog_Event(self):

        self.inference_log_textbox.clear()

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
        #                                  MODEL CONFIGURE                              #
        #-------------------------------------------------------------------------------#
        # Model label
        self.model_selection_label \
            = customtkinter.CTkLabel(self.control_scroll_frame,
                                     text="✓ Model Selection:",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.model_selection_label.pack(anchor="w", padx=10, pady=(15, 5))
 
        # model frame
        self.model_selection_frame \
            = customtkinter.CTkFrame(self.control_scroll_frame, fg_color="transparent")
        self.model_selection_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Trained model radio button
        self.trained_radio \
            = customtkinter.CTkRadioButton(self.model_selection_frame,
                                           text="Trained Model",
                                           variable=self.model_selection_var,
                                           value="Trained",
                                           command=self.ModelSourceChanged_Event)
        self.trained_radio.pack(anchor="w", padx=10, pady=(5, 5))

        # Pre-Trained model radio button
        self.pretrained_radio \
            = customtkinter.CTkRadioButton(self.model_selection_frame,
                                           text="Pretrained Model",
                                           variable=self.model_selection_var,
                                           value="Pretrained",
                                           command=self.ModelSourceChanged_Event)
        self.pretrained_radio.pack(anchor="w", padx=10, pady=(5, 10))

        # trained model frame
        self.trained_model_frame = customtkinter.CTkFrame(self.model_selection_frame, fg_color="transparent")
        self.trained_model_frame.pack(fill="x", pady=5)

        # browse trained model button
        self.browse_model_button \
            = customtkinter.CTkButton(self.trained_model_frame,
                                      width=40,
                                      height=30,
                                      text="Browse Model Path",
                                      command=self.BrowseModel_Event,
                                      font=customtkinter.CTkFont(size=14))
        self.browse_model_button.pack(anchor="w", padx=5, pady=10)

        # pretrained model frame
        self.pretrained_model_frame \
            = customtkinter.CTkFrame(self.model_selection_frame, fg_color="transparent")

        # model version optionmenu
        self.pretrained_model_version_optionmenu \
            = customtkinter.CTkOptionMenu(self.pretrained_model_frame,
                                          variable=self.pretrained_version_var,
                                          values=["YOLO26", "YOLO11", "YOLOv8"])
        self.pretrained_model_version_optionmenu.pack(fill="x", pady=(0, 10))

        self.pretrained_model_type_optionmenu \
            = customtkinter.CTkOptionMenu(self.pretrained_model_frame,
                                         variable=self.pretrained_size_var,
                                         values=["n", "s", "m", "l", "x"])
        self.pretrained_model_type_optionmenu.pack(fill="x")

        #-------------------------------------------------------------------------------#
        #                                TRACKER CONFIGURE                              #
        #-------------------------------------------------------------------------------#
        # Tracking label
        self.tracker_label \
            = customtkinter.CTkLabel(self.control_scroll_frame,
                                     text="✓ MOT Tracker:",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.tracker_label.pack(anchor="w", padx=10, pady=(15, 5))

        # Tracking checkbox
        self.enable_tracking_checkbox \
            = customtkinter.CTkCheckBox(self.control_scroll_frame, text="Enable Tracking")
        self.enable_tracking_checkbox.select()
        self.enable_tracking_checkbox.pack(anchor="w", padx=10, pady=5)

        # Tracker combobox
        self.tracker_combobox \
            = customtkinter.CTkComboBox(self.control_scroll_frame,
                                        values=["ByteTrack", "BoT-SORT"])
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
                                      command=self.StartInference_Event,
                                      height=40,
                                      font=customtkinter.CTkFont(size=14))
        self.start_button.pack(fill="x", padx=10, pady=(25, 10))

        # Stop inference button
        self.stop_button \
            = customtkinter.CTkButton(self.control_scroll_frame,
                                      text="Stop Inference",
                                      command=self.StopInference_Event,
                                      height=40,
                                      fg_color="darkred",
                                      font=customtkinter.CTkFont(size=14))
        self.stop_button.pack(fill="x", padx=10, pady=(5, 20))

        self.ModelSourceChanged_Event()

    def BuildInferenceConfig_Event(self):

        config = {}

        # source process
        source_type = self.source_type_var.get()
        if source_type == "Local Files":
            config["source_type"] = "local"
            config["sources"] = self.selected_local_sources
        else:
            config["source_type"] = "youtube"
            if self.selected_youtube_url:
                config["sources"] = [self.selected_youtube_url]
            else:
                config["sources"] = []
        
        # model path process
        config["model"] = {
            "model_selection": self.model_selection_var.get()
        }
        
        if self.model_selection_var.get() == "Trained":
            config["model"]["path"] = self.trained_model_var.get()
        else:
            config["model"]["version"] = self.pretrained_version_var.get()
            config["model"]["size"] = self.pretrained_size_var.get()

        # tracker process
        config["tracking"] = {
            "enabled": bool(self.enable_tracking_checkbox.get()),
            "tracker": self.tracker_combobox.get()
        }

        # detection process
        config["detection"] = {
            "confidence": round(self.confidence_slider.get(), 2),
            "iou": round(self.iou_slider.get(), 2)
        }

        # output process
        config["output"] = {
            "save_video": bool(self.save_video_checkbox.get()),
            "save_frames": bool(self.save_frames_checkbox.get())
        }

        # runtime process
        config["runtime"] = {
            "device": self.device_combobox.get()
        }

        self.inference_config = config

        return config

    def ModelSourceChanged_Event(self):

        if self.model_selection_var.get() == "Trained":
            self.pretrained_model_frame.pack_forget()
            self.trained_model_frame.pack(fill="x", pady=5)
        else:
            self.trained_model_frame.pack_forget()
            self.pretrained_model_frame.pack(fill="x", pady=5)

    def BrowseModel_Event(self):

        filepath = filedialog.askopenfilename(title="Select YOLO Model",
                                              filetypes=[("PyTorch Model", "*.pt")])

        if not filepath:
            return

        self.trained_model_var.set(filepath)

        self.AppendInferenceLog_Event("INFO", f"Model selected: {filepath}")

    def ConfidenceSlider_Event(self, value):

        self.confidence_value_label.configure(text=f"{value:.2f}")

    def IoUSlider_Event(self, value):

        self.iou_value_label.configure(text=f"{value:.2f}")

    def StartInference_Event(self):

        config = self.BuildInferenceConfig_Event()

        if not config["sources"]:

            self.AppendInferenceLog_Event(
                "ERROR",
                "No source selected"
            )
            return

        self.processor = InferenceProcessor(
            config=config,
            frame_callback=self.UpdateInferenceFrame_Event,
            log_callback=self.AppendInferenceLog_Event
        )

        self.processor.start()

    def StopInference_Event(self):

        if hasattr(self, "processor"):

            self.processor.stop()

    def UpdateInferenceFrame_Event(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(rgb)

        image = image.resize(
            (
                self.video_display_label.winfo_width(),
                self.video_display_label.winfo_height()
            )
        )

        photo = ImageTk.PhotoImage(image)

        self.video_display_label.configure(
            image=photo,
            text=""
        )

        self.video_display_label.image = photo

    # TRAIN PANEL SETUP -------------------------------------------#
    def TrainPanel_Adapter(self):

        pass

    # DATASET PANEL SETUP -----------------------------------------#
    def DatasetPanel_Adapter(self):

        pass

    # FRAME SELECTION SETUP ---------------------------------------#
    def FrameSelection_Adapter(self, frame_name):

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

        self.FrameSelection_Adapter("Inference")

    def TrainFrame_Event(self):

        self.FrameSelection_Adapter("Train")

    def DatasetFrame_Event(self):

        self.FrameSelection_Adapter("Dataset")

    # ------------------- FUNCTIONALITY SETUP RESOURCE ------------------- #
    # ---------------------------------------------------------------------#
    def GUI_CoreFunctionality_Controller(self):

        pass