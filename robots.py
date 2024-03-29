#!/bin/python3

import json
import numpy as np
from copy import deepcopy

from WEC2020.src.problem import load_problem
from util import equal_space_base_stations
from oaat import one_at_a_time_strat
from greedy import greedy_trip
from optimal import optimal_trip

import argparse

strategies = {
    'greedy': [greedy_trip],
    'optimal': [optimal_trip],
    'both': [greedy_trip, optimal_trip]
}

class RobotState:
    def __init__(self, name, fluid, fuel, position):
        self.name = name
        self.fluid = fluid
        self.fuel = fuel
        self.position = position

class GameState:
    def __init__(self, fluid, fuel, tiles, base_stations):
        self.max_fluid = fluid
        self.max_fuel = fuel

        self.base_stations = [bs[0] for bs in base_stations]
        self.base_station_start_dirs = [bs[1] for bs in base_stations]
        self.actions = []
        self.tiles = tiles

        self.rows, self.cols = tiles.shape

        self.contamination = np.sum(tiles)
        self.fuel_spent = 0

        self.robots = [
            RobotState(f'Robot{i}', self.max_fluid, self.max_fuel, bs)
                for i, bs in enumerate(self.base_stations)
        ]

    def get_stranded(self):
        stranded = 0
        for r in self.robots:
            if r.position not in self.base_stations:
                stranded += 1
        return stranded

    def get_score(self, count_stranding=False):
        N_t = self.tiles.size
        if not count_stranding:
            return (20 * N_t - 0.5 * self.contamination - 2 * self.fuel_spent - 15 * len(self.robots)) / (20 * N_t)
        else:
            return (20 * N_t - 0.5 * self.contamination - 2 * self.fuel_spent - 15 * len(self.robots) - 50 * self.get_stranded()) / (20 * N_t)

    def valid_position(self, i):
        return self.in_board(i) or self.robots[i].position in self.base_stations

    def dist_from_base(self, i):
        return sum([abs(self.robots[i].position[j] - self.base_stations[i][j]) for j in range(2)])
    
    def in_range_of_base(self, i):
        return self.dist_from_base(i) <= self.robots[i].fuel

    def in_board(self, i):
        r, c = self.robots[i].position
        return self.in_board_coord(r, c)

    def in_board_coord(self, r, c):
        return r >= 0 and r < self.rows and c >= 0 and c < self.cols

    def move_robot(self, i, d):
        if self.robots[i].fuel <= 0:
            return False

        r, c = self.robots[i].position
        new_pos = (r + d[0], c + d[1])

        # avoid collision
        for j, r in enumerate(self.robots):
            if i != j and r.position == new_pos:
                return False

        self.robots[i].position = new_pos
        self.robots[i].fuel -= 1
        self.fuel_spent += 1

        self.actions.append([self.robots[i].name, 'move', self.robots[i].position])
        return True

    def move_robot_pos(self, i, p):
        d = (p[0] - self.robots[i].position[0], p[1] - self.robots[i].position[1])
        if abs(d[0]) + abs(d[1]) > 1 or abs(d[0]) + abs(d[1]) == 0:
            return False
        return self.move_robot(i, d)

    def clean_tile(self, i, amount):
        if self.tiles[self.robots[i].position] == 0:
            return

        old = self.tiles[self.robots[i].position]
        amount = min(min(amount, self.robots[i].fluid), old)

        self.tiles[self.robots[i].position] = old - amount
        self.robots[i].fluid -= amount

        self.contamination -= amount

        self.actions.append([self.robots[i].name, 'clean', amount])

    def resupply(self, i):
        if self.robots[i].position not in self.base_stations:
            return False

        self.robots[i].fluid = self.max_fluid
        self.robots[i].fuel = self.max_fuel

        self.actions.append([self.robots[i].name, 'resupply'])


    def get_json(self):
        return json.dumps({
            'robots': [[
                robot.name, self.base_stations[i]
            ] for i, robot in enumerate(self.robots)],
            'actions': self.actions
        })

    def print_state(self):
        for r in range(-1, self.rows + 1):
            for c in range(-1, self.cols + 1):
                robot = False
                for i, rob in enumerate(self.robots):
                    if rob.position == (r, c):
                        print(f'R{i}', end='')
                        robot = True
                        break
                if not robot:
                    if r >= 0 and r < self.rows and c >= 0 and c < self.cols:
                        print('%02d' % self.tiles[r][c], end='')
                    elif (r,c) in self.base_stations:
                        print('bb', end='')
                    else:
                        print('  ', end='')
                print(' ', end='')
            print()

    def get_contam(self, coord):
        return self.tiles[coord[0]][coord[1]]

def generate_solution(fluid, fuel, tiles, n_robots=5, trip_strategy=[greedy_trip, optimal_trip]):
    rows, cols = tiles.shape
    base_stations = equal_space_base_stations(tiles, n_robots)

    # remove duplicates
    base_stations = list(set(base_stations))
    if len(base_stations) < n_robots:
        return -100, '{}'       # we are oversaturated

    g = GameState(fluid, fuel, tiles, base_stations)

    g = one_at_a_time_strat(trip_strategy, g)

    return g.get_score(), g.get_json()

def find_optimal_robots(fluid, fuel, tiles, trip_strategy=[greedy_trip, optimal_trip], min_robots=1, max_robots=20):
    max_score = -1
    max_json = '{}'

    for i in range(min_robots, max_robots + 1):
        score, json = generate_solution(fluid, fuel, tiles, n_robots=i, trip_strategy=trip_strategy)
        print(f'{score}')
        if score > max_score:
            max_score = score
            max_json = json

    return max_score, max_json

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generates a solution for cleaning robot planning')
    parser.add_argument('infile', metavar='PROBLEM', type=str,
            help='text document containing the problem test case')
    parser.add_argument('-o', '--output', metavar='SOLUTION', type=str,
            help='the file to write the solution to (default: stdout)')
    parser.add_argument('-s', '--strategy', metavar='STRAT', type=str, choices=['greedy', 'optimal', 'both'], default='both',
            help='which strategy to use for trip routing')
    parser.add_argument('-m', '--min-robots', metavar='N', type=int, default=1,
            help='minimum number of robots to consider using')
    parser.add_argument('-M', '--max-robots', metavar='N', type=int, default=10,
            help='maximum number of robots to consider using')

    args = parser.parse_args()

    problem = load_problem(args.infile)

    score, json = find_optimal_robots(
            problem.max_fluid,
            problem.max_fuel,
            problem.floor,
            trip_strategy=strategies[args.strategy],
            min_robots=args.min_robots,
            max_robots=args.max_robots)

    if args.output:
        with open(args.output, 'w') as ofile:
            ofile.write(json)
            ofile.write('\n')
    else:
        print(json)
