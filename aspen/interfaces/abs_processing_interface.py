#!/usr/bin/env python3
# encoding: utf-8
"""Abstract processing interface"""

from abc import ABC, abstractmethod

import numpy as np


class AbsProcessingInterface(ABC):
    @abstractmethod
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Transform input multiple signals.

        Args:
            x: Signals (`np.ndarray`).

        Returns:
            Output signal.
        """
        raise NotImplementedError
