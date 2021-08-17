#!/usr/bin/env python3
# encoding: utf-8
"""Visualize a waveform"""

from logging import getLogger

import matplotlib.pyplot as plt
import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_visualization_interface import AbsVisualizationInterface

logger = getLogger(__name__)

# Width, Height
PLOTSIZE = [10, 3]
TITLE = "waveform"


class WaveformVisualizer(AbsCommonInterface, AbsVisualizationInterface):
    """Visualize spectrum

    Args:
        waveform_visualizer_color: The color of line. Defaults to `dodgerblue`
        visualization_labels: The flag to add labels (title, xlabel, ylabel).
            Defaults to True.
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        waveform_visualizer_color: str = "dodgerblue",
        visualization_labels: bool = True,
        samp_freq: int = 16000,
    ):
        self.color = waveform_visualizer_color
        self.labels = visualization_labels
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Waveform visualization setting")
        group.add_argument(
            "--waveform-visualizer-color",
            default="dodgerblue",
            type=str,
            help="The color of line",
        )
        return parser

    def plotsize(self):
        return PLOTSIZE

    def title(self):
        return TITLE

    def __call__(self, fig, ax, sample):
        t = np.arange(sample.shape[0]) / self.samp_freq
        if self.labels:
            plt.xlabel("Time [s]")
        else:
            ax.set_xticks([])
            ax.set_yticks([])
        ax.plot(t, sample, color=self.color, linewidth=1.0)
        ax.set_xlim([0, np.max(t)])
        ax.set_ylim([np.min(sample), np.max(sample)])
        return
