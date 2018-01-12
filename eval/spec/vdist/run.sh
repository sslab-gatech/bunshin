#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)

VDIST_CONF=$1
shift

. $ROOT/eval/spec/config.sh

USAGE="Usage: $0 <vdist conf> <original | memstat | bft> <nvariants> <spec name>"

if [ "$#" != 3 ]; then
	echo $USAGE; exit
fi

SETS=$1
NVAR=$2
NAME=$3

spec_locate $NAME

. $ROOT/eval/spec/vdist/settings.sh $VDIST_CONF

COMBO="$SETS"
if [ "$SETS" != "original" ] && [ "$SETS" != "bft" ] && [ "$SETS" != "memstat" ]; then
	echo $USAGE; exit 
elif [ "$SETS" == "bft" ]; then
	COMBO=$SETS-$NVAR
fi

spec_run $NAME $BUILD $COMBO
