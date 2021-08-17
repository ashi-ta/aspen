#!/usr/bin/env python3
# encoding: utf-8
"""Visualize a spectrum"""

from logging import getLogger

import matplotlib.pyplot as plt
import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_visualization_interface import \
    AbsVisualizationInterface

logger = getLogger(__name__)

# Width, Height
PLOTSIZE = [10, 3]
TITLE = "spectrum"


class SpectrumVisualizer(AbsCommonInterface, AbsVisualizationInterface):
    """Visualize spectrum

    Args:
        spectrum_visualizer_scale: The scaling of the values in the spec.
            See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.magnitude_spectrum.html
        visualization_spectral_limit: The limitation of spectral axis in Hz (e.g. 100_1000)
            Defaults to "0" (= do nothing).
        visualization_labels: The flag to add labels (title, xlabel, ylabel).
            Defaults to True.
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        spectrum_visualizer_scale: str = "default",
        visualization_spectral_limit: str = "0",
        visualization_labels: bool = True,
        samp_freq: int = 16000,
    ):
        self.scale = spectrum_visualizer_scale
        self.spectral_limit = visualization_spectral_limit
        self.labels = visualization_labels
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Spectrum visualization setting")
        group.add_argument(
            "--spectrum-visualizer-scale",
            default="default",
            choices=["default", "linear", "dB"],
            type=str,
            help="The scaling of the values in the spec.",
        )

    def plotsize(self):
        return PLOTSIZE

    def title(self):
        return TITLE

    def __call__(self, fig, ax, sample):
        if self.spectral_limit == "0":
            band_limit = (0, int(self.samp_freq / 2))
        else:
            b = np.array(self.spectral_limit.split("_")).astype(np.float64)
            band_limit = [b[0], b[1]]

        spec, freqs, line = ax.magnitude_spectrum(
            sample, Fs=self.samp_freq, scale=self.scale, color="limegreen"
        )
        ax.set_xlim(band_limit)
        if self.scale in ["default", "linear"]:
            ax.set_ylim([0, max(spec) + 0.01])

        if self.labels:
            plt.xlabel("Frequency [Hz]")
        else:
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlabel(None)
            ax.set_ylabel(None)
        return
