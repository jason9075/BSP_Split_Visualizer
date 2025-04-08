import matplotlib

matplotlib.use("TkAgg")

from typing import List
from bsp import BSPLeaf
from dto import Segment
from matplotlib import animation


import matplotlib.pyplot as plt


def draw_segment(ax, seg: Segment, color="black"):
    s1, s2 = seg.start, seg.end
    ax.plot([s1.x, s2.x], [s1.y, s2.y], color=color)


def visualize_bsp(node, ax, depth: int = 0):
    if isinstance(node, BSPLeaf):
        for seg in node.segments:
            draw_segment(ax, seg, color="gray")
    else:
        draw_segment(ax, node.partition, color=f"C{depth % 10}")
        visualize_bsp(node.front, ax, depth + 1)
        visualize_bsp(node.back, ax, depth + 1)


def animate_bsp_build(segments: List[Segment], steps: List[Segment]):
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_title("BSP Partition Build Animation")
    ax.grid(False)

    # draw initial segments (gray)
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
            [seg.start.x, seg.end.x],
            [seg.start.y, seg.end.y],
            color=f"C{frame % 10}",
            linewidth=2,
        )
        partition_lines.append(line)
        return partition_lines

    _ = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=len(steps),
        interval=800,
        blit=True,
        repeat=False,
    )

    plt.show()


def draw_bsp_tree(node, positions, indices, depth=0):

    fig, ax = plt.subplots()
    ax.set_title("BSP Tree Structure", pad=20)

    reculsive_draw(node, ax, positions, indices, depth)

    ax.set_aspect("equal")
    ax.invert_yaxis()  # make root at top
    ax.axis("off")
    plt.show()


def reculsive_draw(node, ax, positions, indices, depth=0):
    node_id = id(node)
    x, y = positions[node_id]
    index = indices[node_id]

    if isinstance(node, BSPLeaf):
        ax.plot(x, y, "o", color="gray")
        ax.text(
            x, y, f"Leaf\n{len(node.segments)}", ha="center", va="bottom", fontsize=8
        )
    else:
        ax.plot(x, y, "s", color=f"C{depth % 10}")
        # Partition segment
        (p1, p2) = node.partition.start, node.partition.end
        ax.text(
            x,
            y,
            f"#{index}\n({p1.x:.1f},{p1.y:.1f})→({p2.x:.1f},{p2.y:.1f})",
            ha="center",
            va="bottom",
            fontsize=8,
        )

        for child in [node.front, node.back]:
            child_id = id(child)
            cx, cy = positions[child_id]
            ax.plot([x, cx], [y, cy], "k-", linewidth=0.8)
            reculsive_draw(child, ax, positions, indices, depth + 1)
