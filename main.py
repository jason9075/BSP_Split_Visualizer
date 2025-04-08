from bsp import BSP
from dto import Point, Segment
from visualizer import animate_bsp_build, draw_bsp_tree


def load_segments_from_file(filename: str):
    segments = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("#") or not line.strip():
                continue
            x1, y1, x2, y2 = map(float, line.strip().split())
            seg = Segment(Point(x1, y1), Point(x2, y2))
            segments.append(seg)
    return segments


def main():
    segments = load_segments_from_file("files/test.txt")
    bsp = BSP(segments)
    bsp.build()

    animate_bsp_build(segments, bsp.steps)

    positions, indices = bsp.layout_bsp_tree(bsp.root)
    draw_bsp_tree(bsp.root, positions, indices)


if __name__ == "__main__":
    print("Starting BSP segmentation...")
    main()
