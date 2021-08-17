import argparse

import numpy as np
import pytest
from scipy.fft import fft, fftfreq

from aspen.sounds.filtered_noise import FilteredNoise, filtered_noise

PARAMS = [
    ([1000], ["bandpass"], ["800_1500"], ["fir"], [512], ["hann"], 1, 16000),
    ([1000], ["bandpass"], ["800_1200"], ["iir"], [2], ["hann"], 1, 16000),
    ([1000], ["bandstop"], ["800_1200"], ["fir"], [512], ["hann"], 1, 16000),
    ([1000], ["lowpass"], ["800"], ["fir"], [512], ["hann"], 1, 16000),
    ([1000], ["highpass"], ["800"], ["fir"], [512], ["hann"], 1, 16000),
]


@pytest.fixture(scope="module")
def data_from_cls():
    np.random.seed(0)
    return FilteredNoise()()


def stopfreq_amplitude(y, btype, filter_freq):
    f_freq = np.array(filter_freq.split("_")).astype(np.float64)
    # Number of sample points
    n = y.shape[0]
    # sample spacing
    t = 1.0 / 16000.0
    yf = 2.0 / n * np.abs(fft(y)[0 : n // 2])
    xf = fftfreq(n, t)[: n // 2]
    if btype == "bandpass":
        yf = yf[(xf <= f_freq[0] - 100) & (xf >= f_freq[1] + 100)]
    elif btype == "bandstop":
        yf = yf[(xf >= f_freq[0] + 100) & (xf <= f_freq[1] - 100)]
    elif btype == "lowpass":
        yf = yf[(xf >= f_freq[0] + 100)]
    elif btype == "highpass":
        yf = yf[(xf <= f_freq[0] - 100)]
    return yf


def test_num_signals():
    dummy1 = [100, 100]
    dummy2 = ["bandpass", "bandpass"]
    dummy3 = ["800_1200", "800_1200"]
    dummy4 = ["fir", "fir"]
    dummy5 = ["hann", "hann"]
    two_signals = filtered_noise(dummy1, dummy2, dummy3, dummy4, dummy1, dummy5, 2)
    assert len(two_signals) == 2
    two_signals = FilteredNoise(dummy1, dummy2, dummy3, dummy4, dummy1, dummy5, 2)()
    assert len(two_signals) == 2


def test_raise_btype_valueerror():
    with pytest.raises(ValueError):
        filtered_noise(btype=["dummy"])
    with pytest.raises(ValueError):
        FilteredNoise(filtered_noise_btype=["dummy"])()


def test_raise_filter_freq_valueerror():
    with pytest.raises(ValueError):
        filtered_noise(filter_freq=["dummy"])
    with pytest.raises(ValueError):
        FilteredNoise(filtered_noise_filter_freq=["dummy"])()


def test_raise_impulse_response_valueerror():
    with pytest.raises(ValueError):
        filtered_noise(filter_impulse_response=["dummy"])
    with pytest.raises(ValueError):
        FilteredNoise(filtered_noise_filter_impulse_response=["dummy"])()


def test_raise_firwin_valueerror():
    with pytest.raises(ValueError):
        filtered_noise(filter_firwin=["dummy"])
    with pytest.raises(ValueError):
        FilteredNoise(filtered_noise_filter_firwin=["dummy"])()


@pytest.mark.parametrize(
    "duration, btype, filter_freq, filter_impulse_response, filter_order, filter_firwin, num_signals, samp_freq",
    PARAMS,
)
def test_not_equal_with_default(
    data_from_cls,
    duration,
    btype,
    filter_freq,
    filter_impulse_response,
    filter_order,
    filter_firwin,
    num_signals,
    samp_freq,
):
    np.random.seed(0)
    tone = filtered_noise(
        duration,
        btype,
        filter_freq,
        filter_impulse_response,
        filter_order,
        filter_firwin,
        num_signals,
        samp_freq,
    )
    assert (data_from_cls[0] != tone[0]).any()
    np.random.seed(0)
    tone = FilteredNoise(
        duration,
        btype,
        filter_freq,
        filter_impulse_response,
        filter_order,
        filter_firwin,
        num_signals,
        samp_freq,
    )()
    assert (data_from_cls[0] != tone[0]).any()


@pytest.mark.parametrize(
    "duration, btype, filter_freq, filter_impulse_response, filter_order, filter_firwin, num_signals, samp_freq",
    PARAMS,
)
def test_arguments(
    duration,
    btype,
    filter_freq,
    filter_impulse_response,
    filter_order,
    filter_firwin,
    num_signals,
    samp_freq,
):
    parser = argparse.ArgumentParser()
    FilteredNoise.add_arguments(parser)
    args = parser.parse_args(
        [
            "--filtered-noise-duration",
            str(duration[0]),
            "--filtered-noise-btype",
            str(btype[0]),
            "--filtered-noise-filter-freq",
            str(filter_freq[0]),
            "--filtered-noise-filter-impulse-response",
            str(filter_impulse_response[0]),
            "--filtered-noise-filter-order",
            str(filter_order[0]),
            "--filtered-noise-filter-firwin",
            str(filter_firwin[0]),
            "--filtered-noise-num-signals",
            str(num_signals),
        ]
    )
    clsobj = FilteredNoise(
        filtered_noise_duration=args.filtered_noise_duration,
        filtered_noise_btype=args.filtered_noise_btype,
        filtered_noise_filter_freq=args.filtered_noise_filter_freq,
        filtered_noise_filter_impulse_response=args.filtered_noise_filter_impulse_response,
        filtered_noise_filter_order=args.filtered_noise_filter_order,
        filtered_noise_filter_firwin=args.filtered_noise_filter_firwin,
        filtered_noise_num_signals=args.filtered_noise_num_signals,
        samp_freq=samp_freq,
    )
    assert clsobj.duration == duration
    assert clsobj.btype == btype
    assert clsobj.filter_freq == filter_freq
    assert clsobj.filter_impulse_response == filter_impulse_response
    assert clsobj.filter_order == filter_order
    assert clsobj.filter_firwin == filter_firwin
    assert clsobj.num_signals == num_signals
    assert clsobj.samp_freq == samp_freq


@pytest.mark.parametrize(
    "btype, filter_freq",
    [
        (["bandpass"], ["500_1000"]),
        (["bandstop"], ["500_1000"]),
        (["lowpass"], ["1000"]),
        (["highpass"], ["1000"]),
    ],
)
@pytest.mark.parametrize(
    "filter_impulse_response, filter_order",
    [
        (["fir"], [512]),
        (["iir"], [14]),  # this order is too high to filter signal (test use only)
    ],
)
def test_bandpass_power(
    btype,
    filter_freq,
    filter_impulse_response,
    filter_order,
):
    np.random.seed(0)
    tone = FilteredNoise(
        filtered_noise_btype=btype,
        filtered_noise_filter_freq=filter_freq,
        filtered_noise_filter_impulse_response=filter_impulse_response,
        filtered_noise_filter_order=filter_order,
    )()
    tonef = stopfreq_amplitude(tone[0], btype[0], filter_freq[0])
    np.testing.assert_allclose(tonef, np.zeros_like(tonef), atol=1e-3)
