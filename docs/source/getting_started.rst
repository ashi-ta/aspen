.. _getting_started:

###############
Getting Started
###############

************
Installation
************

.. code-block:: bash

  git clone https://github.com/ashi-ta/aspen.git
  cd aspen
  pip install -e .


*****
Usage
*****

You can find some example scripts and configs in `egs <https://github.com/ashi-ta/aspen/blob/main/egs/>`_.

.. _run_example_script:

==================
Run example script
==================

Change directory to the ``egs`` and just run ``*.sh``.
For example, the signals of auditory streaming will be generated in ``data/auditory_streaming`` via the below commands.

.. code-block:: bash

  cd egs
  ./run_auditory_streaming.sh
  ls data/auditory_streaming

.. _run_with_conf:

===========================
Run with configuration file
===========================

In the previous section (see :ref:`run_example_script`), you can find that the scripts work with the command ``generate.py --conf *.conf``.
This basic command can also run with any other configuration files formatted `YAML <http://yaml.org/>`_.
You can find the example YAML files in ``egs/conf`` and also customize it as you want.
For example, the iterated rippled noise (IRN) will be generated in ``data/iterated_rippled_noise`` via the below commands,

.. code-block:: bash

  cd egs
  . ./path.sh
  generate.py --conf conf/iterated_rippled_noise.conf
  ls data/iterated_rippled_noise

or will be played on your device:

.. code-block:: bash

  generate.py --conf conf/iterated_rippled_noise.conf --play


In this case, the IRN will be generated according to the `configuration file <https://github.com/ashi-ta/aspen/blob/main/egs/conf/iterated_rippled_noise.conf>`_:

.. code-block:: yaml
  :caption: iterated_rippled_noise.conf

  # general setting
  stimulus-module: iterated_rippled_noise
  samp-freq: 48000
  outdir: "data/iterated_rippled_noise"
  suffix: iter8_delay1
  
  # sounds setting
  sound-generation-pipeline: [colored_noise]
  colored-noise-color: [white]
  colored-noise-duration: [1000]
  colored-noise-num-signals: 1
  
  # stimulus setting
  num-iteration: 8
  delay: 1
  
  # postprocessings setting
  postprocess-pipeline: [declip, apply_ramp]
  declip-thres: 1
  apply-ramp-duration: 5
  apply-ramp-wfunction: hann
  apply-ramp-position: both
  
  # visualization
  visualization-pipeline: [waveform, spectrogram, spectrum, mps]
  visualization-outdir: "data/iterated_rippled_noise/vis"

The detail on how to configure will appear in the next section (see :ref:`configuration`).
