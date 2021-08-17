#!/bin/bash

. ./path.sh || exit 1;

stage=1
stop_stage=100
verbose=0

if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
    echo "stage 1: Generate some types of auditory streaming stimulus"
    for bfreq in 400 500 600; do
        generate.py \
            --verbose ${verbose} \
            --suffix pure_a315hz_b${bfreq}hz \
            --pure-tone-freq 315 ${bfreq} \
            --config conf/auditory_streaming.conf
    done
fi

