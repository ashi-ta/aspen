import argparse
import shutil

import numpy as np

from aspen.executors.visualizer import VISUALIZATIONS, Visualizer


def test_arguments():
    parser = argparse.ArgumentParser()
    Visualizer.add_arguments(parser)

    cmd_args = (
        ["--visualization-pipeline"]
        + VISUALIZATIONS
        + ["--visualization-outdir", "dummy"]
        + ["--visualization-labels", "False"]
        + ["--visualization-vis-original", "False"]
        + ["--visualization-temporal-limit", "0_1000"]
        + ["--visualization-spectral-limit", "0_1000"]
    )
    args, _ = parser.parse_known_args(cmd_args)
    Visualizer.visualization_add_arguments(parser, args)
    args = parser.parse_args(cmd_args)
    args.samp_freq = 16000

    vis = Visualizer(args)
    pipeline = vis.show_pipeline()
    pipeline_module = [i.__class__.__module__.split(".")[-1] for i in pipeline]
    assert len(pipeline) == len(VISUALIZATIONS)
    assert pipeline_module == [i + "_visualizer" for i in VISUALIZATIONS]
    assert vis.outdir == "dummy"
    assert vis.labels is False
    assert vis.vis_original is False
    assert vis.temporal_limit == "0_1000"
    assert vis.spectral_limit == "0_1000"


def test_call():
    t = np.arange(0, 16000) / 16000
    x = np.sin(2 * np.pi * 440 * t, dtype=np.float64)

    parser = argparse.ArgumentParser()
    Visualizer.add_arguments(parser)

    cmd_args = ["--visualization-pipeline"] + VISUALIZATIONS
    args, _ = parser.parse_known_args(cmd_args)
    Visualizer.visualization_add_arguments(parser, args)
    args = parser.parse_args(cmd_args)
    args.samp_freq = 16000

    vis = Visualizer(args)
    vis("dummy1", x, x)
    x_binaural = np.stack([x, x], axis=1).reshape(16000, 2)
    vis("dummy2", x_binaural, x_binaural)
    shutil.rmtree("vis")
