import pyautogui
import time
import numpy as np
from filters import OneEuroFilter
import config as config

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

class MouseController:
    def __init__(self):
        self.filter_x = OneEuroFilter(min_cutoff=config.FILTER_MIN_CUTOFF, beta=config.FILTER_BETA)
        self.filter_y = OneEuroFilter(min_cutoff=config.FILTER_MIN_CUTOFF, beta=config.FILTER_BETA)
        
        self.is_dragging = False
        self.pinch_start_time = None

    def move_cursor(self, raw_x, raw_y):
        # Перетворюємо координати з урахуванням мертвої зони
        screen_x = np.interp(raw_x, (config.DEAD_ZONE_MARGIN, 1 - config.DEAD_ZONE_MARGIN), (0, config.SCREEN_W))
        screen_y = np.interp(raw_y, (config.DEAD_ZONE_MARGIN, 1 - config.DEAD_ZONE_MARGIN), (0, config.SCREEN_H))
        
        smoothed_x = self.filter_x(screen_x)
        smoothed_y = self.filter_y(screen_y)

        # Рухаємо курсор, якщо не затиснуто щипок або якщо ми в режимі перетягування
        if self.pinch_start_time is None or self.is_dragging:
            pyautogui.moveTo(smoothed_x, smoothed_y)

    def handle_gestures(self, normalized_pinch):
        action_status = "IDLE"

        if normalized_pinch < config.PINCH_THRESHOLD:
            if self.pinch_start_time is None:
                self.pinch_start_time = time.time()
                action_status = "CLICK_STARTED"
            elif (time.time() - self.pinch_start_time) > config.DRAG_DELAY_SEC:
                if not self.is_dragging:
                    pyautogui.mouseDown()
                    self.is_dragging = True
                action_status = "DRAGGING"
        else:
            if self.pinch_start_time is not None:
                if self.is_dragging:
                    pyautogui.mouseUp()
                    self.is_dragging = False
                else:
                    pyautogui.click()
                self.pinch_start_time = None
                action_status = "RELEASED"

        return action_status