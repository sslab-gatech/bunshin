#!/usr/bin/env python

import os
import re
import sys
import glob
import numpy
import subprocess

PROFDIR = os.path.join(os.getenv("HOME"), "bft-workspace", "profiles", "spec")
DISTDIR = os.path.join(os.getenv("HOME"), "bft-workspace", "hdist", "spec")

GPROF_RE = re.compile("^(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(.*)$")
NM_RE = re.compile("^.*?\s(\w)\s(.*)$")

class Record:
    
    def __init__(self, func, duration, calls):
        self.func = func
        self.duration = duration
        self.calls = calls


class Symbol:

    def __init__(self, name, cat, src):
        self.name = name
        self.cat = cat
        self.src = src


def get_binary(prog, stage):
    return os.path.join(PROFDIR, "%s_base.%s-profile" % (prog, stage))

def get_symbols(prog, stage):

    ps = subprocess.Popen("nm %s" % get_binary(prog, stage), 
            shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.readlines()

    symbols = dict()
    for line in output:
        line = line.rstrip()
        m = NM_RE.match(line)

        if not m:
            print "unable to parse symbols"
            sys.exit(-1)

        cat = m.group(1)
        func = m.group(2)

        if cat in ["t", "T"]:
            subps = subprocess.Popen("c++filt -i %s" % func, 
                    shell=True, stdout=subprocess.PIPE)
            
            demangled = subps.stdout.readline().strip()
            symbols[demangled] = func

    return symbols

def get_profile(prog, stage):

    symbols = get_symbols(prog, stage)
    
    profile = dict()
    for f in glob.glob("%s/%s-%s-*" % (PROFDIR, prog, stage)):
        ps = subprocess.Popen("gprof -p -b %s %s" % \
                (get_binary(prog, stage), f),
                shell=True, stdout=subprocess.PIPE)

        output = ps.stdout.readlines()

        for line in output[5:]:
            if not ("__asan" in line or \
                    "__sanitizer" in line):

                line = line.strip()
                m = GPROF_RE.match(line)

                if m is not None:
                    func = m.group(7)

                    if "::" in func or "(" in func:
                        if func in symbols:
                            func = symbols[func]
                        else:
                            print "%s not in symbols" % func

                    if func not in profile:
                        profile[func] = []

                    profile[func].append(Record(func, 
                        float(m.group(3)), float(m.group(4))))

    return profile

def aggregate_profile(profile):

    aggregated = dict()
    for func in profile:
        records = profile[func]

        sum_duration = 0
        sum_calls = 0

        for record in records:
            sum_duration = sum_duration + record.duration
            sum_calls = sum_calls + record.calls

        aggregated[func] = Record(func, sum_duration, sum_calls)

    return aggregated

def compare_profile(profile1, profile2):
    
    overheads = dict()
    for func in profile2:
        record2 = profile2[func]
        if func in profile1:
            record1 = profile1[func]
            val = record2.duration - record1.duration
            if val < 0:
                val = 0
            overheads[func] = Record(func, val, record2.calls - record1.calls)
        else:
            overheads[func] = Record(func, record2.duration, record2.calls)

    return overheads

def relative_overhead(overheads):

    relative = dict()

    total_duration = 0
    for func in overheads:
        total_duration = total_duration + overheads[func].duration

    for func in overheads:
        record = overheads[func]
        relative[func] = Record(func,
                record.duration / total_duration,
                record.calls)

    return relative


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

def recursion_3(data, t, n, s0, s1):

    if n == 0:
        return [Solution(3)]

    sols = []
    if s0 - data[n-1] >= 0 and t[n-1][s0-data[n-1]][s1]:
        sub = recursion_3(data, t, n-1, s0-data[n-1], s1)
        for sol in sub:
            sol.parts[0].append(n-1)
            sols.append(sol)

    if s1 - data[n-1] >= 0 and t[n-1][s0][s1-data[n-1]]:
        sub = recursion_3(data, t, n-1, s0, s1-data[n-1])
        for sol in sub:
            sol.parts[1].append(n-1)
            sols.append(sol)

    if t[n-1][s0][s1]:
        sub = recursion_3(data, t, n-1, s0, s1)
        for sol in sub:
            sols.append(sol)

    return sols

def partition_3(data):

    n = len(data) + 1
    s = sum(data)

    # build recursion table
    t = numpy.empty((n,s,s), dtype=bool)
    for i in range(0, n):
        for j in range(0, s):
            for l in range(0, s):
                t[i][j][l] = False

    t[0][0][0] = True

    for i in range(1, n):
        for j in range(0, s):
            if t[i-1][j][0]:
                t[i][j][0] = True
            elif j - data[i-1] >= 0 and t[i-1][j-data[i-1]][0]:
                t[i][j][0] = True

    for i in range(1, n):
        for l in range(0, s):
            if t[i-1][0][l]:
                t[i][0][l] = True
            elif l - data[i-1] >= 0 and t[i-1][0][l-data[i-1]]:
                t[i][0][l] = True

    for i in range(1,n):
        for j in range(1, s):
            for l in range(1, s):
                if t[i-1][j][l]:
                    t[i][j][l] = True
                if j - data[i-1] >= 0 and t[i-1][j-data[i-1]][l]:
                    t[i][j][l] = True
                if l - data[i-1] >= 0 and t[i-1][j][l-data[i-1]]:
                    t[i][j][l] = True

    # get balanced sets
    ave = s/3
    mindiff = s
    minx = -1
    miny = -1
    for x in range(0, s):
        for y in range(0, s):
            if t[n-1][x][y]:
                diff = abs(x-ave) + abs(y-ave) + abs(s-x-y-ave)
                if diff < mindiff:
                    mindiff = diff
                    minx = x
                    miny = y

    # find all indices sets
    sols = recursion_3(data, t, n-1, minx, miny)

    # get the optimal partition
    rank = sorted(range(len(data)), key=lambda k: data[k])

    finals = []
    for sol in sols:
        separated = True
        for i in range(3):
            for j in range(2):
                count = 0
                for l in range(2):
                    if rank[3*i+l] in sol.parts[j]:
                        count = count + 1

                if count != 1:
                    separated = False
                    break

        if separated:
            finals.append(sol)

    if len(finals) != 0:
        balance = sorted(range(len(finals)), key=lambda k: finals[k].calculate_balance(len(data)))
        return finals[balance[0]]
    else:
        print "[!] no optimal solution found"
        return sols[0]

def output_3(prog, stage, slices, ignored, partitioned, 
        func_result, func_overhead):

    func_names = func_overhead.keys()

    with open(os.path.join(DISTDIR, "%s-%s-p%d-1" % \
            (prog, stage, slices)), "w+") as f:

        to = 0
        for i in range(0, len(func_names)):
            if (i in partitioned and i not in func_result[0]) or \
                    (i not in partitioned and i not in ignored[:len(ignored)/3]):

                to = to + func_overhead[func_names[i]].duration * 100
                f.write("fun:%s\n" % func_names[i])

    print "slice 1 overhead: %.3f%%" % to

    with open(os.path.join(DISTDIR, "%s-%s-p%d-2" % \
            (prog, stage, slices)), "w+") as f:

        to = 0
        for i in range(0, len(func_names)):
            if (i in partitioned and i not in func_result[1]) or \
                    (i not in partitioned and i not in ignored[len(ignored)/3:len(ignored)/3*2]):

                to = to + func_overhead[func_names[i]].duration * 100
                f.write("fun:%s\n" % func_names[i])

    print "slice 2 overhead: %.3f%%" % to

    with open(os.path.join(DISTDIR, "%s-%s-p%d-3" % \
            (prog, stage, slices)), "w+") as f:

        to = 0
        for i in range(0, len(func_names)):
            if (i in func_result[0] or i in func_result[1]) or \
                    (i not in partitioned and i not in ignored[len(ignored)/3*2:]):

                to = to + func_overhead[func_names[i]].duration * 100
                f.write("fun:%s\n" % func_names[i])

    print "slice 3 overhead: %.3f%%" % to


if __name__ == "__main__":

    prog = sys.argv[1]
    san = sys.argv[2]
    slices = int(sys.argv[3])

    # analyze and compare two runs
    base_symbols = get_symbols(prog, "base")
    base_profile = aggregate_profile(get_profile(prog, "base"))

    san_symbols = get_symbols(prog, san)
    san_profile = aggregate_profile(get_profile(prog, san))

    overhead = compare_profile(base_profile, san_profile)
    rel_overhead = relative_overhead(overhead)

    # print per-function overhead
    for func in rel_overhead:
        print "%24s: \t\t%.3f\t\t%.2f%%" % \
                (func, overhead[func].duration, 
                        rel_overhead[func].duration * 100)

    # transform data
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

    elif slices == 3:
        raw_result = partition_3(data).parts
        func_result = [[],[]]
        for r in raw_result[0]:
            func_result[0].append(partitioned[r])
        for r in raw_result[1]:
            func_result[1].append(partitioned[r])
        output_3(prog, san, slices, ignored, partitioned,
                func_result, rel_overhead)
