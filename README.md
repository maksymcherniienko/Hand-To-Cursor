# Hand-to-Cursor Control

A modular, real-time Computer Vision virtual trackpad that turns any desk surface into an interactive touchpad using an overhead camera, MediaPipe Hands, and adaptive signal filtering.

The system tracks hand landmarks over a user-defined physical work area (ROI), normalizes gesture metrics to be scale-invariant, filters hand jitter with a 1-Euro filter, and translates hand gestures into low-latency OS mouse events.

---

## ✨ Key Features

* **Modular OOP Architecture:** Cleanly decoupled components (`HandTracker`, `MouseController`, `OneEuroFilter`, and centralized configuration).
* **Work Area Calibration (ROI):** Manually select a region of interest on the camera feed to define the active interaction boundary.
* **1-Euro Adaptive Filter:** Mathematically balances jitter reduction when stationary with zero-latency responsiveness during fast hand motions.
* **Scale-Invariant Gesture Recognition:** Normalizes pinch distance against the anatomical palm size (wrist to middle MCP distance), ensuring consistent tracking regardless of hand distance from the camera.
* **Cursor Freeze on Click:** Freezes cursor position the moment a pinch begins, preventing cursor slipping off small UI elements during clicks.
* **Unified State Machine Gestures:**
  * **Click:** Quick pinch between thumb and index finger (< 0.3s).
  * **Drag & Drop:** Pinch and hold (> 0.3s) to grab and move items; release fingers to drop.
* **Centralized Configuration:** Configurable thresholds, camera parameters, and filter parameters via `config.yaml`.

---

## 📁 Project Structure

```text
Hand-to-Cursor/
├── config.yaml          # Camera, gesture, and filter settings
├── main.py              # Application entry point and visualization loop
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── AGENTS.md            # Coding-agent entry point
├── docs/
│   ├── ai-instructions.md
│   ├── architecture.md
│   ├── decisions.md
│   └── project-overview.md
└── src/
    ├── config.py        # YAML configuration loader
    ├── camera_control.py # Camera-index probing
    ├── gui.py           # Camera setup and work-area selection
    ├── filters.py       # 1-Euro Filter implementation
    ├── hand_tracker.py  # MediaPipe landmark extraction & scale normalization
    └── mouse_control.py # Cursor positioning & gesture state machine
```

Developer documentation is in [`docs/`](docs/project-overview.md),
including the [architecture](docs/architecture.md), [project decisions](docs/decisions.md),
and [coding-agent instructions](docs/ai-instructions.md).

---

## 🛠 Dependencies & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/maksymcherniienko/Hand-To-Cursor.git
   cd Hand-To-Cursor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration (`config.yaml`)

You can tweak camera resolution, gesture thresholds, and filter sensitivity without modifying Python code:

```yaml
camera:
  device_index: 0   # Camera index (0 for built-in, 1 for external)
  width: 960
  height: 540
  flip: 1           # 1 = horizontal, 0 = vertical, -1 = both

gestures:
  pinch_threshold: 0.3   # Normalized pinch distance threshold
  drag_delay_sec: 0.3    # Hold duration to transition from click to drag
  dead_zone_margin: 0.3  # Screen edge deadzone margin (0.0 - 0.5)

filter:
  min_cutoff: 0.1        # Jitter reduction at rest (lower = smoother)
  beta: 0.01             # Speed coefficient (higher = less lag during motion)
```

---

## 🚀 How to Use

1. **Launch the application:**
   ```bash
   python main.py
   ```

2. **Select the work area:**
   - Choose a flip mode: **Horizontal**, **Vertical**, or **Both**.
   - In the camera setup window, drag once over the video preview to draw a blue, semi-transparent rectangle around your physical work surface.
   - Click **Save to config.yaml** to save the camera, flip mode, and selected work area.
   - Click **Continue** to close setup and start tracking with the selected settings.

3. **Interact:**
   - Move your hand within the selected work area to steer the cursor.
   - Pinch quickly to click; pinch and hold to drag.
   - Press **`q`** to quit safely.

---

## 🖐 Controls (Gestures)

| Gesture | Description | Action |
| :--- | :--- | :--- |
| **Move Palm** | Tracks the base of the middle finger (MCP joint) | Cursor Movement |
| **Quick Pinch** | Bring thumb and index finger together and release (< 0.3s) | Left Click |
| **Pinch & Hold** | Keep thumb and index finger pressed together (> 0.3s) | Mouse Drag (Click & Hold) |
| **Release Pinch** | Open thumb and index finger during drag | Drop (`mouseUp`) |

---

## ⚠️ Notes

* **Camera Selection:** By default, the camera index is loaded from `config.yaml`. If you have only one camera and it fails to open, ensure `device_index` is set to `0`.
* **PyAutoGUI Failsafe:** Disabled (`pyautogui.FAILSAFE = False`) for continuous cursor tracking beyond screen borders. Use **`q`** in the OpenCV window to exit cleanly.
