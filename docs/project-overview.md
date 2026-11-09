# Project Overview

Hand-to-Cursor is a Windows-oriented Python desktop application that uses a
camera and MediaPipe Hands to control the system mouse. The user selects a
camera and a rectangular work area in a CustomTkinter setup window, then
controls the cursor with hand movement and pinch gestures.

## Runtime flow

1. `main.py` creates `CameraSetupApp` and starts its Tk event loop.
2. The GUI previews the selected camera, lets the user choose a camera, flip
   mode, and work area, and can save these settings to `config.yaml`.
3. **Continue** closes the setup window and sets `continue_requested`. Closing
   with the window's close button exits without starting tracking.
4. `main.py` opens the camera again, crops each frame to the selected area,
   sends the crop to `HandTracker`, and passes hand coordinates and pinch
   measurements to `MouseController`.
5. Pressing `q` in the OpenCV tracking window exits the loop and releases the
   camera. If a drag is active, the mouse button is released as well.

The selected camera, flip mode, and work area are used immediately after
**Continue**. Click **Save to config.yaml** separately to retain them for the
next launch. When no work area is configured or selected, the full camera
frame is used.

## Repository map

- `main.py` — application entry point and real-time tracking/visualization loop.
- `config.yaml` — runtime camera, work-area, gesture, and filter settings.
- `requirements.txt` — Python package dependencies.
- `src/gui.py` — camera setup window, video preview, flip selection, and
  work-area selection.
- `src/camera_control.py` — camera-index probing.
- `src/config.py` — loads YAML settings and exposes module-level constants.
- `src/hand_tracker.py` — MediaPipe hand detection and normalized pinch data.
- `src/mouse_control.py` — maps hand positions to cursor movements and
  interprets pinch gestures as click/drag actions.
- `src/filters.py` — adaptive One Euro smoothing filter used for cursor motion.
- `docs/` — developer overview, architecture, decisions, and agent guidance.

## Running

Install dependencies with `pip install -r requirements.txt`, then run
`python main.py` from the repository root. See the root `README.md` for user
setup and gesture instructions.

There is currently no automated test suite in the repository. Validate code
changes with the focused checks appropriate to the edited module, and exercise
camera/UI behavior on a machine with a camera when available.
