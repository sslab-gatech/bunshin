#!/usr/bin/env python

import os
import re
import sys
import glob
import numpy
import subprocess

PROFDIR = os.path.join(os.getenv("HOME"), "bft-workspace", "log", "spec")
DISTDIR = os.path.join(os.getenv("HOME"), "bft-workspace", "vdist", "spec")
UTIL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "utils.py")


def get_baseline_profile(prog):

    ps = subprocess.Popen("%s %s/%s" % (UTIL, PROFDIR, "base-original"),
        shell=True, stdout=subprocess.PIPE)

    output = ps.stdout.readlines()

    for line in output:
        line = line.strip()
        if prog in line:
            return float(line.split(":")[1].strip())

    return None

def get_total_profile(prog):

    ps = subprocess.Popen("%s %s/%s" % (UTIL, PROFDIR, "ubsan-original"),
        shell=True, stdout=subprocess.PIPE)

    output = ps.stdout.readlines()

    for line in output:
        line = line.strip()
        if prog in line:
            return float(line.split(":")[1].strip())

    return None

def get_sanitizer_profile(prog):
    
    ps = subprocess.Popen("%s %s/%s" % (UTIL, PROFDIR, "vsplit-original"),
        shell=True, stdout=subprocess.PIPE)

    output = ps.stdout.readlines()

    data = dict()

    for line in output:
        line = line.strip()
        if prog in line:
            tokens = line.split(":")
            data[tokens[1].strip()] = float(tokens[2].strip())

    return data


def compare_profile(sans, total, base):

    to = (total - base) / base
    print "total overhead: %.2f%%" % (to * 100)

    ti = 0
    
    abso = dict()
    relo = dict()
    toto = dict()

    for san in sans:
        io = (sans[san] - base) / base
        abso[san] = io
        relo[san] = io / to

        ti = ti + io

    print "sum overhead: %.2f%%" % (ti * 100)
    print "-" * 72 

    return (abso, relo) 


class Solution:

    def __init__(self, k):
        self.parts = []
        for i in range(k-1):
            self.parts.append([])

    def calculate_balance(self, n):
        k = len(self.parts) + 1
        
        ave = n / k

        balance = 0
        total = 0

        for i in range(k-1):
            balance = balance + abs(len(self.parts[i]) - ave)
            total = total + len(self.parts[i])

        balance = balance + abs(n - total - ave)
        return balance


def recursion_2(data, t, n, s):

    if n == 0:
        return [Solution(2)]

    sols = []
    if s - data[n-1] >= 0 and t[n-1][s-data[n-1]]:
        sub = recursion_2(data, t, n-1, s-data[n-1])
        for sol in sub:
            sol.parts[0].append(n-1)
            sols.append(sol)

    if t[n-1][s]:
        sub = recursion_2(data, t, n-1, s)
        for sol in sub:
            sols.append(sol)

    return sols

def partition_2(data):
    
    n = len(data) + 1
    s = sum(data)

    # build recuision table
    t = numpy.empty((n, s), dtype=bool)
    for i in range(0, n):
        for j in range(0, s):
             t[i][j] = False

    for i in range(0, n):
        t[i][0] = True

    for i in range(1, n):
        for j in range(0, s):
            if t[i-1][j]:
                t[i][j] = True
            if j - data[i-1] >= 0 and t[i-1][j-data[i-1]]:
                t[i][j] = True

    # get balanced sets
    ave = s/2
    mindiff = s
    minx = -1

    for x in range(0, s/2):
        if t[n-1][x]:
            diff = abs(x-ave) + abs(s-x-ave)
            if diff < mindiff:
                mindiff = diff
                minx = x

    # find all indices sets
    sols = recursion_2(data, t, n-1, minx)

    # get the optimal partition
    rank = sorted(range(len(data)), key=lambda k: data[k])

    finals = []
    for sol in sols:
        separated = True
        for i in range(3):
            for j in range(1):
                count = 0
                for l in range(2):
                    if rank[2*i+l] in sol.parts[j]:
                        count = count + 1

                if count != 1:
                    separated = False
                    break

        if separated:
            finals.append(sol)

    if len(finals) != 0:
        balance = sorted(range(len(finals)), 
                key=lambda k: finals[k].calculate_balance(len(data)))

        return finals[balance[0]]

    else:
        print "[!] no optimal solution found"
        return sols[0]

def output_2(prog, stage, slices, ignored, partitioned, 
        func_result, func_overhead):

    func_names = func_overhead.keys()

    with open(os.path.join(DISTDIR, "%s-%s-p%d-1" % \
            (prog, stage, slices)), "w+") as f:

        to = 0
        for i in range(0, len(func_names)):
            if i in func_result or i in ignored[:len(ignored)/2]:
                to = to + func_overhead[func_names[i]].duration * 100
                f.write("fun:%s\n" % func_names[i])

    print "slice 1 overhead: %.3f%%" % to

    with open(os.path.join(DISTDIR, "%s-%s-p%d-2" % \
            (prog, stage, slices)), "w+") as f:

        to = 0
        for i in range(0, len(func_names)):
            if (i in partitioned and i not in func_result) or \
                    i in ignored[len(ignored)/2:]:

                to = to + func_overhead[func_names[i]].duration * 100
                f.write("fun:%s\n" % func_names[i])

    print "slice 2 overhead: %.3f%%" % to


if __name__ == "__main__":

    prog = sys.argv[1]
    slices = int(sys.argv[2])

    # analyze and compare two runs
    base = get_baseline_profile(prog)
    total = get_total_profile(prog)
    sans = get_sanitizer_profile(prog)

    abso, relo = compare_profile(sans, total, base) 

    # print per-function overhead
    for san in relo:
        print "%25s: %.2f%%\t\t%.2f%%" % \
                (san, abso[san] * 100, relo[san] * 100)

    print "-" * 72

    for san in relo:
        print "-fsanitize=%s" % san

    # transform data
    '''
    data = []
    partitioned = []
    ignored = []
    i = 0

    for func in rel_overhead:
        record = rel_overhead[func]
        if record.duration < -0.05:
            print "unacceptable negative overhead"
            sys.exit(-1)

        elif record.duration < 0.01:
            ignored.append(i)
        else:
            data.append(int(round(record.duration * 100)))
            partitioned.append(i)

        i = i + 1

    # decide on how to partition
    if slices == 2:
        raw_result = partition_2(data).parts[0]
        func_result = []
        for r in raw_result:
            func_result.append(partitioned[r])
        output_2(prog, san, slices, ignored, partitioned, 
                func_result, rel_overhead)
    '''
    
