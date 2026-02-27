#!/usr/bin/env python3
"""Setup script for orcatools package."""

from setuptools import setup, find_packages
import os

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="orcatools",
    version="0.5.0",
    author="Gabriel Libânio Silva Rodrigues",
    author_email="",
    description="A Python module to help users run electronic structure calculations with ORCA software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glibaniosr/orcatools",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    scripts=["src/scripts/orca_run.sh"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "py3Dmol",  # For molecular visualization
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
    },
    include_package_data=True,
    zip_safe=False,
)
