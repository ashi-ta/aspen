import os

import numpy as np
import pytest

from aspen.utils.io_utils import NumpyPlayer, WavReader, WavWriter, add_prefix_suffix

WAVPATH = "./tests/helpers/pure_tone_440hz_1000ms_sf16000.wav\n./tests/helpers/pure_tone_1000hz_1000ms_sf16000.wav"


@pytest.fixture(scope="module")
def sin440():
    t = np.arange(0, 16000) / 16000
    return np.sin(2 * np.pi * 440 * t, dtype=np.float64)


@pytest.fixture(scope="module")
def sin1000():
    t = np.arange(0, 16000) / 16000
    return np.sin(2 * np.pi * 1000 * t, dtype=np.float64)


def test_add_prefix_suffix():
    assert "aspen" == add_prefix_suffix(None, None, None)
    assert "dummy2_dummy1" == add_prefix_suffix("dummy1", "dummy2", None)
    assert "dummy1_dummy3" == add_prefix_suffix("dummy1", None, "dummy3")
    assert "dummy2_dummy1_dummy3" == add_prefix_suffix("dummy1", "dummy2", "dummy3")


# tmp_path is one of the fixture from pytest
def test_wavreader(tmp_path, sin440, sin1000):
    wavlist = tmp_path / "wav.list"
    wavlist.write_text(WAVPATH)
    with WavReader(str(wavlist.resolve())) as reader:
        for key, (sr, orgmat) in reader:
            if key == "pure_tone_440hz_1000ms_sf16000":
                np.testing.assert_allclose(orgmat, sin440, atol=1e-4)
            elif key == "pure_tone_1000hz_1000ms_sf16000":
                np.testing.assert_allclose(orgmat, sin1000, atol=1e-4)
            else:
                pass
    with pytest.raises(ValueError):
        WavReader(str(wavlist.resolve()), segments="dummy")


def test_wavwriter(sin440, sin1000):
    with WavWriter() as writer:
        writer("./dummy1.wav", (16000, sin440))
        writer("./dummy2.wav", (16000, sin1000))
    os.remove("./dummy1.wav")
    os.remove("./dummy2.wav")
    with pytest.raises(ValueError):
        WavWriter(wspecifier="dummy")
    with pytest.raises(ValueError):
        WavWriter(write_function="dummy")


def test_numpyplayer(sin440, sin1000):
    with pytest.raises(ValueError):
        NumpyPlayer(wspecifier="dummy")
    with pytest.raises(ValueError):
        NumpyPlayer(write_function="dummy")
