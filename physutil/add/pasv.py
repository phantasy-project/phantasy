# encoding: UTF-8

"""Object model to represent the Accelerator Design Description"""

from __future__ import print_function

from .elem import Element
from .elem import BaseElement




class DriftElement(BaseElement):
    """
    DriftElement represents a drift tube, drift space, bellows or other passive element.
    """
    def __init__(self, length, diameter, desc="drift"):
        super(DriftElement, self).__init__(length, diameter, desc=desc)


class ValveElement(Element):
    """
    ValveElement represents a vaccuum valve or other similar valve.
    """
    def __init__(self, length, diameter, name, desc="valve", system="", subsystem="", device="", dtype=""):
        super(ValveElement, self).__init__(length, diameter, name, desc=desc, system=system,
                                            subsystem=subsystem, device=device, dtype=dtype)


class PortElement(Element):
    """
    PortElement represents a attachment point for pump or other device.
    """
    def __init__(self, length, diameter, name, desc="port", system="", subsystem="", device="", dtype=""):
        super(PortElement, self).__init__(length, diameter, name, desc=desc, system=system,
                                            subsystem=subsystem, device=device, dtype=dtype)
