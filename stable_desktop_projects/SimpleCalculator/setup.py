#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="simplecalculator",
    version="1.0.0",
    description="
        Create a simple calculator application with:
        - Modern UI with dark/light mode toggle
        - Basic arithmetic operations (add, subtract, multiply, divide)
        - Clear and equals buttons
        - Number display
        - Responsive design
        ",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0"
    ],
    entry_points={
        'console_scripts': [
            'simplecalculator=main:main',
        ],
    },
)
