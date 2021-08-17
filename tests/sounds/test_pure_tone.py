import argparse

import pytest

from aspen.sounds.pure_tone import PureTone, pure_tone

PARAMS = [
    ([1000], [500], [0], 1, 16000),
    ([1000], [440], [90], 1, 16000),
]


@pytest.fixture(scope="module")
def data_from_cls():
    return PureTone()()


def test_num_signals():
    dummy = [100, 100]
    two_signals = pure_tone(dummy, dummy, dummy, 2)
    assert len(two_signals) == 2
    two_signals = PureTone(dummy, dummy, dummy, 2)()
    assert len(two_signals) == 2


@pytest.mark.parametrize("duration, freq, phase, num_signals, samp_freq", PARAMS)
def test_not_equal_with_default(
    data_from_cls, duration, freq, phase, num_signals, samp_freq
):
    tone = pure_tone(duration, freq, phase, num_signals, samp_freq)
    assert (data_from_cls[0] != tone[0]).any()
    tone = PureTone(duration, freq, phase, num_signals, samp_freq)()
    assert (data_from_cls[0] != tone[0]).any()


@pytest.mark.parametrize("duration, freq, phase, num_signals, samp_freq", PARAMS)
def test_arguments(duration, freq, phase, num_signals, samp_freq):
    parser = argparse.ArgumentParser()
    PureTone.add_arguments(parser)
    args = parser.parse_args(
        [
            "--pure-tone-duration",
            str(duration[0]),
            "--pure-tone-freq",
            str(freq[0]),
            "--pure-tone-phase",
            str(phase[0]),
            "--pure-tone-num-signals",
            str(num_signals),
        ]
    )
    clsobj = PureTone(
        pure_tone_duration=args.pure_tone_duration,
        pure_tone_freq=args.pure_tone_freq,
        pure_tone_phase=args.pure_tone_phase,
        pure_tone_num_signals=args.pure_tone_num_signals,
        samp_freq=samp_freq,
    )
    assert clsobj.duration == duration
    assert clsobj.freq == freq
    assert clsobj.phase == phase
    assert clsobj.num_signals == num_signals
    assert clsobj.samp_freq == samp_freq
