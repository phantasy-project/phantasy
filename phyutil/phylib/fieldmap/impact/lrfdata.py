# encoding: UTF-8

import numpy


class LRFData:
    """
    LRFData contains Linear RF data.

    Properties:
        n: Number of points
        p: Position (1D)
        f: Field (1D)
        df: Differential of Field (1D)
    """

    def __init__(self, p, f, df, copy=True):
        """
        Initialize LRFData object.

        Arguments:
            p: Position data (1D)
            f: Field (1D)
            df: Differential of Field (1D)

            copy: Make copy of data (default: True)
        """
        self.n = p.shape[0]
        if copy: 
            self.p = numpy.copy(p)
            self.f = numpy.copy(f)
            self.df = numpy.copy(df)
        else:
            self.p = p
            self.f = f
            self.df = df
        pass

    def indexAtPos(self, pos):
        for idx in xrange(self.size()):
            if pos == self.p[idx]:
                return idx
        raise Exception("Position not found in linear RF data: " + str(pos))

    def voltage(self, beta, freq, phase=0.0):
        """
        Calculate the acceleration voltage of the cavity using
        the beta, frequency and optional phase parameters.

             ⌠
        Va = ⎮ E(z)sin(2π⋅freq⋅z/(beta⋅c) + phase) dz
             ⌡

        """
        return numpy.trapz(self.f * numpy.sin(self.p * ((2.0*numpy.pi*freq)/(beta*2.998e8)) + phase), self.p)


    def ttf(self, beta, freq, phase=0.0):
        """
        Calculate the Transit Time Factor of the cavity using
        the beta, frequecy and optional phase parameters.

              ⌠
              ⎮ E(z)sin(2π⋅freq⋅z/(beta⋅c) + phase) dz
              ⌡
        TTF = ----------------------------------------
                       ⌠
                       ⎮ E(z) dz
                       ⌡

        """
        return self.voltage(beta, freq, phase) / numpy.trapz(numpy.abs(self.f), self.p)


def readFromImpactFile(file):
    """
    Read linear RF data from IMPACT data file.
    """

    p = []
    f = []
    df = []

    for line in file:
        data = line.split()
        p.append(float(data[0]))
        f.append(float(data[1]))
        df.append(float(data[2]))

    return LRFData(numpy.array(p), numpy.array(f), numpy.array(df), copy=False)


def writeToImpactFile(data, file):
    """
    Write Linear RF data in IMPACT data file format.
    """
    for idx in xrange(data.n):
        file.write("%.15f\t%.9f\t%.6f\n" % (data.p[idx], data.f[idx], data.df[idx]))


def convertFromFMData(data, posx=0.0, posy=0.0):
    """
    Convert 3D field map data to linear RF data.

    The linear RF data extends the original 3D field map data
    by mirroring the position and field about the first point.

    For example if the field map data is as follows:
        z       Ez
    ---------------
      0.0      3.5
      1.0      5.7
      2.0      6.9
      3.0      3.2

    then the linear RF data format is as follows:
        z        Ez
    ----------------
      -3.0     -3.2
      -2.0     -6.9
      -1.0     -5.7
       0.0      3.5
       1.0      5.7
       2.0      6.9
       3.0      3.2
    """
    x = data.indexAtPosX(posx)
    y = data.indexAtPosY(posy)

    n = data.nz
    p = numpy.empty((2*n)-1)
    f = numpy.empty_like(p)

    p[:n] = -1.0 * data.pz[::-1]
    p[n:] = data.pz[1:]

    f[:n] = -1.0 * numpy.real(data.fz[x,y,::-1])
    f[n:] = numpy.real(data.fz[x,y,1:])

    return LRFData(p, f, _differentiate(p,f), copy=False)


def convertFromNRFData(data, start=-1.0, end=1.0, npoints=11):
    """
    Convert nonlinear RF data to linear RF data using Inverse Fourier Transform.

    WARNING: This algorithm has not been verified to work correctly with all
             possible data sets.  For data sets which are inversely symetric
             about z=0 (ie f(z) = -f(-z)) then this algorithm will correctly
             reproduce the original data from the RF coefficents with the
             exception of the first and last points, which are zero.
    """
    pi = numpy.pi
    sin = numpy.sin
    cos = numpy.cos

    plen = end - start
    pstep = plen / (npoints-1)
    p = numpy.empty(npoints)
    f = numpy.zeros(npoints)

    for idx in xrange(npoints):
        p[idx] = start + (idx*pstep)
        for k in xrange(data.n):
            f[idx] += numpy.real(data.cf[k]) * cos(2.0*pi*k*p[idx]/plen)
            f[idx] += numpy.imag(data.cf[k]) * sin(2.0*pi*k*p[idx]/plen)

    return LRFData(p, f, _differentiate(p,f), copy=False)


def _differentiate(p,f):
    """
    Differentiate using the central difference method.
    """
    n = f.shape[0]
    d = numpy.empty_like(f)

    for z in xrange(n):
        if z == 0:
            d[z] = (f[z+1] - f[z]) / (p[z+1] - p[z])
        elif z == (n-1):
            d[z] = (f[z] - f[z-1]) / (p[z] - p[z-1])
        else:
            d[z] = (f[z+1] - f[z-1]) / (p[z+1] - p[z-1])

    return d
