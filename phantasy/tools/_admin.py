#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implement phytool command 'admin'.

Execute shell commands followed by 'admin', suppored shell commands are
provided by 'phantasy'

Tong Zhang <zhangt@frib.msu.edu>
2017-01-26 16:22:44 EST
"""

import os
import sys

import argparse

parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]) + " admin",
        description="Admin commands only for development (requires permission)",
        formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("cmd", help="special command name")

parser.epilog = \
"""
Availble commands are:
  cfs_start       : Start channel finder service
  cfs_stop        : Stop channel finder service
  cfs_empty_index : Empty index of channel finder service data
  cfs_build_index : Rebuild index of channel finder service data
  cfs_help        : Help message for channel finder service admin cmds
  cfs_test_push   : Data push test to channel finder service
"""
print_help = parser.print_help

if len(sys.argv) == 2:
    print_help()
    sys.exit(1)

def main():
    args = parser.parse_args(sys.argv[2:])
    
    cmd = args.cmd
    
    import subprocess
    subprocess.call(cmd.split())

    return 0
