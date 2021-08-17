import argparse
import shutil

import numpy as np
import pytest
from matplotlib.testing.decorators import check_figures_equal

from aspen.visualizations.mps_visualizer import MpsVisualizer


@check_figures_equal(extensions=["pdf"])
def test_plot(fig_test, fig_ref):
    t = np.arange(0, 16000) / 16000
    test_x = np.sin(2 * np.pi * 1000 * t)
    ref_x = np.sin(2 * np.pi * 1000 * t + np.radians(180))

    test_ax = fig_test.subplots()
    MpsVisualizer(visualization_labels=False)(fig_test, test_ax, test_x)
    ref_ax = fig_ref.subplots()
    MpsVisualizer(visualization_labels=False)(fig_ref, ref_ax, ref_x)


@pytest.mark.parametrize("dbrange", [(40)])
def test_arguments(dbrange):
    parser = argparse.ArgumentParser()
    MpsVisualizer.add_arguments(parser)
    args = parser.parse_args(
        [
            "--mps-visualizer-dbrange",
            str(dbrange),
        ]
    )
    clsobj = MpsVisualizer(mps_visualizer_dbrange=args.mps_visualizer_dbrange)
    assert clsobj.dbrange == dbrange


@pytest.fixture(scope="session", autouse=True)
def remove_result_images_after_all():
    yield
    shutil.rmtree("result_images", ignore_errors=True)
