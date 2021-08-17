import argparse

import numpy as np
import pytest
from scipy.fft import fft, fftfreq

from aspen.processings.declip import declip
from aspen.processings.filter_signal import FilterSignal, filter_signal

PARAMS = [
    ("bandpass", "800_1500", "fir", 512, "hann", 16000),
    ("bandpass", "800_1200", "iir", 2, "hann", 16000),
    ("bandstop", "800_1200", "fir", 512, "hann", 16000),
    ("lowpass", "800", "fir", 512, "hann", 16000),
    ("highpass", "800", "fir", 512, "hann", 16000),
]


@pytest.fixture(scope="module")
def white_noise():
    np.random.seed(0)
    x = np.random.normal(loc=0, scale=1, size=[16000]).astype(np.float64)
    return x


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


def test_raise_btype_valueerror(white_noise):
    with pytest.raises(ValueError):
        filter_signal(white_noise, filter_freq=500, btype="dummy")
    with pytest.raises(ValueError):
        FilterSignal(filter_signal_filter_freq=500, filter_signal_btype="dummy")(
            white_noise
        )


def test_raise_filter_freq_valueerror(white_noise):
    with pytest.raises(ValueError):
        filter_signal(white_noise, filter_freq="dummy", btype="bandpass")
    with pytest.raises(ValueError):
        FilterSignal(filter_signal_filter_freq="dummy", filter_signal_btype="bandpass")(
            white_noise
        )


def test_raise_impulse_response_valueerror(white_noise):
    with pytest.raises(ValueError):
        filter_signal(
            white_noise, filter_freq=500, btype="bandpass", impulse_response="dummy"
        )
    with pytest.raises(ValueError):
        FilterSignal(
            filter_signal_filter_freq=500,
            filter_signal_btype="bandpass",
            filter_signal_impulse_response="dummy",
        )(white_noise)


def test_raise_firwin_valueerror(white_noise):
    with pytest.raises(ValueError):
        filter_signal(white_noise, filter_freq=500, btype="bandpass", firwindow="dummy")
    with pytest.raises(ValueError):
        FilterSignal(
            filter_signal_filter_freq=500,
            filter_signal_btype="bandpass",
            filter_signal_firwindow="dummy",
        )(white_noise)


@pytest.mark.parametrize(
    "btype, filter_freq, impulse_response, filter_order, firwindow, samp_freq",
    PARAMS,
)
def test_not_equal_with_default(
    white_noise,
    btype,
    filter_freq,
    impulse_response,
    filter_order,
    firwindow,
    samp_freq,
):
    indata = white_noise.copy()
    indata = filter_signal(
        indata,
        btype,
        filter_freq,
        impulse_response,
        filter_order,
        firwindow,
        samp_freq,
    )
    indata = declip(indata, 1.0)
    assert (white_noise != indata).any()

    indata = white_noise.copy()
    indata = FilterSignal(
        btype,
        filter_freq,
        impulse_response,
        filter_order,
        firwindow,
        samp_freq,
    )(indata)
    indata = declip(indata, 1.0)
    assert (white_noise != indata).any()


@pytest.mark.parametrize(
    "btype, filter_freq, impulse_response, filter_order, firwindow, samp_freq",
    PARAMS,
)
def test_arguments(
    btype,
    filter_freq,
    impulse_response,
    filter_order,
    firwindow,
    samp_freq,
):
    parser = argparse.ArgumentParser()
    FilterSignal.add_arguments(parser)
    args = parser.parse_args(
        [
            "--filter-signal-btype",
            str(btype),
            "--filter-signal-filter-freq",
            str(filter_freq),
            "--filter-signal-impulse-response",
            str(impulse_response),
            "--filter-signal-filter-order",
            str(filter_order),
            "--filter-signal-firwindow",
            str(firwindow),
        ]
    )
    clsobj = FilterSignal(
        filter_signal_btype=args.filter_signal_btype,
        filter_signal_filter_freq=args.filter_signal_filter_freq,
        filter_signal_impulse_response=args.filter_signal_impulse_response,
        filter_signal_filter_order=args.filter_signal_filter_order,
        filter_signal_firwindow=args.filter_signal_firwindow,
        samp_freq=samp_freq,
    )
    assert clsobj.btype == btype
    assert clsobj.filter_freq == filter_freq
    assert clsobj.impulse_response == impulse_response
    assert clsobj.filter_order == filter_order
    assert clsobj.firwindow == firwindow
    assert clsobj.samp_freq == samp_freq


@pytest.mark.parametrize(
    "btype, filter_freq",
    [
        ("bandpass", "500_1000"),
        ("bandstop", "500_1000"),
        ("lowpass", "1000"),
        ("highpass", "1000"),
    ],
)
@pytest.mark.parametrize(
    "impulse_response, filter_order",
    [
        ("fir", 512),
        ("iir", 14),  # this order is too high to filter signal (test use only)
    ],
)
def test_bandpass_power(
    white_noise,
    btype,
    filter_freq,
    impulse_response,
    filter_order,
):
    indata = white_noise.copy()
    indata = FilterSignal(
        filter_signal_btype=btype,
        filter_signal_filter_freq=filter_freq,
        filter_signal_impulse_response=impulse_response,
        filter_signal_filter_order=filter_order,
    )(indata)
    indata = declip(indata, 1.0)
    indataf = stopfreq_amplitude(indata, btype, filter_freq)
    np.testing.assert_allclose(indataf, np.zeros_like(indataf), atol=1e-3)
