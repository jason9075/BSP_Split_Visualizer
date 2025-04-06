class BSPNode:
    def __init__(self, partition, front=None, back=None):
        self.partition = partition  # 線段
        self.front = front  # BSPNode or Leaf
        self.back = back


class BSPLeaf:
    def __init__(self, segments):
        self.segments = segments
