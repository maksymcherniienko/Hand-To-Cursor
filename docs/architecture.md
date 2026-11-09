# Architecture

## Component boundaries

```text
main.py
  ├── src.gui.CameraSetupApp
  ├── src.config
  ├── src.hand_tracker.HandTracker
  └── src.mouse_control.MouseController
        └── src.filters.OneEuroFilter

src.gui.CameraSetupApp
  ├── src.camera_control.get_available_cameras
  └── config.yaml (read/write)

src.config
  └── config.yaml (read at import time)
```

### Application entry point

`main.py` coordinates setup and tracking. After the GUI event loop finishes, it
checks `continue_requested`; only the Continue action allows tracking to start.
The selected camera index, flip code, and work-area tuple are then used by the
video loop. Each captured frame is flipped according to the GUI selection,
cropped to the work area, converted from BGR to RGB, and processed by
`HandTracker`.

### Setup GUI

`CameraSetupApp` owns a camera capture handle while the setup window is open.
Its Tk event loop updates the preview using `.after()` rather than a blocking
loop. Mouse press, drag, and release events convert the preview coordinates to
frame coordinates and define `(x, y, width, height)`.

The GUI's Save action writes the selected camera and work area to YAML.
The flip selector maps Horizontal, Vertical, and Both to OpenCV flip codes `1`,
`0`, and `-1`, respectively. The selected mode is applied to the live preview
and is passed to the tracking loop on Continue. Save persists the camera index,
flip code, and work area. Continue closes the window without implicitly
saving. The window close handler releases the GUI camera capture; `main.py`
then either exits or opens a separate capture for tracking.

### Vision and mouse control

`HandTracker` wraps MediaPipe Hands and returns normalized pinch distance,
normalized pointer coordinates, and raw landmarks for drawing. It tracks one
hand.

`MouseController` maps normalized coordinates to screen coordinates, smooths
them with independent One Euro filters, and uses pinch duration to distinguish
clicks from drags. A short pinch-and-release clicks; holding beyond the
configured delay begins a drag.

`OneEuroFilter` combines a smoothed derivative with an adaptive cutoff to
smooth slower movement while responding more quickly to faster movement.

### Configuration

`src/config.py` loads `config.yaml` at import time. Its path is rooted relative
to `src/config.py`, and values are exposed as module-level constants used by
the other modules. Camera selection and work-area updates made in the GUI are
persisted only when the user explicitly saves.

## Data flow

```text
config.yaml -> src.config -> GUI defaults and tracking parameters
camera frame -> selected flip -> GUI preview -> selected frame-coordinate work area
camera frame -> selected flip -> crop -> RGB -> HandTracker
hand landmarks -> MouseController -> OneEuroFilter -> OS mouse events
pinch distance -> gesture state -> click / mouse-down / mouse-up
```

## Resource lifecycle

The GUI releases its capture when Continue or the window close button closes
the window. The tracking loop owns a separate capture and releases it on loop
exit, then destroys OpenCV windows. When exiting after a drag, `main.py` also
releases the held mouse button.
