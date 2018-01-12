#!/bin/bash

BUILD=$1
OUTPUT=$2
PROG=$3
shift 3

$@

mv gmon.out $OUTPUT/$PROG-$BUILD-$RANDOM
