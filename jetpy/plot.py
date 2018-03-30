import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def plotPolar(ax, grid, f, scale='linear', vmin=None, vmax=None,
                includeOrigin=False, colorbar=True, cmap=None,
                label=None, xlabel=None, ylabel=None, labelkwargs={}):

    if scale == 'log':
        norm = mpl.colors.LogNorm(vmin, vmax)
    else:
        norm = mpl.colors.Normalize(vmin, vmax)

    if cmap is None:
        try:
            cmap = mpl.cm.inferno
        except:
            cmap = mpl.cm.afmhot

    if vmin is None:
        vmin = f.min()
    if vmax is None:
        vmax = f.max()

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

        C = ax.pcolormesh(X, Y, fray, cmap=cmap, vmin=vmin, vmax=vmax,
                                        norm=norm)

    if colorbar:
        cb = (ax.get_figure()).colorbar(C)
        if label is not None:
            cb.set_label(label, **labelkwargs)
    ax.set_aspect('equal')

    if xlabel is not None:
        ax.set_xlabel(xlabel, **labelkwargs)
    if ylabel is not None:
        ax.set_ylabel(ylabel, **labelkwargs)



