#!/bin/bash

BUILD="gcc-pthreads"

if [ "$SETS" == "profile" ]; then
  EXTRA_CFLAGS="-fno-inline -pg"
  EXTRA_CXXFLAGS="-fno-inline -pg"
  EXTRA_LDFLAGS="-fno-inline -pg"
fi
