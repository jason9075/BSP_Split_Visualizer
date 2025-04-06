import matplotlib
from bsp import BSPNode, BSPLeaf
from matplotlib import animation

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt


def load_segments_from_file(filename):
    segments = []
    with open(filename, "r") as f:
        for line in f:
            if line.strip().startswith("#") or not line.strip():
                continue
            x1, y1, x2, y2 = map(float, line.strip().split())
            segments.append(((x1, y1), (x2, y2)))
    return segments


def choose_partition_line(segments):
    # 簡單策略：總是選第一條
    return segments[0]


def classify_and_split(seg, partition):
    (x1, y1), (x2, y2) = seg
    side1 = point_side((x1, y1), partition)
    side2 = point_side((x2, y2), partition)

    if side1 >= 0 and side2 >= 0:
        return "front"
    if side1 <= 0 and side2 <= 0:
        return "back"
    return "split"


def point_side(point, partition):
    """判斷點在 partition 的哪一側"""
    (px1, py1), (px2, py2) = partition
    (x, y) = point
    # 使用叉積判斷點在哪一側
    return (px2 - px1) * (y - py1) - (py2 - py1) * (x - px1)


def split_segment(seg, partition):
    """將 seg 依照 partition 分割為兩段"""
    (x1, y1), (x2, y2) = seg
    (px1, py1), (px2, py2) = partition

    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = px2 - px1
    dy2 = py2 - py1

    denom = dx1 * dy2 - dy1 * dx2
    if denom == 0:
        # 平行，不處理，歸為 back
        return seg, None

    # 求交點參數 t
    t = ((px1 - x1) * dy2 - (py1 - y1) * dx2) / denom
    ix = x1 + t * dx1
    iy = y1 + t * dy1

    if (ix, iy) == (x1, y1) or (ix, iy) == (x2, y2):
        # 切出來的點跟原點相同，代表太短了
        return seg, None

    return ((x1, y1), (ix, iy)), ((ix, iy), (x2, y2))


def build_bsp(segments, steps=None, depth=0, max_depth=100):
    if steps is None:
        steps = []

    if len(segments) <= 1 or depth >= max_depth:
        return BSPLeaf(segments)

    partition = choose_partition_line(segments)
    steps.append(partition)

    front, back = [], []

    for seg in segments:
        result = classify_and_split(seg, partition)
        if result == "front":
            front.append(seg)
        elif result == "back":
            back.append(seg)
        elif result == "split":
            seg_front, seg_back = split_segment(seg, partition)
            if seg_front:
                front.append(seg_front)
            if seg_back:
                back.append(seg_back)

    return BSPNode(
        partition=partition,
        front=build_bsp(front, depth + 1, max_depth),
        back=build_bsp(back, depth + 1, max_depth),
    )


def draw_segment(ax, seg, color="black"):
    (x1, y1), (x2, y2) = seg
    ax.plot([x1, x2], [y1, y2], color=color)


def visualize_bsp(node, ax, depth=0):
    if isinstance(node, BSPLeaf):
        for seg in node.segments:
            draw_segment(ax, seg, color="gray")
    else:
        draw_segment(ax, node.partition, color=f"C{depth % 10}")
        visualize_bsp(node.front, ax, depth + 1)
        visualize_bsp(node.back, ax, depth + 1)


def animate_bsp_build(segments, steps):
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_title("BSP Partition Build Animation")
    ax.grid(False)

    # 先畫出原始牆面（灰色）
    for seg in segments:
        draw_segment(ax, seg, color="lightgray")

    partition_lines = []

    def init():
        return partition_lines

    def update(frame):
        if frame >= len(steps):
            return partition_lines

        seg = steps[frame]
        (line,) = ax.plot(
            [seg[0][0], seg[1][0]],
            [seg[0][1], seg[1][1]],
            color=f"C{frame % 10}",
            linewidth=2,
        )
        partition_lines.append(line)
        return partition_lines

    animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=len(steps),
        interval=800,
        blit=True,
        repeat=False,
    )

    plt.show()


def main():
    segments = load_segments_from_file("files/test.txt")
    # bsp = build_bsp(segments)
    steps = []
    bsp = build_bsp(segments, steps)

    animate_bsp_build(segments, steps)

    # fig, ax = plt.subplots()
    # ax.set_aspect("equal")
    # visualize_bsp(bsp, ax)
    # plt.title("Map Segmentation with BSP")
    # plt.grid(False)
    # plt.show()


if __name__ == "__main__":
    print("Starting BSP segmentation...")
    main()
