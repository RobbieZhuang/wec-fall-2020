import argparse

from src import problem, visualization

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate visualization frames for a solution')
    parser.add_argument('-p', '--problem',
        type=str, help='Path to the test case', required=True)
    parser.add_argument('-s', '--solution',
        type=str, help='Path to the solution file', required=True)
    parser.add_argument('-o', '--output_dir',
        type=str, help='Path to the output directory', required=True)
    parser.add_argument('-v', '--video_name',
        type=str, help='Filename for the new video', required=True)
    parser.add_argument('-f', '--fps',
        type=str, help='Video fps', required=True)

    args = parser.parse_args()

    prob = problem.load_problem(args.problem)
    soln = problem.load_solution(args.solution)

    visualization.visualize_everything_video(prob, soln, args.output_dir, args.video_name, args.fps)
