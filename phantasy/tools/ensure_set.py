#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from phantasy.library.pv import ensure_set


@click.command(no_args_is_help=True)
@click.option('--set-pv', '-s', required=True, type=str,
              help="A setpoint PV, multiple definition for a list.",
              multiple=True)
@click.option('--value', '-v', required=True, type=float,
              help="A value of goal to set, multiple definition for a list, if only single one value is define, apply all set PVs with the same value.",
              multiple=True)
@click.option('--read-pv', '-r', required=False, type=str,
              help="A readback PV, multiple definition for a list.",
              multiple=True)
@click.option('--tol', '-t', required=False, type=float,
              help="A tolerance value of the discrepancy between read and set, multiple definition for a list, if only single one value is define, apply all tolerances with the same value, defaults to 0.01.",
              multiple=True)
@click.option('--timeout', '-m', required=False, type=float, default=10.0,
              help="Max allowed time in seconds for the whole procedure, defaults to 10.0.")
@click.option('--verbose-off', is_flag=True, default=False,
              help="Turn off the log messages.")
def run(set_pv, value, read_pv, tol, timeout, verbose_off):
    """Perform ensure CA device set operation against the given setpoint PV(s) and monitor
    the readback PV(s) reaching the goal(s) when the value discrepancy between read and set
    within the range defined by the given tolerance(s), all these actions should be finished
    or terminated in the max allowed seconds defined by timeout.

    Please note: when passing a list of PVs, the size of *setpoint_pv*, *readback_pv*, *goal*
    and *tol* parameters must be the same, while if goal and tol is defined as a single float
    number, they will be expanded to a list of that value for convenience.

    The default tolerance is 0.01, and default timeout is 10.0.

    Pass multiple times of the argument option to define a list of variables, e.g. '--set-pv sp1
    --set-pv sp2' defines a list of setpoint PVs with '[sp1, sp2]', the same applies to '-v', '-r',
    and '-t' options.
    """
    # total length of all setpoint PVs
    nsize = len(set_pv)

    # read PVs
    if read_pv == tuple():
        click.secho(f"Empty read-pv, use set-pv instead", fg='red')
        read_pv = set_pv

    # set values
    if len(value) == 1:
        value = [value[0]] * nsize

    # tolerance
    if len(tol) == 0:
        tol = [0.01] * nsize
    elif len(tol) == 1:
        tol = [tol[0]] * nsize

    ensure_set(set_pv, read_pv, value, tol, timeout, not verbose_off)


if __name__ == '__main__':
    run()
