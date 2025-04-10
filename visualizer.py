import matplotlib

matplotlib.use("TkAgg")

from bsp import BSPLeaf
from dto import Segment, Point
from matplotlib import animation


import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, segments: list[Segment]):
        self.segments = segments
        self.anim = None
        self.node_idx = 0

    def animate_split(self, steps: list[Segment]):
        fig, ax = self._create_figure("Partition Line Animation")
        self._draw_segments(ax, self.segments, color="lightgray")

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

        self.anim = animation.FuncAnimation(
            fig,
            update,
            init_func=init,
            frames=len(steps),
            interval=800,
            blit=True,
            repeat=False,
        )

    def draw_bsp_tree(self, node, positions, depth=0, show_text=False):
        fig, ax = self._create_figure("BSP Tree Structure")
        self.node_idx = 0
        self._draw_bsp_tree_node(ax, node, positions, show_text, depth)
        ax.invert_yaxis()  # Root at top

    def draw_same_sector(self, player_loc: Point, root):
        """draw the same segments with the same color"""
        fig, ax = self._create_figure("Same Sector")

        # Draw all segments in light gray
        self._draw_segments(ax, self.segments, color="lightgray")
        # Draw the player location
        ax.plot(player_loc.x, player_loc.y, "o", color="red")
        ax.text(
            player_loc.x,
            player_loc.y,
            "Player",
            ha="center",
            va="bottom",
            fontsize=8,
        )

        # Find the player location in the segments

        same_segments = []

    def show(self):
        plt.show()

    # ========== Private Helpers ==========

    def _create_figure(self, title: str):
        fig, ax = plt.subplots()
        ax.set_title(title, pad=20)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.grid(False)
        return fig, ax

    def _draw_segments(self, ax, segments: list[Segment], color="black"):
        for seg in segments:
            self._draw_segment(ax, seg, color)

    def _draw_segment(self, ax, seg: Segment, color="black"):
        s1, s2 = seg.start, seg.end
        ax.plot([s1.x, s2.x], [s1.y, s2.y], color=color)

    def _draw_bsp_tree_node(self, ax, node, positions, show_text=False, depth=0):
        node_id = id(node)
        x, y = positions[node_id]

        if isinstance(node, BSPLeaf):
            ax.plot(x, y, "o", color="gray")
            list_segments = ""
            for seg in node.segments:
                list_segments += f"{seg.seg_id}: {seg.start}→{seg.end}\n"
            text = f"{node.side}\n{list_segments}" if show_text else ""
            ax.text(
                x,
                y,
                text,
                ha="center",
                va="bottom",
                fontsize=8,
            )
        else:  # BSPNode
            ax.plot(x, y, "s", color=f"C{self.node_idx % 10}", markersize=12)
            self.node_idx += 1
            (p1, p2) = node.partition.start, node.partition.end
            pline = f"#{node.partition.seg_id}: ({p1.x:.1f},{p1.y:.1f})→({p2.x:.1f},{p2.y:.1f})"
            front_segments = ""
            for seg in node.seg_front:
                front_segments += f"{seg.seg_id}: {seg.start}→{seg.end}\n"
            back_segments = ""
            for seg in node.seg_back:
                back_segments += f"{seg.seg_id}: {seg.start}→{seg.end}\n"
            text = (
                f"{pline}\nF:\n{front_segments}B:\n{back_segments}" if show_text else ""
            )
            ax.text(
                x,
                y,
                text,
                ha="center",
                va="bottom",
                fontsize=8,
            )

            for child in [node.front, node.back]:
                child_id = id(child)
                cx, cy = positions[child_id]
                ax.plot([x, cx], [y, cy], "k-", linewidth=0.8)
                self._draw_bsp_tree_node(ax, child, positions, show_text, depth + 1)

    def _visualize_bsp(self, node, ax, depth=0):
        if isinstance(node, BSPLeaf):
            for seg in node.segments:
                self._draw_segment(ax, seg, color="gray")
        else:
            self._draw_segment(ax, node.partition, color=f"C{depth % 10}")
            self._visualize_bsp(node.front, ax, depth + 1)
            self._visualize_bsp(node.back, ax, depth + 1)
