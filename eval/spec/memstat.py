#!/usr/bin/env python

import os
import sys
import glob

STATDIR = os.path.join(os.getenv("HOME"), "bft-workspace", "memstats", "spec")

PROGRAMS = ["perlbench", "bzip2", "gcc", "mcf", "milc", "namd", "gobmk",
"dealII", "soplex", "povray", "hmmer", "sjeng", "libquantum", "h264ref",
"lbm", "astar", "sphinx3", "xalancbmk"]

def parse_memstat(prog, stage):

    result = None

    for fn in glob.glob("%s/%s-%s-*" % (STATDIR, prog, stage)):
        with open(fn) as f:
            content = f.readlines()
            for line in content:
                if "Maximum resident set size" in line:
                    result = int(line.split(":")[1].strip())

    return result 


if __name__ == "__main__":

    stage = sys.argv[1]

    for prog in PROGRAMS:
        r = parse_memstat(prog, stage)
        print r
