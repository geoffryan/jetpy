import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def plotRRay(ax, grid, f, theta=0, phi=0, xscale='linear', yscale='linear', 
                    vmin=None, vmax=None, includeOrigin=False, xlabel=None,
                    ylabel=None, labelkwargs={}, **kwargs):

    j = 0
    k = 0
    a = grid.index[j,k]
    b = grid.index[j,k]+grid.Nr[j,k]

    if not includeOrigin:
        a += 1

    ax.plot(grid.r[a:b], f[a:b], **kwargs)

    if vmin is not None or vmax is not None:
        ax.set_ylim(vmin, vmax)
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)

    if xlabel is not None:
        ax.set_xlabel(xlabel, **labelkwargs)
    if ylabel is not None:
        ax.set_ylabel(xlabel, **labelkwargs)

def plotRAll(ax, grid, f, scale='linear', vmin=None,
                    vmax=None, includeOrigin=False, xlabel=None, ylabel=None,
                    labelkwargs={}, **kwargs):

    ax.plot(grid.r, f, *args, **kwargs)

    ax.set_ylim(vmin, vmax)
    ax.set_xscale(scale)
    ax.set_yscale(scale)

    if xlabel is not None:
        ax.set_xlabel(xlabel, **labelkwargs)
    if ylabel is not None:
        ax.set_ylabel(xlabel, **labelkwargs)


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



