from enum import StrEnum


class HyprlandEvent(StrEnum):
    # Keyboard
    ACTIVE_LAYOUT = "activelayout"

    # Monitors
    MONITORS_CHANGED = "monitorschanged"
    MONITOR_ADDED = "monitoradded"
    MONITOR_ADDED_V2 = "monitoraddedv2"
    MONITOR_REMOVED = "monitorremoved"
    MONITOR_REMOVED_V2 = "monitorremovedv2"

    # Windows
    OPEN_WINDOW = "openwindow"
    CLOSE_WINDOW = "closewindow"
    ACTIVE_WINDOW = "activewindow"
    MOVE_WINDOW_V2 = "movewindowv2"
    CHANGE_FLOATING_MODE = "changefloatingmode"
    FULLSCREEN = "fullscreen"

    # Workspaces
    WORKSPACE = "workspace"
    WORKSPACE_V2 = "workspacev2"
    FOCUSED_MON = "focusedmon"
    FOCUSED_MON_V2 = "focusedmonv2"
    CREATE_WORKSPACE_V2 = "createworkspacev2"
    DESTROY_WORKSPACE_V2 = "destroyworkspacev2"
    MOVE_WORKSPACE_V2 = "moveworkspacev2"
    RENAME_WORKSPACE = "renameworkspace"
