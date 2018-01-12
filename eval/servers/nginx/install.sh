#!/bin/bash

CURDIR=$(pwd)

ROOT=$(git rev-parse --show-toplevel)
PORT=8000

if [ "$#" != 1 ]; then
  echo "Usage: $0 <default | base | asan | msan | ubsan>"; exit
fi

PROF=$1

. $ROOT/eval/servers/lighttpd/$PROF.cfg

BUILD=$HOME/bft-workspace/nginx-$PROF

# clean up previous build
rm -rf $BUILD 2> /dev/null
mkdir -p $BUILD

# download nginx src
mkdir tmp
cd tmp

wget http://nginx.org/download/nginx-1.8.0.tar.gz
tar -xzf nginx-1.8.0.tar.gz

# build nginx
cd nginx-1.8.0

./configure --with-select_module --prefix=$BUILD
sed -i "s/^LINK =.*/LINK = \$(CC) $LDFLAGS/" objs/Makefile

make
make install

# setup config
CONF=$BUILD/conf/nginx.conf

sed -i "s/^worker_processes.*/worker_processes 4;/" $CONF
sed -i "s/listen.*80;/listen    $PORT;/" $CONF
sed -i "s/worker_connections.*1024;/use select;\n    accept_mutex off;\n    worker_connections 1024;/" $CONF

E_ROOT=$(echo $ROOT | sed 's/\//\\\//g')
sed -i "s/root.*html;/root  $E_ROOT\/eval\/servers\/htdocs;/" $CONF

# clean up
cd $CURDIR
rm -rf tmp
