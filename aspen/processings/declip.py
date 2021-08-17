#!/usr/bin/env python3
# encoding: utf-8
"""Declip"""

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_processing_interface import AbsProcessingInterface


class Declip(AbsCommonInterface, AbsProcessingInterface):
    """Declip a signal if saturated.

    Args:
        declip_thres: The threshold whether the signal is saturated or not.
            Defaults to 1.0.
    """

    def __init__(self, declip_thres: float = 1.0):
        self.thres = declip_thres

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("declip setting")
        group.add_argument(
            "--declip-thres",
            default=1,
            type=float,
            help="Threshold to be treated as a clipping",
        )
        return parser

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Apply declip

        Args:
            x: Input signal

        Returns:
            Output signal
        """
        if self.thres <= 0:
            raise ValueError(
                "thres must be greater than 0, but got {}".format(self.thres)
            )
        xabs = np.abs(x)
        if np.any(xabs > self.thres):
            return x / xabs.max() * self.thres
        else:
            return x


def declip(x: np.ndarray, thres: float = 1.0) -> np.ndarray:
    """Declip a signal if saturated.

    Args:
        x: Input signal
        thres: The threshold whether the signal is saturated or not.
            Defaults to 1.0.

    Returns:
        Output signal
    """
    return Declip(thres)(x)
