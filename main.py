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
    # ask which file to load
    print("Select a file to load:\n")
    print("1. files/test.txt")
    print("2. files/de_dust2.txt")
    print("3. files/e1m1.txt")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        player_loc = Point(1.4, 1.6)
        segments = load_segments_from_file("files/test.txt")
    elif choice == "2":
        player_loc = Point(379, 2193)
        segments = load_segments_from_file("files/de_dust2.txt")
    elif choice == "3":
        player_loc = Point(1056, -3616)
        segments = load_segments_from_file("files/e1m1.txt")
    else:
        print("Invalid choice. Exiting.")
        return

    # Visualize the segments and the BSP tree
    visualizer = Visualizer(segments)

    # visualizer.render_map()

    bsp = BSP(segments, max_depth=20, min_segments=10)
    bsp.build(method="score")

    # visualizer.animate_split(bsp.steps, interval=100)

    # positions = bsp.layout_bsp_tree(bsp.root)
    # visualizer.draw_bsp_tree(bsp.root, positions, show_text=False)

    visualizer.render_sectors(player_loc, bsp.root)

    visualizer.show()


if __name__ == "__main__":
    print(">>>>> Starting BSP segmentation...")
    main()
