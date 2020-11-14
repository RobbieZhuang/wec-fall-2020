import GameState
import Util

def eq_pt(p1, p2):
    return p1[0] == p2[0] and p1[1] == p2[1]

def optimal_for_station(state, coords):
    tiles = state.tiles
    max = []
    for row in range(len(tiles)):
        for col in range(len(tiles[row])):
            if abs(row - coords[0]) + abs(col - coords[1]) > state.max_fuel / 2:
                continue

def find_good_endpoint(state, station, start_point, fuel):
    if eq_pt(start_point, station):
        return None

    int best_point = start_point
    int score = 0

    for i in range(-max_dist, max_dist):
        for j in range(-max_dist, max_dist):
            new_point = [start_point[0]-i, start_point[1]-j]
            dist = abs(i) + abs(j)
            station_dist = abs(new_point[0] - station[0]) + abs(new_point[1], station[1])
            if state.in_board(new_point) and dist > 0 and dist + station_dist <= fuel:
                weight = state.get_contam(new_point)/(dist*8)
                if weight > score and weight > 1:
                    score = weight
                    best_point = new_point

    if eq_pt(best_point, start_point):
        return station
    return best_point


def get_score_actions_for_robot(i, gamestate):
    robot = gamestate.robot[i]
    # Move robot initial
    start_point = robot.position
    next_point = find_good_endpoint(gamestate, robot.position, robot.fuel)
    while next_point is not None:
        actions = max_path()


        start_point = next_point
        next_point = find_good_endpoint(gamestate, start_point, robot.fuel)
    max_path

def max_path(state, a, b):
    def max_path_helper(row, col):
        if not state.in_board([row, col]):
            return 0
        if dp[row][col] != -1:
            return dp[row][col]
        v = max_path_helper(row + verticalmove, col)
        h = max_path_helper(row, col + sidemove)
        dp[row][col] = max(v, h) + state.tiles[row][col]
        return dp[row][col]

    verticalmove = 1 if b[0] > a[0] else -1
    sidemove = 1 if b[1] > a[1] else -1
    dp = [[-1 for _ in range(abs(b[1] - a[1]))] for _ in range(abs(b[0] - a[0]))]
    max_path_helper(a[0], a[1])
    return dp[a[0]][a[1]]
