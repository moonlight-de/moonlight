class AnchorHandler:
    @staticmethod
    def statusbar(position) -> list:
        anchor_map = {
            "left": ["left", "top", "bottom"],
            "top": ["left", "top", "right"],
            "right": ["right", "top", "bottom"],
            "bottom": ["left", "bottom", "right"],
        }
        if isinstance(position, str):
            return anchor_map[position]
        raise ValueError("Position should be a string.")
