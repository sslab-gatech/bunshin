#!/bin/bash

BUILD="ubsan"
USAGE="Usage: $0 <original | profile | bft> <nvariants> <spec name>"

CC=$HOME/bft-workspace/llvm/build/bin/clang
CLD=$HOME/bft-workspace/llvm/build/bin/clang
CXX=$HOME/bft-workspace/llvm/build/bin/clang++
CXXLD=$HOME/bft-workspace/llvm/build/bin/clang++
CFLAGS="-fsanitize=undefined -flto -O3"
LDFLAGS="-fsanitize=undefined -flto -fuse-ld=gold -O3"
CXXFLAGS="-stdlib=libstdc++ -fsanitize=undefined -flto -O3"
LDXXFLAGS="-fsanitize=undefined -flto -fuse-ld=gold -O3"
