import argparse

import numpy as np
import pytest

from aspen.stimuli.auditory_streaming import AuditoryStreaming

PARAMS = [
    (32000, 50, 60, 170, 5),
    (16000, 30, 60, 170, 5),
    (16000, 50, 100, 170, 5),
    (16000, 50, 60, 200, 5),
]


@pytest.fixture(scope="module")
def indata():
    t = np.arange(0, 800) / 16000  # generate 50ms tones
    a = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    b = np.sin(2 * np.pi * 500 * t, dtype=np.float64)
    return [a, b]


@pytest.fixture(scope="module")
def default_output():
    t = np.arange(0, 800) / 16000  # generate 50ms tones
    a = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    b = np.sin(2 * np.pi * 500 * t, dtype=np.float64)
    return AuditoryStreaming()([a, b])


def test_zero_or_not(indata):
    tone = AuditoryStreaming(
        16000,
        10,
        50,
        50,
        5,
    )(indata)
    tone = tone.reshape(-1, 800)
    tone_zero = tone[1::2, :]
    tone_nonzero = tone[
        ::2, 1:799
    ]  # ramp function transforms the first & final elements to zero
    np.testing.assert_array_equal(tone_zero, np.zeros_like(tone_zero))
    assert (tone_nonzero != np.zeros_like(tone_nonzero)).all()


def test_raise_num_signal_valueerror():
    with pytest.raises(ValueError):
        AuditoryStreaming()([np.ones(10)])
    with pytest.raises(ValueError):
        AuditoryStreaming()([np.ones(10), np.ones(10), np.ones(10)])


def test_ab_ramp_duration(indata, default_output):
    tone = AuditoryStreaming(ab_ramp_duration=10)(indata)
    assert (tone != default_output).any()


@pytest.mark.parametrize(
    "samp_freq, num_repetition, ab_interval, aba_interval, ab_ramp_duration", PARAMS
)
def test_not_equal_with_default(
    default_output,
    indata,
    samp_freq,
    num_repetition,
    ab_interval,
    aba_interval,
    ab_ramp_duration,
):
    tone = AuditoryStreaming(
        samp_freq,
        num_repetition,
        ab_interval,
        aba_interval,
        ab_ramp_duration,
    )(indata)
    assert tone.shape[0] != default_output.shape[0]


@pytest.mark.parametrize(
    "samp_freq, num_repetition, ab_interval, aba_interval, ab_ramp_duration", PARAMS
)
def test_arguments(
    samp_freq,
    num_repetition,
    ab_interval,
    aba_interval,
    ab_ramp_duration,
):
    parser = argparse.ArgumentParser()
    AuditoryStreaming.add_arguments(parser)
    args = parser.parse_args(
        [
            "--num-repetition",
            str(num_repetition),
            "--ab-interval",
            str(ab_interval),
            "--aba-interval",
            str(aba_interval),
            "--ab-ramp-duration",
            str(ab_ramp_duration),
        ]
    )
    clsobj = AuditoryStreaming(
        samp_freq=samp_freq,
        num_repetition=args.num_repetition,
        ab_interval=args.ab_interval,
        aba_interval=args.aba_interval,
        ab_ramp_duration=args.ab_ramp_duration,
    )
    assert clsobj.samp_freq == samp_freq
    assert clsobj.num_repetition == num_repetition
    assert clsobj.ab_interval == ab_interval
    assert clsobj.aba_interval == aba_interval
    assert clsobj.ab_ramp_duration == ab_ramp_duration
