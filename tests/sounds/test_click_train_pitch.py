import argparse

import pytest

from aspen.sounds.click_train_pitch import ClickTrainPitch, click_train_pitch

PARAMS = [
    ([1000], [2], 1, 16000),
]


@pytest.fixture(scope="module")
def data_from_cls():
    return ClickTrainPitch()()


def test_num_signals():
    dummy = [100, 100]
    two_signals = click_train_pitch(dummy, dummy, 2)
    assert len(two_signals) == 2
    two_signals = ClickTrainPitch(dummy, dummy, 2)()
    assert len(two_signals) == 2


def test_raise_interval_valueerror():
    with pytest.raises(ValueError):
        click_train_pitch(interval=[0])
    with pytest.raises(ValueError):
        ClickTrainPitch(click_train_pitch_interval=[0])()


@pytest.mark.parametrize("duration, interval, num_signals, samp_freq", PARAMS)
def test_not_equal_with_default(
    data_from_cls, duration, interval, num_signals, samp_freq
):
    tone = click_train_pitch(duration, interval, num_signals, samp_freq)
    assert (data_from_cls[0] != tone[0]).any()
    tone = ClickTrainPitch(duration, interval, num_signals, samp_freq)()
    assert (data_from_cls[0] != tone[0]).any()


@pytest.mark.parametrize("duration, interval, num_signals, samp_freq", PARAMS)
def test_arguments(duration, interval, num_signals, samp_freq):
    parser = argparse.ArgumentParser()
    ClickTrainPitch.add_arguments(parser)
    args = parser.parse_args(
        [
            "--click-train-pitch-duration",
            str(duration[0]),
            "--click-train-pitch-interval",
            str(interval[0]),
            "--click-train-pitch-num-signals",
            str(num_signals),
        ]
    )
    clsobj = ClickTrainPitch(
        click_train_pitch_duration=args.click_train_pitch_duration,
        click_train_pitch_interval=args.click_train_pitch_interval,
        click_train_pitch_num_signals=args.click_train_pitch_num_signals,
        samp_freq=samp_freq,
    )
    assert clsobj.duration == duration
    assert clsobj.interval == interval
    assert clsobj.num_signals == num_signals
    assert clsobj.samp_freq == samp_freq
