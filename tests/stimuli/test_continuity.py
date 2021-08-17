import argparse

import numpy as np
import pytest

from aspen.stimuli.continuity import Continuity

PARAMS = [
    (16000, 200, 100, "replace", 10, 20),
    (16000, 100, 200, "replace", 10, 20),
    (16000, 100, 100, "silent", 10, 20),
    (16000, 100, 100, "overlap", 10, 20),
    (16000, 100, 100, "replace", 5, 20),
    (16000, 100, 100, "replace", 10, 10),
    (16000, 100, 104.95, "replace", 5, 20),  # test remain_t <= gap_ramp_duration
]


@pytest.fixture(scope="module")
def indata():
    t = np.arange(0, 64000) / 16000
    target = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    np.random.seed(0)
    noise = np.random.normal(loc=0, scale=1, size=[64000]).astype(np.float64)
    return [target, noise]


@pytest.fixture(scope="module")
def default_output():
    t = np.arange(0, 64000) / 16000
    target = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    np.random.seed(0)
    noise = np.random.normal(loc=0, scale=1, size=[64000]).astype(np.float64)
    return Continuity()([target, noise])


def test_raise_num_signal_valueerror():
    with pytest.raises(ValueError):
        Continuity()([np.ones(10)])
    with pytest.raises(ValueError):
        Continuity()([np.ones(10), np.ones(10), np.ones(10)])


def test_gap_method(indata):
    # head related
    target_head = indata[0][:63360].reshape(-1, 1440)[::2, 160:]
    target_tail = indata[0][63520:]
    noise_head = indata[1][:63360].reshape(-1, 1440)[1::2, 160:]
    target_overlap_head = indata[0][:63360].reshape(-1, 1440)[1::2, 160:]

    tone = Continuity(gap_method="replace")(indata)
    tone_target = tone[:63360].reshape(-1, 1440)[::2, 160:]
    tone_noise = tone[:63360].reshape(-1, 1440)[1::2, 160:]
    rel = np.mean(tone_noise / noise_head)
    np.testing.assert_array_equal(tone_target, target_head)
    np.testing.assert_allclose(tone_noise, noise_head * rel, atol=1e-7)
    tone_target = tone[63520:]
    np.testing.assert_array_equal(tone_target, target_tail)

    tone = Continuity(gap_method="silent")(indata)
    tone_target = tone[:63360].reshape(-1, 1440)[::2, 160:]
    tone_noise = tone[:63360].reshape(-1, 1440)[1::2, 160:]
    np.testing.assert_array_equal(tone_target, target_head)
    np.testing.assert_array_equal(tone_noise, np.zeros_like(tone_noise))
    tone_target = tone[63520:]
    np.testing.assert_array_equal(tone_target, target_tail)

    tone = Continuity(gap_method="overlap")(indata)
    tone_target = tone[:63360].reshape(-1, 1440)[::2, 160:]
    tone_noise = tone[:63360].reshape(-1, 1440)[1::2, 160:]
    np.testing.assert_array_equal(tone_target, target_head)
    np.testing.assert_allclose(
        tone_noise, (noise_head * rel) + target_overlap_head, atol=1e-7
    )
    tone_target = tone[63520:]
    np.testing.assert_array_equal(tone_target, target_tail)


@pytest.mark.parametrize(
    "samp_freq, target_duration, gap_duration, gap_method, gap_ramp_duration, target_snr",
    PARAMS,
)
def test_not_equal_with_default(
    default_output,
    indata,
    samp_freq,
    target_duration,
    gap_duration,
    gap_method,
    gap_ramp_duration,
    target_snr,
):
    tone = Continuity(
        samp_freq,
        target_duration,
        gap_duration,
        gap_method,
        gap_ramp_duration,
        target_snr,
    )(indata)
    assert (tone != default_output).any()


@pytest.mark.parametrize(
    "samp_freq, target_duration, gap_duration, gap_method, gap_ramp_duration, target_snr",
    PARAMS,
)
def test_arguments(
    samp_freq,
    target_duration,
    gap_duration,
    gap_method,
    gap_ramp_duration,
    target_snr,
):
    parser = argparse.ArgumentParser()
    Continuity.add_arguments(parser)
    args = parser.parse_args(
        [
            "--target-duration",
            str(target_duration),
            "--gap-duration",
            str(gap_duration),
            "--gap-method",
            str(gap_method),
            "--gap-ramp-duration",
            str(gap_ramp_duration),
            "--target-snr",
            str(target_snr),
        ]
    )
    clsobj = Continuity(
        samp_freq=samp_freq,
        target_duration=args.target_duration,
        gap_duration=args.gap_duration,
        gap_method=args.gap_method,
        gap_ramp_duration=args.gap_ramp_duration,
        target_snr=args.target_snr,
    )
    assert clsobj.samp_freq == samp_freq
    assert clsobj.target_duration == target_duration
    assert clsobj.gap_duration == gap_duration
    assert clsobj.gap_method == gap_method
    assert clsobj.gap_ramp_duration == gap_ramp_duration
    assert clsobj.target_snr == target_snr
