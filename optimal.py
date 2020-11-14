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
    def max_path_helper(row, col):
        if not state.in_board([row, col]):
            return 0
        if dp[row][col][0] != -1:
            return dp[row][col][0]
        if b[0] == row and b[1] == col:
            return (state.tiles[row][col], [])
        v = max_path_helper(row + verticalmove, col)
        h = max_path_helper(row, col + sidemove)
        dp[row][col][0] = max(v, h) + state.tiles[row][col]
        dp[row][col][1] = [row + verticalmove, col] if v >= h else [row, col + sidemove]
        return dp[row][col]

    verticalmove = 1 if b[0] > a[0] else -1
    sidemove = 1 if b[1] > a[1] else -1
    dp = [[(-1, []) for _ in range(abs(b[1] - a[1]))] for _ in range(abs(b[0] - a[0]))]
    max_path_helper(a[0], a[1])

    point = a
    path = []
    while point != b:
        path.append(dp[point[0]][point[1]][1])
        point = path[-1]

    return (dp[a[0]][a[1]], path)
