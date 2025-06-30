#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="calculator",
    version="1.0.0",
    description="its a modern calculator with multiple colors and a modern desktop icon",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0"
    ],
    entry_points={
        'console_scripts': [
            'calculator=main:main',
        ],
    },
)
