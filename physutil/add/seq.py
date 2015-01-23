# encoding: UTF-8

"""
Implement physutil command 'impact-input'.
"""

from __future__ import print_function


from .elem import NamedElement


class SeqElement(NamedElement):
    """
    SeqElement is a composite element containing a sequence of sub-elements.
    """
    def __init__(self, elements, name="", desc=""):
        super(SeqElement, self).__init__(None, None, name, desc)
        self.elements = elements


    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        self._elements = list(elements)


    @property
    def length(self):
        length = 0.0
        for elem in self.elements:
            length += elem.length
        return length

    @length.setter
    def length(self, length):
        if length != None:
            raise NotImplementedError("SeqElement: Setting length not implemented")


    @property
    def diameter(self):
        diameter = float('inf')
        for elem in self.elements:
            diameter = min(diameter, elem.diameter)
        return diameter

    @diameter.setter
    def diameter(self, diameter):
        if diameter != None:
            raise NotImplementedError("SeqElement: Setting diameter not implemented")


    def __iter__(self):
        return _SeqElementIterator(self)


class _SeqElementIterator(object):
    """
    Deep iterator for SeqElements.
    """
    def __init__(self, seq):
        self._iterators = [ iter(seq.elements) ]


    def __iter__(self):
        return self


    def next(self):
        while len(self._iterators) > 0:
            it = self._iterators[-1]
            try:
                elem = it.next()
                if isinstance(elem, SeqElement):
                    self._iterators.append(iter(elem))
                    continue
            
            except StopIteration:
                self._iterators.pop()
                continue

            return elem

        raise StopIteration()
