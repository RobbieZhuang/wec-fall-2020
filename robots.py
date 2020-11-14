import sys
import json
import numpy as np
from copy import deepcopy

from WEC2020.src.problem import load_problem

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

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

        self.base_stations = base_stations
        self.actions = []
        self.tiles = tiles

        self.contamination = np.sum(tiles)
        self.fuel_spent = 0

        self.robots = [
            RobotState(f'Robot{i}', self.max_fluid, self.max_fuel, bs)
                for i, bs in enumerate(base_stations)
        ]

    def get_score(self):
        N_t = self.tiles.size
        return (20 * N_t - 0.5 * self.contamination - 2 * self.fuel_spent - 15 * len(self.robots)) / (20 * N_t)

    def move_robot(self, i, d):
        r, c = self.robots[i].position
        self.robots[i].position = (r + d[0], c + d[1])
        self.robots[i].fuel -= 1
        self.fuel_spent += 1

        if self.robots[i].position in self.base_stations:
            self.robots[i].fluid = self.max_fluid
            self.robots[i].fuel = self.max_fuel

        self.actions.append([self.robots[i].name, 'move', self.robots[i].position])

    def clean_tile(self, i, amount):
        old = self.tiles[self.robots[i]]
        new = max(0, old - amount)
        self.tiles[self.robots[i]] = new

        self.actions.append([self.robots[i].name, 'clean', new - old])

def generate_solution(fluid, fuel, tiles, n_robots):
    base_stations = equal_space_base_stations(tiles, n_robots)

    g = GameState()

    return json.dumps({})

def cleaning_path(start, end, tiles):
    pass

def equal_space_base_stations(tiles, n):
    total_len = border_len(tiles)

    placed = 0

    for i, pos in enumerate(border_gen(tiles)):
        if i / total_len >= placed / n:
            placed += 1

def border_len(tiles):
    rows, cols = tiles.shape
    return rows * 2 + cols * 2

def border_gen(tiles):
    rows, cols = tiles.shape
    for i in range(cols):
        yield (-1, i)
    for i in range(rows):
        yield (i, cols)
    for i in range(cols):
        yield (rows, cols - i - 1)
    for i in range(rows):
        yield (rows - i - 1, -1)

if __name__=='__main__':
    problem = load_problem(sys.argv[1])

    json = generate_solution(problem.max_fluid, problem.max_fuel, problem.floor)

    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w') as ofile:
            ofile.write(json)
    else:
        print(json)
