# Fusion 360 — Rotate View 45°

A tiny Autodesk Fusion 360 add-in that lets you roll the 3D view in **45° steps** instead of the ViewCube's fixed 90° jumps — without tilting off the face you're looking at.

## Why

Fusion's built-in ViewCube roll arrows only move in 90° increments, and clicking a ViewCube corner/edge tilts the camera off-axis instead of rolling it. This add-in rotates strictly around the camera's own line of sight (`eye` → `target`), so a flat face stays square to your screen while you roll it 45° at a time — handy for isometric-style views of chamfers, hex features, or anything not aligned to a cardinal axis.

It adds two buttons:
- **Roll View 45° CCW**
- **Roll View 45° CW**

to the bottom navigation bar and the **Inspect** menu.

## Install

**Windows (automated):**
1. Click **Code → Download ZIP** above and unzip it.
2. Double-click **`install.bat`**. It copies the `rotate_view_45deg` folder into `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`.
3. In Fusion 360, press **`Shift + S`** to open **Scripts and Add-Ins**.
4. On the **Add-Ins** tab, select `rotate_view_45deg`, check **Run on Startup**, then click **Run**.

**Manual (Windows or macOS):**
1. Copy the `rotate_view_45deg` folder into Fusion's AddIns directory:
   - Windows: `%appdata%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   - macOS: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
2. In Fusion 360, press **`Shift + S`**, select `rotate_view_45deg` under **Add-Ins**, check **Run on Startup**, then click **Run**.

## How to use

1. Click a face on the ViewCube (e.g. *Front* or *Top*) so it's facing you square-on.
2. Click **Roll View 45° CCW** or **Roll View 45° CW** on the far right of the bottom navigation bar — or find them under the **Inspect** dropdown.

> [!TIP]
> To bind a keyboard shortcut: open the **Inspect** dropdown, hover over either command, click the **`...`** menu, and choose **Change Keyboard Shortcut** (e.g. `Alt+Left` / `Alt+Right`).

## How it works

- `roll_camera(degrees)` takes the viewport's current camera, builds a normalized axis vector from `camera.eye` to `camera.target` (the direction you're looking), and rotates `camera.upVector` around that axis by ±45° using a `Matrix3D` rotation. Because the rotation axis is the view direction itself, the face you're looking at never tilts away from you — only the roll (up-vector) changes.
- `run(context)` registers the two commands as `CommandDefinitions`, attaches their icons from `resources/CCW` and `resources/CW`, and adds buttons to both `NavToolbar` and the `InspectPanel`.
- `stop(context)` removes everything it added, so toggling the add-in off (or reloading it) leaves no leftover UI.

## Customizing the rotation step

Open `rotate_view_45deg/rotate_view_45deg.py` and change the `45` / `-45` values in the `commands` list inside `run()` to whatever increment you want (e.g. `30`, `15`). Re-run `install.bat` (or re-copy the folder) and toggle the add-in off/on in Fusion to pick up the change.

## Project structure

```text
Fusion 360 - Rotate View 45 Degrees/
├── rotate_view_45deg/
│   ├── resources/
│   │   ├── CCW/{16x16,32x32}.png
│   │   └── CW/{16x16,32x32}.png
│   ├── lib/fusionAddInUtils/   # small logging/error-handling helper
│   ├── rotate_view_45deg.manifest
│   └── rotate_view_45deg.py
├── install.bat
├── LICENSE
└── README.md
```

## License

[MIT](LICENSE)
