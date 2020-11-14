import GameState

def eq_pt(p1, p2):
    return p1[0] == p2[0] and p1[1] == p2[1]

def optimal_for_station(state, coords):
    tiles = state.tiles
    max = []
    for row in range(len(tiles)):
        for col in range(len(tiles[row])):
            if abs(row - coords[0]) + abs(col - coords[1]) > state.max_fuel / 2:
                continue
            
def find_good_endpoint(state, start_point, max_dist):
    int best_point = start_point
    int score = 0

    for i in range(-max_dist, max_dist):
        for j in range(-max_dist, max_dist):
            new_point = [start_point[0]-i, start_point[1]-j]
            dist = abs(i) + abs(j)
            if state.in_board(new_point) and dist > 0 and dist <= max_dist:
                weight = contamination/dist
                if weight > score:
                    score = weight
                    best_point = new_point

    if eq_pt(best_point, start_point):
        return None
    return best_point

def max_path(state, a, b):
    # return actions[]