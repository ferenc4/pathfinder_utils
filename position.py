from directions import Direction


class Position:
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y
        self.hash = f"{self.x},{self.y}".__hash__()

    def __eq__(self, o: object) -> bool:
        return (type(o) == Position and self.y == o.y and self.x == o.x) or \
               (type(o) == tuple and self.x == o[0] and self.y == o[1])

    def __hash__(self) -> int:
        return self.hash

    def __str__(self) -> str:
        return f"(x={self.x}, y={self.y})"

    def __repr__(self):
        return self.__str__()

    def moved(self, direction: Direction):
        if direction == Direction.RIGHT:
            return Position(x=self.x + 1, y=self.y)
        if direction == Direction.LEFT:
            return Position(x=self.x - 1, y=self.y)
        if direction == Direction.DOWN:
            return Position(x=self.x, y=self.y + 1)
        if direction == Direction.UP:
            return Position(x=self.x, y=self.y - 1)

    def diagonals(self):
        down = self.moved(Direction.DOWN)
        up = self.moved(Direction.UP)
        left = self.moved(Direction.LEFT)
        right = self.moved(Direction.RIGHT)
        return [
            (up.moved(Direction.LEFT), [left, up]),
            (up.moved(Direction.RIGHT), [up, right]),
            (down.moved(Direction.LEFT), [down, left]),
            (down.moved(Direction.RIGHT), [down, right])
        ]
