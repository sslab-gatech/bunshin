#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)
PORT=8000

USAGE="Usage: $0 <default | base | asan | msan | ubsan> <original | trace | bft> <nvar>"

if [ "$#" != 3 ]; then
	echo $USAGE; exit
fi

PROF=$1
SETS=$2
NVAR=$3

. $ROOT/eval/servers/lighttpd/$PROF.cfg

BIN=$HOME/bft-workspace/nginx-$PROF/sbin/nginx
ARG=""

WRAP="$ROOT/mvee run"

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
