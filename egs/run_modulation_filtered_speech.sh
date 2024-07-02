#!/bin/bash

. ./path.sh || exit 1;

stage=1
stop_stage=100
verbose=0

wavlist=$1

# max_spectral_modulation = 1000 / (2 * spacing-freq) [cycles/kHz]
# e.g. max_spectral_modulation=10 when spcing_freq=50
max_spectral_modulation=10
# max_temporal_modulation = spec-samp-freq / 2 [hz]
# e.g. max_temporal_modulation=500 when spec-samp-freq=1000
max_temporal_modulation=500

CMDNAME=`basename $0`
if [ $# -ne 1 ]; then
  echo "Usage: $CMDNAME wavlist (A wavlist is a file that lists the paths of wav files in a bullet-point format.)" 1>&2
  echo "Here, sample_speech_list.txt is used." 1>&2
  wavlist=sample_speech_list.txt
fi

if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
    echo "stage 1: Generate the modulation-filtered speech with low-pass filtering in spectral modulation axis"
    temporal_stopband=0_${max_temporal_modulation}

    for lpf_freq in 1 2 4 8; do
        spectral_stopband=${lpf_freq}_${max_spectral_modulation}
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix temp${temporal_stopband}_spec${spectral_stopband} \
            --temporal-stopbands ${temporal_stopband} \
            --spectral-stopbands ${spectral_stopband} \
            --config conf/modulation_filtered_speech.conf
    done
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    echo "stage 2: Generate the modulation-filtered speech with low-pass filtering in temporal modulation axis"
    spectral_stopband=0_${max_spectral_modulation}

    for lpf_freq in 1 3 6 12 24; do
        temporal_stopband=${lpf_freq}_${max_temporal_modulation}
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix temp${temporal_stopband}_spec${spectral_stopband} \
            --temporal-stopbands ${temporal_stopband} \
            --spectral-stopbands ${spectral_stopband} \
            --config conf/modulation_filtered_speech.conf
    done
fi

if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
    echo "stage 3: Generate the modulation-filtered speech with notch filtering of two modulations"
    temporal_stopband=0_${max_temporal_modulation}
    spectral_stopband=0_${max_spectral_modulation}

    for notch_stopband in 0_1 1_3 3_7 7_15 15_31; do
        # Notch filter in spectral modulation axis
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix temp${temporal_stopband}_spec${notch_stopband} \
            --temporal-stopbands ${temporal_stopband} \
            --spectral-stopbands ${notch_stopband} \
            --config conf/modulation_filtered_speech.conf

        # Notch filter in temporal modulation axis
        generate.py \
            --verbose ${verbose} \
            --wavlist ${wavlist} \
            --suffix temp${notch_stopband}_spec${spectral_stopband} \
            --temporal-stopbands ${notch_stopband} \
            --spectral-stopbands ${spectral_stopband} \
            --config conf/modulation_filtered_speech.conf
    done
fi

if [ ${stage} -le 4 ] && [ ${stop_stage} -ge 4 ]; then
    echo "stage 4: Generate the modulation-filtered speech with core filtering"
    generate.py \
        --verbose ${verbose} \
        --wavlist ${wavlist} \
        --suffix core \
        --temporal-stopbands 7.75_${max_temporal_modulation} \
        --spectral-stopbands 3.75_${max_spectral_modulation} \
        --config conf/modulation_filtered_speech.conf
fi

