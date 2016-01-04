import sys

"""
This is not actually what you should do but is a nice template
if you'd like to use it for your programs in Lab 2.
"""

usage = 'Usage: test.py <inputfile>\n'
if len(sys.argv) == 2:
    try:
        infile = open(sys.argv[1], 'r')
    except IOError:
        sys.stderr.write('Input file does not exist.\n')
        sys.stderr.write(usage)
        sys.exit(-1)
else:
    sys.stderr.write(usage)
    sys.exit(-1)





