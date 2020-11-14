def eq_pt(p1, p2):
    return p1[0] == p2[0] and p1[1] == p2[1]

def optimal_for_station(state, coords):
    tiles = state.tiles
    max = []
    for row in range(len(tiles)):
        for col in range(len(tiles[row])):
            if abs(row - coords[0]) + abs(col - coords[1]) > state.max_fuel / 2:
                continue

# Returns none if there is no "good" next point
def find_good_endpoint(state, station, start_point, fuel, fluid):
    best_point = start_point
    score = 0

    for i in range(-fuel, fuel):
        for j in range(-fuel, fuel):
            new_point = [start_point[0]-i, start_point[1]-j]

            dist = abs(i) + abs(j)
            dist_new_to_station = abs(new_point[0] - station[0]) + abs(new_point[1] - station[1])
            
            if state.in_board_coord(new_point[0], new_point[1]) and dist > 0 and dist + dist_new_to_station <= fuel:
                weight = min(state.get_contam(new_point), fluid) / (dist*8)
                if weight > score and weight > 1:
                    score = weight
                    best_point = new_point

    if eq_pt(best_point, start_point):
        return None
    return best_point

def run_actions_for_robot(i, gamestate):
    robot = gamestate.robots[i]
    station = robot.position

    gamestate.move_robot(i, gamestate.base_station_start_dirs[i])
    entry_point = robot.position

    start_point = robot.position
    next_point = find_good_endpoint(gamestate, station, robot.position, robot.fuel, robot.fluid)

    while next_point is not None:
        score, path = max_path(gamestate, start_point, next_point)

        for point in path:
            gamestate.move_robot_pos(i, point)

        start_point = next_point
        next_point = find_good_endpoint(gamestate, station, start_point, robot.fuel)
    
    # Go back from last point to entry point (from station)
    score, path = max_path(start_point, entry_point)

    for point in path:
        gamestate.move_robot_pos(i, point)
    # Move robot back to station
    gamestate.move_robot_pos(i, station)

def max_path(state, a, b):
    def getdp(row, col):
        return dp[row - rowoff][col - coloff]

    def max_path_helper(row, col):
        if not state.in_board_coord(row, col):
            return 0
        if getdp(row, col)[0] != -1:
            return getdp(row, col)[0]
        if b[0] == row and b[1] == col:
            return state.tiles[row][col]
        v = max_path_helper(row + verticalmove, col)
        h = max_path_helper(row, col + sidemove)
        if v >= h:
            dp[row - rowoff][col - coloff] = (v + state.tiles[row][col], [row + verticalmove, col])
        else:
            dp[row - rowoff][col - coloff] = (h + state.tiles[row][col], [row, col + sidemove])
        return getdp(row, col)[0]

    verticalmove = 1 if b[0] > a[0] else -1
    sidemove = 1 if b[1] > a[1] else -1
    dp = [[(-1, []) for _ in range(abs(b[1] - a[1] + 1))] for _ in range(abs(b[0] - a[0] + 1))]
    print(dp)
    coloff = min(b[1], a[1])
    rowoff = min(b[0], a[0])
    max_path_helper(a[0], a[1])

    point = a
    path = []
    while point != b:
        path.append(getdp(point[0], point[1])[1])
        point = path[-1]

    return (getdp(a[0], a[1]), path)

