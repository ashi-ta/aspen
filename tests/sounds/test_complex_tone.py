import argparse

import pytest

from aspen.sounds.complex_tone import ComplexTone, complex_tone

PARAMS = [
    ([1000], [500], [10], [440], ["1"], ["default"], 1, 16000),
    ([1000], [440], [20], [440], ["1"], ["default"], 1, 16000),
    ([1000], [440], [10], [500], ["1"], ["default"], 1, 16000),
    ([1000], [440], [10], [440], ["1_2_1_2_1_2_1_2_1_2"], ["default"], 1, 16000),
    ([1000], [440], [10], [440], ["1"], ["up"], 1, 16000),
    ([1000], [440], [10], [440], ["1"], ["down"], 1, 16000),
]


@pytest.fixture(scope="module")
def data_from_cls():
    return ComplexTone()()


def test_num_signals():
    dummy1 = [100, 100]
    dummy2 = ["1", "1"]
    dummy3 = ["default", "up"]
    two_signals = complex_tone(
        dummy1,
        dummy1,
        dummy1,
        dummy1,
        dummy2,
        dummy3,
        2,
    )
    assert len(two_signals) == 2
    two_signals = ComplexTone(
        dummy1,
        dummy1,
        dummy1,
        dummy1,
        dummy2,
        dummy3,
        2,
    )()
    assert len(two_signals) == 2


def test_raise_harmonics_amp_valueerror():
    with pytest.raises(ValueError):
        complex_tone(num_harmonics=[3], harmonics_amp=["2_1"])
    with pytest.raises(ValueError):
        ComplexTone(
            complex_tone_num_harmonics=[3], complex_tone_harmonics_amp=["2_1"]
        )()


@pytest.mark.parametrize(
    "duration, fundamental_freq, num_harmonics, first_harmonic_freq, harmonics_amp, tilt_type, num_signals, samp_freq",
    PARAMS,
)
def test_not_equal_with_default(
    data_from_cls,
    duration,
    fundamental_freq,
    num_harmonics,
    first_harmonic_freq,
    harmonics_amp,
    tilt_type,
    num_signals,
    samp_freq,
):
    tone = complex_tone(
        duration,
        fundamental_freq,
        num_harmonics,
        first_harmonic_freq,
        harmonics_amp,
        tilt_type,
        num_signals,
        samp_freq,
    )
    assert (data_from_cls[0] != tone[0]).any()
    tone = ComplexTone(
        duration,
        fundamental_freq,
        num_harmonics,
        first_harmonic_freq,
        harmonics_amp,
        tilt_type,
        num_signals,
        samp_freq,
    )()
    assert (data_from_cls[0] != tone[0]).any()


@pytest.mark.parametrize(
    "duration, fundamental_freq, num_harmonics, first_harmonic_freq, harmonics_amp, tilt_type, num_signals, samp_freq",
    PARAMS,
)
def test_arguments(
    duration,
    fundamental_freq,
    num_harmonics,
    first_harmonic_freq,
    harmonics_amp,
    tilt_type,
    num_signals,
    samp_freq,
):
    parser = argparse.ArgumentParser()
    ComplexTone.add_arguments(parser)
    args = parser.parse_args(
        [
            "--complex-tone-duration",
            str(duration[0]),
            "--complex-tone-fundamental-freq",
            str(fundamental_freq[0]),
            "--complex-tone-num-harmonics",
            str(num_harmonics[0]),
            "--complex-tone-first-harmonic-freq",
            str(first_harmonic_freq[0]),
            "--complex-tone-harmonics-amp",
            str(harmonics_amp[0]),
            "--complex-tone-tilt-type",
            str(tilt_type[0]),
            "--complex-tone-num-signals",
            str(num_signals),
        ]
    )
    clsobj = ComplexTone(
        complex_tone_duration=args.complex_tone_duration,
        complex_tone_fundamental_freq=args.complex_tone_fundamental_freq,
        complex_tone_num_harmonics=args.complex_tone_num_harmonics,
        complex_tone_first_harmonic_freq=args.complex_tone_first_harmonic_freq,
        complex_tone_harmonics_amp=args.complex_tone_harmonics_amp,
        complex_tone_tilt_type=args.complex_tone_tilt_type,
        complex_tone_num_signals=args.complex_tone_num_signals,
        samp_freq=samp_freq,
    )
    assert clsobj.duration == duration
    assert clsobj.fundamental_freq == fundamental_freq
    assert clsobj.num_harmonics == num_harmonics
    assert clsobj.first_harmonic_freq == first_harmonic_freq
    assert clsobj.harmonics_amp == harmonics_amp
    assert clsobj.tilt_type == tilt_type
    assert clsobj.num_signals == num_signals
    assert clsobj.samp_freq == samp_freq
