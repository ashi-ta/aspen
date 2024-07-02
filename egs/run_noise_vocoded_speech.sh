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
    echo "stage 1: Generate some types of noise-vocoded speechs based on octave bands (extracted by half-rect.)"
    for band in 1 2 3 4 5; do
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix octave_rect_band${band} \
            --num-freqband ${band} \
            --config conf/noise_vocoded_speech_rect.conf
    done
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    echo "stage 2: Generate some types of noise-vocoded speechs based on octave bands (extracted by hilbert trans.)"
    for band in 1 2 3 4 5; do
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix octave_hilbert_band${band} \
            --num-freqband ${band} \
            --config conf/noise_vocoded_speech_hilbert.conf
    done
fi

if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
    echo "stage 3: Generate some types of noise-vocoded speechs based on user-defined bands (extracted by half-rect.)"
    for band in 1 2 3 4 5; do
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix user_rect_band${band} \
            --num-freqband ${band} \
            --config conf/noise_vocoded_speech_user.conf
    done
fi

if [ ${stage} -le 4 ] && [ ${stop_stage} -ge 4 ]; then
    echo "stage 4: Generate some types of noise-vocoded speechs based on ERB without step (extracted by half-rect.)"
    for band in `seq 1 30`; do
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix erb_rect_band${band} \
            --freqband-scale-method erb \
            --freqband-limit "0_8000" \
            --erb-band-number-limit "3_35" \
            --erb-band-number-step 1 \
            --num-freqband ${band} \
            --config conf/noise_vocoded_speech_rect.conf
    done
fi

if [ ${stage} -le 5 ] && [ ${stop_stage} -ge 5 ]; then
    echo "stage 5: Generate some types of noise-vocoded speechs based on ERB with step 2 (extracted by half-rect.)"
    for band in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix erb_rect_band${band}_step2 \
            --freqband-scale-method erb \
            --freqband-limit "0_8000" \
            --erb-band-number-limit "3_35" \
            --erb-band-number-step 2 \
            --num-freqband ${band} \
            --config conf/noise_vocoded_speech_rect.conf
    done
fi
