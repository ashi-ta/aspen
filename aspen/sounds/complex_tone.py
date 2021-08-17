#!/usr/bin/env python3
# encoding: utf-8
"""Complex tone"""

from logging import getLogger
from typing import List, Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_sound_interface import AbsSoundInterface
from aspen.processings.declip import declip

logger = getLogger(__name__)


class ComplexTone(AbsCommonInterface, AbsSoundInterface):
    """Generate complex tone.

    Args:
        complex_tone_duration: The duration of complex tone in millisecond.
            Defaults to [1000].
        complex_tone_fundamental_freq: The fundamental frequency of complex tone in Hz.
            This value determines the interval of each frequency peak.
            Defaults to [440].
        complex_tone_num_harmonics: The number of harmonics.
            Defaults to [10].
        complex_tone_first_harmonic_freq: The frequency of first harmonics.
            When this value is not same value as `--complex-tone-fundamental-freq`
            or a multiple of `--complex-tone-fundamental-freq`,
            the output signal becomes inharmonic. Defaults to [440].
        complex_tone_harmonics_amp: Relative amplitude of each harmonics.
            The format is like `2_1_1_1` which is meant that
            the first harmonics has twice as much amplitude as the other three harmonics.
            Defaults to ["1"] which generates the same amplitude signal for all harmonics.
        complex_tone_tilt_type: Type of spectral tilt.
            `up`, `down` means 6, -6 dB/Oct, respectively.
            `default` will do nothing.
        complex_tone_num_signals: Number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        complex_tone_duration: Sequence[float] = [1000],
        complex_tone_fundamental_freq: Sequence[float] = [440],
        complex_tone_num_harmonics: Sequence[int] = [10],
        complex_tone_first_harmonic_freq: Sequence[float] = [440],
        complex_tone_harmonics_amp: Sequence[str] = ["1"],
        complex_tone_tilt_type: Sequence[str] = ["default"],
        complex_tone_num_signals: int = 1,
        samp_freq: int = 16000,
    ):
        self.duration = complex_tone_duration
        self.fundamental_freq = complex_tone_fundamental_freq
        self.num_harmonics = complex_tone_num_harmonics
        self.first_harmonic_freq = complex_tone_first_harmonic_freq
        self.harmonics_amp = complex_tone_harmonics_amp
        self.tilt_type = complex_tone_tilt_type
        self.num_signals = complex_tone_num_signals
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Complex tone setting")
        group.add_argument(
            "--complex-tone-duration",
            type=float,
            default=[1000],
            nargs="*",
            help="Duration of complex tone in millisecond",
        )
        group.add_argument(
            "--complex-tone-fundamental-freq",
            type=float,
            default=[440],
            nargs="*",
            help="Fundamental frequency of complex tone in Hz."
            "This value determines the interval of each frequency peak.",
        )
        group.add_argument(
            "--complex-tone-num-harmonics",
            type=int,
            default=[10],
            nargs="*",
            help="Number of harmonics",
        )
        group.add_argument(
            "--complex-tone-first-harmonic-freq",
            type=float,
            default=[440],
            nargs="*",
            help="Frequency of first harmonics."
            "When this value is not same value as `--complex-tone-fundamental-freq`"
            "or a multiple of `--complex-tone-fundamental-freq`, "
            "the output signal becomes inharmonic.",
        )
        group.add_argument(
            "--complex-tone-harmonics-amp",
            type=str,
            default=["1"],
            nargs="*",
            help="Relative amplitude of each harmonics."
            "The format is like `2_1_1_1` which is meant that"
            "the first harmonics has twice as much amplitude as the other three harmonics.",
        )
        group.add_argument(
            "--complex-tone-tilt-type",
            type=str,
            default=["default"],
            nargs="*",
            choices=["up", "down", "default"],
            help="Type of spectral tilt."
            "`up`, `down` means 6, -6 dB/Oct, respectively."
            "`default` will do nothing.",
        )
        group.add_argument(
            "--complex-tone-num-signals",
            type=int,
            default=1,
            help="Number of signals. If this value greater than 2,"
            "the other arguments should contain 2 types.",
        )
        return parser

    def _generate_each(self, idx: int) -> np.ndarray:
        duration = int(self.duration[idx] * self.samp_freq / 1000)
        fundamental_freq = self.fundamental_freq[idx]
        num_harmonics = self.num_harmonics[idx]
        first_harmonic_freq = self.first_harmonic_freq[idx]
        harmonics_amp = np.array(self.harmonics_amp[idx].split("_")).astype(np.float64)
        tilt_type = self.tilt_type[idx]

        if (harmonics_amp == np.ones(1)).all():
            harmonics_amp = np.ones(num_harmonics)
        else:
            if harmonics_amp.shape[0] != num_harmonics:
                raise ValueError(
                    "Length of harmonics_amp must be equal with num_harmonics, but got {}".format(
                        len(harmonics_amp)
                    )
                )

        t = np.arange(0, duration) / self.samp_freq
        x = np.zeros(duration, dtype=np.float64)
        for i in range(num_harmonics):
            x += harmonics_amp[i] * np.sin(
                2 * np.pi * first_harmonic_freq * t, dtype=np.float64
            )
            first_harmonic_freq += fundamental_freq

        if tilt_type != "default":
            X = np.fft.rfft(x, norm="forward")
            if tilt_type == "up":
                x = np.fft.irfft(X * np.arange(1, X.shape[0] + 1), norm="forward").real[
                    :duration
                ]
            elif tilt_type == "down":
                x = np.fft.irfft(X / np.arange(1, X.shape[0] + 1), norm="forward").real[
                    :duration
                ]
        x = declip(x, 1.0)
        return x


def complex_tone(
    duration: Sequence[float] = [1000],
    fundamental_freq: Sequence[float] = [440],
    num_harmonics: Sequence[int] = [10],
    first_harmonic_freq: Sequence[float] = [440],
    harmonics_amp: Sequence[str] = ["1"],
    tilt_type: Sequence[str] = ["default"],
    num_signals: int = 1,
    samp_freq: int = 16000,
) -> List[np.ndarray]:
    """Generate complex tone.

    Args:
        duration: The duration of complex tone in millisecond.
            Defaults to [1000].
        fundamental_freq: The fundamental frequency of complex tone in Hz.
            This value determines the interval of each frequency peak.
            Defaults to [440].
        num_harmonics: The number of harmonics.
            Defaults to [10].
        first_harmonic_freq: The frequency of first harmonics.
            When this value is not same value as `--complex-tone-fundamental-freq`
            or a multiple of `--complex-tone-fundamental-freq`,
            the output signal becomes inharmonic. Defaults to [440].
        harmonics_amp: Relative amplitude of each harmonics.
            The format is like `2_1_1_1` which is meant that
            the first harmonics has twice as much amplitude as the other three harmonics.
            Defaults to ["1"] which generates the same amplitude signal for all harmonics.
        tilt_type: Type of spectral tilt.
            `up`, `down` means 6, -6 dB/Oct, respectively.
            `default` will do nothing.
        num_signals: Number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.

    Returns:
        Output signals.
    """

    return ComplexTone(
        duration,
        fundamental_freq,
        num_harmonics,
        first_harmonic_freq,
        harmonics_amp,
        tilt_type,
        num_signals,
        samp_freq,
    )()
