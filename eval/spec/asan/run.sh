#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)

. $ROOT/eval/spec/config.sh
. $ROOT/eval/spec/asan/settings.sh

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
fi

spec_run $NAME $BUILD $COMBO
