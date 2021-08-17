import numpy as np

from aspen.utils.dynamic_classimport import dynamic_classimport


def test_dynamic_classimport():
    t = np.arange(0, 16000) / 16000
    x = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    pure_tone_cls = dynamic_classimport("pure_tone", "aspen.sounds")
    np.testing.assert_array_equal(pure_tone_cls()()[0], x)
