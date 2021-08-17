import numpy as np

from aspen.utils.snr_utils import get_snr_noise, rms


def test_rms():
    assert rms(np.ones(10)) == 1.0


def test_get_snr_noise():
    np.testing.assert_array_equal(get_snr_noise(np.ones(10), np.ones(10)), np.ones(10))
    np.testing.assert_array_equal(
        get_snr_noise(np.ones(10), np.ones(10), 0), np.ones(10)
    )
    np.testing.assert_array_equal(
        get_snr_noise(np.ones(10), np.ones(10), 20), np.array([0.1] * 10)
    )
