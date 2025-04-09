from bsp import BSP
from dto import Point, Segment
from visualizer import Visualizer


def load_segments_from_file(filename: str):
    segments = []
    idx = 0
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("#") or not line.strip():
                continue
            x1, y1, x2, y2 = map(float, line.strip().split())
            seg = Segment(Point(x1, y1), Point(x2, y2), seg_id=str(idx))
            segments.append(seg)
            idx += 1
    return segments


def main():
    segments = load_segments_from_file("files/test.txt")

    bsp = BSP(segments)
    bsp.build()
    print("root front:", bsp.root.front.front.front)
    positions = bsp.layout_bsp_tree(bsp.root)
    # print("Positions:", positions)
    # print("Indices:", indices)

    # Visualize the segments and the BSP tree
    visualizer = Visualizer(segments)
    # visualizer.animate_split(bsp.steps)
    visualizer.draw_bsp_tree(bsp.root, positions)

    player_loc = Point(1.4, 1.6)
    # visualizer.draw_same_sector(player_loc, bsp.root)

    visualizer.show()


if __name__ == "__main__":
    print(">>>>> Starting BSP segmentation...")
    main()
