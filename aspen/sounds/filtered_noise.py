#!/usr/bin/env python3
# encoding: utf-8
"""Filtered noise"""

from logging import getLogger
from typing import List, Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_sound_interface import AbsSoundInterface
from aspen.processings.declip import declip
from aspen.processings.filter_signal import filter_signal

logger = getLogger(__name__)


class FilteredNoise(AbsCommonInterface, AbsSoundInterface):
    """Generate filtered noise.

    Args:
        filtered_noise_duration: The duration of filtered noise in millisecond.
            Defaults to [1000].
        filtered_noise_btype: The type of filtering.
            The choices are `lowpass`, `highpass`, `bandpass` or `bandstop`.
            Defaults to ["bandpass"].
        filtered_noise_filter_freq: Cutoff frequency to filter a noise in Hz.
            In the case of bandpass or bandstop,
            specify the lower/upper freqencies splitted by the underscore symbol (e.g. 800_1200).
            Defaults to ["800_1200"].
        filtered_noise_filter_impulse_response:
            The type of impulse response for filtering noise.
            The choices are `fir` or `iir`
            that are a finite impulse response or infinite impulse response, respectively.
            Defaults to ["fir"].
        filtered_noise_filter_order: The number of the filter order.
            Defaults to [512].
        filtered_noise_filter_firwin: Type of FIR window.
            Window functions are listed in Scipy doc (https://docs.scipy.org/doc/scipy/reference/signal.windows.html).
            Defaults to ["hann"].
        filtered_noise_num_signals: Number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        filtered_noise_duration: Sequence[float] = [1000],
        filtered_noise_btype: Sequence[str] = ["bandpass"],
        filtered_noise_filter_freq: Sequence[str] = ["800_1200"],
        filtered_noise_filter_impulse_response: Sequence[str] = ["fir"],
        filtered_noise_filter_order: Sequence[int] = [512],
        filtered_noise_filter_firwin: Sequence[str] = ["hann"],
        filtered_noise_num_signals: int = 1,
        samp_freq: int = 16000,
    ):
        self.duration = filtered_noise_duration
        self.btype = filtered_noise_btype
        self.filter_freq = filtered_noise_filter_freq
        self.filter_impulse_response = filtered_noise_filter_impulse_response
        self.filter_order = filtered_noise_filter_order
        self.filter_firwin = filtered_noise_filter_firwin
        self.num_signals = filtered_noise_num_signals
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Noise signals setting")
        group.add_argument(
            "--filtered-noise-duration",
            default=[1000],
            type=float,
            nargs="*",
            help="Duration of noise in millisecond",
        )
        group.add_argument(
            "--filtered-noise-btype",
            default=["bandpass"],
            type=str,
            nargs="*",
            choices=[
                "lowpass",
                "highpass",
                "bandpass",
                "bandstop",
            ],
            help="Type of filtering",
        )
        group.add_argument(
            "--filtered-noise-filter-freq",
            default=["800_1200"],
            type=str,
            nargs="*",
            help="Cutoff frequency for filtering noise in Hz."
            "In the case of bandpass or bandstop,"
            "specify the lower/upper freqencies splitted by the underscore symbol (e.g. 800_1200)",
        )
        group.add_argument(
            "--filtered-noise-filter-impulse-response",
            default=["fir"],
            type=str,
            nargs="*",
            choices=["fir", "iir"],
            help="Type of impulse response for filtering noise",
        )
        group.add_argument(
            "--filtered-noise-filter-order",
            default=[512],
            type=int,
            nargs="*",
            help="Number of the filter order",
        )
        group.add_argument(
            "--filtered-noise-filter-firwin",
            default=["hann"],
            type=str,
            nargs="*",
            help="Type of FIR window for filtering noise."
            "Window function is listed in Scipy doc (https://docs.scipy.org/doc/scipy/reference/signal.windows.html).",
        )
        group.add_argument(
            "--filtered-noise-num-signals",
            type=int,
            default=1,
            help="Number of signals. If this value greater than 2,"
            "the other arguments should contain 2 types.",
        )

        return parser

    def _generate_each(self, idx: int) -> np.ndarray:
        duration = int(self.duration[idx] * self.samp_freq / 1000)
        btype = self.btype[idx]
        filter_freq = self.filter_freq[idx]
        filter_impulse_response = self.filter_impulse_response[idx]
        filter_order = self.filter_order[idx]
        filter_firwin = self.filter_firwin[idx]

        x = np.random.normal(loc=0, scale=1, size=[duration]).astype(np.float64)
        y = filter_signal(
            x,
            btype,
            filter_freq,
            filter_impulse_response,
            filter_order,
            filter_firwin,
            self.samp_freq,
        )
        y = declip(y, 1.0)
        return y


def filtered_noise(
    duration: Sequence[float] = [1000],
    btype: Sequence[str] = ["bandpass"],
    filter_freq: Sequence[str] = ["800_1200"],
    filter_impulse_response: Sequence[str] = ["fir"],
    filter_order: Sequence[int] = [512],
    filter_firwin: Sequence[str] = ["hann"],
    num_signals: int = 1,
    samp_freq: int = 16000,
) -> List[np.ndarray]:
    """Generate filtered noise.

    Args:
        duration: The duration of filtered noise in millisecond.
            Defaults to [1000].
        btype: The type of filtering.
            The choices are `lowpass`, `highpass`, `bandpass` or `bandstop`.
            Defaults to ["bandpass"].
        filter_freq: Cutoff frequency to filter a noise in Hz.
            In the case of bandpass or bandstop,
            specify the lower/upper freqencies splitted by the underscore symbol (e.g. 800_1200).
            Defaults to ["800_1200"].
        filter_impulse_response:
            The type of impulse response for filtering noise.
            The choices are `fir` or `iir`
            that are a finite impulse response or infinite impulse response, respectively.
            Defaults to ["fir"].
        filter_order: The number of the filter order.
            Defaults to [512].
        filter_firwin: Type of FIR window.
            Window functions are listed in Scipy doc (https://docs.scipy.org/doc/scipy/reference/signal.windows.html).
            Defaults to ["hann"].
        num_signals: Number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.

    Returns:
        Output signals.
    """
    return FilteredNoise(
        duration,
        btype,
        filter_freq,
        filter_impulse_response,
        filter_order,
        filter_firwin,
        num_signals,
        samp_freq,
    )()
