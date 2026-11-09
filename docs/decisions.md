# Project Decisions

This file records decisions reflected in the current implementation. It is not
a complete historical decision log; add dated entries when future changes
introduce a deliberate architectural or behavioral choice.

## Current decisions

### Keep the application split into small modules

Camera setup, configuration, hand tracking, cursor/gesture behavior, and
filtering live in separate modules. `main.py` orchestrates these components
rather than owning all of their implementation details.

### Use CustomTkinter for setup and OpenCV for tracking visualization

The setup screen uses CustomTkinter with a Tk canvas for camera preview and
work-area selection. The tracking loop uses OpenCV's display window and key
handling. This keeps interactive setup in a GUI while retaining the existing
frame-processing loop.

### Select a work area by dragging on the preview

The GUI maps a single mouse drag from displayed preview coordinates to camera
frame coordinates and represents the result as integer `x`, `y`, `width`, and
`height`. With no saved or newly selected area, the entire frame is the
fallback.

### Continue is distinct from closing the setup window

Continue sets `continue_requested` before closing the GUI. `main.py` checks the
flag after the Tk event loop: Continue starts tracking, while closing through
the window manager exits. This keeps an explicit user action in control of
whether the rest of the application starts.

### Saving settings is explicit

Continue uses the current camera, flip mode, and work area for the current run
but does not save them. The Save button writes them to `config.yaml` for
subsequent runs.

### Configure camera flipping in the GUI

The GUI exposes OpenCV's three flip modes: horizontal (`1`), vertical (`0`),
and both axes (`-1`). The selected mode is shared by the GUI preview and
tracking loop so the displayed and processed frames use the same orientation.

### Keep runtime configuration in YAML

Camera, work-area, gesture, and filter settings are stored in the repository's
`config.yaml` and loaded centrally by `src/config.py`. Avoid introducing
duplicate configuration sources without a clear need.

## Constraints to preserve

- Keep work-area coordinates aligned with the flipped frame used by tracking.
- Keep camera resource release behavior intact on both GUI exit paths and
  tracking-loop exit.
- Keep the window-manager close path from starting the tracking loop.
- Scope local feature changes to the smallest relevant modules; do not broaden
  a change to unrelated parts of the application without a concrete reason.
