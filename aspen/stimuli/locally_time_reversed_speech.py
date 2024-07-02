#!/usr/bin/env python3
# encoding: utf-8
"""Locally time-reversed speech"""

from typing import Sequence

import librosa
import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_stimulus_interface import AbsStimulusInterface
from aspen.utils.cli_utils import strtobool


class LocallyTimeReversedSpeech(AbsCommonInterface, AbsStimulusInterface):
    """Generate locally time-reversed speech.

    Args:
        samp_freq: Sampling frequency. Defaults to 16000.
        reverse_duration: Duration of time-reverse in millisecond. Defaults to 50.
        randomize: Apply randomization within the segments instead of reverse. Defaults to False.
    """

    def __init__(
        self,
        samp_freq: int = 16000,
        reverse_duration: float = 50,
        randomize: bool = False,
    ):
        self.samp_freq = samp_freq
        self.reverse_duration = reverse_duration
        self.randomize = randomize
        if randomize:
            self.rng = np.random.default_rng()

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Locally time-reversed speech setting")
        group.add_argument(
            "--reverse-duration",
            required=True,
            type=float,
            help="Duration of time-reverse in millisecond.",
        )
        group.add_argument(
            "--randomize",
            default=False,
            type=strtobool,
            help="Apply randomization within the segments instead of reverse.",
        )
        return parser

    def __call__(self, x: Sequence[np.ndarray]) -> np.ndarray:
        """Generate locally time-reversed speech.

        Args:
            x: Speech signal.
                x must be sequence-like object such as list, tuple and so on.

        Returns:
            Stimulus of locally time-reversed speech.
        """
        if len(x) != 1:
            raise ValueError("input length must be 1, but got {}".format(len(x)))

        stimulus = x[0]
        t = stimulus.shape[0]
        reverse_duration = int(self.reverse_duration * self.samp_freq / 1000)
        head = librosa.util.frame(stimulus, frame_length=reverse_duration, hop_length=reverse_duration, axis=0)
        boundary = (t // reverse_duration) * reverse_duration

        if not self.randomize:
            head = np.flip(head, 1)
            tail = np.flip(stimulus[boundary:])
        else:
            head = self.rng.permutation(head, 1)
            tail = self.rng.permutation(stimulus[boundary:])
        stimulus = np.concatenate([np.hstack(head), tail])
        return stimulus
