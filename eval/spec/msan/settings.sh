#!/bin/bash

BUILD="msan"
USAGE="Usage: $0 <original | profile | bft> <nvariants> <spec name>"

CC=$HOME/bft-workspace/llvm/build/bin/clang
CLD=$HOME/bft-workspace/llvm/build/bin/clang
CXX=$HOME/bft-workspace/llvm/build/bin/clang++
CXXLD=$HOME/bft-workspace/llvm/build/bin/clang++
CFLAGS="-fsanitize=memory -fPIE -pie -flto"
LDFLAGS="-fsanitize=memory -fPIE -pie -flto -fuse-ld=gold"
CXXFLAGS="-stdlib=libstdc++ -fsanitize=memory -fPIE -pie -flto"
LDXXFLAGS="-fsanitize=memory -flto -fPIE -pie -fuse-ld=gold"
