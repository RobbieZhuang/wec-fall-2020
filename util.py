UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

directions = [UP, DOWN, LEFT, RIGHT]

def equal_space_base_stations(tiles, n):
    total_len = border_length(tiles)

    placed = 0
    base_stations = []

    for i, pos in enumerate(border_positions(tiles)):
        if i / total_len >= placed / n:
            placed += 1
            base_stations.append(pos)
        if placed == n:
            break

    return base_stations

def border_length(tiles):
    rows, cols = tiles.shape
    return rows * 2 + cols * 2

def border_positions(tiles):
    rows, cols = tiles.shape
    for i in range(cols):
        yield ((-1, i), DOWN)
    for i in range(rows):
        yield ((i, cols), LEFT)
    for i in range(cols):
        yield ((rows, cols - i - 1), UP)
    for i in range(rows):
        yield ((rows - i - 1, -1), RIGHT)
