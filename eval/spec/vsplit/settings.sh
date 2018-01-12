#!/bin/bash

SAN=$1

BUILD="vsplit-$SAN"
USAGE="Usage: $0 <sanitizer> <original | profile | bft> <nvariants> <spec name>"

CC=$HOME/bft-workspace/llvm/build/bin/clang
CLD=$HOME/bft-workspace/llvm/build/bin/clang
CXX=$HOME/bft-workspace/llvm/build/bin/clang++
CXXLD=$HOME/bft-workspace/llvm/build/bin/clang++
CFLAGS="-fsanitize=$SAN -flto"
LDFLAGS="-fsanitize=$SAN -flto -fuse-ld=gold"
CXXFLAGS="-stdlib=libstdc++ -fsanitize=$SAN -flto"
LDXXFLAGS="-fsanitize=$SAN -flto -fuse-ld=gold"
