#!/usr/bin/env python3
# encoding: utf-8

import logging
import os
import sys

import configargparse

from aspen.executors.visualizer import Visualizer
from aspen.utils.io_utils import add_prefix_suffix


def get_parser():
    parser = configargparse.ArgumentParser(
        description="Generate stimulus waveform or kaldi-format ark,scp",
        config_file_parser_class=configargparse.YAMLConfigFileParser,
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
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
        "--segments",
        default=None,
        type=str,
        help="Kaldi-style segments file path",
    )
    parser.add_argument(
        "--prefix", default=None, type=str, help="prefix of output file or key"
    )
    parser.add_argument(
        "--suffix", default=None, type=str, help="Suffix of output file or key"
    )
    parser.add_argument(
        "--samp-freq", default=16000, type=int, help="Sampling frequency"
    )
    parser.add_argument("--verbose", "-V", default=0, type=int, help="Verbose option")

    return parser


def main(cmd_args):
    parser = get_parser()
    Visualizer.add_arguments(parser)
    args, _ = parser.parse_known_args(cmd_args)
    Visualizer.visualization_add_arguments(parser, args)
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

    if args.wavlist is not None:
        from aspen.utils.io_utils import WavReader as ReadHelper

        args.rspecifier = args.wavlist
    elif args.rspecifier is not None:
        from kaldiio import ReadHelper
    else:
        raise ValueError("wavlist or rspecifier must be specified.")

    visualize = Visualizer(args)

    with ReadHelper(args.rspecifier, segments=args.segments) as reader:
        for key, (sr, orgmat) in reader:
            key = add_prefix_suffix(key, args.prefix, args.suffix)
            visualize(key, orgmat, None)

    logging.info("Done.")


if __name__ == "__main__":
    main(sys.argv[1:])
