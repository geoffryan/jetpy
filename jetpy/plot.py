import math
import numpy as np
import matplotlib.pyplot as plt

def plotPolar(ax, grid, f, includeOrigin=False, colorbar=True):

    k = 0
    for j in range(grid.Nt):
        riph = grid.riph[j][k]
        ta = grid.tjph[j]
        tb = grid.tjph[j+1]
        nr = grid.Nr[j,k]

        a = grid.index[j,k]
        b = grid.index[j,k] + nr

        if includeOrigin:
            fray = np.atleast_2d(f[a:b])
            rf = riph[:]
            X = np.empty((2, nr+1))
            Y = np.empty((2, nr+1))
        else:
            fray = np.atleast_2d(f[a+1:b])
            rf = riph[1:]
            X = np.empty((2, nr))
            Y = np.empty((2, nr))

        X[0,:] = rf*math.cos(ta)
        X[1,:] = rf*math.cos(tb)
        Y[0,:] = rf*math.sin(ta)
        Y[1,:] = rf*math.sin(tb)

        ax.pcolormesh(X, Y, fray)

