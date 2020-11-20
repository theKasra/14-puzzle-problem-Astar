from copy import deepcopy
from collections import deque
import time
import numpy as np

class Node:
    def __init__(self, parent, grid):
        self.parent = parent
        self.grid = grid
        self.hn = None
        self.gn = 1
        self.fn = None

def goaltest(grid):
    goal = [[1, 2, 3, 4], 
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 0]]
    if(grid == goal):
        return True
    else:
        return False

def check_grid(grid, frontier, explored):
    frontier_len = len(frontier)
    if frontier_len == 0:
        if grid not in explored:
            return True
    else:
        if grid not in explored:
            for i in range(frontier_len):
                if frontier[i].grid == grid:
                    return False
        else:
            return False
    return True

def move_left(node, coordinate, frontier, explored):
    i, j = coordinate[0], coordinate[1]
    if j == 0 or node.grid[i][j-1] == 0:
        pass
    else:
        child_grid = deepcopy(node.grid)
        child_grid[i][j], child_grid[i][j-1] = child_grid[i][j-1], child_grid[i][j]
        if check_grid(child_grid, frontier, explored):
            child = Node(node, child_grid)
            child.gn = child.parent.gn + 1
            child.hn = heuristic(child.grid)
            child.fn = child.gn + child.hn
            frontier.append(child)

def move_right(node, coordinate, frontier, explored):
    i, j = coordinate[0], coordinate[1]
    if j == 3 or node.grid[i][j+1] == 0:
        pass
    else:
        child_grid = deepcopy(node.grid)
        child_grid[i][j], child_grid[i][j+1] = child_grid[i][j+1], child_grid[i][j]
        if check_grid(child_grid, frontier, explored):
            child = Node(node, child_grid)
            child.gn = child.parent.gn + 1
            child.hn = heuristic(child.grid)
            child.fn = child.gn + child.hn
            frontier.append(child)

def move_up(node, coordinate, frontier, explored):
    i, j = coordinate[0], coordinate[1]
    if i == 0 or node.grid[i-1][j] == 0:
        pass
    else:
        child_grid = deepcopy(node.grid)
        child_grid[i][j], child_grid[i-1][j] = child_grid[i-1][j], child_grid[i][j]
        if check_grid(child_grid, frontier, explored):
            child = Node(node, child_grid)
            child.gn = child.parent.gn + 1
            child.hn = heuristic(child.grid)
            child.fn = child.gn + child.hn
            frontier.append(child)

def move_down(node, coordinate, frontier, explored):
    i, j = coordinate[0], coordinate[1]
    if i == 3 or node.grid[i+1][j] == 0:
        pass
    else:
        child_grid = deepcopy(node.grid)
        child_grid[i][j], child_grid[i+1][j] = child_grid[i+1][j], child_grid[i][j]
        if check_grid(child_grid, frontier, explored):
            child = Node(node, child_grid)
            child.gn = child.parent.gn + 1
            child.hn = heuristic(child.grid)
            child.fn = child.gn + child.hn
            frontier.append(child)

def expand(node, frontier, explored):
    first_0 = [None, None]
    second_0 = [None, None]

    found_first_0 = False
    found_all_0 = False
    for i in range(4):
        if not found_all_0:
            for j in range(4):
                if node.grid[i][j] == 0:
                    if not found_first_0:
                        first_0 = [i, j]
                        found_first_0 = True
                    else:
                        second_0 = [i, j]
                        found_all_0 = True
                        break
        else:
            break
    move_left(node, first_0, frontier, explored)
    move_left(node, second_0, frontier, explored)
    move_right(node, first_0, frontier, explored)
    move_right(node, second_0, frontier, explored)
    move_up(node, first_0, frontier, explored)
    move_up(node, second_0, frontier, explored)
    move_down(node, first_0, frontier, explored)
    move_down(node, second_0, frontier, explored)

def find_best_in_frontier(frontier):
    if len(frontier) == 1:
        return frontier.popleft()
    else:
        best_node = frontier[0]
        for i in range(len(frontier)):
            if frontier[i].fn < best_node.fn:
                best_node = frontier[i]
        frontier.remove(best_node)
        return best_node

def findxy_in_goal(number, goal):
    xy=[]
    for i in range(4):
        for j in range(4):
            if number == goal[i][j]:
                xy.append(i)
                xy.append(j)
                return xy

def heuristic(grid):
    goal = [[1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 0]]
    h2 = 0

    for i in range(4):
        for j in range(4):
            number = grid[i][j]
            if number == 0:
                continue
            gridxy = findxy_in_goal(number, goal)
            h2 += (abs(i - gridxy[0]) + abs(j - gridxy[1]))
    return h2

def print_answer(initial_grid, node):
    solution = []
    move_count = 0
    while node.parent:
        solution.insert(0, node.grid)
        node = node.parent
    print("\nStep by step solution:\n")
    print(np.matrix(initial_grid), "\n")
    for i in solution:
        print(np.matrix(i))
        move_count+=1
        print("\n")
    print("moves: ", move_count)

def A_star(frontier, explored, initial_grid):
    while frontier:
        node = find_best_in_frontier(frontier)
        if(goaltest(node.grid)):
            print_answer(initial_grid, node)
            break
        else:
            explored.append(node.grid)
            expand(node, frontier, explored)

def read_input_file(filename, grid):
    numbers = ""
    numbers_counter = 0

    f = open(filename, "r")
    numbers = f.readline().split(" ")
    f.close()

    for i in range(4):
        for j in range(4):
            grid[i][j] = int(numbers[numbers_counter])
            numbers_counter += 1
    
    return grid

grid = [[None for _ in range(4)] for _ in range(4)]
grid = read_input_file("input.txt", grid)

initial = Node(None, grid)
initial.hn = heuristic(initial.grid)
initial.gn = 0
initial.fn = initial.gn + initial.hn

frontier = deque()
frontier.append(initial)
explored = []

start_time = time.time()

A_star(frontier, explored, grid)

print("frontier: ", len(frontier))
print("explored: ", len(explored))

print("--- %s seconds ---" % (time.time() - start_time))