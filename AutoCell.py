import config
import os


class Space:

    def __init__(self):
        self.map_height = 40
        self.map_width = 40
        self.start_map = [[0 for _ in range(self.map_width)] for _ in range(self.map_width)]
        self.space = [[[0, 0] for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.map_space()
        self.lives = 0

    @staticmethod
    def begin_map(text):
        map_file = open(os.path.join(config.map_path, text), mode='r', encoding='utf-8')
        origin_map = map_file.readlines()
        map_file.close()
        origin_map = [i.strip() for i in origin_map]
        origin_map = [i.split(' ') for i in origin_map]
        origin_map = [[int(j) for j in i] for i in origin_map]
        map_widths = [len(i) for i in origin_map]
        map_heights = len(origin_map)
        if max(map_widths) != min(map_widths):
            print('wrong map!')
        else:
            return [origin_map, max(map_widths), map_heights]

    def size(self):
        return [self.map_width, self.map_height]

    # 整理地图
    def map_space(self):
        for i in range(self.map_height):
            for j in range(self.map_width):
                self.space[i][j][0] = self.start_map[i][j]

    def neighbor_count(self, location, level):
        counts = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                elif location[0] + i < 0 or location[0] + i >= self.map_height:
                    continue
                elif location[1] + j < 0 or location[1] + j >= self.map_width:
                    continue
                else:
                    counts = counts + self.space[location[0] + i][location[1] + j][level]
        return counts

    def next_map(self, level):
        next_level = 1 - level
        for i in range(self.map_height):
            for j in range(self.map_width):
                if self.neighbor_count([i, j], level) < 2:
                    self.space[i][j][next_level] = 0
                elif self.neighbor_count([i, j], level) > 3:
                    self.space[i][j][next_level] = 0
                elif self.neighbor_count([i, j], level) in [2, 3] and self.space[i][j][level] == 1:
                    self.space[i][j][next_level] = 1
                elif self.neighbor_count([i, j], level) == 3 and self.space[i][j][level] == 0:
                    self.space[i][j][next_level] = 1
                elif self.neighbor_count([i, j], level) == 2 and self.space[i][j][level] == 0:
                    self.space[i][j][next_level] = 0

    def new_map(self, time_passed):
        level = time_passed % 2
        self.next_map(level)

    def reload_map(self, text):
        if text in config.maps:
            re_map = self.begin_map(text)
            self.map_height = re_map[2]
            self.map_width = re_map[1]
            self.start_map = re_map[0]
            self.space = [[[0, 0] for _ in range(self.map_width)] for _ in range(self.map_height)]
            self.map_space()
        else:
            self.start_map = [[0 for _ in range(self.map_width)] for _ in range(self.map_width)]
            self.space = [[[0, 0] for _ in range(self.map_width)] for _ in range(self.map_height)]

    def change_map(self, location):
        self.space[location[1]][location[0]][0] = 1 - self.space[location[1]][location[0]][0]
        if self.space[location[1]][location[0]][0] == 1:
            self.lives = self.lives + 1
        else:
            self.lives = self.lives - 1

    def get_lives(self):
        return self.lives
