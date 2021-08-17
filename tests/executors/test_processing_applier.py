import argparse

from aspen.executors.processing_applier import PROCESSINGS, ProcessingApplier


def test_arguments():
    parser = argparse.ArgumentParser()
    ProcessingApplier.add_arguments(parser)

    cmd_args = (
        ["--postprocess-pipeline"]
        + PROCESSINGS
        + ["--filter-signal-btype", "lowpass", "--filter-signal-filter-freq", "500"]
    )
    args, _ = parser.parse_known_args(cmd_args)
    ProcessingApplier.processing_add_arguments(parser, args)
    args = parser.parse_args(cmd_args)

    postprocessings = ProcessingApplier(args)
    pipeline = postprocessings.show_pipeline()
    assert len(pipeline) == len(PROCESSINGS)
    pipeline_module = [i.__class__.__module__.split(".")[-1] for i in pipeline]
    assert pipeline_module == PROCESSINGS
