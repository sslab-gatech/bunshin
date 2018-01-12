#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)

. $ROOT/eval/spec/config.sh
. $ROOT/eval/spec/default/settings.sh

if [ "$#" != 3 ]; then
	echo $USAGE; exit
fi

SETS=$1
NVAR=$2
NAME=$3

spec_locate $NAME

COMBO="$SETS"
if [ "$SETS" != "original" ] && [[ "$SETS" != "bft" ]] && [[ "$SETS" != "trace" ]]; then
	echo $USAGE; exit 
elif [ "$SETS" == "bft" ]; then
	COMBO=$SETS-$NVAR
fi

SUBMIT=""
if [ "$SETS" == "bft" ]; then
	BINS=""
	for i in $(seq 1 $NVAR); do
		BINS="$BINS `spec_path $NAME $BUILD original`"
	done
	SUBMIT="$WRAPPER $NVAR $BINS \$command"
elif [ "$SETS" == "trace" ]; then
  SUBMIT="$TRACER \$command"
fi

spec_c_compiler $CC $CFLAGS
spec_c_linker $CLD $LDFLAGS
spec_cxx_compiler $CXX $CFLAGS
spec_cxx_linker $CXXLD $LDFLAGS

spec_config $NAME $BUILD $COMBO $SUBMIT

spec_build $NAME $BUILD $COMBO
