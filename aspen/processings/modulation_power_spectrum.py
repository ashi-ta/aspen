#!/usr/bin/env python3
# encoding: utf-8
"""Calculate a modulation power spectrum"""

from logging import getLogger
from typing import Dict, List, Tuple

import librosa
import numpy as np
from scipy import fft, signal

from aspen.interfaces.abs_common_interface import AbsCommonInterface
from aspen.interfaces.abs_processing_interface import AbsProcessingInterface
from aspen.processings.normalize import normalize
from aspen.utils.cli_utils import strtobool

logger = getLogger(__name__)

EPSILON = np.finfo(np.float64).eps


class ModulationPowerSpectrum(AbsCommonInterface, AbsProcessingInterface):
    """Modulation Power Spectrum.

    This class is heavily inspired by soundsig (https://github.com/theunissenlab/soundsig).

    Args:
        modulation_power_spectrum_spec_samp_freq: Sampling frequency in spectrogram space.
            Defaults to 1000.
        modulation_power_spectrum_gauss_window_alpha: The parameter to generate Gaussian window.
            The detail is shown in MATLAB gaussian window method
            (https://www.mathworks.com/help/signal/ref/gausswin.html). Defaults to 3.
        modulation_power_spectrum_spacing_freq: The time-frequency scale for the spectrogram in Hz.
            This variable determines the width of the gaussian window to calculate the SFTF. Defaults to 50.
        modulation_power_spectrum_lower_freq: Lower frequency in the spectrogram to save space.
            Defaults to 0.
        modulation_power_spectrum_upper_freq:
            Upper frequency in the spectrogram to save space. Upper limit is the half of sampling_frequency.
            Defaults to 8000.
        modulation_power_spectrum_spec_normalize:
            The flag of normalizing spectrogram resulted from STFT. Defaults to True.
        modulation_power_spectrum_spec_db_range:
            The range to narrow down the spectrogram amplitude for making it easier to visualize. Defaults to 50.
        modulation_power_spectrum_fft2_win_duration:
            The duration of gaussian window for 2D-FFT in millisecond.
            If the value is 0, fft2 is executed withoud window-shifting. Defaults to 100.
        modulation_power_spectrum_fft2_win_shift:
            The number of points to shift segments for 2D-FFT.
            Defaults is 0 that means `(wduration - 1) // 6` (wduration is fft2_win_duration in sample).
        modulation_power_spectrum_backend: The library to calculate STFT.
            The choices are "librosa" or "scipy". Defaults to "librosa".
        samp_freq: Sampling frequency. Defaults to 16000.
    """

    def __init__(
        self,
        modulation_power_spectrum_spec_samp_freq: int = 1000,
        modulation_power_spectrum_gauss_window_alpha: float = 3,
        modulation_power_spectrum_spacing_freq: float = 50,
        modulation_power_spectrum_lower_freq: float = 0,
        modulation_power_spectrum_upper_freq: float = 8000,
        modulation_power_spectrum_spec_normalize: bool = True,
        modulation_power_spectrum_spec_db_range: float = 50,
        modulation_power_spectrum_fft2_win_duration: float = 100,
        modulation_power_spectrum_fft2_win_shift: int = 0,
        modulation_power_spectrum_backend: str = "librosa",
        samp_freq: int = 16000,
    ):
        self.spec_samp_freq = modulation_power_spectrum_spec_samp_freq
        self.gauss_window_alpha = modulation_power_spectrum_gauss_window_alpha
        self.spacing_freq = modulation_power_spectrum_spacing_freq
        self.lower_freq = modulation_power_spectrum_lower_freq
        self.upper_freq = modulation_power_spectrum_upper_freq
        self.spec_normalize = modulation_power_spectrum_spec_normalize
        self.spec_db_range = modulation_power_spectrum_spec_db_range
        self.fft2_win_duration = modulation_power_spectrum_fft2_win_duration
        self.fft2_win_shift = modulation_power_spectrum_fft2_win_shift
        self.backend = modulation_power_spectrum_backend
        self.samp_freq = samp_freq

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group("modulation-powre-spectrum setting")
        group.add_argument(
            "--modulation-power-spectrum-spec-samp-freq",
            default=1000,
            type=int,
            help="Duration of ramp in millisecond",
        )
        group.add_argument(
            "--modulation-power-spectrum-gauss-window-alpha",
            default=3,
            type=float,
            help="Window function of ramp",
        )
        group.add_argument(
            "--modulation-power-spectrum-spacing-freq",
            default=50,
            type=float,
            help="Position of ramp",
        )
        group.add_argument(
            "--modulation-power-spectrum-lower-freq",
            default=0,
            type=float,
            help="Position of ramp",
        )
        group.add_argument(
            "--modulation-power-spectrum-upper-freq",
            default=8000,
            type=float,
            help="Position of ramp",
        )
        group.add_argument(
            "--modulation-power-spectrum-spec-normalize",
            default=True,
            type=strtobool,
            help="Position of ramp",
        )
        group.add_argument(
            "--modulation-power-spectrum-spec-db-range",
            default=50,
            type=float,
            help="Position of ramp",
        )
        group.add_argument(
            "--modulation-power-spectrum-fft2-win-duration",
            default=100,
            type=float,
            help="Position of ramp",
        )
        group.add_argument(
            "--modulation-power-spectrum-fft2-win-shift",
            default=None,
            type=int,
            help="Position of ramp",
        )
        group.add_argument(
            "--modulation-power-spectrum-backend",
            default="librosa",
            choices=["librosa", "scipy"],
            type=str,
            help="Position of ramp",
        )

        return parser

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Calculate modulation power spectrum

        Args:
            x: Input signal

        Returns:
            Return the modulation power spectrum.
        """

        if self.upper_freq > self.samp_freq / 2:
            raise ValueError(
                "upper_freq must be the Nyquist frequency (the half of sampling frequency)"
            )
        # duration of window is in proportion to the std and
        # in inverse proportion to the frequency resoluton of spectrogram
        wduration = int(
            (2 * self.gauss_window_alpha)
            / (2 * np.pi * self.spacing_freq)
            * self.samp_freq
        )
        wduration = wduration + 1 if wduration % 2 == 0 else wduration
        # so that the window shape is invariant with respect to window duration
        win_std = wduration / (2 * self.gauss_window_alpha)
        win_shift = int(np.around(self.samp_freq / self.spec_samp_freq))
        window = ("gaussian", win_std)
        # calculate the spectrogram with gaussian window
        if self.backend == "librosa":
            spec = librosa.stft(
                x,
                n_fft=wduration,
                hop_length=win_shift,
                win_length=wduration,
                window=window,
                center=True,
                pad_mode="constant",
            )
            spec_f = librosa.fft_frequencies(sr=self.samp_freq, n_fft=wduration)
            spec_t = librosa.core.frames_to_time(
                np.arange(spec.shape[1]), sr=self.samp_freq, hop_length=win_shift
            )
            stft_param = {"n_fft": wduration, "hop_length": win_shift, "window": window}
        elif self.backend == "scipy":
            noverlap = wduration - win_shift
            spec_f, spec_t, spec = signal.stft(
                x,
                self.samp_freq,
                window=window,
                nperseg=wduration,
                noverlap=noverlap,
                detrend=False,
                return_onesided=True,
                boundary="zeros",
                padded=False,
            )
            stft_param = {"window": window, "nperseg": wduration, "noverlap": noverlap}
        else:
            raise ValueError("Invalid backend")
        spec = np.abs(
            spec[(spec_f >= self.lower_freq) & (spec_f <= self.upper_freq), :]
        )
        # avoid to be divided by zero
        spec = np.where(spec == 0, EPSILON, spec)
        spec = 20 * np.log10(spec)  # log (dB) scale
        spec_f_size = spec.shape[0]
        spec_t_size = spec.shape[1]

        # rescale the processing range of the amplitude
        # within lower_amp and spec.max (spec.max - lower_amp = spec_db_range) and normalize
        if self.spec_db_range > 0:
            lower_amp = spec.max() - self.spec_db_range
            spec[spec < lower_amp] = lower_amp
        if self.spec_normalize:
            spec = normalize(spec, "zscore")

        # fft2 w/o window-shifting
        # is easy to calculate the inverse 2D-FFT so that generate modulation filtering signal
        if self.fft2_win_duration == 0:
            logger.info("2D-FFT is executed without window shifting")
            mps = fft.fft2(spec)
            mps_pow = np.abs(mps) ** 2
            mps_f = fft.fftfreq(
                spec_f_size, spec_f[1] - spec_f[0]
            )  # d is the sample spacing
            mps_t = fft.fftfreq(
                spec_t_size, spec_t[1] - spec_t[0]
            )  # d is the sample spacing

        # fft2 w/ window-shifting (like a 2D-STFT)
        # can deal with the distinction between positive and negative temporal modulated frequency
        else:
            logger.info("2D-FFT is executed with window shifting")
            # find the number of samples which can be include the size of window from spectrogram segment time
            wduration = np.where(spec_t >= self.fft2_win_duration / 1000)[0][0]
            wduration = int((wduration + 1) if wduration % 2 == 0 else wduration)
            half_wduration = (wduration - 1) // 2
            win_std = wduration / (2 * self.gauss_window_alpha)
            # signal.windows.gaussian is not multiplied by coefficient in comparison with the reference below.
            # https://github.com/theunissenlab/soundsig/blob/8efaa51f548689ed30370597e37c736a66a61e2a/soundsig/signal.py#L189
            # the multiplied coefficient (1/(sigma*sqrt(2*pi))) is required for a probability density distribution,
            # not for a window
            window = signal.windows.gaussian(wduration, win_std)
            window = np.tile(window, [spec_f_size, 1])
            if self.fft2_win_shift == 0:
                self.fft2_win_shift = int((wduration - 1) // 6)
            # pad with minimum value at the beggining and end of the spectrogram
            padded_spec = np.pad(
                spec,
                [[0], [half_wduration]],
                mode="constant",
                constant_values=spec.min(),
            )
            # padded_spec = np.ones([spec_f_size, half_wduration]) * spec.min()
            # padded_spec = np.concatenate([padded_spec, spec, padded_spec], axis=1)

            fft2_step = list(
                range(half_wduration, spec_t_size + 1, self.fft2_win_shift)
            )
            mps = []
            mps_pow = np.zeros([spec_f_size, wduration])
            for i, wcenter in enumerate(fft2_step):
                cloned = padded_spec.copy()
                wonset = wcenter - half_wduration
                woffset = wcenter + half_wduration + 1
                cloned = cloned[:, wonset:woffset] * window
                mps.append(fft.fft2(cloned))
                mps_pow += np.abs(mps[i]) ** 2

            mps_pow /= len(fft2_step)
            mps_f = fft.fftfreq(
                spec_f_size, spec_f[1] - spec_f[0]
            )  # d is the sample spacing
            mps_t = fft.fftfreq(
                wduration, spec_t[1] - spec_t[0]
            )  # d is the sample spacing

        self.stft_param = stft_param
        self.mps_f = mps_f
        self.mps_t = mps_t
        self.mps = mps

        return mps_pow

    def stft_parameters(self) -> Dict:
        """Return the pameters for short-time Fourier transform.

        Returns:
            the pameters for short-time Fourier transform.
        """
        if not hasattr(self, "stft_param"):
            raise NameError("should run class method of __call__ first.")
        return self.stft_param

    def spectral_modulation_freq(self) -> np.ndarray:
        """Return the modulation power spectrum sample spectral modulation frequency.

        Returns:
            the modulation power spectrum sample spectral modulation frequency.
        """
        if not hasattr(self, "mps_f"):
            raise NameError("should run class method of __call__ first.")
        return self.mps_f

    def temporal_modulation_freq(self) -> np.ndarray:
        """Return the modulation power spectrum sample temporal modulation frequency.

        Returns:
            the modulation power spectrum sample temporal modulation frequency.
        """
        if not hasattr(self, "mps_t"):
            raise NameError("should run class method of __call__ first.")
        return self.mps_t

    def raw_mps(self) -> List:
        """Return the listed result of 2-D discrete Fourier transform.

        Returns:
            the listed result of 2-D discrete Fourier transform.
        """
        if not hasattr(self, "mps"):
            raise NameError("should run class method of __call__ first.")
        return self.mps


def modulation_power_spectrum(
    x: np.ndarray,
    spec_samp_freq: int = 1000,
    gauss_window_alpha: float = 3,
    spacing_freq: float = 50,
    lower_freq: float = 0,
    upper_freq: float = 8000,
    spec_normalize: bool = True,
    spec_db_range: float = 50,
    fft2_win_duration: float = 100,
    fft2_win_shift: int = 0,
    backend: str = "librosa",
    samp_freq: int = 16000,
) -> Tuple[Dict, np.ndarray, np.ndarray, List, np.ndarray]:
    """Modulation Power Spectrum.

    This method is heavily inspired by soundsig (https://github.com/theunissenlab/soundsig).

    Args:
        x: Input signal
        spec_samp_freq: Sampling frequency in spectrogram space.
            Defaults to 1000.
        gauss_window_alpha: The parameter to generate Gaussian window.
            The detail is shown in MATLAB gaussian window method
            (https://www.mathworks.com/help/signal/ref/gausswin.html). Defaults to 3.
        spacing_freq: The time-frequency scale for the spectrogram in Hz.
            This variable determines the width of the gaussian window to calculate the SFTF. Defaults to 50.
        lower_freq: Lower frequency in the spectrogram to save space.
            Defaults to 0.
        upper_freq:
            Upper frequency in the spectrogram to save space. Upper limit is the half of sampling_frequency.
            Defaults to 8000.
        spec_normalize:
            The flag of normalizing spectrogram resulted from STFT. Defaults to True.
        spec_db_range:
            The range to narrow down the spectrogram amplitude for making it easier to visualize. Defaults to 50.
        fft2_win_duration:
            The duration of gaussian window for 2D-FFT in millisecond.
            If the value is 0, fft2 is executed withoud window-shifting. Defaults to 100.
        fft2_win_shift:
            The number of points to shift segments for 2D-FFT.
            Defaults is 0 that means `(wduration - 1) // 6` (wduration is fft2_win_duration in sample).
        backend: The library to calculate STFT.
            The choices are "librosa" or "scipy". Defaults to "librosa".
        samp_freq: Sampling frequency. Defaults to 16000.

    Returns:
        Return the pameters for short-time Fourier transform,
        the modulation power spectrum sample spectral modulation frequency,
        the modulation power spectrum sample temporal modulation frequency,
        the listed result of 2-D discrete Fourier transform and
        the modulation power spectrum.
    """

    mps = ModulationPowerSpectrum(
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
    mps_pow = mps(x)
    return (
        mps.stft_parameters(),
        mps.spectral_modulation_freq(),
        mps.temporal_modulation_freq(),
        mps.raw_mps(),
        mps_pow,
    )
