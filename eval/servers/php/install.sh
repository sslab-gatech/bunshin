#!/bin/bash

CURDIR=$(pwd)

BUILD=$HOME/bft-workspace/php

# clean up previous build
rm -rf $BUILD 2> /dev/null
mkdir -p $BUILD

# download php src
mkdir tmp
cd tmp

wget http://php.net/distributions/php-5.6.16.tar.gz
tar -xzf php-5.6.16.tar.gz

# build php
cd php-5.6.16

./configure --prefix=$BUILD
make
make install

# clean up
cd $CURDIR
rm -rf tmp
