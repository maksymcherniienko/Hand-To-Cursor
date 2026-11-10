import cv2, yaml
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import src.config as config
from src.camera_control import get_available_cameras
from src.hand_tracker import HandTracker
from src.mouse_control import MouseController


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
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class CameraSetupApp(ctk.CTk):
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

    def setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- ЛІВА ПАНЕЛЬ (Керування) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=5)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.sidebar, text="Налаштування", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 20))

        ctk.CTkLabel(self.sidebar, text="Оберіть камеру:").pack(anchor="w", padx=20)
        
        self.cam_selector = ctk.CTkOptionMenu(
            self.sidebar, 
            values=get_available_cameras(),
            command=self.change_camera
        )
        self.cam_selector.set(config.CAM_INDEX) #обирає збережений до цього індекс
        self.cam_selector.pack(pady=(0, 20), padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="Flip camera:").pack(anchor="w", padx=20)
        self.flip_selector = ctk.CTkOptionMenu(
            self.sidebar,
            values=list(FLIP_CODE_BY_LABEL),
            command=self.change_flip,
        )
        self.flip_selector.set(FLIP_LABEL_BY_CODE[self.cam_flip])
        self.flip_selector.pack(pady=(0, 20), padx=20, fill="x")

        ctk.CTkLabel(
            self.sidebar,
            text="Потягніть мишкою щоб вибрати робочу область.",
            wraplength=160,
            justify="left",
            fg_color="#333333",
            corner_radius=5,
            padx=5, pady=5
        ).pack(anchor="w", padx=20, pady=(0, 10))

        self.btn_close = ctk.CTkButton(
            self.sidebar,
            text="Close",
            fg_color="blue",
            hover_color="darkblue",
            command=self.on_closing,
        )
        self.btn_close.pack(pady=(0, 10), padx=20, fill="x", side="bottom")

        self.btn_save = ctk.CTkButton(
            self.sidebar, 
            text="Зберегти в config.yaml", 
            command=self.save_config,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.btn_save.pack(pady=(20, 20), padx=20, fill="x", side="bottom")

        self.btn_clear_area_selection = ctk.CTkButton(
            self.sidebar,
            text="Clear\n(will use whole camera frame)",
            command=self.clear_area_selection
        )
        self.btn_clear_area_selection.pack(padx=20, pady=(0, 10), fill="x")

        self.btn_start_stop = ctk.CTkButton(
            self.sidebar,
            text="Start",
            fg_color="green",
            hover_color="darkgreen",
            command=self.start_stop_app,
        )
        self.btn_start_stop.pack(pady=(0, 10), padx=20, fill="x", side="bottom")

        self.video_frame = ctk.CTkFrame(self)
        self.video_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        
        self.video_canvas = tk.Canvas(
            self.video_frame,
            background="black",
            highlightthickness=0,
        )
        self.video_canvas.pack(expand=True, fill="both", padx=10, pady=10)
        self.video_canvas.bind("<ButtonPress-1>", self.start_area_selection)
        self.video_canvas.bind("<B1-Motion>", self.update_area_selection)
        self.video_canvas.bind("<ButtonRelease-1>", self.finish_area_selection)

    def change_camera(self, choice):
        """Змінює камеру "на льоту" при виборі зі списку."""
        self.cam_index = int(choice)
        self.cap.release()
        self.cap = cv2.VideoCapture(self.cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)

    def change_flip(self, choice):
        self.cam_flip = FLIP_CODE_BY_LABEL[choice]

    def get_work_area(self) -> tuple[int, int, int, int]:
        """Повертає робочу область у координатах кадру."""
        if self.work_area is not None:
            return self.work_area
        return 0, 0, self.frame_size[0], self.frame_size[1]

    def canvas_to_frame(self, canvas_x, canvas_y):
        left, top, display_width, display_height = self.image_bounds
        if display_width == 0 or display_height == 0:
            return None

        frame_width, frame_height = self.frame_size
        frame_x = round((canvas_x - left) * frame_width / display_width)
        frame_y = round((canvas_y - top) * frame_height / display_height)
        return (
            min(max(frame_x, 0), frame_width - 1),
            min(max(frame_y, 0), frame_height - 1),
        )

    @staticmethod
    def area_from_points(start, end):
        x1, y1 = start
        x2, y2 = end
        x_area = min(x1, x2)
        y_area = min(y1, y2)
        w_area = abs(x2 - x1) + 1
        h_area = abs(y2 - y1) + 1
        return x_area, y_area, w_area, h_area

    def start_area_selection(self, event):
        if self.is_running:
            return
        point = self.canvas_to_frame(event.x, event.y)
        if point is None:
            return
        left, top, display_width, display_height = self.image_bounds
        if not (left <= event.x < left + display_width and top <= event.y < top + display_height):
            return
        self.drag_start = point
        self.drag_area = self.area_from_points(point, point)

    def update_area_selection(self, event):
        if self.is_running or self.drag_start is None:
            return
        point = self.canvas_to_frame(event.x, event.y)
        if point is not None:
            self.drag_area = self.area_from_points(self.drag_start, point)

    def finish_area_selection(self, event):
        if self.is_running or self.drag_start is None:
            return
        point = self.canvas_to_frame(event.x, event.y)
        if point is not None:
            self.work_area = self.area_from_points(self.drag_start, point)
        self.drag_start = None
        self.drag_area = None

    def clear_area_selection(self):
        if self.is_running:
            return
        self.work_area = None
        self.drag_start = None
        self.drag_area = None
    
    def save_config(self):
        """Зберігає індекс камери, flip і робочу область."""
        config_data = {}
        
        # Читаємо існуючий файл, якщо він є
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f) or {}

        # Створюємо секцію camera, якщо її ще не було
        if "camera" not in config_data:
            config_data["camera"] = {}

        # Оновлюємо індекс
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
        # Записуємо назад
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            
        # Змінюємо текст кнопки для візуального зворотного зв'язку
        self.btn_save.configure(text="Saved!", fg_color="blue")
        self.after(2000, lambda: self.btn_save.configure(text="Save to config.yaml", fg_color="green"))

    def update_video_frame(self):
        """Безперервний цикл оновлення кадру."""
        ret, frame = self.cap.read()
        if ret:
            if self.cam_flip is not None:
                frame = cv2.flip(frame, self.cam_flip)
            frame_height, frame_width = frame.shape[:2]
            self.frame_size = (frame_width, frame_height)

            canvas_width = self.video_canvas.winfo_width()
            canvas_height = self.video_canvas.winfo_height()
            if canvas_width > 1 and canvas_height > 1:
                scale = min(canvas_width / frame_width, canvas_height / frame_height)
                display_width = max(1, round(frame_width * scale))
                display_height = max(1, round(frame_height * scale))
                left = (canvas_width - display_width) // 2
                top = (canvas_height - display_height) // 2
                self.image_bounds = (left, top, display_width, display_height)

                if self.is_running:
                    x, y, w, h = self.get_work_area()
                    cropped_frame = frame[y:y + h, x:x + w]

                    if cropped_frame.size:
                        rgb_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
                        hand_data = self.tracker.process_frame(rgb_frame)

                        if hand_data:
                            self.tracker.mp_draw.draw_landmarks(
                                cropped_frame,
                                hand_data["raw_landmarks"],
                                self.tracker.mp_hands.HAND_CONNECTIONS,
                            )
                            self.mouse.move_cursor(hand_data["pointer_x"], hand_data["pointer_y"])
                            status = self.mouse.handle_gestures(hand_data["normalized_pinch"])

                            if status == "DRAGGING":
                                cv2.putText(frame, "DRAGGING", (10, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            elif status in ("CLICK_STARTED", "RELEASED"):
                                cv2.putText(frame, "CLICK", (10, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                preview = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                preview = cv2.resize(preview, (display_width, display_height))
                area = self.drag_area if self.drag_area is not None else self.work_area
                if area is not None:
                    x_area, y_area, w_area, h_area = area
                    x1 = round(x_area * display_width / frame_width)
                    y1 = round(y_area * display_height / frame_height)
                    x2 = round((x_area + w_area) * display_width / frame_width) - 1
                    y2 = round((y_area + h_area) * display_height / frame_height) - 1
                    overlay = preview.copy()
                    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), -1)
                    preview = cv2.addWeighted(overlay, 0.5, preview, 0.5, 0)
                    cv2.rectangle(preview, (x1, y1), (x2, y2), (0, 0, 255), 2)

                photo = ImageTk.PhotoImage(Image.fromarray(preview))
                self.video_canvas.delete("all")
                self.video_canvas.create_image(left, top, anchor=tk.NW, image=photo)
                self.video_canvas.image = photo
        else:
            self.video_canvas.delete("all")
            self.video_canvas.create_text(
                self.video_canvas.winfo_width() // 2,
                self.video_canvas.winfo_height() // 2,
                text=f"Camera {self.cam_index} unavailable",
                fill="white",
            )

        self.after(15, self.update_video_frame)

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
        # звільнення камери при закритті хрестиком
        self.cap.release()
        self.destroy()