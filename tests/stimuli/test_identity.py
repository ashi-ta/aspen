import argparse

import numpy as np
import pytest

from aspen.stimuli.identity import Identity


@pytest.fixture(scope="module")
def indata():
    t = np.arange(0, 16000) / 16000
    return np.sin(2 * np.pi * 440 * t, dtype=np.float64)


def test_raise_input_length_valueerror(indata):
    with pytest.raises(ValueError):
        Identity()([np.ones(10), np.ones(10)])


def test_equal_with_default(indata):
    tone = Identity()([indata])
    np.testing.assert_array_equal(indata, tone)


def test_binaural(indata):
    binaural = np.stack([indata, indata], axis=1)
    tone = Identity(binaural=True)([indata, indata])
    np.testing.assert_array_equal(binaural, tone)


@pytest.mark.parametrize("binaural", [(True), (False)])
def test_arguments(binaural):
    parser = argparse.ArgumentParser()
    Identity.add_arguments(parser)
    args = parser.parse_args(
        [
            "--binaural",
            str(binaural),
        ]
    )
    clsobj = Identity(binaural=args.binaural)
    assert clsobj.binaural == binaural
