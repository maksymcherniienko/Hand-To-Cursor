# Hand to Cursor Control

This Python script allows you to use a webcam and hand gestures to fully control your mouse cursor. It is designed for setups where the camera is pointed at a work surface (like a desk). Before tracking begins, the script prompts you to select a specific "work area" in the frame to improve accuracy.

## ✨ Key Features

* **Work Area Setup:** Manually select a region of interest (ROI) on the video feed where the hand will be recognized.


* **Smooth Cursor Movement:** Tracks the hand with built-in smoothening to prevent erratic mouse jumps.


* **Clicking:** Simulates a left mouse click by calculating the distance between the ring finger tip and its base joint.


* **Drag & Drop:** Clicks and holds items using a "pinch" gesture (bringing the index finger and thumb together).



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


* **Click:** Sharply bend your ring finger. The text `CLICK!` will appear on the video feed.


* **Drag:** Bring the tips of your index finger and thumb together. The text `DRAGGING` will appear on the screen. Spread the fingers apart to release the object.



## ⚠️ Important Notes

* **Camera Index:** The code is set to capture video from camera index `1` (`cv2.VideoCapture(1)`). If you only have one webcam and the program fails to capture video, edit the code and change the `1` to `0`.


* **PyAutoGUI Failsafe:** The `pyautogui.FAILSAFE` feature is disabled (`False`). Throwing your cursor into the corner of the screen will not abort the script. You must use the `q` key to stop execution.
