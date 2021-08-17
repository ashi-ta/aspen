#!/usr/bin/env python3
# encoding: utf-8
"""Apply ramp function"""

from logging import getLogger

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_processing_interface import AbsProcessingInterface

logger = getLogger(__name__)


class ApplyRamp(AbsCommonInterface, AbsProcessingInterface):
    """Apply ramp function to a given signal.

    Args:
        x: Input signal
        apply_ramp_duration: Duration of ramp function in millisecond. Defaults to 0.0.
        apply_ramp_wfunction: Ramp function.
            wfunction can apply some functions which are listed in Scipy doc or `linear` function.
            (https://docs.scipy.org/doc/scipy/reference/signal.windows.html)
            Defaults to "hann".
        apply_ramp_position: Position of application for ramp function.
            `onset`, `offset` and `both` are able to be applied. Defaults to "both".
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        apply_ramp_duration: float = 0.0,
        apply_ramp_wfunction: str = "hann",
        apply_ramp_position: str = "both",
        samp_freq: int = 16000,
    ):
        self.duration = apply_ramp_duration
        self.wfunction = apply_ramp_wfunction
        self.position = apply_ramp_position
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("apply-ramp setting")
        group.add_argument(
            "--apply-ramp-duration",
            default=0,
            type=float,
            help="Duration of ramp in millisecond",
        )
        group.add_argument(
            "--apply-ramp-wfunction",
            default="hann",
            type=str,
            help="Window function of ramp",
        )
        group.add_argument(
            "--apply-ramp-position",
            default="both",
            choices=["onset", "offset", "both"],
            type=str,
            help="Position of ramp",
        )
        return parser

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Apply ramp

        Args:
            x: Input signal

        Returns:
            Output signal
        """

        duration = int(self.duration * self.samp_freq / 1000)
        t = x.shape[0]
        if duration == 0:
            logger.warning("duration=0 means no ramp application")
            return x

        if self.wfunction == "linear":
            w_raise = np.linspace(0, 1, duration)
            w_fall = np.linspace(1, 0, duration)
        else:
            from scipy.signal import windows  # noqa: F401

            w = eval("windows." + self.wfunction)(duration * 2)
            w_raise = w[:duration]
            w_fall = w[duration:]

        if self.position == "onset":
            if t < duration:
                raise ValueError(
                    "input duration must be greater than ramp_duration, but got input={} and ramp={}".format(
                        t, duration
                    )
                )
            x[:duration] = x[:duration] * w_raise
        elif self.position == "offset":
            if t < duration:
                raise ValueError(
                    "input duration must be greater than ramp_duration, but got input={} and ramp={}".format(
                        t, duration
                    )
                )
            x[-duration:] = x[-duration:] * w_fall
        elif self.position == "both":
            if t < duration * 2:
                raise ValueError(
                    "input duration must be greater than 2*ramp_duration, but got input={} and 2*rmap={}".format(
                        t, duration * 2
                    )
                )
            x[:duration] = x[:duration] * w_raise
            x[-duration:] = x[-duration:] * w_fall
        else:
            raise ValueError("Invalid position")
        return x


def apply_ramp(
    x: np.ndarray,
    duration: float = 0.0,
    wfunction: str = "hann",
    position: str = "both",
    samp_freq: int = 16000,
) -> np.ndarray:
    """Apply ramp function to a given signal.

    Args:
        x: Input signal
        duration: Duration of ramp function in millisecond. Defaults to 0.0.
        wfunction: Ramp function.
            wfunction can apply some functions which are listed in Scipy doc or `linear` function.
            (https://docs.scipy.org/doc/scipy/reference/signal.windows.html)
            Defaults to "hann".
        position: Position of application for ramp function.
            `onset`, `offset` and `both` are able to be applied. Defaults to "both".
        samp_freq: Sampling frequency. Defaults to 16000.

    Returns:
        Output signal
    """
    return ApplyRamp(duration, wfunction, position, samp_freq)(x)
