import numpy as np
import pytest

from aspen.utils.freqband import erb_band, octave_band


@pytest.mark.parametrize(
    "lower_freq, upper_freq, samp_freq, expected",
    [
        (0, 8000, 16000, [16, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000]),
        (500, 8000, 16000, [500, 1000, 2000, 4000, 8000]),
    ],
)
def test_octave_band(lower_freq, upper_freq, samp_freq, expected):
    octcenter, octcutoff = octave_band(lower_freq, upper_freq, samp_freq)
    np.testing.assert_array_equal(octcenter, expected)
    assert len(octcutoff) == len(expected)


def test_raise_octave_band_valueerror():
    with pytest.raises(ValueError):
        octave_band(lower_freq=-10)
    with pytest.raises(ValueError):
        octave_band(lower_freq=0, upper_freq=10000, samp_freq=16000)


@pytest.mark.parametrize(
    "lower_band, upper_band, lower_freq, upper_freq, samp_freq, expected_length",
    [(3, 35, 0, 8000, 16000, 31), (0, 50, 500, 8000, 16000, 23)],
)
def test_erb_band(
    lower_band, upper_band, lower_freq, upper_freq, samp_freq, expected_length
):
    bands = erb_band(lower_band, upper_band, lower_freq, upper_freq, samp_freq)
    assert len(bands) == expected_length


def test_erb_band_value():
    sample = [
        123.56048495,
        163.72621508,
        208.47002671,
        258.31372863,
        313.83860524,
        375.69219567,
        444.59584537,
    ]
    bands = erb_band(lower_freq=100, upper_freq=500)
    np.testing.assert_almost_equal(bands, sample)


def test_raise_erb_band_valueerror():
    with pytest.raises(ValueError):
        erb_band(lower_freq=-10)
    with pytest.raises(ValueError):
        erb_band(lower_freq=0, upper_freq=10000, samp_freq=16000)
