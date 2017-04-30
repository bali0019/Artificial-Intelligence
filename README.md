# Artificial Intelligence - Diagonal Sudoku Solve

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We use constraint propagation as a "mapreduce" for this soduku puzzle to repeatedly apply elimination
   and only choice functions to an incomplete  soduku puzzle. For diagonal soduku,
   naked twins problem additionally elimates naked twins' digits from all other other boxes in the diagonal unit.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We use contraint propagation for solving diagonal sudoku problem by simply adding diagonal units to the original
   superset of soduku units. For diagonal soduku problem, we add diagonal peers to all diagonal boxes, which get included
   as a criteria to the constraint propagation of applying elimation and only choice functions repeatedly to the diagonal peers as well.

### Install

This project requires **Python 3**.

* `solution.py` - Algorithm that solves n by n diagonal soduku puzzle
* `solution_test.py` - Unit tests suite for solution.py, also demonstrates usage of solution.py
