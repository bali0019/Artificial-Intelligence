import sys

assignments = []

# Defining util class here to be used by this file, since doing "udacity submit" did not pack a different file with zip. Suggestions?
class SolutionUtil:
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = None
    row_units = None
    column_units = None
    square_units = None
    diagonal_units = None
    unitlist = None
    units = None
    peers = None

    def __init__(self):
        def cross(A, B):
            "Cross product of elements in A and elements in B."
            return [k + l for k in A for l in B]

        self.boxes = cross(self.rows, self.cols)
        self.row_units = [cross(r, self.cols) for r in self.rows]
        self.column_units = [cross(self.rows, c) for c in self.cols]
        self.square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
        self.diagonal_units = [["A1", "B2", "C3", "D4", "E5", "F6", "G7", "H8", "I9"],
                          ["A9", "B8", "C7", "D6", "E5", "F4", "G3", "H2", "I1"]]
        self.unitlist = self.row_units + self.column_units + self.square_units + self.diagonal_units
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.boxes)
        self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.boxes)

def getUtil():
    solution_util = SolutionUtil()
    return solution_util

solution_util = getUtil()

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def find_naked_twins_by_unit(values, unit):
    """Given a unit, find its naked twins.
    Args:
        values(dict): the puzzle as a dictionary
        unit: a unit to be searched for naked twins

    Returns:
        a dictionary of naked twins in the format {"27":[A1,A5]}
    """
    naked_twins_dict = dict()
    for box in unit:
        l = []
        if len(values[box]) > 1:
            if values[box] in naked_twins_dict:
                l.append(naked_twins_dict[values[box]])
            l.append(box)
            naked_twins_dict[values[box]] = l
    return naked_twins_dict

def eliminate_with_naked_twins_by_unit(values, naked_twins_dict, unit):
    """Given a unit and its naked twins, this function applies elimination on other boxes within a given unit 
    Args:
        values(dict): the puzzle as a dictionary
        naked_twins_dict: a dictionary of naked twins in the format {"27":[A1,A5]}
        unit: a unit to be searched for naked twins

    Returns:
        a reduced puzzle
    """
    if len(naked_twins_dict) > 1:
        for a, b in naked_twins_dict.items():
            if len(b) == 2 and len(a) == 2:
                for box in unit:
                    if not values[box] == a:
                        if len(values[box]) >= len(a):
                            for c in a:
                                values[box] = str(values[box]).replace(c, '')

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    has_naked_twins = True

    while has_naked_twins:
        old_values = values.copy()
        for unit in solution_util.unitlist:
            # Find all instances of naked twins
            naked_twins_dict = find_naked_twins_by_unit(values, unit)
            # Eliminate the naked twins as possibilities for their peers
            eliminate_with_naked_twins_by_unit(values, naked_twins_dict, unit)
        if old_values == values:
            break

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    new_dict = dict()
    digits_seq = '123456789'
    for i,v in enumerate(grid):
        if v == '.':
            new_dict[solution_util.boxes[i]] = digits_seq
            continue
        new_dict[solution_util.boxes[i]] = v
    return new_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in solution_util.boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in solution_util.rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in solution_util.cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        a puzzle dictionary after applying elimation round to it, wherein it replaces a solved box for all its other peers.
    """
    for key, value in values.items():
        if len(value) == 1:
            boxPeers = solution_util.peers[key]
            for k in boxPeers:
                s = values[k]
                values[k] = str(s).replace(value, '')
    return values

def only_choice(values):
    """Apply only-choice strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        a puzzle dictionary after applying only-choice strategy.
    """

    digits = '123456789'
    for unit in solution_util.unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """Repeatedly applies elimination, only-choice and naked-twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        a reduced puzzle dictionary after applying only-choice strategy.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Further pruning search space by using naked twins reduction
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    #"Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    result = reduce_puzzle(values)

    # Choose one of the unfilled squares with the fewest possibilities
    noDigitsPerBox = filterPuzzleToBoxDigitsSize(values)

    if result is False:
        return False

    if is_solved(noDigitsPerBox):
        return values

    box = min(noDigitsPerBox, key = noDigitsPerBox.get)

    for digit in values[box]:
        new_values = values.copy()
        new_values[box] = digit
        solved = search(new_values)
        if solved:
            return solved

def filterPuzzleToBoxDigitsSize(values):
    noDigitsPerBox = dict()
    for key,value in values.items():
        if len(value) > 1:
            noDigitsPerBox[key] = len(value)
    return noDigitsPerBox

def is_solved(valuesBoxSize):
    solved = [box for box,vbox in valuesBoxSize.items() if (valuesBoxSize[box] > 1 or valuesBoxSize[box] == 0)]
    if len(solved) == 0:
        return True
    else:
        return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = search(grid_values(grid))
    return values

# if __name__ == '__main__':
#     diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
#     display(solve(diag_sudoku_grid))
#
#     try:
#         from visualize import visualize_assignments
#         visualize_assignments(assignments)
#
#     except SystemExit:
#         pass
#     except:
#         print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

# display(solve("9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................"))
# for s in units: