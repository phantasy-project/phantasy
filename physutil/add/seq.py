# encoding: UTF-8

"""
Implement physutil command 'impact-input'.
"""

from __future__ import print_function

import sys

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


    def print_details(self, indent=2, file=sys.stdout):
        level = 0
        iterators = [ iter(self.elements) ]

        while len(iterators) > 0:
            it = iterators[-1]
            try:
                elem = it.next()
            except StopIteration:
                del iterators[-1]
                level -= 1
                continue

            print(" "*(indent*level) + str(elem), file=file)

            if isinstance(elem, SeqElement):
                iterators.append(iter(elem.elements))
                level += 1
                continue


    def __iter__(self):
        return _SeqElementIterator(self)


    def iter(self, start=None, end=None):
        return _SeqElementIterator(self, start, end)


    def __str__(self):
        s = "{{ name:'{elem.name}', desc:'{elem.desc}', nelements:{nelements} }}"
        return type(self).__name__ + s.format(elem=self, nelements=len(self.elements))



class _SeqElementIterator(object):
    """
    Deep iterator for SeqElements.
    """
    def __init__(self, seq, start=None, end=None):
        self._iterators = [ iter(seq.elements) ]
        self._start = start
        self._end = end if end != None else start


    def __iter__(self):
        return self


    def next(self):
        while len(self._iterators) > 0:
            it = self._iterators[-1]
            try:
                elem = it.next()
            except StopIteration:
                del self._iterators[-1]
                continue

            if self._start != None:
                if self._start == elem.name:
                    self._start = None

            if self._end != None:
                if self._end == elem.name:
                    self._iterators = []
                    self._end = None
                    
            if isinstance(elem, SeqElement):
                self._iterators.append(iter(elem))
                continue

            if self._start == None:
                return elem

        raise StopIteration()
