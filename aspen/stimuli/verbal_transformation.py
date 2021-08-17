#!/usr/bin/env python3
# encoding: utf-8
"""Verbal transformation stimulus"""

from typing import Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_stimulus_interface import AbsStimulusInterface


class VerbalTransformation(AbsCommonInterface, AbsStimulusInterface):
    """Stimulus that occurs the verbal transformation.

    Args:
        num_iteration: Number of iteratoins. Defaults to 20.
    """

    def __init__(
        self,
        num_iteration: int = 20,
    ):
        self.num_iteration = num_iteration

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Verbal transformation effect setting")
        group.add_argument(
            "--num-iteration", default=20, type=int, help="Number of iteration"
        )
        return parser

    def __call__(self, x: Sequence[np.ndarray]) -> np.ndarray:
        """Generate stimulus for verbal transformation.

        Args:
            x: Speech signal.
                x must be sequence-like object such as list, tuple and so on.

        Returns:
            Stimulus of verbal transformation.
        """
        if len(x) != 1:
            raise ValueError("input length must be 1, but got {}".format(len(x)))

        stimulus = np.tile(x[0], self.num_iteration)
        return stimulus
