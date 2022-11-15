# tree, but leaf nodes collide with the opposite leaf of a sibling node
class OverlappingTree:
    def __init__(self, depth):
        self.__depth = depth
        self._data = [[0 for _ in range(2 * i + 1)] for i in range(depth + 1)]

    def __getitem__(self, key):
        return self._data[key[0]][key[1] + key[0]]

    def __setitem__(self, key, value):
        self._data[key[0]][key[1] + key[0]] = value

    def greeks(self, s_0, u, d, d_t):
        d_u = (self[2, 2] - self[2, 0]) / s_0 / (u * u - 1)
        d_d = (self[2, 0] - self[2, -2]) / s_0 / (1 - d * d)
        return (self[1, 1] - self[1, -1]) / s_0 / (u - d), (d_u - d_d) / s_0 / (u - d), (self[2, 0] - self[0, 0]) / 2 / d_t / 365

    def print_greeks(self, s_0, u, d, d_t):
        greeks = self.greeks(s_0, u, d, d_t)
        print(f"  delta: {greeks[0]:.6f}")
        print(f"  gamma: {greeks[1]:.6f}")
        print(f"  theta: {greeks[2]:.6f}")
