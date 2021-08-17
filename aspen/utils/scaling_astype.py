#!/usr/bin/env python3
# encoding: utf-8

from typing import Union

import numpy as np
import numpy.typing as npt

from aspen.processings.declip import declip


def scaling_astype(x: np.ndarray, out_dtype: Union[str, npt.DTypeLike]) -> np.ndarray:
    """Numpy astype with scaling.
    Because numeric types have the different value range,
    numpy astype function needs value scaling.
    This function scale the input value to mix-max when out_dtype include np.signedinteger.
    Otherwise, the input value is scaled to from -1 to 1 when out_dtype include np.floating.
    Ref: https://numpy.org/doc/stable/reference/arrays.scalars.html
    Ref: https://numpy.org/doc/stable/user/basics.types.html

    Args:
        x: Input signal.
        out_dtype: Output numpy dtype.

    Returns:
        Output signal.
    """

    if not isinstance(x, np.ndarray):
        raise TypeError("x must be np.ndarray, but got {}".format(type(x)))
    else:
        in_dtype = x.dtype

    cloned = x.copy()
    if in_dtype == out_dtype:
        pass
    elif np.issubdtype(in_dtype, np.floating):
        # if the x has the element > 1.0, declip is applied to scale the output
        cloned = declip(cloned, 1.0)
        # when float -> int, the values are scaled to min-max value of dtype
        if np.issubdtype(out_dtype, np.signedinteger):
            cloned *= np.iinfo(out_dtype).max
    elif np.issubdtype(in_dtype, np.signedinteger):
        # e.g. -32768 <= np.iinfo("int16") <= 32767
        cloned = cloned.astype(np.float64)
        cloned /= np.iinfo(in_dtype).max + 1
        if np.issubdtype(out_dtype, np.signedinteger):
            cloned = cloned * np.iinfo(out_dtype).max
    cloned = cloned.astype(out_dtype)
    return cloned
