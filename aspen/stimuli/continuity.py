#!/usr/bin/env python3
# encoding: utf-8
"""Continuity illusion stimulus"""

from typing import Sequence

import numpy as np

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_stimulus_interface import AbsStimulusInterface
from aspen.processings.apply_ramp import apply_ramp
from aspen.utils.snr_utils import get_snr_noise


class Continuity(AbsCommonInterface, AbsStimulusInterface):
    """Stimulus that occurs continuity illusion.

    Basic stimulus for continuity illusion consists of the repetitions of target_signal and gap_signal.

    Args:
        samp_freq: Sampling frequency. Defaults to 16000.
        target_duration: Duration of target signal in millisecond. Defaults to 100.
        gap_duration: Duration of gap signal in millisecond. Defaults to 100.
        gap_method: Kind of gap method.
            In the case of `replace` and `silent`, the gap sections are replaced by noise and silent, respectively.
            In the case of `overlap`, the target signal superimpose noise in the gap sections. Defaults to "replace".
        gap_ramp_duration: Duration of ramps in the gap sections in millisecond. Defaults to 10.
        target_snr: Signal-to-noise ratio. Defaults to 20.
    """

    def __init__(
        self,
        samp_freq: int = 16000,
        target_duration: float = 100,
        gap_duration: float = 100,
        gap_method: str = "replace",
        gap_ramp_duration: float = 10,
        target_snr: float = 20,
    ):
        self.samp_freq = samp_freq
        self.target_duration = target_duration
        self.gap_duration = gap_duration
        self.gap_method = gap_method
        self.gap_ramp_duration = gap_ramp_duration
        self.target_snr = target_snr

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Continuity illusion setting")
        group.add_argument(
            "--target-duration",
            default=100,
            type=float,
            help="Duration of target in millisecond.",
        )
        group.add_argument(
            "--gap-duration",
            default=100,
            type=float,
            help="Duration of gap in millisecond.",
        )
        group.add_argument(
            "--gap-method",
            default="replace",
            type=str,
            choices=["replace", "silent", "overlap"],
            help="Kind of gap method",
        )
        group.add_argument(
            "--gap-ramp-duration",
            default=10,
            type=float,
            help="Duration of ramp of target and gap signal in millisecond.",
        )
        group.add_argument(
            "--target-snr",
            default=20,
            type=float,
            help="Signal-to-noise ratio",
        )
        return parser

    def __call__(self, x: Sequence[np.ndarray]) -> np.ndarray:
        """Generate stimulus for continuity illusion.

        Args:
            x: Target signal (`np.ndarray`) and noise signal (`np.ndarray`).
                x must be sequence-like object such as list, tuple and so on.
                The first element is target signal and the second one is noise (i.e. [target, noise]).
                The duration of noise must be equal to or greater than the one of target signal.
                In the case of `gap_method=silent`, the second element is ignored.

        Returns:
            Stimulus for continuity illusion.
        """

        if self.gap_method != "silent" and len(x) != 2:
            raise ValueError(
                "x must contain the 2 elements which is comprised by"
                "[target, noise] in the case of 'replace' or 'overlap'."
            )

        # use the clone object to estimate the SNR
        stimulus = x[0].copy()
        stimulus_t = stimulus.shape[0]
        snr_noise = get_snr_noise(stimulus, x[1].copy(), self.target_snr)

        target_duration = int(self.target_duration * self.samp_freq / 1000)
        gap_duration = int(self.gap_duration * self.samp_freq / 1000)
        gap_ramp_duration = int(self.gap_ramp_duration * self.samp_freq / 1000)

        x_onset = 0
        x_offset = target_duration
        x_prev_offset = target_duration
        section_len = target_duration + gap_duration - 2 * gap_ramp_duration
        # insertion of each processing(replace, overlap, silent) iteratively
        # onset and offset means the those of target potion of tone
        # head processing
        while x_offset < stimulus_t:
            # apply ramp function at the position except for whole signal onset & offset
            if x_onset == 0:
                position = "offset"
            elif x_offset < stimulus_t:
                position = "both"
            elif x_offset == stimulus_t:
                position = "onset"
            stimulus[x_onset:x_offset] = apply_ramp(
                stimulus[x_onset:x_offset],
                duration=self.gap_ramp_duration,
                position=position,
                samp_freq=self.samp_freq,
            )

            if x_onset > 0:
                n_onset = x_prev_offset - gap_ramp_duration
                n_offset = x_onset + gap_ramp_duration
                noise = apply_ramp(
                    snr_noise[n_onset:n_offset],
                    duration=self.gap_ramp_duration,
                    position="both",
                    samp_freq=self.samp_freq,
                )
                # Ramp centers of noise are synchronized with
                # those of the respective input offsets and onsets.
                if self.gap_method == "overlap":
                    stimulus[n_onset:n_offset] += noise
                else:
                    stimulus[x_prev_offset:x_onset] = np.zeros(x_onset - x_prev_offset)
                    if self.gap_method == "replace":
                        stimulus[n_onset:n_offset] += noise
            # update onset
            x_prev_offset = x_offset
            # next onset & offset
            x_onset += section_len
            x_offset += section_len

        # tail processing
        remain_t = stimulus_t - x_prev_offset
        if remain_t <= gap_ramp_duration:
            pass
        elif (
            remain_t > gap_ramp_duration
            and remain_t <= gap_duration - gap_ramp_duration
        ):  # end in the middle of gap
            n_onset = x_prev_offset - gap_ramp_duration
            n_offset = stimulus_t
            noise = apply_ramp(
                snr_noise[n_onset:n_offset],
                duration=self.gap_ramp_duration,
                position="onset",
                samp_freq=self.samp_freq,
            )
            if self.gap_method == "overlap":
                stimulus[n_onset:n_offset] += noise
            else:
                stimulus[x_prev_offset:stimulus_t] = np.zeros(remain_t)
                if self.gap_method == "replace":
                    stimulus[n_onset:n_offset] += noise
        else:  # end in the middle of target
            stimulus[x_onset:] = apply_ramp(
                stimulus[x_onset:], duration=self.gap_ramp_duration, position="onset"
            )
            n_onset = x_prev_offset - gap_ramp_duration
            n_offset = x_onset + gap_ramp_duration
            noise = apply_ramp(
                snr_noise[n_onset:n_offset],
                duration=self.gap_ramp_duration,
                position="both",
                samp_freq=self.samp_freq,
            )
            if self.gap_method == "overlap":
                stimulus[n_onset:n_offset] += noise
            else:
                stimulus[x_prev_offset:x_onset] = np.zeros(x_onset - x_prev_offset)
                if self.gap_method == "replace":
                    stimulus[n_onset:n_offset] += noise

        return stimulus
