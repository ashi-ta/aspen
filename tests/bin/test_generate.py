import argparse

import pytest

from aspen.bin.generate import get_parser, main


def test_get_parser():
    assert isinstance(get_parser(), argparse.ArgumentParser)


def test_main_null_cmd_args():
    with pytest.raises(SystemExit):
        main("")
