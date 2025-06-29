#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="scientific-calculator",
    version="1.0.0",
    description="
        Create a modern scientific calculator with the following features:
        - Basic arithmetic operations (+, -, *, /)
        - Scientific functions (sin, cos, tan, log, sqrt, power)
        - Memory functions (M+, M-, MR, MC)
        - History of calculations
        - Dark mode toggle
        - Responsive design with CustomTkinter
        - Error handling for invalid operations
        - Clear and intuitive user interface
        ",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0"
    ],
    entry_points={
        'console_scripts': [
            'scientific-calculator=main:main',
        ],
    },
)
