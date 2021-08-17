#!/usr/bin/env python3
# encoding: utf-8
"""Filter a signal"""

from logging import getLogger
from typing import Optional, Union

import numpy as np
from scipy import signal

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_processing_interface import AbsProcessingInterface

logger = getLogger(__name__)


class FilterSignal(AbsCommonInterface, AbsProcessingInterface):
    """Filter a signal.

    Args:
        filter_signal_btype: The type of filter.
        filter_signal_filter_freq: Cutoff frequency.
            In the case of bandpass or bandstop,
            specify the lower/upper freqencies splitted by the underscore symbol (e.g. 800_1200).
        filter_signal_impulse_response: Type of impulse response of filter.
            Defaults to "fir".
        filter_signal_filter_order: Number of the filter order.
            Defaults to "None". This means that the filter order set 512 for `fir` and 2 for `iir`, respectively.
        filter_signal_firwindow: Type of FIR window for filtering noise.
            Window function is listed in Scipy doc.
            (https://docs.scipy.org/doc/scipy/reference/signal.windows.html)
            Use only when impulse-response=fir". Defaults to "hann".
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        filter_signal_btype: str,
        filter_signal_filter_freq: Union[str, float, np.ndarray],
        filter_signal_impulse_response: str = "fir",
        filter_signal_filter_order: Optional[int] = None,
        filter_signal_firwindow: str = "hann",
        samp_freq: int = 16000,
    ):
        self.btype = filter_signal_btype
        self.filter_freq = filter_signal_filter_freq
        self.impulse_response = filter_signal_impulse_response
        self.filter_order = filter_signal_filter_order
        self.firwindow = filter_signal_firwindow
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("filter-signal setting")
        group.add_argument(
            "--filter-signal-btype",
            required=True,
            type=str,
            choices=["lowpass", "highpass", "bandpass", "bandstop"],
            help="The type of filter",
        )
        group.add_argument(
            "--filter-signal-filter-freq",
            required=True,
            type=str,
            help="Cutoff frequency. In the case of bandpass or bandstop,"
            "specify the lower/upper freqencies splitted by the underscore symbol (e.g. 800_1200)",
        )
        group.add_argument(
            "--filter-signal-impulse-response",
            default="fir",
            choices=["fir", "iir"],
            type=str,
            help="Type of impulse response of filter",
        )
        group.add_argument(
            "--filter-signal-filter-order",
            default=None,
            type=int,
            help="Number of the filter order",
        )
        group.add_argument(
            "--filter-signal-firwindow",
            default="hann",
            type=str,
            help="Type of FIR window for filtering noise. "
            "Window function is listed in Scipy doc (https://docs.scipy.org/doc/scipy/reference/signal.windows.html). "
            "Use only when impulse-response=fir",
        )
        return parser

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Apply signal filtering

        Args:
            x: Input signal

        Returns:
            Output signal
        """
        # filtering preserved the phase characteristics
        t = x.shape[0]
        if isinstance(self.filter_freq, str):
            self.filter_freq = np.array(self.filter_freq.split("_")).astype(np.float64)
        if self.impulse_response == "fir":
            # FIR filter taken care of the phase delay by zero padding
            # https://www.mathworks.com/help/signal/ug/practical-introduction-to-digital-filtering.html
            # the phase delay of the filtered signal is half the filter order
            if self.filter_order is None:
                self.filter_order = 512
            elif self.filter_order % 2 != 0:
                self.filter_order += 1
            # for delay compensation, length of x must be greater than twice the filter order
            if t < self.filter_order * 2:
                raise ValueError(
                    "Invalid filter order. Must be smaller than "
                    + str(int(t / 2))
                    + ", otherwise use IIR filter"
                )
            delay = int(self.filter_order / 2)
            # before filtering, append delay-dim zeros at the end of the input data to compensate for delay
            x = np.concatenate([x, np.zeros(delay)])
            # 1st argv of firwin is the number of taps (= the filter order + 1)
            b = signal.firwin(
                self.filter_order + 1,
                self.filter_freq,
                window=self.firwindow,
                pass_zero=self.btype,
                fs=self.samp_freq,
            )
            x = signal.lfilter(b, 1, x)
            x = x[delay:]

        elif self.impulse_response == "iir":
            # butterworth filter (IIR) with SOS (Second Order Section, Biquad) type
            if self.filter_order is None:
                self.filter_order = 2
            sos = signal.butter(
                self.filter_order,
                self.filter_freq,
                btype=self.btype,
                fs=self.samp_freq,
                output="sos",
            )
            # the group delay introduced by the filter shows nonlinearity on frequency axis.
            # therefore apply (sos)filtfilt function (forward-backward filtering to compensate the delay)
            x = signal.sosfiltfilt(sos, x)
        else:
            raise ValueError("Invalid impulse_response. Must be either fir or iir.")
        return x


def filter_signal(
    x: np.ndarray,
    btype: str,
    filter_freq: Union[str, float, np.ndarray],
    impulse_response: str = "fir",
    filter_order: Optional[int] = None,
    firwindow: str = "hann",
    samp_freq: int = 16000,
) -> np.ndarray:
    """Filter a signal.

    Args:
        x: Input signal
        btype: The type of filter.
        filter_freq: Cutoff frequency.
            In the case of bandpass or bandstop,
            specify the lower/upper freqencies splitted by the underscore symbol (e.g. 800_1200).
        impulse_response: Type of impulse response of filter.
            Defaults to "fir".
        filter_order: Number of the filter order.
            Defaults to "None". This means that the filter order set 512 for `fir` and 2 for `iir`, respectively.
        firwindow: Type of FIR window for filtering noise.
            Window function is listed in Scipy doc.
            (https://docs.scipy.org/doc/scipy/reference/signal.windows.html)
            Use only when impulse-response=fir". Defaults to "hann".
        samp_freq: Sampling frequency. Defaults to 16000.

    Returns:
        Output signal
    """
    return FilterSignal(
        btype,
        filter_freq,
        impulse_response,
        filter_order,
        firwindow,
        samp_freq,
    )(x)
