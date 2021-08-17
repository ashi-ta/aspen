import argparse

import numpy as np
import pytest

from aspen.processings.declip import Declip, declip


@pytest.fixture(scope="module")
def sin_data():
    t = np.arange(0, 16000) / 16000
    return 2.0 * np.sin(2 * np.pi * 440 * t, dtype=np.float64)


def test_raise_depth_valueerror(sin_data):
    with pytest.raises(ValueError):
        declip(sin_data, thres=0)
    with pytest.raises(ValueError):
        Declip(declip_thres=0)(sin_data)


def test_default(sin_data):
    indata = sin_data.copy()
    out = declip(indata)
    np.testing.assert_allclose(0.5 * sin_data, out)

    indata = sin_data.copy()
    out = Declip()(indata)
    np.testing.assert_allclose(0.5 * sin_data, out)


def test_params(sin_data):
    indata = sin_data.copy()
    out = declip(indata, 0.5)
    np.testing.assert_allclose(0.25 * sin_data, out)

    indata = sin_data.copy()
    out = Declip(0.5)(indata)
    np.testing.assert_allclose(0.25 * sin_data, out)


def test_arguments():
    parser = argparse.ArgumentParser()
    Declip.add_arguments(parser)
    args = parser.parse_args(
        [
            "--declip-thres",
            "0.5",
        ]
    )
    clsobj = Declip(declip_thres=args.declip_thres)
    assert clsobj.thres == 0.5
