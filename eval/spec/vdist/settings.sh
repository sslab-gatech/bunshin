#!/bin/bash

VDIST_CONF=$1

BUILD="vdist-$VDIST_CONF"

CC=$HOME/bft-workspace/llvm/build/bin/clang
CLD=$HOME/bft-workspace/llvm/build/bin/clang
CXX=$HOME/bft-workspace/llvm/build/bin/clang++
CXXLD=$HOME/bft-workspace/llvm/build/bin/clang++

SANS=$(cat $VDIST_DIR/$NAME-ubsan-$VDIST_CONF | tr '\n' ' ')

CFLAGS="$SANS -flto"
LDFLAGS="$SANS -flto -fuse-ld=gold"
CXXFLAGS="-stdlib=libstdc++ $SANS -flto"
LDXXFLAGS="-fsanitize=address $SANS -flto -fuse-ld=gold"
