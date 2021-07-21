#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Parse alignment data.
"""
import pandas as pd

NAME_MAP = {
    'Name': 'name',
    "Pitch_R1_Deg": "pitch",
    "Roll_R2_Deg": "roll",
    "Yaw_R3_Deg": "yaw",
    "Horz_Off_Meters": "dx",
    "Vert_Off_Meters": "dy",
    "Linear_Off_Meters": "dz",
    "Timestamp": "ts"
}

def read_alignment_data(xlsx_file, **kws):
    """Read device alignment data from *xlsx_file*.

    Parameters
    ----------
    xlsx_file : str
        Path of the alignment data file.

    Returns
    -------
    r : DataFrame
        A dataframe of alignment data indexed by element name.
    """
    df = pd.read_excel(xlsx_file, **kws)
    df.rename(columns=NAME_MAP, inplace=True)
    df.set_index('name', inplace=True)
    return df
