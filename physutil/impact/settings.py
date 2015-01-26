# encoding: UTF-8

"""Read an IMPACT input file are extract the accelerator settings using a ADD as a guide."""

from __future__ import print_function

import sys, os.path, json

from ..add import pasv, diag, mag, rf, cs


def write_settings(add, latpath, start="LS1", end=None):

    if not os.path.isfile(latpath):
        raise Exception("settings: IMPACT lattice file not found: {}".format(latpath))

    with open(latpath, "r") as latfile:
        lattice_element = _LatticeIterator(latfile.readlines(), start=11)

    settings = {}

    for elem in add.iter(start, end):

        if isinstance(elem, rf.CavityElement):
            (latidx, latelm) = next(lattice_element)

            if latelm[3] not in [ "103", "110" ]:
                raise Exception("settings: expecting cavity element at line {}, found element: {}".format(latidx+1, latelm))

            if float(latelm[0]) != elem.length:
                raise Exception("settings: expecting cavity element at line {} with length {}: expecting length {}".format(latidx+1, latelm[0], elem.length))

            settings[elem.name] = {}
            settings[elem.name]["AMPL"] = float(latelm[4])
            settings[elem.name]["PHA"] = float(latelm[6])

        elif isinstance(elem, mag.SolElement):
            length = 0.0
            while length < elem.length:
                (latidx, latelm) = next(lattice_element)
                if latelm[3] != "3":
                    raise Exception("settings: expecting solenoid element at line {}, found element: {}".format(latidx+1, latelm))
                length += float(latelm[0])

            if length > elem.length:
                raise Exception("settings: expecting solenoid element at line {} with length {}: expecting length {}".format(latidx+1, latelm[0], elem.length))

            settings[elem.name] = {}
            settings[elem.name]["B"] = float(latelm[4])

        elif isinstance(elem, mag.QuadElement):
            (latidx, latelm) = next(lattice_element)

            if latelm[3] != "1":
                raise Exception("settings: expecting quad element at line {}: found element: {}".format(latidx+1, latelm))
    
            if float(latelm[0]) != elem.length:
                raise Exception("settings: expecting quad element at line {} with length {}: expecting length {}".format(latidx+1, latelm[0], elem.length))

            settings[elem.name] = {}
            settings[elem.name]["B"] = float(latelm[4])                

        elif isinstance(elem, mag.CorrElement):
            pass # ignore for now, there is one is LS1

        elif isinstance(elem, cs.CSElement):
            pass # ignore for now, there is one is LS1

        #elif isinstance(elem, mag.HexElement):
        #    pass

        elif isinstance(elem, (diag.BLMElement, diag.BCMElement, diag.BPMElement, diag.BLElement, diag.PMElement)):
            pass # ignore diagnostic elements

        elif isinstance(elem, (pasv.DriftElement, pasv.ValveElement, pasv.PortElement)):
            pass # ignore passive elements
        
        else:
            raise Exception("settings: unsupported ADD element: {}".format(elem))


    json.dump(settings, sys.stdout, indent=2)



class _LatticeIterator():

    def __init__(self, seq, start=0):
        self._idx = -1
        self._iter = iter(seq)
        self._start = start


    def __iter__(self):
        return self


    def next(self):
        while self._idx < (self._start-1):
            self._iter.next()
            self._idx += 1

        while True:
            line = self._iter.next()
            self._idx += 1
            if line.startswith("!"):
                continue
            elm = line.strip().split()
            if (len(elm) <= 3) or (float(elm[3]) <= 0):
                continue
            return (self._idx, elm)
