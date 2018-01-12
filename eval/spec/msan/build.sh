#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)

. $ROOT/eval/spec/config.sh
. $ROOT/eval/spec/msan/settings.sh

if [ "$#" != 3 ]; then
	echo $USAGE; exit
fi

SETS=$1
NVAR=$2
NAME=$3

spec_locate $NAME

COMBO="$SETS"
if [ "$SETS" != "original" ] && [ "$SETS" != "bft" ] && [ "$SETS" != "profile" ] && [ "$SETS" != "memstat" ]; then
	echo $USAGE; exit 
elif [ "$SETS" == "bft" ]; then
	COMBO=$SETS-$NVAR
elif [ "$SETS" == "profile" ]; then
  CFLAGS="$CFLAGS -fno-inline -g -pg"
  CXXFLAGS="$CXXFLAGS -fno-inline -g -pg"
  LDFLAGS="$LDFLAGS -g -pg"
  LDXXFLAGS="$LDXXFLAGS -g -pg"
fi

SUBMIT=""
if [ "$SETS" == "bft" ]; then
	BINS=""
	for i in $(seq 1 $NVAR); do
		BINS="$BINS `spec_path $NAME $BUILD original`"
	done
	SUBMIT="$WRAPPER $NVAR $BINS \$command"

elif [ "$SETS" == "profile" ]; then
  mkdir -p $HOME/bft-workspace/profiles/spec
  SUBMIT="$PROFILER $BUILD $HOME/bft-workspace/profiles/spec $NAME \$command"

elif [ "$SETS" == "memstat" ]; then
  mkdir -p $HOME/bft-workspace/memstats/spec
  SUBMIT="$MEMSTAT $BUILD $HOME/bft-workspace/memstats/spec $NAME \$command"

fi

spec_c_compiler $CC $CFLAGS
spec_c_linker $CLD $LDFLAGS
spec_cxx_compiler $CXX $CXXFLAGS
spec_cxx_linker $CXXLD $LDXXFLAGS

spec_config $NAME $BUILD $COMBO $SUBMIT

spec_build $NAME $BUILD $COMBO
