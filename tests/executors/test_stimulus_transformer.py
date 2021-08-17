import argparse

import pytest

from aspen.executors.stimulus_transformer import STIMULI, StimulusTransformer


@pytest.mark.parametrize("stimuli", STIMULI)
@pytest.mark.parametrize("equalize", [True, False])
def test_arguments(stimuli, equalize):
    parser = argparse.ArgumentParser()
    StimulusTransformer.add_arguments(parser)

    cmd_args = [
        "--stimulus-module",
        stimuli,
        "--equalize-inout-duration",
        str(equalize),
    ]
    args, _ = parser.parse_known_args(cmd_args)
    StimulusTransformer.stimulus_add_arguments(parser, args)

    stimulus = StimulusTransformer(args)
    assert stimulus.show_module().__class__.__module__ == "aspen.stimuli." + stimuli
    assert stimulus.equalize == equalize
