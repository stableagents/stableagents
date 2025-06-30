#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="web-browser",
    version="1.0.0",
    description="I want to create a new type of browser",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.4.0"
    ],
    entry_points={
        'console_scripts': [
            'web-browser=main:main',
        ],
    },
)
