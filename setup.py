#!/usr/bin/env python3

import os

from setuptools import find_packages, setup

wd = os.path.dirname(__file__)
with open(os.path.join(wd, "aspen", "version.txt"), "r") as f:
    version = f.read().strip()
with open(os.path.join(wd, "README.md"), "r", encoding="utf8") as f:
    long_description = f.read()

install_requires = [
    "numpy < 2.0.0",
    "scipy",
    "matplotlib",
    "configargparse",
    "librosa",
    "soundfile",
    "sounddevice",
    "kaldiio",
    "pyyaml",
]

extras_require = {
    "docs": [
        "sphinx",
        "pydata_sphinx_theme",
        "recommonmark",
        "m2r",
        "nbsphinx",
        "pandoc",
        "docutils",
        "sphinxcontrib-fulltoc",
        "sphinxcontrib-mockautodoc",
        "pydata_sphinx_theme",
        "sphinx-autodoc-typehints",
        "sphinx-paramlinks",
        "sphinx-togglebutton",
        "sphinx-copybutton",
        "sphinxcontrib-katex",
    ],
    "tests": ["pytest", "pytest-cov", "flake8", "mypy", "black"],
}

setup(
    name="aspen",
    version=version,
    packages=find_packages(),
    description="ASPEN | Auditory Stimulus and Psycophsical ENvironment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache Software License",
    author="Takanori Ashihara",
    author_email="taka.ashihara.22@gmail.com",
    url="https://github.com/ashi-ta/auditoryillusion",
    keywords="auditory illusion psycophysics signal",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=install_requires,
    extras_require=extras_require,
)
