# -*- coding: utf-8 -*-
"""Decorators for UNICORN function integration,
only for physics field: elemField_phy, field_phy.
"""

def unicorn_read(fn):
    """Decorator to apply scaling law upon read_policy, the decorated
    function will be the new read_policy (for physics field).

    Parameters
    ----------
    fn :
        Scaling law from engineering to physics, UNICORN function name
        ends with '-P'.

    Examples
    --------
    >>> # 1. define read policy function or already known as `rp`
    >>> # 2. define scaling law function or already known as `fn`
    >>> # 3. create read policy for physics field by:
    >>> @unicorn_read(fn)
    >>> def read_policy(x):
    >>>     return rp(x)
    """
    def decorator(read_policy):
        def f(x):
            return fn(read_policy(x))
        return f
    return decorator


def unicorn_write(fn):
    """Decorator to apply scaling law upon write_policy, the decorated
    function will be the new write_policy (for physics field).

    Parameters
    ----------
    fn :
        Scaling law from physics to engineering, UNICORN function name
        ends with '-N'

    Examples
    --------
    >>> # 1. define write policy function or already known as `wp`
    >>> # 2. define scaling law function or already known as `fn`
    >>> # 3. create write policy for physics field by:
    >>> @unicorn_write(fn)
    >>> def write_policy(x, v, **kws):
    >>>     wp(x, v, **kws)
    """
    def decorator(write_policy):
        def f(x, v, **kws):
            write_policy(x, fn(v), **kws)
        return f
    return decorator


if __name__ == '__main__':
    """class to simulate epics PV.
    """
    class PV(object):
        def __init__(self, name, value=0):
            self.name = name
            self._val = value

        @property
        def value(self):
            return self._val

        def put(self, x):
            self._val = x


    """Note: the following functions: f_read, f_write, fn_p and fn_n are
    preloaded Python object, not defined by the user (however, user has option
    to define new ones.)
    """
    def f_read(x):
        return 0.5 * (-x[0].value + x[1].value)

    def f_write(x, v, **kws):
        x[0].put(-v, **kws)
        x[1].put(v, **kws)

    def fn_p(x):
        """ENG --> PHY
        """
        return 10 * x

    def fn_n(x):
        """PHY --> ENG
        """
        return x / 10.0


    """Note: the following functions: phy_read and phy_write are the new read
    and write policies for physics field, which can be generated from the
    above four function as shown:
    """
    @unicorn_read(fn_p)
    def phy_read(x):
        return f_read(x)

    @unicorn_write(fn_n)
    def phy_write(x, v, **kws):
        f_write(x, v, **kws)


    """Test with PV class
    """
    pv1 = PV('pv1', value=-1.0)
    pv2 = PV('pv2', value=1.0)

    pv = [pv1, pv2]  # the first input parameter of read_policy
    new_value = 2.0  # the second input parameter of write_policy

    assert f_read(pv) == 1.0  # the read value is 1.0
    f_write(pv, new_value)    # change the value to be 2.0
    assert f_read(pv) == 2.0  # confirm value updated to be 2.0

    assert phy_read(pv) == 20.0  # read physics value, is 10 * 2.0 = 20.0
    phy_write(pv, 2.0)           # chage physics value to be 2.0
    assert f_read(pv) == 0.2     # raw value should be 2.0 / 10.0 = 0.2
    assert phy_read(pv) == 2     # confirm physics value: 10 * 0.2 = 2.0
