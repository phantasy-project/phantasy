
import sys, fmdata

"""
Simple script to extract a 'test' data set from a real '.dat' file.
"""

f = open(sys.argv[1], "r")
d = fmdata.readFromDatFile(f)
f.close()

linenums = []
for x in xrange(0, d.nx, 2):
    for y in xrange(0, d.ny, 2):
        for z in xrange(0, d.nz, 6):
            linenums.append(x*d.ny*d.nz + y*d.nz + z)

linenums.sort()

f = open(sys.argv[1], "r")
sys.stdout.write(f.readline())
sys.stdout.write(f.readline())

current = -1
for linenum in linenums:
    while current != linenum:
        line = f.readline()
        current += 1
    sys.stdout.write(line)

f.close()
