from argparse import Namespace

import pytest

from aspen.interfaces.abs_common_interface import AbsCommonInterface


def test_abs_common_interface():
    class DummyClass(AbsCommonInterface):
        pass

    with pytest.raises(RuntimeError):
        DummyClass()

    class DummyClass(AbsCommonInterface):
        def __init__(self, dummy1, dummy2="dummy2"):
            pass

    args = Namespace()
    args.dummy1 = "dummy1"
    kwargs = DummyClass.load_class_kwargs(args)
    assert kwargs["dummy1"] == "dummy1"
    assert kwargs["dummy2"] == "dummy2"
