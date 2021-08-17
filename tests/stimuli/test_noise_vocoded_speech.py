import argparse

import numpy as np
import pytest

from aspen.stimuli.noise_vocoded_speech import NoiseVocodedSpeech

DEFAULT = (
    16000,
    4,
    "octave",
    "0_600_1500_2100_4000",
    "500_8000",
    "3_35",
    1,
    "fir",
    512,
    "hann",
    "rect",
    "fir",
    512,
    "hann",
    16,
)


FREQBAND_PARAMS = [
    (32000, 3, "octave", "0_600_1500_2100_4000", "300_7000", "3_35", 1),
    (16000, 3, "octave", "0_600_1500_2100_4000", "500_8000", "3_35", 1),
    (16000, 4, "octave", "0_600_1500_2100_4000", "300_7000", "3_35", 1),
    (16000, 4, "erb", "0_600_1500_2100_4000", "500_8000", "3_35", 1),
    (16000, 4, "erb", "0_600_1500_2100_4000", "300_7000", "3_35", 1),
    (16000, 4, "erb", "0_600_1500_2100_4000", "500_8000", "10_20", 1),
    (16000, 4, "erb", "0_600_1500_2100_4000", "500_8000", "3_35", 2),
    (16000, 4, "user", "0_600_1500_2100_4000", "500_8000", "3_35", 1),
    (16000, 4, "user", "0_500_1600_2200_5000", "500_8000", "3_35", 1),
]

FILTER_PARAMS = [("fir", 256, "hann"), ("fir", 512, "hamming"), ("iir", 2, "hann")]

ENVELOPE_PARAMS = [
    ("rect", "fir", 256, "hann", 16),
    ("rect", "fir", 512, "hamming", 16),
    ("rect", "fir", 512, "hann", 30),
    ("rect", "iir", 2, "hann", 16),
    ("hilbert", "fir", 256, "hann", 16),
    ("hilbert", "fir", 512, "hamming", 16),
    ("hilbert", "fir", 512, "hann", 30),
    ("hilbert", "iir", 2, "hann", 16),
]

PARAMS = []
for params in FREQBAND_PARAMS:
    PARAMS.append(params + DEFAULT[7:])
for params in FILTER_PARAMS:
    PARAMS.append(DEFAULT[:7] + params + DEFAULT[-5:])
for params in ENVELOPE_PARAMS:
    PARAMS.append(DEFAULT[:10] + params)


@pytest.fixture(scope="module")
def indata():
    t = np.arange(0, 16000) / 16000
    target = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    np.random.seed(0)
    noise = np.random.normal(loc=0, scale=1, size=[16000]).astype(np.float64)
    return [target, noise]


@pytest.fixture(scope="module")
def default_output():
    t = np.arange(0, 16000) / 16000
    target = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    np.random.seed(0)
    noise = np.random.normal(loc=0, scale=1, size=[16000]).astype(np.float64)
    return NoiseVocodedSpeech()([target, noise])


def test_raise_num_signal_valueerror():
    with pytest.raises(ValueError):
        NoiseVocodedSpeech()([np.ones(10)])


@pytest.mark.parametrize(
    (
        "samp_freq, num_freqband, freqband_scale_method, user_freqband,"
        "freqband_limit, erb_band_number_limit, erb_band_number_step, filter_impulse_response_method,"
        "filter_order, filter_fir_window, ext_env_method, ext_env_impulse_response_method,"
        "ext_env_filter_order, ext_env_fir_window, ext_env_freq"
    ),
    PARAMS,
)
def test_not_equal_with_default(
    default_output,
    indata,
    samp_freq,
    num_freqband,
    freqband_scale_method,
    user_freqband,
    freqband_limit,
    erb_band_number_limit,
    erb_band_number_step,
    filter_impulse_response_method,
    filter_order,
    filter_fir_window,
    ext_env_method,
    ext_env_impulse_response_method,
    ext_env_filter_order,
    ext_env_fir_window,
    ext_env_freq,
):
    x = indata.copy()
    tone = NoiseVocodedSpeech(
        samp_freq,
        num_freqband,
        freqband_scale_method,
        user_freqband,
        freqband_limit,
        erb_band_number_limit,
        erb_band_number_step,
        filter_impulse_response_method,
        filter_order,
        filter_fir_window,
        ext_env_method,
        ext_env_impulse_response_method,
        ext_env_filter_order,
        ext_env_fir_window,
        ext_env_freq,
    )(x)
    assert (tone != default_output).any()


@pytest.mark.parametrize(
    (
        "samp_freq, num_freqband, freqband_scale_method, user_freqband,"
        "freqband_limit, erb_band_number_limit, erb_band_number_step, filter_impulse_response_method,"
        "filter_order, filter_fir_window, ext_env_method, ext_env_impulse_response_method,"
        "ext_env_filter_order, ext_env_fir_window, ext_env_freq"
    ),
    PARAMS,
)
def test_arguments(
    samp_freq,
    num_freqband,
    freqband_scale_method,
    user_freqband,
    freqband_limit,
    erb_band_number_limit,
    erb_band_number_step,
    filter_impulse_response_method,
    filter_order,
    filter_fir_window,
    ext_env_method,
    ext_env_impulse_response_method,
    ext_env_filter_order,
    ext_env_fir_window,
    ext_env_freq,
):
    parser = argparse.ArgumentParser()
    NoiseVocodedSpeech.add_arguments(parser)
    args = parser.parse_args(
        [
            "--num-freqband",
            str(num_freqband),
            "--freqband-scale-method",
            str(freqband_scale_method),
            "--user-freqband",
            str(user_freqband),
            "--freqband-limit",
            str(freqband_limit),
            "--erb-band-number-limit",
            str(erb_band_number_limit),
            "--erb-band-number-step",
            str(erb_band_number_step),
            "--filter-impulse-response-method",
            str(filter_impulse_response_method),
            "--filter-order",
            str(filter_order),
            "--filter-fir-window",
            str(filter_fir_window),
            "--ext-env-method",
            str(ext_env_method),
            "--ext-env-impulse-response-method",
            str(ext_env_impulse_response_method),
            "--ext-env-filter-order",
            str(ext_env_filter_order),
            "--ext-env-fir-window",
            str(ext_env_fir_window),
            "--ext-env-freq",
            str(ext_env_freq),
        ]
    )
    clsobj = NoiseVocodedSpeech(
        samp_freq=samp_freq,
        num_freqband=args.num_freqband,
        freqband_scale_method=args.freqband_scale_method,
        user_freqband=args.user_freqband,
        freqband_limit=args.freqband_limit,
        erb_band_number_limit=args.erb_band_number_limit,
        erb_band_number_step=args.erb_band_number_step,
        filter_impulse_response_method=args.filter_impulse_response_method,
        filter_order=args.filter_order,
        filter_fir_window=args.filter_fir_window,
        ext_env_method=args.ext_env_method,
        ext_env_impulse_response_method=args.ext_env_impulse_response_method,
        ext_env_filter_order=args.ext_env_filter_order,
        ext_env_fir_window=args.ext_env_fir_window,
        ext_env_freq=args.ext_env_freq,
    )
    assert clsobj.samp_freq == samp_freq
    assert clsobj.num_freqband == num_freqband
    assert clsobj.freqband_scale_method == freqband_scale_method
    assert clsobj.user_freqband == user_freqband
    assert clsobj.freqband_limit == freqband_limit
    assert clsobj.erb_band_number_limit == erb_band_number_limit
    assert clsobj.erb_band_number_step == erb_band_number_step
    assert clsobj.filter_impulse_response_method == filter_impulse_response_method
    assert clsobj.filter_order == filter_order
    assert clsobj.filter_fir_window == filter_fir_window
    assert clsobj.ext_env_method == ext_env_method
    assert clsobj.ext_env_impulse_response_method == ext_env_impulse_response_method
    assert clsobj.ext_env_filter_order == ext_env_filter_order
    assert clsobj.ext_env_fir_window == ext_env_fir_window
    assert clsobj.ext_env_freq == ext_env_freq
