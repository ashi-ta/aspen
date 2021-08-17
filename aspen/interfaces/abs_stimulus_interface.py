#!/usr/bin/env python3
# encoding: utf-8
"""Abstract stimuli interface"""

from abc import ABC, abstractmethod
from typing import Sequence

import numpy as np


class AbsStimulusInterface(ABC):
    @abstractmethod
    def __call__(self, x: Sequence[np.ndarray]) -> np.ndarray:
        """Transform input multiple signals.

        Args:
            x: Signals (`np.ndarray`).
                x must be sequence-like object such as list, tuple and so on.

        Returns:
            Output signal.
        """
        raise NotImplementedError
