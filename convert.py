from math import isclose, hypot
import bsp_tool
import struct
import tqdm
from dto import Point


class Edge:
    def __init__(self, vertex1: Point, vertex2: Point):
        # force line is left to right and up to down
        if (vertex1.x > vertex2.x) or (
            vertex1.x == vertex2.x and vertex1.y > vertex2.y
        ):
            vertex1, vertex2 = vertex2, vertex1
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.dx = self.vertex2.x - self.vertex1.x
        self.dy = self.vertex2.y - self.vertex1.y
        self.slope = self.dy / self.dx if self.dx != 0 else float("inf")
        self.length = hypot(self.dx, self.dy)
        if self.length != 0:
            self.direction = (self.dx / self.length, self.dy / self.length)
        else:
            self.direction = (0.0, 0.0)

    def __repr__(self):
        return f"Edge({self.vertex1}, {self.vertex2})"

    def __str__(self):
        return f"Edge({self.vertex1}, {self.vertex2})"

    def is_same_line(self, other, epsilon=0.0001):
        dot = (
            self.direction[0] * other.direction[0]
            + self.direction[1] * other.direction[1]
        )
        if not isclose(abs(dot), 1.0, abs_tol=epsilon):
            return False

        # 將 other.vertex1 投影到 self 線段上，檢查是否共線（偏移量一致）
        dx = other.vertex1.x - self.vertex1.x
        dy = other.vertex1.y - self.vertex1.y
        cross = self.dx * dy - self.dy * dx
        return abs(cross) < epsilon

    def is_overlapping_or_touching(self, other, epsilon=0.0001):
        if not self.is_same_line(other, epsilon):
            return False

        # 用 1D 投影的方式檢查是否重疊
        def project_1d(p):
            return p.x * self.direction[0] + p.y * self.direction[1]

        p1 = project_1d(self.vertex1)
        p2 = project_1d(self.vertex2)
        q1 = project_1d(other.vertex1)
        q2 = project_1d(other.vertex2)

        a, b = sorted([p1, p2])
        c, d = sorted([q1, q2])

        return not (d < a - epsilon or c > b + epsilon)

    def merge_with(self, other):
        points = [self.vertex1, self.vertex2, other.vertex1, other.vertex2]
        # 排序後取頭尾
        points = sorted(
            points, key=lambda p: (p.x * self.direction[0] + p.y * self.direction[1])
        )
        return Edge(points[0], points[-1])


def parse_vertices(raw_date: bytes):
    vertices = []
    stride = 12  # 3 floats (x, y, z) * 4 bytes each
    count = len(raw_date) // stride

    for i in range(count):
        start = i * stride
        end = start + stride
        vertex_data = raw_date[start:end]
        x, y, z = struct.unpack("<fff", vertex_data)
        vertices.append((x, y, z))

    print("Total vertices:", len(vertices))
    return vertices


def parse_edges(raw_data: bytes):
    edges = []
    stride = 4  # 2 shorts (vertex1, vertex2) * 2 bytes each
    count = len(raw_data) // stride

    for i in range(count):
        start = i * stride
        end = start + stride
        edge_data = raw_data[start:end]
        vertex1, vertex2 = struct.unpack("<HH", edge_data)
        edges.append((vertex1, vertex2))

    print("Total edges:", len(edges))
    return edges


def save_to_file(filename: str, edges: list):
    print("Saving to file:", filename)
    with open(filename, "w", encoding="utf-8") as file:
        # tqdm for progress bar
        for edge in tqdm.tqdm(edges, desc="Writing edges", unit="edge"):
            x1, y1 = edge.vertex1.x, edge.vertex1.y
            x2, y2 = edge.vertex2.x, edge.vertex2.y
            file.write(f"{x1:.1f} {y1:.1f} {x2:.1f} {y2:.1f}\n")


def main():

    bsp = bsp_tool.load_bsp("files/de_dust2.bsp")

    # print(dir(bsp))
    print("bsp headers:")
    print(bsp.headers)

    print("parsing VERTICES")
    vertices = parse_vertices(bsp.lump_as_bytes("VERTICES"))

    print("parsing EDGES")
    edges = parse_edges(bsp.lump_as_bytes("EDGES"))

    # filter edges to remove those that are not part of the map
    edges = [
        e
        for e in edges
        if abs(vertices[e[0]][0] - vertices[e[1]][0]) > 10
        or abs(vertices[e[0]][1] - vertices[e[1]][1]) > 10
    ]

    # filter duplicate edges
    edges = list(set(edges))

    edge_list = []
    for edge in tqdm.tqdm(edges, desc="Processing edges", unit="edge"):
        v1 = vertices[edge[0]]
        v2 = vertices[edge[1]]
        edge_list.append(Edge(Point(v1[0], v1[1]), Point(v2[0], v2[1])))

    # put same edges slope in dictionary
    data = {}
    for edge in edge_list:
        if edge.slope not in data:
            data[edge.slope] = []
        data[edge.slope].append(edge)

    print(len(data), "unique slopes")

    final_edges = []
    for _, group in data.items():
        merged = []
        group = sorted(
            group, key=lambda e: (e.vertex1.x, e.vertex1.y, e.vertex2.x, e.vertex2.y)
        )

        while group:
            current = group.pop(0)
            i = 0
            while i < len(group):
                if current.is_overlapping_or_touching(group[i]):
                    current = current.merge_with(group[i])
                    group.pop(i)  # remove merged one
                    i = 0  # restart scan
                else:
                    i += 1
            merged.append(current)
        final_edges.extend(merged)

    print("Filtered edges:", len(final_edges))

    save_to_file("files/de_dust2.txt", final_edges)  # optimized
    # save_to_file("files/de_dust2.txt", edge_list) # origin


if __name__ == "__main__":
    print("converting...")
    main()
