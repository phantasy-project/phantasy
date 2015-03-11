# encoding: UTF-8

import os, unittest, tempfile, fmdata, t7data


class T7DataTest(unittest.TestCase):

    def setUp(self):
        efile = open("testA_E.dat", "r")
        edata = fmdata.readFromDatFile(efile, pscale=0.001, fscale=2.2)
        efile.close()

        hfile = open("testA_H.dat", "r")
        hdata = fmdata.readFromDatFile(hfile, pscale=0.001, fscale=2.2)
        hfile.close()

        tdata = t7data.convertFromFMData(edata, hdata)

        tfile = open("1TTESTB.T7", "w")
        t7data.writeToImpactFile(tdata, tfile)
        tfile.close()

        tfileA = open("1TTESTA.T7", "r")
        self.tdataA = t7data.readFromImpactFile(tfileA)
        tfileA.close()

        tfileB = open("1TTESTB.T7", "r")
        self.tdataB = t7data.readFromImpactFile(tfileB)
        tfileB.close()


    def tearDown(self):
        os.remove("1TTESTB.T7")


    def test_position_x(self):
        self.assertTrue(self.tdataA.nx == self.tdataB.nx)
        for x in xrange(self.tdataA.nx):
            self.assertTrue(self.tdataA.px[x] == self.tdataB.px[x])


    def test_position_y(self):
        self.assertTrue(self.tdataA.ny == self.tdataB.ny)
        for y in xrange(self.tdataA.ny):
            self.assertTrue(self.tdataA.py[y] == self.tdataB.py[y])


    def test_position_z(self):
        self.assertTrue(self.tdataA.nz == self.tdataB.nz)
        for z in xrange(self.tdataA.nz):
            self.assertTrue(self.tdataA.pz[z] == self.tdataB.pz[z])


    def test_e_field(self):
        for x in xrange(self.tdataA.nx):
            for y in xrange(self.tdataA.ny):
                for z in xrange(self.tdataA.nz):
                    self.assertTrue(self.tdataA.ex[x,y,z] == self.tdataB.ex[x,y,z])
                    self.assertTrue(self.tdataA.ey[x,y,z] == self.tdataB.ey[x,y,z])
                    self.assertTrue(self.tdataA.ez[x,y,z] == self.tdataB.ez[x,y,z])
        pass


    def test_h_field(self):
        for x in xrange(self.tdataA.nx):
            for y in xrange(self.tdataA.ny):
                for z in xrange(self.tdataA.nz):
                    self.assertTrue(self.tdataA.hx[x,y,z] == self.tdataB.hx[x,y,z])
                    self.assertTrue(self.tdataA.hy[x,y,z] == self.tdataB.hy[x,y,z])
                    self.assertTrue(self.tdataA.hz[x,y,z] == self.tdataB.hz[x,y,z])
        pass


if __name__ == '__main__':
    unittest.main()
