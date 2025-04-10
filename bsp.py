from typing import Union, Optional
from dto import Segment, Point
from utils import classify_and_split
import tqdm


class BSPNode:
    def __init__(
        self,
        partition: Segment,
        front: Optional[Union["BSPNode", "BSPLeaf"]],
        back=Optional[Union["BSPNode", "BSPLeaf"]],
        seg_front: Optional[list[Segment]] = None,
        seg_back: Optional[list[Segment]] = None,
    ):
        self.partition = partition  # wall line
        self.front = front  # BSPNode or Leaf
        self.back = back
        self.seg_front = seg_front if seg_front is not None else []
        self.seg_back = seg_back if seg_back is not None else []

    def __repr__(self):
        return f"BSPNode(partition={self.partition}, front={self.seg_front}, back={self.seg_back})"

    def __str__(self):
        return f"BSPNode(partition={self.partition}, front={self.seg_front}, back={self.seg_back})"


class BSPLeaf:
    def __init__(self, segments: list[Segment], side: Optional[str] = None):
        self.segments = segments
        self.side = side  # "front" or "back"

    def __repr__(self):
        return f"BSPLeaf(segments={self.segments}, side={self.side})"

    def __str__(self):
        return f"BSPLeaf(segments={self.segments}, side={self.side})"


class BSP:
    def __init__(
        self, segments: list[Segment], max_depth: int = 20, min_segments: int = 2
    ):
        self.segments = segments
        self.steps = []  # used for animation
        self.max_depth = max_depth
        self.min_segments = min_segments
        self.root = None
        self.depth = 0

    def build(self, method: str = "score"):
        self.root = self._build_bsp(self.segments, 0, method=method)

    def _build_bsp(
        self,
        segments: list[Segment],
        depth: int,
        side: Optional[str] = None,
        method: str = "score",
    ):
        """
        segments: wall segments
        steps: used for animation
        depth: current depth of recursion
        max_depth: max depth of recursion
        """
        if len(segments) <= self.min_segments or depth >= self.max_depth:
            self.depth = depth
            return BSPLeaf(segments, side)

        partition = self._choose_partition_line(segments, method=method)
        self.steps.append(partition)

        front, back = [], []

        for seg in segments:
            if seg == partition:
                continue
            result = classify_and_split(seg, partition)
            if result == "front":
                front.append(seg)
            elif result == "back":
                back.append(seg)
            elif result == "split":
                seg_front, seg_back = self._split_segment(seg, partition)
                if seg_front:
                    front.append(seg_front)
                if seg_back:
                    back.append(seg_back)

        return BSPNode(
            partition=partition,
            front=self._build_bsp(front, depth + 1, side="front"),
            back=self._build_bsp(back, depth + 1, side="back"),
            seg_front=front,
            seg_back=back,
        )

    def _choose_partition_line(
        self, segments: list[Segment], method: str = "score"
    ) -> Segment:
        # simple heuristic: choose the first segment as the partition line
        if method == "simple":
            return segments[0]

        # more complex heuristic: choose the longest segment as the partition line
        if method == "score":
            partition = segments[0]
            best_split_score = 999999
            for candi in tqdm.tqdm(
                segments, desc="Choosing partition line", unit="candi"
            ):
                score = 0
                front_count = 0
                back_count = 0
                for seg in segments:
                    if seg == candi:
                        continue
                    result = classify_and_split(seg, candi)
                    if result == "split":
                        score += 1
                    elif result == "front":
                        front_count += 1
                    elif result == "back":
                        back_count += 1
                score += abs(front_count - back_count)  # balance

                if score < best_split_score:
                    best_split_score = score
                    partition = candi

            return partition

        raise ValueError(f"Unknown partition method: {method}")

    def _split_segment(
        self, seg: Segment, partition: Segment
    ) -> tuple[Segment, Optional[Segment]]:
        """
        Split a segment by a partition line. Will return two segments if split,
        otherwise return the original segment and None. The first segment is
        front of the partition line, the second is back.
        """
        s1, s2 = seg.start, seg.end
        p1, p2 = partition.start, partition.end

        dsx, dsy = s2.x - s1.x, s2.y - s1.y  # vector of segment
        dpx, dpy = p2.x - p1.x, p2.y - p1.y  # vector of partition line

        epsilon = 1e-6

        # calculate the determinant
        denom = dsx * dpy - dsy * dpx
        if abs(denom) < epsilon:
            # parallel lines, no intersection
            return seg, None

        # calculate intersection point
        t = ((p1.x - s1.x) * dpy - (p1.y - s1.y) * dpx) / denom
        ix = s1.x + t * dsx
        iy = s1.y + t * dsy

        # no split, return original segment
        if abs(ix - s1.x) < epsilon and abs(iy - s1.y) < epsilon:
            return seg, None
        if abs(ix - s2.x) < epsilon and abs(iy - s2.y) < epsilon:
            return seg, None

        return (
            Segment(s1, Point(ix, iy), seg_id=f"{seg.seg_id}/{partition.seg_id}-f"),
            Segment(Point(ix, iy), s2, seg_id=f"{seg.seg_id}/{partition.seg_id}-b"),
        )

    def layout_bsp_tree(
        self,
        node,
        x: float = 0.0,
        y: float = 0.0,
        level_gap: float = 1.5,
        x_gap: float = 1.0,
        positions=None,
        counter=None,
    ) -> dict:
        """
        Recursively assign positions and indices to each node.
        """
        if positions is None:
            positions = {}
        if counter is None:
            counter = [0.0]  # mutable counter to track x-position

        if isinstance(node, BSPLeaf):
            positions[id(node)] = (counter[0], y)
            counter[0] += x_gap
            return positions

        # Recurse on children
        self.layout_bsp_tree(
            node.front, x, y + level_gap, level_gap, x_gap, positions, counter
        )
        node_x = counter[0]
        positions[id(node)] = (node_x, y)
        counter[0] += x_gap
        self.layout_bsp_tree(
            node.back,
            x,
            y + level_gap,
            level_gap,
            x_gap,
            positions,
            counter,
        )

        return positions
