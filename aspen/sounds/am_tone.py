#!/usr/bin/env python3
# encoding: utf-8
"""Amplitude-modulated (AM) tone"""

from logging import getLogger
from typing import List, Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_sound_interface import AbsSoundInterface
from aspen.processings.declip import declip

logger = getLogger(__name__)


class AmTone(AbsCommonInterface, AbsSoundInterface):
    """Generate sinusoidally amplitude modulated tone.

    Args:
        am_tone_duration: Duration of am tone in millisecond.
            Defaults to [1000].
        am_tone_freq: Frequency of carrier in Hz.
            Defaults to [440].
        am_tone_phase: Phase of carrier in degree.
            Defaults to [0].
        am_tone_modulation_freq: Frequency of modulator in Hz.
            Defaults to [440].
        am_tone_depth: Depth of modulator in percentage.
            Defaults to [100].
        am_tone_modulator_phase: Phase of modulator in degree.
            Defaults to [0].
        am_tone_num_signals: Number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        am_tone_duration: Sequence[float] = [1000],
        am_tone_freq: Sequence[float] = [440],
        am_tone_phase: Sequence[float] = [0],
        am_tone_modulation_freq: Sequence[float] = [440],
        am_tone_depth: Sequence[float] = [100],
        am_tone_modulator_phase: Sequence[float] = [0],
        am_tone_num_signals: int = 1,
        samp_freq: int = 16000,
    ):
        self.duration = am_tone_duration
        self.freq = am_tone_freq
        self.phase = am_tone_phase
        self.modulation_freq = am_tone_modulation_freq
        self.depth = am_tone_depth
        self.modulator_phase = am_tone_modulator_phase
        self.num_signals = am_tone_num_signals
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("AM tone setting")
        group.add_argument(
            "--am-tone-duration",
            type=float,
            default=[1000],
            nargs="*",
            help="Duration of tone in millisecond",
        )
        group.add_argument(
            "--am-tone-freq",
            type=float,
            default=[440],
            nargs="*",
            help="Frequency of carrier in Hz",
        )
        group.add_argument(
            "--am-tone-phase",
            type=float,
            default=[0],
            nargs="*",
            help="Phase of carrier in degree.",
        )
        # am setting
        group.add_argument(
            "--am-tone-modulation-freq",
            type=float,
            default=[440],
            nargs="*",
            help="Frequency of modulator in Hz.",
        )
        group.add_argument(
            "--am-tone-depth",
            type=float,
            default=[100],
            nargs="*",
            help="Depth of modulator in percentage",
        )
        group.add_argument(
            "--am-tone-modulator-phase",
            type=float,
            default=[0],
            nargs="*",
            help="Phase of modulator in degree",
        )
        group.add_argument(
            "--am-tone-num-signals",
            type=int,
            default=1,
            help="Number of signals. If this value greater than 2,"
            "the other arguments should contain 2 types.",
        )
        return parser

    def _generate_each(self, idx: int) -> np.ndarray:
        duration = int(self.duration[idx] * self.samp_freq / 1000)
        freq = self.freq[idx]
        phase = np.deg2rad(self.phase[idx])
        modulation_freq = self.modulation_freq[idx]
        depth = self.depth[idx] / 100
        modulator_phase = np.deg2rad(self.modulator_phase[idx])
        if depth > 1:
            raise ValueError(
                "am_tone_depth must be smaller than 100, but got {}".format(
                    self.depth[idx]
                )
            )

        t = np.arange(0, duration) / self.samp_freq
        # x(t) = A*sin(2*pi*freq*t)[1 + md*sin(2*pi*modulation_freq*t)]
        # md is the modulation depth(index) (0-100%)
        carrier = np.sin(2 * np.pi * freq * t + phase, dtype=np.float64)
        modulator = depth * np.sin(
            2 * np.pi * modulation_freq * t - np.pi / 2 + modulator_phase,
            dtype=np.float64,
        )
        x = carrier * (1 + modulator)
        x = declip(x, 1.0)
        return x


def am_tone(
    duration: Sequence[float] = [1000],
    freq: Sequence[float] = [440],
    phase: Sequence[float] = [0],
    modulation_freq: Sequence[float] = [440],
    depth: Sequence[float] = [100],
    modulator_phase: Sequence[float] = [0],
    num_signals: int = 1,
    samp_freq: int = 16000,
) -> List[np.ndarray]:
    """Generate sinusoidally amplitude modulated tone.

    Args:
        duration: The duration of am tone in millisecond.
            Defaults to [1000].
        freq: The frequency of the carrier in Hz.
            Defaults to [440].
        phase: Phase of modulator in degree.
        modulation_freq: The frequency of modulator in Hz.
            Defaults to [440].
        depth: Depth of modulator in percentage.
            Defaults to [100].
        modulator_phase: Phase of modulator in degree.
            Defaults to [0].
        num_signals: Number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.

    Returns:
        Output signals.
    """
    return AmTone(
        duration,
        freq,
        phase,
        modulation_freq,
        depth,
        modulator_phase,
        num_signals,
        samp_freq,
    )()
