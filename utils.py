from dto import Point, Segment


def classify_and_split(seg: Segment, partition: Segment) -> str:
    """will return "front", "back", or "split" """
    side1 = point_side(seg.start, partition)
    side2 = point_side(seg.end, partition)

    if side1 >= 0 and side2 >= 0:
        return "front"
    if side1 <= 0 and side2 <= 0:
        return "back"
    return "split"


def point_side(point: Point, partition: Segment) -> float:
    """判斷點在 partition 的哪一側"""
    p1, p2 = partition.start, partition.end
    (x, y) = point.x, point.y
    # use cross product to determine the side
    return (p2.x - p1.x) * (y - p1.y) - (p2.y - p1.y) * (x - p1.x)
