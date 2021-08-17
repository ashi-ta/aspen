#!/bin/bash

. ./path.sh || exit 1;

stage=1
stop_stage=100
verbose=0

if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
    echo "stage 1: Generate some types of tone"
    for types in pure_tone am_tone fm_tone_sin fm_tone_upward fm_tone_downward fm_tone_updown complex_tone; do
        generate.py \
            --verbose ${verbose} \
            --config conf/identity/${types}.conf
    done
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    echo "stage 2: Generate all types of colored noise"
    for color in white pink blue brown violet; do
        generate.py \
            --verbose ${verbose} \
            --suffix ${color}_noise \
            --colored-noise-color ${color} \
            --config conf/identity/colored_noise.conf
    done
fi

if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
    echo "stage 3: Generate all types of filtered noise"
    for btype in lowpass highpass; do
        generate.py \
            --verbose ${verbose} \
            --suffix filtered_noise_${btype}_800hz \
            --filtered-noise-btype ${btype} \
            --filtered-noise-filter-freq 800 \
            --config conf/identity/filtered_noise.conf
    done

    for btype in bandpass bandstop; do
        generate.py \
            --verbose ${verbose} \
            --suffix filtered_noise_${btype}_800-1200hz \
            --filtered-noise-btype ${btype} \
            --filtered-noise-filter-freq "800_1200" \
            --config conf/identity/filtered_noise.conf
    done
fi

if [ ${stage} -le 4 ] && [ ${stop_stage} -ge 4 ]; then
    echo "stage 4: Generate some types of click trian pitch"
    # this configuration means 500, 1000 and 2000Hz, respectively
    for click_interval in 2 1 0.5; do
        generate.py \
            --verbose ${verbose} \
            --suffix click_train_pitch_interval${click_interval}ms \
            --click-train-pitch-interval ${click_interval} \
            --config conf/identity/click_train_pitch.conf
    done
fi

