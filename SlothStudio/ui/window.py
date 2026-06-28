
import cv2
import sys
import time
import numpy
import customtkinter
from PIL import Image, ImageTk
from queue import Queue, Empty
from CTkMessagebox import CTkMessagebox

# internal modules
from utils.log_textbox import LogTextboxUtils
from ui.dragdrop import DND_ALL, DnD
from ui.assets import asset_resources
from utils.filedialog import FileDialogUtils
from processor.system_monitor import SystemUsageMonitor
from processor.inference_processor import InferenceProcessor
from processor.training_processor import TrainingProcessor


# custom appearance of UI
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class MainWindow(DnD):

    width_dashboard = 1300
    height_dashboard = 800

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.init_cfg = config
        self.model_cfg = self.init_cfg["models"]
        self.tracker_cfg = self.init_cfg["trackers"]
        self.inference_cfg = self.init_cfg["inference"]
        self.train_cfg = self.init_cfg["training"]

        # --------------------------------------------------------------------------#
        # MODELS VARIABLES ---------------------------------------------------------#
        # --------------------------------------------------------------------------#
        self.yolo_versions_list_var = self.model_cfg["families"]["yolo"]["versions"]      # ["YOLO26", "YOLO12", "YOLO11", "YOLOv10", "YOLOv9", "YOLOv9", "YOLOv8"]
        self.yolo_sizes_list_var = self.model_cfg["families"]["yolo"]["sizes"]            # ["n", "s", "m", "l", "x"]
        self.rtdetr_versions_list_var = self.model_cfg["families"]["rt-detr"]["versions"] # ["RT-DETR", "RT-DETRv2"]
        self.rtdetr_sizes_list_var = self.model_cfg["families"]["rt-detr"]["sizes"]       # ["l", "x"]
        self.rfdetr_versions_list_var = self.model_cfg["families"]["rf-detr"]["versions"] # ["RF-DETR"]
        self.rfdetr_sizes_list_var = self.model_cfg["families"]["rf-detr"]["sizes"]       # ["n", "s", "m", "l", "xl", "2xl"]


        # --------------------------------------------------------------------------#
        # INFERENCE VARIABLES ------------------------------------------------------#
        # --------------------------------------------------------------------------#
        # inference mode
        self.inference_mode = False

        # inference config json
        self.inference_config = {}

        # varible for optionmenu source type
        self.source_type_var \
            = customtkinter.StringVar(
                value=self.inference_cfg["source"]["default_type"])

        self.source_type_list_var = self.inference_cfg["source"]["source_types"]

        # variables for source local
        self.selected_local_sources = []
        self.local_file_checkboxes = []

        # variables for youtube source
        self.youtube_url_var \
            = customtkinter.StringVar(value="")

        # variable model selection
        self.model_selection_var \
            = customtkinter.StringVar(
                value=self.inference_cfg["models"]["default_mode"])

        self.trained_model_var \
            = customtkinter.StringVar(value="")                

        self.pretrained_version_var = customtkinter.StringVar(
            value=self.inference_cfg["models"]["pretrained"]["default_version"])

        self.pretrained_size_var = customtkinter.StringVar(
            value=self.inference_cfg["models"]["pretrained"]["default_size"])

        # variables for tracking
        self.enable_tracking_var = customtkinter.BooleanVar(
            value=self.inference_cfg["tracking"]["enabled"])

        self.tracker_var \
            = customtkinter.StringVar(
                value=self.inference_cfg["tracking"]["default_tracker"])
        
        self.tracker_list_var \
            = self.tracker_cfg["availabel"]  # ["BoT-SORT", "ByteTrack", "Deep OC-SORT", "OC-SORT", "FastTracker", "TrackTrack"]

        # variable for detection
        self.confidence_var \
            = customtkinter.DoubleVar(
                value=self.inference_cfg["detection"]["confidence"]["default"])
        
        self.confidence_min_var = self.inference_cfg["detection"]["confidence"]["min"]
        self.confidence_max_var = self.inference_cfg["detection"]["confidence"]["max"]

        # IOU - Intersection over Union
        self.iou_var \
            = customtkinter.DoubleVar(
                value=self.inference_cfg["detection"]["iou"]["default"])

        self.iou_min_var = self.inference_cfg["detection"]["iou"]["min"]
        self.iou_max_var = self.inference_cfg["detection"]["iou"]["max"]

        self.image_size_var \
            = customtkinter.StringVar(
                value=self.inference_cfg["detection"]["image_size"]["default"])
        self.image_size_list_var = self.inference_cfg["detection"]["image_size"]["options"]

        self.fp16_enabled_var \
            = customtkinter.BooleanVar(
                value=self.inference_cfg["detection"]["fp16"]["default"])

        self.max_detection_var \
            = customtkinter.StringVar(
                value=self.inference_cfg["detection"]["max_detection"]["default"])
        self.max_detection_list_var = self.inference_cfg["detection"]["max_detection"]["options"]

        # varible for output mode
        self.save_video_var \
            = customtkinter.BooleanVar(
                value=self.inference_cfg["output"]["save_video"]["default"])

        self.save_frames_var \
            = customtkinter.BooleanVar(
                value=self.inference_cfg["output"]["save_frames"]["default"])

        # variable for runtime
        self.device_var \
            = customtkinter.StringVar(
                value=self.inference_cfg["runtime"]["default_device"])
        self.device_list_var = self.inference_cfg["runtime"]["options"]

        # flag of inference processor
        self.inference_processor = None

        # frame queue
        self.frame_queue = Queue(maxsize=1)
        self.last_frame_time = 0

        # --------------------------------------------------------------------------#
        # TRAINING VARIABLES -------------------------------------------------------#
        # --------------------------------------------------------------------------#
        self.training_config = {}
        self.training_processor = None

        self.dataset_yaml_var \
            = customtkinter.StringVar(
                value=self.train_cfg["dataset"]["dataset_yaml"])
    
        self.model_family_var \
            = customtkinter.StringVar(
                value=self.train_cfg["models"]["default_family"])

        self.model_family_list_var = self.train_cfg["models"]["model_family"]

        self.model_version_var = customtkinter.StringVar(value="")

        self.model_size_var = customtkinter.StringVar(value="")

        # variable for training
        self.epochs_var \
            = customtkinter.StringVar(
                value=self.train_cfg["hyperparameters"]["epochs"]["default"])

        self.batch_size_var \
            = customtkinter.StringVar(
                value=self.train_cfg["hyperparameters"]["batch_size"]["default"])

        self.batch_size_list_var = self.train_cfg["hyperparameters"]["batch_size"]["options"]

        self.train_image_size_var \
            = customtkinter.StringVar(
                value=self.train_cfg["hyperparameters"]["image_size"]["default"])
        
        self.train_image_size_list_var \
            = self.train_cfg["hyperparameters"]["image_size"]["options"]

        self.train_workers_var \
            = customtkinter.StringVar(
                value=self.train_cfg["hyperparameters"]["workers"]["default"])

        self.train_amp_var \
            = customtkinter.BooleanVar(
                value=self.train_cfg["hyperparameters"]["amp"]["default"])

        self.run_validation_var \
            = customtkinter.BooleanVar(
                value=self.train_cfg["validation"]["run_validation"]["default"])

        self.show_result_validation_var \
            = customtkinter.BooleanVar(
                value=self.train_cfg["validation"]["show_result"]["default"])

        # variable for models export
        self.export_onnx_var \
            = customtkinter.BooleanVar(
                value=self.train_cfg["export"]["onnx"]["default"])

        self.export_tensorrt_var \
            = customtkinter.BooleanVar(
                value=self.train_cfg["export"]["tensorrt"]["default"])

        # Monitoring object
        self.system_monitor = SystemUsageMonitor()

        # init UI
        self.GUI_InitSetupResources_Controller()

        # functionality UI
        self.GUI_CoreFunctionality_Controller()

        self.after(30, self.RenderInferenceFrameLoop_Event)
        self.after(1000, self.UpdateSystemMonitor_Event)

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

        self.monitoring_img = customtkinter.CTkImage(
            Image.open(asset_resources("monitoring.png")), size=(30, 30))

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

    # -------------------- CORE FUNCTIONALITY -------------------- #
    # -------------------------------------------------------------#
    def GUI_CoreFunctionality_Controller(self):

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
    # -------------------------------------------------------------#
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

        # System Monitor frame
        self.system_monitor_frame \
            = customtkinter.CTkFrame(self.menu_panel, corner_radius=10)
        self.system_monitor_frame.grid(row=4, column=0, padx=15, pady=(10, 10), sticky="ew")

        self.system_monitor_title \
            = customtkinter.CTkButton(self.system_monitor_frame,
                                      text=" System Monitor",
                                      anchor="w",
                                      state="disabled",
                                      fg_color="transparent",
                                      text_color=("gray10", "gray90"),
                                      hover_color=("gray70", "gray30"),
                                      image=self.monitoring_img,
                                      font=customtkinter.CTkFont(size=16, slant="italic"))
        self.system_monitor_title.pack(anchor="w", padx=0, pady=(10, 5))

        self.cpu_label \
            = customtkinter.CTkLabel(self.system_monitor_frame, text="CPU: 0%")
        self.cpu_label.pack(anchor="w", padx=10)

        self.ram_label \
            = customtkinter.CTkLabel(self.system_monitor_frame, text="RAM: 0 / 0 GB")
        self.ram_label.pack(anchor="w", padx=10)

        self.gpu_label \
            = customtkinter.CTkLabel(self.system_monitor_frame, text="GPU: N/A")
        self.gpu_label.pack(anchor="w", padx=10)

        self.vram_label \
            = customtkinter.CTkLabel(self.system_monitor_frame, text="VRAM: N/A")
        self.vram_label.pack(anchor="w", padx=10, pady=(0, 10))

        # show menu panel
        self.menu_panel.grid_rowconfigure(5, weight=1)

        # runtime mode frame
        self.inference_runtime_mode_frame \
            = customtkinter.CTkFrame(self.menu_panel, corner_radius=10)

        self.stop_inference_button \
            = customtkinter.CTkButton(self.inference_runtime_mode_frame,
                                      text="Stop Inference",
                                      command=self.StopInference_Event)
        self.stop_inference_button.pack(fill="x", padx=10, pady=(10, 10))

        self.inference_runtime_mode_log_textbox \
            = LogTextboxUtils(self.inference_runtime_mode_frame)
        self.inference_runtime_mode_log_textbox.pack(fill="both", expand=True, padx=5, pady=5)

    def UpdateSystemMonitor_Event(self):

        usage = self.system_monitor.get_usage()

        self.cpu_label.configure(text=f"CPU: {usage['cpu_percent']:.1f}%")

        self.ram_label.configure(text=f"RAM: "f"{usage['ram_used_gb']:.1f} / {usage['ram_total_gb']:.1f} GB")

        if usage["gpu_percent"] is not None:
            self.gpu_label.configure(text=f"GPU: {usage['gpu_percent']:.1f}%")
            self.vram_label.configure(text=f"VRAM: {usage['gpu_memory_used_gb']:.1f} / {usage['gpu_memory_total_gb']:.1f} GB")
        else:
            self.gpu_label.configure(text="GPU: N/A")
            self.vram_label.configure(text="VRAM: N/A")
        self.after(1000,self.UpdateSystemMonitor_Event)

    # DISPLAY PANEL SETUP -----------------------------------------#
    # -------------------------------------------------------------#
    def DisplayPanel_Adapter(self):

        # inference frame
        self.inference_frame \
            = customtkinter.CTkFrame(self.display_panel, corner_radius=10, fg_color="transparent")

        # train frame
        self.training_frame \
            = customtkinter.CTkFrame(self.display_panel, corner_radius=10, fg_color="transparent")

        # dataset frame
        self.dataset_frame \
            = customtkinter.CTkFrame(self.display_panel, corner_radius=10, fg_color="transparent")

        for frame in (self.inference_frame, self.training_frame, self.dataset_frame):
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        # fullscreen inference mode
        self.fullscreen_inference_mode_label \
            = customtkinter.CTkLabel(self.display_panel, text="")

    # INFERENCE PANEL SETUP ---------------------------------------#
    # -------------------------------------------------------------#
    def InferencePanel_Adapter(self):

        # setup rate of inference_frame
        self.inference_frame.grid_columnconfigure(0, weight=9)
        self.inference_frame.grid_columnconfigure(1, weight=1)
        self.inference_frame.grid_columnconfigure(2, weight=1)
        self.inference_frame.grid_rowconfigure(0, weight=1)

        # Create Subframes
        # inference display frame
        self.inference_display_frame \
            = customtkinter.CTkFrame(self.inference_frame, corner_radius=10)
        self.inference_display_frame.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="snew")
        self.inference_display_frame.grid_rowconfigure(0, weight=1)
        self.inference_display_frame.grid_columnconfigure(0, weight=1)

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

        # call infernence source input function
        self.InferenceSourceInput_WidgetsConfigure()

        # call infernece log function
        self.InferenceLog_WidgetsConfigure()

        # call inference control function
        self.InferenceControl_WidgetsConfigure()

    # Inference Source Input widgets setup
    def InferenceSourceInput_WidgetsConfigure(self):

        # ----------------------------------------------------------------------------#
        # Common frame for display inference
        # ----------------------------------------------------------------------------#
        # Display panel label
        self.inference_source_input_panel \
            = customtkinter.CTkLabel(self.inference_display_frame,
                                     text="✓ Source Input Panel",
                                     font=customtkinter.CTkFont(size=18, weight="bold"))
        self.inference_source_input_panel.pack(anchor="w", padx=5, pady=(10, 5))

        # source type options
        self.source_type_optionmenu \
            = customtkinter.CTkOptionMenu(self.inference_display_frame,
                                          width=200,
                                          height=30,
                                          variable=self.source_type_var,
                                          values=self.source_type_list_var,
                                          command=self.UpdateUISourceTypeChanged_Event)
        self.source_type_optionmenu.pack(anchor="w", padx=5, pady=(10, 5))

        # ----------------------------------------------------------------------------#
        # Youtube widget configuration
        # ----------------------------------------------------------------------------#
        # youtube message label
        self.youtube_message_label \
            = customtkinter.CTkLabel(self.inference_display_frame,
                                     text="▼ Youtube URL: Paste a link to the content you want to inference ▼",
                                     text_color="#90EE90",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))

        # youtube entry
        self.youtube_entry \
            = customtkinter.CTkEntry(self.inference_display_frame,
                                     textvariable=self.youtube_url_var,
                                     width=690,
                                     height=50,
                                     placeholder_text="https://www.youtube.com/watch?v=...")

        # clear button
        self.clear_url_button \
            = customtkinter.CTkButton(self.inference_display_frame,
                                      width=25,
                                      height=25,
                                      text="Clear URL",
                                      command=self.ClearURL_Event,
                                      font=customtkinter.CTkFont(size=14))

        self.submit_youtube_url_button \
            = customtkinter.CTkButton(self.inference_display_frame,
                                      width=50,
                                      height=25,
                                      text="Submit URL",
                                      command=self.SubmitYoutubeSources_Event,
                                      font=customtkinter.CTkFont(size=28))

        # ----------------------------------------------------------------------------#
        # Local widget configuration
        # ----------------------------------------------------------------------------#
        self.upload_files_label \
            = customtkinter.CTkLabel(self.inference_display_frame,
                                     text="▼ Upload Source Files ▼",
                                     text_color="#90EE90",
                                     font=customtkinter.CTkFont(size=22))

        # drop frame
        self.drop_zone_entry \
            = customtkinter.CTkEntry(self.inference_display_frame,
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
            = customtkinter.CTkLabel(self.inference_display_frame,
                                     text="Or",
                                     text_color="#90EE90",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))

        # Browse file button
        self.browse_files_button \
            = customtkinter.CTkButton(self.inference_display_frame,
                                      width=50,
                                      height=25,
                                      text="Browse Files",
                                      command=self.BrowseLocalSourceFiles_Event,
                                      font=customtkinter.CTkFont(size=28))

        self.source_files_list_label \
            = customtkinter.CTkLabel(self.inference_display_frame,
                                     text="▼ Source Files List ▼",
                                     text_color="#87CEFA",
                                     font=customtkinter.CTkFont(size=22))

        # source list frame
        self.source_list_checkbox \
            = customtkinter.CTkScrollableFrame(self.inference_display_frame,
                                               width=760, height=390,
                                               border_color="#90EE90")
        
        # Init 
        self.UpdateUISourceTypeChanged_Event(self.source_type_var.get())

    def UpdateUISourceTypeChanged_Event(self, source_type):

        # Hide all widgets first

        # youtube source widgets
        self.youtube_message_label.pack_forget()
        self.youtube_entry.pack_forget()
        self.clear_url_button.pack_forget()
        self.submit_youtube_url_button.pack_forget()

        # local source widgets
        self.upload_files_label.pack_forget()
        self.drop_zone_entry.pack_forget()
        self.or_label.pack_forget()
        self.browse_files_button.pack_forget()
        self.source_files_list_label.pack_forget()
        self.source_list_checkbox.pack_forget()

        if source_type == "Youtube URL":
            self.youtube_message_label.pack(anchor="center", padx=5, pady=(50, 10))
            self.youtube_entry.pack(anchor="center", pady=(10, 10))
            self.clear_url_button.pack(anchor="w", padx=80, pady=(10, 10))
            self.submit_youtube_url_button.pack(anchor="center", pady=(50, 10))
        elif source_type == "Local Files":
            self.upload_files_label.pack(anchor="center", padx=5, pady=(50, 10))
            self.drop_zone_entry.pack(anchor="center", pady=(10, 5))
            self.or_label.pack(anchor="center", pady=(5, 5))
            self.browse_files_button.pack(anchor="center", pady=(5, 10))
            self.source_files_list_label.pack(anchor="center", pady=(50, 10))
            self.source_list_checkbox.pack(anchor="center", padx=5, pady=10)

    def SubmitYoutubeSources_Event(self):

        # get youtube url from youtube url var entry
        youtube_url = self.youtube_url_var.get().strip()

        if not youtube_url:
            self.AppendInferenceLog_Event("ERROR", "Please enter a youtube URL")
            return

        self.AppendInferenceLog_Event("INFO", f"Youtube URL selected: {youtube_url}")

    def ClearURL_Event(self):
        
        # reset youtube url var to empty
        self.youtube_url_var.set("")

        self.AppendInferenceLog_Event("INFO", "Youtube URL cleared")

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

        filepaths \
            = FileDialogUtils.BrowseFiles(title="Select Source Files",
                                          filetypes=[("Media Files", "*.jpg *.jpeg *.png *.bmp *.mp4 *.avi *.mov *.mkv")])
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

        self.BuildInferenceConfig_Event()

        self.AppendInferenceLog_Event("INFO", f"Local source: {len(selected_files)} files submitted")

    # Inference Log widgets setup
    def InferenceLog_WidgetsConfigure(self):
        
        # Inference log label
        self.inference_log_label \
            = customtkinter.CTkLabel(self.inference_log_frame,
                                     text="✓ Inference log",
                                     font=customtkinter.CTkFont(size=18, weight="bold"))
        self.inference_log_label.pack(anchor="w", padx=15, pady=(10, 5))

        # Clear Log button
        self.inference_clearn_log_button \
            = customtkinter.CTkButton(self.inference_log_frame,
                                      text="Clear Log",
                                      command=self.ClearInferenceLog_Event,
                                      font=customtkinter.CTkFont(size=16, slant="italic"))
        self.inference_clearn_log_button.pack(anchor="w", padx=15, pady=(5, 10))

        # Inference Progress textbox
        self.inference_log_textbox \
            = LogTextboxUtils(self.inference_log_frame)
        self.inference_log_textbox.pack(fill="both", expand=True, padx=10, pady=(10, 10))

    def AppendInferenceLog_Event(self, log_type, message):

        targets = [self.inference_log_textbox]

        if self.inference_mode:
            targets.append(self.inference_runtime_mode_log_textbox)
        
        LogTextboxUtils.Broadcast(targets, log_type, message)

    def ClearInferenceLog_Event(self):

        self.inference_log_textbox.clear()

    # Inference Control widgets setup
    def InferenceControl_WidgetsConfigure(self):

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
        self.inference_control_scroll_frame \
            = customtkinter.CTkScrollableFrame(self.inference_control_tab, corner_radius=10)
        self.inference_control_scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)


        #-------------------------------------------------------------------------------#
        #                                  MODEL CONFIGURE                              #
        #-------------------------------------------------------------------------------#
        # model selection label
        self.model_selection_label \
            = customtkinter.CTkLabel(self.inference_control_scroll_frame,
                                     text="✓ Model Selection:",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.model_selection_label.pack(anchor="w", padx=10, pady=(15, 5))
 
        # model frame (able to show Trained Model and Pretrained Model widgets when changing radio button type)
        self.model_selection_frame \
            = customtkinter.CTkFrame(self.inference_control_scroll_frame, fg_color="transparent")
        self.model_selection_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Trained model radio button
        self.trained_model_radio \
            = customtkinter.CTkRadioButton(self.model_selection_frame,
                                           text="Trained Model",
                                           variable=self.model_selection_var,
                                           value="Trained",
                                           command=self.ModelSelectionUIChanged_Event)
        self.trained_model_radio.pack(anchor="w", padx=10, pady=(5, 5))

        # Pre-Trained model radio button
        self.pretrained_model_radio \
            = customtkinter.CTkRadioButton(self.model_selection_frame,
                                           text="Pretrained Model",
                                           variable=self.model_selection_var,
                                           value="Pretrained",
                                           command=self.ModelSelectionUIChanged_Event)
        self.pretrained_model_radio.pack(anchor="w", padx=10, pady=(5, 10))

        # trained model frame
        self.trained_model_frame \
            = customtkinter.CTkFrame(self.model_selection_frame, fg_color="transparent")
        self.trained_model_frame.pack(fill="x", pady=5)

        # browse trained model button
        self.browse_model_button \
            = customtkinter.CTkButton(self.trained_model_frame,
                                      text="Browse Trained Model",
                                      command=self.BrowseTrainedModel_Event,
                                      width=40,
                                      height=30,
                                      font=customtkinter.CTkFont(size=14))
        self.browse_model_button.pack(anchor="w", padx=5, pady=5)

        # pretrained model frame
        self.pretrained_model_frame \
            = customtkinter.CTkFrame(self.model_selection_frame, fg_color="transparent")

        # model version optionmenu
        self.pretrained_model_version_optionmenu \
            = customtkinter.CTkOptionMenu(self.pretrained_model_frame,
                                          variable=self.pretrained_version_var,
                                          values=self.yolo_versions_list_var)
        self.pretrained_model_version_optionmenu.pack(fill="x", pady=(0, 10))

        self.pretrained_model_type_optionmenu \
            = customtkinter.CTkOptionMenu(self.pretrained_model_frame,
                                         variable=self.pretrained_size_var,
                                         values=self.yolo_sizes_list_var)
        self.pretrained_model_type_optionmenu.pack(fill="x")

        #-------------------------------------------------------------------------------#
        #                                TRACKER CONFIGURE                              #
        #-------------------------------------------------------------------------------#
        # Tracking label
        self.tracker_label \
            = customtkinter.CTkLabel(self.inference_control_scroll_frame,
                                     text="✓ MOT Tracker:",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.tracker_label.pack(anchor="w", padx=10, pady=(0, 5))

        # Tracking checkbox (default is True, follow define of self.enable_tracking_var)
        self.enable_tracking_checkbox \
            = customtkinter.CTkCheckBox(self.inference_control_scroll_frame,
                                        text="Enable Tracking",
                                        variable=self.enable_tracking_var)
        self.enable_tracking_checkbox.select()
        self.enable_tracking_checkbox.pack(anchor="w", padx=10, pady=5)

        # Tracker combobox (default is BoT-SORT)
        self.tracker_combobox \
            = customtkinter.CTkComboBox(self.inference_control_scroll_frame,
                                        variable=self.tracker_var,
                                        values=self.tracker_list_var)
        self.tracker_combobox.set("BoT-SORT")
        self.tracker_combobox.pack(fill="x", padx=10, pady=10)

        #-------------------------------------------------------------------------------#
        #                       DETECTION PARAMETERS CONFIGURE                          #
        #-------------------------------------------------------------------------------#
        # detection parameters label
        self.detection_parameters_label \
            = customtkinter.CTkLabel(self.inference_control_scroll_frame,
                                    text="✓ Detection Parameters",
                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.detection_parameters_label.pack(anchor="w", padx=10, pady=(5, 5))

        self.confidence_frame \
            = customtkinter.CTkFrame(self.inference_control_scroll_frame, fg_color="transparent")
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
            = customtkinter.CTkSlider(self.inference_control_scroll_frame,
                                      variable=self.confidence_var,
                                      command=self.ConfidenceSlider_Event,
                                      from_=self.confidence_min_var,
                                      to=self.confidence_max_var)
        self.confidence_slider.set(0.25)
        self.confidence_slider.pack(fill="x", padx=10, pady=0)

        self.iou_frame = customtkinter.CTkFrame(self.inference_control_scroll_frame, fg_color="transparent")
        self.iou_frame.pack(fill="x", padx=10, pady=(0, 5))

        # IoU label
        self.iou_label \
            = customtkinter.CTkLabel(self.iou_frame,
                                     text="NMS IoU Threshold")
        self.iou_label.pack(side="left")

        self.iou_value_label \
            = customtkinter.CTkLabel(self.iou_frame, text="0.45", width=50)
        self.iou_value_label.pack(side="right")

        # IoU slider
        self.iou_slider \
            = customtkinter.CTkSlider(self.inference_control_scroll_frame,
                                      variable=self.iou_var,
                                      command=self.IoUSlider_Event,
                                      from_=self.iou_min_var,
                                      to=self.iou_max_var)
        self.iou_slider.set(0.45)
        self.iou_slider.pack(fill="x", padx=10, pady=0)

        # image size label
        self.inference_image_size_label \
            = customtkinter.CTkLabel(self.inference_control_scroll_frame,
                                     text="Image Size")
        self.inference_image_size_label.pack(anchor="w", padx=10, pady=(0, 5))

        # image size combobox
        self.image_size_combobox \
            = customtkinter.CTkComboBox(self.inference_control_scroll_frame,
                                        variable=self.image_size_var,
                                        width=300,
                                        values=self.image_size_list_var)
        self.image_size_combobox.set("640")
        self.image_size_combobox.pack(anchor="w", padx=10, pady=(5, 5))

        # FP16 enabled checkbox
        self.fp16_enabled_checkbox \
            = customtkinter.CTkCheckBox(self.inference_control_scroll_frame,
                                        text="Enable FP16 (CUDA only)",
                                        variable=self.fp16_enabled_var)
        self.fp16_enabled_checkbox.pack(anchor="w", padx=10, pady=(10, 5))

        # max detection label
        self.max_detection_label \
            = customtkinter.CTkLabel(self.inference_control_scroll_frame,
                                     text="Max Detection")
        self.max_detection_label.pack(anchor="w", padx=10, pady=(5, 5))

        # max detection combobox
        self.max_detection_combobox \
            = customtkinter.CTkComboBox(self.inference_control_scroll_frame,
                                        variable=self.max_detection_var,
                                        width=300,
                                        values=self.max_detection_list_var)
        self.max_detection_combobox.set("100")
        self.max_detection_combobox.pack(anchor="w", padx=10, pady=(5, 5))

        # Output Options label
        self.output_options_label \
            = customtkinter.CTkLabel(self.inference_control_scroll_frame,
                                     text="✓ Output Options",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.output_options_label.pack(anchor="w", padx=10, pady=(15, 5))
    
        # Save video checkbox
        self.save_video_checkbox = \
            customtkinter.CTkCheckBox(self.inference_control_scroll_frame,
                                     text="Save Output Video/Image",
                                     variable=self.save_video_var)
        self.save_video_checkbox.pack(anchor="w", padx=10, pady=5)

        # Save Frame checkbox
        self.save_frames_checkbox = \
            customtkinter.CTkCheckBox(self.inference_control_scroll_frame,
                                      text="Save Detection Frames",
                                      variable=self.save_frames_var)
        self.save_frames_checkbox.pack(anchor="w", padx=10, pady=5)

        # Runtime label
        self.runtime_label \
            = customtkinter.CTkLabel(self.inference_control_scroll_frame,
                                     text="✓ Runtime",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.runtime_label.pack(anchor="w", padx=10, pady=(5, 5))
        
        # device combobox
        self.device_combobox = \
            customtkinter.CTkComboBox(self.inference_control_scroll_frame,
                                      variable=self.device_var,
                                      values=self.device_list_var)
        self.device_combobox.set("CUDA")
        self.device_combobox.pack(fill="x", padx=10, pady=5)

        # Start inference button
        self.start_button \
            = customtkinter.CTkButton(self.inference_control_scroll_frame,
                                      text="Start Inference",
                                      command=self.StartInference_Event,
                                      height=40,
                                      font=customtkinter.CTkFont(size=14))
        self.start_button.pack(fill="x", padx=10, pady=(20, 10))

        self.ModelSelectionUIChanged_Event()

    def ModelSelectionUIChanged_Event(self):

        if self.model_selection_var.get() == "Trained":
            self.pretrained_model_frame.pack_forget()
            self.trained_model_frame.pack(fill="x", pady=5)
        else:
            self.trained_model_frame.pack_forget()
            self.pretrained_model_frame.pack(fill="x", pady=5)

    def BrowseTrainedModel_Event(self):

        filepath = FileDialogUtils.BrowseFiles(title="Select Model", filetypes=[("Pytorch Model", "*.pt")])
        if not filepath:
            self.AppendInferenceLog_Event("WARNING", "Model path not found. Please enter model to continue!")
            return
        
        self.trained_model_var.set(filepath)

        self.AppendInferenceLog_Event("INFO", f"Model selected: {filepath}")

    def ConfidenceSlider_Event(self, value):

        self.confidence_value_label.configure(text=f"{value:.2f}")

    def IoUSlider_Event(self, value):

        self.iou_value_label.configure(text=f"{value:.2f}")

    def BuildInferenceConfig_Event(self):

        config = {}

        # source process
        if self.source_type_var.get() == "Local Files":
            config["source"] = {
                "type": "local",
                "items": self.selected_local_sources
            }
        else:
            config["source"] = {
                "type": "youtube",
                "items": [self.youtube_url_var.get()]
                if self.youtube_url_var.get() else []
            }

        # model process
        if self.model_selection_var.get() == "Trained":
            config["model"] = {
                "type": "trained",
                "path": self.trained_model_var.get()
            }
        else:
            config["model"] = {
                "type": "pretrained",
                "version": self.pretrained_version_var.get(),
                "size": self.pretrained_size_var.get()
            }

        # tracking process
        config["tracking"] = {
            "enabled": self.enable_tracking_var.get(),
            "tracker": self.tracker_var.get()
        }

        # detection process
        config["detection"] = {
            "confidence": round(self.confidence_var.get(), 2),
            "iou": round(self.iou_var.get(), 2),
            "image_size": int(self.image_size_var.get()),
            "fp16": self.fp16_enabled_var.get(),
            "max_detection": int(self.max_detection_var.get())
        }

        # output process
        config["output"] = {
            "save_video": self.save_video_var.get(),
            "save_frames": self.save_frames_var.get()
        }

        # runtime process
        config["runtime"] = {
            "device": self.device_var.get()
        }

        self.inference_config = config
        print("self.inference_config: \n", self.inference_config)

        return config

    def EnterInferenceMode_Event(self):

        self.inference_mode = True

        # hide config panels
        self.inference_log_frame.grid_remove()
        self.inference_control_frame.grid_remove()

        # fullscreen video
        self.fullscreen_inference_mode_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.fullscreen_inference_mode_label.lift()

        # runtime menu
        self.inference_runtime_mode_frame.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

        self.inference_runtime_mode_log_textbox.clear()

    def ExitInferenceMode_Event(self):

        self.inference_mode = False

        self.fullscreen_inference_mode_label.place_forget()

        self.inference_runtime_mode_frame.grid_remove()

        self.inference_log_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.inference_control_frame.grid(row=0, column=2, padx=5, pady=0, sticky="nsew")

        self.UpdateUISourceTypeChanged_Event(self.source_type_var.get())

    def EnqueueInferenceFrame_Event(self, frame):

        now = time.time()
        if now - self.last_frame_time < 0.03:  # ~30 FPS cap
            return

        self.last_frame_time = now

        if self.frame_queue.full():
            self.frame_queue.get_nowait()

        self.frame_queue.put_nowait(frame)

    def StartInference_Event(self):

        # build latest config
        self.BuildInferenceConfig_Event()

        # already running or not?
        if self.inference_processor is not None and self.inference_processor.running:
            self.AppendInferenceLog_Event("WARNING", "Inference is already running")
            return

        self.EnterInferenceMode_Event()
        self.AppendInferenceLog_Event("INFO", "Starting inference model")

        self.inference_processor \
            = InferenceProcessor(config=self.inference_config,
                                 frame_callback=self.EnqueueInferenceFrame_Event,
                                 log_callback=self.AppendInferenceLog_Event)
        self.inference_processor.start()

        self.AppendInferenceLog_Event("INFO", "Inference started")

    def StopInference_Event(self):

        if self.inference_processor:
            self.inference_processor.stop()

        self.ExitInferenceMode_Event()

        self.AppendInferenceLog_Event("INFO", "Inference stopped")

    def RenderInferenceFrameLoop_Event(self):

        try:
            frame = self.frame_queue.get(timeout=0.05)
            self.UpdateInferenceFrameUI_Event(frame)
        except Empty:
            pass
        self.after(15, self.RenderInferenceFrameLoop_Event)

    def UpdateInferenceFrameUI_Event(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_h, frame_w = rgb.shape[:2]

        target = self.fullscreen_inference_mode_label

        width = target.winfo_width()
        height = target.winfo_height()

        if width < 10 or height < 10:
            return

        scale = min(width / frame_w, height / frame_h)

        new_w = int(frame_w * scale)
        new_h = int(frame_h * scale)

        resized = cv2.resize(rgb, (new_w, new_h))

        canvas = numpy.zeros((height, width, 3), dtype=numpy.uint8)

        x_offset = (width - new_w) // 2
        y_offset = (height - new_h) // 2

        canvas[y_offset:y_offset + new_h,
            x_offset:x_offset + new_w] = resized

        image = Image.fromarray(canvas)
        photo = ImageTk.PhotoImage(image)

        target.configure(image=photo)
        target.image = photo

    # TRAIN PANEL SETUP -------------------------------------------#
    # -------------------------------------------------------------#
    def TrainPanel_Adapter(self):

        # main layout
        self.training_frame.grid_rowconfigure(0, weight=1)
        self.training_frame.grid_columnconfigure(0, weight=1)
        self.training_frame.grid_columnconfigure(1, weight=2)

        # LEFT SIDE: training configuration frame
        self.training_configuration_frame = customtkinter.CTkFrame(self.training_frame)
        self.training_configuration_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.training_configuration_frame.grid_rowconfigure(0, weight=1)
        self.training_configuration_frame.grid_rowconfigure(1, weight=0)
        self.training_configuration_frame.grid_columnconfigure(0, weight=1)

        # RIGHT SIDE: training log frame
        self.training_log_frame = customtkinter.CTkFrame(self.training_frame)
        self.training_log_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.training_log_frame.grid_rowconfigure(1, weight=1)
        self.training_log_frame.grid_columnconfigure(0, weight=1)

        self.TrainingConfiguration_WidgetsConfigure()

        self.TrainingLog_WidgetsConfigure()

    def TrainingConfiguration_WidgetsConfigure(self):

        # TABVIEW --------------------------------------------------------------#
        self.training_tabview \
            = customtkinter.CTkTabview(self.training_configuration_frame)
        self.training_tabview.grid(row=0, column=0, padx=10, pady=0, sticky="nsew")

        self.training_control_frame = customtkinter.CTkFrame(self.training_configuration_frame)
        self.training_control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.training_control_frame.grid_columnconfigure((0, 1), weight=1)

        # add Training Configuration tab
        self.training_tabview.add("Training Configuration")
        self.training_tabview.add("Training Documentation")
        self.training_config_tab = self.training_tabview.tab("Training Configuration")
        self.training_doc_tab = self.training_tabview.tab("Training Documentation")

        # Scroll Frame of training config
        self.training_scroll_frame \
            = customtkinter.CTkScrollableFrame(self.training_config_tab, corner_radius=10)
        self.training_scroll_frame.grid_columnconfigure(0, weight=1)
        self.training_scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.training_doc_textbox \
            = customtkinter.CTkTextbox(self.training_doc_tab)
        self.training_doc_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # DATASET WIDGETS ----------------------------------------------------------#
        self.dataset_title_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="✓ Dataset",
                                     font=customtkinter.CTkFont(size=22, weight="bold"))
        self.dataset_title_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.dataset_path_entry \
            = customtkinter.CTkEntry(self.training_scroll_frame,
                                     height=40,
                                     textvariable=self.dataset_yaml_var)
        self.dataset_path_entry.pack(fill="both", padx=10, pady=(5, 5))

        self.dataset_browse_button \
            = customtkinter.CTkButton(self.training_scroll_frame,
                                      text="Browse Dataset YAML",
                                      command=self.BrowseDataset_Event,
                                      height=30,
                                      font=customtkinter.CTkFont(size=14))
        self.dataset_browse_button.pack(anchor="w", padx=10, pady=(10, 10))

        # MODEL WIDGETS ----------------------------------------------------------#
        self.model_title_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="✓ Model",
                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.model_title_label.pack(anchor="w", padx=10, pady=(20, 5))

        self.model_family_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="Model Family",
                                     font=customtkinter.CTkFont(size=16, slant="italic"))
        self.model_family_label.pack(anchor="w", padx=10, pady=(5, 5))

        self.model_family_optionmenu \
            = customtkinter.CTkOptionMenu(self.training_scroll_frame,
                                          variable=self.model_family_var,
                                          values=self.model_family_list_var,
                                          command=self.ModelFamilyChanged_Event)
        self.model_family_optionmenu.pack(fill="both", padx=10, pady=(5, 5))

        self.model_version_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="Model Version",
                                     font=customtkinter.CTkFont(size=14, slant="italic"))
        self.model_version_label.pack(anchor="w", padx=10, pady=(5, 5))

        self.model_version_optionmenu \
            = customtkinter.CTkOptionMenu(self.training_scroll_frame,
                                          variable=self.model_version_var,
                                          values=[],
                                          command=self.ModelVersionChanged_Event)
        self.model_version_optionmenu.pack(fill="both", padx=10, pady=(5, 5))

        self.model_size_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="Model Size",
                                     font=customtkinter.CTkFont(size=16, slant="italic"))
        self.model_size_label.pack(anchor="w", padx=10, pady=(5, 5))

        self.model_size_optionmenu \
            = customtkinter.CTkOptionMenu(self.training_scroll_frame,
                                          variable=self.model_size_var,
                                          values=[],
                                          command=self.ModelSizeChanged_Event)
        self.model_size_optionmenu.pack(fill="both", padx=10, pady=(5, 5))

        # TRAINING WIDGETS ----------------------------------------------------------#
        self.hyperparams_title_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="✓ Hyperparameters",
                                     font=customtkinter.CTkFont(size=22, weight="bold"))
        self.hyperparams_title_label.pack(anchor="w", padx=10, pady=(20, 5))

        self.epochs_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="Epochs",
                                     font=customtkinter.CTkFont(size=16, slant="italic"))
        self.epochs_label.pack(anchor="w", padx=10, pady=(5, 5))

        self.epochs_entry \
            = customtkinter.CTkEntry(self.training_scroll_frame,
                                     width=30,
                                     textvariable=self.epochs_var)
        self.epochs_entry.pack(fill="both", padx=10, pady=(5, 10))
        
        self.batch_size_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="Batch Size",
                                     font=customtkinter.CTkFont(size=16, slant="italic"))
        self.batch_size_label.pack(anchor="w", padx=10, pady=(5, 5))

        self.batch_size_optionmenu \
            = customtkinter.CTkOptionMenu(self.training_scroll_frame,
                                          variable=self.batch_size_var,
                                          values=self.batch_size_list_var)
        self.batch_size_optionmenu.pack(fill="both", padx=10, pady=(5, 10))

        self.train_image_size_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="Image Size",
                                     font=customtkinter.CTkFont(size=16, slant="italic"))
        self.train_image_size_label.pack(anchor="w", padx=10, pady=(5, 5))

        self.train_image_size_optionmenu \
            = customtkinter.CTkOptionMenu(self.training_scroll_frame,
                                          variable=self.train_image_size_var,
                                          values=list(self.train_image_size_list_var))
        self.train_image_size_optionmenu.pack(fill="both", padx=10, pady=(5, 10))

        self.enabled_amp_fp16_checkbox \
            = customtkinter.CTkCheckBox(self.training_scroll_frame,
                                        text="Enable AMP FP16",
                                        variable=self.train_amp_var)
        self.enabled_amp_fp16_checkbox.pack(anchor="w", padx=10, pady=(10, 10))

        # TRAINING WIDGETS ----------------------------------------------------------#
        self.validation_title_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="✓ Validation",
                                     font=customtkinter.CTkFont(size=22, weight="bold"))
        self.validation_title_label.pack(anchor="w", padx=10, pady=(20, 5))

        self.run_validation_checkbox \
            = customtkinter.CTkCheckBox(self.training_scroll_frame,
                                        text="Run validation after training",
                                        variable=self.run_validation_var)
        self.run_validation_checkbox.pack(anchor="w", padx=10, pady=(10, 5))

        self.show_validation_results_checkbox \
            = customtkinter.CTkCheckBox(self.training_scroll_frame,
                                        text="Show validation results",
                                        variable=self.show_result_validation_var)
        self.show_validation_results_checkbox.pack(anchor="w", padx=10, pady=(10, 5))

        # MODEL EXPORT WIDGETS ----------------------------------------------------------#
        self.export_title_label \
            = customtkinter.CTkLabel(self.training_scroll_frame,
                                     text="✓ Model Export",
                                     font=customtkinter.CTkFont(size=22, weight="bold"))
        self.export_title_label.pack(anchor="w", padx=10, pady=(20, 5))

        self.export_onnx_checkbox \
            = customtkinter.CTkCheckBox(self.training_scroll_frame,
                                        text="Export ONNX",
                                        variable=self.export_onnx_var)
        self.export_onnx_checkbox.pack(anchor="w", padx=10, pady=(10, 5))

        self.export_tensorrt_checkbox \
            = customtkinter.CTkCheckBox(self.training_scroll_frame,
                                        text="Export TensorRT",
                                        variable=self.export_tensorrt_var)
        self.export_tensorrt_checkbox.pack(anchor="w", padx=10, pady=(10, 5))

        self.start_training_button \
            = customtkinter.CTkButton(self.training_control_frame,
                                      text="Start Training",
                                      height=40,
                                      command=self.StartTraining_Event,
                                      font=customtkinter.CTkFont(size=18, weight="bold"))
        self.start_training_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.stop_training_button \
            = customtkinter.CTkButton(self.training_control_frame,
                                      text="Stop Training",
                                      state="disabled",
                                      height=40,
                                      command=self.StopTraining_Event,
                                      font=customtkinter.CTkFont(size=18, weight="bold"))
        self.stop_training_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.ModelFamilyChanged_Event(self.model_family_var.get())

    def BrowseDataset_Event(self):

        filepath = FileDialogUtils.BrowseFiles(title="Select Dataset YAML", filetypes=[("Dataset YAML", "*.yaml *.yml")])
        if not filepath:
            self.AppendInferenceLog_Event("WARNING", "Model path not found. Please enter model to continue!")
            return

        self.dataset_yaml_var.set(filepath)

    def ModelFamilyChanged_Event(self, value):

        family_key = value.lower()

        family_cfg = self.model_cfg["families"][family_key]

        version_list = family_cfg["versions"]
        size_list = family_cfg["sizes"]

        self.model_version_optionmenu.configure(values=version_list)

        self.model_size_optionmenu.configure(values=size_list)

        self.model_version_var.set(version_list[0])

        self.model_size_var.set(size_list[0])

    def ModelVersionChanged_Event(self, value):

        self.model_version_var.set(value)

    def ModelSizeChanged_Event(self, value):

        self.model_size_var.set(value)

    def LoadTrainingDocument_Event(self):

        doc_path = "docs/training_guide.md"
        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.training_doc_textbox.delete("1.0", "end")
            self.training_doc_textbox.insert("1.0", content)
        except Exception as e:
            self.training_doc_textbox.insert("1.0", f"Unable to load training guide\n\n{e}")

    def BuildTrainingConfig_Event(self):

        config = {}
        
        # dataset
        config["dataset"] = {
            "dataset_yaml": self.dataset_yaml_var.get().strip()
        }
        
        # model 
        config["model"] = {
            "family": self.model_family_var.get(),
            "version": self.model_version_var.get(),
            "size": self.model_size_var.get()
        }

        # hyperparameter
        config["hyperparameters"] = {
            "epochs": int(self.epochs_var.get()),
            "batch_size": int(self.batch_size_var.get()),
            "image_size": int(self.train_image_size_var.get()),
            "amp_fp16": self.train_amp_var.get()
        }

        # validation
        config["validation"] = {
            "run_validation": self.run_validation_var.get(),
            "show_results": self.show_result_validation_var.get()
        }

        # export
        config["export"] = {
            "onnx": self.export_onnx_var.get(),
            "tensorrt": self.export_tensorrt_var.get()
        }

        self.training_config = config
        print(self.training_config)

        return config

    def TrainingLog_WidgetsConfigure(self):

        self.training_log_toolbar = customtkinter.CTkFrame(self.training_log_frame, fg_color="transparent")
        self.training_log_toolbar.grid(row=0,column=0,padx=10,pady=10,sticky="ew")

        self.clear_log_button \
            = customtkinter.CTkButton(self.training_log_toolbar,
                                      text="Clear Log",
                                      width=120,
                                      command=self.ClearLog_Event,
                                      font=customtkinter.CTkFont(size=14))
        self.clear_log_button.pack(side="left", padx=5)

        self.save_log_button \
            = customtkinter.CTkButton(self.training_log_toolbar,
                                      text="Save Log",
                                      width=120,
                                      command=self.SaveLog_Event,
                                      font=customtkinter.CTkFont(size=14))

        self.save_log_button.pack(side="right", padx=5)

        self.training_log_textbox \
            = LogTextboxUtils(self.training_log_frame)
        self.training_log_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def AppendTrainingLog_Event(
            self,
            level,
            message):

        self.after(
            0,
            lambda: self.training_log_textbox.log(
                level,
                message
            )
        )

    def ClearLog_Event(self):

        self.training_log_textbox.delete("1.0", "end")

    def SaveLog_Event(self):

        pass

    def StartTraining_Event(self):
        
        self.BuildTrainingConfig_Event()

        if self.training_processor is not None and self.training_processor.running:
            print("ERROR")
            return

        self.training_processor \
            = TrainingProcessor(config=self.training_config, log_callback=self.AppendTrainingLog_Event)
        self.training_processor.start()

    def StopTraining_Event(self):

        if self.training_processor:
            self.training_processor.stop()
        
        # self.AppendTrainingLog_Event("INFO", "Training Stopped")

    # DATASET PANEL SETUP -----------------------------------------#
    # -------------------------------------------------------------#
    def DatasetPanel_Adapter(self):

        pass

    # FRAME SELECTION SETUP ---------------------------------------#
    # -------------------------------------------------------------#
    def FrameSelection_Adapter(self, frame_name):

        self.inference_menu_tab.configure(fg_color="transparent")

        self.train_menu_tab.configure(fg_color="transparent")

        self.dataset_menu_tab.configure(fg_color="transparent")

        self.inference_frame.grid_forget()
        self.training_frame.grid_forget()
        self.dataset_frame.grid_forget()

        if frame_name == "Inference":
            self.inference_menu_tab.configure(fg_color=("gray75", "gray25"))
            self.inference_frame.grid(row=0, column=0, sticky="nsew")
        elif frame_name == "Train":
            self.train_menu_tab.configure(fg_color=("gray75", "gray25"))
            self.training_frame.grid(row=0, column=0, sticky="nsew")
        elif frame_name == "Dataset":
            self.dataset_menu_tab.configure(fg_color=("gray75", "gray25"))
            self.dataset_frame.grid(row=0, column=0, sticky="nsew")

    def InferenceFrame_Event(self):

        self.FrameSelection_Adapter("Inference")

    def TrainFrame_Event(self):

        self.FrameSelection_Adapter("Train")

    def DatasetFrame_Event(self):

        self.FrameSelection_Adapter("Dataset")

