import argparse

from aspen.executors.sound_generator import SOUNDS, SoundGenerator


def test_arguments():
    parser = argparse.ArgumentParser()
    SoundGenerator.add_arguments(parser)

    cmd_args = ["--sound-generation-pipeline"] + SOUNDS
    args, _ = parser.parse_known_args(cmd_args)
    SoundGenerator.sound_add_arguments(parser, args)

    sounds = SoundGenerator(args)
    pipeline = sounds.show_pipeline()
    assert len(pipeline) == len(SOUNDS)
    pipeline_module = [i.__class__.__module__.split(".")[-1] for i in pipeline]
    assert pipeline_module == SOUNDS
