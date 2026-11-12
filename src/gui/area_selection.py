class AreaSelectionMixin:
    def get_work_area(self) -> tuple[int, int, int, int]:
        """Return the work area in frame coordinates."""
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