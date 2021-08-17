from aspen.interfaces.abs_processing_interface import AbsProcessingInterface


def test_abs_processing_interface():
    class DummyClass(AbsProcessingInterface):
        def __call__(self, x):
            return x

    dummy = "dummy"
    assert dummy == DummyClass()(dummy)
