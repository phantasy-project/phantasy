# encoding: UTF-8

import re, numpy

class T7Data:
    """
    T7Data contains 3D field data for IMPACT.

    Properties:
        nx: Number of points in X direction
        ny: Number of points in Y direction
        nz: Number of points in Z direction

        px: Position in X direction (1D)
        py: Position in Y direction (1D)
        pz: Position in Z direction (1D)

        ex: Electric field in X direction (3D)
        ey: Electric field in Y direction (3D)
        ez: Electric field in Z direction (3D)

        hx: Magnetic field in X direction (3D)
        hy: Magnetic field in Y direction (3D)
        hz: Magnetic field in Z direction (3D)
    """

    def __init__(self, px, py, pz, ex, ey, ez, hx, hy, hz, copy=True):
        """
        Initialize the T7Data object

        Arguments:
             px: Position in X direction (1D)
            py: Position in Y direction (1D)
            pz: Position in Z direction (1D)

            ex: Electric field in X direction (3D)
            ey: Electric field in Y direction (3D)
            ez: Electric field in Z direction (3D)

            hx: Magnetic field in X direction (3D)
            hy: Magnetic field in Y direction (3D)
            hz: Magnetic field in Z direction (3D)
        """
        self.nx = px.shape[0]
        self.ny = py.shape[0]
        self.nz = pz.shape[0]
        if copy: 
            self.px = numpy.copy(px)
            self.py = numpy.copy(py)
            self.pz = numpy.copy(pz)
            self.ex = numpy.copy(ex)
            self.ey = numpy.copy(ey)
            self.ez = numpy.copy(ez)
            self.hx = numpy.copy(hx)
            self.hy = numpy.copy(hy)
            self.hz = numpy.copy(hz)
        else:
            self.px = px
            self.py = py
            self.pz = pz
            self.ex = ex
            self.ey = ey
            self.ez = ez
            self.hx = hx
            self.hy = hy
            self.hz = hz
        pass


def readFromImpactFile(file):
    """
    Read field data from IMPACT T7.

    Data format is as follows:
    xstart  xend  xsteps
    ystart  yend  ysteps
    zstart  zend  zsteps
    ex(0,0,0)  ey(0,0,0)  ez(0,0,0)  hx(0,0,0)  hy(0,0,0)  hz(0,0,0)
    ex(1,0,0)  ey(1,0,0)  ez(1,0,0)  hx(1,0,0)  hy(1,0,0)  hz(1,0,0)
    (continued...)
    ex(x,0,0)  ey(x,0,0)  ez(x,0,0)  hx(x,0,0)  hy(1,0,0)  hz(x,0,0)
    ex(0,1,0)  ey(0,1,0)  ez(0,1,0)  hx(0,1,0)  hy(0,1,0)  hz(0,1,0)
    (continued...)
    ex(x,y,0)  ey(x,y,0)  ez(x,y,0)  hx(x,y,0)  hy(x,y,0)  hz(x,y,0)
    ex(0,0,1)  ey(0,0,1)  ez(0,0,1)  hx(0,0,1)  hy(0,0,1)  hz(0,0,1)
    (continued...)
    ex(x,y,z)  ey(z,y,z)  ez(z,y,z)  hx(x,y,z)  hy(x,y,z)  hz(x,y,z)

    where x = zsteps, y = ysteps, z = zsteps

    For example:
    -1.500000e-03 1.500000e-03 6
    -1.500000e-03 1.500000e-03 6
    0.000000e+00 3.000000e-03 6
    3.460248e+05 3.528382e+05 -6.831880e+05 -3.475408e-04 6.960133e-07 -3.534405e-04 
    2.311034e+05 3.534982e+05 -6.857950e+05 -3.486024e-04 4.601209e-07 -2.358553e-04 
    1.156775e+05 3.538942e+05 -6.873570e+05 -3.492383e-04 2.288944e-07 -1.179960e-04 
    0.000000e+00 3.540262e+05 -6.878784e+05 -3.494512e-04 0.000000e+00 -0.000000e+00 
    -1.156775e+05 3.538942e+05 -6.873570e+05 -3.492383e-04 -2.288944e-07 1.179960e-04 
    -2.311034e+05 3.534982e+05 -6.857950e+05 -3.486024e-04 -4.601209e-07 2.358553e-04 
    -3.460248e+05 3.528382e+05 -6.831880e+05 -3.475408e-04 -6.960133e-07 3.534405e-04 
    (continued...)
    """
    xhead = file.readline().split()
    if len(xhead) < 3:
        raise Exception("Invalid T7 file header (X).")
    xsteps = int(xhead[2])
    xstart = float(xhead[0])
    xend = float(xhead[1])
    xstep = (xend - xstart) / xsteps

    yhead = file.readline().split()
    if len(yhead) < 3:
        raise Exception("Invalid T7 file header (Y).")
    ysteps = int(yhead[2])
    ystart = float(yhead[0])
    yend = float(yhead[1])
    ystep = (yend - ystart) / ysteps

    zhead = file.readline().split()
    if len(zhead) < 3:
        raise Exception("Invalid T7 file header (Z).")
    zsteps = int(zhead[2])
    zstart = float(zhead[0])
    zend = float(zhead[1])
    zstep = (zend - zstart) / zsteps

    nx = xsteps + 1
    ny = ysteps + 1
    nz = zsteps + 1

    px = numpy.empty(nx)
    py = numpy.empty(ny)
    pz = numpy.empty(nz)

    ex = numpy.empty([nx,ny,nz])
    ey = numpy.empty([nx,ny,nz])
    ez = numpy.empty([nx,ny,nz])

    hx = numpy.empty([nx,ny,nz])
    hy = numpy.empty([nx,ny,nz])
    hz = numpy.empty([nx,ny,nz])

    x = -1
    y =  0
    z =  0
    for line in file:
        x += 1
        if x == nx:
            x = 0
            y += 1
            if y == ny:
                y = 0
                z += 1
                if z == nz:
                    raise Exception("Invalid T7 file: too many data rows.")

        data = line.split()
        if len(data) < 6:
            raise Exception()

        px[x] = xstart + (x*xstep)
        py[y] = ystart + (y*ystep)
        pz[z] = zstart + (z*zstep)
        ex[x,y,z] = float(data[0])
        ey[x,y,z] = float(data[1])
        ez[x,y,z] = float(data[2])
        hx[x,y,z] = float(data[3])
        hy[x,y,z] = float(data[4])
        hz[x,y,z] = float(data[5])

    return  T7Data(px, py, pz, ex, ey, ez, hx, hy, hz, copy=False) 



def writeToImpactFile(data, file):
    """
    Write field data in IMPACT T7 format.
    """

    nx = data.nx
    ny = data.ny
    nz = data.nz

    xsteps = nx-1
    xstart = data.px[0]
    xend = data.px[xsteps]

    ysteps = ny-1
    ystart = data.py[0]
    yend = data.py[ysteps]

    zsteps = nz-1
    zstart = data.pz[0]
    zend = data.pz[zsteps]

    file.write("%e %e %d\r\n" % (xstart, xend, xsteps))
    file.write("%e %e %d\r\n" % (ystart, yend, ysteps))
    file.write("%e %e %d\r\n" % (zstart, zend, zsteps))

    for z in xrange(nz):
        for y in xrange(ny):
            for x in xrange(nx):
                file.write("%e %e %e %e %e %e \r\n" % (data.ex[x,y,z],data.ey[x,y,z],data.ez[x,y,z],data.hx[x,y,z],data.hy[x,y,z],data.hz[x,y,z]))



def convertFromFMData(edata, hdata):
    """
    Convert field map data to T7 data.
    """
    nx = edata.nx
    ny = edata.ny
    nz = edata.nz

    zmax = numpy.max(edata.pz)
    zstep = zmax / nz

    px = numpy.empty(nx)
    py = numpy.empty(ny)
    pz = numpy.empty(2*nz-1)

    ex = numpy.empty([nx,ny,2*nz-1])
    ey = numpy.empty([nx,ny,2*nz-1])
    ez = numpy.empty([nx,ny,2*nz-1])

    hx = numpy.empty([nx,ny,2*nz-1])
    hy = numpy.empty([nx,ny,2*nz-1])
    hz = numpy.empty([nx,ny,2*nz-1])

    efactor = 1.0
    hfactor = 4.0e-7*numpy.pi*numpy.cos(numpy.pi) # cos(pi) comes from IMPACT convention

    for x in xrange(nx):
        px[x] = edata.px[x]
        for y in xrange(ny):
            py[y] = edata.py[y]
            for z in xrange(nz):
                zalt =  (nz-1) + z
                pz[zalt] = zmax + edata.pz[z]
                ex[x,y,zalt] = efactor * numpy.real(edata.fx[x,y,z])
                ey[x,y,zalt] = efactor * numpy.real(edata.fy[x,y,z])
                ez[x,y,zalt] = efactor * numpy.real(edata.fz[x,y,z])
                hx[x,y,zalt] = hfactor * numpy.imag(hdata.fx[x,y,z])
                hy[x,y,zalt] = hfactor * numpy.imag(hdata.fy[x,y,z])
                hz[x,y,zalt] = hfactor * numpy.imag(hdata.fz[x,y,z])
                if z != 0:
                    zalt2 = (nz-1) - z
                    pz[zalt2] = zmax - edata.pz[z]
                    ex[x,y,zalt2] = ex[x,y,zalt]
                    ey[x,y,zalt2] = ey[x,y,zalt]
                    ez[x,y,zalt2] = -1.0 * ez[x,y,zalt]
                    hx[x,y,zalt2] = -1.0 * hx[x,y,zalt]
                    hy[x,y,zalt2] = -1.0 * hy[x,y,zalt]
                    hz[x,y,zalt2] = hz[x,y,zalt]

    return  T7Data(px, py, pz, ex, ey, ez, hx, hy, hz, copy=False)
