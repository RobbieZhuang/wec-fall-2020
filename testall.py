from glob import glob
import json

from robots import find_optimal_robots
from WEC2020.src import problem, scoring
from greedy import greedy_trip
from optimal import optimal_trip

cases = sorted(glob('WEC2020/test_cases/case*.txt'))

strat = optimal_trip

total_score = 0
for c in cases:
    p = problem.load_problem(c)
    solution = json.loads(find_optimal_robots(p.max_fluid, p.max_fuel, p.floor, max_robots=8, trip_strategy=strat)[1])
    solution = problem.Solution(solution['robots'], solution['actions'])

    score = 10 * scoring.evaluate(p, solution)
    total_score += score
    print(f'Score for {c}: {score}')

print(f'Overall score: {total_score}')
