import cv2
import customtkinter as ctk

import src.config as config
from src.gui.area_selection import AreaSelectionMixin
from src.gui.camera_settings import CameraSettingsMixin
from src.gui.layout import SetupUIMixin
from src.gui.video_preview import VideoPreviewMixin
from src.hand_tracker import HandTracker
from src.mouse_control import MouseController


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class CameraSetupApp(
    SetupUIMixin,
    AreaSelectionMixin,
    CameraSettingsMixin,
    VideoPreviewMixin,
    ctk.CTk,
):
    def __init__(self):
        super().__init__()

        self.tracker = HandTracker()
        self.mouse = MouseController()

        self.title("Вибір камери")
        self.geometry("1000x600")
        self.is_running = False

        self.cam_index = config.CAM_INDEX
        self.cam_flip = config.CAM_FLIP
        self.work_area = config.WORK_AREA
        self.frame_size = (config.CAM_WIDTH, config.CAM_HEIGHT)
        self.image_bounds = (0, 0, 0, 0)
        self.drag_start = None
        self.drag_area = None
        self.cap = cv2.VideoCapture(self.cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)
        self.continue_requested = False # для того щоб при закритті на крестик не продовжувався весь інший код

        self.setup_ui()
        self.update_video_frame()

    def start_stop_app(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.drag_start = None
            self.drag_area = None
            self.btn_clear_area_selection.configure(state="disabled")
            self.btn_start_stop.configure(text="Stop", fg_color="red", hover_color="darkred")
        else:
            self.btn_clear_area_selection.configure(state="normal")
            self.btn_start_stop.configure(text="Start", fg_color="green", hover_color="darkgreen")

    def on_closing(self):
        self.cap.release()
        self.destroy()
