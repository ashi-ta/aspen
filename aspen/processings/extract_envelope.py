#!/usr/bin/env python3
# encoding: utf-8
"""Extract envelope"""

import numpy as np
from scipy import signal

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_processing_interface import AbsProcessingInterface
from aspen.processings.filter_signal import filter_signal


class ExtractEnvelope(AbsCommonInterface, AbsProcessingInterface):
    """Extract the envelope from a signal

    Args:
        extract_envelope_method: Extracting method of envelope.
            Defaults to "rect".
        extract_envelope_lpf_freq: Frequency of low-pass filter.
            Defaults to 16.0.
        extract_envelope_lpf_impulse_response: Impulse response for low-pass filter.
            Defaults to "fir".
        extract_envelope_lpf_filter_order: Filter order of low-pass filter.
            Defaults to 512.
        extract_envelope_lpf_fir_window: Window function for low-pass filter.
            Use only when `lpf-impulse-response=fir`. Defaults to "hann".
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        extract_envelope_method: str = "rect",
        extract_envelope_lpf_freq: float = 16.0,
        extract_envelope_lpf_impulse_response: str = "fir",
        extract_envelope_lpf_filter_order: int = 512,
        extract_envelope_lpf_fir_window: str = "hann",
        samp_freq: int = 16000,
    ):
        self.method = extract_envelope_method
        self.lpf_freq = extract_envelope_lpf_freq
        self.lpf_impulse_response = extract_envelope_lpf_impulse_response
        self.lpf_filter_order = extract_envelope_lpf_filter_order
        self.lpf_fir_window = extract_envelope_lpf_fir_window
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("extract-envelope setting")
        group.add_argument(
            "--extract-envelope-method",
            default="rect",
            choices=["hilbert", "rect"],
            type=str,
            help="Extracting method of envelope",
        )
        group.add_argument(
            "--extract-envelope-lpf-freq",
            default=16,
            type=float,
            help="Frequency of low-pass filter",
        )
        group.add_argument(
            "--extract-envelope-lpf-impulse-response",
            default="fir",
            choices=["fir", "iir"],
            type=str,
            help="Impulse response for low-pass filter",
        )
        group.add_argument(
            "--extract-envelope-lpf-filter-order",
            default=512,
            type=int,
            help="Filter order of low-pass filter",
        )
        group.add_argument(
            "--extract-envelope-lpf-fir-window",
            default="hann",
            type=str,
            help="Window function for low-pass filter. Use only when lpf-impulse-response=fir",
        )
        return parser

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Apply envelope extracting

        Args:
            x: Input signal

        Returns:
            Output signal
        """
        if self.method == "hilbert":
            half = np.abs(signal.hilbert(x))
        elif self.method == "rect":
            half = np.where(x < 0, 0, x)
        else:
            raise ValueError("Invalid extract_envelope method %s" % self.method)

        env = filter_signal(
            half,
            "lowpass",
            self.lpf_freq,
            self.lpf_impulse_response,
            self.lpf_filter_order,
            self.lpf_fir_window,
            self.samp_freq,
        )
        return env


def extract_envelope(
    x: np.ndarray,
    method: str = "rect",
    lpf_freq: float = 16,
    lpf_impulse_response: str = "fir",
    lpf_filter_order: int = 512,
    lpf_fir_window: str = "hann",
    samp_freq: int = 16000,
) -> np.ndarray:
    """Extract the envelope from a signal

    Args:
        x: Input signal
        method: Extracting method of envelope.
            Defaults to "rect".
        lpf_freq: Frequency of low-pass filter.
            Defaults to 16.0.
        lpf_impulse_response: Impulse response for low-pass filter.
            Defaults to "fir".
        lpf_filter_order: Filter order of low-pass filter.
            Defaults to 512.
        lpf_fir_window: Window function for low-pass filter.
            Use only when `lpf-impulse-response=fir`. Defaults to "hann".
        samp_freq: Sampling frequency. Defaults to 16000.

    Returns:
        Output signal
    """
    return ExtractEnvelope(
        method,
        lpf_freq,
        lpf_impulse_response,
        lpf_filter_order,
        lpf_fir_window,
        samp_freq,
    )(x)
