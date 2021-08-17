#!/usr/bin/env python3
# encoding: utf-8

from typing import Optional

import numpy as np


def rms(x: np.ndarray) -> np.ndarray:
    """Calculate the root mean square of signal

    Args:
        x: Input signal

    Returns:
        Root mean square of signal
    """
    return np.sqrt(np.mean(np.square(x)))


def get_snr_noise(
    x: np.ndarray, noise: np.ndarray, snr: Optional[float] = None
) -> np.ndarray:
    """Return the noise signal with signal-to-noise ratio(SNR) by x
    `RMS_noise = RMS_x / (10 ** (SNR / 20))`
    which SNR is `20 * log10(RMS_x / RMS_noise)`

    Args:
        x: Reference signal
        noise: Target noise
        snr: Signal-to-noise ratio. Defaults to None (= do nothing).

    Returns:
        noise signal with signal-to-noise ratio(SNR) by x
    """
    if snr is None:
        return noise
    rms_noise_at_snr = rms(x) / (10 ** (snr / 20))
    return noise / rms(noise) * rms_noise_at_snr
