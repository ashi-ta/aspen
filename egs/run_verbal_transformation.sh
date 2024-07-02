#!/bin/bash

. ./path.sh || exit 1;

stage=1
stop_stage=100
verbose=0

wavlist=$1

CMDNAME=`basename $0`
if [ $# -ne 1 ]; then
  echo "Usage: $CMDNAME wavlist (A wavlist is a file that lists the paths of wav files in a bullet-point format.)" 1>&2
  exit 1
fi


if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
    echo "stage 1: Generate verbal transformation stimulus"
    generate.py \
        --verbose ${verbose} \
        --wavlist ${wavlist} \
        --config conf/verbal_transformation.conf
fi

