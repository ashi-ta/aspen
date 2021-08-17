import argparse

import numpy as np
import pytest

from aspen.processings.normalize import Normalize, normalize


@pytest.fixture(scope="module")
def white_noise():
    np.random.seed(0)
    x = np.random.normal(loc=0, scale=1, size=[16000]).astype(np.float64)
    return x


def test_raise_method_valueerror(white_noise):
    with pytest.raises(ValueError):
        normalize(white_noise, method="dummy")
    with pytest.raises(ValueError):
        Normalize(normalize_method="dummy")(white_noise)


def test_default(white_noise):
    indata = white_noise.copy()
    out = normalize(indata)
    np.testing.assert_allclose(out.mean(), 0, atol=1e-8)
    np.testing.assert_allclose(np.std(out), 1, atol=1e-8)

    indata = white_noise.copy()
    out = Normalize()(indata)
    np.testing.assert_allclose(out.mean(), 0, atol=1e-8)
    np.testing.assert_allclose(np.std(out), 1, atol=1e-8)


@pytest.mark.parametrize("method", [("zscore")])
def test_params(white_noise, method):
    indata = white_noise.copy()
    out = normalize(indata, method)
    np.testing.assert_allclose(out.mean(), 0, atol=1e-8)
    np.testing.assert_allclose(np.std(out), 1, atol=1e-8)

    indata = white_noise.copy()
    out = Normalize(method)(indata)
    np.testing.assert_allclose(out.mean(), 0, atol=1e-8)
    np.testing.assert_allclose(np.std(out), 1, atol=1e-8)


@pytest.mark.parametrize("method", [("zscore")])
def test_arguments(method):
    parser = argparse.ArgumentParser()
    Normalize.add_arguments(parser)
    args = parser.parse_args(
        [
            "--normalize-method",
            method,
        ]
    )
    clsobj = Normalize(normalize_method=args.normalize_method)
    assert clsobj.method == method
