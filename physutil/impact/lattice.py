# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

from __future__ import print_function

import sys

from ..add import pasv, diag, mag, rf, accel


def write_lattice(add, steps=20, mapsteps=20):

    if not isinstance(add, accel.Accelerator):
        raise TypeError("Expecting type Accelerator")

    for elem in add.elements:
        if elem.name == "LS1":
            LS1 = elem
            break
    else:
        raise Exception("Subsequence not found 'LS1'")

    for elem in LS1.elements:
        if elem.name == "CA01":
            CA01 = elem
            break
    else:
        raise Exception("Subsequence not found 'CA01'")    

    settings = {
        "LS1_CA01:CAV1_D1127":{ "voltage":0.6400, "phase":-0.652400000E+01 },
        "LS1_CA01:SOL1_D1131":{ "field":0.534000E+01 },
        "LS1_CA01:CAV2_D1135":{ "voltage":0.7000, "phase":+0.329788000E+03 },
        "LS1_CA01:CAV3_D1143":{ "voltage":0.7600, "phase":0.602740000E+02 },
        "LS1_CA01:SOL2_D1147":{ "field":0.590000E+01 },
        "LS1_CA01:CAV4_D1150":{ "voltage":0.82000, "phase":0.258148000E+03 }
    }

    lattice = []

    result_map = []

    for elem in CA01:
        if isinstance(elem, pasv.DriftElement):
            lattice.append([elem.length, steps, mapsteps, 0, elem.diameter/2.0])

        elif isinstance(elem, pasv.ValveElement):
            lattice.append([elem.length, steps, mapsteps, 0, elem.diameter/2.0])

        elif isinstance(elem, pasv.PortElement):
            lattice.append([elem.length, steps, mapsteps, 0, elem.diameter/2.0])

        elif isinstance(elem, rf.CavityElement):
            if elem.name not in settings:
                raise Exception("settings not found for element: {}".format(elem.name))
            if "voltage" not in settings[elem.name]:
                raise Exception("setting: 'voltage' not found for element: {}".format(elem.name))
            vscale =  settings[elem.name]["voltage"] / elem.voltage
            if "phase" not in settings[elem.name]:
                raise Exception("setting: 'phase' not found for element: {}".format(elem.name))
            phase =  settings[elem.name]["phase"]
            radius = elem.diameter / 2.0
            lattice.append([elem.length, steps, mapsteps, 110, vscale, elem.frequency, phase, _file_id(elem.beta), radius, radius, 0, 0, 0, 0, 0, 1, 2 ])

        elif isinstance(elem, mag.SolElement):
            if elem.name not in settings:
                raise Exception("settings not found for element: {}".format(elem.name))
            if "field" not in settings[elem.name]:
                raise Exception("setting: 'field' not found for element: {}".format(elem.name))
            field = settings[elem.name]["field"]
            lattice.append([elem.length, steps, mapsteps, 3, field, 0.0, elem.diameter/2.0])

        elif isinstance(elem, diag.BLMElement):
            pass # ignore Beam Loss Monitor

        elif isinstance(elem, diag.BLElement):
            pass # ignore Bunch Length Monitor

        elif isinstance(elem, diag.PMElement):
            pass # ignore Beam Profile Monitor

        elif isinstance(elem, diag.BPMElement):
            lattice.append([elem.length, 0, 0, -23])
            result_map.append(elem.name)
            
        else:
            #raise Exception("Unsupport ADD element: {}".format(elem))
            print("Unsupported ADD element: {}".format(elem), file=sys.stderr)
            break
            

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
        line.append("/")
        print(*line)
        #for param in line:

        
def _file_id(n):
    if n > 0.0:
        while n < 100.0:
            n *= 10
        return int(n)
    else:
        raise Exception("Cannot generate file id from '{}'".format(n))
  
