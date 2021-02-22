#!/usr/bin/env python

"""
Install Records package. 
Call `pip install -e .` to install package locally for testing.
"""

from setuptools import setup

# build command
setup(
    name="records",
    version="0.0.1",
    description="A package for extracting GBIF data",
    classifiers=["Programming Language :: Python :: 3"],
    install_requires=[
    	"pandas",
    	"requests",
    	"json",
    ],
)
