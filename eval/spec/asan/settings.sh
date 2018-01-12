#!/bin/bash

BUILD="asan"
USAGE="Usage: $0 <original | profile | bft> <nvariants> <spec name>"

export ASAN_OPTIONS=detect_leaks=0,detect_odr_violation=0

CC=$HOME/bft-workspace/llvm/build/bin/clang
CLD=$HOME/bft-workspace/llvm/build/bin/clang
CXX=$HOME/bft-workspace/llvm/build/bin/clang++
CXXLD=$HOME/bft-workspace/llvm/build/bin/clang++
CFLAGS="-fsanitize=address -flto"
LDFLAGS="-fsanitize=address -flto -fuse-ld=gold"
CXXFLAGS="-stdlib=libstdc++ -fsanitize=address -flto"
LDXXFLAGS="-fsanitize=address -flto -fuse-ld=gold"
