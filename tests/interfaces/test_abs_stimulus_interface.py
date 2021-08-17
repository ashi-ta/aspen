import numpy as np

from aspen.interfaces.abs_stimulus_interface import AbsStimulusInterface


def test_abs_stimulus_interface():
    class DummyClass(AbsStimulusInterface):
        def __call__(self, x):
            return x

    indata = [np.ones(10)]
    out = DummyClass()(indata)
    assert out == indata
