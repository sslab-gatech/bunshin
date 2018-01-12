#!/usr/bin/env python

import subprocess as sp
import re
import time
import sys
import argparse
import numpy

HOST    = "128.61.240.116"
PORT    = 8000
NUM     = 10
PATTERN = re.compile("^Time per request:\s*(\d+\.\d+).*requests\)$")

CONCURRENCY_VARIATIONS  = (1, 64, 256, 512)
WORKLOAD_VARIATIONS     = ("1k", "256k", "1m", "16m")

DEFAULT_CONCURRENCY     = 64
DEFAULT_WORKLOAD        = "1k"

def run_once(host, port, concurrency, workload):
    proc = sp.Popen([
        "ab", 
        "-n", str(concurrency),
        "-c", str(concurrency),
        "-s", str(5),
        "http://%s:%d/data-%s" % (host, port, workload)
        ], stdout=sp.PIPE, stderr=sp.PIPE)

    proc.wait()

    output = proc.stdout.readlines()
    for l in output:
        l = l.strip()
        m = PATTERN.match(l)
        if m:
            return float(m.group(1))

    return None

def run_multi(host, port, concurrency, workload, num):
    results = []
    for i in range(num):
        fin = False
        rep = 0
        while(not fin and rep < 10):
            result = run_once(host, port, concurrency, workload)
            if result is not None:
                print result
                results.append(result)
                fin = True
            else:
                rep = rep + 1

    return results

def run_concurrency_test(host, port, workload, num):
    for concurrency in CONCURRENCY_VARIATIONS:
        print "Concurrency test with -c=%d" % concurrency
        
        results = run_multi(host, port, concurrency, workload, num)
        
        print "ave. %.2f, med. %.2f" % (numpy.mean(results), numpy.median(results))

        print "-" * 32
        
        time.sleep(2)

def run_workload_test(host, port, concurrency, num):
    for workload in WORKLOAD_VARIATIONS:
        print "Workload test with data-%s" % workload
        
        results = run_multi(host, port, concurrency, workload, num)
        
        for r in results:
            print r
        print "-" * 32
        
        time.sleep(2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("-c", "--concurrency", action="store_true")
    actions.add_argument("-w", "--workload", action="store_true")

    parser.add_argument("--num", default=NUM, type=int)
    parser.add_argument("--host", default=HOST, type=str)
    parser.add_argument("--port", default=PORT, type=int)

    args = parser.parse_args()

    num = args.num
    host = args.host
    port = args.port

    if args.concurrency:
        run_concurrency_test(host, port, DEFAULT_WORKLOAD, num)

    if args.workload:
        run_workload_test(host, port, DEFAULT_CONCURRENCY, num)
