import argparse

import numpy as np
import pytest

from aspen.processings.amplitude_maximize import AmplitudeMaximize, amplitude_maximize


@pytest.fixture(scope="module")
def sin_data():
    t = np.arange(0, 16000) / 16000
    return 0.1 * np.sin(2 * np.pi * 440 * t, dtype=np.float64)


def test_raise_depth_valueerror(sin_data):
    with pytest.raises(ValueError):
        amplitude_maximize(sin_data, maximum_num=0)
    with pytest.raises(ValueError):
        AmplitudeMaximize(amplitude_maximize_maximum_num=0)(sin_data)


def test_default(sin_data):
    indata = sin_data.copy()
    out = amplitude_maximize(indata)
    np.testing.assert_allclose(10 * sin_data, out)

    indata = sin_data.copy()
    out = AmplitudeMaximize()(indata)
    np.testing.assert_allclose(10 * sin_data, out)


def test_params(sin_data):
    indata = sin_data.copy()
    out = amplitude_maximize(indata, 0.5)
    np.testing.assert_allclose(5 * sin_data, out)

    indata = sin_data.copy()
    out = AmplitudeMaximize(0.5)(indata)
    np.testing.assert_allclose(5 * sin_data, out)


def test_arguments():
    parser = argparse.ArgumentParser()
    AmplitudeMaximize.add_arguments(parser)
    args = parser.parse_args(
        [
            "--amplitude-maximize-maximum-num",
            "0.5",
        ]
    )
    clsobj = AmplitudeMaximize(
        amplitude_maximize_maximum_num=args.amplitude_maximize_maximum_num
    )
    assert clsobj.maximum_num == 0.5
