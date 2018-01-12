#!/usr/bin/env python

import os
import sys
import time
import numpy
import subprocess

BUILD_SUCCESS = "Build successes:"
RUN_SUCCESS = "format: ASCII"

PROGRAMS = ["perlbench", "bzip2", "gcc", "mcf", "milc", "namd", "gobmk",
"dealII", "soplex", "povray", "hmmer", "sjeng", "libquantum", "h264ref",
"lbm", "astar", "sphinx3", "xalancbmk"]
CONFS = ["p2-1", "p2-2"]

def build(conf, wrap, num, prog):
	
	print "Experiment: %s %s %s %s" % (conf, wrap, num, prog)

	build = False
	ps = subprocess.Popen("./build.sh %s %s %s %s" % (conf, wrap, num, prog), shell=True, stdout=subprocess.PIPE)
	output = ps.stdout.readlines()

	for line in output:
		if BUILD_SUCCESS in line:
			build = True
			print line.strip()
			break

	if not build:
		print "Build does not seem to be successful, following is the output"
		print output


def run(conf, wrap, num, prog):

	print "Experiment: %s, %s %s %s" % (conf, wrap, num, prog)
	
	time.sleep(3)

	ps = subprocess.Popen("./run.sh %s %s %s %s" %  (conf, wrap, num, prog), shell=True, stdout=subprocess.PIPE)
	output = ps.stdout.readlines()

	run = False 
	for line in output:
		if RUN_SUCCESS in line:
			run = True
			print line.strip()
			break

	if not run:
		print "Run does not seem to be successful, following is the output"
		print output


def build_original():
	
	for prog in PROGRAMS:
            for conf in CONFS:
		build(conf, "original", 1, prog)

def run_original():

	for prog in PROGRAMS:
            for conf in CONFS:
		run(conf, "original", 1, prog)	

def build_memstat():
	
	for prog in PROGRAMS:
            for conf in CONFS:
		build(conf, "memstat", 1, prog)

def run_memstat():

	for prog in PROGRAMS:
            for conf in CONFS:
		run(conf, "memstat", 1, prog)	


if __name__ == "__main__":

	cmd = sys.argv[1]
	cat = sys.argv[2]

	locals()["%s_%s" % (cmd, cat)]()
