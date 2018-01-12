#!/bin/bash

ROOT=$(git rev-parse --show-toplevel)

# paths
WKS=$HOME/bft-workspace/parsec/parsec-3.0
PARMACS=$WKS/pkgs/libs/parmacs
PROFDIR=$HOME/bft-workspace/profiles/parsec

# possible submits
TIMER="$ROOT/timer"
WRAPPER="$ROOT/mvee buddy"
PROFER="$ROOT/profile"
TRACER="strace -ff -o trace"

# configs
INSET="native"
NPROC=2

parsec_locate(){

NAME=$1

# always parsec first then splash2x
CATEGORY="parsec"
LOCATION=$(find $HOME/bft-workspace/parsec/parsec-3.0/pkgs/ -maxdepth 2 -type d -name "$NAME")

if [[ -z "$LOCATION" ]]; then
  LOCATION=$(find $HOME/bft-workspace/parsec/parsec-3.0/ext/splash2x/ -maxdepth 2 -type d -name "$NAME")
  OLDVER=$(find $HOME/bft-workspace/parsec/parsec-3.0/ext/splash2/ -maxdepth 2 -type d -name "$NAME")
  CATEGORY="splash2x"
fi

if [[ -z "$LOCATION" ]]; then
  echo "No such program"; exit
fi

}

parsec_submit(){

SUBMIT="$*"

}

parsec_clean(){

NAME=$1
BUILD=$2

$WKS/bin/parsecmgmt -a clean -p $NAME -c $BUILD 
$WKS/bin/parsecmgmt -a uninstall -p $NAME -c $BUILD

}

parsec_build(){

NAME=$1
BUILD=$2

$WKS/bin/parsecmgmt -a build -p $NAME -c $BUILD 

if [ "$CATEGORY" == "splash2x" ]; then
  cp -r $LOCATION/inst $OLDVER
fi

}

parsec_run(){

NAME=$1
BUILD=$2

$WKS/bin/parsecmgmt -a run -p $NAME -c $BUILD -i $INSET -n $NPROC -s "$SUBMIT"

}
