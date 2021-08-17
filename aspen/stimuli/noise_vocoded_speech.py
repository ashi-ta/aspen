#!/usr/bin/env python3
# encoding: utf-8
"""Noise-vocoded speech"""

from logging import getLogger
from typing import Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_stimulus_interface import AbsStimulusInterface
from aspen.processings.extract_envelope import extract_envelope
from aspen.processings.filter_signal import filter_signal
from aspen.utils.freqband import erb_band, octave_band

logger = getLogger(__name__)


class NoiseVocodedSpeech(AbsCommonInterface, AbsStimulusInterface):
    """Generate nosie-vocoded speech.

    Args:
        samp_freq: Sampling frequency. Defaults to 16000.
        num_freqband: Number of frequency band. Defaults to 4.
        freqband_scale_method: Scale of frequency band.
            The choices are `octave`, `erb` and `user`. Defaults to "octave".
        user_freqband: User defiened frequency band scale.
            Use only when freqband_scale_method is `user`. Defaults to "0_600_1500_2100_4000".
        freqband_limit: Lower & upper frequency of bandpass.
            Use only when freqband_scale_method is `octave` or `erb`. Defaults to "500_8000".
        erb_band_number_limit: Lower & upper bandlimit number in ERB scale.
            Use only when freqband_scale_method is `erb`. Defaults to "3_35".
        erb_band_number_step: Step number in ERB scale to reduce the ERB.
            Use only when freqband_scale_method `erb`. Defaults to 1.
        filter_impulse_response_method: Type of impulse response for filtering. Defaults to "fir".
        filter_order: Number of the filter order. Defaults to 512.
        filter_fir_window: Type of FIR window for filtering.
            Window function is listed in Scipy doc (https://docs.scipy.org/doc/scipy/reference/signal.windows.html).
            Defaults to "hann".
        ext_env_method: Method of envelope extraction.
            `hilbert` is (hilbert transform + low-pass filter).
            `rect` is (half-wave rectification + low-pass filter). Defaults to "rect".
        ext_env_impulse_response_method: Type of impulse response for extracting envelope.
            Defaults to "fir".
        ext_env_filter_order: Number of the filter order for extracting envelope. Defaults to 512.
        ext_env_fir_window: Type of FIR window for extracting envelope.
            Window function is listed in Scipy doc (https://docs.scipy.org/doc/scipy/reference/signal.windows.html).",
            Defaults to "hann".
        ext_env_freq: Frequency of the lowpass filter for extracting envelope. Defaults to 16.
    """

    def __init__(
        self,
        samp_freq: int = 16000,
        num_freqband: int = 4,
        freqband_scale_method: str = "octave",
        user_freqband: str = "0_600_1500_2100_4000",
        freqband_limit: str = "500_8000",
        erb_band_number_limit: str = "3_35",
        erb_band_number_step: int = 1,
        filter_impulse_response_method: str = "fir",
        filter_order: int = 512,
        filter_fir_window: str = "hann",
        ext_env_method: str = "rect",
        ext_env_impulse_response_method: str = "fir",
        ext_env_filter_order: int = 512,
        ext_env_fir_window: str = "hann",
        ext_env_freq: float = 16,
    ):
        self.samp_freq = samp_freq
        self.num_freqband = num_freqband
        self.freqband_scale_method = freqband_scale_method
        self.user_freqband = user_freqband
        self.freqband_limit = freqband_limit
        self.erb_band_number_limit = erb_band_number_limit
        self.erb_band_number_step = erb_band_number_step
        self.filter_impulse_response_method = filter_impulse_response_method
        self.filter_order = filter_order
        self.filter_fir_window = filter_fir_window
        self.ext_env_method = ext_env_method
        self.ext_env_impulse_response_method = ext_env_impulse_response_method
        self.ext_env_filter_order = ext_env_filter_order
        self.ext_env_fir_window = ext_env_fir_window
        self.ext_env_freq = ext_env_freq

        self._configure_frequency_band()

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Noise-vocoded speech setting")
        group.add_argument(
            "--num-freqband",
            default=4,
            type=int,
            help="Number of frequency band",
        )
        group.add_argument(
            "--freqband-scale-method",
            default="octave",
            type=str,
            choices=["octave", "erb", "user"],
            help="Scale of frequency band",
        )
        group.add_argument(
            "--user-freqband",
            default="0_600_1500_2100_4000",
            type=str,
            help="User defiened frequency band scale."
            "Use only when --freqband-scale-method=user",
        )
        group.add_argument(
            "--freqband-limit",
            default="500_8000",
            type=str,
            help="Lower & upper frequency of bandpass."
            "Use only when --freqband-scale-method={octave|erb}",
        )
        group.add_argument(
            "--erb-band-number-limit",
            default="3_35",
            type=str,
            help="Lower & upper bandlimit number in ERB scale."
            "Use only when --freqband-scale-method=erb",
        )
        group.add_argument(
            "--erb-band-number-step",
            default=1,
            type=int,
            help="Step number in ERB scale (use when ERB scale is too detailed)."
            "Use only when --freqband-scale-method=erb",
        )
        group.add_argument(
            "--filter-impulse-response-method",
            default="fir",
            type=str,
            choices=["fir", "iir"],
            help="Type of impulse response for filtering noise",
        )
        group.add_argument(
            "--filter-order",
            default=512,
            type=int,
            help="Number of the filter order",
        )
        group.add_argument(
            "--filter-fir-window",
            default="hann",
            type=str,
            help="Type of FIR window for filtering noise."
            "Window function is listed in Scipy doc (https://docs.scipy.org/doc/scipy/reference/signal.windows.html).",
        )
        group.add_argument(
            "--ext-env-method",
            default="rect",
            type=str,
            choices=["rect", "hilbert"],
            help="Method of envelope extraction"
            "rect = half-wave rectification + low-pass filter"
            "hilbert = hilbert transform + low-pass filter",
        )
        group.add_argument(
            "--ext-env-impulse-response-method",
            default="fir",
            type=str,
            choices=["fir", "iir"],
            help="Impulse response for the envelope extraction",
        )
        group.add_argument(
            "--ext-env-filter-order",
            default=512,
            type=int,
            help="Order of the filter for the envelope extraction",
        )
        group.add_argument(
            "--ext-env-fir-window",
            default="hann",
            type=str,
            help="Kind of the window function for the envelope extraction",
        )
        group.add_argument(
            "--ext-env-freq",
            default=16,
            type=float,
            help="Frequency of the lowpass filter for the envelope extraction",
        )

        return parser

    def __call__(self, x: Sequence[np.ndarray]) -> np.ndarray:
        """Generate noise-vocoded speech.

        Args:
            x: Speech signal and noise signal.
                x must be sequence-like object such as list, tuple and so on.
                The first element is speech signal and the second one is noise (i.e. [speech, noise]).
                The duration of noise must be equal to or greater than the one of speech signal.
                In the case of `gap_method=silent`, the second element is ignored.

        Returns:
            Noise-vocoded speech.
        """
        if len(x) != 2:
            raise ValueError(
                "x must contain the 2 elements which is comprised by [speech, noise]"
            )
        if x[0].shape[0] > x[1].shape[0]:
            raise ValueError(
                "noise must be equal to or greater than the one of speech signal"
            )
        noise = x[1]
        stimulus = x[0]
        t = stimulus.shape[0]

        band_signals = []
        for i, band in enumerate(self.bands):
            x_cloned = stimulus.copy()
            n_cloned = noise.copy()[:t]
            # bandpass speech
            if band[0] == 0 and band[1] >= self.samp_freq / 2:
                pass  # do nothing when freq_band=[0, nyquist_freq]
            else:
                if band[0] == 0:
                    btype = "lowpass"
                    freq_array = band[1]
                elif band[1] >= self.samp_freq / 2:
                    if band[0] >= self.samp_freq / 2:
                        raise ValueError(
                            "Invalid bandwidth = ("
                            + str(band[0])
                            + ", "
                            + str(band[1])
                            + ")."
                        )
                    btype = "highpass"
                    freq_array = band[0]
                else:
                    btype = "bandpass"
                    freq_array = band
                x_cloned = filter_signal(
                    x_cloned,
                    btype,
                    freq_array,
                    self.filter_impulse_response_method,
                    self.filter_order,
                    self.filter_fir_window,
                    self.samp_freq,
                )
                n_cloned = filter_signal(
                    n_cloned,
                    btype,
                    freq_array,
                    self.filter_impulse_response_method,
                    self.filter_order,
                    self.filter_fir_window,
                    self.samp_freq,
                )
            env = extract_envelope(
                x_cloned,
                self.ext_env_method,
                self.ext_env_freq,
                self.ext_env_impulse_response_method,
                self.ext_env_filter_order,
                self.ext_env_fir_window,
                self.samp_freq,
            )
            band_signals.append(env * n_cloned)

        # sum the above all signals
        stimulus = np.zeros(t)
        for s in band_signals:
            stimulus += s

        return stimulus

    def _configure_frequency_band(self):
        """Generate frequency band configuration"""

        freqband_limit = np.array(self.freqband_limit.split("_")).astype(np.float64)

        if self.freqband_scale_method == "octave":
            octband, _ = octave_band(
                freqband_limit[0], freqband_limit[1], self.samp_freq
            )
            b = np.concatenate([np.zeros(1), octband])  # band start with 0Hz
        elif self.freqband_scale_method == "erb":
            erb_band_number_limit = np.array(
                self.erb_band_number_limit.split("_")
            ).astype(np.int64)
            erbband = erb_band(
                erb_band_number_limit[0],
                erb_band_number_limit[1],
                freqband_limit[0],
                freqband_limit[1],
                self.samp_freq,
            )
            b = erbband[:: self.erb_band_number_step]
        elif self.freqband_scale_method == "user":
            b = np.array(self.user_freqband.split("_")).astype(np.float64)

        if self.num_freqband > b.shape[0] - 1:
            raise ValueError(
                "num_freqband={} must be smaller than the number of bands={}".format(
                    self.num_freqband, b.shape[0] - 1
                )
            )

        # divisions of frequency band
        # e.g. lower_freq=500, upper_freq=8000
        #      num_freqband=1: bands=[[0, 4000]]
        #      num_freqband=2: bands=[[0, 500], [500, 4000]]
        #      num_freqband=3: bands=[[0, 500], [500, 1000], [1000, 4000]]
        #      num_freqband=4: bands=[[0, 500], [500, 1000], [1000, 2000], [2000, 4000]]
        self.bands = []
        if self.num_freqband == 1:
            self.bands.append([b[0], b[-1]])
        else:
            for i in range(self.num_freqband):
                i += 1
                if i == self.num_freqband:
                    self.bands.append([b[i - 1], b[-1]])
                else:
                    self.bands.append([b[i - 1], b[i]])
        logger.info(
            "Frequency band = "
            + ", ".join([str(i[0]) + "_" + str(i[1]) for i in self.bands])
        )
