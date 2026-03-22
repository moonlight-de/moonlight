from enum import StrEnum


class HyprlandEvent(StrEnum):
    """
    Enumeration of all available Hyprland IPC events.
    
    This enum provides type-safe access to event names used throughout
    the codebase when subscribing to Hyprland events via the .on() method.
    """

    # Keyboard events
    ACTIVE_LAYOUT = "activelayout"

    # Monitor events
    MONITOR_ADDED_V2 = "monitoraddedv2"
    MONITOR_REMOVED_V2 = "monitorremovedv2"

    # Window events
    OPEN_WINDOW = "openwindow"
    CLOSE_WINDOW = "closewindow"
    ACTIVE_WINDOW = "activewindow"
    MOVE_WINDOW_V2 = "movewindowv2"
    CHANGE_FLOATING_MODE = "changefloatingmode"
    FULLSCREEN = "fullscreen"

    # Workspace events
    WORKSPACE_V2 = "workspacev2"
    CREATE_WORKSPACE_V2 = "createworkspacev2"
    DESTROY_WORKSPACE_V2 = "destroyworkspacev2"
    MOVE_WORKSPACE_V2 = "moveworkspacev2"
    RENAME_WORKSPACE = "renameworkspace"

