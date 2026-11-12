import tkinter as tk

import cv2
from PIL import Image, ImageTk


class VideoPreviewMixin:
    def update_video_frame(self):
        """Continuously update the camera preview."""
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