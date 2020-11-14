from util import *
from copy import deepcopy

def execute_greedy(gs):
    while True:
        # first try to clean tiles
        for i, robot in enumerate(gs.robots):
            if gs.in_board(i) and gs.tiles[robot.position] > 0:
                gs.clean_tile(i, gs.tiles[robot.position])

        possible_moves = []

        for i, robot in enumerate(gs.robots):
            for d in directions:
                g = deepcopy(gs)
                g.move_robot(i, d)

                # only consider moves that are in range of base and which will allow us to clean more stuff
                # or are moving back towards base
                if g.in_range_of_base(i) and (robot.fluid > 0 or g.dist_from_base(i) < gs.dist_from_base(i)):
                    priority = 0
                    if (robot.fluid == 0 or gs.contamination == 0) and g.dist_from_base(i) < gs.dist_from_base(i):
                        priority = 1000     # prioritize getting empty robots back to base
                    else:
                        priority = min(robot.fluid, g.tiles[g.robots[i].position])

                    possible_moves.append((priority, g))

        if not possible_moves:
            break
        possible_moves.sort(key=lambda a: a[0])

        # overwrite game state with best move
        gs = possible_moves[0][1]

        gs.print_state()

    return gs
