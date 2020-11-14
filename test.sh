#!/bin/bash
set -e

python robots.py WEC2020/test_cases/case$2.txt -s $1 -o solutions/case$2.out
mkdir -p visualizations/case$2
rm -f visualizations/case$2/*
# python WEC2020/visualize_solution.py -p WEC2020/test_cases/case$2.txt -s solutions/case$2.out -o visualizations/case$2
python WEC2020/mark_solution.py -p WEC2020/test_cases/case$2.txt -s solutions/case$2.out
