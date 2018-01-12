#!/bin/bash

BUILD="base"
USAGE="Usage: $0 <original | profile | memstat | bft> <nvariants> <spec name>"

CC=$HOME/bft-workspace/llvm/build/bin/clang
CLD=$HOME/bft-workspace/llvm/build/bin/clang
CXX=$HOME/bft-workspace/llvm/build/bin/clang++
CXXLD=$HOME/bft-workspace/llvm/build/bin/clang++
CFLAGS="-flto"
LDFLAGS="-flto -fuse-ld=gold"
CXXFLAGS="-flto -stdlib=libstdc++"
LDXXFLAGS="-flto -fuse-ld=gold"
