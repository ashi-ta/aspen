import argparse

from aspen.interfaces.abs_visualization_interface import AbsVisualizationInterface


def test_abs_visualization_interface():
    class DummyClass(AbsVisualizationInterface):
        def plotsize(self):
            return [10, 10]

        def title(self):
            return "dummy"

        def __call__(self, fig, ax, sample):
            return fig, ax, sample

    indata = ("dummy1", "dummy2", "dummy3")
    assert indata == DummyClass()(*indata)
    assert [10, 10] == DummyClass().plotsize()
    DummyClass.add_arguments(argparse.ArgumentParser())
