class PositionHandler:
    @staticmethod
    def statusbar_is_vertical(position: str) -> bool:
        if position == "left" or position == "right":
            return True
        return False
