# ASPEN | Auditory Stimulus for Psychophysical ExperimeNt

ASPEN is a full python toolkit to generate `Auditory Stimulus for Psychophysical ExperimeNt`.

[**Docs**](https://ashi-ta.github.io/aspen/)
| [**Toolkit Overview**](https://ashi-ta.github.io/aspen/configuration.html#overview-of-toolkit-architecture)
| [**Installation & Usage**](https://ashi-ta.github.io/aspen/getting_started.html)
| [**How To Use**](https://ashi-ta.github.io/aspen/configuration.html#customize-configuration)

## Purpose

- This project aims to
  - create any auditory signal to examine human perception for research
  - mainly focus on stimulus generation itself, not a platform for psychophysical experiment.

## Key Features

- Support multiple auditory stimulus
  - locally time-reversed speech
  - continuity illusion
  - auditory streaming
  - noise-vocoded speech
  - modulation-filtered speech
  - verbal transformation effect
  - iterated rippled noise
- Support multiple fundamental signals
  - pure tone
  - harmonic complex tone
  - amplitude modulated tone
  - frequency modulated tone
  - click train pitch
  - colored noise (white / brown / pink / blue / violet)
  - filtered noise (lowpass / highpass / bandpass / bandstop)
- Support multiple visualization
  - waveform
  - spectrum
  - spectrogram
  - modulation power spectrum

## Installation

```shell
git clone https://github.com/ashi-ta/aspen.git
cd aspen
pip install -e .
```

## Usage

- there are some example scripts and configs
  - `egs/run_*.sh` are example bash scripts
  - `egs/conf` contain example configuration files

```shell
$ cd egs

# generate auditory streaming signals under some conditions
$ ./run_auditory_streaming.sh
```

- More details in [docs](https://ashi-ta.github.io/aspen).

## References

The paper utilized this toolkit is to be published in INTERSPEECH 2021.

```
Takanori Ashihara, Takafumi Moriya, Makio Kashino, "Investigating the Impact of Spectral and Temporal Degradation on End-to-End Automatic Speech Recognition Performance", In Proc. INTERSPEECH, 2021
```
