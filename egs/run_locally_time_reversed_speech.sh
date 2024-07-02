#!/bin/bash

. ./path.sh || exit 1;

stage=1
stop_stage=100
verbose=0

wavlist=$1

CMDNAME=`basename $0`
if [ $# -ne 1 ]; then
  echo "Usage: $CMDNAME wavlist (A wavlist is a file that lists the paths of wav files in a bullet-point format.)" 1>&2
  echo "Here, sample_speech_list.txt is used." 1>&2
  wavlist=sample_speech_list.txt
fi


if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
    echo "stage 1: Generate some types of locally time-reversed speech"
    for duration in 1 5 10 25 50 75 100; do
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix duration${duration} \
            --reverse-duration ${duration} \
            --config conf/locally_time_reversed_speech.conf
    done
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    echo "stage 2: Generate some types of locally time-randomized speech"
    for duration in 1 5 10 25 50 75 100; do
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix duration${duration}_randomize \
            --reverse-duration ${duration} \
            --randomize true \
            --config conf/locally_time_reversed_speech.conf
    done
fi
