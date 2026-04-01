INTERESTING_EVENTS = {
    "changed",
    "changes_done_hint",
    "created",
    "deleted",
    "moved",
    "moved_in",
    "moved_out",
    "renamed",
    "attribute_changed",
}


HARD_RELOAD_PATHS = {
    "widgets.statusbar.enabled",
    "widgets.statusbar.position",
    "widgets.statusbar.modules",
}

HARD_RELOAD_PREFIXES: tuple[str, ...] = ()

SOFT_RELOAD_PREFIXES = (
    "widgets.statusbar.modules.",
    "general.styles.",
    "widgets.statusbar.modules_layout.",
)
