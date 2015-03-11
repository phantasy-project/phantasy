# encoding: UTF-8

import sys, numpy

class NRFData:
    """
    NRFData contains Nonlinear RF data.
    """
    def __init__(self, cf, copy=True):
        self.n = cf.shape[0]
        if copy:
            self.cf = numpy.copy(cf)
        else:
            self.cf = cf


def readFromImpactFile(file):
    """
    Read nonlinear RF data from IMPACT data file format.
    """
    cf = []
    real = True
    line = file.readline()
    cf.append(float(line) + 0.0j)

    for line in file:
        if real:
            re = float(line)
            real = False
        else:
            im = float(line)
            real = True
            cf.append(re + 1.0j * im)
    
    return NRFData(numpy.array(cf), copy=False)


def writeToImpactFile(data, file=sys.stdout):
    """
    Write nonlinear RF data to IMPACT data file format.
    """
    file.write("%.14g\r\n" % (numpy.real(data.cf[0]),))
    for idx in xrange(1, data.n):
        file.write("%.14g\r\n" % (numpy.real(data.cf[idx]),))
        file.write("%.14g\r\n" % (numpy.imag(data.cf[idx]),))


def convertFromLRFData(data, ncoefs=40):
    """
    Convert linear RF data to nonlinear RF data. 

    Algorithm has been copied from 'rfcoef' utility written by Ji Qiang, LBNL (c) 2011.
    """
#  !----------------------------------------------------------------
#  ! (c) Copyright, 2011 by the Regents of the University of California.
#  ! Version: 1.1
#  ! Author: Ji Qiang, LBNL
#  ! Description: find the Fourier coeficients of input discrete RF data.
#  !----------------------------------------------------------------

#   program rfcoef

    pi = numpy.pi
    cos = numpy.cos
    sin = numpy.sin

    ndatareal = data.n
    ncoefreal = ncoefs

#   integer, parameter :: Ndata = 50000
#   integer, parameter :: Ncoef = 100
#   double precision, dimension(Ndata) :: zdata,edata
    zdata = data.p
    edata = data.f
#   double precision, dimension(Ncoef) :: Fcoef,Fcoef2
    Fcoef = numpy.zeros(ncoefreal)
    Fcoef2 = numpy.zeros(ncoefreal)
#   double precision :: emax

#    emax = 0.0d0
#    open(3,file="rfdata.in",status="old")
#    n = 0
#10  continue
#    read(3,*,end=100)tmp1,tmp2,tmp3
#    n = n+1
#    zdata(n) = tmp1
#    edata(n) = tmp2
#    if(emax.le.abs(tmp2)) then
#        emax = abs(tmp2)
#    endif
#    goto 10
#100 continue
#    close(3)
#    ndatareal = n
#
#    print*,"Emax is: ",emax
#
#    print*,"How many Fourier coeficients you want?"
#    read(*,*)ncoefreal

#   zlen = zdata(ndatareal)-zdata(1)
    zlen = zdata[ndatareal-1]-zdata[0]
    zhalf = zlen/2.0
#   zmid = (zdata(ndatareal)+zdata(1))/2
    zmid = (zdata[ndatareal-1]+zdata[0])/2.0
    h = zlen/(ndatareal-1)
    #pi = 2*asin(1.0)

#   do j = 1, ncoefreal
    for j in xrange(ncoefreal):
#       zz = zdata(1) - zmid
        zz = zdata[0] - zmid
#       Fcoef(j) = (-0.5*edata(1)*cos((j-1)*2*pi*zz/zlen)*h)/zhalf
        Fcoef[j] = (-0.5*edata[0]*cos( j *2.0*pi*zz/zlen)*h)/zhalf
#       Fcoef2(j) = (-0.5*edata(1)*sin((j-1)*2*pi*zz/zlen)*h)/zhalf
        Fcoef2[j] = (-0.5*edata[0]*sin( j *2.0*pi*zz/zlen)*h)/zhalf
#       zz = zdata(ndatareal) - zmid
        zz = zdata[ndatareal-1] - zmid
#       Fcoef(j) = Fcoef(j)-(0.5*edata(ndatareal)*cos((j-1)*2*pi*zz/zlen)*h)/zhalf
        Fcoef[j] = Fcoef[j]-(0.5*edata[ndatareal-1]*cos(j*2.0*pi*zz/zlen)*h)/zhalf
#       Fcoef2(j) = Fcoef2(j)-(0.5*edata(ndatareal)*sin((j-1)*2*pi*zz/zlen)*h)/zhalf
        Fcoef2[j] = Fcoef2[j]-(0.5*edata[ndatareal-1]*sin(j*2.0*pi*zz/zlen)*h)/zhalf
#   enddo


#   do i = 1, ndatareal
    for i in xrange(ndatareal):
#       zz = (i-1)*h + zdata(1)
        zz = i*h + zdata[0]
#       !zz = zdata(i) - zmid
#       klo=1
        klo=0
#       khi=ndatareal
        khi=ndatareal-1
#1      if(khi-klo.gt.1) then
        while khi-klo > 1:
            k=(khi+klo)/2
#           if(zdata(k).gt.zz)then
            if zdata[k] > zz:
                khi=k
#           else
            else:
                klo=k
#           endif
#           goto 1
#       endif
#       hstep=zdata(khi)-zdata(klo)
        hstep=zdata[khi]-zdata[klo]
#       slope=(edata(khi)-edata(klo))/hstep
        slope=(edata[khi]-edata[klo])/hstep
#       ez1 =edata(klo)+slope*(zz-zdata(klo))
        ez1 =edata[klo]+slope*(zz-zdata[klo])

#       !zz = (i-1)*h - zmid
#       !zz = (i-1)*h - half
#       zz = zdata(1) + (i-1)*h - zmid
        zz = zdata[0] +   i*h - zmid
#       !zz = zdata(i) - zmid

#       do j = 1, ncoefreal
        for j in xrange(ncoefreal):
#           !Fcoef(j) = Fcoef(j) + (edata(i)*cos((j-1)*2*pi*zz/zlen)*h)/zhalf
#           !Fcoef2(j) = Fcoef2(j) + (edata(i)*sin((j-1)*2*pi*zz/zlen)*h)/zhalf
#           Fcoef(j) = Fcoef(j) + (ez1*cos((j-1)*2*pi*zz/zlen)*h)/zhalf
            Fcoef[j] = Fcoef[j] + (ez1*cos( j *2.0*pi*zz/zlen)*h)/zhalf
#           Fcoef2(j) = Fcoef2(j) + (ez1*sin((j-1)*2*pi*zz/zlen)*h)/zhalf
            Fcoef2[j] = Fcoef2[j] + (ez1*sin( j *2.0*pi*zz/zlen)*h)/zhalf
#       enddo
#   enddo

    return NRFData(Fcoef + 1.0j*Fcoef2, copy=False)

#   open(7,file="rfcoef.out",status="unknown")
#   do j = 1, ncoefreal
#      write(7,*)j,Fcoef(j),Fcoef2(j)
#   enddo
#   close(7)
#
#   emax = 1.0d0
#   open(8,file="rfdatax",status="unknown")
#   write(8,*)Fcoef(1)/emax
#   do j = 2, ncoefreal
#       write(8,*)Fcoef(j)/emax
#       write(8,*)Fcoef2(j)/emax
#   enddo
#   close(8)
#
#   open(8,file="rfdata.out",status="unknown")
#   do i = 1, ndatareal
#       zz = zdata(i) - zmid
#       tmpsum = 0.5*Fcoef(1)
#       tmpsump = 0.0
#       tmpsumpp = 0.0
#       do j = 2,ncoefreal
#           tmpsum = tmpsum + Fcoef(j)*cos((j-1)*2*pi*zz/zlen) + &
#                    Fcoef2(j)*sin((j-1)*2*pi*zz/zlen)
#           tmpsump = tmpsump-(j-1)*2*pi*Fcoef(j)*sin((j-1)*2*pi*zz/zlen)/zlen +&
#                     (j-1)*2*pi*Fcoef2(j)*cos((j-1)*2*pi*zz/zlen)/zlen
#           tmpsumpp = tmpsumpp-((j-1)*2*pi*Fcoef(j)/zlen)**2*cos((j-1)*2*pi*zz/zlen) -&
#                      ((j-1)*2*pi*Fcoef2(j)/zlen)**2*sin((j-1)*2*pi*zz/zlen)
#       enddo
#       write(8,*)zdata(i),tmpsum,tmpsump,tmpsumpp
#    enddo
#    close(8)
#
#    stop
#    end program rfcoef
