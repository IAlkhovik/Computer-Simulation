import numpy as np
import matplotlib.pyplot as plt

#show_grid is imported from the cellular automata demo
DEF_CMAP = 'binary'
def show_grid(grid, vertical=True, **args):
    if 'cmap' not in args:
        args['cmap'] = DEF_CMAP
    if vertical:
        plt.matshow(grid.T, **args)
        plt.xlabel('position, $n$')
        plt.ylabel('time, $t$', rotation=0, horizontalalignment='right')
    else:
        plt.matshow(grid, **args)
        plt.ylabel('position, $n$', rotation=0, horizontalalignment='right')
        plt.xlabel('time, $t$')

#sets up the grid 100 (position) x 120 (time)
N = 100
T = 120
X = np.zeros((N, T), dtype=int)

#this initializes the grid by setting half the cells to 46 to 1 (-5km to -.3) and then all the cells from 47 to 50 (-.3 to 0)
#this gives a density of 80(out of 160) in the first setup and 160(out of 160) in the other
def initializeGrid():
    indices = np.random.choice(47, size=23, replace=False)
    X[indices, 0] = 1
    X[48:51, 0] = 1

#this is the simulation which calls the stepper
def simulate(time):
    for t in range(time-1):
        stepper(t)

#this is the stepper which for each row, looks at previous row, increments the speed (capped at 5), and then moves all cars by the speed
speed = 1
def stepper(t):
    row = X[:, t]
    mask = row > 0 
    next_row = X[:, t+1]
    next_row[mask] = row[mask] + 1
    X[X>5] = 5
    if t < 5:
        X[:, t+1] = np.roll(X[:, t+1], t)
    else:
        X[:, t+1] = np.roll(X[:, t+1], 5)

initializeGrid()
simulate(120)
show_grid(X)
plt.show()