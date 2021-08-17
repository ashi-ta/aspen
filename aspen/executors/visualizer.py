#!/usr/bin/env python3
# encoding: utf-8

import os
from logging import getLogger

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

from aspen.utils.cli_utils import strtobool
from aspen.utils.dynamic_classimport import dynamic_classimport

logger = getLogger(__name__)

plt.style.use("ggplot")

EPSILON = np.finfo(np.float64).eps

VISUALIZATIONS = ["waveform", "spectrogram", "spectrum", "mps"]


class Visualizer(object):
    def __init__(self, args):
        self.outdir = args.visualization_outdir
        self.labels = args.visualization_labels
        self.vis_original = args.visualization_vis_original
        self.temporal_limit = args.visualization_temporal_limit
        self.spectral_limit = args.visualization_spectral_limit
        self.visualizations = []
        self.widths = []
        self.heights = []
        for visualization in args.visualization_pipeline:
            visualizer_class = dynamic_classimport(
                visualization + "_visualizer", "aspen.visualizations"
            )
            visualizer_kwargs = visualizer_class.load_class_kwargs(args)
            visualizer = visualizer_class(**visualizer_kwargs)
            self.visualizations.append(visualizer)
            plotsize = visualizer.plotsize()
            self.widths.append(plotsize[0])
            self.heights.append(plotsize[1])
        self.samp_freq = args.samp_freq

    @staticmethod
    def add_arguments(parser):
        # visualization settings
        group = parser.add_argument_group("Visualizer setting")
        group.add_argument(
            "--visualization-pipeline",
            default=[],
            type=str,
            choices=VISUALIZATIONS,
            nargs="*",
            help="Stack of visualization figure type.",
        )
        group.add_argument(
            "--visualization-outdir",
            default="vis",
            type=str,
            help="Output directory of visualization",
        )
        group.add_argument(
            "--visualization-labels",
            default=True,
            type=strtobool,
            help="The flag to add labels (title, xlabel, ylabel)",
        )
        group.add_argument(
            "--visualization-vis-original",
            default=True,
            type=strtobool,
            help="The flag to add origianl data",
        )
        group.add_argument(
            "--visualization-temporal-limit",
            default="0",
            type=str,
            help="The limitation of temporal axis in millisecond (e.g. 0_1000)",
        )
        group.add_argument(
            "--visualization-spectral-limit",
            default="0",
            type=str,
            help="The limitation of spectral axis in Hz (e.g. 100_1000)",
        )
        return parser

    def show_pipeline(self):
        return self.visualizations

    @staticmethod
    def visualization_add_arguments(parser, args):
        for visualize in args.visualization_pipeline:
            visualize_class = dynamic_classimport(
                visualize + "_visualizer", "aspen.visualizations"
            )
            visualize_class.add_arguments(parser)
        return parser

    def __call__(self, key, outsample, orgsample=None):
        if len(self.visualizations) == 0:
            return
        else:
            os.makedirs(self.outdir, exist_ok=True)

        if not self.vis_original:
            orgsample = None

        # if the sample contains zero, set the smallest positive number to alleviate
        # RuntimeWarning: divide by zero encountered in log10 (Z = 10. * np.log10(spec))
        t = outsample.shape[0]
        outsample = np.where(outsample == 0, EPSILON, outsample).reshape(t, -1)

        num_channel = 1
        if outsample.shape[1] == 2:
            num_channel = 2

        if self.temporal_limit != "0":
            temporal_limit = np.array(self.temporal_limit.split("_")).astype(np.float64)
            temporal_limit = (temporal_limit * self.samp_freq / 1000).astype(np.int64)
            outsample = outsample[temporal_limit[0] : temporal_limit[1]]
        samples = [outsample]

        if orgsample is None:
            ncols = 1
        else:
            ncols = 2
            t = orgsample.shape[0]
            orgsample = np.where(orgsample == 0, EPSILON, orgsample).reshape(t, -1)
            if self.temporal_limit != "0":
                orgsample = orgsample[temporal_limit[0] : temporal_limit[1]]
            samples.append(orgsample)
            if orgsample.shape[1] == 2:
                num_channel = 2

        outpath = os.path.join(self.outdir, key + ".pdf")
        figsize = (max(self.widths) * ncols - 1, sum(self.heights) * num_channel)
        with PdfPages(outpath) as pp:
            fig = plt.figure(figsize=figsize, tight_layout=True)
            gspec = gridspec.GridSpec(figsize[1], figsize[0], wspace=0)
            visrowidx = 0
            for i, visualizer in enumerate(self.visualizations):
                colidx = 0
                for sample in samples:
                    rowidx = visrowidx
                    for c in range(sample.shape[1]):
                        ax = plt.subplot(
                            gspec[
                                rowidx : self.heights[i] + rowidx,
                                colidx : self.widths[i] + colidx - 1,
                            ]
                        )
                        if self.labels:
                            if colidx == 0:
                                if num_channel == 2:
                                    if c == 0:
                                        ax.set_title(visualizer.title() + "(left)")
                                    else:
                                        ax.set_title(visualizer.title() + "(right)")
                                else:
                                    ax.set_title(visualizer.title())
                            else:
                                if num_channel == 2:
                                    if c == 0:
                                        ax.set_title(
                                            "original " + visualizer.title() + "(left)"
                                        )
                                    else:
                                        ax.set_title(
                                            "original " + visualizer.title() + "(right)"
                                        )
                                else:
                                    ax.set_title("original " + visualizer.title())
                        visualizer(fig, ax, sample[:, c])
                        rowidx += self.heights[i]
                    colidx += self.widths[i]
                visrowidx += num_channel * self.heights[i]
            pp.savefig()
            plt.clf()
            plt.close()
