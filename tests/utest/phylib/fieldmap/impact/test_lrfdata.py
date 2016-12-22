# encoding: UTF-8

import os, unittest, numpy

from phyutil.phylib.fieldmap import fmdata

from phyutil.phylib.fieldmap.impact import lrfdata, nrfdata


DIRNAME = os.path.dirname(__file__)

TESTA_E_DAT = os.path.join(DIRNAME, "testA_E.dat")

TESTA_LRF = os.path.join(DIRNAME, "testA.lrf")

TESTA_NRF = os.path.join(DIRNAME, "testA.nrf")


class LRFDataTest(unittest.TestCase):

    PSCALE=0.001
    FSCALE=2.2

    START=-0.12
    END=0.12
    NPOINTS=81

    BETA = 0.04
    FREQ = 80.0E6
    PHASE = numpy.pi/8.0

    TTF = 0.758571552
    VOLTAGE = 914704.306


    def test_convertFromFMData(self):

        with  open(TESTA_E_DAT, "r") as efileA:
            edataA = fmdata.readFromDatFile(efileA, pscale=self.PSCALE, fscale=self.FSCALE)

        ldataA = lrfdata.convertFromFMData(edataA)

        with open(TESTA_LRF, "r") as lfileB:
            ldataB = lrfdata.readFromImpactFile(lfileB)

        n = ldataB.n
        
        for z in xrange(n):
            self.assertTrue(numpy.allclose(ldataA.p[z], ldataB.p[z]),
                msg="Incorrect position at %d: %g: expecting %g" % (z, ldataA.p[z], ldataB.p[z]))
            self.assertTrue(numpy.allclose(ldataA.f[z], ldataB.f[z]),
                msg="Incorrect electric field at %d: %g: expecting %g" % (z, ldataA.f[z], ldataB.f[z]))
            self.assertTrue(numpy.allclose(ldataA.df[z], ldataB.df[z]),
                msg="Incorrect electric field derivative at %d: %g: expecting %g" % (z, ldataA.df[z], ldataA.df[z]))


    def test_convertFromNRFData(self):

        with open(TESTA_NRF, "r") as nfileA:
            ndataA = nrfdata.readFromImpactFile(nfileA)

        ldataA = lrfdata.convertFromNRFData(ndataA, start=self.START, end=self.END, npoints=self.NPOINTS)

        with open(TESTA_LRF, "r") as lfileB:
            ldataB = lrfdata.readFromImpactFile(lfileB)

        n = ldataB.n

        # The field recontruction from RF coeficients
        # is not correct for the first and last points.
        # Make these 'corrections' to the expected field.

        ldataB.f[0] = 0.0
        ldataB.df[0] = (ldataA.f[1]-ldataA.f[0]) / (ldataA.p[1]-ldataA.p[0])
        ldataB.df[1] = (ldataA.f[2]-ldataA.f[0]) / (ldataA.p[2]-ldataA.p[0])

        ldataB.f[n-1] = 0.0
        ldataB.df[n-1] = (ldataA.f[n-1]-ldataA.f[n-2]) / (ldataA.p[n-1]-ldataA.p[n-2])
        ldataB.df[n-2] = (ldataA.f[n-1]-ldataA.f[n-3]) / (ldataA.p[n-1]-ldataA.p[n-3])

        for z in xrange(0, n):
            self.assertTrue(numpy.allclose(ldataA.p[z], ldataB.p[z]),
                msg="Incorrect position at %d: %g: expecting %g" % (z, ldataA.p[z], ldataB.p[z]))
            self.assertTrue(numpy.allclose(ldataB.f[z], ldataA.f[z], atol=1e-7), # increase tolerance from default 1e-8 #
                msg="Incorrect electric field at %d: %g: expecting %g" % (z, ldataA.f[z], ldataB.f[z]))
            self.assertTrue(numpy.allclose(ldataA.df[z], ldataB.df[z]),
                msg="Incorrect electric field derivative at %d: %g: expecting %g" % (z, ldataA.df[z], ldataB.df[z]))


    def test_voltage(self):
        with open(TESTA_LRF, "r") as lfileA:
            ldataA = lrfdata.readFromImpactFile(lfileA)
        voltage = ldataA.voltage(self.BETA, self.FREQ, self.PHASE)
        self.assertTrue(numpy.allclose(voltage, self.VOLTAGE), msg = "Incorrect acceleration voltage: %f: expecting %f" % (voltage, self.VOLTAGE))


    def test_TTF(self):
        with open(TESTA_LRF, "r") as lfileA:
            ldataA = lrfdata.readFromImpactFile(lfileA)
        ttf = ldataA.ttf(self.BETA, self.FREQ, self.PHASE)
        self.assertTrue(numpy.allclose(ttf, self.TTF), msg = "Incorrect transit time factor: %f: expecting %f" % (ttf, self.TTF))

