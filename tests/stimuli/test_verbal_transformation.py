import argparse

import numpy as np
import pytest

from aspen.stimuli.verbal_transformation import VerbalTransformation

PARAMS = [(50)]


@pytest.fixture(scope="module")
def indata():
    t = np.arange(0, 16000) / 16000
    return np.sin(2 * np.pi * 440 * t, dtype=np.float64)


@pytest.fixture(scope="module")
def default_output():
    t = np.arange(0, 16000) / 16000
    x = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    return VerbalTransformation()([x])


def test_equal_with_input(default_output):
    t = np.arange(0, 32000) / 16000
    sin_data = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    tone = VerbalTransformation(num_iteration=10)([sin_data])
    np.testing.assert_allclose(tone, default_output, atol=1e-3)


def test_raise_num_signal_valueerror():
    with pytest.raises(ValueError):
        VerbalTransformation()([np.ones(10), np.ones(10)])


@pytest.mark.parametrize("num_iteration", PARAMS)
def test_not_equal_with_default(default_output, indata, num_iteration):
    x = indata.copy()
    tone = VerbalTransformation(num_iteration)([x])
    assert tone.shape[0] != default_output.shape[0]


@pytest.mark.parametrize("num_iteration", PARAMS)
def test_arguments(num_iteration):
    parser = argparse.ArgumentParser()
    VerbalTransformation.add_arguments(parser)
    args = parser.parse_args(
        [
            "--num-iteration",
            str(num_iteration),
        ]
    )
    clsobj = VerbalTransformation(num_iteration=args.num_iteration)
    assert clsobj.num_iteration == num_iteration
