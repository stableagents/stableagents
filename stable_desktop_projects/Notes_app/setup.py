#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="notes-app",
    version="1.0.0",
    description="Create a sleek and modern notes app",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0"
    ],
    entry_points={
        'console_scripts': [
            'notes-app=main:main',
        ],
    },
)
