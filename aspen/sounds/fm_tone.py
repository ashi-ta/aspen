#!/usr/bin/env python3
# encoding: utf-8
"""Frequency-modulated (FM) tone"""

from logging import getLogger
from typing import List, Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_sound_interface import AbsSoundInterface
from aspen.processings.apply_ramp import apply_ramp

logger = getLogger(__name__)


class FmTone(AbsCommonInterface, AbsSoundInterface):
    """Generate frequency modulated tone.

    Args:
        fm_tone_duration: The duration of am tone in millisecond.
            Defaults to [1000].
        fm_tone_freq: The frequency of the carrier in Hz.
            Defaults to [440].
        fm_tone_method: The type of frequency sweep.
            The choices are `sin`, `upward`, `downward`, `updown` or `downup`. Defaults to ["sin"].
        fm_tone_modulation_freq: The frequency of the modulation.
            Defaults to [2].
        fm_tone_freq_excursion: The frequency excusion of modulator in Hz.
            Defaults to [25].
        fm_tone_num_signals: The number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.

    Todo:
        Other chirp method (e.g. logarithmic).
            Ref: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.chirp.html
        A rectangular approximation of the integral of the instantaneous frequency formula.
            Ref: https://www.mathworks.com/help/signal/ref/modulate.html
        Randomly changed phase for fm-sin (refer the frequency modulation detection limens).
            Ref: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3946142/
                 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5112215/
    """

    def __init__(
        self,
        fm_tone_duration: Sequence[float] = [1000],
        fm_tone_freq: Sequence[float] = [440],
        fm_tone_method: Sequence[str] = ["sin"],
        fm_tone_modulation_freq: Sequence[float] = [2],
        fm_tone_freq_excursion: Sequence[float] = [25],
        fm_tone_num_signals: int = 1,
        samp_freq: int = 16000,
    ):
        self.duration = fm_tone_duration
        self.freq = fm_tone_freq
        self.method = fm_tone_method
        self.modulation_freq = fm_tone_modulation_freq
        self.freq_excursion = fm_tone_freq_excursion
        self.num_signals = fm_tone_num_signals
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("FM tone setting")
        group.add_argument(
            "--fm-tone-duration",
            default=[1000],
            type=float,
            nargs="*",
            help="Duration of tone in millisecond",
        )
        group.add_argument(
            "--fm-tone-freq",
            default=[440],
            type=float,
            nargs="*",
            help="Frequency of the carrier in Hz.",
        )
        group.add_argument(
            "--fm-tone-method",
            default=["sin"],
            type=str,
            nargs="*",
            choices=["sin", "upward", "downward", "updown", "downup"],
            help="Kind of frequency sweep.",
        )
        group.add_argument(
            "--fm-tone-modulation-freq",
            default=[2],
            type=float,
            nargs="*",
            help="Frequency used by the sinusoidaly frequency modulation.",
        )
        group.add_argument(
            "--fm-tone-freq-excursion",
            default=[25],
            type=float,
            nargs="*",
            help="Frequency excusion (delta f) of modulator of FM in Hz",
        )
        group.add_argument(
            "--fm-tone-num-signals",
            type=int,
            default=1,
            help="Number of signals. If this value greater than 2,"
            "the other arguments should contain 2 types.",
        )
        return parser

    def _generate_each(self, idx: int) -> np.ndarray:
        duration = int(self.duration[idx] * self.samp_freq / 1000)
        freq = self.freq[idx]
        method = self.method[idx]
        modulation_freq = self.modulation_freq[idx]
        freq_excursion = self.freq_excursion[idx]

        t = np.arange(0, duration) / self.samp_freq
        if method == "sin":
            phase = self._sin_phase(t, freq, modulation_freq, freq_excursion)
            x = np.sin(phase, dtype=np.float64)
        elif method in ["upward", "downward"]:
            phase = self._linear_phase(t, freq, freq_excursion, method)
            x = np.sin(phase, dtype=np.float64)
        elif method in ["updown", "downup"]:
            boundary = int(duration / 2)
            x_up = np.sin(
                self._linear_phase(t[:boundary], freq, freq_excursion, "upward"),
                dtype=np.float64,
            )
            x_down = np.sin(
                self._linear_phase(
                    t[boundary:],
                    freq + freq_excursion,
                    freq_excursion,
                    "downward",
                ),
                dtype=np.float64,
            )
            if method == "updown":
                x_head = apply_ramp(x_up, 5.0, "hann", "offset", self.samp_freq)
                x_tail = apply_ramp(x_down, 5.0, "hann", "onset", self.samp_freq)
                x = np.concatenate([x_head, x_tail])
            else:
                x_head = apply_ramp(x_down, 5.0, "hann", "offset", self.samp_freq)
                x_tail = apply_ramp(x_up, 5.0, "hann", "onset", self.samp_freq)
                x = np.concatenate([x_head, x_tail])
        else:
            raise ValueError("Invalid method")

        return x

    def _sin_phase(self, t, freq, modulation_freq, freq_excursion):
        # integral of the sine function with the DC component (i.e. freq)
        # (sin(2*pi*modulation_freq*t) + freq --> -cos(2*pi*modulation_freq*t)/(2*pi) + freq*t)
        # 2*pi*(freq*t - cos(2*pi*modulation_freq*t)/(2*pi)) = 2*pi*freq*t - cos(2*pi*modulation_freq*t)
        # modulation index is (2*pi*freq_excusion)/(2*pi*modulation_freq)
        phase = 2 * np.pi * freq * t - (freq_excursion / modulation_freq) * np.cos(
            2 * np.pi * modulation_freq * t
        )
        return phase

    def _linear_phase(self, t, freq, freq_excursion, method):
        # integral of the linear function
        # (a*x + b --> a*x^2/2 + b*x)
        gradient = freq_excursion / t[-1]  # a
        if method == "downward":
            gradient = -gradient
        intercept = freq  # b
        phase = 2 * np.pi * (gradient * np.square(t) / 2 + intercept * t)
        return phase


def fm_tone(
    duration: Sequence[float] = [1000],
    freq: Sequence[float] = [440],
    method: Sequence[str] = ["sin"],
    modulation_freq: Sequence[float] = [2],
    freq_excursion: Sequence[float] = [25],
    num_signals: int = 1,
    samp_freq: int = 16000,
) -> List[np.ndarray]:
    """Generate frequency modulated tone.

    Args:
        duration: The duration of am tone in millisecond.
            Defaults to [1000].
        freq: The frequency of the carrier in Hz.
            Defaults to [440].
        method: The type of frequency sweep.
            The choices are `sin`, `linear`, `updown` or `downup`. Defaults to ["sin"].
        modulation_freq: The frequency of the modulation.
            Defaults to [2].
        freq_excursion: The frequency excusion of modulator in Hz.
            Defaults to [25].
        num_signals: The number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.

    Returns:
        Output signals.
    """
    return FmTone(
        duration,
        freq,
        method,
        modulation_freq,
        freq_excursion,
        num_signals,
        samp_freq,
    )()
