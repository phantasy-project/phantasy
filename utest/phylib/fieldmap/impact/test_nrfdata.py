# encoding: UTF-8

import os, unittest, numpy

from phyutil.phylib.fieldmap import fmdata

from phyutil.phylib.fieldmap.impact import lrfdata, nrfdata


DIRNAME = os.path.dirname(__file__)

TESTA_E_DAT = os.path.join(DIRNAME,  "testA_E.dat")


class NRFDataTest(unittest.TestCase):

    COEFS = numpy.array([ 
                            1.3984902125230292E-009  +0.0000000000000000j,
                            2.8919089345436078E-012  +7157768.1074381620j,
                           -3.3138292110379552E-010  +7498817.9610251356j,
                           -9.5305097147502238E-011  +2971740.5672894213j,
                           -1.0725642596298712E-010  -593259.74093360268j,
                           -2.3213786448650353E-009  -1163231.2334608522j,
                           -2.9465780926329899E-009  -415063.84283348132j,
                           -4.8821391374076484E-010  +3068.7472211114532j,
                            3.6619383081415435E-009  -69922.159757224043j,
                            4.1821976992650889E-009  -174323.89862790916j,
                            3.2408067340838898E-009  -120393.85503225695j,
                            1.4235297385312151E-009  -17610.150890604858j,
                            1.6607657471467974E-009  +25062.943401117394j,
                           -1.5492460647692496E-009  +15136.545836446834j,
                           -4.8442245770274894E-009  +495.60041154660036j,
                           -7.3580537218731479E-009  +20.779114688271960j,
                           -3.6433220884646289E-009  +4242.4187362657904j,
                            2.4399611220360384E-009  +4589.3004330069825j,
                            5.3467701377485355E-009  +1674.5147594865171j,
                            5.8368385680296342E-009  -298.88820898759212j
                       ])

    def setUp(self):
        efile = open(TESTA_E_DAT, "r")
        edata = fmdata.readFromDatFile(efile, pscale=0.001, fscale=2.2)
        efile.close()

        self.lrfdata = lrfdata.convertFromFMData(edata)


    def test_conversion(self):        
        data = nrfdata.convertFromLRFData(self.lrfdata, ncoefs=20)
        for idx in xrange(20):
            self.assertTrue(numpy.allclose(numpy.real(data.cf[idx]), numpy.real(self.COEFS[idx])), msg = "Incorrect real Fourier coefficient %d: %g: expecting %g" % (idx, numpy.real(data.cf[idx]), numpy.real(self.COEFS[idx])))
            self.assertTrue(numpy.allclose(numpy.imag(data.cf[idx]), numpy.imag(self.COEFS[idx])), msg = "Incorrect imag Fourier coefficient %d: %g: expecting %g" % (idx, numpy.imag(data.cf[idx]), numpy.imag(self.COEFS[idx])))

