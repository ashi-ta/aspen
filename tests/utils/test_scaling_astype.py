import numpy as np

from aspen.utils.scaling_astype import scaling_astype


def test_scaling_astype():
    x = np.ones(10, dtype=np.float64)
    np.testing.assert_array_equal(np.array([32767] * 10), scaling_astype(x, np.int16))

    x = np.ones(10, dtype=np.int16)
    np.testing.assert_array_equal(
        np.array([1 / 32768] * 10, dtype=np.float64), scaling_astype(x, np.float64)
    )

    x = np.ones(10, dtype=np.float64)
    np.testing.assert_array_equal(
        np.ones(10, dtype=np.float16), scaling_astype(x, np.float16)
    )

    x = np.ones(10, dtype=np.int16)
    val = 2147483647 / 32768
    np.testing.assert_array_equal(
        np.array([val] * 10, dtype=np.int32),
        scaling_astype(x, np.int32),
    )

    x = np.array([1] * 5 + [10] * 5, dtype=np.float64)
    np.testing.assert_array_equal(
        np.array([0.1 * 32767] * 5 + [32767] * 5, dtype=np.int16),
        scaling_astype(x, np.int16),
    )

    x = np.array([1] * 5 + [10] * 5, dtype=np.int16)
    np.testing.assert_array_equal(
        np.array([1 / 32768] * 5 + [10 / 32768] * 5, dtype=np.float64),
        scaling_astype(x, np.float64),
    )

    x = np.array([1] * 5 + [10] * 5, dtype=np.float64)
    np.testing.assert_array_equal(
        np.array([0.1] * 5 + [1] * 5, dtype=np.float16), scaling_astype(x, np.float16)
    )

    x = np.array([1] * 5 + [10] * 5, dtype=np.int16)
    val = 2147483647 / 32768
    np.testing.assert_array_equal(
        np.array([val] * 5 + [val * 10] * 5, dtype=np.int32),
        scaling_astype(x, np.int32),
    )
