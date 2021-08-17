import argparse

import numpy as np
import pytest

from aspen.stimuli.iterated_rippled_noise import IteratedRippledNoise

PARAMS = [
    (32000, 8, 1),
    (16000, 9, 1),
    (16000, 8, 2),
]


@pytest.fixture(scope="module")
def indata():
    np.random.seed(0)
    noise = np.random.normal(loc=0, scale=1, size=[64000]).astype(np.float64)
    return [noise]


@pytest.fixture(scope="module")
def default_output():
    np.random.seed(0)
    noise = np.random.normal(loc=0, scale=1, size=[64000]).astype(np.float64)
    return IteratedRippledNoise()([noise])


def test_raise_num_signal_valueerror():
    with pytest.raises(ValueError):
        IteratedRippledNoise()([np.ones(10), np.ones(10)])


@pytest.mark.parametrize("samp_freq, num_iteration, delay", PARAMS)
def test_addition(samp_freq, num_iteration, delay):
    input = np.ones(samp_freq)
    expected = np.repeat(
        [num_iteration], samp_freq - (delay * samp_freq / 1000) * (num_iteration - 1)
    )
    tone = IteratedRippledNoise(
        samp_freq=samp_freq, num_iteration=num_iteration, delay=delay
    )([input])
    np.testing.assert_array_equal(expected, tone)


@pytest.mark.parametrize("samp_freq, num_iteration, delay", PARAMS)
def test_not_equal_with_default(
    default_output, indata, samp_freq, num_iteration, delay
):
    tone = IteratedRippledNoise(samp_freq, num_iteration, delay)(indata)
    assert tone.shape[0] != default_output.shape[0]


@pytest.mark.parametrize("samp_freq, num_iteration, delay", PARAMS)
def test_arguments(samp_freq, num_iteration, delay):
    parser = argparse.ArgumentParser()
    IteratedRippledNoise.add_arguments(parser)
    args = parser.parse_args(
        [
            "--num-iteration",
            str(num_iteration),
            "--delay",
            str(delay),
        ]
    )
    clsobj = IteratedRippledNoise(
        samp_freq=samp_freq,
        num_iteration=args.num_iteration,
        delay=args.delay,
    )
    assert clsobj.samp_freq == samp_freq
    assert clsobj.num_iteration == num_iteration
    assert clsobj.delay == delay
