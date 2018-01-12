#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)
PORT=8000

BIN=$HOME/bft-workspace/apache/bin/httpd
ARG="-k start"

WRAP="$ROOT/mvee run"

USAGE="Usage: $0 <original | trace | bft>"

if [ "$#" != 2 ]; then
	echo $USAGE; exit
fi

SETS=$1
NVAR=$2
if [[ "$SETS" == "bft" ]]; then
	BINS=""
	for i in $(seq 1 $NVAR); do
		BINS="$BINS $BIN"
	done

	$WRAP $NVAR $BINS $BIN $ARG
elif [[ "$SETS" == "trace" ]]; then
	strace -ff -o trace $BIN $ARG
else
	$BIN $ARG
fi
