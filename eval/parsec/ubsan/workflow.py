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
VARIANTS = [2, 3, 4]

def build(wrap, num, prog):
	
	print "Experiment: %s %s %s" % (wrap, num, prog)

	build = False
	ps = subprocess.Popen("./build.sh %s %s %s" % (wrap, num, prog), shell=True, stdout=subprocess.PIPE)
	output = ps.stdout.readlines()

	for line in output:
		if BUILD_SUCCESS in line:
			build = True
			print line.strip()
			break

	if not build:
		print "Build does not seem to be successful, following is the output"
		print output


def run(wrap, num, prog):

	print "Experiment: %s %s %s" % (wrap, num, prog)
	
	time.sleep(3)

	ps = subprocess.Popen("./run.sh %s %s %s" %  (wrap, num, prog), shell=True, stdout=subprocess.PIPE)
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
		build("original", 1, prog)

def run_original():

	for prog in PROGRAMS:
		run("original", 1, prog)	

def build_profile():
	
	for prog in PROGRAMS:
		build("profile", 1, prog)

def run_profile():

	for prog in PROGRAMS:
		run("profile", 1, prog)	

def build_bft():

	for v in VARIANTS:
		for prog in PROGRAMS:
			build("bft", v, prog)

def run_bft():
	
	for v in VARIANTS:
		for prog in PROGRAMS:
			run("bft", v, prog)


if __name__ == "__main__":

	cmd = sys.argv[1]
	cat = sys.argv[2]

	locals()["%s_%s" % (cmd, cat)]()
