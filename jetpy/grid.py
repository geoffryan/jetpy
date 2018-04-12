import h5py as h5
import numpy as np

class JetGrid:

    t = 0
    r = None
    th = None
    phi = None
    dV = None

    prim = None

    riph = None
    tjph = None
    pkph = None
    index = None
    Nr = None

    threeDee = False

    filename = None

    def __init__(self, filename=None):
        if filename is not None:
            self._loadFromCheckpoint(filename)

    @property
    def Nt(self):
        if self.tjph is not None:
            return self.tjph.shape[0]-1
        return 0
    
    @property
    def Np(self):
        if sel.pkph is not None:
            return self.pkph.shape[0]-1
        return 0

    @property
    def rho(self):
        if self.prim is not None:
            return self.prim[:,0]

    @property
    def P(self):
        if self.prim is not None:
            return self.prim[:,1]

    @property
    def ur(self):
        if self.prim is not None:
            return self.prim[:,2]

    @property
    def ut(self):
        if self.prim is not None:
            return self.prim[:,3]

    @property
    def up(self):
        if self.threeDee and self.prim is not None:
            return self.prim[:,4]

    @property
    def q(self):
        if self.prim is not None:
            if self.threeDee:
                return self.prim[:,5:].T
            else:
                return self.prim[:,4:].T

    def _loadFromCheckpoint(self, filename):
        self.filename = filename
        f = h5.File(filename, "r")
        gridG = f['Grid']
        dataG = f['Data']

        self.index = gridG['Index'][...]
        self.Nr = gridG['Nr'][...]
        self.t = gridG['T'][0]
        self.pkph = gridG['p_kph'][...]
        self.tjph = gridG['t_jph'][...]

        cells = dataG['Cells'][...]

        f.close()

        nc = cells.shape[0]
        nphi = self.pkph.shape[0] - 1
        nth = self.tjph.shape[0] - 1

        if nphi > 1:
            self.threeDee = True

        self.prim = cells[:,:-1]

        self.r = np.empty(nc)
        self.th = np.empty(nc)
        self.phi = np.empty(nc)
        self.dV = np.empty(nc)

        self.riph = []
        for j in range(nth):
            self.riph.append([])

        for k in range(nphi):
            for j in range(nth):
                a = self.index[j,k]
                b = self.index[j,k] + self.Nr[j,k]

                Riph = np.zeros(self.Nr[j,k]+1)
                Riph[1:] = cells[a:b,-1]
                self.riph[j].append(Riph.copy())

                self.r[a:b] = 0.5*(Riph[1:]+Riph[:-1])
                dr = self.r[a:b]*self.r[a:b] * (Riph[1:]-Riph[:-1])

                if nth == 1:
                    self.th[a:b] = 0.0
                    dth = 2.0
                else:
                    self.th[a:b] = 0.5*(self.tjph[j]+self.tjph[j+1])
                    dth = np.sin(self.th[a:b])*(self.tjph[j+1]-self.tjph[j])
                if nphi == 1:
                    self.phi[a:b] = 0.0
                    dphi = 2*np.pi
                else:
                    self.phi[a:b] = 0.5*(self.pkph[k]+self.pkph[k+1])
                    dphi = self.pkph[k+1]-self.pkph[k]
                    while dphi < 0.0:
                        dphi += 2*np.pi

                self.dV[a:b] = dr*dth*dphi

