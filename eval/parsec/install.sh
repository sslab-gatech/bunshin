#!/bin/bash -e

CURDIR=$(pwd)

mkdir -p $HOME/bft-workspace/parsec

cd $HOME/bft-workspace/parsec

wget http://meng.gtisc.gatech.edu/tmp/parsec-3.0.tar.gz
tar xzf parsec-3.0.tar.gz

rm parsec-3.0.tar.gz

cd $CURDIR
