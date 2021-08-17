#!/usr/bin/env python3
# encoding: utf-8

import os

wd = os.path.dirname(__file__)
with open(os.path.join(wd, "version.txt"), "r") as f:
    __version__ = f.read().strip()
