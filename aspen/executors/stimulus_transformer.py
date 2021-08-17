#!/usr/bin/env python3
# encoding: utf-8

from logging import getLogger
from typing import List

import numpy as np

from aspen.utils.cli_utils import strtobool
from aspen.utils.dynamic_classimport import dynamic_classimport

logger = getLogger(__name__)

STIMULI = [
    "auditory_streaming",
    "continuity",
    "identity",
    "iterated_rippled_noise",
    "locally_time_reversed_speech",
    "modulation_filtered_speech",
    "noise_vocoded_speech",
    "verbal_transformation",
]


class StimulusTransformer(object):
    def __init__(self, args):
        stimulus_class = dynamic_classimport(args.stimulus_module, "aspen.stimuli")
        stimulus_kwargs = stimulus_class.load_class_kwargs(args)
        self.stimulus = stimulus_class(**stimulus_kwargs)
        self.equalize = args.equalize_inout_duration

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Sound generation setting")
        group.add_argument(
            "--stimulus-module",
            required=True,
            type=str,
            choices=STIMULI,
            help="Auditory stimulus",
        )
        group.add_argument(
            "--equalize-inout-duration",
            type=strtobool,
            default=True,
            help="The flag to equalize the duration between input and output"
            "by copying edge value at the first position"
            "or removing the first few sample.",
        )
        return parser

    @staticmethod
    def stimulus_add_arguments(parser, args):
        stimulus_class = dynamic_classimport(args.stimulus_module, "aspen.stimuli")
        stimulus_class.add_arguments(parser)
        return parser

    def show_module(self):
        return self.stimulus

    def __call__(self, x: List[np.ndarray]) -> np.ndarray:
        in_t = x[0].shape[0]
        y = self.stimulus(x)
        out_t = y.shape[0]
        if self.equalize:
            if in_t != out_t:
                logger.warning(
                    "Equalize the duration between input={} and output={}".format(
                        in_t, out_t
                    )
                )

            if out_t < in_t:
                y = np.pad(y, [in_t - out_t, 0], "edge")
            elif out_t > in_t:
                y = y[(out_t - in_t) :]
            else:
                pass

        return y
