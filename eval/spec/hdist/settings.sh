#!/bin/bash

HDIST_CONF=$1

BUILD="hdist-$HDIST_CONF"

export ASAN_OPTIONS=detect_leaks=0,detect_odr_violation=0

CC=$HOME/bft-workspace/llvm/build/bin/clang
CLD=$HOME/bft-workspace/llvm/build/bin/clang
CXX=$HOME/bft-workspace/llvm/build/bin/clang++
CXXLD=$HOME/bft-workspace/llvm/build/bin/clang++
CFLAGS="-fsanitize=address -fsanitize-blacklist=$HDIST_DIR/$NAME-asan-$HDIST_CONF -flto"
LDFLAGS="-fsanitize=address -fsanitize-blacklist=$HDIST_DIR/$NAME-asan-$HDIST_CONF -flto -fuse-ld=gold"
CXXFLAGS="-stdlib=libstdc++ -fsanitize=address -fsanitize-blacklist=$HDIST_DIR/$NAME-asan-$HDIST_CONF -flto"
LDXXFLAGS="-fsanitize=address -flto -fsanitize-blacklist=$HDIST_DIR/$NAME-asan-$HDIST_CONF -fuse-ld=gold"
