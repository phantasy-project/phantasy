# encoding: UTF-8

import os, unittest, numpy, tempfile, fmdata, t7data


class FMDataTest(unittest.TestCase):

    def setUp(self):
        tfile = open("1TTESTA.T7", "r")
        tdata = t7data.readFromImpactFile(tfile)
        tfile.close()

        (edata, hdata) = fmdata.convertFromT7Data(tdata)

        efile = open("testB_E.dat", "w")
        fmdata.writeToDatFile(edata, efile, field="E", punits="mm", funits="V/m", pscale=1000, fscale=(1.0/2.2))
        efile.close()

        hfile = open("testB_H.dat", "w")
        fmdata.writeToDatFile(hdata, hfile, field="H", punits="mm", funits="A/m", pscale=1000, fscale=(1.0/2.2))
        hfile.close()

        efileA = open("testA_E.dat", "r")
        self.edataA = fmdata.readFromDatFile(efileA, pscale=0.001, fscale=2.2)
        efileA.close()

        hfileA = open("testA_H.dat", "r")
        self.hdataA = fmdata.readFromDatFile(hfileA, pscale=0.001, fscale=2.2)
        hfileA.close()

        efileB = open("testB_E.dat", "r")
        self.edataB = fmdata.readFromDatFile(efileB, pscale=0.001, fscale=2.2)
        efileB.close()

        hfileB = open("testB_H.dat", "r")
        self.hdataB = fmdata.readFromDatFile(hfileB, pscale=0.001, fscale=2.2)
        hfileB.close()


    def tearDown(self):
        os.remove("testB_E.dat")
        os.remove("testB_H.dat")
        pass


    def test_position_x(self):
        self.assertTrue(self.edataA.nx == self.edataB.nx)
        for x in xrange(self.edataA.nx):
            self.assertTrue(self.edataA.px[x] == self.edataB.px[x], msg="Mismatch in E field at X position: %d: %f vs %f" % (x, self.edataA.px[x], self.edataB.px[x]))

        self.assertTrue(self.hdataA.nx == self.hdataB.nx)
        for x in xrange(self.hdataA.nx):
            self.assertTrue(self.hdataA.px[x] == self.hdataB.px[x], msg="Mismatch in H field at X position: %d: %f vs %f" % (x, self.hdataA.px[x], self.hdataB.px[x]))


    def test_position_y(self):
        self.assertTrue(self.edataA.ny == self.edataB.ny)
        for y in xrange(self.edataA.ny):
            self.assertTrue(self.edataA.py[y] == self.edataB.py[y], msg="Mismatch in E field at Y position: %d: %f vs %f" % (y, self.edataA.py[y], self.edataB.py[y]))

        self.assertTrue(self.hdataA.ny == self.hdataB.ny)
        for y in xrange(self.hdataA.ny):
            self.assertTrue(self.hdataA.py[y] == self.hdataB.py[y], msg="Mismatch in H field at Y position: %d: %f vs %f" % (y, self.hdataA.py[y], self.hdataB.py[y]))


    def test_position_z(self):
        self.assertTrue(self.edataA.nz == self.edataB.nz)
        for z in xrange(self.edataA.nz):
            self.assertTrue(self.edataA.pz[z] == self.edataB.pz[z], msg="Mismatch in E field at Z position: %d: %f vs %f" % (z, self.edataA.pz[z], self.edataB.pz[z]))

        self.assertTrue(self.hdataA.nz == self.hdataB.nz)
        for z in xrange(self.hdataA.nz):
            self.assertTrue(self.hdataA.pz[z] == self.hdataB.pz[z], msg="Mismatch in H field at Z position: %d: %f vs %f" % (z, self.hdataA.pz[z], self.hdataB.pz[z]))


    def test_e_field(self):
        for x in xrange(self.edataA.nx):
            for y in xrange(self.edataA.ny):
                for z in xrange(self.edataA.nz):
                    self.assertTrue(self.edataA.fx[x,y,z] == self.edataB.fx[x,y,z], msg="Mismatch in E field (X) at %d, %d, %d: %f  %fj vs %f %fj" % (x, y, z, numpy.real(self.edataA.fx[x,y,z]), numpy.imag(self.edataA.fx[x,y,z]), numpy.real(self.edataB.fx[x,y,z]), numpy.imag(self.edataB.fx[x,y,z])))
                    self.assertTrue(self.edataA.fy[x,y,z] == self.edataB.fy[x,y,z], msg="Mismatch in E field (Y) at %d, %d, %d: %f  %fj vs %f %fj" % (x, y, z, numpy.real(self.edataA.fy[x,y,z]), numpy.imag(self.edataA.fy[x,y,z]), numpy.real(self.edataB.fy[x,y,z]), numpy.imag(self.edataB.fy[x,y,z])))
                    self.assertTrue(self.edataA.fz[x,y,z] == self.edataB.fz[x,y,z], msg="Mismatch in E field (Z) at %d, %d, %d: %f  %fj vs %f %fj" % (x, y, z, numpy.real(self.edataA.fz[x,y,z]), numpy.imag(self.edataA.fz[x,y,z]), numpy.real(self.edataB.fz[x,y,z]), numpy.imag(self.edataB.fz[x,y,z])))
        pass


    def test_h_field(self):
        for x in xrange(self.hdataA.nx):
            for y in xrange(self.hdataA.ny):
                for z in xrange(self.hdataA.nz):
                    self.assertTrue(self.hdataA.fx[x,y,z] == self.hdataB.fx[x,y,z], msg="Mismatch in H field (X) at %d, %d, %d: %f  %fj vs %f %fj" % (x, y, z, numpy.real(self.hdataA.fx[x,y,z]), numpy.imag(self.hdataA.fx[x,y,z]), numpy.real(self.hdataB.fx[x,y,z]), numpy.imag(self.hdataB.fx[x,y,z])))
                    self.assertTrue(self.hdataA.fy[x,y,z] == self.hdataB.fy[x,y,z], msg="Mismatch in H field (Y) at %d, %d, %d: %f  %fj vs %f %fj" % (x, y, z, numpy.real(self.hdataA.fy[x,y,z]), numpy.imag(self.hdataA.fy[x,y,z]), numpy.real(self.hdataB.fy[x,y,z]), numpy.imag(self.hdataB.fy[x,y,z])))
                    self.assertTrue(self.hdataA.fz[x,y,z] == self.hdataB.fz[x,y,z], msg="Mismatch in H field (Z) at %d, %d, %d: %f  %fj vs %f %fj" % (x, y, z, numpy.real(self.hdataA.fz[x,y,z]), numpy.imag(self.hdataA.fz[x,y,z]), numpy.real(self.hdataB.fz[x,y,z]), numpy.imag(self.hdataB.fz[x,y,z])))
        pass


if __name__ == '__main__':
    unittest.main()
