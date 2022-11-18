#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import os
import sys
from phantasy.library.pv import fetch_data


@click.command(no_args_is_help=True)
@click.option('--pv',
              '-p',
              required=True,
              type=str,
              help="A string of PV name, multiple definition for a list.",
              multiple=True)
@click.option(
    '--time-span',
    '-t',
    required=True,
    type=float,
    help="The total time period for fetching data, in second, defaults to 5.0."
)
@click.option(
    '--abs-z',
    '-z',
    required=False,
    type=float,
    help=
    "The absolute value of z-score, drop the data beyond, defaults to None, meaing no data filtering."
)
@click.option('--with-no-data',
              is_flag=True,
              default=False,
              help="Do not return the fetched data table after filtering.")
@click.option(
    '--output',
    type=str,
    help=
    "Write fetched data table to a CSV file, ignore when --with-no-data is set."
)
@click.option('--verbose-off',
              is_flag=True,
              default=False,
              help="Turn off the log messages.")
def run(pv, time_span, abs_z, with_no_data, output, verbose_off):
    """Fetch the readback data from a list of given PVs in the given time period in seconds,
    trim the data beyond the given z-score (absolute value), and return the data of interest:
    average readings, and the data table if the option is set accordingly.
    """
    avg, df = fetch_data(pv, time_span, abs_z, not with_no_data,
                         not verbose_off)
    _s = f"Average readings for each PV in the past {time_span} seconds:"
    print(_s)
    print("-" * len(_s))
    for i, (ipv, iavg) in enumerate(zip(pv, avg)):
        print(f"[{i+1}] {ipv:<30s} : {iavg:>.6g}")
    print("-" * len(_s))
    if df is not None:
        if output is None:
            click.secho(
                "Print out the data to the screen, define --output to write into a CSV file.",
                fg="red")
            try:
                print(df.to_string())
                sys.stdout.flush()
            except BrokenPipeError:
                devnull = os.open(os.devnull, os.O_WRONLY)
                os.dup2(devnull, sys.stdout.fileno())
                sys.exit(1)
        else:
            click.secho(f"Write the data into {output}", fg="blue")
            df.to_csv(output)
