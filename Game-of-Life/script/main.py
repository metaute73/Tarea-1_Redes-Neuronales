#!/usr/bin/env python3

import time
import os
import random
import sys
import numpy as np
from scipy import ndimage
import cv2

k = np.array([[1,1,1],[1,0,1],[1,1,1]]) # kernel matrix to get the number of neighbors of each cell

def clear_console():
    """
    Clears the console using a system command based on the user's operating system.

    """

    if sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('linux'):
        os.system("clear")
    elif sys.platform.startswith('darwin'):
        os.system("clear")
    else:
        print("Unable to clear terminal. Your operating system is not supported.\n\r")


def resize_console(rows, cols):
    """
    Re-sizes the console to the size of rows x columns

    :param rows: Int - The number of rows for the console to re-size to
    :param cols: Int - The number of columns for the console to re-size to
    """

    if cols < 32:
        cols = 32

    if sys.platform.startswith('win'):
        command = "mode con: cols={0} lines={1}".format(cols + cols, rows + 5)
        os.system(command)
    elif sys.platform.startswith('linux'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
        sys.stdout.write(command)
    elif sys.platform.startswith('darwin'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
        sys.stdout.write(command)
    else:
        print("Unable to resize terminal. Your operating system is not supported.\n\r")


def create_initial_grid(rows, cols):
    """
    Creates a random list of lists that contains 1s and 0s to represent the cells in Conway's Game of Life.

    :param rows: Int - The number of rows that the Game of Life grid will have
    :param cols: Int - The number of columns that the Game of Life grid will have
    :return: Int[][] - A list of lists containing 1s for live cells and 0s for dead cells
    """

    grid = []
    for row in range(rows):
        grid_rows = []
        for col in range(cols):
            # Generate a random number and based on that decide whether to add a live or dead cell to the grid
            if random.randint(0, 7) == 0:
                grid_rows += [1]
            else:
                grid_rows += [0]
        grid += [grid_rows]
    return grid


def print_grid(rows, cols, grid, generation):
    """
    Prints to console the Game of Life grid

    :param rows: Int - The number of rows that the Game of Life grid has
    :param cols: Int - The number of columns that the Game of Life grid has
    :param grid: Int[][] - The list of lists that will be used to represent the Game of Life grid
    :param generation: Int - The current generation of the Game of Life grid
    """

    clear_console()

    # A single output string is used to help reduce the flickering caused by printing multiple lines
    output_str = ""

    # Compile the output string together and then print it to console
    output_str += "Generation {0} - To exit the program press <Ctrl-C>\n\r".format(generation)
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                output_str += ". "
            else:
                output_str += "@ "
        output_str += "\n\r"
    #print(grid)
    print(output_str, end=" ")


def create_next_grid(rows, cols, grid, next_grid):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live and die in the next
    generation of the Game of Life grid.

    :param rows: Int - The number of rows that the Game of Life grid has
    :param cols: Int - The number of columns that the Game of Life grid has
    :param grid: Int[][] - The list of lists that will be used to represent the current generation Game of Life grid
    :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Game of Life
    grid

    """
    '''
    We use the convolve function from the scipy library to calculate the number of live neighbors
    for each cell in the grid.
    '''
    live_neighbors = ndimage.convolve(grid, k, mode='constant', cval=0.0) 
    
    for row in range(rows):
        for col in range(cols):
            # Get the number of live cells adjacent to the cell at grid[row][col]
            #live_neighbors = get_live_neighbors(row, col, rows, cols, grid)

            # If the number of surrounding live cells is < 2 or > 3 then we make the cell at grid[row][col] a dead cell
            '''
            Remember that the number of live neighbors is now a matrix with the same dimensions as the grid, 
            to get the number of neighbors of a cell we just need to access the value of the matrix at each position.
            '''
            if live_neighbors[row][col] < 2 or live_neighbors[row][col] > 3:
                next_grid[row][col] = 0
                
            # If the number of surrounding live cells is 3 and the cell at grid[row][col] was previously dead then make
            # the cell into a live cell
            elif live_neighbors[row][col] == 3 and grid[row][col] == 0:
                next_grid[row][col] = 1
            # If the number of surrounding live cells is 3 and the cell at grid[row][col] is alive keep it alive
            else:
                next_grid[row][col] = grid[row][col]


def grid_changing(rows, cols, grid, next_grid):
    """
    Checks to see if the current generation Game of Life grid is the same as the next generation Game of Life grid.

    :param rows: Int - The number of rows that the Game of Life grid has
    :param cols: Int - The number of columns that the Game of Life grid has
    :param grid: Int[][] - The list of lists that will be used to represent the current generation Game of Life grid
    :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Game of Life
    grid
    :return: Boolean - Whether the current generation grid is the same as the next generation grid
    """

    for row in range(rows):
        for col in range(cols):
            # If the cell at grid[row][col] is not equal to next_grid[row][col]
            if not grid[row][col] == next_grid[row][col]:
                return True
    return False


def get_integer_value(prompt, low, high):
    """
    Asks the user for integer input and between given bounds low and high.

    :param prompt: String - The string to prompt the user for input with
    :param low: Int - The low bound that the user must stay within
    :param high: Int - The high bound that the user must stay within
    :return: The valid input value that the user entered
    """

    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Input was not a valid integer value.")
            continue
        if value < low or value > high:
            print("Input was not inside the bounds (value <= {0} or value >= {1}).".format(low, high))
        else:
            break
    return value


def run_game():
    """
    Asks the user for input to setup the Game of Life to run for a given number of generations.

    """

    clear_console()

    # Get the number of rows and columns for the Game of Life grid
    rows = get_integer_value("Enter the number of rows (10-60): ", 10, 60)
    clear_console()
    cols = get_integer_value("Enter the number of cols (10-118): ", 10, 118)
    # Get the name of the image that will be used to create the initial grid
    image = input("Enter the name of the image: ")
    # Get the number of generations that the Game of Life should run for
    generations = 5000
    resize_console(rows, cols)

    # Create the initial random Game of Life grids 
    image_path1 = 'script\el juego de la vida.png'
    image_path2 = 'script\heart p.png' 

    if image == "vida":
        image_path = image_path1
    else:
        image_path = image_path2
    image = cv2.imread(image_path)
    #show the original image
    cv2.imshow('El juego de la vida', image)
    cv2.waitKey(0) # to avoid the console from crashing down
    #convert the image to grayscale to delete the extra color channels
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # resize the image to the desired dimensions
    new_size = (rows, cols) 
    image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA) 

    # to turn the grayscale image into a binary image of zeros and ones we use the threshold function
    # Any pixel value above 127 will be turned into 255 (white) and any pixel value below 127 will be turned into 0 (black)
    _, image_binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    
    image_array = image_binary // 255
    image_array = -image_array + 1
    current_generation = image_array
    next_generation = create_initial_grid(rows, cols)

    # Run Game of Life sequence
    gen = 1
    for gen in range(1, generations + 1):
        if not grid_changing(rows, cols, current_generation, next_generation):
            break
        print_grid(rows, cols, current_generation, gen)
        create_next_grid(rows, cols, current_generation, next_generation)
        time.sleep(1/5.0)
        current_generation, next_generation = next_generation, current_generation

    print_grid(rows, cols, current_generation, gen)
    return input("<Enter> to exit or r to run again: ")


# Start the Game of Life
run = "r"
while run == "r":
    out = run_game()
    run = out
