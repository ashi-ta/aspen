import argparse

import numpy as np
import pytest

from aspen.processings.apply_ramp import ApplyRamp, apply_ramp


def assert_ramp_apply(x, x_ramp, duration, position, samp_freq):
    duration = int(duration * samp_freq / 1000)
    if position == "both":
        assert (x[: duration - 1] != x_ramp[: duration - 1]).any()
        assert (x[duration + 1 :] != x_ramp[duration + 1 :]).any()
        np.testing.assert_array_equal(
            x[duration + 1 : -duration - 1], x_ramp[duration + 1 : -duration - 1]
        )
    elif position == "onset":
        assert (x[: duration - 1] != x_ramp[: duration - 1]).any()
        np.testing.assert_array_equal(x[duration + 1 :], x_ramp[duration + 1 :])
    else:  # offsets
        assert (x[duration + 1 :] != x_ramp[duration + 1 :]).any()
        np.testing.assert_array_equal(x[: -duration - 1], x_ramp[: -duration - 1])


@pytest.fixture(scope="function")
def sin_data():
    t = np.arange(0, 16000) / 16000
    return np.sin(2 * np.pi * 440 * t, dtype=np.float64)


def test_raise_position_valueerror(sin_data):
    with pytest.raises(ValueError):
        apply_ramp(sin_data, duration=5, position="dummy")
    with pytest.raises(ValueError):
        ApplyRamp(apply_ramp_duration=5, apply_ramp_position="dummy")(sin_data)


def test_default(sin_data):
    indata = sin_data.copy()
    outdata = apply_ramp(indata)
    np.testing.assert_array_equal(sin_data, outdata)

    indata = sin_data.copy()
    outdata = ApplyRamp()(indata)
    np.testing.assert_array_equal(sin_data, outdata)


@pytest.mark.parametrize("duration", [(5), (10)])
@pytest.mark.parametrize("wfunction", [("linear"), ("hamming")])
@pytest.mark.parametrize("position", [("both"), ("onset"), ("offset")])
@pytest.mark.parametrize("samp_freq", [(16000), (32000)])
def test_params(sin_data, duration, wfunction, position, samp_freq):
    indata = sin_data.copy()
    outdata = apply_ramp(indata, duration, wfunction, position, samp_freq)
    assert_ramp_apply(sin_data, outdata, duration, position, samp_freq)
    indata = sin_data.copy()
    outdata = ApplyRamp(duration, wfunction, position, samp_freq)(indata)
    assert_ramp_apply(sin_data, outdata, duration, position, samp_freq)


@pytest.mark.parametrize("duration", [(5), (10)])
@pytest.mark.parametrize("wfunction", [("linear"), ("hamming")])
@pytest.mark.parametrize("position", [("both"), ("onset"), ("offset")])
@pytest.mark.parametrize("samp_freq", [(16000), (32000)])
def test_arguments(duration, wfunction, position, samp_freq):
    parser = argparse.ArgumentParser()
    ApplyRamp.add_arguments(parser)
    args = parser.parse_args(
        [
            "--apply-ramp-duration",
            str(duration),
            "--apply-ramp-wfunction",
            str(wfunction),
            "--apply-ramp-position",
            str(position),
        ]
    )
    clsobj = ApplyRamp(
        apply_ramp_duration=args.apply_ramp_duration,
        apply_ramp_wfunction=args.apply_ramp_wfunction,
        apply_ramp_position=args.apply_ramp_position,
        samp_freq=samp_freq,
    )
    assert clsobj.duration == duration
    assert clsobj.wfunction == wfunction
    assert clsobj.position == position
    assert clsobj.samp_freq == samp_freq
