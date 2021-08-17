#!/usr/bin/env python3
# encoding: utf-8
"""Auditory streaming stimulus"""

from typing import Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_stimulus_interface import AbsStimulusInterface
from aspen.processings.apply_ramp import apply_ramp


class AuditoryStreaming(AbsCommonInterface, AbsStimulusInterface):
    """Stimulus that occurs the auditory streaming.

    Basic stimulus for auditory streaming consists of A-B-A--A-B-A--... sequence.
    A and B are arbitrary signal such as pure tone, harmonic complex tone and so on.

    Args:
        samp_freq: Sampling frequency. Defaults to 16000.
        num_repetition: Number of repetition of A-B-A sequence. Defaults to 50.
        ab_interval: Interval between A and B signal in millisecond. Defaults to 60.
        aba_interval: Interval between A-B-A and A-B-A sequence in millisecond. Defaults to 170.
        ab_ramp_duration: Ramp duration of A and B in millisecond. Defaults to 5.
    """

    def __init__(
        self,
        samp_freq: int = 16000,
        num_repetition: int = 50,
        ab_interval: float = 60,
        aba_interval: float = 170,
        ab_ramp_duration: float = 5,
    ):
        self.samp_freq = samp_freq
        self.num_repetition = num_repetition
        self.ab_interval = ab_interval
        self.aba_interval = aba_interval
        self.ab_ramp_duration = ab_ramp_duration

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group(
            "Auditory streaming setting (A-B-A--A-B-A--...)"
        )
        group.add_argument(
            "--num-repetition",
            default=50,
            type=int,
            help="Number of repetition of A-B-A sequence",
        )
        group.add_argument(
            "--ab-interval",
            default=60,
            type=float,
            help="Interval duration between A and B in millisecond",
        )
        group.add_argument(
            "--aba-interval",
            default=170,
            type=int,
            help="Interval duration between A-B-A and A-B-A",
        )
        group.add_argument(
            "--ab-ramp-duration",
            default=5,
            type=float,
            help="Duration of ramp of target and gap signal in millisecond.",
        )
        return parser

    def __call__(self, x: Sequence[np.ndarray]) -> np.ndarray:
        """Generate stimulus for auditory streaming.

        Args:
            x: A (`np.ndarray`) and B (`np.ndarray`) signal.
                x must be sequence-like object such as list, tuple and so on.
                The first element is signal A and the second one is signal B (i.e. [A, B]).

        Returns:
            Stimulus for auditory streaming.
        """
        if len(x) != 2:
            raise ValueError("x must have the 2 elements which is comprised by [A, b]")
        # generate A-B-A-- sequence
        ab_i = np.zeros(int(self.ab_interval * self.samp_freq / 1000))
        aba_i = np.zeros(int(self.aba_interval * self.samp_freq / 1000))
        y = []
        for each_x in x:
            y.append(
                apply_ramp(
                    each_x,
                    duration=self.ab_ramp_duration,
                    position="both",
                    samp_freq=self.samp_freq,
                )
            )
        aba = np.concatenate([y[0], ab_i, y[1], ab_i, y[0], aba_i])
        # repeat A-B-A-- sequence
        stimulus = np.tile(aba, self.num_repetition)
        return stimulus
