from typing import Union, Optional
from dto import Segment, Point
from utils import classify_and_split


class BSPNode:
    def __init__(
        self,
        partition: Segment,
        front: Optional[Union["BSPNode", "BSPLeaf"]],
        back=Optional[Union["BSPNode", "BSPLeaf"]],
    ):
        self.partition = partition  # wall line
        self.front = front  # BSPNode or Leaf
        self.back = back

    def __repr__(self):
        return (
            f"BSPNode(partition={self.partition}, front={self.front}, back={self.back})"
        )

    def __str__(self):
        return (
            f"BSPNode(partition={self.partition}, front={self.front}, back={self.back})"
        )


class BSPLeaf:
    def __init__(self, segments: list[Segment]):
        self.segments = segments

    def __repr__(self):
        return f"BSPLeaf(segments={self.segments})"

    def __str__(self):
        return f"BSPLeaf(segments={self.segments})"


class BSP:
    def __init__(self, segments: list[Segment], max_depth: int = 20):
        self.segments = segments
        self.steps = []  # used for animation
        self.max_depth = max_depth
        self.root = None

    def build(self):
        self.root = self._build_bsp(self.segments, 0)

    def _build_bsp(self, segments: list[Segment], depth: int):
        """
        segments: wall segments
        steps: used for animation
        depth: current depth of recursion
        max_depth: max depth of recursion
        """
        if len(segments) <= 1 or depth >= self.max_depth:
            return BSPLeaf(segments)

        partition = self._choose_partition_line(segments)
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
            front=self._build_bsp(front, depth + 1),
            back=self._build_bsp(back, depth + 1),
        )

    def _choose_partition_line(self, segments: list[Segment]) -> Segment:
        # simple heuristic: choose the first segment as the partition line
        return segments[0]

    def _split_segment(
        self, seg: Segment, partition: Segment
    ) -> tuple[Segment, Optional[Segment]]:
        """將 seg 依照 partition 分割為兩段"""
        s1, s2 = seg.start, seg.end
        p1, p2 = partition.start, partition.end

        dx1 = s2.x - s1.x
        dy1 = s2.y - s2.y
        dx2 = p2.x - p1.x
        dy2 = p2.y - p1.y

        denom = dx1 * dy2 - dy1 * dx2
        if denom == 0:
            # parallel lines, no intersection
            return seg, None

        # calculate intersection point
        t = ((p1.x - s1.x) * dy2 - (p1.y - s1.y) * dx2) / denom
        ix = s1.x + t * dx1
        iy = s1.y + t * dy1

        if (ix, iy) == (s1.x, s1.y) or (ix, iy) == (s2.x, s2.y):
            # no split, return original segment
            return seg, None

        return Segment(s1, Point(ix, iy)), Segment(Point(ix, iy), s2)

    def layout_bsp_tree(
        self,
        node,
        x: float = 0.0,
        y: float = 0.0,
        level_gap: float = 1.5,
        x_gap: float = 1.0,
        positions=None,
        counter=None,
        node_indices=None,
        current_index=None,
    ) -> tuple[dict, dict]:
        """
        Recursively assign positions and indices to each node.
        """
        if positions is None:
            positions = {}
        if counter is None:
            counter = [0.0]  # mutable counter to track x-position
        if node_indices is None:
            node_indices = {}
        if current_index is None:
            current_index = [0]

        if isinstance(node, BSPLeaf):
            positions[id(node)] = (counter[0], y)
            node_indices[id(node)] = None  # Leaf has no index
            counter[0] += x_gap
            return positions, node_indices

        # Assign index to node
        node_indices[id(node)] = current_index[0]
        current_index[0] += 1

        # Recurse on children
        self.layout_bsp_tree(
            node.front,
            x,
            y + level_gap,
            level_gap,
            x_gap,
            positions,
            counter,
            node_indices,
            current_index,
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
            node_indices,
            current_index,
        )

        return positions, node_indices
