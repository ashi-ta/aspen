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
    echo "stage 1: Generate continuity illusion stimulus by using an input wavlist"
    for gap_method in replace silent overlap; do
        for snr in 0 10 20; do
            for gap in 50 100 200;do
                generate.py \
                    --verbose ${verbose} \
                    --wavlist ${wavlist} \
                    --suffix ${gap_method}_target${gap}ms_gap${gap}ms_snr-${snr} \
                    --gap-method ${gap_method} \
                    --target-duration ${gap} \
                    --gap-duration ${gap} \
                    --target-snr -${snr} \
                    --config conf/continuity.conf
            done
        done
    done
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    echo "stage 2: Generate continuity illusion stimulus by using a pure tone created from scratch"
    for gap_method in replace silent overlap; do
        for snr in 0 10 20; do
            generate.py \
                --verbose ${verbose} \
                --suffix ${gap_method}_pure_tone_target200ms_gap200ms_snr-${snr} \
                --gap-method ${gap_method} \
                --target-snr -${snr} \
                --config conf/continuity_tone.conf
        done
    done
fi

if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
    echo "stage 3: Generate continuity illusion stimulus by using a updown chirped fm tone created from scratch"
    for gap_method in replace silent overlap; do
        for snr in 0 10 20; do
            generate.py \
                --verbose ${verbose} \
                --suffix ${gap_method}_fm_tone_updown_target200ms_gap200ms_snr-${snr} \
                --gap-method ${gap_method} \
                --target-snr -${snr} \
                --config conf/continuity_tone_updown.conf
        done
    done
fi
