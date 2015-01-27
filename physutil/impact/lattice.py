# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

from __future__ import print_function

import sys

from ..add import pasv, diag, mag, rf, accel


def write_lattice(add, settings, start="LS1", steps=20, mapsteps=20, lorentz=True, cavity_field_3d=True):

    if not isinstance(add, accel.Accelerator):
        raise TypeError("Expecting type Accelerator")

    lattice = []

    result_map = []

    for elem in add.iter(start):
        if isinstance(elem, pasv.DriftElement):
            lattice.append([elem.length, steps, mapsteps, 0, elem.diameter/2.0])

        elif isinstance(elem, pasv.ValveElement):
            lattice.append([elem.length, steps, mapsteps, 0, elem.diameter/2.0])

        elif isinstance(elem, pasv.PortElement):
            lattice.append([elem.length, steps, mapsteps, 0, elem.diameter/2.0])

        elif isinstance(elem, rf.CavityElement):
            if elem.name not in settings:
                raise Exception("settings not found for element: {}".format(elem.name))
            if "AMPL" not in settings[elem.name]:
                raise Exception("setting: 'AMPL' not found for element: {}".format(elem.name))
            vscale =  settings[elem.name]["AMPL"] / elem.voltage
            if "PHA" not in settings[elem.name]:
                raise Exception("setting: 'PHA' not found for element: {}".format(elem.name))
            phase =  settings[elem.name]["PHA"]
            radius = elem.diameter / 2.0
            if cavity_field_3d:
                lattice.append([elem.length, 48, 20, 110, vscale, elem.frequency, phase, _file_id(elem.beta), radius, radius, 0, 0, 0, 0, 0, 1, 2 ])
            else:
                lattice.append([elem.length, 60, 20, 103, vscale, elem.frequency, phase, _file_id(elem.beta), radius])

        elif isinstance(elem, mag.SolElement):
            if elem.name not in settings:
                raise Exception("settings not found for element: {}".format(elem.name))
            if "B" not in settings[elem.name]:
                raise Exception("setting: 'B' not found for element: {}".format(elem.name))
            field = settings[elem.name]["B"]
            lattice.append([elem.length/2.0, 1, 20, 3, field, 0.0, elem.diameter/2.0])
            lattice.append([0.0, 0, 0, -21, elem.diameter/2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            lattice.append([elem.length/2.0, 1, 20, 3, field, 0.0, elem.diameter/2.0])

        elif isinstance(elem, mag.QuadElement):
            if elem.name not in settings:
                raise Exception("settings not found for element: {}".format(elem.name))
            if "B" not in settings[elem.name]:
                raise Exception("setting: 'B' not found for element: {}".format(elem.name))
            field = settings[elem.name]["B"]
            lattice.append([elem.length, 50, 20, 1, field, 0.0, elem.diameter/2.0])

        elif isinstance(elem, mag.CorrElement):
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
            

    # compact lattice by merging drifts
    clattice = []
    for line in lattice:
        if (line[3] == 0) and (len(clattice) > 0) and (clattice[-1][3] == 0):
            clattice[-1][0] += line[0]
        else:
            clattice.append(line)

    print("""10 1
6 20642 2 0 2
65 65 129 4 0.140000 0.140000 0.1025446
19 0 0 2
10111 10531
0.0 0.0
1.48852718947e-10 1.533634074e-10
0.22734189E-02  0.88312578E-04  0.00000000E+00  1.000  1.000  0.000  0.000
0.22734189E-02  0.88312578E-04  0.00000000E+00  1.000  1.000  0.000  0.000
0.76704772E-01  0.34741445E-05  0.00000000E+00  1.000  1.000  0.000  0.000
0.0 0.5e6 931.49432e6 0.1386554621848 80.50e6 0.0 99.9""")

    with open("result_map.txt", "w") as f:
        for name in result_map:
            print(name,file=f)


    for line in clattice:
        #line.append("/")
        for rec in line:
            if isinstance(rec, int):
                sys.stdout.write("{:d} ".format(rec))
            elif isinstance(rec, float):
                sys.stdout.write("{:.7E} ".format(rec))
        sys.stdout.write("/\r\n")

        #print(*line)
        #for param in line:

        
def _file_id(n):
    if n > 0.0:
        while n < 100.0:
            n *= 10
        return int(n)
    else:
        raise Exception("Cannot generate file id from '{}'".format(n))
  
