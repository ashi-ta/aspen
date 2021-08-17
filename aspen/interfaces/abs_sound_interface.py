#!/usr/bin/env python3
# encoding: utf-8
"""Abstract sound interface"""

from abc import ABC, abstractmethod
from typing import List

import numpy as np

NUM_SIGNALS = 1


class AbsSoundInterface(ABC):
    def __init__(self):
        self.num_signals = NUM_SIGNALS

    def __call__(self) -> List[np.ndarray]:
        """Generate a specified number of signals.

        Returns:
            Generate signals.
                Output well be sequence-like object such as list, tuple and so on.
        """
        x = []
        for i in range(self.num_signals):
            x.append(self._generate_each(i))
        return x

    @abstractmethod
    def _generate_each(self, idx: int) -> np.ndarray:
        """Generate each signal.

        Args:
            idx: Index of signal generation.

        Returns:
            Generate signal.
        """
        raise NotImplementedError
