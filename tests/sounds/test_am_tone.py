import argparse

import numpy as np
import pytest

from aspen.sounds.am_tone import AmTone, am_tone

PARAMS = [
    ([1000], [500], [0], [440], [100], [0], 1, 16000),
    ([1000], [440], [90], [440], [100], [0], 1, 16000),
    ([1000], [440], [0], [500], [100], [0], 1, 16000),
    ([1000], [440], [0], [440], [50], [0], 1, 16000),
    ([1000], [440], [0], [440], [50], [90], 1, 16000),
]


@pytest.fixture(scope="module")
def data_from_cls():
    return AmTone()()


def test_num_signals():
    dummy = [100, 100]
    two_signals = am_tone(dummy, dummy, dummy, dummy, dummy, dummy, 2)
    assert len(two_signals) == 2
    two_signals = AmTone(dummy, dummy, dummy, dummy, dummy, dummy, 2)()
    assert len(two_signals) == 2


def test_raise_depth_valueerror():
    with pytest.raises(ValueError):
        am_tone(depth=[101])
    with pytest.raises(ValueError):
        AmTone(am_tone_depth=[101])()


def test_modulation_amplitude():
    idx = int(16000 / 5)
    out = am_tone(freq=[1000], modulation_freq=[5])[0][::idx]
    np.testing.assert_allclose(out, np.zeros_like(out))


@pytest.mark.parametrize(
    "duration, freq, phase, modulation_freq, depth, modulator_phase, num_signals, samp_freq",
    PARAMS,
)
def test_not_equal_with_default(
    data_from_cls,
    duration,
    freq,
    phase,
    modulation_freq,
    depth,
    modulator_phase,
    num_signals,
    samp_freq,
):
    tone = am_tone(
        duration,
        freq,
        phase,
        modulation_freq,
        depth,
        modulator_phase,
        num_signals,
        samp_freq,
    )
    assert (data_from_cls[0] != tone[0]).any()
    tone = AmTone(
        duration,
        freq,
        phase,
        modulation_freq,
        depth,
        modulator_phase,
        num_signals,
        samp_freq,
    )()
    assert (data_from_cls[0] != tone[0]).any()


@pytest.mark.parametrize(
    "duration, freq, phase,modulation_freq, depth, modulator_phase, num_signals, samp_freq",
    PARAMS,
)
def test_arguments(
    duration,
    freq,
    phase,
    modulation_freq,
    depth,
    modulator_phase,
    num_signals,
    samp_freq,
):
    parser = argparse.ArgumentParser()
    AmTone.add_arguments(parser)
    args = parser.parse_args(
        [
            "--am-tone-duration",
            str(duration[0]),
            "--am-tone-freq",
            str(freq[0]),
            "--am-tone-phase",
            str(phase[0]),
            "--am-tone-modulation-freq",
            str(modulation_freq[0]),
            "--am-tone-depth",
            str(depth[0]),
            "--am-tone-modulator-phase",
            str(modulator_phase[0]),
            "--am-tone-num-signals",
            str(num_signals),
        ]
    )
    clsobj = AmTone(
        am_tone_duration=args.am_tone_duration,
        am_tone_freq=args.am_tone_freq,
        am_tone_phase=args.am_tone_phase,
        am_tone_modulation_freq=args.am_tone_modulation_freq,
        am_tone_depth=args.am_tone_depth,
        am_tone_modulator_phase=args.am_tone_modulator_phase,
        am_tone_num_signals=args.am_tone_num_signals,
        samp_freq=samp_freq,
    )
    assert clsobj.duration == duration
    assert clsobj.freq == freq
    assert clsobj.phase == phase
    assert clsobj.modulation_freq == modulation_freq
    assert clsobj.depth == depth
    assert clsobj.modulator_phase == modulator_phase
    assert clsobj.num_signals == num_signals
    assert clsobj.samp_freq == samp_freq
