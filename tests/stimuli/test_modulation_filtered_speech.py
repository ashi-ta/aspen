import argparse

import numpy as np
import pytest

from aspen.stimuli.modulation_filtered_speech import ModulationFilteredSpeech

PARAMS = [
    (16000, "0_100", "100_200", 1000, 3, 50, False, -1, 20),
    (16000, "100_200", "0_100", 1000, 3, 50, False, -1, 20),
    (16000, "100_200", "100_200", 1000, 4, 50, False, -1, 20),
    (16000, "100_200", "100_200", 1000, 3, 20, False, -1, 20),
    (16000, "100_200", "100_200", 1000, 3, 50, False, -1, 20),
    (16000, "100_200", "100_200", 1000, 3, 50, False, -1, 20),
    (16000, "100_200", "100_200", 1000, 3, 50, True, -1, 20),
    (16000, "100_200", "100_200", 1000, 3, 50, False, 50, 20),
    (16000, "100_200", "100_200", 1000, 3, 50, False, -1, 10),
]


@pytest.fixture(scope="module")
def indata():
    t = np.arange(0, 32000) / 16000
    target = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    return [target]


@pytest.fixture(scope="module")
def default_output():
    t = np.arange(0, 32000) / 16000
    target = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    return ModulationFilteredSpeech()([target])


def test_raise_num_signal_valueerror():
    with pytest.raises(ValueError):
        ModulationFilteredSpeech()([np.ones(10), np.ones(10)])


@pytest.mark.parametrize(
    (
        "samp_freq, temporal_stopbands, spectral_stopbands,"
        "spec_samp_freq, gauss_window_alpha, spacing_freq,"
        "spec_standardize, spec_db_range, griffinlim_iter"
    ),
    PARAMS,
)
def test_not_equal_with_default(
    default_output,
    indata,
    samp_freq,
    temporal_stopbands,
    spectral_stopbands,
    spec_samp_freq,
    gauss_window_alpha,
    spacing_freq,
    spec_standardize,
    spec_db_range,
    griffinlim_iter,
):
    x = indata.copy()
    tone = ModulationFilteredSpeech(
        samp_freq,
        temporal_stopbands,
        spectral_stopbands,
        spec_samp_freq,
        gauss_window_alpha,
        spacing_freq,
        spec_standardize,
        spec_db_range,
        griffinlim_iter,
    )(x)
    assert (tone != default_output).any()


@pytest.mark.parametrize(
    (
        "samp_freq, temporal_stopbands, spectral_stopbands,"
        "spec_samp_freq, gauss_window_alpha, spacing_freq,"
        "spec_standardize, spec_db_range, griffinlim_iter"
    ),
    [
        (32000, "100_200", "100_200", 1000, 3, 50, False, -1, 20),
        (16000, "100_200", "100_200", 800, 3, 50, False, -1, 20),
    ],
)
def test_not_equal_with_default_size(
    default_output,
    indata,
    samp_freq,
    temporal_stopbands,
    spectral_stopbands,
    spec_samp_freq,
    gauss_window_alpha,
    spacing_freq,
    spec_standardize,
    spec_db_range,
    griffinlim_iter,
):
    x = indata.copy()
    tone = ModulationFilteredSpeech(
        samp_freq,
        temporal_stopbands,
        spectral_stopbands,
        spec_samp_freq,
        gauss_window_alpha,
        spacing_freq,
        spec_standardize,
        spec_db_range,
        griffinlim_iter,
    )(x)
    assert tone.shape[0] != default_output.shape[0]


@pytest.mark.parametrize(
    (
        "samp_freq, temporal_stopbands, spectral_stopbands,"
        "spec_samp_freq, gauss_window_alpha, spacing_freq,"
        "spec_standardize, spec_db_range, griffinlim_iter"
    ),
    PARAMS,
)
def test_arguments(
    samp_freq,
    temporal_stopbands,
    spectral_stopbands,
    spec_samp_freq,
    gauss_window_alpha,
    spacing_freq,
    spec_standardize,
    spec_db_range,
    griffinlim_iter,
):
    parser = argparse.ArgumentParser()
    ModulationFilteredSpeech.add_arguments(parser)
    args = parser.parse_args(
        [
            "--temporal-stopbands",
            str(temporal_stopbands),
            "--spectral-stopbands",
            str(spectral_stopbands),
            "--spec-samp-freq",
            str(spec_samp_freq),
            "--gauss-window-alpha",
            str(gauss_window_alpha),
            "--spacing-freq",
            str(spacing_freq),
            "--spec-standardize",
            str(spec_standardize),
            "--spec-db-range",
            str(spec_db_range),
            "--griffinlim-iter",
            str(griffinlim_iter),
        ]
    )
    clsobj = ModulationFilteredSpeech(
        samp_freq=samp_freq,
        temporal_stopbands=args.temporal_stopbands,
        spectral_stopbands=args.spectral_stopbands,
        spec_samp_freq=args.spec_samp_freq,
        gauss_window_alpha=args.gauss_window_alpha,
        spacing_freq=args.spacing_freq,
        spec_standardize=args.spec_standardize,
        spec_db_range=args.spec_db_range,
        griffinlim_iter=args.griffinlim_iter,
    )
    assert clsobj.samp_freq == samp_freq
    assert clsobj.temporal_stopbands == temporal_stopbands
    assert clsobj.spectral_stopbands == spectral_stopbands
    assert clsobj.spec_samp_freq == spec_samp_freq
    assert clsobj.gauss_window_alpha == gauss_window_alpha
    assert clsobj.spacing_freq == spacing_freq
    assert clsobj.spec_standardize == spec_standardize
    assert clsobj.spec_db_range == spec_db_range
    assert clsobj.griffinlim_iter == griffinlim_iter
