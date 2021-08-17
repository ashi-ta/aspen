#!/usr/bin/env python3
# encoding: utf-8
"""Click train pitch"""

from typing import List, Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_sound_interface import AbsSoundInterface


class ClickTrainPitch(AbsCommonInterface, AbsSoundInterface):
    """Generate click train pitch.

    Args:
        click_train_pitch_duration: The duration of click train pitch in millisecond.
            Defaults to [1000].
        click_train_pitch_interval: Interval duration of clicks in millisecond.
            This variable determines the fundamental frequency (f0 = 1 / interval * 1000). Defaults to [1].
        click_train_pitch_num_signals: Number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        click_train_pitch_duration: Sequence[float] = [1000],
        click_train_pitch_interval: Sequence[float] = [1],
        click_train_pitch_num_signals: int = 1,
        samp_freq: int = 16000,
    ):
        self.duration = click_train_pitch_duration
        self.interval = click_train_pitch_interval
        self.num_signals = click_train_pitch_num_signals
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Click train pitch setting")
        group.add_argument(
            "--click-train-pitch-duration",
            type=float,
            default=[1000],
            nargs="*",
            help="Duration of click train pitch in millisecond",
        )
        group.add_argument(
            "--click-train-pitch-interval",
            type=float,
            default=[1],
            nargs="*",
            help="Interval duration of click train in millisecond."
            "This variable determines the fundamental frequency (f=1/interval*1000).",
        )
        group.add_argument(
            "--click-train-pitch-num-signals",
            type=int,
            default=1,
            help="Number of signals. If this value greater than 2,"
            "the other arguments should contain 2 types.",
        )

        return parser

    def _generate_each(self, idx: int) -> np.ndarray:
        duration = int(self.duration[idx] * self.samp_freq / 1000)
        click_interval = int(self.interval[idx] * self.samp_freq / 1000)
        if click_interval <= 0:
            raise ValueError(
                "click_interval mustbe greater than 0, but got{}".format(click_interval)
            )

        # one click (click + interval)
        x = np.append(np.ones(1), np.zeros(click_interval - 1))
        # iteration
        num_repetition = int(np.ceil(duration / click_interval))
        x = np.tile(x, num_repetition)
        x = x[:duration]
        return x


def click_train_pitch(
    duration: Sequence[float] = [1000],
    interval: Sequence[float] = [1],
    num_signals: int = 1,
    samp_freq: int = 16000,
) -> List[np.ndarray]:
    """Generate click train pitch.

    Args:
        duration: The duration of click train pitch in millisecond.
            Defaults to [1000].
        interval: Interval duration of clicks in millisecond.
            This variable determines the fundamental frequency (f0 = 1 / interval * 1000). Defaults to [1].
        num_signals: Number of signals.
            If this value greater than 2, the other arguments should contain 2 types.
            Defaults to 1.
        samp_freq: Sampling frequency. Defaults to 16000.

    Returns:
        Output signals.
    """
    return ClickTrainPitch(duration, interval, num_signals, samp_freq)()
