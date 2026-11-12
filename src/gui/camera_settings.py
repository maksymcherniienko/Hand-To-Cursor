import cv2
import yaml

import src.config as config
from src.camera_control import get_available_cameras


CONFIG_PATH = config.CONFIG_PATH
FLIP_CODE_BY_LABEL = {
    "None": None,
    "Horizontal": 1,
    "Vertical": 0,
    "Both": -1,
}
FLIP_LABEL_BY_CODE = {
    flip_code: label for label, flip_code in FLIP_CODE_BY_LABEL.items()
}


class CameraSettingsMixin:
    def get_available_cameras(self):
        return get_available_cameras()

    def change_camera(self, choice):
        """Change the selected camera immediately."""
        self.cam_index = int(choice)
        self.cap.release()
        self.cap = cv2.VideoCapture(self.cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)

    def change_flip(self, choice):
        self.cam_flip = FLIP_CODE_BY_LABEL[choice]

    def save_config(self):
        """Save the camera index, flip mode, and work area."""
        config_data = {}

        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as file:
                config_data = yaml.safe_load(file) or {}

        if "camera" not in config_data:
            config_data["camera"] = {}

        config_data["camera"]["device_index"] = self.cam_index
        config_data["camera"]["flip"] = self.cam_flip

        if self.work_area is not None:
            x_area, y_area, w_area, h_area = self.work_area
            config_data["work_area"] = {
                "x": x_area,
                "y": y_area,
                "width": w_area,
                "height": h_area,
            }
        else:
            config_data.pop("work_area", None)

        with open(CONFIG_PATH, "w", encoding="utf-8") as file:
            yaml.dump(config_data, file, default_flow_style=False, allow_unicode=True)

        self.btn_save.configure(text="Saved!", fg_color="blue")
        self.after(2000, lambda: self.btn_save.configure(text="Save to config.yaml", fg_color="green"))
