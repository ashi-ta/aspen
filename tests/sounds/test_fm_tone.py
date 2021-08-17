import argparse

import pytest

from aspen.sounds.fm_tone import FmTone, fm_tone

PARAMS = [
    ([1000], [500], ["sin"], [2], [25], 1, 16000),
    ([1000], [440], ["upward"], [2], [25], 1, 16000),
    ([1000], [440], ["downward"], [2], [25], 1, 16000),
    ([1000], [440], ["updown"], [2], [25], 1, 16000),
    ([1000], [440], ["downup"], [2], [25], 1, 16000),
    ([1000], [440], ["sin"], [5], [25], 1, 16000),
    ([1000], [440], ["sin"], [2], [50], 1, 16000),
]


@pytest.fixture(scope="module")
def data_from_cls():
    return FmTone()()


def test_num_signals():
    dummy1 = [100, 100]
    dummy2 = ["sin", "sin"]
    two_signals = fm_tone(dummy1, dummy1, dummy2, dummy1, dummy1, 2)
    assert len(two_signals) == 2
    two_signals = FmTone(dummy1, dummy1, dummy2, dummy1, dummy1, 2)()
    assert len(two_signals) == 2


def test_raise_depth_valueerror():
    with pytest.raises(ValueError):
        fm_tone(method=["dummy"])
    with pytest.raises(ValueError):
        FmTone(fm_tone_method=["dummy"])()


@pytest.mark.parametrize(
    "duration, freq, method, modulation_freq, freq_excursion, num_signals, samp_freq",
    PARAMS,
)
def test_not_equal_with_default(
    data_from_cls,
    duration,
    freq,
    method,
    modulation_freq,
    freq_excursion,
    num_signals,
    samp_freq,
):
    tone = fm_tone(
        duration, freq, method, modulation_freq, freq_excursion, num_signals, samp_freq
    )
    assert (data_from_cls[0] != tone[0]).any()
    tone = FmTone(
        duration, freq, method, modulation_freq, freq_excursion, num_signals, samp_freq
    )()
    assert (data_from_cls[0] != tone[0]).any()


@pytest.mark.parametrize(
    "duration, freq, method, modulation_freq, freq_excursion, num_signals, samp_freq",
    PARAMS,
)
def test_arguments(
    duration,
    freq,
    method,
    modulation_freq,
    freq_excursion,
    num_signals,
    samp_freq,
):
    parser = argparse.ArgumentParser()
    FmTone.add_arguments(parser)
    args = parser.parse_args(
        [
            "--fm-tone-duration",
            str(duration[0]),
            "--fm-tone-freq",
            str(freq[0]),
            "--fm-tone-method",
            str(method[0]),
            "--fm-tone-modulation-freq",
            str(modulation_freq[0]),
            "--fm-tone-freq-excursion",
            str(freq_excursion[0]),
            "--fm-tone-num-signals",
            str(num_signals),
        ]
    )
    clsobj = FmTone(
        fm_tone_duration=args.fm_tone_duration,
        fm_tone_freq=args.fm_tone_freq,
        fm_tone_method=args.fm_tone_method,
        fm_tone_modulation_freq=args.fm_tone_modulation_freq,
        fm_tone_freq_excursion=args.fm_tone_freq_excursion,
        fm_tone_num_signals=args.fm_tone_num_signals,
        samp_freq=samp_freq,
    )
    assert clsobj.duration == duration
    assert clsobj.freq == freq
    assert clsobj.method == method
    assert clsobj.modulation_freq == modulation_freq
    assert clsobj.freq_excursion == freq_excursion
    assert clsobj.num_signals == num_signals
    assert clsobj.samp_freq == samp_freq
