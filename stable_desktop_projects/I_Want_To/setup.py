#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="i-want-to",
    version="1.0.0",
    description="I want to create a simple calculator app",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0"
    ],
    entry_points={
        'console_scripts': [
            'i-want-to=main:main',
        ],
    },
)
