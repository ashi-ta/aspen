#!/usr/bin/env python3
# encoding: utf-8
"""Visualize a modulation power spectrum"""

from logging import getLogger

import matplotlib.pyplot as plt
import numpy as np
from scipy import fft

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_visualization_interface import AbsVisualizationInterface
from aspen.processings.modulation_power_spectrum import modulation_power_spectrum

logger = getLogger(__name__)

# Width, Height
PLOTSIZE = [7, 5]
TITLE = "mps"


class MpsVisualizer(AbsCommonInterface, AbsVisualizationInterface):
    """Visualize modulation power spectrum

    Args:
        mps_visualizer_dbrange: The magnitude range limiting axes of modulation power spectrum.
            Defaults to 50.
        visualization_labels: The flag to add labels (title, xlabel, ylabel).
            Defaults to True.
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        mps_visualizer_dbrange: int = 50,
        visualization_labels: bool = True,
        samp_freq: int = 16000,
    ):
        self.dbrange = mps_visualizer_dbrange
        self.labels = visualization_labels
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("MPS visualization setting")
        group.add_argument(
            "--mps-visualizer-dbrange",
            default=50,
            type=int,
            help="Magnitude range limiting axes of modulation power spectrum",
        )
        return parser

    def plotsize(self):
        return PLOTSIZE

    def title(self):
        return TITLE

    def __call__(self, fig, ax, sample):
        if self.labels:
            plt.ylabel("Spectral Frequency (Cycles/KHz)")
            plt.xlabel("Temporal Frequency (Hz)")
        else:
            ax.set_xticks([])
            ax.set_yticks([])
        (_, mps_f, mps_t, mps, mps_pow,) = modulation_power_spectrum(
            sample, samp_freq=self.samp_freq
        )  # use default for other argv
        mps_pow_shift = fft.fftshift(mps_pow)
        mps_f_shift = fft.fftshift(mps_f)
        mps_t_shift = fft.fftshift(mps_t)
        mps_pow_shift = 10 * np.log10(mps_pow_shift)
        mps_pow_max = mps_pow_shift.max()
        mps_pow_min = mps_pow_max - self.dbrange
        mps_pow_shift = np.where(
            mps_pow_shift < mps_pow_min, mps_pow_min, mps_pow_shift
        )
        mps_f_max, mps_f_min = mps_f_shift.max(), mps_f_shift.min()
        mps_t_max, mps_t_min = mps_t_shift.max(), mps_t_shift.min()

        extent = (mps_t_min, mps_t_max, mps_f_min * 1000, mps_f_max * 1000)
        ax.contour(
            mps_pow_shift,
            [
                mps_pow_max * 0.35,
                mps_pow_max * 0.5,
                mps_pow_max * 0.65,
                mps_pow_max * 0.8,
            ],
            colors="black",
            extent=extent,
        )
        img = ax.imshow(
            mps_pow_shift,
            interpolation="nearest",
            aspect="auto",
            origin="lower",
            cmap=plt.get_cmap("jet"),
            extent=extent,
        )
        if self.labels:
            fig.colorbar(img)
        ax.grid(False)
        ax.set_ylim((0, mps_f_shift.max() * 1000))
        return
