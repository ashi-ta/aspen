#!/usr/bin/env python3
# encoding: utf-8
"""Amplitude maximize"""

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_processing_interface import AbsProcessingInterface


class AmplitudeMaximize(AbsCommonInterface, AbsProcessingInterface):
    """Maximize the amplitude.

    Args:
        amplitude_maximize_maximum_num: Maximization value.
            Upper limit of signal amplitude is set to this value. Defaults to 1.0.
    """

    def __init__(self, amplitude_maximize_maximum_num: float = 1.0):
        self.maximum_num = amplitude_maximize_maximum_num

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("amplitude-maximize setting")
        group.add_argument(
            "--amplitude-maximize-maximum-num",
            default=1.0,
            type=float,
            help="Maximization value",
        )
        return parser

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Apply amplitude maximize

        Args:
            x: Input signal

        Returns:
            Output signal
        """
        if self.maximum_num <= 0:
            raise ValueError(
                "maximum_num must be positive, but got {}".format(self.maximum_num)
            )
        xabs = np.abs(x)
        if np.any(xabs == self.maximum_num) and not np.any(xabs > self.maximum_num):
            return x
        else:
            return x / xabs.max() * self.maximum_num


def amplitude_maximize(x: np.ndarray, maximum_num: float = 1.0) -> np.ndarray:
    """Maximize the amplitude.

    Args:
        x: Input signal
        maximum_num: Maximization value.
            Upper limit of signal amplitude is set to this value. Defaults to 1.0.

    Returns:
        Output signal
    """
    return AmplitudeMaximize(maximum_num)(x)
