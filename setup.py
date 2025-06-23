#!/usr/bin/env python3
"""Setup script for stableagents-ai package."""

from setuptools import setup, find_packages
import os

if __name__ == "__main__":
    setup(
        name="stableagents-ai",
        version="0.2.3",
        description="A framework for self healing agents that can run locally and minimize hallucinations",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        author="Jordan Plows",
        author_email="jordan@plows.ai",
        url="https://github.com/jordanplows/stableagents",
        packages=find_packages(),
        install_requires=[
            "requests>=2.28.0",
            "openai>=1.0.0",
            "anthropic>=0.5.0",
            "psutil>=5.9.0",
            "pyppeteer>=1.0.2",
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "cryptography>=3.4.0",
        ],
        extras_require={
            "local": ["llama-cpp-python"],
            "all": ["llama-cpp-python"],
        },
        entry_points={
            "console_scripts": [
                "stableagents-ai=stableagents.run_cli:main",
                "stableagents-api=stableagents.api:app",
                "stableagents-keys=stableagents.cli_key_manager:main",
            ],
        },
        python_requires=">=3.8",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
        include_package_data=True,
        zip_safe=False,
    ) 