import os


pro_path = os.path.dirname(os.path.abspath(__file__))
map_path = os.path.join(pro_path, 'maps')

maps = os.listdir(map_path)

speed = 30
which_map = os.path.join(map_path, maps[1])


if __name__ == '__main__':
    print(os.listdir(map_path))
