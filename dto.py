class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


class Segment:
    def __init__(self, start: Point, end: Point, seg_id: str = "no_id"):
        self.seg_id = seg_id
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Segment({self.seg_id}, {self.start}, {self.end})"

    def __str__(self):
        return f"Segment({self.seg_id}, {self.start}, {self.end})"
