# Sudoku CSP Solver

## Description
This repository contains a Python implementation of a CSP-based Sudoku solver that uses backtracking search, forward checking, and the AC-3 algorithm to solve puzzles of varying difficulty. It was developed as part of an Artificial Intelligence course assignment.

## Files Included
* `sudoku_solver.py`: The main source code for the CSP solver.
* `easy.txt`, `medium.txt`, `hard.txt`, `veryhard.txt`: Text files containing the test Sudoku boards.

## Input Format
The solver reads Sudoku boards from text files with the following strict format requirements:
* The file contains exactly 9 lines.
* Each line contains exactly 9 digits (0-9).
* The digit `0` represents an empty cell on the board.

**Example Input:**
004030050
609400000
005100489
000060930
300807002
026040000
453009600
000004705
090050200

## How to Run
Ensure you have Python installed on your system. You can run the solver from your terminal or command prompt using the following command:

python sudoku_solver.py

*(Note: Depending on how your code is set up to receive the input files, you may need to pass the file name as an argument, e.g., `python sudoku_solver.py easy.txt`)*
