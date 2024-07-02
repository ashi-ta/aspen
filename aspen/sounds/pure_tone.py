#!/usr/bin/env python3
# encoding: utf-8
"""Pure tone"""

from logging import getLogger
from typing import List, Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_sound_interface import AbsSoundInterface

logger = getLogger(__name__)


class PureTone(AbsCommonInterface, AbsSoundInterface):
    """Generate pure tone.

    Args:
        pure_tone_duration: The duration of pure tone in millisecond.
            Defaults to [1000].
        pure_tone_freq: The frequency of pure tone in Hz.
            Defaults to [440].
        pure_tone_phase: The phase of pure tone in degree.
            Defaults to [0].
        pure_tone_num_signals: Number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        pure_tone_duration: Sequence[float] = [1000],
        pure_tone_freq: Sequence[float] = [440],
        pure_tone_phase: Sequence[float] = [0],
        pure_tone_num_signals: int = 1,
        samp_freq: int = 16000,
    ):
        self.num_signals = pure_tone_num_signals
        assert self.num_signals == len(
            pure_tone_duration
        ), f"Should specify same number of parameters for pure-tone-duration ({self.num_signals} vs. {len(pure_tone_duration)})"
        assert self.num_signals == len(
            pure_tone_freq
        ), f"Should specify same number of parameters for pure-tone-freq ({self.num_signals} vs. {len(pure_tone_freq)})"
        assert self.num_signals == len(
            pure_tone_phase
        ), f"Should specify same number of parameters ({self.num_signals} vs. {len(pure_tone_phase)})"
        self.duration = pure_tone_duration
        self.freq = pure_tone_freq
        self.phase = pure_tone_phase
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Pure tone setting")
        group.add_argument(
            "--pure-tone-duration",
            type=float,
            default=[1000],
            nargs="*",
            help="Duration of tone in millisecond",
        )
        group.add_argument(
            "--pure-tone-freq",
            type=float,
            default=[440],
            nargs="*",
            help="Frequency of tone in Hz.",
        )
        group.add_argument(
            "--pure-tone-phase",
            type=float,
            default=[0],
            nargs="*",
            help="Phase of tone in Hz.",
        )
        group.add_argument(
            "--pure-tone-num-signals",
            type=int,
            default=1,
            help="Number of signals. If this value greater than 2," "the other arguments should contain 2 types.",
        )
        return parser

    def _generate_each(self, idx: int) -> np.ndarray:
        duration = int(self.duration[idx] * self.samp_freq / 1000)
        freq = self.freq[idx]
        phase = np.deg2rad(self.phase[idx])

        t = np.arange(0, duration) / self.samp_freq
        # x(t) = A * sin(2 * pi * freq * t)
        x = np.sin(2 * np.pi * freq * t + phase, dtype=np.float64)

        return x


def pure_tone(
    duration: Sequence[float] = [1000],
    freq: Sequence[float] = [440],
    phase: Sequence[float] = [0],
    num_signals: int = 1,
    samp_freq: int = 16000,
) -> List[np.ndarray]:
    """Generate pure tone.

    Args:
        duration: The duration of pure tone in millisecond.
            Defaults to [1000].
        freq: The frequency of pure tone in Hz.
            Defaults to [440].
        phase: The phase of pure tone in degree.
            Defaults to [0].
        num_signals: Number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.

    Returns:
        Output signals.
    """
    return PureTone(duration, freq, phase, num_signals, samp_freq)()
