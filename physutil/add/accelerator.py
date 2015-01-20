# encoding: UTF-8

"""Object model to represent the Accelerator Design Description"""


class BaseElement(object):
    """
    BaseElement is the base class for all accelerator elements.
    """
    def __init__(self, name=None, length=0.0):
        self.name = name
        self.length = length


class Element(BaseElement):
    """
    Element is the standard accelerator element.
    """
    def __init__(self, system=None, subsystem=None, instance=None, device=None, name=None, length=0.0):
        super(Element, self).__init__(name, length)
        self.system = system
        self.subsystem = system
        self.instance = instance
        self.device = device


class SeqElement(BaseElement):
    """
    SeqElement is a composite element containing a sequence of sub-elements.
    """
    def __init__(self, elements, name=None):
        super(SeqElement, self).__init__(name)
        self.elements = elements


class ValveElement(Element):
    """
    ValveElement represents a vaccuum value or other similar element.
    """
    def __init__(self, system=None, subsystem=None, instance=None, device=None, name=None, length=0.0 ):
        super(ValveElement,self).__init__(system, subsystem, instance, device, name, length)


class DriftElement(BaseElement):
    """
    DriftElement represents a drift tube, drift space, bellows or other passive element.
    """
    def __init__(self, name=None, length=0.0):
        super(DriftElement, self).__iniit__(name, length)


class Accelerator(SeqElement):

    def __init__(self, elements, name=None):
        super(Accelerator, self).__init__(elements, name)
