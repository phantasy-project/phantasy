# -*- coding: utf-8 -*-

"""Read polarity.
"""
import csv


def readfile(filepath, fmt='csv'):
    with open(filepath, 'r') as f:
        data = csv.reader(f, delimiter=',', skipinitialspace=True)
        next(data)
        r = {i[0]: int(i[1]) for i in data if not i[0].startswith("#")}
    return r
