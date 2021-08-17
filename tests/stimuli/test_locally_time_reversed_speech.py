import argparse

import numpy as np
import pytest

from aspen.stimuli.locally_time_reversed_speech import LocallyTimeReversedSpeech

PARAMS = [
    (32000, 50, False),
    (16000, 100, False),
    (16000, 50, True),
]


@pytest.fixture(scope="module")
def indata():
    t = np.arange(0, 16000) / 16000
    return np.sin(2 * np.pi * 440 * t, dtype=np.float64)


@pytest.fixture(scope="module")
def default_output():
    t = np.arange(0, 16000) / 16000
    x = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    return LocallyTimeReversedSpeech()([x])


def test_equal_with_input(indata):
    t = np.arange(0, 16000) / 16000
    sin_data = np.sin(2 * np.pi * 10 * t, dtype=np.float64)
    x = sin_data.copy()
    tone = LocallyTimeReversedSpeech(reverse_duration=50)([x])
    np.testing.assert_allclose(tone, sin_data, atol=1e-2)


def test_raise_num_signal_valueerror():
    with pytest.raises(ValueError):
        LocallyTimeReversedSpeech()([np.ones(10), np.ones(10)])


@pytest.mark.parametrize("samp_freq, reverse_duration, randomize", PARAMS)
def test_not_equal_with_default(
    default_output, indata, samp_freq, reverse_duration, randomize
):
    x = indata.copy()
    tone = LocallyTimeReversedSpeech(samp_freq, reverse_duration, randomize)([x])
    assert (tone != default_output).any()


@pytest.mark.parametrize("samp_freq, reverse_duration, randomize", PARAMS)
def test_arguments(samp_freq, reverse_duration, randomize):
    parser = argparse.ArgumentParser()
    LocallyTimeReversedSpeech.add_arguments(parser)
    args = parser.parse_args(
        [
            "--reverse-duration",
            str(reverse_duration),
            "--randomize",
            str(randomize),
        ]
    )
    clsobj = LocallyTimeReversedSpeech(
        samp_freq=samp_freq,
        reverse_duration=args.reverse_duration,
        randomize=args.randomize,
    )
    assert clsobj.samp_freq == samp_freq
    assert clsobj.reverse_duration == reverse_duration
    assert clsobj.randomize == randomize
