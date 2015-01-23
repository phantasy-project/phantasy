# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

from __future__ import print_function

import sys

from ..add import pasv, diag, mag, rf, accel


def write_lattice(add, steps=20, mapsteps=20):

    if not isinstance(add, accel.Accelerator):
        raise TypeError("Expecting type Accelerator")

    lattice = []

    for elem in add:
        if isinstance(elem, pasv.DriftElement):
            lattice.append([elem.length, steps, mapsteps, 0, elem.diameter])

        elif isinstance(elem, pasv.ValveElement):
            lattice.append([elem.length, steps, mapsteps, 0, elem.diameter])

        elif isinstance(elem, pasv.PortElement):
            lattice.append([elem.length, steps, mapsteps, 0, elem.diameter])

        elif isinstance(elem, rf.CavityElement):
            lattice.append([elem.length, steps, mapsteps, 110, 0.64, 80.5e6, 421, 0.017, 0.017, 0, 0, 0, 0, 0, 1, 2 ])

        elif isinstance(elem, mag.SolElement):
            lattice.append([elem.length, steps, mapsteps, 3, 0.534e1, 0.0, 0.2e-1])

        elif isinstance(elem, diag.BLMElement):
            pass # ignore Beam Loss Monitor

        elif isinstance(elem, diag.BLElement):
            pass # ignore Bunch Length Monitor

        elif isinstance(elem, diag.PMElement):
            pass # ignore Beam Profile Monitor

        elif isinstance(elem, diag.BPMElement):
            lattice.append([elem.length, 0, 0, -27])
            
        else:
            #raise Exception("Unsupport ADD element: {}".format(elem))
            print("Unsupported ADD element: {}".format(elem), file=sys.stderr)
            break
            

    # compact lattice by merging drifts
    #clattice = []
    #for line in lattice:
    #    if (line[3] == 0) and (len(clattice) > 0) and (clattice[-1][3] == 0):
    #        clattice[-1][0] += line[0]
    #    else:
    #        clattice.append(line)

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


    for line in lattice:
        print(*line)
        #for param in line:

        
