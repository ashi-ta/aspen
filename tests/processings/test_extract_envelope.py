import argparse

import numpy as np
import pytest

from aspen.processings.extract_envelope import (ExtractEnvelope,
                                                extract_envelope)
from aspen.sounds.am_tone import am_tone

# PARAMS = [("hilbert"), ("rect")]
PARAMS = [
    ("hilbert", 16.0, "fir", 512, "hann", 16000),
    ("rect", 16.0, "fir", 512, "hann", 16000),
    ("hilbert", 32.0, "fir", 512, "hann", 16000),
    ("hilbert", 16.0, "iir", 14, "hann", 16000),
    ("hilbert", 16.0, "fir", 512, "hamming", 16000),
]


@pytest.fixture(scope="module")
def am_data():
    return am_tone(freq=[5000], modulation_freq=[5], depth=[100])[0]


@pytest.fixture(scope="module")
def am_data_expected():
    t = np.arange(0, 16000) / 16000
    return 0.5 * np.sin(2 * np.pi * 5 * t + np.radians(270)) + 0.5


def test_raise_method_valueerror(am_data):
    with pytest.raises(ValueError):
        extract_envelope(am_data, method="dummy")
    with pytest.raises(ValueError):
        ExtractEnvelope(extract_envelope_method="dummy")(am_data)


def test_default(am_data, am_data_expected):
    indata = am_data.copy()
    out = extract_envelope(indata)
    np.testing.assert_allclose(out, am_data_expected, atol=1e-2)

    indata = am_data.copy()
    out = ExtractEnvelope()(indata)
    np.testing.assert_allclose(out, am_data_expected, atol=1e-2)


# @pytest.mark.parametrize("method", PARAMS)
@pytest.mark.parametrize(
    "method, lpf_freq, lpf_impulse_response, lpf_filter_order, lpf_fir_window, samp_freq",
    PARAMS,
)
def test_params(
    am_data,
    am_data_expected,
    method,
    lpf_freq,
    lpf_impulse_response,
    lpf_filter_order,
    lpf_fir_window,
    samp_freq,
):
    indata = am_data.copy()
    out = extract_envelope(indata, method=method)
    np.testing.assert_allclose(out, am_data_expected, atol=1e-2)

    indata = am_data.copy()
    out = ExtractEnvelope(extract_envelope_method=method)(indata)
    np.testing.assert_allclose(out, am_data_expected, atol=1e-2)


@pytest.mark.parametrize(
    "method, lpf_freq, lpf_impulse_response, lpf_filter_order, lpf_fir_window, samp_freq",
    PARAMS,
)
def test_arguments(
    method, lpf_freq, lpf_impulse_response, lpf_filter_order, lpf_fir_window, samp_freq
):
    parser = argparse.ArgumentParser()
    ExtractEnvelope.add_arguments(parser)
    args = parser.parse_args(
        [
            "--extract-envelope-method",
            str(method),
            "--extract-envelope-lpf-freq",
            str(lpf_freq),
            "--extract-envelope-lpf-impulse-response",
            str(lpf_impulse_response),
            "--extract-envelope-lpf-filter-order",
            str(lpf_filter_order),
            "--extract-envelope-lpf-fir-window",
            str(lpf_fir_window),
        ]
    )

    clsobj = ExtractEnvelope(
        extract_envelope_method=args.extract_envelope_method,
        extract_envelope_lpf_freq=args.extract_envelope_lpf_freq,
        extract_envelope_lpf_impulse_response=args.extract_envelope_lpf_impulse_response,
        extract_envelope_lpf_filter_order=args.extract_envelope_lpf_filter_order,
        extract_envelope_lpf_fir_window=args.extract_envelope_lpf_fir_window,
        samp_freq=samp_freq,
    )
    assert clsobj.method == method
    assert clsobj.lpf_freq == lpf_freq
    assert clsobj.lpf_impulse_response == lpf_impulse_response
    assert clsobj.lpf_filter_order == lpf_filter_order
    assert clsobj.lpf_fir_window == lpf_fir_window
    assert clsobj.samp_freq == samp_freq
