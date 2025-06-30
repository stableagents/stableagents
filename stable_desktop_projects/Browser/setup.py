#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="browser",
    version="1.0.0",
    description="Lets create a browser that can open up youtube",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0"
    ],
    entry_points={
        'console_scripts': [
            'browser=main:main',
        ],
    },
)
