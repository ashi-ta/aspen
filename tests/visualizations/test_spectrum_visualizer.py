import shutil

import numpy as np
import pytest
from matplotlib.testing.decorators import check_figures_equal

from aspen.visualizations.spectrum_visualizer import SpectrumVisualizer


@check_figures_equal(extensions=["pdf"])
def test_plot(fig_test, fig_ref):
    t = np.arange(0, 16000) / 16000
    test_x = np.sin(2 * np.pi * 1000 * t)
    ref_x = np.sin(2 * np.pi * 1000 * t + np.radians(180))

    test_ax = fig_test.subplots()
    SpectrumVisualizer(visualization_labels=False)(fig_test, test_ax, test_x)
    ref_ax = fig_ref.subplots()
    SpectrumVisualizer(visualization_labels=False)(fig_ref, ref_ax, ref_x)


@pytest.fixture(scope="session", autouse=True)
def remove_result_images_after_all():
    yield
    shutil.rmtree("result_images", ignore_errors=True)
