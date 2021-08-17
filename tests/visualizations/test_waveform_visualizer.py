import argparse
import shutil

import numpy as np
import pytest
from matplotlib.testing.decorators import check_figures_equal

from aspen.visualizations.waveform_visualizer import WaveformVisualizer


@check_figures_equal(extensions=["pdf"])
def test_plot(fig_test, fig_ref):
    t = np.arange(0, 16000) / 16000
    test_x = np.sin(2 * np.pi * 1000 * t)
    ref_x = np.sin(2 * np.pi * 1000 * t + np.radians(360))

    test_ax = fig_test.subplots()
    WaveformVisualizer(visualization_labels=False)(fig_test, test_ax, test_x)
    ref_ax = fig_ref.subplots()
    WaveformVisualizer(visualization_labels=False)(fig_ref, ref_ax, ref_x)


@pytest.mark.parametrize("color", ["darkorange"])
def test_arguments(color):
    parser = argparse.ArgumentParser()
    WaveformVisualizer.add_arguments(parser)
    args = parser.parse_args(
        [
            "--waveform-visualizer-color",
            str(color),
        ]
    )
    clsobj = WaveformVisualizer(
        waveform_visualizer_color=args.waveform_visualizer_color
    )
    assert clsobj.color == color


@pytest.fixture(scope="session", autouse=True)
def remove_result_images_after_all():
    yield
    shutil.rmtree("result_images", ignore_errors=True)
