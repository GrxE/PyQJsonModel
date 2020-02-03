# -*- coding: utf-8 -*-
# Copyright Gregor Engberding

"""
    Installs the PyQtJsonModel

"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyQtJsonModel",
    version="0.0.2",
    author="Gregor Engberding",
    author_email="gregor@rabotix.de",
    description="Model for a QTreeView with JSON/dict data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrxE/PyQtJsonModel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: (c) 2020 by Gregor Engberding, MIT-License",
        "Operating System :: OS Independent",
        ],

    install_requires=[
        "PySide2",
        ],
    )
