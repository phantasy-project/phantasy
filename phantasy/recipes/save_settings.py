#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import copy
import json

from phantasy.library.operation import MachinePortal


def save_all_settings(filepath, segments=["LEBT", "MEBT"], machine="FRIB",
                      **kws):
    """Save all physics and engineering settings for all the elements defined
    in each one of *segments* of *machine* to JSON file *filepath*,
    additional information could be embedded by key-value pairs.

    Parameters
    ----------
    filepath : str
        File path for the JSON file to save data.
    segments : list[str]
        List of segments.
    machine : str
        Machine name.

    Examples
    --------
    >>> from phantasy.recipes import save_all_settings
    >>> import time
    >>>
    >>> filepath = "/tmp/all-settings.json"
    >>> save_all_settings(filepath, segments=["LINAC"],
    >>>                   machine="VA_LS1FS1",
    >>>                   timestamp=time.time())
    >>>

    Returns
    -------
    r : OrderedDict
        All settings.
    """
    settings = OrderedDict()
    for seg in segments:
        mp = MachinePortal(machine=machine, segment=seg)
        lat = mp.work_lattice_conf
        lat.sync_settings(data_source='control')
        settings.update(lat.settings)

        for elem_name, elem_phy_conf in lat.settings.items():
            elem = lat[elem_name]
            if elem is None: continue
            for phy_fld_name in set(elem_phy_conf).intersection(elem.get_phy_fields()):
                eng_fields = elem.get_eng_fields()
                if len(eng_fields) == 1:
                    v = elem.convert(field=phy_fld_name, value=elem_phy_conf[phy_fld_name])
                    settings[elem_name].update({eng_fields[0]: v})

    settings.update(**kws)
    with open(filepath, 'w') as f:
        json.dump(settings, f, indent=2)

    return settings


if __name__ == "__main__":
    from phantasy.recipes import save_all_settings
    import time

    save_all_settings("/tmp/all-settings.json", segments=["LINAC"],
                      machine="VA_LS1FS1", timestamp=time.time())
