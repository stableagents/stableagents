from setuptools import setup, find_packages

setup(
    name="stableagents-ai",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "openai>=1.0.0",
        "anthropic>=0.5.0",
    ],
    entry_points={
        'console_scripts': [
            'stableagents=stableagents.run_cli:main',
            'stableagents-ai=stableagents.run_cli:main',
            'run-stableagents=stableagents.run_cli:main',
        ],
    },
) 