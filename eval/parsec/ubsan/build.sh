#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)

. $ROOT/eval/parsec/config.sh

USAGE="Usage: $0 <original | trace | profile | bft> <nvar> <spec name>"

if [ "$#" != 3 ]; then
	echo $USAGE; exit
fi

SETS=$1
NVAR=$2
NAME=$3

. $ROOT/eval/parsec/ubsan/settings.sh $SETS

if [ "$SETS" == "bft" ]; then
  parsec_submit $TIMER $WRAPPER
elif [ "$SETS" == "trace" ]; then
  parsec_submit $TRACER
elif [ "$SETS" == "profile" ]; then
  parsec_submit $PROFER $COMBO $PROFDIR $NAME
else
  parsec_submit $TIMER
fi

parsec_locate $NAME

if [ "$CATEGORY" == "splash2x" ]; then
  NAME="splash2x.$NAME"
fi

cp $LOCATION/parsec/gcc-pthreads.bldconf $LOCATION/parsec/$COMBO.bldconf

parsec_clean $NAME $COMBO
parsec_build $NAME $COMBO
