import sys
import json

from WEC2020.src.problem import load_problem

def generate_solution(fluid, fuel, tiles):
    return json.dumps({'a': 'b'})

if __name__=='__main__':
    problem = load_problem(sys.argv[1])

    json = generate_solution(problem.max_fluid, problem.max_fuel, problem.floor)

    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w') as ofile:
            ofile.write(json)
    else:
        print(json)
