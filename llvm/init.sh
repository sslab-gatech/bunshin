#!/bin/bash

mkdir -p $HOME/bft-workspace/llvm
cd $HOME/bft-workspace/llvm

# get sources
if [ ! -d "src" ]; then
  mkdir src 
  svn co http://llvm.org/svn/llvm-project/llvm/trunk src 
  cd src/tools
  svn co http://llvm.org/svn/llvm-project/cfe/trunk clang
  cd ../projects
  svn co http://llvm.org/svn/llvm-project/compiler-rt/trunk compiler-rt
  svn co http://llvm.org/svn/llvm-project/libcxx/trunk libcxx
  svn co http://llvm.org/svn/llvm-project/libcxxabi/trunk libcxxabi
  # cannot build test-suite successfully
  #svn co http://llvm.org/svn/llvm-project/test-suite/trunk test-suite
  cd ../../
fi

# Configure and build
if [ ! -d "build" ]; then
  mkdir build
fi

cd build

cmake -DLLVM_TARGETS_TO_BUILD=X86 -DLLVM_BINUTILS_INCDIR=/usr/include -DCMAKE_BUILD_TYPE=Release ../src/
make -j8
