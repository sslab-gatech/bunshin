#!/bin/bash

CURDIR=$(pwd)

ROOT=$(git rev-parse --show-toplevel)
PORT=8000

BUILD=$HOME/bft-workspace/apache

# clean up previous build
rm -rf $BUILD 2> /dev/null
mkdir -p $BUILD

# download apache src
mkdir tmp
cd tmp

wget http://apache.spinellicreations.com//httpd/httpd-2.4.18.tar.gz
tar -xzf httpd-2.4.18.tar.gz

# build apache
cd httpd-2.4.18

./configure --enable-mpms-shared=all --prefix=$BUILD
make
make install

# setup config
CONF=$BUILD/conf/httpd.conf

sed -i "s/^Listen 80.*/Listen $PORT/" $CONF

sed -i "s/^LoadModule mpm_event_module.*/#LoadModule mpm_event_module modules\/mod_mpm_event.so/" $CONF
sed -i "s/^#LoadModule mpm_prefork_module.*/LoadModule mpm_prefork_module modules\/mod_mpm_prefork.so/" $CONF

echo '<IfModule mpm_prefork_module>' >> $CONF
echo '  StartServers 4' >> $CONF
echo '  MinSpareServers 1' >> $CONF
echo '  MaxSpareServers 4' >> $CONF
echo '  MaxRequestWorkers 4' >> $CONF
echo '  MaxConnectionsPerChild 0' >> $CONF
echo '</IfModule>' >> $CONF

E_ROOT=$(echo $ROOT | sed 's/\//\\\//g')
E_BUILD=$(echo $BUILD | sed 's/\//\\\//g')
sed -i "s/^DocumentRoot.*/DocumentRoot \"$E_ROOT\/eval\/servers\/htdocs\"/" $CONF
sed -i "s/^<Directory \"$E_BUILD\/htdocs\".*/<Directory \"$E_ROOT\/eval\/servers\/htdocs\">/" $CONF

# clean up
cd $CURDIR
rm -rf tmp
