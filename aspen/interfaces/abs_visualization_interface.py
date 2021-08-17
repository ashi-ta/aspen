#!/usr/bin/env python3
# encoding: utf-8
"""Abstract visualization interface"""

from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np


class AbsVisualizationInterface(ABC):
    @staticmethod
    def add_arguments(parser):
        """add plotter specific arguments"""
        return parser

    @abstractmethod
    def plotsize(self):
        """return plotter figure size [width, height]"""
        raise NotImplementedError

    @abstractmethod
    def title(self):
        """return title of figure"""
        raise NotImplementedError

    @abstractmethod
    def __call__(
        self,
        fig: plt.Figure,
        ax: plt.Axes,
        sample: np.ndarray,
    ):
        """Plot the figure.

        Args:
            fig: Figure object
            ax: Axes object
            sample: input waveform sequence (t, )
        """
        raise NotImplementedError
