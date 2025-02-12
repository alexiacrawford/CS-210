"""Flood-fill to count chambers in a cave.
CS 210 project.
Alexia Crawford, 10/30/2023
Credits: worked with Sam
"""
import doctest
import cave
import cave_view
import config

def scan_cave(cavern: list[list[str]]) -> int: #write this code
    """Scan the cave for air pockets.  Return the number of
    air pockets encountered.

    >>> cavern_1 = cave.read_cave("data/tiny-cave.txt")
    >>> scan_cave(cavern_1)
    1
    >>> cavern_2 = cave.read_cave("data/cave.txt")
    >>> scan_cave(cavern_2)
    3
    """
    air_pockets = 0
    for row_i in range(len(cavern)):
        for col_i in range(len(cavern[row_i])):
            if cavern[row_i][col_i] == config.AIR:
                air_pockets += 1
                fill(cavern, row_i, col_i)
                cave_view.change_water()
    return air_pockets

def fill(cavern: list[list[str]], row_i: int, col_i: int):
    """Pour water into cell at row_i, col_i"""
   # [[7,8,9]
   # [4,5,6]
   # [1,2,3]]
    in_grid = (0 <= row_i < len (cavern))
    if in_grid and (0 <= col_i < len (cavern[row_i])) and cavern[row_i][col_i] == config.AIR:
        cavern[row_i][col_i] = config.WATER
        cave_view.fill_cell(row_i, col_i)
        fill(cavern, row_i, col_i - 1)
        fill(cavern, row_i - 1, col_i)
        fill(cavern, row_i + 1, col_i)
        fill(cavern, row_i, col_i + 1)
    else:
        return

def main():
    doctest.testmod()
    cavern = cave.read_cave(config.CAVE_PATH)
    cave_view.display(cavern,config.WIN_WIDTH, config.WIN_HEIGHT)
    chambers = scan_cave(cavern)
    print(f"Found {chambers} chambers")
    cave_view.redisplay(cavern)
    cave_view.prompt_to_close()


if __name__ == "__main__":
    main()