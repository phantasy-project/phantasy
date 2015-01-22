# encoding: UTF-8

"""Diagnostic elements of the Accelerator Design Description"""

from __future__ import print_function

from .elem import Element


class BLMElement(Element):
    """
    BLMElement represents Beam Loss Monitor diagnostic device.
    """
    def __init__(self, length, diameter, name, desc="beam loss monitor", system="", subsystem="", device="", dtype=""):
        super(BLMElement, self).__init__(length, diameter, name, desc=desc, system=system,
                                            subsystem=subsystem, device=device, dtype=dtype)


class BPMElement(Element):
    """
    BPMElement represents Beam Position Monitor diagnostic device.
    """
    def __init__(self, length, diameter, name, desc="beam positon monitor", system="", subsystem="", device="", dtype=""):
        super(BPMElement,self).__init__(length, diameter, name, desc=desc, system=system,
                                            subsystem=subsystem, device=device, dtype=dtype)


class BLElement(Element):
    """
    BLElement represents Bunch Length Monitor diagnostic device.
    """
    def __init__(self, length, diameter, name, desc="bunch length monitor", system="", subsystem="", device="", dtype=""):
        super(BLElement, self).__init__(length, diameter, name, desc=desc, system=system,
                                             subsystem=subsystem, device=device, dtype=dtype)


class PMElement(Element):
    """
    PMElement represents Beam Profile Monitor diagnostic device.
    """
    def __init__(self, length, diameter, name, desc="beam profile monitor", system="", subsystem="", device="", dtype=""):
        super(PMElement, self).__init__(length, diameter, name, desc=desc, system=system,
                                             subsystem=subsystem, device=device, dtype=dtype)
