#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="calculator",
    version="1.0.0",
    description="Create a modern calculator with scientific functions, dark mode, and history",
    packages=find_packages(),
    install_requires=[
        "# tkinter is included with Python"
    ],
    entry_points={
        'console_scripts': [
            'calculator=main:main',
        ],
    },
)
