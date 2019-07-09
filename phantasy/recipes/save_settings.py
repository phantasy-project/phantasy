#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import json
import time

from phantasy.library.operation import MachinePortal


def init_mp(machine, segments=None, **kws):
    """Load *segments* of *machine*, if *segments* is None, all the defined
    segments will be loaded, to generate a MachinePortal instance.

    Parameters
    ----------
    machine : str
        Machine name.
    segments : list[str]
        List of lattice names to load.

    Keyword Arguments
    -----------------
    wait : float
        If set, wait *wait* seconds after mp initialization.

    Returns
    -------
    o :
        MachinePortal instance.
    """
    mp = MachinePortal(machine)
    segs = mp.get_all_segment_names() if segments is None else segments
    for seg in segs:
        mp.load_lattice(seg)
    t = kws.get('wait', None)
    if t is not None:
        print("Sleep {} secs...".format(t))
        time.sleep(t)
    return mp


def save_all_settings(filepath=None, segments=["LEBT", "MEBT"], machine="FRIB",
                      **kws):
    """Save all physics and engineering settings for all the elements defined
    in each one of *segments* of *machine* to JSON file *filepath*,
    additional information could be embedded by key-value pairs excluding
    the kws defined in the folloing Keyword Arguments section.

    Parameters
    ----------
    filepath : str
        File path for the JSON file to save data, if defined.
    segments : list[str]
        List of segments.
    machine : str
        Machine name.

    Keyword Arguments
    -----------------
    mp : obj
        MachinePortal instance, created from `init_mp` function, if not given,
        additional kws will be passed to `init_mp` function.

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
    if 'mp' in kws:
        mp = kws.pop('mp')
    else:
        mp = init_mp(machine, segments, **kws)

    settings = OrderedDict()
    for seg in segments:
        lat = mp.lattices.get(seg)
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

    settings.update(**{k:v for k,v in kws.items() if k not in ["wait",]})
    if filepath is not None:
        with open(filepath, 'w') as f:
            json.dump(settings, f, indent=2)

    return settings


if __name__ == "__main__":
    from phantasy.recipes import save_all_settings
    import time

    save_all_settings("/tmp/all-settings.json", segments=["LINAC"],
                      machine="VA_LS1FS1", timestamp=time.time())
