from position import Position


class DistancedStep:
    def __init__(self, distance: int, position: Position):
        self.distance, self.position = distance, position

    def __str__(self) -> str:
        return f"dist={self.distance},pos={self.position}"