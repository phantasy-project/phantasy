#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Get all diagnostics devices per type name.
"""

from phantasy.library.operation import MachinePortal


ALL_SEGS = ("LEBT", "MEBT2FS1A", "MEBT2FS1B")


def get_devices_by_type(device_type,
                        segments=ALL_SEGS, machine="FRIB"):
    mp = MachinePortal(machine, segment=segments[0])
    if len(segments) > 1:
        [mp.load_lattice(n) for n in segments[1:]]
    device_names = []
    device_elems = []
    for seg in segments:
        lat = mp.lattices[seg]
        for elem in lat:
            if elem.family == device_type and elem.name not in device_names:
                device_names.append(elem.name)
                device_elems.append(elem)
    return device_names, device_elems



