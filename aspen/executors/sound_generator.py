#!/usr/bin/env python3
# encoding: utf-8

from logging import getLogger
from typing import List

import numpy as np

from aspen.utils.dynamic_classimport import dynamic_classimport

logger = getLogger(__name__)

SOUNDS = [
    "am_tone",
    "click_train_pitch",
    "colored_noise",
    "complex_tone",
    "filtered_noise",
    "fm_tone",
    "pure_tone",
]


class SoundGenerator(object):
    def __init__(self, args):
        self.gen_sounds = []
        for sounds in args.sound_generation_pipeline:
            sounds_class = dynamic_classimport(sounds, "aspen.sounds")
            sound_kwargs = sounds_class.load_class_kwargs(args)
            self.gen_sounds.append(sounds_class(**sound_kwargs))

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Sound generation setting")
        group.add_argument(
            "--sound-generation-pipeline",
            default=[],
            type=str,
            choices=SOUNDS,
            nargs="*",
            help="Stack of sound type that is used by stimulus transformation",
        )
        return parser

    @staticmethod
    def sound_add_arguments(parser, args):
        for sounds in args.sound_generation_pipeline:
            sounds_class = dynamic_classimport(sounds, "aspen.sounds")
            sounds_class.add_arguments(parser)
        return parser

    def show_pipeline(self):
        return self.gen_sounds

    def __call__(self) -> List[np.ndarray]:
        x = []
        for gen_sound in self.gen_sounds:
            x.extend(gen_sound())
        return x
