from util import *
from copy import deepcopy
from time import sleep

def greedy_trip(i, gs):
    started = False
    while not started or gs.dist_from_base(i) != 0:
        started = True

        robot = gs.robots[i]
        # first try to clean tiles
        if gs.in_board(i) and gs.tiles[robot.position] > 0:
            gs.clean_tile(i, gs.tiles[robot.position])

        possible_moves = []

        for d in directions:
            g = deepcopy(gs)
            if not g.move_robot(i, d):
                continue

            robot = g.robots[i]

            # only consider moves that are in range of base and which will allow us to clean more stuff
            # or are moving back towards base
            if g.valid_position(i) and \
               g.in_range_of_base(i) and \
               (robot.fluid > 0 or g.dist_from_base(i) < gs.dist_from_base(i)):

                priority = 0
                if (robot.fluid == 0 or gs.contamination == 0) and g.dist_from_base(i) < gs.dist_from_base(i):
                    priority = 1000     # prioritize getting empty robots back to base
                elif g.in_board(i):
                    priority = min(robot.fluid, g.tiles[robot.position])

                possible_moves.append((priority, g))

        if not possible_moves:
            break
        possible_moves.sort(key=lambda a: a[0], reverse=True)

        # overwrite game state with best move
        gs = possible_moves[0][1]

    gs.resupply(i)

    return gs
