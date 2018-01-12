#!/usr/bin/env python

import os
import sys
import time
import numpy
import subprocess

def parse_report(report, prog):

	data = []
	
	with open(report) as f:
		content = f.readlines()

		section = False
		for line in content:
			if line.startswith("--------------"):
				section = True
				continue

			if section and prog in line:
				data.append(float(line.strip().split()[2]))
			
			if line.startswith("=============="):
				section = False
				break

	return str(data[0])					


def parse_log(log):

	with open(log) as f:
		content = f.readlines()

		prog = None
                conf = None
		for line in content:
                        line = line.strip()
                        tokens = line.split()
		        if "Experiment" in line:
                            if "," in line:
                                conf = tokens[1][:-1]
                                prog = tokens[4]
                            else:
				prog = tokens[3]
			elif " -> " in line:
				report = line.strip().split(" -> ")[1]
				data = parse_report(report, prog)
			
                                if conf is None:
                                    print "%10s: %s" % (prog, data)
                                else:
                                    print "%10s: %25s: %s" % (prog, conf, data)


if __name__ == "__main__":
	
	log = sys.argv[1]
	parse_log(log)
