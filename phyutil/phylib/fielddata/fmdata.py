# encoding: UTF-8

import re, numpy

class FMData:
    """
    FMData contains the electic or magnetic 3D field map data.

    Properties:
        nx: Number of points in X direction
        ny: Number of points in Y direction
        nz: Number of points in Z direction

        px: Position in X direction (1D)
        py: Position in Y direction (1D)
        pz: Position in Z direction (1D)

        fx: Field in X direction (Complex 3D)
        fy: Field in Y direction (Complex 3D)
        fz: Field in Z direction (Complex 3D)
    """

    def __init__(self, px, py, pz, fx, fy, fz, copy=True):
        """
        Initialize the FMData object
        
        Arguments:
            px: Position in X direction (1D)
            py: Position in Y direction (1D)
            pz: Position in Z direction (1D)

            fx: Field in X direction (Complex 3D)
            fy: Field in Y direction (Complex 3D)
            fz: Field in Z direction (Complex 3D)

            copy: Make copy of data (default: True)
        """
        self.nx = px.shape[0]
        self.ny = py.shape[0]
        self.nz = pz.shape[0]
        if copy:
            self.px = numpy.copy(px)
            self.py = numpy.copy(py)
            self.pz = numpy.copy(pz)
            self.fx = numpy.copy(fx)
            self.fy = numpy.copy(fy)
            self.fz = numpy.copy(fz)
        else:
            self.px = px
            self.py = py
            self.pz = pz
            self.fx = fx
            self.fy = fy
            self.fz = fz
        pass

    def indexAtPosX(self, posx):
        for idx in xrange(self.nx):
            if posx == self.px[idx]:
                return idx
        raise Exception("Position (X) not found in field map: " + str(posx))

    def indexAtPosY(self, posy):
        for idx in xrange(self.ny):
            if posy == self.py[idx]:
                return idx
        raise Exception("Position (Y) not found in field map: " + str(posy))

    def indexAtPosZ(self, posz):
        for idx in xrange(self.nz):
            if posz == self.pz[idx]:
                return idx
        raise Exception("Position (Z) not found in field map: " + str(posz))



def readFromDatFile(file, pscale=1.0, fscale=1.0):
    """
    Read 3D field map data (typically file extention '.dat') and construct a FMData object.

    Data format is as follows:
            x [mm]     y [mm]     z [mm]     ExRe [V/m]   EyRe [V/m]     EzRe [V/m]   ExIm [V/m]   EyIm [V/m]   EzIm [V/m]  
    ---------------------------------------------------------------------------------------------------------------------------
             px(0)      py(0)      pz(0)    exre(0,0,0)  eyre(0,0,0)    ezre(0,0,0)  exim(0,0,0)  eyim(0,0,0)  ezim(0,0,0)
             px(0)      py(0)      pz(1)    exre(0,0,1)  eyre(0,0,1)    ezre(0,0,1)  exim(0,0,1)  eyim(0,0,1)  ezim(0,0,1)
    (continued...)
             px(0)      py(0)      pz(z)    exre(0,0,z)  eyre(0,0,z)    ezre(0,0,z)  exim(0,0,z)  eyim(0,0,z)  ezim(0,0,z)
             px(0)      py(1)      pz(0)    exre(0,1,0)  eyre(0,1,0)    ezre(0,1,0)  exim(0,1,0)  eyim(0,1,0)  ezim(0,1,0)
    (continued...)
             px(0)      py(y)      pz(z)    exre(0,y,z)  eyre(0,y,z)    ezre(0,y,z)  exim(0,y,z)  eyim(0,y,z)  ezim(0,y,z)
             px(1)      py(0)      pz(0)    exre(1,0,0)  eyre(1,0,0)    ezre(1,0,0)  exim(1,0,0)  eyim(1,0,0)  ezim(1,0,0)
    (continued...)
             px(x)      py(y)      pz(z)    exre(x,y,z)  eyre(x,y,z)    ezre(x,y,z)  exim(x,y,z)  eyim(x,y,z)  ezim(x,y,z)

    where x, y and z are the number of steps (or indexes) in each direction respectively.


    For example:
            x [mm]     y [mm]     z [mm]     ExRe [V/m]   EyRe [V/m]     EzRe [V/m]   ExIm [V/m]   EyIm [V/m]   EzIm [V/m]  
    ---------------------------------------------------------------------------------------------------------------------------
               -17        -17       16.5       -776.224      1757.55   1.04082e+007           -0            0            0
               -17        -17         17       -25981.6      58809.3   1.03967e+007           -0            0            0
               -17        -17       17.5       -51887.1       113364   1.03643e+007           -0            0            0
               -17        -17         18       -79062.8       163416   1.03134e+007           -0            0            0
               -17        -17       18.5        -107792       207626   1.02471e+007           -0            0            0
               -17        -17         19        -138036       245302   1.01687e+007           -0            0            0
               -17        -17       19.5        -169456       276448   1.00817e+007           -0            0            0
               -17        -17         20        -201611       301186   9.98904e+006           -0            0            0
    (continued...)
    """

    COLUMN_POSX = 0
    COLUMN_POSY = 1
    COLUMN_POSZ = 2
    COLUMN_FXRE = 3
    COLUMN_FYRE = 4
    COLUMN_FZRE = 5
    COLUMN_FXIM = 6
    COLUMN_FYIM = 7
    COLUMN_FZIM = 8

    scale = numpy.array([ pscale, pscale, pscale, fscale, fscale, fscale, fscale, fscale, fscale ])

    labels = [ "x", "y", "z", "[EH]xRe", "[EH]yRe", "[EH]zRe", "[EH]xIm", "[EH]yIm", "[EH]zIm" ]

    header = re.findall("\s*(\S*)\s*\[(\S*)\]", file.readline())
    if len(header) != len(labels):
        raise Exception("Invalid header: expecting " + str(len(labels)) + " columns")

    for col in xrange(len(labels)):
        if not re.match(labels[col], header[col][0]):
            raise Exception("Invalid column " + str(col) + ": unexpected label: " + header[col][0])
    
    # ignore seperator line
    file.readline()

    count = 0
    x, nx, px = 0, 0, numpy.empty(10)
    y, ny, py = 0, 0, numpy.empty(10)
    z, nz, pz = 0, 0, numpy.empty(10)

    fx = numpy.empty((10,10,10), dtype=numpy.complex)
    fy = numpy.empty((10,10,10), dtype=numpy.complex)
    fz = numpy.empty((10,10,10), dtype=numpy.complex)

    for line in file:     
        
        count += 1

        data = numpy.fromstring(line, sep=" ")
        if len(data) < 9:
            raise Exception("Invalid data record at line " + str(count))
        
        data *= scale

        if nx == 0:
            nx = 1
            px[x] = data[COLUMN_POSX]

        elif px[x] > data[COLUMN_POSX]:
            x = 0
            
        elif px[x] < data[COLUMN_POSX]:
            x += 1
            if x == nx:
                nx += 1
                if nx == len(px):
                    px.resize(2 * px.shape[0])
                    fx.resize((2 * fx.shape[0], fx.shape[1], fx.shape[2]))
                    fy.resize((2 * fy.shape[0], fy.shape[1], fy.shape[2]))
                    fz.resize((2 * fz.shape[0], fz.shape[1], fz.shape[2]))

                px[x] = data[COLUMN_POSX]

            elif px[x] != data[COLUMN_POSX]:
                raise Exception("Invalid position (Y) at line " + str(count) + ": " + str(data[COLUMN_POSX]))

        if ny == 0:
            ny = 1
            py[y] = data[COLUMN_POSY]

        elif py[y] > data[COLUMN_POSY]:
            y = 0
            
        elif py[y] < data[COLUMN_POSY]:
            y += 1
            if y == ny:
                ny += 1
                if ny == len(py):
                    py.resize(2 * py.shape[0])
                    fx.resize((fx.shape[0], 2 * fx.shape[1], fx.shape[2]))
                    fy.resize((fy.shape[0], 2 * fy.shape[1], fy.shape[2]))
                    fz.resize((fz.shape[0], 2 * fz.shape[1], fz.shape[2]))

                py[y] = data[COLUMN_POSY]

            elif py[y] != data[COLUMN_POSY]:
                raise Exception("Invalid position (Y) at line " + str(count) + ": " + str(data[COLUMN_POSY]))

        if nz == 0:
            nz = 1
            pz[z] = data[COLUMN_POSZ]

        elif pz[z] > data[COLUMN_POSZ]:
            z = 0
            
        elif pz[z] < data[COLUMN_POSZ]:
            z += 1
            if z == nz:
                nz += 1
                if nz == len(pz):
                    pz.resize(2 * pz.shape[0])
                    fx.resize((fx.shape[0], fx.shape[1], 2 * fx.shape[2]))
                    fy.resize((fy.shape[0], fy.shape[1], 2 * fy.shape[2]))
                    fz.resize((fz.shape[0], fz.shape[1], 2 * fz.shape[2]))

                pz[z] = data[COLUMN_POSZ]

            elif pz[z] != data[COLUMN_POSZ]:
                raise Exception("Invalid position (Z) at line " + str(count) + ": " + str(data[COLUMN_POSZ]))

        fx[x,y,z] = data[COLUMN_FXRE] + 1j * data[COLUMN_FXIM]
        fy[x,y,z] = data[COLUMN_FYRE] + 1j * data[COLUMN_FYIM]
        fz[x,y,z] = data[COLUMN_FZRE] + 1j * data[COLUMN_FZIM]

    if (nx * ny * nz) != count:
        raise Exception("Invalid data: expecting " + str(nx*ny*nz) + " lines, only " + str(count) + " read")

    return FMData(px[:nx], py[:ny], pz[:nz], fx[:nx,:ny,:nz], fy[:nx,:ny,:nz], fz[:nx,:ny,:nz], copy=False)


def writeToDatFile(data, file, field="E", punits="mm", funits="V/m", pscale=1.0, fscale=1.0):
    """
    Write to field map to DAT data file.
    """

    nx = data.nx
    ny = data.ny
    nz = data.nz

    file.write("       x [{0}]         y [{0}]         z [{0}]     {1}xRe [{2}]     {1}yRe [{2}]     {1}zRe [{2}]     {1}xIm [{2}]     {1}yIm [{2}]     {1}zIm [{2}]  \r\n".format(punits, field, funits))
    file.write("------------------------------------------------------------------------------------------------------------------------------------------\r\n")

    for x in xrange(nx):
        px = pscale * data.px[x]
        for y in xrange(ny):
            py = pscale * data.py[y]
            for z in xrange(nz):
                pz = pscale * data.pz[z]
                fxre = fscale * numpy.real(data.fx[x,y,z])
                fyre = fscale * numpy.real(data.fy[x,y,z])
                fzre = fscale * numpy.real(data.fz[x,y,z])
                fxim = fscale * numpy.imag(data.fx[x,y,z])
                fyim = fscale * numpy.imag(data.fy[x,y,z])
                fzim = fscale * numpy.imag(data.fz[x,y,z])
                file.write("%13.1f  %13.1f  %13.1f  %13.6g  %13.6g  %13.6g  %13.6g  %13.6g  %13.6g\r\n" % (px, py, pz, fxre, fyre, fzre, fxim, fyim, fzim))


def convertFromT7Data(data, eimag=0.0, hreal=0.0):
    """
    Convert T7 data to field map data.
    """
    nx =  data.nx
    ny =  data.ny
    nz = (data.nz + 1) / 2

    epx = numpy.empty(nx)
    epy = numpy.empty(ny)
    epz = numpy.empty(nz)

    efx = numpy.empty([nx,ny,nz], dtype=numpy.complex)
    efy = numpy.empty([nx,ny,nz], dtype=numpy.complex)
    efz = numpy.empty([nx,ny,nz], dtype=numpy.complex)

    hpx = numpy.empty(nx)
    hpy = numpy.empty(ny)
    hpz = numpy.empty(nz)

    hfx = numpy.empty([nx,ny,nz], dtype=numpy.complex)
    hfy = numpy.empty([nx,ny,nz], dtype=numpy.complex)
    hfz = numpy.empty([nx,ny,nz], dtype=numpy.complex)

    zmax = numpy.max(data.pz) / 2.0

    efactor = 1.0
    hfactor = 1.0 / (4.0e-7*numpy.pi*numpy.cos(numpy.pi)) # cos(pi) comes from IMPACT convention

    for x in xrange(nx):
        epx[x] = data.px[x]
        hpx[x] = data.px[x]
        for y in xrange(ny):
            epy[y] = data.py[y]
            hpy[y] = data.py[y]
            for z in xrange(nz):
                zalt = (nz-1) + z
                epz[z] = data.pz[zalt] - zmax
                hpz[z] = data.pz[zalt] - zmax
                efx[x,y,z] = (efactor * data.ex[x,y,zalt] + 1.0j * eimag)
                efy[x,y,z] = (efactor * data.ey[x,y,zalt] + 1.0j * eimag)
                efz[x,y,z] = (efactor * data.ez[x,y,zalt] + 1.0j * eimag)
                hfx[x,y,z] = (hreal + 1.0j * hfactor * data.hx[x,y,zalt])
                hfy[x,y,z] = (hreal + 1.0j * hfactor * data.hy[x,y,zalt])
                hfz[x,y,z] = (hreal + 1.0j * hfactor * data.hz[x,y,zalt])

    return (FMData(epx, epy, epz, efx, efy, efz, copy=False), FMData(hpx, hpy, hpz, hfx, hfy, hfz, copy=False))
