#!/usr/bin/env python3
# encoding: utf-8

from logging import getLogger

import numpy as np

from aspen.utils.dynamic_classimport import dynamic_classimport

logger = getLogger(__name__)

PROCESSINGS = [
    "amplitude_maximize",
    "apply_ramp",
    "declip",
    "extract_envelope",
    "filter_signal",
    "normalize",
]


class ProcessingApplier(object):
    def __init__(self, args):
        self.postprocess = []
        for process in args.postprocess_pipeline:
            process_class = dynamic_classimport(process, "aspen.processings")
            process_kwargs = process_class.load_class_kwargs(args)
            self.postprocess.append(process_class(**process_kwargs))

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("Postprocessing setting")
        group.add_argument(
            "--postprocess-pipeline",
            default=[],
            type=str,
            choices=PROCESSINGS,
            nargs="*",
            help="Stack of postprocessing",
        )
        return parser

    @staticmethod
    def processing_add_arguments(parser, args):
        for process in args.postprocess_pipeline:
            process_class = dynamic_classimport(process, "aspen.processings")
            process_class.add_arguments(parser)
        return parser

    def show_pipeline(self):
        return self.postprocess

    def __call__(self, x: np.ndarray) -> np.ndarray:
        for proc in self.postprocess:
            # apply_along_axis is applicable for either single or multi channel signal
            x = np.apply_along_axis(proc, 0, x)
        return x
