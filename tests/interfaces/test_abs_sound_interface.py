from aspen.interfaces.abs_sound_interface import AbsSoundInterface


def test_abs_sound_interface():
    class DummyClass(AbsSoundInterface):
        def __init__(self, indata, num_signals):
            self.indata = indata
            self.num_signals = num_signals

        def _generate_each(self, idx):
            return self.indata[idx]

    indata = ["dummy1", "dummy2", "dummy3", "dummy4", "dummy5"]
    num_signals = 5
    out = DummyClass(indata, num_signals)()
    assert out == indata
