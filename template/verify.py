#!/usr/bin/env python

import os
import sys
import re
import glob
import fnmatch
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSLIST = os.path.join(ROOT, "template", "syscall.list")
IGNLIST = os.path.join(ROOT, "template", "ignored.list")

SYS_RE = re.compile("^(\w+)\(.*$")
SIG_RE = re.compile("^%s.*" % (re.escape("-") * 3))
EXT_RE = re.compile("^%s.*" % (re.escape("+") * 3))

SYSCALL = []
IGNORED = []

def load():
    with open(SYSLIST, "r") as f:
        content = f.readlines()
        for line in content:
            SYSCALL.append(line.strip())

    with open(IGNLIST, "r") as f:
        content = f.readlines()
        for line in content:
            IGNORED.append(line.strip())


def verify(path):
    with open(path, "r") as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            m = SYS_RE.match(line)
            if m is not None:
                sysname = m.group(1)
                if sysname not in SYSCALL and sysname not in IGNORED:
                    print "[*] %s - %s" %  (sysname, line)
            elif not (SIG_RE.match(line) or EXT_RE.match(line)):
                print "[!] line mismatch: %s" % line

if __name__ == "__main__":

    # config parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", action="store")
    parser.add_argument("-d", "--dir", action="store")
    parser.add_argument("-t", "--tree", action="store")

    # parse
    args = parser.parse_args()

    # load syscall list
    load()

    # verify
    if args.file:
        path = args.file
        verify(path)
    elif args.dir:
        dpath = args.dir
        paths = glob.glob("%s/trace.*" % dpath)
        for path in paths:
            verify(path)
    elif args.tree:
        tpath = args.tree
        for root, dnames, fnames in os.walk(tpath):
            for fname in fnmatch.filter(fnames, "trace.[0123456789]*"):
                path = os.path.join(root, fname)
                verify(path)
