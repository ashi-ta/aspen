#!/bin/bash

. ./path.sh || exit 1;

stage=1
stop_stage=100
verbose=0


if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
    echo "stage 1: Generate iterated rippled noises changing the noise delay"
    # this configurations will generate 500, 1000 and 2000Hz IRN
    for noise_delay in 2 1 0.5; do
        generate.py \
            --verbose ${verbose} \
            --suffix iter8_delay${noise_delay} \
            --delay ${noise_delay} \
            --config conf/iterated_rippled_noise.conf
    done
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    echo "stage 2: Generate iterated rippled noises changing the number of iteration"
    for num_iteration in 2 4 8; do
        generate.py \
            --verbose ${verbose} \
            --suffix iter${num_iteration}_delay1 \
            --num-iteration ${num_iteration} \
            --config conf/iterated_rippled_noise.conf
    done
fi
