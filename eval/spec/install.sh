#!/bin/bash -e

CURDIR=$(pwd)

mkdir -p $HOME/bft-workspace/spec/cpu2006

mkdir tmp
cd tmp
wget http://meng.gtisc.gatech.edu/tmp/SPEC_CPU2006v1.2.tar.gz
tar -xzf SPEC_CPU2006v1.2.tar.gz

cd SPEC_CPU2006v1.2
./install.sh -d $HOME/bft-workspace/spec/cpu2006 -f

cd $HOME/bft-workspace/spec/cpu2006
patch -p1 < $CURDIR/sanitizer.patch

cd $CURDIR
sudo rm -rf tmp
