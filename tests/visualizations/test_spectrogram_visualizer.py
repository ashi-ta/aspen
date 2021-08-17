import argparse
import shutil

import numpy as np
import pytest
from matplotlib.testing.decorators import check_figures_equal

from aspen.visualizations.spectrogram_visualizer import SpectrogramVisualizer


@check_figures_equal(extensions=["pdf"])
def test_plot(fig_test, fig_ref):
    t = np.arange(0, 16000) / 16000
    test_x = np.sin(2 * np.pi * 1000 * t)
    ref_x = np.sin(2 * np.pi * 1000 * t + np.radians(180))

    test_ax = fig_test.subplots()
    SpectrogramVisualizer(visualization_labels=False)(fig_test, test_ax, test_x)
    ref_ax = fig_ref.subplots()
    SpectrogramVisualizer(visualization_labels=False)(fig_ref, ref_ax, ref_x)


@pytest.mark.parametrize("cmap", ["inferno"])
def test_arguments(cmap):
    parser = argparse.ArgumentParser()
    SpectrogramVisualizer.add_arguments(parser)
    args = parser.parse_args(
        [
            "--spectrogram-visualizer-cmap",
            str(cmap),
        ]
    )
    clsobj = SpectrogramVisualizer(
        spectrogram_visualizer_cmap=args.spectrogram_visualizer_cmap
    )
    assert clsobj.cmap == cmap


@pytest.fixture(scope="session", autouse=True)
def remove_result_images_after_all():
    yield
    shutil.rmtree("result_images", ignore_errors=True)
