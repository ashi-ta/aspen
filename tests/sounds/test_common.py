import numpy as np
import pytest

from aspen.sounds.am_tone import AmTone, am_tone
from aspen.sounds.click_train_pitch import ClickTrainPitch, click_train_pitch
from aspen.sounds.colored_noise import ColoredNoise, colored_noise
from aspen.sounds.complex_tone import ComplexTone, complex_tone
from aspen.sounds.filtered_noise import FilteredNoise, filtered_noise
from aspen.sounds.fm_tone import FmTone, fm_tone
from aspen.sounds.pure_tone import PureTone, pure_tone

SOUNDS = [
    (AmTone, am_tone),
    (ClickTrainPitch, click_train_pitch),
    (ColoredNoise, colored_noise),
    (ComplexTone, complex_tone),
    (FilteredNoise, filtered_noise),
    (FmTone, fm_tone),
    (PureTone, pure_tone),
]


@pytest.mark.parametrize("cls, func", SOUNDS)
def test_class_function_default(cls, func):
    np.random.seed(0)
    data_from_cls = cls()()
    np.random.seed(0)
    data_from_func = func()
    np.testing.assert_array_equal(data_from_cls, data_from_func)


@pytest.mark.parametrize("cls, func", SOUNDS)
def test_duration(cls, func):
    # first augment is always duration
    short_tone = func([500])
    long_tone = func([1000])
    assert 2 * len(short_tone[0]) == len(long_tone[0])
    short_tone = cls([500])()
    long_tone = cls([1000])()
    assert 2 * len(short_tone[0]) == len(long_tone[0])


@pytest.mark.parametrize("cls, func", SOUNDS)
def test_sampling_frequency(cls, func):
    short_tone = func(samp_freq=16000)
    long_tone = func(samp_freq=32000)
    assert 2 * len(short_tone[0]) == len(long_tone[0])
    short_tone = cls(samp_freq=16000)()
    long_tone = cls(samp_freq=32000)()
    assert 2 * len(short_tone[0]) == len(long_tone[0])
