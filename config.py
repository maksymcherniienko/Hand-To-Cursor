import pyautogui

SCREEN_W, SCREEN_H = pyautogui.size()
CAM_WIDTH, CAM_HEIGHT = 960, 540

# Налаштування жестів
PINCH_THRESHOLD = 0.3
DRAG_DELAY_SEC = 0.3
DEAD_ZONE_MARGIN = 0.3

# Налаштування фільтра
FILTER_MIN_CUTOFF = 0.1
FILTER_BETA = 0.01