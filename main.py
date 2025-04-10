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
            # force line is left to right and up to down
            if (x1 > x2) or (x1 == x2 and y1 > y2):
                x1, y1, x2, y2 = x2, y2, x1, y1

            seg = Segment(Point(x1, y1), Point(x2, y2), seg_id=str(idx))
            segments.append(seg)
            idx += 1
    return segments


def main():
    # segments = load_segments_from_file("files/test.txt")
    segments = load_segments_from_file("files/de_dust2.txt")

    # Visualize the segments and the BSP tree
    visualizer = Visualizer(segments)

    # visualizer.render_map()

    bsp = BSP(segments, max_depth=20, min_segments=10)
    bsp.build(method="score")

    visualizer.animate_split(bsp.steps, interval=100)

    # positions = bsp.layout_bsp_tree(bsp.root)
    # visualizer.draw_bsp_tree(bsp.root, positions, show_text=False)

    player_loc = Point(1.4, 1.6)
    # visualizer.render_sectors(player_loc, bsp.root)

    visualizer.show()


if __name__ == "__main__":
    print(">>>>> Starting BSP segmentation...")
    main()
