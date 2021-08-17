import argparse

import numpy as np
import pytest

from aspen.processings.modulation_power_spectrum import (
    ModulationPowerSpectrum,
    modulation_power_spectrum,
)

PARAMS = [
    (500, 3, 50, 0, 8000, True, 50, 100, 0, "librosa", 16000),
    (1000, 5, 50, 0, 8000, True, 50, 100, 0, "librosa", 16000),
    (1000, 3, 100, 0, 8000, True, 50, 100, 0, "librosa", 16000),
    (1000, 3, 50, 100, 8000, True, 50, 100, 0, "librosa", 16000),
    (1000, 3, 50, 0, 6000, True, 50, 100, 0, "librosa", 16000),
    (1000, 3, 50, 0, 8000, False, 20, 100, 0, "librosa", 16000),
    (1000, 3, 50, 0, 8000, True, 50, 150, 0, "librosa", 16000),
    (1000, 3, 50, 0, 8000, True, 50, 100, 50, "librosa", 16000),
]


def assert_not_equal_value_or_shape(x, y):
    if x.shape == y.shape:
        assert (x != y).any()
    else:
        assert True


@pytest.fixture(scope="module")
def sin_data():
    t = np.arange(0, 16000) / 16000
    return np.sin(2 * np.pi * 440 * t, dtype=np.float64)


@pytest.fixture(scope="module")
def default_result():
    t = np.arange(0, 16000) / 16000
    indata = np.sin(2 * np.pi * 440 * t, dtype=np.float64)
    return ModulationPowerSpectrum()(indata)


def test_raise_upper_freq_valueerror(sin_data):
    with pytest.raises(ValueError):
        modulation_power_spectrum(sin_data, upper_freq=9000, samp_freq=16000)
    with pytest.raises(ValueError):
        ModulationPowerSpectrum(
            modulation_power_spectrum_upper_freq=9000, samp_freq=16000
        )(sin_data)


def test_raise_backend_valueerror(sin_data):
    with pytest.raises(ValueError):
        modulation_power_spectrum(sin_data, backend="dummy")
    with pytest.raises(ValueError):
        ModulationPowerSpectrum(modulation_power_spectrum_backend="dummy")(sin_data)


def test_default(sin_data, default_result):
    indata = sin_data.copy()
    out = ModulationPowerSpectrum()(indata)
    np.testing.assert_array_equal(out, default_result)


@pytest.mark.parametrize(
    (
        "spec_samp_freq, gauss_window_alpha, spacing_freq, lower_freq, upper_freq, spec_normalize,"
        "spec_db_range, fft2_win_duration, fft2_win_shift, backend, samp_freq"
    ),
    PARAMS,
)
def test_not_equal_with_default(
    sin_data,
    default_result,
    spec_samp_freq,
    gauss_window_alpha,
    spacing_freq,
    lower_freq,
    upper_freq,
    spec_normalize,
    spec_db_range,
    fft2_win_duration,
    fft2_win_shift,
    backend,
    samp_freq,
):
    indata = sin_data.copy()
    _, _, _, _, out = modulation_power_spectrum(
        indata,
        spec_samp_freq,
        gauss_window_alpha,
        spacing_freq,
        lower_freq,
        upper_freq,
        spec_normalize,
        spec_db_range,
        fft2_win_duration,
        fft2_win_shift,
        backend,
        samp_freq,
    )
    assert_not_equal_value_or_shape(default_result, out)

    indata = sin_data.copy()
    out = ModulationPowerSpectrum(
        spec_samp_freq,
        gauss_window_alpha,
        spacing_freq,
        lower_freq,
        upper_freq,
        spec_normalize,
        spec_db_range,
        fft2_win_duration,
        fft2_win_shift,
        backend,
        samp_freq,
    )(indata)
    assert_not_equal_value_or_shape(default_result, out)


@pytest.mark.parametrize(
    (
        "spec_samp_freq, gauss_window_alpha, spacing_freq, lower_freq, upper_freq, spec_normalize,"
        "spec_db_range, fft2_win_duration, fft2_win_shift, backend, samp_freq"
    ),
    PARAMS,
)
def test_arguments(
    spec_samp_freq,
    gauss_window_alpha,
    spacing_freq,
    lower_freq,
    upper_freq,
    spec_normalize,
    spec_db_range,
    fft2_win_duration,
    fft2_win_shift,
    backend,
    samp_freq,
):
    parser = argparse.ArgumentParser()
    ModulationPowerSpectrum.add_arguments(parser)
    args = parser.parse_args(
        [
            "--modulation-power-spectrum-spec-samp-freq",
            str(spec_samp_freq),
            "--modulation-power-spectrum-gauss-window-alpha",
            str(gauss_window_alpha),
            "--modulation-power-spectrum-spacing-freq",
            str(spacing_freq),
            "--modulation-power-spectrum-lower-freq",
            str(lower_freq),
            "--modulation-power-spectrum-upper-freq",
            str(upper_freq),
            "--modulation-power-spectrum-spec-normalize",
            str(spec_normalize),
            "--modulation-power-spectrum-spec-db-range",
            str(spec_db_range),
            "--modulation-power-spectrum-fft2-win-duration",
            str(fft2_win_duration),
            "--modulation-power-spectrum-fft2-win-shift",
            str(fft2_win_shift),
            "--modulation-power-spectrum-backend",
            str(backend),
        ]
    )
    clsobj = ModulationPowerSpectrum(
        modulation_power_spectrum_spec_samp_freq=args.modulation_power_spectrum_spec_samp_freq,
        modulation_power_spectrum_gauss_window_alpha=args.modulation_power_spectrum_gauss_window_alpha,
        modulation_power_spectrum_spacing_freq=args.modulation_power_spectrum_spacing_freq,
        modulation_power_spectrum_lower_freq=args.modulation_power_spectrum_lower_freq,
        modulation_power_spectrum_upper_freq=args.modulation_power_spectrum_upper_freq,
        modulation_power_spectrum_spec_normalize=args.modulation_power_spectrum_spec_normalize,
        modulation_power_spectrum_spec_db_range=args.modulation_power_spectrum_spec_db_range,
        modulation_power_spectrum_fft2_win_duration=args.modulation_power_spectrum_fft2_win_duration,
        modulation_power_spectrum_fft2_win_shift=args.modulation_power_spectrum_fft2_win_shift,
        modulation_power_spectrum_backend=args.modulation_power_spectrum_backend,
        samp_freq=samp_freq,
    )
    assert clsobj.spec_samp_freq == spec_samp_freq
    assert clsobj.gauss_window_alpha == gauss_window_alpha
    assert clsobj.spacing_freq == spacing_freq
    assert clsobj.lower_freq == lower_freq
    assert clsobj.upper_freq == upper_freq
    assert clsobj.spec_normalize == spec_normalize
    assert clsobj.spec_db_range == spec_db_range
    assert clsobj.fft2_win_duration == fft2_win_duration
    assert clsobj.fft2_win_shift == fft2_win_shift
    assert clsobj.backend == backend
    assert clsobj.samp_freq == samp_freq
