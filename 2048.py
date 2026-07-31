import random
import sys


def draw_grid(grid):
    """
    Given the current grid, prints the grid out to the terminal, using ASCII to draw tiles.
    """
    square = {0: "┌─────────┐ ",
              1: "│         │ ",
              2: "│   ",
              3: "│         │ ",
              4: "└─────────┘ "}
    squareFilling = {0: "      │ ",
                     2: " 2    │ ",
                     4: " 4    │ ",
                     8: " 8    │ ",
                     16: " 16   │ ",
                     32: " 32   │ ",
                     64: " 64   │ ",
                     128: "128   │ ",
                     256: "256   │ ",
                     512: "512   │ ",
                     1024: "1024  │ ",
                     2048: "2048  │ "}

    for row in grid:
        for i in range(0, 5):
            toPrint = ""
            for tile in row:
                if i == 2:

                    toPrint += square[2] + squareFilling[tile]
                else:
                    toPrint += square[i]
            print(toPrint)

    pass


def get_empty_spaces(grid):
    """
    Returns a list of coordinates of empty tiles in the grid.
    """

    emptySpaces = []
    x = 0
    for row in grid:
        y = 0
        for tile in row:
            if tile == 0:
                emptySpaces.append([x, y])
            y += 1
        x += 1

    return emptySpaces


def spawn_tile(grid):
    """
    Creates a tile in a random unoccupied space on the grid.

    There is a 10% chance that a '4' is created, and a 90% chance that a '2' is created. 
    """

    empty = get_empty_spaces(grid)

    location = empty[random.randint(0, len(empty)-1)]
    if random.randint(0, 9) == 0:
        toSpawn = 4
    else:
        toSpawn = 2

    grid[location[0]][location[1]] = toSpawn
    pass


def rotate_grid(toRotate, turns):
    """ Given a grid and a number of turns (each turn 90 degrees clockwise), returns a rotated grid"""
    tempGrid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    if turns == 0:
        return toRotate

    y = 0
    for row in toRotate:
        x = 0
        for tile in row:
            tempGrid[x][3-y] = tile
            x += 1
        y += 1
    rotated = tempGrid
    rotated = rotate_grid(rotated, turns - 1)

    return rotated


def move(grid, direction):
    """
    Returns a grid, given a grid and a direction, moves every tile in the grid as many spaces as possible until they 
    collide with a wall or another tile.

    Returns True if any movement was successfully made, False if not.

    If a tile collides with another tile with the same value, they merge together to form a higher value tile, creating 
    more space on the grid. (E.g. 4 merges with 4 to create an '8' tile. )

    If a '2048' tile is created, the game ends and the player is victorious.

    If no tiles are able to move in the specified direction (for example, the only existing tiles are against the wall)
    then that move is invalid and nothing happens.

    """

    topBlank = [4, 4, 4, 4]
    moved = False
    victory = False

    # The directions rotate the grid, then the grid will shift upwards, then the grid will be rotated back.
    # e.g a 'right' shift of the grid is created by rotating the grid 270 degrees clockwise, shifting everything
    # up, and then rotating the grid to its original position. A direction of up thus requires no rotation.
    # rotatedGrid = rotateGrid(grid, 1)

    rotatedGrid = rotate_grid(grid, direction)
    y = 0
    for row in rotatedGrid:
        x = 0
        for tile in row:
            if tile == 0:
                if y < topBlank[x]:
                    topBlank[x] = y

            elif topBlank[x] < y:
                moved = True

                # check if there is a merge to be made
                if not topBlank[x] == 0:
                    if tile == rotatedGrid[topBlank[x]-1][x]:
                        rotatedGrid[topBlank[x]-1][x] *= 2
                        if tile == 1024:
                            victory = True

                    else:
                        rotatedGrid[topBlank[x]][x] = tile
                        topBlank[x] += 1

                else:
                    rotatedGrid[topBlank[x]][x] = tile
                    topBlank[x] += 1
                rotatedGrid[y][x] = 0

            elif (y > 0) & (tile == rotatedGrid[y-1][x]):
                rotatedGrid[y-1][x] *= 2
                if tile == 1024:
                    victory = True
                rotatedGrid[y][x] = 0
                topBlank[x] = y
                moved = True

            x += 1
        y += 1

    if direction == 0:
        grid = rotatedGrid
    else:
        grid = rotate_grid(rotatedGrid, 4 - direction)

    return (grid, moved, victory)


def check_game_over(grid):
    """
    Return True if the game is over.

    The game is over if no move can be made. No move can be made if the grid is full and no two adjacent tiles are 
    equal value.
    """
    pair = False
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if x < 3:
                if grid[y][x+1] == tile:
                    pair = True
                    break
            if y < 3:
                if grid[y+1][x] == tile:
                    pair = True
                    break
        if pair == True:
            break
    return not pair


def play_turn(grid):
    """
    Allows the player to play a turn. Returns a new grid after a turn has been played. A turn starts with a new tile
    being created, followed by the user inputting a direction to shift the grid.

    If a player move is invalid - they try to move tiles in a direction they can't move, the turn is not used and 
    the player must move in a different direction. If there are no possible moves, it is game over.
    """

    spawn_tile(grid)
    print('\n'*50)
    print("WASD to move the tiles. (W - UP, A - LEFT, S - DOWN, D - RIGHT), type 'P' to exit.")
    draw_grid(grid)

    directionDict = {"w": 0, "a": 1, "s": 2, "d": 3}
    gameOver = False
    while True:

        if len(get_empty_spaces(grid)) == 0:
            if check_game_over(grid) == True:
                print("GAME OVER")
                gameOver = True

                break

        while True:
            direction = input("")
            if direction.lower() in directionDict:
                break
            elif direction.lower() == 'p':
                sys.exit()
            else:
                print("Only enter w a s or d.")

        grid, valid, victory = move(grid, directionDict[direction.lower()])
        if victory:
            gameOver = True
            print('\n'*50)
            draw_grid(grid)
            print("2048 - YOU WIN!!")
            break
        if valid:
            break
        else:
            print('\n'*50)
            print("Cannot move that way")
            print("WASD to move the tiles. (W - UP, A - LEFT, S - DOWN, D - RIGHT)")
            draw_grid(grid)

    return (grid, gameOver)


def main():

    grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    gameOver = False
    while not gameOver:
        grid, gameOver = play_turn(grid)
    print("Thanks for playing!")


main()
