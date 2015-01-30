# encoding: UTF-8

"""
Element
-------

The base class is Element



"""

from __future__ import print_function




class Settings(object)
    """
    Settings is a simple object to contain setting names.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(key, value)


    def __str__(self):
        return str(self.__dict__)


class BaseElement(object):
    """
    BaseElement is the base for the ADD class heirarchy.
    """
    def __init__(self, length, diameter, desc=""):
        self.desc = desc
        self.length = length
        self.diameter = diameter
        self.settings = Settings()


    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if not isinstance(length, (int, float)):
            raise TypeError("BaseElement: 'length' property must be type a number")
        self._length = length


    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter):
        if not isinstance(diameter, (int, float)):
            raise TypeError("BaseElement: 'diameter' property must be a number")    
        self._diameter = diameter


    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        if not isinstance(desc, basestring):
            raise TypeError("BaseElement: 'desc' property must be a string")
        self._desc = desc


    def __str__(self):
        s = "{{ desc:'{.desc}', length:{.length}, diameter:{.diameter}, settings:{.settings} }}"
        return type(self).__name__ + s.format(self)


class NamedElement(BaseElement):
    """
    NamedElement represents a named accelerator component.
    """
    def __init__(self, length, diameter, name, desc=""):
        super(NamedElement, self).__init__(length, diameter, desc=desc)
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, basestring):
            raise TypeError("NamedElement: 'name' property must be a string")
        if len(name) == 0:
            raise ValueError("NamedElement: 'name' property must not be empty")
        self._name = name


    def __str__(self):
        s = "{{ name:'{.name}', desc:'{.desc}', length:{.length}, diamter:{.diameter}, settings:{.settings} }}"
        return type(self).__name__ + s.format(self)



class Element(NamedElement):
    """
    Element represents an accelerator component with a standard
    name based on system, subsystem, device and instance.
    """
    def __init__(self, length, diameter, name, desc="", system="", subsystem="", device="", dtype="",):
        super(Element, self).__init__(length, diameter, name, desc=desc)
        self.system = system
        self.subsystem = subsystem
        self.device = device
        self.dtype = dtype

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system):
        if not isinstance(system, basestring):
            raise TypeError("Element: 'system' property must be a string")
        self._system = system


    @property
    def subsystem(self):
        return self._subsystem

    @subsystem.setter
    def subsystem(self, subsystem):
        if not isinstance(subsystem, basestring):
            raise TypeError("Element: 'subsystem' property must be a string")
        self._subsystem = subsystem


    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, device):
        if not isinstance(device, basestring):
            raise TypeError("Element: 'device' property must be a string")
        self._device = device


    @property
    def dtype(self):
        return self._dtype

    @dtype.setter
    def dtype(self, dtype):
        if not isinstance(dtype, basestring):
            raise TypeError("Element: 'dtype' property must be a string")
        self._dtype = dtype


    def __str__(self):
        s = "{{ name:'{.name}', desc:'{.desc}', length:{.length}, diamter:{.diameter}, system:'{.system}', " + \
                "subsystem:'{.subsystem}', device:'{.device}', dtype:'{.dtype}', settings:{.settings} }}"
        return type(self).__name__ + s.format(self)
