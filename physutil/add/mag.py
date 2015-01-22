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


# class DipolElement(Element):
#     """
#     """
#     def __init__(self, length, name="", system="", subsystem="", device="", dtype=""):
#         super(DipoleElement,self).__init__(length, diameter, name, system, subsystem, device, dtype)


# class QuadElement(Element):
#     """
#     """
#     def __init__(self, length, name="", system="", subsystem="", device="", dtype=""):
#         super(QuadrupoleElement,self).__init__(length, diameter, name, system, subsystem, device, dtype)
