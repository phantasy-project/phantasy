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
        self.beta = 0.0
        self.voltage = 0.0
        self.frequency = 0.0


    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, beta):
        if not isinstance(beta, (int, float)):
            raise TypeError("CavityElement: 'beta' property must be type a number")
        self._beta = beta

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        if not isinstance(voltage, (int, float)):
            raise TypeError("CavityElement: 'voltage' property must be type a number")
        self._voltage = voltage


    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        if not isinstance(frequency, (int, float)):
            raise TypeError("CavityElement: 'frequency' property must be type a number")
        self._frequency = frequency
