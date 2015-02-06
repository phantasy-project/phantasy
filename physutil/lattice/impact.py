# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

from __future__ import print_function

import sys

from .. import cfg

from ..layout import accel



def build_lattice(accel, config=None, settings=None):
    """
    """
    lat_factory = LatticeFactory(accel, config, settings)

    lat_factory.start = "LS1"

    return lattice_factory.build()


class LatticeFactory(object):

    def __init__(self, accel, config=None, settings=None, start=None, end=None):
        self.settings = settings
        self.accel = accel
        self.start = start
        self.end = end
        #def write_lattice(add, settings, start="LS1", steps=20, mapsteps=20, lorentz=True, cavity_field_3d=True):




    def build(self):

        if not isinstance(self.accel, accel.Accelerator):
            raise TypeError("Expecting type Accelerator")

        lattice = ImpactLattice()



        for elem in self.accel.iter(self.start, self.end):
            if isinstance(elem, pasv.DriftElement):
                
                #mapsteps = self.config.getint_default("mapsteps")
                lattice.append(elem.length, steps, mapsteps, 0, elem.diameter/2.0)

            elif isinstance(elem, pasv.ValveElement):
                #steps = self.config.getint(elem.dtype, "steps")
                #mapsteps = self.config.getint(elem.dtype, "mapsteps")
                lattice.append(elem.length, steps, mapsteps, 0, elem.diameter/2.0)

            elif isinstance(elem, pasv.PortElement):
                #steps = self.config.getint(elem.dtype, "steps")
                #mapsteps = self.config.getint(elem.dtype, "mapsteps")
                lattice.append(elem.length, steps, mapsteps, 0, elem.diameter/2.0)

            elif isinstance(elem, rf.CavityElement):
                #steps = self.config.getint(elem.dtype, "steps")
                #mapsteps = self.config.getint(elem.dtype, "mapsteps")

                if elem.channels.phase in self.settings:
                    phase = self.settings[elem.channels.phase]
                else:
                    raise Exception("setting: '{}' not found for element: {}".format(elem.channels.phase, elem.channels.phase))

                if elems.channels.amplitude in self.settings:
                    amplitude = self.settings[elem.channels.amplitude]
                else:
                    raise Exception("setting: 'AMPL' not found for element: {}".format(elem.name))
                
                radius = elem.diameter / 2.0
                if cavity_field_3d:
                    lattice.append([elem.length, 48, 20, 110, amplitude, elem.frequency, phase, _file_id(elem.beta), radius, radius, 0, 0, 0, 0, 0, 1, 2 ])
                else:
                    lattice.append([elem.length, 60, 20, 103, amplitude, elem.frequency, phase, _file_id(elem.beta), radius])

            elif isinstance(elem, mag.SolElement):
                #steps = self.config.getint(elem.dtype, "steps")
                #mapsteps = self.config.getint(elem.dtype, "mapsteps")
                if elems.channels.field in self.settings:
                    field = settings[elems.channels.field]
                else:
                    raise Exception("setting: 'B' not found for element: {}".format(elem.name))

                lattice.append([elem.length/2.0, 1, 20, 3, field, 0.0, elem.diameter/2.0])
                lattice.append([0.0, 0, 0, -21, elem.diameter/2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
                lattice.append([elem.length/2.0, 1, 20, 3, field, 0.0, elem.diameter/2.0])

            elif isinstance(elem, mag.QuadElement):
                #steps = self.config.getint(elem.dtype, "steps")
                #mapsteps = self.config.getint(elem.dtype, "mapsteps")

                # if elem.name not in settings:
                #     raise Exception("settings not found for element: {}".format(elem.name))
                # if "B" not in settings[elem.name]:
                #     raise Exception("setting: 'B' not found for element: {}".format(elem.name))
                # field = settings[elem.name]["B"]

                if elems.channels.field in self.settings:
                    field = settings[elems.channels.field]
                else:
                    raise Exception("setting: 'B' not found for element: {}".format(elem.name))

                lattice.append([elem.length, 50, 20, 1, field, 0.0, elem.diameter/2.0])

            elif isinstance(elem, mag.CorrElement):
                #steps = self.config.getint(elem.dtype, "steps")
                #mapsteps = self.config.getint(elem.dtype, "mapsteps")

                #if elem.length != 0.0:
                #    raise Exception("expecting corrector element with length 0.0 for element: {}".format(elem.name))
                #if elem.name not in settings:
                #    raise Exception("settings not found for element: {}".format(elem.name))
                #if "B" not in settings[elem.name]:
                #    raise Exception("settings: 'B' not found for element: {}".format(elem.name))
                #field = float(settings[elem.name]["B"])
                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.diameter/2.0])

                lattice.append([0.0, 0, 0, -21, elem.diameter/2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.diameter/2.0])

            elif isinstance(elem, (diag.BLMElement, diag.PMElement, diag.BLElement)):
                if elem.length != 0.0:
                    #steps = self.config.getint(elem.dtype, "steps")
                    #mapsteps = self.config.getint(elem.dtype, "mapsteps")
                    lattice.append([elem.length, steps, mapsteps, 0, elem.diameter/2.0])

            elif isinstance(elem, diag.BPMElement):
                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.diameter/2.0])

                lattice.append([0.0, 0, 0, -23])
                result_map.append(elem.name)

                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.diameter/2.0])
                
            else:
                raise Exception("Unsupport ADD element: {}".format(elem))
                
        return lattice


        
def _file_id(n):
    if n > 0.0:
        while n < 100.0:
            n *= 10
        return int(n)
    else:
        raise Exception("Cannot generate file id from '{}'".format(n))
  

class Lattice(object):

    # _HEADER_OFFSET = 11

    # OUTPUT_TYPE_STANDARD

    # OUTPUT_TYPE_90_95_99

    # INTEGRATOR_LINEAR

    # INTEGRATOR_LORENTZ

    #DISTRIBUTION_

    def __init__(self):
        self.nparticles = 1000
        self.nprocessors = 10
    #    self._change_states = []
        self._elements = []
        pass


    @property
    def nparticles(self):
        return self._nparticle

    @nparticles.setter
    def nparticles(self, nparticles):
        self._nparticles = int(nparticles)


    @property
    def nprocessors(self):
        return self._nprocessors

    @nprocessors.setter
    def nprocessors(self, nprocessors):
        self._nprocessors = int(nprocessors)



    def append(self, *args):
        self._elements.append(args)


    def write(self, file=sys.stdout):
        file.write("{lat.nprocessors} 1\r\n".format(lat=self))
        file.write("6 {lat.nparticles} 2 0 2\r\n".format(lat=self))
        file.write("3 0 0 1\r\n")
        file.write("{lat.nparticles}\r\n".format(lat=self))
        file.write("0.0\r\n")
        file.write("1.48852718947e-10\r\n")
        file.write("0.22734189E-02  0.88312578E-04  0.00000000E+00  1.000  1.000  0.000  0.000\r\n")
        file.write("0.22734189E-02  0.88312578E-04  0.00000000E+00  1.000  1.000  0.000  0.000\r\n")
        file.write("0.76704772E-01  0.34741445E-05  0.00000000E+00  1.000  1.000  0.000  0.000\r\n")
        file.write("0.0 0.5e6 931.49432e6 0.1386554621848 80.50e6 0.0 99.9\r\n")

    #     # compact lattice by merging drifts
    #     clattice = []
    #     for line in lattice:
    #         if (line[3] == 0) and (len(clattice) > 0) and (clattice[-1][3] == 0):
    #             clattice[-1][0] += line[0]
    #         else:
    #             clattice.append(line)


        for line in self._elements:
            for rec in line:
                if isinstance(rec, int):
                    file.write("{:d} ".format(rec))
                elif isinstance(rec, float):
                    file.write("{:.7E} ".format(rec))
            file.write("/\r\n")
