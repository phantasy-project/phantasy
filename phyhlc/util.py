# encoding: UTF-8

"""Utilities that are used throughout the package.

..moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value
