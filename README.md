# Artificial Intelligence Agent - Diagonal Sudoku Solver


```Description```<br>
Applies constraint propagation, elimination, only choice, naked twins strategies to prune search area and then applies depth-wise search to find a possible solution for a diagonal sudoku.



# Naked Twins
Uses constraint propagation as a "mapreduce" for this soduku puzzle to repeatedly apply elimination
and only choice functions to an incomplete  soduku puzzle. For diagonal soduku,
naked twins problem additionally elimates naked twins' digits from all other other boxes in the diagonal unit.


# Diagonal Sudoku
Uses contraint propagation for solving diagonal sudoku problem by simply adding diagonal units to the original
superset of soduku units. For diagonal soduku problem, we add diagonal peers to all diagonal boxes, which get included
as a criteria to the constraint propagation of applying elimation and only choice functions repeatedly to the diagonal peers as well.

### Install and Usage

This project requires **Python 3**.

* `solution.py` - Algorithm that solves n by n diagonal soduku puzzle
* `solution_test.py` - Unit tests suite for solution.py, also demonstrates usage of solution.py
