#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="email",
    version="1.0.0",
    description="Create a simple email app",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.4.0"
    ],
    entry_points={
        'console_scripts': [
            'email=main:main',
        ],
    },
)
