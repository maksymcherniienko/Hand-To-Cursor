import tkinter as tk

import customtkinter as ctk

import src.config as config
from src.gui.camera_settings import FLIP_CODE_BY_LABEL, FLIP_LABEL_BY_CODE


class SetupUIMixin:
    def setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=5)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.sidebar, text="Налаштування", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 20))

        ctk.CTkLabel(self.sidebar, text="Оберіть камеру:").pack(anchor="w", padx=20)

        self.cam_selector = ctk.CTkOptionMenu(
            self.sidebar,
            values=self.get_available_cameras(),
            command=self.change_camera,
        )
        self.cam_selector.set(config.CAM_INDEX)
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
            padx=5,
            pady=5,
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
            hover_color="darkgreen",
        )
        self.btn_save.pack(pady=(20, 20), padx=20, fill="x", side="bottom")

        self.btn_clear_area_selection = ctk.CTkButton(
            self.sidebar,
            text="Clear\n(will use whole camera frame)",
            command=self.clear_area_selection,
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