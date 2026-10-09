"""
setup.py - TaskPaper CLI Installation Script

This script is used to package and install the TaskPaper CLI tool
using setuptools. It defines the package, installation requirements, 
and entry point for the installation.

Usage:
    - To install ("cd" to where .whl file is) "pipx install xxx.whl"
    - To install (in development mode) "pipx install --editable ."
    - To build a distribution package: "python3 setup.py sdist bdist_wheel"

Author: Yamin Ohmar
University: University of Leicester
"""

from setuptools import setup, find_packages

setup(
    name="taskpaper-cli",
    version="1.0.0",    # official release V1.0.0
    packages=find_packages(where="src"),  # to find packages inside 'src' folder
    package_dir={"": "src"},  # to map package discovery to 'src' directory
    entry_points={
        "console_scripts": [
            "TaskPaper=cli.main:main"  # to register 'TaskPaper' as a CLI command
        ]
    },
    python_requires=">=3.10",
    install_requires=[
        "termcolor",  # to get this installed automatically
        "tabulate",  # to get this installed automatically
    ],
)
