#!/usr/bin/env python3
# encoding: utf-8
"""Normalize"""

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_processing_interface import AbsProcessingInterface


class Normalize(AbsCommonInterface, AbsProcessingInterface):
    """Nomarlize a signal.

    Args:
        normalize_method: Type of normalization method.
            `zscore` provide the mean (centre) of the distribution = 0 and
            standard deviation (spread or “width”) of the distribution = 1.
            Defaults to "zscore".

    Todo:
        Implementation of other method if necessary.
        REF(https://www.mathworks.com/help/matlab/ref/double.normalize.html)
    """

    def __init__(self, normalize_method: str = "zscore"):
        self.method = normalize_method

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("normalize setting")
        group.add_argument(
            "--normalize-method",
            default="zscore",
            type=str,
            choices=["zscore"],
            help="The type of method of normalization",
        )
        return parser

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Apply normalization

        Args:
            x: Input signal

        Returns:
            Output signal
        """
        if self.method == "zscore":
            # z_score = (x - mu) / sigma [mu = mean, sigma = standard deviation]
            return (x - x.mean()) / np.std(x)
        else:
            raise ValueError("Invalid method")


def normalize(x: np.ndarray, method: str = "zscore") -> np.ndarray:
    """Nomarlize a signal.

    Args:
        x: Input signal.
        method: Type of normalization method.
            `zscore` provide the mean (centre) of the distribution = 0 and
            standard deviation (spread or “width”) of the distribution = 1.
            Defaults to "zscore".

    Returns:
        Output signal.
    """
    return Normalize(method)(x)
