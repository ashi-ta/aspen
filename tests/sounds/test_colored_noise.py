import argparse

import numpy as np
import pytest

from aspen.sounds.colored_noise import ColoredNoise, colored_noise

PARAMS = [
    ([1000], ["pink"], 1, 16000),
    ([1000], ["blue"], 1, 16000),
    ([1000], ["brown"], 1, 16000),
    ([1000], ["violet"], 1, 16000),
]


@pytest.fixture(scope="module")
def data_from_cls():
    np.random.seed(0)
    return ColoredNoise()()


def test_num_signals():
    dummy1 = [100, 100]
    dummy2 = ["white", "white"]
    two_signals = colored_noise(dummy1, dummy2, 2)
    assert len(two_signals) == 2
    two_signals = ColoredNoise(dummy1, dummy2, 2)()
    assert len(two_signals) == 2


def test_raise_depth_valueerror():
    with pytest.raises(ValueError):
        colored_noise(color=["dummy"])
    with pytest.raises(ValueError):
        ColoredNoise(colored_noise_color=["dummy"])()


@pytest.mark.parametrize("duration, color, num_signals, samp_freq", PARAMS)
def test_not_equal_with_default(data_from_cls, duration, color, num_signals, samp_freq):
    np.random.seed(0)
    tone = colored_noise(duration, color, num_signals, samp_freq)
    assert (data_from_cls[0] != tone[0]).any()
    np.random.seed(0)
    tone = ColoredNoise(duration, color, num_signals, samp_freq)()
    assert (data_from_cls[0] != tone[0]).any()


@pytest.mark.parametrize("duration, color, num_signals, samp_freq", PARAMS)
def test_arguments(duration, color, num_signals, samp_freq):
    parser = argparse.ArgumentParser()
    ColoredNoise.add_arguments(parser)
    args = parser.parse_args(
        [
            "--colored-noise-duration",
            str(duration[0]),
            "--colored-noise-color",
            str(color[0]),
            "--colored-noise-num-signals",
            str(num_signals),
        ]
    )
    np.random.seed(0)
    clsobj = ColoredNoise(
        colored_noise_duration=args.colored_noise_duration,
        colored_noise_color=args.colored_noise_color,
        colored_noise_num_signals=args.colored_noise_num_signals,
        samp_freq=samp_freq,
    )
    assert clsobj.duration == duration
    assert clsobj.color == color
    assert clsobj.num_signals == num_signals
    assert clsobj.samp_freq == samp_freq
