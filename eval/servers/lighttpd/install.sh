#!/bin/bash

CURDIR=$(pwd)

ROOT=$(git rev-parse --show-toplevel)
PORT=8000

if [ "$#" != 1 ]; then
  echo "Usage: $0 <default | base | asan | msan | ubsan>"; exit
fi

PROF=$1

. $ROOT/eval/servers/lighttpd/$PROF.cfg

BUILD=$HOME/bft-workspace/lighttpd-$PROF

# clean up previous build
rm -rf $BUILD 2> /dev/null
mkdir -p $BUILD

# download lighttpd src
mkdir tmp
cd tmp

wget http://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.37.tar.gz 
tar -xzf lighttpd-1.4.37.tar.gz 

# build lighttpd
cd lighttpd-1.4.37

./configure --prefix=$BUILD
make
make install

# setup config
CONF=$BUILD/lighttpd.conf

cat > $CONF << EOF
server.document-root = "$ROOT/eval/servers/htdocs"
server.port = $PORT 
server.event-handler = "select"
mimetype.assign = (
  ".html" => "text/html"
)
index-file.names = ( "index.html" )
EOF

# clean up
cd $CURDIR
rm -rf tmp
