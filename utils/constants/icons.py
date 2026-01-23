from types import SimpleNamespace


def _ns(**kwargs):
    return SimpleNamespace(**kwargs)


"""
use *
    TEXT_ICONS.wifi.strength_3
    TEXT_ICONS.volume.muted
    TEXT_ICONS.ui.keyboard
    TEXT_ICONS.power
    *
"""

TEXT_ICONS = _ns(
    ui=_ns(
        window_close="",
        question="",
        headset="󰋎",
        headphones="󰋋",
        phone="󰏲",
        watch="",
        keyboard="",
        mouse="",
        tv="",
        printer="󰐪",
        camera="",
        speakers="󰓃",
        package="",
    ),
    wifi=_ns(
        connected="󰤨",
        disconnected="󰤩",
        connecting="󰤪",
        disabled="󰤭",
        generic="󰤬",
        strength_0="󰤯",
        strength_1="󰤟",
        strength_2="󰤢",
        strength_3="󰤥",
        strength_4="󰤨",
    ),
    volume=_ns(
        overamplified="󰕾",
        high="󰕾",
        medium="󰖀",
        low="󰕿",
        muted="󰝟",
    ),
    power="",
    cpu="",
    fallback="",
)
