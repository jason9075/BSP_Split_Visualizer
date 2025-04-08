class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class Segment:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Segment({self.start}, {self.end})"

    def __str__(self):
        return f"Segment({self.start}, {self.end})"
