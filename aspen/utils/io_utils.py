#!/usr/bin/env python3
# encoding: utf-8

import os
from typing import Optional

import librosa
import numpy as np
import sounddevice as sd
import soundfile as sf


def add_prefix_suffix(basedname: Optional[str], prefix: Optional[str] = None, suffix: Optional[str] = None) -> str:
    """add `prefix` and `suffix` to input string with hyphens

    Args:
        basedname: input string
        prefix: Defaults to None (= without adding the prefix).
        suffix: Defaults to None (= without adding the suffix).

    Returns:
        `prefix`_`basename`_`suffix`
    """
    if basedname is None and prefix is None and suffix is None:
        return "aspen"
    outname = basedname if basedname is not None else ""
    outname = prefix + "_" + outname if prefix is not None else outname
    outname = outname + "_" + suffix if suffix is not None else outname
    outname = outname.rstrip("_").lstrip("_")
    return outname


class WavReader(object):
    def __init__(self, wav_list, segments=None):
        if segments is not None:
            raise ValueError("Not supported to use segments. Use kaldiio instead.")
        self.initialized = False
        self.closed = False
        self.dummy = False
        if wav_list is None:
            self.dummy = True
        else:
            self.file = open(wav_list, "r")
        self.initialized = True

    def __iter__(self):
        if self.dummy:
            # dummy generator (iterate only one time for generation method)
            yield None, (None, None)
        else:
            with self.file as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue
                    try:
                        k = os.path.splitext(os.path.basename(line))[0]
                        v, sr = librosa.load(line, sr=None, dtype=np.float64)
                    except Exception:
                        raise
                    yield k, (sr, v)
            self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.dummy and not self.closed:
            self.close()

    def close(self):
        if self.initialized and not self.dummy and not self.closed:
            self.file.close()
            self.closed = True


class WavWriter(object):
    def __init__(self, wspecifier=None, write_function=None):
        if wspecifier is not None:
            raise ValueError("Not supported to use wspecifier. Use kaldiio instead.")
        if write_function is not None:
            raise ValueError("Not supported to use write_function. Use kaldiio instead.")
        self.initialized = True
        self.closed = False

    def __call__(self, key, array):
        # array = (sr, x)
        if self.closed:
            raise RuntimeError("WavWriter has been already closed")
        # (TODO) subtype argument
        sf.write(key, array[1], array[0], subtype="PCM_16", format="WAV")

    def __setitem__(self, key, value):
        self(key, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closed = True


class NumpyPlayer(object):
    def __init__(self, wspecifier=None, write_function=None):
        if wspecifier is not None:
            raise ValueError("Not supported to use wspecifier. Use kaldiio instead.")
        if write_function is not None:
            raise ValueError("Not supported to use write_function. Use kaldiio instead.")
        self.initialized = True
        self.closed = False

    def __call__(self, key, array):
        # array = (sr, x)
        if self.closed:
            raise RuntimeError("NumpyPlayer has been already closed")
        try:
            sd.play(array[1], array[0])
        except Exception:
            raise
        sd.wait()

    def __setitem__(self, key, value):
        self(key, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sd.stop()
        self.closed = True
