# -*- coding: utf-8 -*-
"""Read/write policy for PVs. The policy for PV read/write is a
defined function, of which the input parameters are:

* read: `readback_pv` attribute as argument, return a value;
* write: `setpoint_pv` attribute and new value(s) as arguments;

`readback_pv` and `setpoint_pv` are both instantiated from `epics.PV`,
the value of PV could be reached by `.value`, while setting new value by
`.put()` method.

All input PV parameters are list type, while value for writing is a scalar.
"""

# Default policy for all PVs except those defined by other policies.
#   Read: return the average reading of all readback PVs.
#   Write: set all setpoint PVs with the same value defined by *v*.


def _default_read_policy(x):
    if len(x) == 1:
        return _get_value(x[0])
    else:
        try:
            return sum(_get_value(x) for i in x)/len(x)
        except:
            return _get_value(x[0])


def _default_write_policy(x, v, **kws):
    for i in x:
        i.put(v, **kws)

# _default_read_policy = lambda x: sum([i.value for i in x])/len(x)
# _default_write_policy = lambda x,v: [i.put(v) for i in x]


# Policy for horizontal focusing equad
# Signs: PSQ1(-), PSQ2(+), Value(+)
#   Read: return the average reading for all readback PVs, the final sign
#         depends on the one of `Value` (here is `+`)
#   Write: set PSQ1: -Value, PSQ2: Value

# Policy for vertical focusing equad
# Signs: PSQ1(+), PSQ2(-), Value(-)
#   Read: return the average reading for all readback PVs, the final sign
#         depends on the one of `Value` (here is `-`)
#   Write: set PSQ1: -Value, PSQ2: Value

def _equad_read_policy(x):
    return 0.5 * (-_get_value(x[0]) + _get_value(x[1]))

def _equad_write_policy(x, v, **kws):
    x[0].put(-v, **kws)
    x[1].put(v, **kws)


# Policy for ebend
# Signs: PSD1(+), PSD2(-), Value(-)

def _ebend_read_policy(x):
    return 0.5 * (-_get_value(x[0]) + _get_value(x[1]))


def _ebend_write_policy(x, v, **kws):
    x[0].put(-v, **kws)
    x[1].put(v, **kws)


#
PV_POLICIES = {
        "DEFAULT": {
            "read": _default_read_policy,
            "write": _default_write_policy,
        },
        "EQUAD": {
            "read": _equad_read_policy,
            "write": _equad_write_policy,
        },
        "EBEND": {
            "read": _ebend_read_policy,
            "write": _ebend_write_policy,
        },
}

def _get_value(pv):
    if pv.auto_monitor:
        return pv.value
    else:
        return pv.get()
