# encoding: UTF-8

"""Object model to represent the Accelerator Design Description"""

from __future__ import print_function

from .elem import Element


class CavityElement(Element):
    """
    CavityElement represents a RF cavity.
    """
    def __init__(self, length, diameter, name, desc="cavity", system="", subsystem="", device="", dtype=""):
        super(CavityElement, self).__init__(length, diameter, name, desc=desc, system=system,
        										subsystem=subsystem, device=device, dtype=dtype)
