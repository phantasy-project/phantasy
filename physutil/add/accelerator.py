# encoding: UTF-8

"""Object model to represent the Accelerator Design Description"""


class BaseElement(object):
    """
    BaseElement is the base class for all accelerator elements.
    """
    def __init__(self, length=None, name=""):
        if length != None:
            self.length = length
        self.name = name

class SeqElement(BaseElement):
    """
    SeqElement is a composite element containing a sequence of sub-elements.
    """
    def __init__(self, elements, name=""):
        super(SeqElement, self).__init__(None, name)
        self.elements = elements

    @property
    def length(self):
        length = 0.0
        for elem in self.elements:
            length += elem.length
        return length

    def __iter__(self):
        """
        Deep iteration of nested elements.
        """
        stack = list(self.elements)
        stack.reverse()
        elements = []
        while len(stack) > 0:
            elem = stack.pop()
            if isinstance(elem, SeqElement):
                stack.extend(elem.elements)
            else:
                elements.append(elem)
        return elements.__iter__()


class DriftElement(BaseElement):
    """
    DriftElement represents a drift tube, drift space, bellows or other passive element.
    """
    def __init__(self, length, name="drift"):
        super(DriftElement, self).__init__(length, name)


class Element(BaseElement):
    """
    Element is the standard accelerator element.
    """
    def __init__(self, length, name="", system="", subsystem="", device="", instance=""):
        super(Element, self).__init__(length, name)
        self.system = system
        self.subsystem = system
        self.instance = instance
        self.device = device


class BeamLossElement(Element):
    """
    BeamLossElement represents Beam Loss Monitor diagnostic device.
    """
    def __init__(self, length, name="", system="", subsystem="", device="", instance=""):
        super(BeamLossElement,self).__init__(length, name, system, subsystem, device, instance)


class BeamPositionElement(Element):
    """
    BeamPositionElement represents Beam Position Monitor diagnostic device.
    """
    def __init__(self, length, name="", system="", subsystem="", device="", instance=""):
        super(BeamPositionElement,self).__init__(length, name, system, subsystem, device, instance)


class BunchLengthElement(Element):
    """
    BunchLengthElement represents Bunch Length Moinitor diagnostic device.
    """
    def __init__(self, length, name="", system="", subsystem="", device="", instance=""):
        super(BunchLengthElement,self).__init__(length, name, system, subsystem, device, instance)


class ValveElement(Element):
    """
    ValveElement represents a vaccuum value or other similar valve.
    """
    def __init__(self, length, name="", system="", subsystem="", device="", instance=""):
        super(ValveElement,self).__init__(length, name, system, subsystem, device, instance)


class CavityElement(Element):
    """
    CavityElement represents a RF cavity.
    """
    def __init__(self, length, name="", system="", subsystem="", device="", instance=""):
        super(CavityElement,self).__init__(length, name, system, subsystem, device, instance)


class SolenoidElement(Element):
    """
    SolenoidElement represents a solenoid magnet
    """
    def __init__(self, length, name="", system="", subsystem="", device="", instance=""):
        super(SolenoidElement,self).__init__(length, name, system, subsystem, device, instance)


class DipoleElement(Element):
    """
    """
    def __init__(self, length, name="", system="", subsystem="", device="", instance=""):
        super(DipoleElement,self).__init__(length, name, system, subsystem, device, instance)

class QuadrupoleElement(Element):
    """
    """
    def __init__(self, length, name="", system="", subsystem="", device="", instance=""):
        super(QuadrupoleElement,self).__init__(length, name, system, subsystem, device, instance)



class Accelerator(SeqElement):
    """
    Accelerator represents full particle accelerator.
    """
    def __init__(self, elements, name=""):
        super(Accelerator, self).__init__(elements, name)
