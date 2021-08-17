#!/usr/bin/env python3
# encoding: utf-8

import logging
import os
import random
import sys

import configargparse
import numpy as np

from aspen.executors.processing_applier import ProcessingApplier
from aspen.executors.sound_generator import SoundGenerator
from aspen.executors.stimulus_transformer import StimulusTransformer
from aspen.executors.visualizer import Visualizer
from aspen.utils.io_utils import add_prefix_suffix
from aspen.utils.scaling_astype import scaling_astype


def get_parser():
    parser = configargparse.ArgumentParser(
        description="Generate stimulus",
        config_file_parser_class=configargparse.YAMLConfigFileParser,
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        "--config", "--conf", is_config_file=True, help="config file path"
    )

    parser.add_argument(
        "--wavlist",
        default=None,
        type=str,
        help="Path of listed wav file. "
        "If not specified, the signal is generated from scratch.",
    )
    parser.add_argument(
        "--rspecifier",
        default=None,
        type=str,
        help="Kaldi-style file reader. "
        "If not specified, the signal is generated from scratch.",
    )
    parser.add_argument(
        "--wspecifier",
        default=None,
        type=str,
        help="Kaldi-style file writer",
    )
    parser.add_argument(
        "--segments",
        default=None,
        type=str,
        help="Kaldi-style segments file path",
    )
    parser.add_argument(
        "--write-function",
        default=None,
        type=str,
        help="kaldiio write_function",
    )
    parser.add_argument("--outdir", default=None, type=str, help="Output directory")
    parser.add_argument(
        "--prefix", default=None, type=str, help="prefix of output file or key"
    )
    parser.add_argument(
        "--suffix", default=None, type=str, help="Suffix of output file or key"
    )
    parser.add_argument(
        "--play",
        action="store_true",
        help="The flag to play sound instead of writing file",
    )

    parser.add_argument(
        "--samp-freq", default=16000, type=int, help="Sampling frequency"
    )

    # other settings
    parser.add_argument(
        "--seed",
        default=None,
        type=int,
        help="Random seed. Default to current time.",
    )
    parser.add_argument("--verbose", "-V", default=0, type=int, help="Verbose option")

    return parser


def main(cmd_args):
    parser = get_parser()
    StimulusTransformer.add_arguments(parser)
    SoundGenerator.add_arguments(parser)
    ProcessingApplier.add_arguments(parser)
    Visualizer.add_arguments(parser)
    args, _ = parser.parse_known_args(cmd_args)
    # add argument of sub-classes to existing parser
    StimulusTransformer.stimulus_add_arguments(parser, args)
    SoundGenerator.sound_add_arguments(parser, args)
    ProcessingApplier.processing_add_arguments(parser, args)
    Visualizer.visualization_add_arguments(parser, args)

    # lazy help
    parser.add_argument(
        "--help", "-h", action="help", help="show this help message and exit"
    )
    args = parser.parse_args(cmd_args)

    if args.verbose > 0:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )
    else:
        logging.basicConfig(
            level=logging.WARN,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )

    logging.info(args)
    logging.info("python path = " + os.environ.get("PYTHONPATH", "(None)"))

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)
        logging.info("random seed = %d" % args.seed)

    if args.outdir is None and args.wspecifier != "ark:-":
        raise ValueError("--outdir argument must be specified.")
    elif args.outdir is not None:
        os.makedirs(args.outdir, exist_ok=True)
        logging.info("outdir = " + args.outdir)
    else:  # the case of wspecifier
        pass

    stimulus = StimulusTransformer(args)
    sounds = SoundGenerator(args)
    postprocessings = ProcessingApplier(args)
    visualize = Visualizer(args)

    if args.wavlist is not None:
        from aspen.utils.io_utils import WavReader as ReadHelper

        args.rspecifier = args.wavlist
    elif args.rspecifier is not None:
        from kaldiio import ReadHelper
    else:
        from aspen.utils.io_utils import WavReader as ReadHelper

    if args.play:
        from aspen.utils.io_utils import NumpyPlayer as WriteHelper
    elif args.wspecifier is None:
        from aspen.utils.io_utils import WavWriter as WriteHelper
    else:
        from kaldiio import WriteHelper

    with WriteHelper(args.wspecifier, write_function=args.write_function) as writer:
        with ReadHelper(args.rspecifier, segments=args.segments) as reader:
            for key, (sr, orgmat) in reader:
                x = []
                if key is not None:
                    logging.info("loaded file key = " + key)
                    logging.info(
                        "length of loaded file = {} [s]".format(
                            orgmat.shape[0] / args.samp_freq
                        )
                    )
                    cloned = orgmat.copy()
                    x.append(cloned)
                    if args.samp_freq != sr:
                        logging.warning(
                            "Overwrite sampling frequency from {} to {}".format(
                                args.samp_freq, sr
                            )
                        )
                        args.samp_freq = sr
                x.extend(sounds())
                for i in range(len(x)):
                    # processing as
                    x[i] = scaling_astype(x[i], out_dtype=np.float64)
                y = stimulus(x)
                logging.info(
                    "length of write file = {} [s]".format(y.shape[0] / args.samp_freq)
                )
                y = postprocessings(y)
                key = add_prefix_suffix(key, args.prefix, args.suffix)
                if args.wspecifier is None:
                    outkey = os.path.join(args.outdir, key + ".wav")
                else:
                    outkey = key
                writer(outkey, (args.samp_freq, scaling_astype(y, out_dtype="int16")))
                visualize(key, y, orgmat)

    logging.info("Done.")


if __name__ == "__main__":
    main(sys.argv[1:])
