#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)

# program compile config
SPEC_J=8
SPEC_RUNS=1
SPEC_TUNE="base"
SPEC_OLEVEL="-O3"
SPEC_SIZE="train"

# path-related constants
WKS=$HOME/bft-workspace/spec/cpu2006
HDIST_DIR=$HOME/bft-workspace/hdist/spec
VDIST_DIR=$HOME/bft-workspace/vdist/spec

WRAPPER="$ROOT/mvee run"
PROFILER="$ROOT/profile"
MEMSTAT="$ROOT/memstat"
TRACER="strace -ff -o trace"

# utility functions
spec_locate(){

NAME=$1

# always cpu2006 first then 2000
LOCATION=$(find $WKS/benchspec/ -maxdepth 2 -type d -name "*$NAME")

if [[ -z "$LOCATION" ]]; then
	LOCATION=$(find $WKS/benchspec/ -maxdepth 2 -type d -name "*$NAME")	
fi

if [[ -z "$LOCATION" ]]; then
	echo "No such program"; exit
fi

# resolve spec dir and spec category
SPEC_BMK=$(basename $LOCATION)
SPEC_CAT=$(basename $(dirname $LOCATION))
SPEC_DIR=$(dirname $(dirname $(dirname $LOCATION)))
SPEC_SET=$(basename $SPEC_DIR)

# per spec dir customization
if [ "$SPEC_SET" == "cpu2000" ]; then
	SPEC_SIZE="ref"
fi

# per program customization
if [ "$NAME" == "libquantum" ]; then
	SPEC_SIZE="ref"
fi

if [ "$NAME" == "gcc" ]; then
  SPEC_SIZE="ref"
fi

if [ "$NAME" == "sphinx3" ]; then
  SPEC_SIZE="ref"
fi

}

spec_path(){

# basic config 
NAME=$1
BUILD=$2
COMBO=$3

EXEBASE=$NAME
if [ "$NAME" == "sphinx3" ]; then
	EXEBASE="sphinx_livepretend"
fi

if [ "$NAME" == "xalancbmk" ]; then
  EXEBASE="Xalan"
fi

echo "$SPEC_DIR/benchspec/$SPEC_CAT/$SPEC_BMK/exe/${EXEBASE}_${SPEC_TUNE}.$BUILD-$COMBO"

}

spec_c_compiler(){

C_COMPILER="$*"

}

spec_c_linker(){

C_LINKER="$*"

}

spec_cxx_compiler(){

CXX_COMPILER="$*"

}

spec_cxx_linker(){

CXX_LINKER="$*"

}

spec_libs(){

LIBS="$*"

}

spec_config(){

# basic config 
NAME=$1
BUILD=$2
COMBO=$3

# launch instruction
shift 3
SUBMIT="$*"

INSERT1=""
INSERT2=""
if [[ ! -z "$SUBMIT" ]]; then
	INSERT1="submit = $SUBMIT"
	INSERT2="use_submit_for_speed = 1"
fi

# construct the config file name
CONF="$NAME-$BUILD-$COMBO.cfg"

# goto spec top dir
cd $SPEC_DIR

# test file existence
if [ -f "config/$CONF" ]; then
	read -p "found $CONF, force rebuild ? " ANSWER
	if [[ "$ANSWER" != "y" ]]; then
		exit
	fi
fi

# clean existing file if exists
rm -rf config/$CONF

cat << EOF > config/$CONF
ignore_errors = 1
tune          = $SPEC_TUNE
ext           = $BUILD-$COMBO 
output_format = asc
reportable    = 0
teeout        = 1
teerunout     = 1
makeflags     = -j$SPEC_J
strict_rundir_verify = 0

$INSERT1
$INSERT2

default=$SPEC_TUNE=default=default:
CC         = $C_COMPILER 
CLD        = $C_LINKER 
CXX        = $CXX_COMPILER
CXXLD      = $CXX_LINKER
OPTIMIZE   = $SPEC_OLEVEL
EXTRA_LIBS = $LIBS
PORTABILITY    = -DSPEC_CPU_LP64

400.perlbench=$SPEC_TUNE=default=default:
CC           = $C_COMPILER -std=gnu89
CPORTABILITY = -DSPEC_CPU_LINUX_X64

462.libquantum=$SPEC_TUNE=default=default:
CPORTABILITY = -DSPEC_CPU_LINUX

447.dealII=$SPEC_TUNE=default=default:
CXXPORTABILITY= -include string.h -include stdlib.h -include cstddef

483.xalancbmk=$SPEC_TUNE=default=default:
CXXPORTABILITY= -DSPEC_CPU_LINUX -include string.h
EOF

}

spec_build(){

# basic config 
NAME=$1
BUILD=$2
COMBO=$3

# construct the config file name
CONF="$NAME-$BUILD-$COMBO.cfg"

cd $SPEC_DIR

# setup spec environment
. shrc

runspec --config $CONF --action build $NAME

}

spec_run(){

# basic config 
NAME=$1
BUILD=$2
COMBO=$3

# construct the config file name
CONF="$NAME-$BUILD-$COMBO.cfg"

cd $SPEC_DIR

# setup spec environment
. shrc

echo "config: $CONF"

runspec --config $CONF --size $SPEC_SIZE --iterations $SPEC_RUNS $NAME

}
