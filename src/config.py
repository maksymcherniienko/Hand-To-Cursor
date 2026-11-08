import pyautogui, yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"

def load_config(path=CONFIG_PATH) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            f"Конфігураційний файл не знайдено за шляхом: {path}"
        )
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

cfg = load_config()

SCREEN_W, SCREEN_H = pyautogui.size()

CAM_INDEX: int = cfg["camera"]["device_index"]
CAM_WIDTH: int = cfg["camera"]["width"]
CAM_HEIGHT: int = cfg["camera"]["height"]

PINCH_THRESHOLD: float = cfg["gestures"]["pinch_threshold"]
DRAG_DELAY_SEC: float = cfg["gestures"]["drag_delay_sec"]
DEAD_ZONE_MARGIN: float = cfg["gestures"]["dead_zone_margin"]

#for 1 euro filter
FILTER_MIN_CUTOFF: float = cfg["filter"]["min_cutoff"]
FILTER_BETA: float = cfg["filter"]["beta"]