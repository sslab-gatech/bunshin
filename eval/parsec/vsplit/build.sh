#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)

SAN=$1
shift

. $ROOT/eval/parsec/config.sh
. $ROOT/eval/parsec/vsplit/settings.sh $SAN

if [ "$#" != 3 ]; then
	echo $USAGE; exit
fi

SETS=$1
NVAR=$2
NAME=$3

parsec_locate $NAME

if [ "$CATEGORY" == "splash2x" ]; then
  NAME="splash2x.$NAME"
fi

cp $LOCATION/parsec/gcc-pthreads.bldconf $LOCATION/parsec/$COMBO.bldconf

if [ "$SETS" == "bft" ]; then
  parsec_submit $TIMER $WRAPPER
elif [ "$SETS" == "trace" ]; then
  parsec_submit $TRACER
else
  parsec_submit $TIMER
fi

parsec_clean $NAME $COMBO
parsec_build $NAME $COMBO
