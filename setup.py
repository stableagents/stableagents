from setuptools import setup, find_packages

setup(
    name="stableagents",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'stableagents=stableagents.cli:main',
        ],
    },
    install_requires=[
        'tensorflow',
    ],
    python_requires='>=3.6',
    description="StableAgents - A framework for building stable AI agents",
    author="StableAgents Team",
) 