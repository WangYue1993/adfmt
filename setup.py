#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="adfmt",
    version="0.0.5",
    author="Yue Wang",
    author_email="wangyue930203@gmail.com",
    description="a simple format tool for apiDoc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WangYue1993/adfmt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
