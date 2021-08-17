#!/usr/bin/env python3
# encoding: utf-8
"""Modulation-filtered speech"""

from typing import Sequence

import librosa
import numpy as np
import scipy.fft

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_stimulus_interface import AbsStimulusInterface
from aspen.processings.modulation_power_spectrum import modulation_power_spectrum
from aspen.utils.cli_utils import strtobool


class ModulationFilteredSpeech(AbsCommonInterface, AbsStimulusInterface):
    """Generate modulation-filtered speech.

    Args:
        samp_freq: Sampling frequency. Defaults to 16000.
        temporal_stopbands: Lower & upper temporal modulation frequency of bandstop.
            Defaults to "100_200".
        spectral_stopbands: Lower & upper spectral modulation frequency of bandstop.
            Defaults to "100_200".
        spec_samp_freq: Sampling frequency in spectrogram space in Hz.
            The value determines the width of Gaussian window shift to calculate the spectrogram. Defaults to 1000.
        gauss_window_alpha: Width factor of Gaussian window.
            The value is inversely proportional to the width of the window.
            (ref: https://www.mathworks.com/help/signal/ref/gausswin.html) Defaults to 3.
        spacing_freq: The time-frequency scale for the spectrogram in Hz.
            This value determines the width of the Gaussian window to calculate spectrogram. Defaults to 50.
        spec_standardize: Spectrogram normalize. Defaults to False.
        spec_db_range: The range of narrowing down the spectrogram amplitude.
            Defaults to -1 (without narrowing).
        griffinlim_iter: Number of iteration for Griffin-Lim algorithm
            Defaults to 20.
    """

    def __init__(
        self,
        samp_freq: int = 16000,
        temporal_stopbands: str = "100_200",
        spectral_stopbands: str = "100_200",
        spec_samp_freq: int = 1000,
        gauss_window_alpha: float = 3,
        spacing_freq: int = 50,
        spec_standardize: bool = False,
        spec_db_range: float = -1,
        griffinlim_iter: int = 20,
    ):
        self.samp_freq = samp_freq
        self.temporal_stopbands = temporal_stopbands
        self.spectral_stopbands = spectral_stopbands
        self.spec_samp_freq = spec_samp_freq
        self.gauss_window_alpha = gauss_window_alpha
        self.spacing_freq = spacing_freq
        self.spec_standardize = spec_standardize
        self.spec_db_range = spec_db_range
        self.griffinlim_iter = griffinlim_iter

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Noise-vocoded speech setting")
        group.add_argument(
            "--temporal-stopbands",
            default="100_200",
            type=str,
            help="Lower & upper temporal modulation frequency of bandstop",
        )
        group.add_argument(
            "--spectral-stopbands",
            default="100_200",
            type=str,
            help="Lower & upper spectral modulation frequency of bandstop",
        )
        group.add_argument(
            "--spec-samp-freq",
            default=1000,
            type=int,
            help="Sampling frequency in spectrogram space",
        )
        group.add_argument(
            "--gauss-window-alpha",
            default=3,
            type=float,
            help="Width factor of Gaussian window."
            "The value is inversely proportional to the width of the window."
            "ref: https://www.mathworks.com/help/signal/ref/gausswin.html",
        )
        group.add_argument(
            "--spacing-freq",
            default=50,
            type=int,
            help="The time-frequency scale for the spectrogram in Hz",
        )
        group.add_argument(
            "--spec-standardize",
            default=False,
            type=strtobool,
            help="The flag of Spectrogram standardization and narrowing down the amplitude range",
        )
        group.add_argument(
            "--spec-db-range",
            default=-1,
            type=float,
            help="The range of narrowing down the spectrogram amplitude",
        )
        group.add_argument(
            "--griffinlim-iter",
            default=20,
            type=int,
            help="Number of iteration for Griffin-Lim algorithm",
        )

        return parser

    def __call__(self, x: Sequence[np.ndarray]) -> np.ndarray:
        """Generate modulation-filtered speech.

        Args:
            x: Speech signal.
                x must be sequence-like object such as list, tuple and so on.

        Returns:
            Stimulus of modulation filtered speech.
        """
        if len(x) != 1:
            raise ValueError("input length must be 1, but got {}".format(len(x)))

        stimulus = x[0]
        temporal_stopbands = np.array(self.temporal_stopbands.split("_")).astype(
            np.float64
        )
        spectral_stopbands = np.array(self.spectral_stopbands.split("_")).astype(
            np.float64
        )

        # mps is calculated from log-spectrogram
        (stft_param, mps_f, mps_t, mps, mps_pow,) = modulation_power_spectrum(
            stimulus,
            self.spec_samp_freq,
            self.gauss_window_alpha,
            self.spacing_freq,
            0,
            self.samp_freq / 2,
            self.spec_standardize,
            self.spec_db_range,
            0,
            0,
            "librosa",
            self.samp_freq,
        )

        # condition of spectral and temporal modulation filtering
        mps_t_stopband_r = (mps_t >= temporal_stopbands[0]) & (
            mps_t <= temporal_stopbands[1]
        )
        mps_t_stopband_l = (mps_t <= -temporal_stopbands[0]) & (
            mps_t >= -temporal_stopbands[1]
        )
        mps_t_stopband = mps_t_stopband_r + mps_t_stopband_l
        mps_f *= 1000  # Hz to kHz
        mps_f_stopband_r = (mps_f >= spectral_stopbands[0]) & (
            mps_f <= spectral_stopbands[1]
        )
        mps_f_stopband_l = (mps_f <= -spectral_stopbands[0]) & (
            mps_f >= -spectral_stopbands[1]
        )
        mps_f_stopband = mps_f_stopband_r + mps_f_stopband_l
        mps_tt_stopband, mps_ff_stopband = np.meshgrid(mps_t_stopband, mps_f_stopband)
        mps_tt_stopband_not = np.logical_not(mps_tt_stopband)
        mps_ff_stopband_not = np.logical_not(mps_ff_stopband)

        # spectral LPF
        if np.all(mps_tt_stopband):
            filter2 = mps_ff_stopband_not.astype(int)
        # temporal LPF
        elif np.all(mps_ff_stopband):
            filter2 = mps_tt_stopband_not.astype(int)
        # notch filter or no filter
        else:
            filter2 = (mps_tt_stopband_not * mps_ff_stopband_not).astype(int)

        # filtering
        filtered_mps = mps * filter2

        # filtered mps to spectrogram
        spec_filtered = np.real(scipy.fft.ifft2(filtered_mps))

        # spectrogram without the phase to signal
        spec_filtered = 10 ** (spec_filtered / 20)
        stimulus = librosa.griffinlim(
            spec_filtered,
            n_iter=self.griffinlim_iter,
            hop_length=stft_param["hop_length"],
            win_length=stft_param["n_fft"] - 1,
            window=stft_param["window"],
            pad_mode="constant",
        )

        return stimulus
