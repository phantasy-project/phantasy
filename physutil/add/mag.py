# encoding: UTF-8

"""Object model to represent the Accelerator Design Description"""

from __future__ import print_function

from .elem import Element


class SolElement(Element):
    """
    SolenoidElement represents a solenoid magnet
    """
    def __init__(self, length, diameter, name, desc="solenoid", system="", subsystem="", device="", dtype=""):
        super(SolElement, self).__init__(length, diameter, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype)



class BendElement(Element):
    """
    """
    def __init__(self, length, diameter, name, desc="bend magnet", system="", subsystem="", device="", dtype=""):
        super(BendElement, self).__init__(length, diameter, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype)


class CorrElement(Element):
    """
    """
    def __init__(self, length, diameter, name, desc="corrector magnet", system="", subsystem="", device="", dtype=""):
        super(CorrElement, self).__init__(length, diameter, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype)


class QuadElement(Element):
    """
    """
    def __init__(self, length, diameter, name, desc="quadrupole magnet", system="", subsystem="", device="", dtype=""):
        super(QuadElement, self).__init__(length, diameter, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype)


class HexElement(Element):
    """
    """
    def __init__(self, length, diameter, name, desc="hexapole magnet", system="", subsystem="", device="", dtype=""):
        super(HexElement, self).__init__(length, diameter, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype)
