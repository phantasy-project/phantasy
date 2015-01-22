# encoding: UTF-8

"""
Implement physutil command 'impact-input'.
"""

from __future__ import print_function



class Accelerator(SeqElement):
    """
    Accelerator represents full particle accelerator.
    """
    def __init__(self, elements, name, desc="accelerator"):
        super(Accelerator, self).__init__(elements, name, desc=desc)
