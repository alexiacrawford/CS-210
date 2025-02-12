"""Boggler:  Boggle game solver. CS 210, Fall 2022.
Alexia Crawford
Credits: Worked with Sam
"""
import doctest
import config
import sys
import board_view

def test_it():
    """A little extra work to keep text display from
    interfering with doctests.
    """
    saved_flag = config.TEXT_VIEW
    config.TEXT_VIEW = False
    doctest.testmod(verbose=True)
    config.TEXT_VIEW = saved_flag


""""Configuration of Boggle player"""
# List of words to search for
DICT_PATH = "data/dict.txt"


def read_dict(path: str) -> list[str]:
    """Returns ordered list of valid, normalized words from dictionary.
    >>> read_dict("data/shortdict.txt")
    ['ALPHA', 'BED', 'BETA', 'DELTA', 'GAMMA', 'OMEGA']
    """
    word_list = []
    with open(path, 'r') as file:
        for line in file:
            line = normalize(line)
            word = line.strip()
            if allowed(word):
                word_list.append(word)
    word_list.sort()
    return word_list


def allowed(s: str) -> bool:
    """Is s a legal Boggle word?
    >>> allowed("am")  ## Too short
    False
    >>> allowed("de novo")  ## Non-alphabetic
    False
    >>> allowed("about-face")  ## Non-alphabetic
    False
    """
    from config import MIN_WORD
    if s.isalpha() and len(s) >= MIN_WORD:
        return True
    return False


def normalize(s: str) -> str:
    """Canonical for strings in dictionary or on board
    >>> normalize("filter")
    'FILTER'
    """
    return s.upper()


NOPE = "Nope"  # Not a match, nor a prefix of a match
MATCH = "Match"  # Exact match to a valid word
PREFIX = "Prefix"  # Not an exact match, but a prefix (keep searching!)


def search(candidate: str, word_list: list[str]) -> str:
    """Determine whether candidate is a MATCH, a PREFIX of a match, or a big NOPE
    Note word list MUST be in sorted order.
    >>> search("ALPHA", ['ALPHA', 'BETA', 'GAMMA']) == MATCH
    True
    >>> search("BE", ['ALPHA', 'BETA', 'GAMMA']) == PREFIX
    True
    >>> search("FOX", ['ALPHA', 'BETA', 'GAMMA']) == NOPE
    True
    >>> search("ZZZZ", ['ALPHA', 'BETA', 'GAMMA']) == NOPE
    True
    """
    low = 0
    high = len(word_list) - 1
    while low <= high:
        mid = (low + high) // 2
        word = word_list[mid]
        if candidate == word:
            return MATCH
        elif word < candidate:
            low = mid + 1
        elif word > candidate:
            high = mid - 1
        # else:
        #     high = mid - 1
    if low < len(word_list) and word_list[low].startswith(candidate):
        return PREFIX
    return NOPE


# Board dimensions
N_ROWS = 4
N_COLS = N_ROWS
BOARD_SIZE = N_ROWS * N_COLS


def get_board_letters() -> str:
    while True:
        board_string = input("Boggle board letters (or 'return' to exit)> ")
        if allowed(board_string) and len(board_string) == config.BOARD_SIZE:
            return normalize(board_string)
        elif len(board_string) == 0:
            print(f"OK, sorry it didn't work out")
            sys.exit(0)
        else:
            print(f'"{board_string}" is not a valid Boggle board')
            print(f'Please enter exactly {config.BOARD_SIZE} letters (or empty to quit)')
    return normalize(board_string)


def unpack_board(letters: str, rows=config.N_ROWS) -> list[list[str]]:
    """Unpack a single string of characters into
    a square matrix of individual characters, N_ROWS x N_ROWS.
    >>> unpack_board("abcdefghi", rows=3)
    [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']]
    >>> unpack_board("abcdefghijklmnop", rows=4)
    [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l'], ['m', 'n', 'o', 'p']]
    """
    board = []
    letter_index = 0
    for _ in range(rows):
        row = []
        for _ in range(rows):
            row.append(letters[letter_index])
            letter_index += 1
        board.append(row)
    return board


def boggle_solve(board: list[list[str]], words: list[str]) -> list[str]:
    """Find all the words that can be made by traversing
    the Boggle board in all 8 directions. Returns a sorted list without duplicates.
    >>> board = unpack_board("PLXXMEXXXAXXSXXX")
    >>> words = read_dict("data/dict.txt")
    >>> boggle_solve(board, words)
    ['AMP', 'AMPLE', 'AXE', 'AXLE', 'ELM', 'EXAM', 'LEA', 'MAX', 'PEA', 'PLEA', 'SAME', 'SAMPLE', 'SAX']
    """
    solutions = []

    def solve(row: int, col: int, prefix: str):
        """One solution step"""
        IN_USE = '@'
        if row < 0 or row >= config.N_ROWS or col < 0 or col >= config.N_COLS:
            return
        # Special character in position that is already in use
        if board[row][col] == IN_USE:
            return
        letter = board[row][col]
        prefix = prefix + letter
        status = search(prefix, words)
        if status == NOPE:
            return
        board[row][col] = IN_USE  # Mark the cell as used
        board_view.mark_occupied(row, col)
        # Further exploration goes here
        if status == MATCH:
            solutions.append(prefix)
            board_view.celebrate(prefix)
        if status == MATCH or status == PREFIX:
            for d_row in [0, -1, 1]:
                for d_col in [0, -1, 1]:
                    solve(row + d_row, col + d_col, prefix)
        # Restore
        board[row][col] = letter
        board_view.mark_unoccupied(row, col)

    # Look for solutions starting from each board position
    for row_i in range(config.N_ROWS):
        for col_i in range(config.N_COLS):
            solve(row_i, col_i, "")
    # Return solutions without duplicates, in sorted order
    solutions = list(set(solutions))
    return sorted(solutions)


# Max word length is 16, so we can just list all
# the point values.
#
#         0  1  2  3  4  5  6  7  8

POINTS = [0, 0, 0, 1, 1, 2, 3, 5, 11,
          11, 11, 11, 11, 11, 11, 11, 11]


# 9  10  11  12  13  14  15  16

def word_score(word: str) -> int:
    """Standard point value in Boggle"""
    assert len(word) <= 16
    return POINTS[len(word)]


def score(solutions: list[str]) -> int:
    """Sum of scores for each solution
    >>> score(["ALPHA", "BETA", "ABSENTMINDED"])
    14
    """
    point_counter = 0
    for word in solutions:
        point_counter += word_score(word)
    return point_counter


def main():
    words = read_dict(config.DICT_PATH)
    board_string = get_board_letters()
    board_string = normalize(board_string)
    board = unpack_board(board_string)
    board_view.display(board)
    solutions = boggle_solve(board, words)
    print(solutions)
    print(f"{score(solutions)} points")
    board_view.prompt_to_close()


if __name__ == "__main__":
    test_it()
    main()
