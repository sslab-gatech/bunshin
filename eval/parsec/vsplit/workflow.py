#!/usr/bin/env python

import os
import sys
import time
import numpy
import subprocess

BUILD_SUCCESS = "[PARSEC] Done."
RUN_SUCCESS1 = "[PARSEC] Done."
RUN_SUCCESS2 = "[mvee] execution completed"

PROGRAMS = ["barnes", "fmm", "ocean_cp", "ocean_ncp", "radix", "radiosity", "volrend", 
"water_nsquared", "water_spatial", "cholesky", "fft", "lu_cb", "lu_ncb"]
SANITIZERS = ["alignment", "bool", "bounds", "enum", "float-cast-overflow",
        "float-divide-by-zero", "function", "integer-divide-by-zero",
        "nonnull-attribute", "null", "object-size", "return",
        "returns-nonnull-attribute", "signed-integer-overflow",
        "unsigned-integer-overflow", "unreachable", "vla-bound", "vptr"]
VARIANTS = [2, 3, 4]

def build(san, wrap, num, prog):
	
	print "Experiment: %s %s %s %s" % (san, wrap, num, prog)

	build = False
	ps = subprocess.Popen("./build.sh %s %s %s %s" % (san, wrap, num, prog), shell=True, stdout=subprocess.PIPE)
	output = ps.stdout.readlines()

	for line in output:
		if BUILD_SUCCESS in line:
			build = True
			print line.strip()
			break

	if not build:
		print "Build does not seem to be successful, following is the output"
		print output


def run(san, wrap, num, prog):

	print "Experiment: %s %s %s %s" % (san, wrap, num, prog)
	
	time.sleep(3)

	ps = subprocess.Popen("./run.sh %s %s %s %s" %  (san, wrap, num, prog), shell=True, stdout=subprocess.PIPE)
	output = ps.stdout.readlines()

	run = False 
	for line in output:
		if RUN_SUCCESS1 in line or RUN_SUCCESS2 in line:
			run = True
			print line.strip()
			break

	if not run:
		print "Run does not seem to be successful, following is the output"
		print output


def build_original():
	
	for prog in PROGRAMS:
            for san in SANITIZERS:
		build(san, "original", 1, prog)

def run_original():

	for prog in PROGRAMS:
            for san in SANITIZERS:
		run(san, "original", 1, prog)	

def build_profile():
	
	for prog in PROGRAMS:
            for san in SANITIZERS:
		build(san, "profile", 1, prog)

def run_profile():

	for prog in PROGRAMS:
            for san in SANITIZERS:
		run(san, "profile", 1, prog)	

def build_bft():

	for v in VARIANTS:
		for prog in PROGRAMS:
                    for san in SANITIZERS:
			build(san, "bft", v, prog)

def run_bft():
	
	for v in VARIANTS:
		for prog in PROGRAMS:
                    for san in SANITIZERS:
			run(san, "bft", v, prog)


if __name__ == "__main__":

	cmd = sys.argv[1]
	cat = sys.argv[2]

	locals()["%s_%s" % (cmd, cat)]()
