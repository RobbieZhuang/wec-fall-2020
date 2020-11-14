#!/bin/bash
set -e

./robots.py WEC2020/test_cases/case$2.txt -s $1 -o solutions/case$2.out
python WEC2020/mark_solution.py -p WEC2020/test_cases/case$2.txt -s solutions/case$2.out
