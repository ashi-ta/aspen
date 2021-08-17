#!/usr/bin/env python3
# encoding: utf-8

from typing import Sequence, Tuple
from logging import getLogger

import numpy as np

logger = getLogger(__name__)

OCTAVE_CENTER = [16, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000, 32000]


def octave_band(
    lower_freq: float = 500, upper_freq: float = 8000, samp_freq: int = 16000
) -> Tuple[np.ndarray, Sequence[np.ndarray]]:
    """Return center frequency of 1/1 octave band and cutoff frequency of octave filter.
    Center freqency is based on nominal center frequency (ANSI S1.11)

    Args:
        lower_freq: lower limit of frequency. Defaults to 500.
        upper_freq: upper limit of frequency. Defaults to 8000.
        samp_freq: sampling frequency. Defaults to 16000.

    Returns:
        Center frequency of 1/1 octave band and cutoff frequency of octave filter
    """
    if lower_freq < 0 or upper_freq > (samp_freq / 2):
        raise ValueError(
            "Lower and upper frequencies must be "
            "between 0 and Nyquist frequency (sampling frequency / 2), but got lower={} and upper={}".format(
                lower_freq, upper_freq
            )
        )
    octcenter = np.array(
        [i for i in OCTAVE_CENTER if i >= lower_freq and i <= upper_freq]
    )
    octcutoff = [np.array([i / np.sqrt(2), i * np.sqrt(2)]) for i in octcenter]
    return octcenter, octcutoff


def erb_band(
    lower_band: int = 3,
    upper_band: int = 35,
    lower_freq: float = 0,
    upper_freq: float = 8000,
    samp_freq: int = 16000,
) -> np.ndarray:
    """Return Equivalent rectangular bandwidth (ERB).
    This function is based on erb2hz function of MATLAB audio Toolbox.
    (Reference: https://jp.mathworks.com/help/audio/ref/erb2hz.html)

    Args:
        lower_band: lower limit of band number. Defaults to 3.
        upper_band: upper limit of band number. Defaults to 35.
        lower_freq: lower limit of frequency. Defaults to 0.
        upper_freq: upper limit of frequency. Defaults to 8000.
        samp_freq: sampling frequency. Defaults to 16000.

    Returns:
        Equivalent rectangular bandwidth (ERB) limited by each parameters.
    """
    if lower_freq < 0 or upper_freq > (samp_freq / 2):
        raise ValueError(
            "Lower and upper frequencies must be "
            "between 0 and Nyquist frequency (sampling frequency / 2), but got lower={} and upper={}".format(
                lower_freq, upper_freq
            )
        )
    erb = np.arange(lower_band, upper_band + 1)
    a = 1000 * np.log(10) / (24.7 * 4.37)
    f = (10 ** (erb / a) - 1) / 0.00437
    f_limit = np.array([i for i in f if i >= lower_freq and i <= upper_freq])

    if f.shape[0] > f_limit.shape[0]:
        f_del = np.array([i for i in f if i <= lower_freq or i >= upper_freq])
        logger.info(
            "The number of ERB is limited by lower_freq ({}Hz) or upper_freq ({}Hz) from {} to {}.".format(
                lower_freq,
                upper_freq,
                f.shape[0],
                f_limit.shape[0],
            )
            + " The limited frequencies are {}.".format(f_del)
        )

    return f_limit
