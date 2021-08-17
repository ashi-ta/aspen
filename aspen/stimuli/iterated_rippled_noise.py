#!/usr/bin/env python3
# encoding: utf-8
"""Iterated rippled noise"""

from typing import Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_stimulus_interface import AbsStimulusInterface


class IteratedRippledNoise(AbsCommonInterface, AbsStimulusInterface):
    """Generate iterated rippled noise (IRN).

    Args:
        samp_freq: Sampling frequency. Defaults to 16000.
        num_iteration: Number of iteration of delaying and adding.
            The value must be greater than 2 (num_iteration=1 is noise itself).
            Defaults to 8.
        delay: Duration of delay in millisecond. Defaults to 1.
            The value determines the fundamental frequency `f0=1/delay*1000`.
    """

    def __init__(
        self,
        samp_freq: int = 16000,
        num_iteration: int = 8,
        delay: float = 1,
    ):
        if num_iteration < 1:
            raise ValueError(
                "num_iteration must be greater than 2, but got {}".format(num_iteration)
            )
        self.samp_freq = samp_freq
        self.num_iteration = num_iteration
        self.delay = delay

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Iterated rippled noise (IRN) setting")
        group.add_argument(
            "--num-iteration",
            default=8,
            type=int,
            help="Number of iteration of delaying and adding"
            "The value must be greater than 2 (num_iteration=1 is noise itself).",
        )
        group.add_argument(
            "--delay",
            default=1,
            type=float,
            help="Duration of noise delay in millisecond."
            "The value determines the fundamental frequency (f=1/delay*1000).",
        )
        return parser

    def __call__(self, x: Sequence[np.ndarray]) -> np.ndarray:
        """Generate IRN.

        Args:
            x: Noise signal.
                x must be sequence-like object such as list, tuple and so on.

        Returns:
            Stimulus of IRN.
                The length of the output is `L - delay * (num_iteration - 1)`
                , where L is length of x.
        """

        if len(x) != 1:
            raise ValueError("input length must be 1, but got {}".format(len(x)))
        stimulus = x[0].copy()
        delay_sample = int(self.delay * self.samp_freq / 1000)
        # delay-and-add process
        for i in range(1, self.num_iteration):
            delay = i * delay_sample
            delay_noise = np.append(np.zeros(delay), x[0][:-delay])
            stimulus += delay_noise

        stimulus = stimulus[delay_sample * (self.num_iteration - 1) :]
        return stimulus
