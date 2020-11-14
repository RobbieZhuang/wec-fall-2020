import GameState

def optimal_for_station(state, coords):
    tiles = state.tiles
    max = []
    for row in range(len(tiles)):
        for col in range(len(tiles[row])):
            if abs(row - coords[0]) + abs(col - coords[1]) > state.max_fuel / 2:
                continue
            

def max_path(state, a, b):
    # return actions[]