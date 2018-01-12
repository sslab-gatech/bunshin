#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)

. $ROOT/eval/parsec/config.sh
. $ROOT/eval/parsec/default/settings.sh

if [ "$#" != 3 ]; then
	echo $USAGE; exit
fi

SETS=$1
NVAR=$2
NAME=$3

if [ "$SETS" == "bft" ]; then
  parsec_submit $TIMER $WRAPPER
elif [ "$SETS" == "trace" ]; then
  parsec_submit $TRACER
else
  parsec_submit $TIMER
fi

parsec_run $NAME $BUILD 
