#!/usr/bin/python
# -*- coding: utf-8 -*-

"""softIoc with reccaster support

Tong Zhang <zhangt@frib.msu.edu>
2016-12-07 10:24:05 AM EST
"""

import argparse
import sys
import os
import subprocess


parser = argparse.ArgumentParser(
        description="softIoc with reccaster support",
        formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-d', dest='dbfile', help='db file')
parser.add_argument('-stt', dest='stcmdt', help='st.cmd template file')
parser.add_argument('-st', dest='stcmd', help='st.cmd file to generate')
parser.add_argument('-echo', dest='echo', nargs='?', default=None, 
        const=True, help='if set, do not suppress output message')

parser.epilog = \
"""
Example:
> {n} -d va.db -stt st.cmd -st st_new.cmd
""".format(n=sys.argv[0])

if len(sys.argv) < 3:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args(sys.argv[1:])

if args.dbfile is None:
    parser.print_help()
    sys.exit(1)

db_file, stt_file, st_file = args.dbfile, args.stcmdt, args.stcmd
echo = args.echo

if stt_file is None:
    stt_file = "/home/tong/FRIB/projects/CFS/recsync/client/iocBoot/iocdemo/st_va.cmd"

if st_file is None:
    st_file = 'st_va{0:d}.cmd'.format(os.getpid())

st_fid = open(st_file, 'w')
for line in open(stt_file):
    if "VADB" in line:
        line = line.replace('VADB', db_file)
    st_fid.write(line)
st_fid.close()
os.chmod(st_file, 0o755)

if echo is not None:
    out=sys.stdout
else:
    out=open(os.devnull, 'w')

subprocess.call([st_file], stdout=out)
