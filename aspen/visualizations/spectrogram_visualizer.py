#!/usr/bin/env python3
# encoding: utf-8
"""Visualize a spectrogram"""

from logging import getLogger
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_visualization_interface import \
    AbsVisualizationInterface

logger = getLogger(__name__)

# Width, Height
PLOTSIZE = [10, 3]
TITLE = "spectrogram"


class SpectrogramVisualizer(AbsCommonInterface, AbsVisualizationInterface):
    """Visualize spectrogram

    Args:
        spectrogram_visualizer_scale: Same value of `scale` augment of specgram in matplotlib.
            (Ref: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.specgram.html)
            Defaults to `default`.
        spectrogram_visualizer_vmax: Same value of `vmax` augment of specgram in matplotlib.
        spectrogram_visualizer_vmin: Same value of `vmin` augment of specgram in matplotlib.
        spectrogram_visualizer_cmap: Colormap. Defaults to `viridis`.
        visualization_spectral_limit: The limitation of spectral axis in Hz (e.g. 100_1000)
        visualization_labels: The flag to add labels (title, xlabel, ylabel).
            Defaults to "0" (= do nothing).
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        spectrogram_visualizer_scale: str = "default",
        spectrogram_visualizer_vmax: Optional[float] = None,
        spectrogram_visualizer_vmin: Optional[float] = None,
        spectrogram_visualizer_cmap: str = "viridis",
        visualization_spectral_limit: str = "0",
        visualization_labels: bool = True,
        samp_freq: int = 16000,
    ):
        self.scale = spectrogram_visualizer_scale
        self.vmax = spectrogram_visualizer_vmax
        self.vmin = spectrogram_visualizer_vmin
        self.cmap = spectrogram_visualizer_cmap
        self.spectral_limit = visualization_spectral_limit
        self.labels = visualization_labels
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Spectrogram visualization setting")
        group.add_argument(
            "--spectrogram-visualizer-scale",
            default="default",
            type=str,
            help="Same value of `scale` augment of specgram in matplotlib.",
        )
        group.add_argument(
            "--spectrogram-visualizer-vmax",
            default=None,
            type=float,
            help="Same value of `vmax` augment of specgram in matplotlib.",
        )
        group.add_argument(
            "--spectrogram-visualizer-vmin",
            default=None,
            type=float,
            help="Same value of `vmin` augment of specgram in matplotlib.",
        )
        group.add_argument(
            "--spectrogram-visualizer-cmap",
            default="viridis",
            type=str,
            help="Colormap",
        )
        return parser

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

        t = np.arange(sample.shape[0]) / self.samp_freq
        if self.labels:
            plt.xlabel("Time [s]")
            plt.ylabel("Frequency [Hz]")
        else:
            ax.set_xticks([])
            ax.set_yticks([])
        with np.errstate(divide="ignore"):
            spec, freqs, t, im = ax.specgram(
                sample,
                Fs=self.samp_freq,
                xextent=(0, np.max(t)),
                scale=self.scale,
                vmax=self.vmax,
                vmin=self.vmin,
                cmap=self.cmap,
            )
        ax.set_xlim([0, np.max(t)])
        ax.set_ylim(band_limit)
        return
