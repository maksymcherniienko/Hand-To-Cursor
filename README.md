# Hand to Cursor Control

This Python script allows you to use a webcam and hand gestures to fully control your mouse cursor. It is designed for setups where the camera is pointed at a work surface (like a desk). Before tracking begins, the script prompts you to select a specific "work area" in the frame to improve accuracy.

## ✨ Key Features

* **Work Area Setup:** Manually select a region of interest (ROI) on the video feed where the hand will be recognized.


* **Adaptive Smooth Movement:** Dynamic smoothing eliminates cursor jitter at low speeds while maintaining instant responsiveness during fast movements, with a deadzone for resting hand stability.


* **Cursor Freeze on Click:** Automatically freezes cursor position while pinching to prevent accidental cursor drift off target buttons.


* **Unified Pinch Gestures:** Distinguishes between quick taps and drag-and-drop based on pinch duration:
  * **Click:** Quick pinch between thumb and index finger (< 0.3s).
  * **Drag & Drop:** Pinch and hold (> 0.3s) to grab and move items.



## 🛠 Dependencies & Installation

This script requires Python 3.x and several external libraries. Install them using pip:

```bash
pip install opencv-python numpy mediapipe pyautogui

```

## 🚀 How to Use

1. Run the script:
```bash
python hand_to_cursor_choose_work_area.py

```


2. **Select the area:** Upon launch, a window displaying your camera feed will appear. Use your standard mouse to draw a rectangle over your physical work surface.


3. Press **ENTER** or **SPACE** to confirm the selection.


4. Place your hand in the frame over the selected area — the cursor will begin to move.


5. To exit the program, press the **`q`** key.



## 🖐 Controls (Gestures)

* **Movement:** Move your palm over the desk. The cursor tracks the base of your middle finger (the MCP joint).


* **Click:** Quickly pinch your index finger and thumb together (< 0.3s) and release.


* **Drag:** Pinch and hold your index finger and thumb together (> 0.3s). The text `DRAGGING` will appear. Move your hand to drag the object, and spread your fingers apart to release.



## ⚠️ Important Notes

* **Camera Index:** The code is currently set to camera index `0` (`cv2.VideoCapture(0)`). If you are using an external webcam and it doesn't open, change `0` to `1`.


* **PyAutoGUI Failsafe:** The `pyautogui.FAILSAFE` feature is disabled (`False`). Throwing your cursor into the corner of the screen will not abort the script. You must use the `q` key to stop execution.
