#!/usr/bin/env python3
# encoding: utf-8
"""Abstract common interface"""

import argparse
import inspect
from abc import ABC


class AbsCommonInterface(ABC):
    def __init__(self):
        raise RuntimeError("This class can't be instantiated.")

    @staticmethod
    def add_arguments(parser):
        """add arguments"""
        return parser

    @classmethod
    def load_class_kwargs(cls, args: argparse.Namespace) -> dict:
        """Return the kwargs dict for class `__init__` from parsed arguments

        Args:
            args: (config)argparse arguments

        Returns:
            kwargs for class `__init__`
        """
        d = dict(inspect.signature(cls.__init__).parameters)
        kwargs = {}
        for k, v in d.items():
            if k == "self":
                continue
            elif hasattr(args, k):
                kwargs[k] = getattr(args, k)
            elif v.default != inspect.Parameter.empty:
                kwargs[k] = v.default
            else:
                raise ValueError(
                    "could not find the argv '{}' to instantiate '{}'".format(
                        k, cls.__name__
                    )
                )
        return kwargs
