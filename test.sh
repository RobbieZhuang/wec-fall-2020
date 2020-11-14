#!/bin/bash

python robots.py WEC2020/test_cases/case$1.txt solutions/case$1.out
python WEC2020/mark_solution.py -p WEC2020/test_cases/case$1.txt -s solutions/case$1.out
